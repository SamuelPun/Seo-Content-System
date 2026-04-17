"""
fetch_url.py — Fetch a URL and save clean markdown to disk.

Usage:
    python fetch_url.py --url "https://example.com/article" --out "serp-pages/1.md"
    python fetch_url.py --urls serp-urls.json --out-dir "serp-pages/"
    python fetch_url.py --urls serp-urls.json --out-dir "sources/"

Arguments:
    --url       Single URL to fetch.
    --urls      Path to a JSON file containing a list of URL strings,
                or a list of objects with a "url" key.
    --out       Output file path (used with --url).
    --out-dir   Output directory (used with --urls). Files are named 1.md, 2.md, etc.
                unless the JSON objects include a "slug" key.
    --delay     Seconds to wait between requests (default: 2).
    --timeout   Request timeout in seconds (default: 15).

Exit codes:
    0 — all fetches succeeded (or were skipped because file already exists)
    1 — one or more fetches failed (details printed to stderr)
"""

import argparse
import json
import sys
import time
from pathlib import Path

try:
    import trafilatura
except ImportError:
    print("ERROR: trafilatura is not installed. Run: pip install trafilatura", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Core fetch logic
# ---------------------------------------------------------------------------

def fetch_to_markdown(url: str, timeout: int = 15) -> str | None:
    """
    Fetch a URL and return clean markdown text, or None on failure.

    trafilatura handles:
    - Boilerplate removal (nav, ads, footers)
    - Main content extraction
    - Markdown formatting
    """
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return None

    text = trafilatura.extract(
        downloaded,
        output_format="markdown",
        include_comments=False,
        include_tables=True,
        no_fallback=False,          # allow fallback extractors if primary fails
        favor_recall=True,          # prefer more content over precision
    )

    return text  # may be None if extraction yields nothing


def write_output(content: str, path: Path) -> None:
    """Write content to path, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Single URL mode
# ---------------------------------------------------------------------------

def run_single(url: str, out_path: Path, timeout: int) -> bool:
    """Fetch one URL and write to out_path. Returns True on success."""
    if out_path.exists():
        print(f"[SKIP] Already exists: {out_path}")
        return True

    print(f"[FETCH] {url}")
    content = fetch_to_markdown(url, timeout)

    if not content:
        print(f"[FAIL] No content extracted from: {url}", file=sys.stderr)
        return False

    # Prepend source URL as metadata comment so it's traceable
    output = f"<!-- source: {url} -->\n\n{content}"
    write_output(output, out_path)
    print(f"[OK]   Saved {len(content):,} chars → {out_path}")
    return True


# ---------------------------------------------------------------------------
# Batch URL mode
# ---------------------------------------------------------------------------

def load_urls(json_path: Path) -> list[dict]:
    """
    Load URLs from a JSON file.

    Accepts two formats:
      - List of strings:  ["https://...", "https://..."]
      - List of objects:  [{"url": "https://...", "slug": "site-name"}, ...]

    Returns a list of dicts, always with at least a "url" key.
    """
    data = json.loads(json_path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        # Handle Serper-style output: {"organic": [...]}
        if isinstance(data, dict) and "organic" in data:
            data = data["organic"]
        else:
            print(f"ERROR: Expected a JSON array in {json_path}", file=sys.stderr)
            sys.exit(1)

    normalised = []
    for item in data:
        if isinstance(item, str):
            normalised.append({"url": item})
        elif isinstance(item, dict) and "url" in item:
            normalised.append(item)
        elif isinstance(item, dict) and "link" in item:
            # Serper uses "link" not "url"
            entry = dict(item)
            entry["url"] = entry.pop("link")
            normalised.append(entry)
        else:
            print(f"[WARN] Skipping unrecognised item in URL list: {item}", file=sys.stderr)

    return normalised


def run_batch(urls_file: Path, out_dir: Path, delay: float, timeout: int) -> bool:
    """Fetch all URLs from a JSON file. Returns True if all succeeded."""
    entries = load_urls(urls_file)
    if not entries:
        print("ERROR: No URLs found in input file.", file=sys.stderr)
        return False

    print(f"[INFO] {len(entries)} URLs to fetch → {out_dir}")
    all_ok = True

    for i, entry in enumerate(entries, start=1):
        url = entry["url"]

        # Determine output filename
        if "slug" in entry and entry["slug"]:
            filename = f"{entry['slug']}.md"
        else:
            filename = f"{i}.md"

        out_path = out_dir / filename

        success = run_single(url, out_path, timeout)
        if not success:
            all_ok = False

        # Polite delay between requests (skip after last one)
        if i < len(entries):
            time.sleep(delay)

    return all_ok


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch URLs and save clean markdown to disk.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--url", help="Single URL to fetch.")
    parser.add_argument("--urls", help="Path to JSON file with list of URLs.")
    parser.add_argument("--out", help="Output file path (used with --url).")
    parser.add_argument("--out-dir", help="Output directory (used with --urls).")
    parser.add_argument("--delay", type=float, default=2.0,
                        help="Seconds between requests in batch mode (default: 2).")
    parser.add_argument("--timeout", type=int, default=15,
                        help="Request timeout in seconds (default: 15).")
    return parser.parse_args()


def main():
    args = parse_args()

    # Validate argument combinations
    if args.url and args.urls:
        print("ERROR: Use either --url or --urls, not both.", file=sys.stderr)
        sys.exit(1)

    if not args.url and not args.urls:
        print("ERROR: Provide --url (single) or --urls (batch).", file=sys.stderr)
        sys.exit(1)

    if args.url and not args.out:
        print("ERROR: --url requires --out to specify the output file path.", file=sys.stderr)
        sys.exit(1)

    if args.urls and not args.out_dir:
        print("ERROR: --urls requires --out-dir to specify the output directory.", file=sys.stderr)
        sys.exit(1)

    # Run
    if args.url:
        ok = run_single(
            url=args.url,
            out_path=Path(args.out),
            timeout=args.timeout,
        )
    else:
        ok = run_batch(
            urls_file=Path(args.urls),
            out_dir=Path(args.out_dir),
            delay=args.delay,
            timeout=args.timeout,
        )

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
