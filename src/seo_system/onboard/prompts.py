"""Terminal I/O helpers for the interactive onboarding flow."""

from __future__ import annotations

import sys


def header(text: str):
    width = 54
    print()
    print(f"  {'─' * width}")
    print(f"  {text}")
    print(f"  {'─' * width}")
    print()


def ask(prompt: str, default: str = "") -> str:
    """Single-line prompt. Returns stripped input, or default if empty."""
    hint = f" [{default}]" if default else ""
    try:
        raw = input(f"  {prompt}{hint}\n  → ").strip()
    except KeyboardInterrupt:
        print("\n\n  Onboarding cancelled.")
        sys.exit(0)
    return raw if raw else default


def ask_multiline(prompt: str) -> str:
    """Multi-line prompt. User types lines, blank line to finish."""
    print(f"  {prompt}")
    print("  (blank line to finish)")
    lines = []
    try:
        while True:
            line = input("  → ")
            if line == "":
                break
            lines.append(line.strip())
    except KeyboardInterrupt:
        print("\n\n  Onboarding cancelled.")
        sys.exit(0)
    return "\n".join(lines)


def ask_list(prompt: str) -> list[str]:
    """Ask for one item per line. Returns list of non-empty strings."""
    raw = ask_multiline(prompt)
    return [l for l in raw.splitlines() if l.strip()]


def confirm(prompt: str) -> bool:
    try:
        raw = input(f"  {prompt} [y/N] → ").strip().lower()
    except KeyboardInterrupt:
        print("\n\n  Onboarding cancelled.")
        sys.exit(0)
    return raw in ("y", "yes")
