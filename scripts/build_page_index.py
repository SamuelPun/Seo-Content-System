"""
build_page_index.py — Build or incrementally update a keyword index of all pages on a client site.

Reads the client sitemap, fetches page content using trafilatura, extracts
keyphrases using YAKE, and writes a structured page-index.json for use by
match_internal_links.py.

On first run (empty index): crawls every page in the sitemap.
On subsequent runs: only crawls pages whose lastmod has changed or that are new.

Usage:
    python build_page_index.py --page-index brand/page-index.json --sitemap-url https://monx.team/sitemap_index.xml
    python build_page_index.py --page-index brand/page-index.json  # uses site_url from existing index

Dependencies:
    pip install trafilatura yake beautifulsoup4 requests
"""

import argparse
import json
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    import trafilatura
except ImportError:
    print("ERROR: trafilatura not installed. Run: pip install trafilatura", file=sys.stderr)
    sys.exit(1)

try:
    import yake
except ImportError:
    print("ERROR: yake not installed. Run: pip install yake", file=sys.stderr)
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 not installed. Run: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)


NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
DEFAULT_TYPES = ["post", "page"]

_kw_extractor = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.7, top=25, features=None)


# ---------------------------------------------------------------------------
# Sitemap fetching
# ---------------------------------------------------------------------------

def _fetch_xml(url: str) -> ET.Element | None:
    try:
        r = requests.get(url, timeout=20, allow_redirects=True)
        if r.status_code != 200:
            print(f"  WARN: {r.status_code} fetching {url}", file=sys.stderr)
            return None
        return ET.fromstring(r.content)
    except Exception as e:
        print(f"  WARN: failed to fetch {url}: {e}", file=sys.stderr)
        return None


def fetch_sitemap_entries(sitemap_index_url: str, types: list) -> list[dict]:
    """Return [{url, lastmod}] from all matching child sitemaps."""
    root = _fetch_xml(sitemap_index_url)
    if root is None:
        return []

    child_urls = []
    for sitemap in root.findall("sm:sitemap", NS):
        loc = sitemap.findtext("sm:loc", namespaces=NS) or ""
        for t in types:
            if f"{t}-sitemap.xml" in loc:
                child_urls.append(loc)
                break

    entries = []
    for child_url in child_urls:
        child = _fetch_xml(child_url)
        if child is None:
            continue
        for url_el in child.findall("sm:url", NS):
            loc     = url_el.findtext("sm:loc",     namespaces=NS)
            lastmod = url_el.findtext("sm:lastmod", namespaces=NS)
            if loc:
                entries.append({
                    "url":     loc.strip(),
                    "lastmod": lastmod.strip() if lastmod else None,
                })

    return entries


# ---------------------------------------------------------------------------
# Page crawling
# ---------------------------------------------------------------------------

_NAV_STOPS = {
    "got a question", "get in touch", "learn more", "related posts",
    "related articles", "contact us", "contact your", "newsletter",
    "subscribe", "recent posts", "you may also like", "read more",
}


