import argparse
import json
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("ERROR: markdown is not installed. Run: pip install markdown", file=sys.stderr)
    sys.exit(1)


SITE_URL = "https://monx.team"


def load_json(path):
    if path and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def md_to_html(text):
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "toc"],
    )


def build_html(title, description, url, body_html, schemas, internal_links):
    # Inject internal links as data attribute on body for CMS use
    links_json = json.dumps(internal_links or [])

    schema_tags = ""
    for schema in (schemas or []):
        schema_tags += f'\n<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{url}">{schema_tags}
</head>
<body data-internal-link-candidates='{links_json}'>

{body_html}

</body>
</html>"""


def run(workspace: Path) -> bool:
    draft_path   = workspace / "draft.md"
    meta_path    = workspace / "meta.json"
    schema_path  = workspace / "schema.json"
    links_path   = workspace / "internal-link-candidates.json"

    if not draft_path.exists():
        print(f"ERROR: draft.md not found in {workspace}", file=sys.stderr)
        return False

    print(f"[INFO] Building output from {workspace}")

    draft_text     = draft_path.read_text(encoding="utf-8")
    meta           = load_json(meta_path)
    schemas        = load_json(schema_path)
    internal_links = load_json(links_path)

    title       = (meta or {}).get("title")       or "Untitled"
    description = (meta or {}).get("description") or ""
    url         = (meta or {}).get("url")         or f"{SITE_URL}/"

    body_html = md_to_html(draft_text)

    html = build_html(title, description, url, body_html, schemas, internal_links)

    out_path = workspace / "final.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"[OK]   {out_path}")

    # Summary
    word_count = len(draft_text.split())
    print(f"\n=== OUTPUT SUMMARY ===")
    print(f"  Title:       {title}")
    print(f"  URL:         {url}")
    print(f"  Word count:  {word_count}")
    print(f"  Schemas:     {len(schemas) if schemas else 0}")
    print(f"  Int. links:  {len(internal_links) if internal_links else 0} candidates embedded")
    print(f"  Output:      {out_path}")
    return True


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, help="Article workspace directory (e.g. workspace/article/my-slug/)")
    return parser.parse_args()


def main():
    args = parse_args()
    ok = run(Path(args.workspace))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
