"""
fetch_sitemap.py — Fetch monx.team sitemap and write sitemap-candidates.json
to an article workspace directory.

Usage:
    python fetch_sitemap.py --out-dir workspace/article/my-slug/
    python fetch_sitemap.py --out-dir workspace/article/my-slug/ --types post page

Arguments:
    --out-dir   Article workspace directory. Writes sitemap-candidates.json here.
    --types     Which sitemap types to include (default: post page).
                Options: post, page, career, category, author.

Output files:
    sitemap-candidates.json  — List of URL objects with url and lastmod.
                               Used by match_internal_links.py in step 10.

Exit codes:
    0 — success
    1 — error (details printed to stderr)
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests is not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SITEMAP_INDEX = "https://monx.team/sitemap_index.xml"
DEFAULT_TYPES = ["post", "page"]
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


# ---------------------------------------------------------------------------
# Fetch helpers
# ---------------------------------------------------------------------------

def fetch_xml(url: str) -> ET.Element:
    """Fetch a URL and parse as XML. Follows redirects automatically."""
    response = requests.get(url, timeout=30, allow_redirects=True)
    if response.status_code != 200:
        print(f"ERROR: Got {response.status_code} fetching {url}", file=sys.stderr)
        sys.exit(1)
    return ET.fromstring(response.content)



def parse_urlset(root: ET.Element) -> list:
    """Extract {url, lastmod} entries from a <urlset> element."""
    entries = []
    for url_el in root.findall("sm:url", NS):
        loc     = url_el.findtext("sm:loc",     namespaces=NS)
        lastmod = url_el.findtext("sm:lastmod", namespaces=NS)
        if loc:
            entries.append({
                "url":     loc.strip(),
                "lastmod": lastmod.strip() if lastmod else None,
            })
    return entries


def parse_child_sitemap(url: str) -> list:
    """Fetch a child sitemap URL and return list of {url, lastmod} dicts."""
    return parse_urlset(fetch_xml(url))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(out_dir: Path, types: list, sitemap_url: str = None) -> bool:
    out_dir.mkdir(parents=True, exist_ok=True)

    index_url = sitemap_url or SITEMAP_INDEX
    print(f"[INFO] Fetching sitemap index: {index_url}")
    root = fetch_xml(index_url)

    # Detect flat sitemap (urlset) vs sitemap index (sitemapindex)
    tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
    if tag == "urlset":
        print("[INFO] Flat sitemap detected — reading URLs directly")
        all_entries = parse_urlset(root)
    else:
        child_urls = []
        for sitemap in root.findall("sm:sitemap", NS):
            loc = sitemap.findtext("sm:loc", namespaces=NS) or ""
            for t in types:
                if f"{t}-sitemap.xml" in loc:
                    child_urls.append(loc)
                    break

        if not child_urls:
            print(f"ERROR: No child sitemaps found for types: {types}", file=sys.stderr)
            return False

        print(f"[INFO] Found {len(child_urls)} child sitemap(s): {[u.split('/')[-1] for u in child_urls]}")

        all_entries = []
        for child_url in child_urls:
            print(f"[FETCH] {child_url}")
            entries = parse_child_sitemap(child_url)
            print(f"[OK]   {len(entries)} URLs")
            all_entries.extend(entries)

    # Deduplicate by URL
    seen = set()
    deduped = []
    for e in all_entries:
        if e["url"] not in seen:
            seen.add(e["url"])
            deduped.append(e)

    print(f"[INFO] {len(deduped)} total URLs after deduplication")

    out_path = out_dir / "sitemap-candidates.json"
    out_path.write_text(json.dumps(deduped, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK]   {out_path}")

    return True


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch monx.team sitemap and write sitemap-candidates.json.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--out-dir", required=True, help="Article workspace directory.")
    parser.add_argument("--sitemap-url", default=None,
                        help="Override the default sitemap index URL.")
    parser.add_argument("--types", nargs="+", default=DEFAULT_TYPES,
                        help="Sitemap types to include (default: post page).")
    return parser.parse_args()


def main():
    args = parse_args()
    ok = run(Path(args.out_dir), args.types, sitemap_url=args.sitemap_url)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
