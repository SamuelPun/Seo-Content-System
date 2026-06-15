"""Fetch homepage and about page from a client's website for onboarding context."""

from __future__ import annotations

import trafilatura

from seo_system.onboard.scraper import list_all_sitemap_urls

_ABOUT_KEYWORDS = ("about", "team", "company", "our-story", "who-we-are", "meet")


def _fetch_text(url: str) -> str | None:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return None
    text = trafilatura.extract(
        downloaded,
        include_comments=False,
        include_tables=False,
        no_fallback=False,
    )
    if not text or len(text.split()) < 100:
        return None
    return text


def fetch_website_pages(website_url: str, sitemap_url: str = "") -> list[dict]:
    """Fetch homepage + first about-style page found in the sitemap.

    Returns a list of {url, text} dicts — 1 or 2 entries; empty list on total failure.
    """
    pages: list[dict] = []

    try:
        text = _fetch_text(website_url.rstrip("/"))
        if text:
            pages.append({"url": website_url, "text": text})
            print(f"    ✓ {website_url}")
    except Exception:
        pass

    if sitemap_url:
        all_urls = list_all_sitemap_urls(sitemap_url)
        about_candidates = [
            u for u in all_urls
            if any(kw in u.lower() for kw in _ABOUT_KEYWORDS)
        ]
        for url in about_candidates:
            try:
                text = _fetch_text(url)
                if text:
                    pages.append({"url": url, "text": text})
                    print(f"    ✓ {url}")
                    break
            except Exception:
                continue

    return pages
