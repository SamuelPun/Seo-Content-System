import argparse
import html
import json
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("ERROR: markdown is not installed. Run: pip install markdown", file=sys.stderr)
    sys.exit(1)


def load_json(path):
    if path and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def md_to_html(text):
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "toc"],
    )


def build_html(title, description, url, body_html, schemas):
    schema_tags = ""
    for schema in (schemas or []):
        schema_json = json.dumps(schema, indent=2).replace("</script>", "<\\/script>")
        schema_tags += f'\n<script type="application/ld+json">\n{schema_json}\n</script>'

    title = html.escape(title)
    description = html.escape(description)
    url = html.escape(url)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{url}">{schema_tags}
</head>
<body>

{body_html}

</body>
</html>"""


def run(workspace: Path) -> bool:
    editorial_dir = workspace / "editorial"
    data_dir      = workspace / "data"
    publish_dir   = workspace / "publish"
    publish_dir.mkdir(parents=True, exist_ok=True)

    draft_path   = editorial_dir / "draft.md"
    meta_path    = data_dir / "meta.json"
    schema_path  = data_dir / "schema.json"

    if not draft_path.exists():
        print(f"ERROR: editorial/draft.md not found in {workspace}", file=sys.stderr)
        return False

    print(f"[INFO] Building output from {workspace}")

    draft_text = draft_path.read_text(encoding="utf-8")
    meta       = load_json(meta_path)
    schemas    = load_json(schema_path)

    title       = (meta or {}).get("title")       or "Untitled"
    description = (meta or {}).get("description") or ""
    url         = (meta or {}).get("url")         or ""

    body_html = md_to_html(draft_text)

    html = build_html(title, description, url, body_html, schemas)

    out_path = publish_dir / "final.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"[OK]   {out_path}")

    # Summary
    word_count = len(draft_text.split())
    print("\n=== OUTPUT SUMMARY ===")
    print(f"  Title:       {title}")
    print(f"  URL:         {url}")
    print(f"  Word count:  {word_count}")
    print(f"  Schemas:     {len(schemas) if schemas else 0}")
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
