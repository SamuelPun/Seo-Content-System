import argparse
import json
import re
import sys
from pathlib import Path


def extract_title(text):
    match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    return match.group(1).strip() if match else None


def extract_frontmatter_description(text):
    m = re.match(r'\A---\n(.*?)\n---\n', text, re.DOTALL)
    if not m:
        return None
    dm = re.search(r'^description:\s*(.+)$', m.group(1), re.MULTILINE)
    return dm.group(1).strip() if dm else None


def extract_first_paragraph(text):
    # Strip YAML frontmatter before processing
    text = re.sub(r'\A---\n.*?\n---\n?', '', text, flags=re.DOTALL)
    text = re.sub(r'^#+.+$', '', text, flags=re.MULTILINE)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs[0] if paragraphs else None


def run(draft_path, out_dir, title=None, description=None, url=None):
    """Extract title/description from the draft and write meta.json.

    This is extraction only — it does not judge length. generate_checklist.py
    (run later, in the output step) is the single place that decides what's
    good enough to publish. Keeping the judgment in one place means there's
    only one set of thresholds to keep correct, instead of two that can quietly
    drift out of sync with each other.
    """
    if not draft_path.exists():
        print(f"ERROR: Draft not found: {draft_path}", file=sys.stderr)
        return False

    out_dir.mkdir(parents=True, exist_ok=True)
    text = draft_path.read_text(encoding="utf-8")

    # Auto-extract if not provided
    if not title:
        title = extract_title(text) or ""
    if not description:
        description = extract_frontmatter_description(text) or extract_first_paragraph(text) or ""

    out_path = out_dir / "meta.json"
    # Preserve any extra fields (e.g. author) already in meta.json
    existing = {}
    if out_path.exists():
        try:
            existing = json.loads(out_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    meta = {
        **existing,
        "title":       title,
        "description": description,
        "url":         url or existing.get("url", ""),
    }
    out_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK]   {out_path}")
    print(f"  Title ({len(title)} chars): {title[:70]}")
    print(f"  Desc  ({len(description)} chars): {description[:80]}...")
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
