"""
Interactive gate helpers — parse skill output files and prompt the human editor.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from seo_system.runner import print_status


def _parse_angle(angle_path: Path):
    """Extract target reader and angle statement from angle.md."""
    if not angle_path.exists():
        return None, None
    text = angle_path.read_text(encoding="utf-8")
    reader_m = re.search(r'^target_reader:\s*(.+)', text, re.MULTILINE)
    angle_m  = re.search(r'^angle:\s*(.+)', text, re.MULTILINE)
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
    """Return (source_count, gaps) from data/sources/index.json."""
    index_path = sources_dir / "index.json"
    if not index_path.exists():
        return 0, []
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
        return len(data.get("sources", [])), data.get("gaps", [])
    except Exception:
        return 0, []


def _parse_revision_flags(ws: Path):
    """Return (flags, ready_status) from editorial/revision-notes.md."""
    notes_path = ws / "editorial" / "revision-notes.md"
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
            reader, angle = _parse_angle(ws / "editorial" / "angle.md")
            print("  ⏸  ANGLE REVIEW")
            if reader:
                print(f"  Target reader : {reader}")
            if angle:
                print(f"  Our angle     : {angle}")
            print()
            print("  Press Enter to accept, or type your own angle:")
            raw = input("  → ").strip()
            if raw:
                angle_path = ws / "editorial" / "angle.md"
                if angle_path.exists():
                    text = angle_path.read_text(encoding="utf-8")
                    text = re.sub(r'^(angle:\s*).*', rf'\g<1>{raw}', text, flags=re.MULTILINE)
                    angle_path.write_text(text, encoding="utf-8")
                print_status(f"Angle updated to: {raw}", "ok")

        elif step == "headline-outline":
            options = _parse_headlines(ws / "editorial" / "headline.md")
            print("  ⏸  HEADLINE OPTIONS")
            if options:
                for i, opt in enumerate(options, 1):
                    print(f"  [{i}] {opt}  ({len(opt)} chars)")
            else:
                print("  (Could not parse headline options — review editorial/headline.md manually)")
            print()
            print("  Select 1–5, type your own, or press Enter to edit files manually:")
            raw = input("  → ").strip()
            if raw:
                if raw.isdigit() and options and 1 <= int(raw) <= len(options):
                    chosen = options[int(raw) - 1]
                else:
                    chosen = raw
                _write_chosen_headline(
                    ws / "editorial" / "headline.md",
                    ws / "editorial" / "outline.md",
                    chosen,
                )
                print_status(f"Chosen: {chosen}", "ok")
            else:
                print("  Edit editorial/headline.md and editorial/outline.md, then press Enter when ready.")
                input("  → ")

        elif step == "research":
            source_count, gaps = _parse_research_summary(ws / "data" / "sources")
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

        else:
            print(f"  ⏸  {step.upper()} — review workspace files, then press Enter:")
            input("  → ")

    except KeyboardInterrupt:
        print(f"\n\n  Stopped. Resume with: --from {step}")
        sys.exit(0)
    except EOFError:
        print("  (non-interactive — gate auto-passed)")

    print()
