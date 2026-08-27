"""
Summarise SERP pages into a compact JSON file for the angle stage.

Reads serp-pages/1.md … N.md and extracts only what Claude needs for
competitive analysis: headings, introduction, H2 section snippets, external
links, and word count.  Reduces ~44 KB of full page markdown to ~6-8 KB of
structured data with no information loss for judgment tasks.

Usage:
    python3 summarise_serp_pages.py \
        --serp-pages-dir data/serp-pages \
        --out-dir data
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

_H2_SNIPPET_WORDS = 50   # words captured per H2 section
_INTRO_MAX_WORDS  = 200  # words captured before the first H2
_MAX_LINKS        = 20   # external links captured per page


def _word_count(text: str) -> int:
    return len(text.split())


def _summarise_page(content: str) -> dict:
    lines = content.splitlines()

    headings: list[dict] = []
    intro_lines: list[str] = []
    h2_sections: dict[str, str] = {}
    external_links: list[dict] = []

    current_h2: str | None = None
    current_h2_words: list[str] = []
    in_intro = True

    for line in lines:
        stripped = line.strip()

        # --- Headings ---
        h1 = re.match(r'^#\s+(.+)$', stripped)
        h2 = re.match(r'^##\s+(.+)$', stripped)
        h3 = re.match(r'^###\s+(.+)$', stripped)

        if h1:
            headings.append({"level": "h1", "text": h1.group(1).strip()})
            continue
        if h2:
            if current_h2 is not None:
                h2_sections[current_h2] = " ".join(current_h2_words[:_H2_SNIPPET_WORDS])
            current_h2 = h2.group(1).strip()
            current_h2_words = []
            in_intro = False
            headings.append({"level": "h2", "text": current_h2})
            continue
        if h3:
            headings.append({"level": "h3", "text": h3.group(1).strip()})
            continue

        # Skip empty lines, table rows, horizontal rules
        if not stripped or stripped.startswith("|") or re.match(r'^-{3,}$', stripped):
            continue

        # --- Intro text (before first H2) ---
        if in_intro:
            intro_lines.append(stripped)

        # --- H2 section snippet ---
        if current_h2 is not None and len(current_h2_words) < _H2_SNIPPET_WORDS * 2:
            current_h2_words.extend(stripped.split())

        # --- External links ---
        if len(external_links) < _MAX_LINKS:
            for m in re.finditer(r'\[([^\]]*)\]\((https?://[^\)]+)\)', stripped):
                anchor = m.group(1).strip()
                url = m.group(2).strip()
                # Skip empty anchors and image files
                if not anchor or re.search(r'\.(png|jpg|gif|svg|webp)(\?|$)', url, re.I):
                    continue
                external_links.append({
                    "url": url,
                    "anchor": anchor,
                    "context": stripped[:200],
                })
                if len(external_links) >= _MAX_LINKS:
                    break

    # Flush last H2 section
    if current_h2 is not None:
        h2_sections[current_h2] = " ".join(current_h2_words[:_H2_SNIPPET_WORDS])

    # Trim introduction to word budget
    intro_text = " ".join(" ".join(intro_lines).split()[:_INTRO_MAX_WORDS])

    # Attach snippets to H2 headings
    headings_out = []
    for h in headings:
        entry = dict(h)
        if h["level"] == "h2" and h["text"] in h2_sections:
            entry["snippet"] = h2_sections[h["text"]]
        headings_out.append(entry)

    return {
        "word_count": _word_count(content),
        "headings": headings_out,
        "introduction": intro_text,
        "external_links": external_links,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarise SERP pages to compact JSON.")
    parser.add_argument("--serp-pages-dir", required=True, help="Directory containing 1.md … N.md")
    parser.add_argument("--out-dir",        required=True, help="Directory to write serp-summaries.json")
    args = parser.parse_args()

    pages_dir = Path(args.serp_pages_dir)
    out_dir   = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    summaries = []
    for i in range(1, 11):
        page_file = pages_dir / f"{i}.md"
        if not page_file.exists():
            continue
        content = page_file.read_text(encoding="utf-8")
        summary = _summarise_page(content)
        summary["position"] = i
        summaries.append(summary)

    if not summaries:
        print(f"[summarise_serp_pages] No page files found in {pages_dir}")
        raise SystemExit(1)

    out_path = out_dir / "serp-summaries.json"
    out_path.write_text(json.dumps(summaries, indent=2, ensure_ascii=False), encoding="utf-8")

    total_in  = sum((pages_dir / f"{s['position']}.md").stat().st_size for s in summaries)
    total_out = out_path.stat().st_size
    print(
        f"[summarise_serp_pages] {len(summaries)} pages → {out_path.name} "
        f"({total_in // 1024} KB → {total_out // 1024} KB)"
    )


if __name__ == "__main__":
    main()
