#!/usr/bin/env python3
"""
onboard_client.py — Interactive client onboarding for the SEO Content System.

Creates the full client folder structure under CONTENT_BASE and generates all
brand files from a guided Q&A session. Claude synthesises the brand-voice-card
and audience profiles from your answers.

Usage:
    python3 onboard_client.py --client monx
    python3 onboard_client.py  # will prompt for client slug
"""

import argparse
import shutil
import sys

from seo_system.config import BRAND_TMPL, get_content_base, normalise_slug
from seo_system.onboard.claude import generate_claude_files, generate_voice_dna
from seo_system.onboard.prompts import ask, confirm, header
from seo_system.onboard.qa import build_qa_text, run_qa
from seo_system.onboard.scraper import fetch_posts_for_voice_analysis
from seo_system.onboard.writers import (
    write_competitors,
    write_content_index,
    write_cta_library,
    write_glossary,
    write_profile,
)


def main():
    parser = argparse.ArgumentParser(description="Onboard a new client for the SEO Content System")
    parser.add_argument("--client", default=None, help="Client slug (e.g. monx)")
    args = parser.parse_args()

    content_base = get_content_base()

    print()
    print("  ┌─────────────────────────────────────────────────┐")
    print("  │  SEO Content System — Client Onboarding         │")
    print("  └─────────────────────────────────────────────────┘")

    client_slug = args.client or ask("Client slug (lowercase, hyphenated, e.g. monx):")
    client_slug = normalise_slug(client_slug)

    client_dir = content_base / client_slug
    if client_dir.exists():
        print(f"\n  WARNING: {client_dir} already exists.")
        if not confirm("Continue and overwrite existing files?"):
            print("  Cancelled.")
            sys.exit(0)

    data = run_qa(client_slug)
    data["client_name"] = data["name"]

    header("Building folder structure")
    brand_dir   = client_dir / "brand"
    content_dir = client_dir / "content"
    brand_dir.mkdir(parents=True, exist_ok=True)
    content_dir.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ {client_dir}")
    print(f"  ✓ {brand_dir}")
    print(f"  ✓ {content_dir}")

    write_profile(client_dir, data)
    print("  ✓ profile.md")
    write_competitors(brand_dir, data)
    print("  ✓ brand/competitors.md")
    write_glossary(brand_dir, data)
    print("  ✓ brand/glossary.md")
    write_cta_library(brand_dir, data)
    print("  ✓ brand/cta-library.md")
    write_content_index(content_dir)
    print("  ✓ content/_index.md")

    de_ai_src = BRAND_TMPL / "de-ai-guidelines.md"
    if de_ai_src.exists():
        shutil.copy2(de_ai_src, brand_dir / "de-ai-guidelines.md")
        print("  ✓ brand/de-ai-guidelines.md (copied from repo)")
    else:
        print("  ✗ de-ai-guidelines.md not found in repo brand/ — copy manually")

    header("Voice DNA — analyse existing blog posts")
    sitemap_url = data.get("sitemap_url", "")
    if sitemap_url and confirm(
        "Fetch existing blog posts to extract Voice DNA? (recommended if the client has published content)"
    ):
        max_posts = 20
        print(f"\n  Fetching up to {max_posts} posts from {sitemap_url}...\n")
        try:
            posts = fetch_posts_for_voice_analysis(sitemap_url, max_posts=max_posts)
        except Exception as exc:
            print(f"  ✗ Could not fetch posts: {exc}")
            posts = []
        if posts:
            print(f"\n  ✓ {len(posts)} posts extracted")
            generate_voice_dna(brand_dir, posts, data["name"])
        else:
            print("  ✗ No posts extracted — skipping Voice DNA")
    else:
        print("  Skipped — voice-dna.md can be generated later by re-running with --voice-dna")

    header("Generating brand voice files with Claude")
    generate_claude_files(brand_dir, build_qa_text(data), data["name"])

    print()
    print("  ┌─────────────────────────────────────────────────┐")
    print(f"  │  {data['name']} onboarded successfully{'':>21}│")
    print("  └─────────────────────────────────────────────────┘")
    print()
    print(f"  Client folder : {client_dir}")
    print(f"  Brand folder  : {brand_dir}")
    print()
    print("  Next steps:")
    print("    1. Review brand/brand-voice-card.md — edit anything Claude got wrong")
    print("    2. Review brand/audience-profiles.md — fill any gaps")
    print("    3. Run your first article:")
    print(f"       python3 run_workflow.py --client {client_slug} --article \"your keyword\" --step all")
    print()


