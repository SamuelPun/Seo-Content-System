#!/usr/bin/env python3
"""
onboard_client.py — Interactive client onboarding for the SEO Content System.

Usage:
    python3 onboard_client.py --client monx
    python3 onboard_client.py  # will prompt for client slug
"""
from seo_system.cli.onboard import main

if __name__ == "__main__":
    main()
