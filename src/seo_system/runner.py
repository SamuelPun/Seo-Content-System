"""
Subprocess runners — Python utility scripts and Claude Code skill sessions.
All functions take explicit path arguments (no globals).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from seo_system.config import SCRIPTS_DIR, SKILLS_DIR


def print_status(msg: str, kind: str = "info"):
    icons = {"info": "→", "ok": "✓", "skip": "·", "gate": "⏸", "error": "✗"}
    print(f"  {icons.get(kind, '→')} {msg}")


def run_script(script_name: str, args: list[str]) -> bool:
    """Run a Python utility script from the scripts/ directory. Returns True on success."""
    cmd = [sys.executable, str(SCRIPTS_DIR / script_name)] + args
    print_status(f"Running {script_name} {' '.join(args)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print_status(f"{script_name} failed (exit {result.returncode})", "error")
        return False
    return True


def run_claude_skill(
    skill_file: str,
    ws: Path,
    brand_dir: Path,
    seed: str = None,
) -> bool:
    """
    Launch a Claude Code session with the given skill file.
    WORKSPACE and BRAND_DIR are injected into the prompt header so skills
    can resolve both article files and brand files by absolute path.
    Optional seed is prepended so Claude builds on the editor's idea.
    Returns True on success.
    """
    skill_path = SKILLS_DIR / skill_file

    if not skill_path.exists():
        print_status(f"Skill file not found: {skill_path}", "error")
        return False

    skill_content = skill_path.read_text()

    header = (
        f"WORKSPACE: {ws.resolve()}\n"
        f"EDITORIAL_DIR: {(ws / 'editorial').resolve()}\n"
        f"DATA_DIR: {(ws / 'data').resolve()}\n"
        f"PUBLISH_DIR: {(ws / 'publish').resolve()}\n"
        f"BRAND_DIR: {brand_dir.resolve()}\n"
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
        cwd=str(Path.cwd()),
    )
    if result.returncode != 0:
        print_status(f"Claude Code session failed (exit {result.returncode})", "error")
        return False
    return True
