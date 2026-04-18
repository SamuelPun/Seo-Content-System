#!/usr/bin/env python3
"""
run_workflow.py — SEO Content System Orchestrator
Chains all scripts and Claude Code sessions together for a single article.

Usage:
    python3 run_workflow.py --article "us-expat-tax" --step all
    python3 run_workflow.py --article "us-expat-tax" --step keyword
    python3 run_workflow.py --article "us-expat-tax" --from outline
    python3 run_workflow.py --article "us-expat-tax" --step audit --force
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import datetime


def init_article_files(slug, workspace_path):
    """Initialise work-log.md and writer-notes.md for a new article."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    work_log_path = workspace_path / "work-log.md"
    if not work_log_path.exists():
        work_log_path.write_text(
            f"# Work Log — {slug}\n"
            "*Append-only. Written by every skill step and the orchestrator. Never edited — only added to.*\n"
            "*Read by: human editor at any gate, revision skill before final pass.*\n\n"
            f"---\nstep: init | {timestamp} | status: complete\n---\n"
            f"Workspace created for {slug}. work-log.md and writer-notes.md initialised.\n\n"
        )

    writer_notes_path = workspace_path / "writer-notes.md"
    if not writer_notes_path.exists():
        writer_notes_path.write_text(
            f"# Writer Notes — {slug}\n"
            "*Append-only. Written on instinct — not on a schedule. Short, unpolished, honest.*\n"
            "*Written by: writing skill, audit skill, human editor (at revision gate).*\n"
            "*Read by: revision skill before final pass. Human editor after the run for system improvement.*\n\n"
            "---\n\n"
        )


