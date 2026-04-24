"""
fetch_serp.py — Fetch SERP overview from Ahrefs API v3 and write
serp-urls.json and paa.json to an article workspace directory.

Usage:
    python fetch_serp.py --keyword "us expat tax" --country us --out-dir workspace/article/my-slug/
    python fetch_serp.py --keyword "us expat tax" --country us --out-dir workspace/article/my-slug/ --top 10

Arguments:
    --keyword   Target keyword (required).
    --country   Two-letter country code, e.g. us, gb, au (default: us).
    --out-dir   Article workspace directory. Writes serp-urls.json and paa.json here.
    --top       Number of organic positions to request from API (default: 10).

Environment:
    AHREFS_API_KEY  — required. Set in .env file or shell environment.

Output files:
    serp-urls.json  — Top organic results, one per position, sorted ascending.
                      Nulls filtered out. Sitelinks deduplicated.
    paa.json        — People Also Ask questions extracted from SERP features.

How the API response is interpreted:
    - position=1 with null URL  → SERP feature (AI overview, image pack, etc.) → skip
    - Null metrics + question title → PAA → paa.json
    - Multiple entries at same position from same domain → sitelinks → keep first only
    - Entries with a real URL and at least some metrics → organic → serp-urls.json

Exit codes:
    0 — success
    1 — error (details printed to stderr)
"""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("ERROR: requests is not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from ddgs import DDGS
    _DDG_AVAILABLE = True
except ImportError:
    _DDG_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional — key can be set in shell environment directly


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

AHREFS_ENDPOINT = "https://api.ahrefs.com/v3/serp-overview/serp-overview"

# Fields to request. traffic, keywords, refdomains cost extra units but are
# essential for competitive analysis — worth the cost.
SELECT_FIELDS = ",".join([
    "position",
    "url",
    "title",
    "domain_rating",
    "url_rating",
    "traffic",
    "keywords",
    "backlinks",
    "refdomains",
])


def fetch_serp(keyword: str, country: str, top: int, api_key: str) -> list[dict]:
    """Call the Ahrefs SERP Overview API and return raw positions list."""
    params = {
        "keyword": keyword,
        "country": country,
        "top_positions": top,
        "select": SELECT_FIELDS,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }

    response = requests.get(AHREFS_ENDPOINT, params=params, headers=headers, timeout=30)

    if response.status_code == 401:
        print("ERROR: Invalid API key.", file=sys.stderr)
        sys.exit(1)
    if response.status_code == 403:
        print("ERROR: API key does not have permission for this endpoint.", file=sys.stderr)
        sys.exit(1)
    if response.status_code == 429:
        print("ERROR: Rate limit hit. Wait a moment and retry.", file=sys.stderr)
        sys.exit(1)
    if response.status_code != 200:
        print(f"ERROR: API returned {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)

    data = response.json()
    return data.get("positions", [])


# ---------------------------------------------------------------------------
# DDG fallback
# ---------------------------------------------------------------------------

def fetch_serp_ddg(keyword: str, top: int) -> list[dict]:
    """Fetch top organic results via DuckDuckGo when Ahrefs has no data.

    Returns organic-shaped dicts with null SEO metrics and a snippet field.
    PAA is not available via DDG — callers should write an empty paa.json.
    """
    if not _DDG_AVAILABLE:
        print("ERROR: ddgs is not installed. Run: pip install ddgs", file=sys.stderr)
        return []

    results = DDGS().text(keyword, max_results=top)
    organic = []
    for i, r in enumerate(results or [], start=1):
        organic.append({
            "position":      i,
            "url":           r.get("href"),
            "title":         r.get("title"),
            "snippet":       r.get("body"),
            "domain_rating": None,
            "url_rating":    None,
            "traffic":       None,
            "keywords":      None,
            "backlinks":     None,
            "refdomains":    None,
        })
    return organic


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

def root_domain(url: str) -> str:
    """Extract root domain from a URL for sitelink deduplication."""
    try:
        return urlparse(url).netloc
    except Exception:
        return url


def is_paa(entry: dict) -> bool:
    """
    PAA entries have a real URL but null metrics, and their title is a question.
    """
    return (
        entry.get("url") is not None
        and entry.get("domain_rating") is None
        and entry.get("title") is not None
        and entry["title"].strip().endswith("?")
    )


def is_serp_feature(entry: dict) -> bool:
    """SERP features have no URL at all."""
    return entry.get("url") is None


def is_organic(entry: dict) -> bool:
    """Organic results have a URL and at least a domain_rating value."""
    return (
        entry.get("url") is not None
        and entry.get("domain_rating") is not None
    )


def parse_positions(raw: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Split raw API positions into:
      - organic: real ranking pages, one per position (sitelinks deduplicated)
      - paa: People Also Ask questions

    Returns (organic_results, paa_questions)
    """
    organic = []
    paa = []
    seen_positions = set()
    seen_domains = {}

    for entry in raw:
        if is_serp_feature(entry):
            continue

        if is_paa(entry):
            paa.append({
                "question": entry["title"].strip(),
                "source_url": entry["url"],
            })
            continue

        if is_organic(entry):
            pos = entry["position"]
            domain = root_domain(entry["url"])

            # Skip sitelinks: same position, same domain as one we already took
            if pos in seen_domains and seen_domains[pos] == domain:
                continue

            # Skip if we already have a result at this position
            if pos in seen_positions:
                continue

            seen_positions.add(pos)
            seen_domains[pos] = domain

            organic.append({
                "position":      pos,
                "url":           entry["url"],
                "title":         entry.get("title"),
                "domain_rating": entry.get("domain_rating"),
                "url_rating":    entry.get("url_rating"),
                "traffic":       entry.get("traffic"),
                "keywords":      entry.get("keywords"),
                "backlinks":     entry.get("backlinks"),
                "refdomains":    entry.get("refdomains"),
            })

    organic.sort(key=lambda r: r["position"])
    return organic, paa


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(keyword: str, country: str, top: int, out_dir: Path, api_key: str | None) -> bool:
    out_dir.mkdir(parents=True, exist_ok=True)

    organic = []
    paa = []
    source = "ahrefs"

    if api_key:
        print(f"[INFO] Fetching SERP via Ahrefs: '{keyword}' / {country.upper()} / top {top}")
        raw = fetch_serp(keyword, country, top, api_key)
        print(f"[INFO] {len(raw)} raw positions returned from Ahrefs")
        organic, paa = parse_positions(raw)
        print(f"[INFO] {len(organic)} organic results, {len(paa)} PAA questions")

    if not organic:
        if api_key:
            print(f"[WARN] Ahrefs returned no organic results for '{keyword}' — falling back to DuckDuckGo")
        else:
            print(f"[INFO] No AHREFS_API_KEY — fetching SERP via DuckDuckGo: '{keyword}'")
        source = "duckduckgo"
        organic = fetch_serp_ddg(keyword, top)
        print(f"[INFO] {len(organic)} results from DuckDuckGo (SEO metrics unavailable)")

    # Write serp-urls.json
    serp_path = out_dir / "serp-urls.json"
    serp_path.write_text(json.dumps(organic, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK]   {serp_path}")

    # Write paa.json (empty when using DDG — long-tail keywords rarely have PAA boxes)
    paa_path = out_dir / "paa.json"
    paa_path.write_text(json.dumps(paa, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK]   {paa_path}")

    # Summary table
    print(f"\n=== SERP SUMMARY (source: {source}) ===")
    print(f"{'Pos':>3}  {'DR':>4}  {'Traffic':>8}  URL")
    print("-" * 65)
    for r in organic:
        pos     = str(r["position"]).rjust(3)
        dr      = str(r["domain_rating"] or "-").rjust(4)
        traffic = str(r["traffic"] or "-").rjust(8)
        url     = r["url"] or ""
        if len(url) > 52:
            url = url[:49] + "..."
        print(f"{pos}  {dr}  {traffic}  {url}")

    if paa:
        print("\n=== PEOPLE ALSO ASK ===")
        for q in paa:
            print(f"  * {q['question']}")

    return True


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch Ahrefs SERP overview and write serp-urls.json + paa.json.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--keyword",  required=True, help="Target keyword.")
    parser.add_argument("--country",  default="us",  help="Two-letter country code (default: us).")
    parser.add_argument("--out-dir",  required=True, help="Article workspace directory.")
    parser.add_argument("--top",      type=int, default=10, help="Number of top positions to fetch (default: 10).")
    return parser.parse_args()


def main():
    args = parse_args()

    api_key = os.environ.get("AHREFS_API_KEY")
    if not api_key:
        print("[WARN] AHREFS_API_KEY not set — will use DuckDuckGo fallback.")

    ok = run(
        keyword=args.keyword,
        country=args.country,
        top=args.top,
        out_dir=Path(args.out_dir),
        api_key=api_key,
    )
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
