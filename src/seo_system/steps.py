"""
Workflow step runners. Each step_* function receives a RunContext and article slug.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from seo_system.runner import print_status, run_claude_skill, run_script
from seo_system.workspace import load_log, save_log, workspace


@dataclass
class RunContext:
    content_dir: Path
    brand_dir: Path
    market: str = "us"


def get_keyword(ctx: RunContext, article: str) -> str:
    """Read keyword from log.json, or prompt user."""
    log = load_log(ctx.content_dir, article)
    kw = log.get("keyword", "").strip()
    if not kw:
        label = log.get("display_name", article)
        print()
        kw = input(f"  Enter the target keyword for '{label}': ").strip()
        log["keyword"] = kw
        save_log(ctx.content_dir, article, log)
    return kw


def step_keyword(ctx: RunContext, article: str) -> bool:
    ws = workspace(ctx.content_dir, article)
    kw = get_keyword(ctx, article)

    data_dir = ws / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    serp_out = data_dir / "serp-urls.json"
    serp_pages_dir = data_dir / "serp-pages"
    serp_pages_dir.mkdir(parents=True, exist_ok=True)

    ok = run_script("fetch_serp.py", ["--keyword", kw, "--country", ctx.market, "--out-dir", str(data_dir)])
    if not ok:
        return False

    if not serp_out.exists():
        print_status("serp-urls.json not found — cannot fetch SERP pages", "error")
        return False

    with open(serp_out) as f:
        serp_data = json.load(f)

    urls = [entry.get("url") for entry in serp_data if entry.get("url")]
    for i, url in enumerate(urls[:10], 1):
        out_file = serp_pages_dir / f"{i}.md"
        ok = run_script("fetch_url.py", ["--url", url, "--out", str(out_file)])
        if not ok:
            print_status(f"fetch_url failed for URL {i} — skipping (partial SERP data)", "error")

    ok = run_script("summarise_serp_pages.py", [
        "--serp-pages-dir", str(serp_pages_dir),
        "--out-dir",        str(data_dir),
    ])
    if not ok:
        print_status("summarise_serp_pages failed — serp-summaries.json not created", "error")
        return False

    return True


def step_angle(ctx: RunContext, article: str) -> bool:
    ws = workspace(ctx.content_dir, article)
    print()
    seed = input("  Your angle idea (Enter to let Claude analyse the SERP freely): ").strip()
    return run_claude_skill("keyword-and-angle.md", ws, ctx.brand_dir, seed=seed or None)


def step_headline_outline(ctx: RunContext, article: str) -> bool:
    ws = workspace(ctx.content_dir, article)
    print()
    seed = input("  Your headline idea (Enter for Claude's options): ").strip()
    return run_claude_skill("headline-and-outline.md", ws, ctx.brand_dir, seed=seed or None)


def step_research(ctx: RunContext, article: str) -> bool:
    ws = workspace(ctx.content_dir, article)
    sources_dir = ws / "data" / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    ok = run_claude_skill("research-authority.md", ws, ctx.brand_dir)
    if not ok:
        return False

    index_path = sources_dir / "index.json"
    if not index_path.exists():
        print_status("Claude exited cleanly but data/sources/index.json was not written — research produced nothing", "error")
        return False

    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
        sources = index.get("sources", [])
        if not sources:
            print_status("data/sources/index.json exists but contains no sources — research produced nothing", "error")
            return False

        missing = [s["id"] for s in sources if not (sources_dir / f"{s['id']}.md").exists()]
        if missing:
            print_status(f"index.json lists sources with no matching file: {', '.join(missing)}", "error")
            return False

        print_status(f"sources verified: {len(sources)} source(s) in index, all files present", "ok")
    except (json.JSONDecodeError, Exception) as e:
        print_status(f"data/sources/index.json is not valid JSON: {e}", "error")
        return False

    return True


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


def _seed_publisher_meta(ctx: RunContext, data_dir: Path) -> None:
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
    existing["publisher_name"] = name_m.group(1).strip()
    existing["site_url"] = url_m.group(1).strip()
    meta_path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")


def step_writing(ctx: RunContext, article: str) -> bool:
    ws = workspace(ctx.content_dir, article)
    data_dir = ws / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    ok = run_claude_skill("writing.md", ws, ctx.brand_dir)
    if not ok:
        return False
    return _validate_banned_phrases(ws, data_dir)


def step_polish(ctx: RunContext, article: str) -> bool:
    ws = workspace(ctx.content_dir, article)
    draft = ws / "editorial" / "draft.md"
    data_dir = ws / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    if not draft.exists():
        print_status("editorial/draft.md not found — run 'writing' step first", "error")
        return False

    ok = run_script("scan_banned_phrases.py", ["--draft", str(draft), "--out-dir", str(data_dir)])
    if not ok:
        print_status("scan_banned_phrases failed — audit-flags.json not created", "error")
        return False

    ok = run_script("analyse_rhythm.py", ["--draft", str(draft), "--out-dir", str(data_dir)])
    if not ok:
        print_status("analyse_rhythm failed — rhythm-analysis.json not created", "error")
        return False

    ok = run_claude_skill("polish.md", ws, ctx.brand_dir)
    if not ok:
        return False
    return _validate_banned_phrases(ws, data_dir)



def step_output(ctx: RunContext, article: str) -> bool:
    ws = workspace(ctx.content_dir, article)
    draft = ws / "editorial" / "draft.md"
    data_dir = ws / "data"
    publish_dir = ws / "publish"
    data_dir.mkdir(parents=True, exist_ok=True)
    publish_dir.mkdir(parents=True, exist_ok=True)

    if not draft.exists():
        print_status("editorial/draft.md not found", "error")
        return False

    _seed_publisher_meta(ctx, data_dir)
    ok = run_script("validate_meta.py", ["--draft", str(draft), "--out-dir", str(data_dir)])
    if not ok:
        return False

    ok = run_script("generate_schema.py", [
        "--draft", str(draft),
        "--meta",  str(data_dir / "meta.json"),
        "--out-dir", str(data_dir),
    ])
    if not ok:
        return False

    ok = run_script("build_output.py", ["--workspace", str(ws)])
    if not ok:
        return False

    return run_script("generate_checklist.py", ["--workspace", str(ws)])


STEP_RUNNERS: dict[str, callable] = {
    "keyword":          step_keyword,
    "angle":            step_angle,
    "headline-outline": step_headline_outline,
    "research":         step_research,
    "writing":          step_writing,
    "polish":           step_polish,
    "output":           step_output,
}
