"""Fetch and extract article text from a client's blog for Voice DNA analysis."""

from __future__ import annotations

import xml.etree.ElementTree as ET

import requests
import trafilatura

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; SEOContentSystem/1.0)"}


def _fetch_xml(url: str) -> ET.Element:
    r = requests.get(url, timeout=20, headers=_HEADERS)
    r.raise_for_status()
    return ET.fromstring(r.content)


def _entries_from_urlset(root: ET.Element) -> list[dict]:
    """Return [{url, lastmod}] for every <url> entry in a urlset."""
    entries = []
    for url_el in root.findall("sm:url", NS):
        loc = url_el.findtext("sm:loc", namespaces=NS)
        if not loc:
            continue
        lastmod = url_el.findtext("sm:lastmod", namespaces=NS)
        entries.append({"url": loc.strip(), "lastmod": lastmod.strip() if lastmod else None})
    return entries


def _urls_from_urlset(root: ET.Element) -> list[str]:
    return [e["url"] for e in _entries_from_urlset(root)]


def _newest_first(entries: list[dict]) -> list[dict]:
    """Sort by lastmod descending; entries without a lastmod sort last."""
    return sorted(entries, key=lambda e: e["lastmod"] or "", reverse=True)


def _post_urls_from_sitemap(sitemap_url: str, want: int) -> list[str]:
    """Return up to `want` URLs from a sitemap index or urlset, newest first."""
    root = _fetch_xml(sitemap_url)
    tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag

    if tag != "sitemapindex":
        return [e["url"] for e in _newest_first(_entries_from_urlset(root))[:want]]

    # Sitemap index: prefer child sitemaps whose URL contains "post" or "blog",
    # most recently updated first.
    children = [
        {"url": el.text, "lastmod": sm.findtext("sm:lastmod", namespaces=NS)}
        for sm in root.findall("sm:sitemap", NS)
        for el in [sm.find("sm:loc", NS)]
        if el is not None and el.text
    ]
    priority = [c for c in children if any(k in c["url"] for k in ("post", "blog", "article"))]
    rest = [c for c in children if c not in priority]
    ordered = _newest_first(priority) + _newest_first(rest)

    entries: list[dict] = []
    for child in ordered:
        if len(entries) >= want:
            break
        try:
            child_root = _fetch_xml(child["url"])
            entries.extend(_entries_from_urlset(child_root))
        except Exception:
            continue

    return [e["url"] for e in _newest_first(entries)[:want]]


def list_all_sitemap_urls(sitemap_url: str) -> list[str]:
    """Return every URL in a sitemap index or urlset, with no post/blog filtering."""
    try:
        root = _fetch_xml(sitemap_url)
    except Exception:
        return []
    tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag

    if tag != "sitemapindex":
        return _urls_from_urlset(root)

    urls: list[str] = []
    child_locs = [
        el.text
        for sm in root.findall("sm:sitemap", NS)
        for el in [sm.find("sm:loc", NS)]
        if el is not None and el.text
    ]
    for child_url in child_locs:
        try:
            child_root = _fetch_xml(child_url)
            urls.extend(_urls_from_urlset(child_root))
        except Exception:
            continue
    return urls


def fetch_posts_for_voice_analysis(sitemap_url: str, max_posts: int = 20) -> list[dict]:
    """
    Fetch up to max_posts articles from sitemap_url.
    Returns list of {url, text} dicts with text trimmed to ~800 words.
    """
    # Fetch extra URLs in case some fail to extract
    candidates = _post_urls_from_sitemap(sitemap_url, max_posts * 3)

    posts: list[dict] = []
    for url in candidates:
        if len(posts) >= max_posts:
            break
        try:
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                continue
            text = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=False,
                no_fallback=False,
            )
            if not text or len(text.split()) < 150:
                continue
            words = text.split()
            if len(words) > 800:
                text = " ".join(words[:800]) + " [...]"
            posts.append({"url": url, "text": text})
            print(f"    ✓ {url}")
        except Exception:
            continue

    return posts
