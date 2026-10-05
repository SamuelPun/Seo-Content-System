"""
Workflow step runners. Each step_* function receives a RunContext and article slug.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from seo_system.runner import print_status, run_claude_skill, run_script
from seo_system.workspace import (
    completed_substeps,
    load_log,
    mark_substep_complete,
    reset_substeps,
    save_log,
    workspace,
)


@dataclass
class RunContext:
    content_dir: Path
    brand_dir: Path
    market: str = "us"
    keyword: str | None = None  # supplied once via --keyword; skips the interactive prompt
    seed: str | None = None  # --seed: your angle/headline idea, skips the interactive prompt
    force: bool = False


@dataclass
class StepResult:
    """What a step_* function actually reports, distinct from whether its subprocess
    chain merely exited 0. 'complete' is the only status that gets mark_complete()'d
    and lets a re-run skip the step — 'needs_human' means the step ran fine but its
    own success criteria weren't met (e.g. the Editor still hasn't approved after the
    one revision pass) and a human has to look, not the code silently calling it done.
    'usage_limit' means a Claude session hit a usage/rate limit — a plain re-run of
    the same command resumes at the same checkpoint once the limit resets, nothing
    was lost."""
    status: str  # "complete" | "needs_human" | "failed" | "usage_limit"
    message: str = ""

    @property
    def ok(self) -> bool:
        return self.status == "complete"


def _skill_failure(result) -> "StepResult":
    """Turn a non-ok SkillRunResult into the matching StepResult status."""
    status = "usage_limit" if result.status == "usage_limit" else "failed"
    return StepResult(status, result.message)


def _prompt(msg: str) -> str:
    """input() that degrades to '' instead of crashing when there's no TTY (e.g. run headlessly)."""
    try:
        return input(msg).strip()
    except EOFError:
        return ""


def get_keyword(ctx: RunContext, article: str) -> str:
    """Read keyword from ctx.keyword override, log.json, or prompt (once) if neither is set."""
    log = load_log(ctx.content_dir, article)
    kw = (ctx.keyword or log.get("keyword", "")).strip()
    if not kw:
        label = log.get("display_name", article)
        print()
        try:
            kw = input(f"  Enter the target keyword for '{label}': ").strip()
        except EOFError:
            print_status("No keyword set and no input available — pass --keyword", "error")
            raise SystemExit(1)
    if kw != log.get("keyword", "").strip():
        log["keyword"] = kw
        save_log(ctx.content_dir, article, log)
    return kw


def step_keyword(ctx: RunContext, article: str) -> StepResult:
    ws = workspace(ctx.content_dir, article)
    kw = get_keyword(ctx, article)

    data_dir = ws / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    serp_out = data_dir / "serp-urls.json"
    serp_pages_dir = data_dir / "serp-pages"
    serp_pages_dir.mkdir(parents=True, exist_ok=True)

    ok = run_script("fetch_serp.py", ["--keyword", kw, "--country", ctx.market, "--out-dir", str(data_dir)])
    if not ok:
        return StepResult("failed", "fetch_serp.py failed")

    if not serp_out.exists():
        print_status("serp-urls.json not found — cannot fetch SERP pages", "error")
        return StepResult("failed", "serp-urls.json not found")

    # Batch mode (not a loop of single-URL calls): one subprocess, and it applies the
    # polite inter-request delay between competitor sites that a loop here would skip.
    ok = run_script("fetch_url.py", [
        "--urls",    str(serp_out),
        "--out-dir", str(serp_pages_dir),
    ])
    if not ok:
        print_status("fetch_url had failures — continuing with partial SERP data", "error")

    ok = run_script("summarise_serp_pages.py", [
        "--serp-pages-dir", str(serp_pages_dir),
        "--out-dir",        str(data_dir),
    ])
    if not ok:
        print_status("summarise_serp_pages failed — serp-summaries.json not created", "error")
        return StepResult("failed", "summarise_serp_pages.py failed")

    return StepResult("complete")