def extract_headings(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main") or soup.find("article") or soup
    headings = []
    seen = set()
    for tag in main.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(strip=True)
        if not text:
            continue
        if text.lower() in _NAV_STOPS or any(s in text.lower() for s in _NAV_STOPS):
            break
        if text not in seen:
            headings.append(text)
            seen.add(text)
    return headings


def extract_keyphrases(text: str) -> list[str]:
    if not text or len(text.strip()) < 50:
        return []
    # Drop the first 60 words to skip bylines / author-date noise
    words = text.split()
    text = " ".join(words[60:]) if len(words) > 60 else text
    try:
        results = _kw_extractor.extract_keywords(text)
        # lower score = more relevant; return phrases only
        return [phrase for phrase, _score in results]
    except Exception:
        return []


def crawl_page(url: str) -> dict | None:
    try:
        html = trafilatura.fetch_url(url)
        if not html:
            return None

        body_text = trafilatura.extract(
            html,
            include_tables=False,
            include_comments=False,
        ) or ""

        metadata = trafilatura.extract_metadata(html)
        title = (metadata.title or "") if metadata else ""

        headings = extract_headings(html)

        full_text = " ".join(filter(None, [title] + headings + [body_text]))
        keyphrases = extract_keyphrases(full_text)

        return {
            "title":      title,
            "headings":   headings,
            "keyphrases": keyphrases,
        }
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(page_index_path: Path, sitemap_url: str, types: list, delay: float) -> bool:
    # Load existing index
    existing_data = {}
    client = ""
    if page_index_path.exists():
        try:
            raw = json.loads(page_index_path.read_text(encoding="utf-8"))
            client = raw.get("client", "")
            for page in raw.get("pages", []):
                existing_data[page["url"]] = page
        except Exception:
            pass

    print(f"[INFO] Fetching sitemap: {sitemap_url}")
    sitemap_entries = fetch_sitemap_entries(sitemap_url, types)
    if not sitemap_entries:
        print("ERROR: No sitemap entries found. Check the sitemap URL and types.", file=sys.stderr)
        return False
    print(f"[INFO] {len(sitemap_entries)} pages in sitemap")
    print(f"[INFO] {len(existing_data)} pages in existing index")

    # Determine which pages need crawling
    to_crawl = []
    for entry in sitemap_entries:
        url = entry["url"]
        lastmod = entry.get("lastmod")
        if url not in existing_data:
            to_crawl.append(entry)
        elif lastmod and existing_data[url].get("lastmod") != lastmod:
            to_crawl.append(entry)

    print(f"[INFO] {len(to_crawl)} pages to crawl (new or updated)")

    if not to_crawl:
        print("[OK]   Index is up to date — nothing to crawl")
        return True

    # Crawl
    for i, entry in enumerate(to_crawl, 1):
        url = entry["url"]
        print(f"  [{i:>3}/{len(to_crawl)}] {url}")
        result = crawl_page(url)
        if result:
            existing_data[url] = {
                "url":        url,
                "lastmod":    entry.get("lastmod"),
                "title":      result["title"],
                "headings":   result["headings"],
                "keyphrases": result["keyphrases"],
            }
            print(f"         → {len(result['keyphrases'])} keyphrases, {len(result['headings'])} headings")
        else:
            print(f"         → skipped (fetch failed)")

        if i < len(to_crawl):
            time.sleep(delay)

    # Write updated index — preserve order (sitemap order)
    sitemap_urls = [e["url"] for e in sitemap_entries]
    pages = [existing_data[url] for url in sitemap_urls if url in existing_data]

    output = {
        "client":       client,
        "site_url":     sitemap_url,
        "last_crawled": datetime.now(timezone.utc).isoformat(),
        "pages":        pages,
    }
    page_index_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[OK]   {page_index_path} — {len(pages)} pages indexed")
    return True


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build or update a keyword index of client site pages."
    )
    parser.add_argument("--page-index",   required=True, help="Path to page-index.json (created if missing)")
    parser.add_argument("--sitemap-url",  default=None,  help="Sitemap index URL (reads site_url from existing index if omitted)")
    parser.add_argument("--types",        nargs="+", default=DEFAULT_TYPES, help="Sitemap types to include (default: post page)")
    parser.add_argument("--delay",        type=float, default=1.0, help="Seconds between page requests (default: 1.0)")
    return parser.parse_args()


def main():
    args = parse_args()
    page_index_path = Path(args.page_index)

    sitemap_url = args.sitemap_url
    if not sitemap_url:
        # Try to read site_url from existing index
        if page_index_path.exists():
            try:
                raw = json.loads(page_index_path.read_text(encoding="utf-8"))
                sitemap_url = raw.get("site_url", "").rstrip("/") + "/sitemap_index.xml"
            except Exception:
                pass
        if not sitemap_url:
            print("ERROR: --sitemap-url required when page-index.json has no site_url.", file=sys.stderr)
            sys.exit(1)

    ok = run(page_index_path, sitemap_url, args.types, args.delay)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
