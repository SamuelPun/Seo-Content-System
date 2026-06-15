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


def _urls_from_urlset(root: ET.Element) -> list[str]:
    return [
        el.text for el in root.findall(".//sm:loc", NS)
        if el.text
    ]


def _post_urls_from_sitemap(sitemap_url: str, want: int) -> list[str]:
    """Return up to `want` URLs from a sitemap index or urlset."""
    root = _fetch_xml(sitemap_url)
    tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag

    if tag != "sitemapindex":
        return _urls_from_urlset(root)[:want]

    # Sitemap index: prefer child sitemaps whose URL contains "post" or "blog"
    child_locs = [
        el.text
        for sm in root.findall("sm:sitemap", NS)
        for el in [sm.find("sm:loc", NS)]
        if el is not None and el.text
    ]

    priority = [u for u in child_locs if any(k in u for k in ("post", "blog", "article"))]
    ordered = priority + [u for u in child_locs if u not in priority]

    urls: list[str] = []
    for child_url in ordered:
        if len(urls) >= want:
            break
        try:
            child_root = _fetch_xml(child_url)
            urls.extend(_urls_from_urlset(child_root))
        except Exception:
            continue

    return urls[:want]


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
