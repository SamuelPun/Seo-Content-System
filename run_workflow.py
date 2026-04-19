#!/usr/bin/env python3
"""
run_workflow.py — SEO Content System Orchestrator
Chains all scripts and Claude Code sessions together for a single article.

Usage:
    python3 run_workflow.py --client monx --article "us-expat-tax" --step all
    python3 run_workflow.py --client monx --article "us-expat-tax" --step keyword
    python3 run_workflow.py --client monx --article "us-expat-tax" --from headline-outline
    python3 run_workflow.py --client monx --article "us-expat-tax" --step audit --force
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def normalise_slug(name: str) -> str:
    """Convert any article name to a filesystem-safe hyphenated slug."""
    slug = name.lower().strip()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    return slug.strip('-')


def init_article_files(slug, workspace_path, display_name=None):
    """Initialise work-log.md and writer-notes.md for a new article."""
    label = display_name or slug
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    work_log_path = workspace_path / "work-log.md"
    if not work_log_path.exists():
        work_log_path.write_text(
            f"# Work Log — {label}\n"
            "*Append-only. Written by every skill step and the orchestrator. Never edited — only added to.*\n"
            "*Read by: human editor at any gate, revision skill before final pass.*\n\n"
            f"---\nstep: init | {timestamp} | status: complete\n---\n"
            f"Workspace created for {label}. work-log.md and writer-notes.md initialised.\n\n"
        )

    writer_notes_path = workspace_path / "writer-notes.md"
    if not writer_notes_path.exists():
        writer_notes_path.write_text(
            f"# Writer Notes — {label}\n"
            "*Append-only. Written on instinct — not on a schedule. Short, unpolished, honest.*\n"
            "*Written by: writing skill, audit skill, human editor (at revision gate).*\n"
            "*Read by: revision skill before final pass. Human editor after the run for system improvement.*\n\n"
            "---\n\n"
        )


def log_step_start(slug, workspace_path, step_name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = (
        f"---\nstep: {step_name} | {timestamp} | status: running\n---\n"
        f"Orchestrator started {step_name} step.\n\n"
    )
    with open(workspace_path / "work-log.md", "a") as f:
        f.write(entry)


def log_step_end(slug, workspace_path, step_name, status, note=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    note_line = f"\n{note}" if note else ""
    entry = (
        f"---\nstep: {step_name} | {timestamp} | status: {status}\n---\n"
        f"Orchestrator completed {step_name} step.{note_line}\n\n"
    )
    with open(workspace_path / "work-log.md", "a") as f:
        f.write(entry)


# ---------------------------------------------------------------------------
# Configuration (paths resolved in main() once --client is known)
# ---------------------------------------------------------------------------

STEPS = [
    "keyword",          # fetch_serp + fetch_url (SERP pages) → serp-urls.json, serp-pages/
    "angle",            # Claude Code session → angle.md
    "headline-outline", # fetch_sitemap + Claude Code session → headline.md, outline.md
    "research",         # fetch_url (sources) → sources/
    "writing",          # Claude Code session → draft.md
    "audit",            # scan_banned_phrases + analyse_rhythm + Claude Code → draft.md revised
    "revision",         # Human + Claude Code session → draft.md final
    "links",            # match_internal_links → internal-link-candidates.json
    "output",           # validate_meta + generate_schema + build_output → final.html
]

# Steps where the orchestrator pauses and waits for human input before continuing
HUMAN_GATES = {"angle", "headline-outline", "research", "revision"}

SCRIPTS_DIR = Path(__file__).parent / "scripts"
SKILLS_DIR  = Path(__file__).parent / "skills"

# Set in main() once --client is resolved
CONTENT_DIR: Path = None
BRAND_DIR:   Path = None
CLIENT_SITEMAP_URL: str = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def workspace(article: str) -> Path:
    return CONTENT_DIR / article


def log_path(article: str) -> Path:
    return workspace(article) / "log.json"


def load_log(article: str) -> dict:
    p = log_path(article)
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return {"article": article, "display_name": article, "keyword": "", "steps": {}}


def save_log(article: str, log: dict):
    with open(log_path(article), "w") as f:
        json.dump(log, f, indent=2)


def mark_complete(article: str, step: str):
    log = load_log(article)
    log["steps"][step] = {
        "status": "complete",
        "completed_at": datetime.now(timezone.utc).isoformat()
    }
    save_log(article, log)


def mark_pending(article: str, step: str):
    log = load_log(article)
    log["steps"][step] = {"status": "pending"}
    save_log(article, log)


def is_complete(article: str, step: str) -> bool:
    log = load_log(article)
    return log.get("steps", {}).get(step, {}).get("status") == "complete"


def update_content_index():
    """Regenerate _index.md in CONTENT_DIR from all article log.json files."""
    rows = []
    for article_dir in sorted(CONTENT_DIR.iterdir()):
        if not article_dir.is_dir() or article_dir.name.startswith("_"):
            continue
        log_file = article_dir / "log.json"
        if not log_file.exists():
            continue
        try:
            data = json.loads(log_file.read_text(encoding="utf-8"))
        except Exception:
            continue
        keyword = data.get("display_name", article_dir.name)
        steps = data.get("steps", {})
        completed = [s for s in STEPS if steps.get(s, {}).get("status") == "complete"]
        status = completed[-1] if completed else "pending"
        last_edit = datetime.fromtimestamp(log_file.stat().st_mtime).strftime("%Y-%m-%d")
        rows.append(f"| {keyword} | {status} | {last_edit} |")

    header = "| Keyword | Status | Last edited |\n|---|---|---|\n"
    index_path = CONTENT_DIR / "_index.md"
    index_path.write_text(header + "\n".join(rows) + "\n", encoding="utf-8")


def print_status(msg: str, kind: str = "info"):
    icons = {"info": "→", "ok": "✓", "skip": "·", "gate": "⏸", "error": "✗"}
    print(f"  {icons.get(kind, '→')} {msg}")


def run_script(script_name: str, args: list[str]) -> bool:
    """Run a Python utility script. Returns True on success."""
    cmd = [sys.executable, str(SCRIPTS_DIR / script_name)] + args
    print_status(f"Running {script_name} {' '.join(args)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print_status(f"{script_name} failed (exit {result.returncode})", "error")
        return False
    return True


def run_claude_skill(skill_file: str, article: str, seed: str = None) -> bool:
    """
    Launch a Claude Code session with the given skill file.
    WORKSPACE and BRAND_DIR are injected into the prompt header so skills
    can resolve both article files and brand files by absolute path.
    Optional seed is prepended so Claude builds on the editor's idea.
    Returns True on success.
    """
    skill_path = SKILLS_DIR / skill_file
    ws = workspace(article)

    if not skill_path.exists():
        print_status(f"Skill file not found: {skill_path}", "error")
        return False

    skill_content = skill_path.read_text()

    header = (
        f"WORKSPACE: {ws.resolve()}\n"
        f"BRAND_DIR: {BRAND_DIR.resolve()}\n"
    )

    if seed:
        prompt = (
            f"{header}\n"
            f"EDITOR SEED — use this as your starting point, verify and build on it "
            f"using the SERP data and inputs: {seed}\n\n"
            f"{skill_content}"
        )
    else:
        prompt = f"{header}\n{skill_content}"

    print_status(f"Launching Claude Code — skill: {skill_file}")
    result = subprocess.run(
        ["claude", "--print", "--dangerously-skip-permissions"],
        input=prompt,
        text=True,
        cwd=str(Path.cwd())
    )
    if result.returncode != 0:
        print_status(f"Claude Code session failed (exit {result.returncode})", "error")
        return False
    return True


# ---------------------------------------------------------------------------
# Interactive gate helpers
# ---------------------------------------------------------------------------

def _parse_angle(angle_path: Path):
    """Extract target reader and angle statement from angle.md."""
    if not angle_path.exists():
        return None, None
    text = angle_path.read_text(encoding="utf-8")
    reader_m = re.search(r'## Target reader\s*\n([^\n#]+)', text)
    angle_m  = re.search(r'## Our angle\s*\n([^\n#]+)', text)
    reader = reader_m.group(1).strip() if reader_m else None
    angle  = angle_m.group(1).strip()  if angle_m  else None
    return reader, angle


def _parse_headlines(headline_path: Path):
    """Extract headline option texts from headline.md."""
    if not headline_path.exists():
        return []
    text = headline_path.read_text(encoding="utf-8")
    return [m.strip() for m in re.findall(r'## Option \d+\n([^\n*]+)', text) if m.strip()]


def _write_chosen_headline(headline_path: Path, outline_path: Path, chosen: str):
    """Write chosen headline into the Chosen headline field in both files."""
    for path in [headline_path, outline_path]:
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        new_lines = []
        for line in lines:
            if line.startswith("**Chosen headline:**"):
                new_lines.append(f"**Chosen headline:** {chosen}")
            elif line.strip() == "## Chosen headline":
                new_lines.append(line)
                new_lines.append(chosen)
                continue
            else:
                new_lines.append(line)
        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def _parse_research_summary(sources_dir: Path):
    """Return (source_count, gaps) from sources/index.json."""
    index_path = sources_dir / "index.json"
    if not index_path.exists():
        return 0, []
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
        return len(data.get("sources", [])), data.get("gaps", [])
    except Exception:
        return 0, []


def _parse_revision_flags(ws: Path):
    """Return (flags, ready_status) from revision-notes.md."""
    notes_path = ws / "revision-notes.md"
    if not notes_path.exists():
        return [], "unknown"
    text = notes_path.read_text(encoding="utf-8")
    flags = re.findall(r'^- (.+)$', text, re.MULTILINE)
    ready_m = re.search(r'## Ready to publish\?\s*\n([^\n]+)', text)
    ready = ready_m.group(1).strip() if ready_m else "unknown"
    return flags, ready


def interactive_gate(step: str, ws: Path):
    """Present key decisions from each gate step directly in the terminal."""
    print()
    try:
        if step == "angle":
            reader, angle = _parse_angle(ws / "angle.md")
            print("  ⏸  ANGLE REVIEW")
            if reader:
                print(f"  Target reader : {reader}")
            if angle:
                print(f"  Our angle     : {angle}")
            print()
            print("  Press Enter to accept, or type your own angle:")
            raw = input("  → ").strip()
            if raw:
                angle_path = ws / "angle.md"
                if angle_path.exists():
                    text = angle_path.read_text(encoding="utf-8")
                    text = re.sub(r'(## Our angle\s*\n)[^\n#]*', rf'\g<1>{raw}\n', text)
                    angle_path.write_text(text, encoding="utf-8")
                print_status(f"Angle updated to: {raw}", "ok")

        elif step == "headline-outline":
            options = _parse_headlines(ws / "headline.md")
            print("  ⏸  HEADLINE OPTIONS")
            if options:
                for i, opt in enumerate(options, 1):
                    print(f"  [{i}] {opt}  ({len(opt)} chars)")
            else:
                print("  (Could not parse headline options — review headline.md manually)")
            print()
            print("  Select 1–5, type your own, or press Enter to edit files manually:")
            raw = input("  → ").strip()
            if raw:
                if raw.isdigit() and options and 1 <= int(raw) <= len(options):
                    chosen = options[int(raw) - 1]
                else:
                    chosen = raw
                _write_chosen_headline(ws / "headline.md", ws / "outline.md", chosen)
                print_status(f"Chosen: {chosen}", "ok")
            else:
                print("  Edit headline.md and outline.md, then press Enter when ready.")
                input("  → ")

        elif step == "research":
            source_count, gaps = _parse_research_summary(ws / "sources")
            print("  ⏸  RESEARCH REVIEW")
            print(f"  Sources gathered : {source_count}")
            if gaps:
                print(f"  Gaps flagged     : {len(gaps)}")
                for g in gaps[:5]:
                    impact  = g.get("impact", "?").upper()
                    missing = g.get("missing", "")
                    print(f"    [{impact}] {missing}")
            print()
            print("  Press Enter to accept, or review sources/index.json manually first:")
            input("  → ")

        elif step == "revision":
            flags, ready = _parse_revision_flags(ws)
            print("  ⏸  REVISION REVIEW")
            print(f"  Status : {ready}")
            if flags:
                print(f"  Flags  ({len(flags)}):")
                for f in flags[:10]:
                    print(f"    · {f}")
            print()
            print("  Press Enter to continue to output:")
            input("  → ")

        else:
            print(f"  ⏸  {step.upper()} — review workspace files, then press Enter:")
            input("  → ")

    except KeyboardInterrupt:
        print(f"\n\n  Stopped. Resume with: --from {step}")
        sys.exit(0)

    print()


def get_keyword(article: str) -> str:
    """Read keyword from log.json, or prompt user."""
    log = load_log(article)
    kw = log.get("keyword", "").strip()
    if not kw:
        label = log.get("display_name", article)
        print()
        kw = input(f"  Enter the target keyword for '{label}': ").strip()
        log["keyword"] = kw
        save_log(article, log)
    return kw


# ---------------------------------------------------------------------------
# Step runners
# ---------------------------------------------------------------------------

def step_keyword(article: str):
    ws = workspace(article)
    kw = get_keyword(article)

    serp_out = ws / "serp-urls.json"
    serp_pages_dir = ws / "serp-pages"
    serp_pages_dir.mkdir(parents=True, exist_ok=True)

    ok = run_script("fetch_serp.py", [
        "--keyword", kw,
        "--out-dir", str(ws)
    ])
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

    return True


def step_angle(article: str):
    print()
    seed = input("  Your angle idea (Enter to let Claude analyse the SERP freely): ").strip()
    return run_claude_skill("keyword-and-angle.md", article, seed=seed or None)


def step_headline_outline(article: str):
    ws = workspace(article)
    print()
    seed = input("  Your headline idea (Enter for Claude's options): ").strip()

    sitemap_args = ["--out-dir", str(ws)]
    if CLIENT_SITEMAP_URL:
        sitemap_args += ["--sitemap-url", CLIENT_SITEMAP_URL]

    ok = run_script("fetch_sitemap.py", sitemap_args)
    if not ok:
        print_status("fetch_sitemap failed — sitemap-candidates.json will be missing; links step will fail", "error")
        return False
    return run_claude_skill("headline-and-outline.md", article, seed=seed or None)


def step_research(article: str):
    ws = workspace(article)
    sources_dir = ws / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    ok = run_claude_skill("research-authority.md", article)
    if not ok:
        return False

    index_path = sources_dir / "index.json"
    if not index_path.exists():
        print_status("Claude exited cleanly but sources/index.json was not written — research produced nothing", "error")
        return False

    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
        sources = index.get("sources", [])
        if not sources:
            print_status("sources/index.json exists but contains no sources — research produced nothing", "error")
            return False
        print_status(f"sources verified: {len(sources)} source(s) in index", "ok")
    except (json.JSONDecodeError, Exception) as e:
        print_status(f"sources/index.json is not valid JSON: {e}", "error")
        return False

    return True


def step_writing(article: str):
    return run_claude_skill("writing.md", article)


def step_audit(article: str):
    ws = workspace(article)
    draft = ws / "draft.md"

    if not draft.exists():
        print_status("draft.md not found — run 'writing' step first", "error")
        return False

    ok = run_script("scan_banned_phrases.py", [
        "--draft", str(draft),
        "--out-dir", str(ws)
    ])
    if not ok:
        print_status("scan_banned_phrases failed — audit-flags.json not created", "error")
        return False

    ok = run_script("analyse_rhythm.py", [
        "--draft", str(draft),
        "--out-dir", str(ws)
    ])
    if not ok:
        print_status("analyse_rhythm failed — rhythm-analysis.json not created", "error")
        return False

    return run_claude_skill("audit.md", article)


def step_revision(article: str):
    return run_claude_skill("revision.md", article)


def step_links(article: str):
    ws = workspace(article)
    draft = ws / "draft.md"
    sitemap = ws / "sitemap-candidates.json"

    if not draft.exists():
        print_status("draft.md not found — run 'writing' step first", "error")
        return False

    if not sitemap.exists():
        print_status("sitemap-candidates.json not found — run 'headline-outline' step first", "error")
        return False

    return run_script("match_internal_links.py", [
        "--draft", str(draft),
        "--candidates", str(sitemap),
        "--out-dir", str(ws)
    ])


def step_output(article: str):
    ws = workspace(article)
    draft = ws / "draft.md"

    if not draft.exists():
        print_status("draft.md not found", "error")
        return False

    ok = run_claude_skill("output.md", article)
    if not ok:
        return False

    ok = run_script("validate_meta.py", [
        "--draft", str(draft),
        "--out-dir", str(ws)
    ])
    if not ok:
        return False

    ok = run_script("generate_schema.py", [
        "--draft", str(draft),
        "--out-dir", str(ws)
    ])
    if not ok:
        return False

    return run_script("build_output.py", [
        "--workspace", str(ws)
    ])


# ---------------------------------------------------------------------------
# Step dispatch
# ---------------------------------------------------------------------------

STEP_RUNNERS = {
    "keyword":          step_keyword,
    "angle":            step_angle,
    "headline-outline": step_headline_outline,
    "research":         step_research,
    "writing":          step_writing,
    "audit":            step_audit,
    "revision":         step_revision,
    "links":            step_links,
    "output":           step_output,
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_client_profile(client_dir: Path) -> dict:
    """Parse profile.md and return a dict with known fields."""
    profile_path = client_dir / "profile.md"
    if not profile_path.exists():
        return {}
    text = profile_path.read_text(encoding="utf-8")
    data = {}
    m = re.search(r'\*\*Sitemap index:\*\*\s*(\S+)', text)
    if m:
        data["sitemap_url"] = m.group(1).strip()
    return data


def main():
    global CONTENT_DIR, BRAND_DIR, CLIENT_SITEMAP_URL

    parser = argparse.ArgumentParser(description="SEO Content System Orchestrator")
    parser.add_argument("--client",  required=True, help="Client slug (e.g. monx)")
    parser.add_argument("--article", required=True, help="Article slug (e.g. us-expat-tax)")
    parser.add_argument("--step",    default="all",  help="Single step to run, or 'all'")
    parser.add_argument("--from",    dest="from_step", default=None,
                        help="Resume from this step (skips earlier completed steps)")
    parser.add_argument("--force",   action="store_true",
                        help="Re-run step even if already marked complete")
    args = parser.parse_args()

    # Resolve client paths
    content_base_env = os.environ.get("CONTENT_BASE", "").strip()
    if not content_base_env:
        print("ERROR: CONTENT_BASE is not set. Add it to .env or export it before running.")
        sys.exit(1)

    content_base = Path(content_base_env)
    client_dir = content_base / args.client

    if not client_dir.exists():
        print(f"ERROR: Client folder not found: {client_dir}")
        print(f"       Run onboard_client.py --client {args.client} to create it.")
        sys.exit(1)

    CONTENT_DIR = client_dir / "content"
    BRAND_DIR   = client_dir / "brand"
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    if not BRAND_DIR.exists():
        print(f"WARNING: Brand folder not found at {BRAND_DIR} — skills will not find brand files")

    profile = load_client_profile(client_dir)
    CLIENT_SITEMAP_URL = profile.get("sitemap_url")

    display_name = args.article
    article = normalise_slug(display_name)
    ws = workspace(article)
    ws.mkdir(parents=True, exist_ok=True)

    # Initialise log and workspace files if new article
    log = load_log(article)
    if not log.get("steps"):
        log["steps"] = {s: {"status": "pending"} for s in STEPS}
        log["display_name"] = display_name
        save_log(article, log)
    init_article_files(article, ws, display_name)

    # Determine which steps to run
    if args.step == "all" or args.from_step:
        steps_to_run = STEPS
        if args.from_step:
            if args.from_step not in STEPS:
                print(f"Unknown step: {args.from_step}. Valid steps: {', '.join(STEPS)}")
                sys.exit(1)
            start = STEPS.index(args.from_step)
            steps_to_run = STEPS[start:]
    else:
        if args.step not in STEPS:
            print(f"Unknown step: {args.step}. Valid steps: {', '.join(STEPS)}")
            sys.exit(1)
        steps_to_run = [args.step]

    print()
    print(f"  SEO Content System — {args.client} / {display_name}  [{article}]")
    print(f"  {'─' * 50}")
    print()

    for step in steps_to_run:
        # Skip if complete (unless --force)
        if not args.force and is_complete(article, step):
            print_status(f"{step} — already complete, skipping", "skip")
            continue

        print_status(f"Starting step: {step.upper()}")
        log_step_start(article, ws, step)

        runner = STEP_RUNNERS[step]
        success = runner(article)

        if not success:
            log_step_end(article, ws, step, "failed")
            print_status(f"Step '{step}' failed. Fix the issue and re-run with --step {step} --force", "error")
            sys.exit(1)

        mark_complete(article, step)
        log_step_end(article, ws, step, "complete")
        update_content_index()
        print_status(f"{step} — done", "ok")

        # Interactive gate — pause before continuing to next step
        if step in HUMAN_GATES and steps_to_run.index(step) < len(steps_to_run) - 1:
            interactive_gate(step, ws)

    print()
    print_status(f"All done. Workspace: {ws.resolve()}", "ok")
    print()


if __name__ == "__main__":
    main()
