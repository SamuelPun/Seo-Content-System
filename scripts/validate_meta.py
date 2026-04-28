import argparse
import json
import re
import sys
from pathlib import Path

TITLE_MIN = 30
TITLE_MAX = 60
DESC_MIN  = 100
DESC_MAX  = 160


def extract_title(text):
    match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    return match.group(1).strip() if match else None


def extract_first_paragraph(text):
    # Strip YAML frontmatter before processing
    text = re.sub(r'\A---\n.*?\n---\n?', '', text, flags=re.DOTALL)
    text = re.sub(r'^#+.+$', '', text, flags=re.MULTILINE)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs[0] if paragraphs else None


def run(draft_path, out_dir, title=None, description=None, url=None):
    if not draft_path.exists():
        print(f"ERROR: Draft not found: {draft_path}", file=sys.stderr)
        return False

    out_dir.mkdir(parents=True, exist_ok=True)
    text = draft_path.read_text(encoding="utf-8")

    # Auto-extract if not provided
    if not title:
        title = extract_title(text) or ""
    if not description:
        first_para = extract_first_paragraph(text) or ""
        description = first_para

    title_len = len(title)
    desc_len  = len(description)

    flags = []
    if title_len < TITLE_MIN:
        flags.append(f"Title too short ({title_len} chars, min {TITLE_MIN})")
    if title_len > TITLE_MAX:
        flags.append(f"Title too long ({title_len} chars, max {TITLE_MAX})")
    if desc_len < DESC_MIN:
        flags.append(f"Description too short ({desc_len} chars, min {DESC_MIN})")
    if desc_len > DESC_MAX:
        flags.append(f"Description too long ({desc_len} chars, max {DESC_MAX})")

    meta = {
        "title":            title,
        "title_length":     title_len,
        "description":      description,
        "description_length": desc_len,
        "url":              url or "",
        "flags":            flags,
        "passed":           len(flags) == 0,
    }

    out_path = out_dir / "meta.json"
    out_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK]   {out_path}")
    print("\n=== META VALIDATION ===")
    print(f"  Title ({title_len} chars): {title[:70]}")
    print(f"  Desc  ({desc_len} chars): {description[:80]}...")
    if flags:
        print("\n  ⚠ FLAGS:")
        for f in flags:
            print(f"    - {f}")
    else:
        print("\n  ✓ All checks passed")
    return True


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft",       required=True)
    parser.add_argument("--out-dir",     required=True)
    parser.add_argument("--title",       default=None, help="Override title (default: extract from draft H1)")
    parser.add_argument("--description", default=None, help="Override meta description")
    parser.add_argument("--url",         default=None, help="Page URL")
    return parser.parse_args()


def main():
    args = parse_args()
    ok = run(Path(args.draft), Path(args.out_dir), args.title, args.description, args.url)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
