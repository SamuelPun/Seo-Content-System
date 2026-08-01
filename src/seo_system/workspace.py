"""
Workspace management — article log I/O, step tracking, and editorial file init.
All functions take content_dir as an explicit first parameter (no globals).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from seo_system.config import STEPS


def workspace(content_dir: Path, article: str) -> Path:
    return content_dir / article


def log_path(content_dir: Path, article: str) -> Path:
    return workspace(content_dir, article) / "data" / "log.json"


def load_log(content_dir: Path, article: str) -> dict:
    p = log_path(content_dir, article)
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return {"article": article, "display_name": article, "keyword": "", "steps": {}}


def save_log(content_dir: Path, article: str, log: dict):
    log_path(content_dir, article).parent.mkdir(parents=True, exist_ok=True)
    with open(log_path(content_dir, article), "w") as f:
        json.dump(log, f, indent=2)


def mark_complete(content_dir: Path, article: str, step: str):
    log = load_log(content_dir, article)
    log["steps"][step] = {
        "status": "complete",
        "completed_at": datetime.now(timezone.utc).isoformat(),
    }
    save_log(content_dir, article, log)


def mark_pending(content_dir: Path, article: str, step: str):
    log = load_log(content_dir, article)
    log["steps"][step] = {"status": "pending"}
    save_log(content_dir, article, log)


def is_complete(content_dir: Path, article: str, step: str) -> bool:
    log = load_log(content_dir, article)
    return log.get("steps", {}).get(step, {}).get("status") == "complete"


def update_content_index(content_dir: Path):
    """Regenerate _index.md in content_dir from all article log.json files."""
    rows = []
    for article_dir in sorted(content_dir.iterdir()):
        if not article_dir.is_dir() or article_dir.name.startswith("_"):
            continue
        log_file = article_dir / "data" / "log.json"
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
    index_path = content_dir / "_index.md"
    index_path.write_text(header + "\n".join(rows) + "\n", encoding="utf-8")


def init_article_files(slug: str, workspace_path: Path, display_name: str = None):
    """Initialise work-log.md and writer-notes.md inside the editorial/ subfolder."""
    label = display_name or slug
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    editorial_dir = workspace_path / "editorial"
    editorial_dir.mkdir(parents=True, exist_ok=True)

    work_log_path = editorial_dir / "work-log.md"
    if not work_log_path.exists():
        work_log_path.write_text(
            f"# Work Log — {label}\n"
            "*Append-only. Written by every skill step and the orchestrator. Never edited — only added to.*\n"
            "*Read by: human editor at any gate, polish skill before final pass.*\n\n"
            f"---\nstep: init | {timestamp} | status: complete\n---\n"
            f"Workspace created for {label}. work-log.md and writer-notes.md initialised.\n\n"
        )

    writer_notes_path = editorial_dir / "writer-notes.md"
    if not writer_notes_path.exists():
        writer_notes_path.write_text(
            f"# Writer Notes — {label}\n"
            "*Append-only. Written on instinct — not on a schedule. Short, unpolished, honest.*\n"
            "*Written by: writing skill, human editor.*\n"
            "*Read by: polish skill before final pass. Human editor after the run for system improvement.*\n\n"
            "---\n\n"
        )


def log_step_start(workspace_path: Path, step_name: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = (
        f"---\nstep: {step_name} | {timestamp} | status: running\n---\n"
        f"Orchestrator started {step_name} step.\n\n"
    )
    with open(workspace_path / "editorial" / "work-log.md", "a") as f:
        f.write(entry)


def log_step_end(workspace_path: Path, step_name: str, status: str, note: str = ""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    note_line = f"\n{note}" if note else ""
    entry = (
        f"---\nstep: {step_name} | {timestamp} | status: {status}\n---\n"
        f"Orchestrator completed {step_name} step.{note_line}\n\n"
    )
    with open(workspace_path / "editorial" / "work-log.md", "a") as f:
        f.write(entry)
