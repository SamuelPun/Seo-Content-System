import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


def extract_title(text):
    match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    return match.group(1).strip() if match else None


def extract_headings(text):
    return re.findall(r'^#{2,3}\s+(.+)$', text, re.MULTILINE)


def extract_questions(text):
    headings = extract_headings(text)
    return [h for h in headings if h.strip().endswith('?')]


def detect_type(text):
    questions = extract_questions(text)
    steps = re.findall(r'(?:step\s+\d+|^\d+\.\s)', text, re.IGNORECASE | re.MULTILINE)

    if len(steps) >= 3:
        return "HowTo"
    if len(questions) >= 2:
        return "FAQPage"
    return "Article"


def build_article_schema(title, url, date_published, author=None, description=None,
                          publisher_name=None, publisher_url=None, date_modified=None):
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "url": url,
        "datePublished": date_published,
        "dateModified": date_modified or date_published,
        "publisher": {
            "@type": "Organization",
            "name": publisher_name or "",
            "url": publisher_url or "",
        }
    }
    if description:
        schema["description"] = description
    if author:
        schema["author"] = {"@type": "Person", "name": author}
    return schema


def build_faq_schema(questions_text):
    pairs = []
    parts = re.split(r'^#{2,3}\s+(.+\?)\s*$', questions_text, flags=re.MULTILINE)
    i = 1
    while i < len(parts) - 1:
        question = parts[i].strip()
        answer_block = parts[i+1].strip()
        answer = re.sub(r'#.*?\n', '', answer_block).strip()
        answer = re.sub(r'\s+', ' ', answer)[:300]
        if question and answer:
            pairs.append({
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer}
            })
        i += 2

    if not pairs:
        return None

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": pairs
    }


def build_howto_schema(title, text):
    steps = []
    headings = re.findall(r'^#{2,3}\s+(Step\s+\d+.+)$', text, re.MULTILINE | re.IGNORECASE)

    for i, heading in enumerate(headings):
        steps.append({
            "@type": "HowToStep",
            "name": heading.strip(),
            "position": i + 1,
        })

    if not steps:
        return None

    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": title,
        "step": steps
    }


def run(draft_path, meta_path, out_dir, url=None):
    if not draft_path.exists():
        print(f"ERROR: Draft not found: {draft_path}", file=sys.stderr)
        return False

    out_dir.mkdir(parents=True, exist_ok=True)
    text = draft_path.read_text(encoding="utf-8")
    title = extract_title(text) or "Untitled"
    today_str = date.today().isoformat()

    # Get URL, author, description, publisher from meta.json if available
    page_url = url
    meta_author = None
    meta_description = None
    meta_publisher_name = None
    meta_publisher_url = None
    meta = {}
    if meta_path and meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        page_url = page_url or meta.get("url")
        meta_author = meta.get("author")
        meta_description = meta.get("description")
        meta_publisher_name = meta.get("publisher_name")
        meta_publisher_url = meta.get("site_url")
    if not page_url:
        page_url = f"{meta_publisher_url or ''}/blog/placeholder-url/"

    # datePublished must stay fixed once set — re-running `output` (e.g. to fix a typo
    # and regenerate) should only ever move dateModified forward, not silently rewrite
    # the original publish date to today. Persisted in meta.json, which validate_meta.py
    # (run just before this in the output step) already preserves unknown fields on.
    date_published = meta.get("date_first_published") or today_str
    if meta_path and not meta.get("date_first_published"):
        meta["date_first_published"] = date_published
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    schema_type = detect_type(text)
    print(f"[INFO] Detected schema type: {schema_type}")

    schemas = []

    # Always include Article schema
    schemas.append(build_article_schema(
        title, page_url, date_published, meta_author, meta_description,
        meta_publisher_name, meta_publisher_url, date_modified=today_str,
    ))

    # Add FAQ or HowTo if detected
    if schema_type == "FAQPage":
        faq = build_faq_schema(text)
        if faq:
            schemas.append(faq)
    elif schema_type == "HowTo":
        howto = build_howto_schema(title, text)
        if howto:
            schemas.append(howto)

    out_path = out_dir / "schema.json"
    out_path.write_text(json.dumps(schemas, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK]   {out_path}")
    print("  Article schema:  ✓")
    print(f"  {schema_type} schema: {'✓' if len(schemas) > 1 else 'not applicable'}")
    return True


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft",   required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--meta",    default=None, help="Path to meta.json (optional)")
    parser.add_argument("--url",     default=None, help="Page URL (overrides meta.json)")
    return parser.parse_args()


def main():
    args = parse_args()
    meta_path = Path(args.meta) if args.meta else None
    ok = run(Path(args.draft), meta_path, Path(args.out_dir), args.url)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