def log_step_start(slug, workspace_path, step_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = (
        f"---\nstep: {step_name} | {timestamp} | status: running\n---\n"
        f"Orchestrator started {step_name} step.\n\n"
    )
    with open(workspace_path / "work-log.md", "a") as f:
        f.write(entry)


def log_step_end(slug, workspace_path, step_name, status, note=""):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    note_line = f"\n{note}" if note else ""
    entry = (
        f"---\nstep: {step_name} | {timestamp} | status: {status}\n---\n"
        f"Orchestrator completed {step_name} step.{note_line}\n\n"
    )
    with open(workspace_path / "work-log.md", "a") as f:
        f.write(entry)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

STEPS = [
    "keyword",   # fetch_serp + fetch_url (SERP pages) → serp-urls.json, serp-pages/
    "angle",     # Claude Code session → angle.md
    "headline",  # Claude Code session → headline.md
    "outline",   # Claude Code session + fetch_sitemap → outline.md
    "research",  # fetch_serp (sources) + fetch_url → sources/
    "writing",   # Claude Code session → draft.md
    "audit",     # scan_banned_phrases + analyse_rhythm + Claude Code → draft.md revised
    "revision",  # Human + Claude Code session → draft.md final
    "links",     # match_internal_links → internal-link-candidates.json
    "output",    # validate_meta + generate_schema + build_output → final.html
]

# Steps where the orchestrator pauses and waits for human input before continuing
HUMAN_GATES = {"angle", "headline", "research", "revision"}

WORKSPACE_BASE = Path("workspace/article")
SCRIPTS_DIR = Path("scripts")
SKILLS_DIR = Path("skills")
BRAND_DIR = Path("brand")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def workspace(article: str) -> Path:
    return WORKSPACE_BASE / article


def log_path(article: str) -> Path:
    return workspace(article) / "log.json"


def load_log(article: str) -> dict:
    p = log_path(article)
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return {"article": article, "keyword": "", "steps": {}}


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


def run_claude_skill(skill_file: str, article: str) -> bool:
    """
    Launch a Claude Code session with the given skill file.
    The skill file is passed as the initial prompt.
    Returns True on success.
    """
    skill_path = SKILLS_DIR / skill_file
    ws = workspace(article)

    if not skill_path.exists():
        print_status(f"Skill file not found: {skill_path}", "error")
        return False

    skill_content = skill_path.read_text()

    # Inject workspace path into the skill prompt
    prompt = f"WORKSPACE: {ws.resolve()}\n\n{skill_content}"

    print_status(f"Launching Claude Code — skill: {skill_file}")
    result = subprocess.run(
        ["claude", "--print", prompt],
        cwd=str(Path.cwd())
    )
    if result.returncode != 0:
        print_status(f"Claude Code session failed (exit {result.returncode})", "error")
        return False
    return True


def human_gate(step: str):
    """Pause and wait for human confirmation before continuing."""
    print()
    print(f"  ⏸  HUMAN GATE — {step.upper()}")
    print(f"     Review the output for '{step}' in your workspace folder.")
    print(f"     Edit if needed, then press Enter to continue (or Ctrl+C to stop).")
    print()
    try:
        input("     Press Enter when ready → ")
    except KeyboardInterrupt:
        print("\n\n  Stopped at human gate. Run again with --from {step} to resume.")
        sys.exit(0)
    print()


def get_keyword(article: str) -> str:
    """Read keyword from log.json, or prompt user."""
    log = load_log(article)
    kw = log.get("keyword", "").strip()
    if not kw:
        print()
        kw = input("  Enter the target keyword for this article: ").strip()
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
    paa_out = ws / "paa.json"
    serp_pages_dir = ws / "serp-pages"
    serp_pages_dir.mkdir(parents=True, exist_ok=True)

    # 1. Fetch SERP data from Ahrefs
    ok = run_script("fetch_serp.py", [
        "--keyword", kw,
        "--out-dir", str(ws)
    ])
    if not ok:
        return False

    # 2. Fetch each SERP URL → clean markdown
    if not serp_out.exists():
        print_status("serp-urls.json not found — cannot fetch SERP pages", "error")
        return False

    with open(serp_out) as f:
        serp_data = json.load(f)

    urls = [entry.get("url") for entry in serp_data if entry.get("url")]
    for i, url in enumerate(urls[:10], 1):
        out_file = serp_pages_dir / f"{i}.md"
        run_script("fetch_url.py", ["--url", url, "--out", str(out_file)])

    return True


def step_angle(article: str):
    return run_claude_skill("keyword-and-angle.md", article)


def step_headline(article: str):
    return run_claude_skill("headline-and-outline.md", article)


def step_outline(article: str):
    ws = workspace(article)
    # Fetch sitemap first (refreshes internal link candidates)
    run_script("fetch_sitemap.py", ["--out-dir", str(ws)])
    return run_claude_skill("headline-and-outline.md", article)


def step_research(article: str):
    ws = workspace(article)
    sources_dir = ws / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    return run_claude_skill("research-authority.md", article)


def step_writing(article: str):
    return run_claude_skill("writing.md", article)


def step_audit(article: str):
    ws = workspace(article)
    draft = ws / "draft.md"

    if not draft.exists():
        print_status("draft.md not found — run 'writing' step first", "error")
        return False

    # Run both analysis scripts against the draft
    run_script("scan_banned_phrases.py", [
        "--draft", str(draft),
        "--out", str(ws / "audit-flags.json")
    ])
    run_script("analyse_rhythm.py", [
        "--draft", str(draft),
        "--out", str(ws / "rhythm-analysis.json")
    ])

    # Claude Code session to revise based on audit output
    return run_claude_skill("audit.md", article)


def step_revision(article: str):
    return run_claude_skill("revision.md", article)


def step_links(article: str):
    ws = workspace(article)
    draft = ws / "draft.md"
    sitemap = ws / "sitemap-candidates.json"

    if not draft.exists():
        print_status("draft.md not found", "error")
        return False

    return run_script("match_internal_links.py", [
        "--draft", str(draft),
        "--sitemap", str(sitemap),
        "--out", str(ws / "internal-link-candidates.json")
    ])


def step_output(article: str):
    ws = workspace(article)
    draft = ws / "draft.md"

    if not draft.exists():
        print_status("draft.md not found", "error")
        return False

    # Generate meta, schema, then assemble HTML
    run_script("validate_meta.py", [
        "--draft", str(draft),
        "--out", str(ws / "meta.json")
    ])
    run_script("generate_schema.py", [
        "--draft", str(draft),
        "--out", str(ws / "schema.json")
    ])
    run_script("build_output.py", [
        "--workspace", str(ws),
        "--out", str(ws / "final.html")
    ])
    return True


# ---------------------------------------------------------------------------
# Step dispatch
# ---------------------------------------------------------------------------

STEP_RUNNERS = {
    "keyword":  step_keyword,
    "angle":    step_angle,
    "headline": step_headline,
    "outline":  step_outline,
    "research": step_research,
    "writing":  step_writing,
    "audit":    step_audit,
    "revision": step_revision,
    "links":    step_links,
    "output":   step_output,
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="SEO Content System Orchestrator")
    parser.add_argument("--article", required=True, help="Article slug (e.g. us-expat-tax)")
    parser.add_argument("--step",    default="all",  help="Single step to run, or 'all'")
    parser.add_argument("--from",    dest="from_step", default=None,
                        help="Resume from this step (skips earlier completed steps)")
    parser.add_argument("--force",   action="store_true",
                        help="Re-run step even if already marked complete")
    args = parser.parse_args()

    article = args.article
    ws = workspace(article)
    ws.mkdir(parents=True, exist_ok=True)

    # Initialise log if new article
    log = load_log(article)
    if not log.get("steps"):
        log["steps"] = {s: {"status": "pending"} for s in STEPS}
        save_log(article, log)

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
    print(f"  SEO Content System — {article}")
    print(f"  {'─' * 40}")
    print()

    for step in steps_to_run:
        # Skip if complete (unless --force)
        if not args.force and is_complete(article, step):
            print_status(f"{step} — already complete, skipping", "skip")
            continue

        print_status(f"Starting step: {step.upper()}")

        runner = STEP_RUNNERS[step]
        success = runner(article)

        if not success:
            print_status(f"Step '{step}' failed. Fix the issue and re-run with --step {step} --force", "error")
            sys.exit(1)

        mark_complete(article, step)
        print_status(f"{step} — done", "ok")

        # Human gate — pause before continuing to next step
        if step in HUMAN_GATES and steps_to_run.index(step) < len(steps_to_run) - 1:
            human_gate(step)

    print()
    print_status(f"All done. Workspace: {ws.resolve()}", "ok")
    print()


if __name__ == "__main__":
    main()
