"""
Subprocess runners — Python utility scripts and Claude Code skill sessions.
All functions take explicit path arguments (no globals).
"""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from seo_system.config import SCRIPTS_DIR, SKILLS_DIR

# Default timeouts. A hung subprocess with no timeout blocks the whole pipeline
# indefinitely with no way to tell "still working" from "stuck" — these are generous
# enough for real runs but bounded. Override per-call if a specific script/skill
# genuinely needs longer.
SCRIPT_TIMEOUT_SECONDS = 300     # 5 min — mechanical scripts (fetches, scans, builds)
SKILL_TIMEOUT_SECONDS  = 1800    # 30 min — a Claude Code session doing real research/writing

# Best-effort match for usage/rate-limit messages in a Claude Code session's output, so
# a stopped run can be classified distinctly from a genuine failure (see StepResult's
# "usage_limit" status) instead of the driving Claude having to remember it saw a
# warning earlier in the conversation. Wording isn't guaranteed stable across CLI
# versions — tune this if it stops matching real output.
_USAGE_LIMIT_PATTERN = re.compile(
    r"usage limit|rate limit|rate_limit_error|overloaded_error|try again later",
    re.IGNORECASE,
)


def print_status(msg: str, kind: str = "info"):
    icons = {"info": "→", "ok": "✓", "skip": "·", "gate": "⏸", "error": "✗"}
    print(f"  {icons.get(kind, '→')} {msg}")


def _skill_model(skill_content: str) -> str | None:
    """Optional `model:` frontmatter field — lets a mechanical, rubric-bound role
    (a verdict, a bounded revision) opt into a cheaper/faster model instead of every
    role defaulting to the same tier regardless of how much judgment it needs. None
    of the current skill files set this yet — it's a deliberate quality/cost tradeoff
    per role, not something to guess at file-by-file without being able to evaluate
    the output."""
    m = re.match(r'\A---\n(.*?)\n---\n', skill_content, re.DOTALL)
    if not m:
        return None
    fm = re.search(r'^model:\s*(\S+)\s*$', m.group(1), re.MULTILINE)
    return fm.group(1).strip() if fm else None


def run_script(script_name: str, args: list[str], timeout: int = SCRIPT_TIMEOUT_SECONDS) -> bool:
    """Run a Python utility script from the scripts/ directory. Returns True on success."""
    cmd = [sys.executable, str(SCRIPTS_DIR / script_name)] + args
    print_status(f"Running {script_name} {' '.join(args)}")
    try:
        result = subprocess.run(cmd, timeout=timeout)
    except subprocess.TimeoutExpired:
        print_status(f"{script_name} timed out after {timeout}s", "error")
        return False
    if result.returncode != 0:
        print_status(f"{script_name} failed (exit {result.returncode})", "error")
        return False
    return True


@dataclass
class SkillRunResult:
    """What a Claude Code skill session actually did, distinct from a bare pass/fail —
    a timeout and a usage-limit cutoff both need different handling upstream (surfaced
    to the human differently) than a genuine failure."""
    status: str  # "ok" | "failed" | "timeout" | "usage_limit"
    message: str = ""

    @property
    def ok(self) -> bool:
        return self.status == "ok"


def run_claude_skill(
    skill_file: str,
    ws: Path,
    brand_dir: Path,
    seed: str = None,
    timeout: int = SKILL_TIMEOUT_SECONDS,
) -> SkillRunResult:
    """
    Launch a Claude Code session with the given skill file.
    WORKSPACE and BRAND_DIR are injected into the prompt header so skills
    can resolve both article files and brand files by absolute path.
    Optional seed is prepended so Claude builds on the editor's idea.
    """
    skill_path = SKILLS_DIR / skill_file

    if not skill_path.exists():
        print_status(f"Skill file not found: {skill_path}", "error")
        return SkillRunResult("failed", f"Skill file not found: {skill_path}")

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

    cmd = ["claude", "--print", "--dangerously-skip-permissions"]
    model = _skill_model(skill_content)
    if model:
        cmd += ["--model", model]

    print_status(f"Launching Claude Code — skill: {skill_file}" + (f" (model: {model})" if model else ""))
    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout,
            # ponytail: cwd is the workspace, not the orchestrator repo — Claude Code
            # auto-loads CLAUDE.md from cwd for every session it starts, including
            # --print subprocesses, so running from the orchestrator's own directory
            # leaks its "drive everything through the CLI" instructions into the skill
            # session and makes it role-play as a second orchestrator instead of doing
            # its job. The workspace has no CLAUDE.md, so nothing leaks.
            cwd=str(ws.resolve()),
        )
    except subprocess.TimeoutExpired:
        print_status(f"Claude Code session timed out after {timeout}s — skill: {skill_file}", "error")
        return SkillRunResult("timeout", f"{skill_file} timed out after {timeout}s")

    # Stream through what the session printed — capture_output means it no longer
    # reaches the terminal on its own.
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    combined_output = f"{result.stdout or ''}\n{result.stderr or ''}"
    if _USAGE_LIMIT_PATTERN.search(combined_output):
        print_status(f"Usage/rate limit detected in output — skill: {skill_file}", "error")
        return SkillRunResult("usage_limit", f"{skill_file} hit a usage or rate limit")

    if result.returncode != 0:
        print_status(f"Claude Code session failed (exit {result.returncode})", "error")
        return SkillRunResult("failed", f"{skill_file} exited {result.returncode}")

    return SkillRunResult("ok")