def _read_editor_verdict(ws: Path) -> bool | None:
    """Read editorial/editor-verdict.json. Returns the approved bool, or None if missing/invalid."""
    verdict_path = ws / "editorial" / "editor-verdict.json"
    if not verdict_path.exists():
        return None
    try:
        data = json.loads(verdict_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if "approved" not in data:
        return None
    return bool(data["approved"])


# (checkpoint name, skill file, takes the seed, expected output files) — order matters,
# each is a separate Claude session. Expected files are relative to editorial/.
_ANGLE_SUBSTEPS = [
    ("angle-seo-research", "angle-seo-research.md", True, ("research-brief.md",)),
    ("angle-writer-draft", "angle-writer-draft.md", True, ("angle.md",)),
    ("angle-reader-check", "angle-reader-check.md", False, ("reader-feedback.md",)),
    ("angle-editor-review", "angle-editor-review.md", False, ("editor-verdict.json",)),
]

_OUTLINE_SUBSTEPS = [
    ("outline-writer-draft", "outline-writer-draft.md", True, ("headline.md", "outline.md")),
    ("outline-editor-review", "outline-editor-review.md", False, ("editor-verdict.json",)),
    ("outline-reader-check", "outline-reader-check.md", False, ("reader-feedback.md",)),
]


def _run_substeps(ctx: RunContext, article: str, step: str, substeps: list, draft_name: str,
                   revise_name: str, revise_skill: str, seed_prompt: str) -> StepResult:
    """Run a multi-role stage, checkpointing after each role so a re-run resumes at the next
    unfinished one instead of redoing the whole stage."""
    ws = workspace(ctx.content_dir, article)
    if ctx.force:
        reset_substeps(ctx.content_dir, article, step)
    done = completed_substeps(ctx.content_dir, article, step)

    seed = ctx.seed
    if not seed and draft_name not in done:
        print()
        seed = _prompt(seed_prompt) or None

    for name, skill_file, uses_seed, expected_files in substeps:
        if name in done:
            continue
        skill_result = run_claude_skill(skill_file, ws, ctx.brand_dir, seed=seed if uses_seed else None)
        if not skill_result.ok:
            return _skill_failure(skill_result)
        missing = [f for f in expected_files if not (ws / "editorial" / f).exists()]
        if missing:
            print_status(f"{name} finished but didn't write {', '.join(missing)} — not marking complete", "error")
            return StepResult("failed", f"{name} didn't write {', '.join(missing)}")
        mark_substep_complete(ctx.content_dir, article, step, name)

    approved = _read_editor_verdict(ws)
    if approved is None:
        print_status(f"editor-verdict.json missing or invalid after {step} review", "error")
        return StepResult("failed", f"editor-verdict.json missing or invalid after {step} review")

    if not approved and revise_name not in done:
        print_status("Editor requested a revision — running one revision pass", "info")
        skill_result = run_claude_skill(revise_skill, ws, ctx.brand_dir)
        if not skill_result.ok:
            return _skill_failure(skill_result)
        mark_substep_complete(ctx.content_dir, article, step, revise_name)
        # Re-read: the whole point of the revision pass is to earn approval. Don't take
        # it on faith — a still-rejected draft after the one revision must not be marked
        # complete (that's the bug that let a silently-abandoned angle slip through on
        # teapot-hong-kong: the step exited 0 and log.json said "complete" regardless of
        # what editor-verdict.json actually said).
        approved = _read_editor_verdict(ws)

    if not approved:
        return StepResult(
            "needs_human",
            f"Editor still hasn't approved {step} after the revision pass — "
            f"read editorial/editor-verdict.json and the draft, then either fix it "
            f"by hand or re-run with --force to redo the stage.",
        )

    return StepResult("complete")


def step_angle(ctx: RunContext, article: str) -> StepResult:
    """Angle stage — SEO Manager, Writer, Reader Advocate, Editor as separate Claude sessions."""
    return _run_substeps(
        ctx, article, "angle", _ANGLE_SUBSTEPS,
        draft_name="angle-writer-draft",
        revise_name="angle-writer-revise", revise_skill="angle-writer-revise.md",
        seed_prompt="  Your angle idea (Enter to let Claude analyse the SERP freely): ",
    )


def step_headline_outline(ctx: RunContext, article: str) -> StepResult:
    """Outline stage — Writer, Editor, Reader Advocate as separate Claude sessions."""
    return _run_substeps(
        ctx, article, "headline-outline", _OUTLINE_SUBSTEPS,
        draft_name="outline-writer-draft",
        revise_name="outline-writer-revise", revise_skill="outline-writer-revise.md",
        seed_prompt="  Your headline idea (Enter for Claude's options): ",
    )


def step_research(ctx: RunContext, article: str) -> StepResult:
    ws = workspace(ctx.content_dir, article)
    sources_dir = ws / "data" / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    skill_result = run_claude_skill("research-authority.md", ws, ctx.brand_dir)
    if not skill_result.ok:
        return _skill_failure(skill_result)

    index_path = sources_dir / "index.json"
    if not index_path.exists():
        print_status("Claude exited cleanly but data/sources/index.json was not written — research produced nothing", "error")
        return StepResult("failed", "data/sources/index.json was not written")

    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
        sources = index.get("sources", [])
        if not sources:
            print_status("data/sources/index.json exists but contains no sources — research produced nothing", "error")
            return StepResult("failed", "index.json contains no sources")

        missing = [s["id"] for s in sources if not (sources_dir / f"{s['id']}.md").exists()]
        if missing:
            print_status(f"index.json lists sources with no matching file: {', '.join(missing)}", "error")
            return StepResult("failed", f"index.json lists sources with no matching file: {', '.join(missing)}")

        print_status(f"sources verified: {len(sources)} source(s) in index, all files present", "ok")
    except (json.JSONDecodeError, Exception) as e:
        print_status(f"data/sources/index.json is not valid JSON: {e}", "error")
        return StepResult("failed", f"data/sources/index.json is not valid JSON: {e}")

    return StepResult("complete")


def _validate_banned_phrases(ws: Path, data_dir: Path) -> bool:
    """Hard gate: run scan_banned_phrases and fail if any HIGH severity flags remain."""
    draft = ws / "editorial" / "draft.md"
    if not draft.exists():
        print_status("draft.md not found — cannot validate banned phrases", "error")
        return False

    ok = run_script("scan_banned_phrases.py", ["--draft", str(draft), "--out-dir", str(data_dir)])
    if not ok:
        print_status("scan_banned_phrases failed", "error")
        return False

    flags_path = data_dir / "audit-flags.json"
    if not flags_path.exists():
        return True

    try:
        flags_data = json.loads(flags_path.read_text(encoding="utf-8"))
        flags = flags_data if isinstance(flags_data, list) else flags_data.get("flags", [])
        high = [f for f in flags if f.get("severity") == "HIGH"]
        if high:
            lines = "\n".join(
                f"  Line {f.get('line_number', f.get('line', '?'))}: {f.get('phrase', '?')!r}"
                for f in high
            )
            print_status(
                f"{len(high)} HIGH severity violation(s) in draft — fix before continuing:\n{lines}",
                "error",
            )
            return False
    except (json.JSONDecodeError, KeyError):
        pass

    return True


def _seed_publisher_meta(ctx: RunContext, data_dir: Path, article: str) -> None:
    profile = ctx.brand_dir.parent / "profile.md"
    if not profile.exists():
        return
    text = profile.read_text(encoding="utf-8")
    name_m = re.search(r'\*\*Client name:\*\*\s*(.+)', text)
    url_m  = re.search(r'\*\*Website:\*\*\s*(\S+)', text)
    if not (name_m and url_m):
        return
    meta_path = data_dir / "meta.json"
    existing = {}
    if meta_path.exists():
        try:
            existing = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    site_url = url_m.group(1).strip().rstrip("/")
    existing["publisher_name"] = name_m.group(1).strip()
    existing["site_url"] = site_url
    if not existing.get("url"):
        existing["url"] = f"{site_url}/blog/{article}/"
    meta_path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")


def step_writing(ctx: RunContext, article: str) -> StepResult:
    ws = workspace(ctx.content_dir, article)
    data_dir = ws / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    skill_result = run_claude_skill("writing.md", ws, ctx.brand_dir)
    if not skill_result.ok:
        return _skill_failure(skill_result)
    if not _validate_banned_phrases(ws, data_dir):
        return StepResult("failed", "banned-phrase gate failed — see audit-flags.json")
    return StepResult("complete")


def step_polish(ctx: RunContext, article: str) -> StepResult:
    ws = workspace(ctx.content_dir, article)
    draft = ws / "editorial" / "draft.md"
    data_dir = ws / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    if not draft.exists():
        print_status("editorial/draft.md not found — run 'writing' step first", "error")
        return StepResult("failed", "editorial/draft.md not found")

    ok = run_script("scan_banned_phrases.py", ["--draft", str(draft), "--out-dir", str(data_dir)])
    if not ok:
        print_status("scan_banned_phrases failed — audit-flags.json not created", "error")
        return StepResult("failed", "scan_banned_phrases.py failed")

    ok = run_script("analyse_rhythm.py", ["--draft", str(draft), "--out-dir", str(data_dir)])
    if not ok:
        print_status("analyse_rhythm failed — rhythm-analysis.json not created", "error")
        return StepResult("failed", "analyse_rhythm.py failed")

    skill_result = run_claude_skill("polish.md", ws, ctx.brand_dir)
    if not skill_result.ok:
        return _skill_failure(skill_result)
    if not _validate_banned_phrases(ws, data_dir):
        return StepResult("failed", "banned-phrase gate failed — see audit-flags.json")
    return StepResult("complete")


def step_output(ctx: RunContext, article: str) -> StepResult:
    ws = workspace(ctx.content_dir, article)
    draft = ws / "editorial" / "draft.md"
    data_dir = ws / "data"
    publish_dir = ws / "publish"
    data_dir.mkdir(parents=True, exist_ok=True)
    publish_dir.mkdir(parents=True, exist_ok=True)

    if not draft.exists():
        print_status("editorial/draft.md not found", "error")
        return StepResult("failed", "editorial/draft.md not found")

    _seed_publisher_meta(ctx, data_dir, article)
    ok = run_script("validate_meta.py", ["--draft", str(draft), "--out-dir", str(data_dir)])
    if not ok:
        return StepResult("failed", "validate_meta.py failed")

    ok = run_script("generate_schema.py", [
        "--draft", str(draft),
        "--meta",  str(data_dir / "meta.json"),
        "--out-dir", str(data_dir),
    ])
    if not ok:
        return StepResult("failed", "generate_schema.py failed")

    ok = run_script("build_output.py", ["--workspace", str(ws)])
    if not ok:
        return StepResult("failed", "build_output.py failed")

    ok = run_script("generate_checklist.py", ["--workspace", str(ws)])
    if not ok:
        return StepResult("failed", "generate_checklist.py failed")

    return StepResult("complete")


STEP_RUNNERS: dict[str, callable] = {
    "keyword":          step_keyword,
    "angle":            step_angle,
    "headline-outline": step_headline_outline,
    "research":         step_research,
    "writing":          step_writing,
    "polish":           step_polish,
    "output":           step_output,
}
