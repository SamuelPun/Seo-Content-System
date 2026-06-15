"""
Central configuration and shared constants for the SEO content system.
Imported by run_workflow.py and onboard_client.py.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Static paths
# ---------------------------------------------------------------------------

REPO_DIR    = Path(__file__).parent.parent.parent  # seo-content-system/
SCRIPTS_DIR = REPO_DIR / "scripts"
SKILLS_DIR  = REPO_DIR / "skills"
BRAND_TMPL  = REPO_DIR / "brand"  # de-ai-guidelines.md lives here

# ---------------------------------------------------------------------------
# Pipeline constants
# ---------------------------------------------------------------------------

STEPS = [
    "keyword",           # fetch_serp + fetch_url (SERP pages) → serp-urls.json, serp-pages/
    "angle",             # Claude Code session → angle.md
    "headline-outline",  # fetch_sitemap + Claude Code session → headline.md, outline.md
    "research",          # fetch_url (sources) → sources/
    "writing",           # Claude Code session → draft.md (+ banned phrase gate)
    "polish",            # scan scripts + Claude Code → editorial + mechanical cleanup → draft.md polished
    "links",             # build_page_index (incremental) + match_internal_links → candidates.json
    "output",            # validate_meta + generate_schema + build_output + generate_checklist → final.html + publish-checklist.md
]

HUMAN_GATES = {"angle", "headline-outline", "research", "polish"}

# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------

def normalise_slug(name: str) -> str:
    """Convert any article name to a filesystem-safe hyphenated slug."""
    slug = name.lower().strip()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    return slug.strip('-')


def get_content_base() -> Path:
    """Read CONTENT_BASE env var and return as Path, or exit with an error."""
    val = os.environ.get("CONTENT_BASE", "").strip()
    if not val:
        print("ERROR: CONTENT_BASE is not set. Add it to .env or export it before running.")
        sys.exit(1)
    return Path(val)


def load_client_profile(client_dir: Path) -> dict:
    """Parse profile.md and return a dict with known fields."""
    profile_path = client_dir / "profile.md"
    if not profile_path.exists():
        return {}
    text = profile_path.read_text(encoding="utf-8")
    data = {}
    m = re.search(r'\*\*Sitemap index:\*\*\s*(\S+)', text)
    if m:
        data["sitemap_url"] = m.group(1).strip()
    return data
