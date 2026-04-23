"""Brand and content file generators — write structured markdown files from Q&A data."""

from __future__ import annotations

from datetime import date
from pathlib import Path


def write_profile(client_dir: Path, data: dict):
    today = date.today().isoformat()
    text = f"""# Client Profile — {data['name']}

---

## Basic information

**Client name:** {data['name']}
**Website:** {data['website']}
**Industry:** {data['industry']}
**Primary market:** {data['primary_market']}
**Onboarded:** {today}

---

## Content goals

{data['content_goals']}

---

## Sitemap

**Sitemap index:** {data['sitemap_url']}

---

## Asana

**Project URL:** {data.get('asana_url', '')}
**Project ID:** {data.get('asana_id', '')}

---

## Notes

{data.get('notes', '')}
"""
    (client_dir / "profile.md").write_text(text, encoding="utf-8")


def write_competitors(brand_dir: Path, data: dict):
    direct_rows = "\n".join(
        f"| {d} | |" for d in data.get("direct_competitors", [])
    ) or "| | |"

    avoid_rows = "\n".join(
        f"| {d} | |" for d in data.get("avoid_domains", [])
    ) or "| | |"

    trusted_rows = "\n".join(
        f"| {d} | |" for d in data.get("trusted_domains", [])
    ) or "| gov.uk | UK government |\n| irs.gov | US IRS |\n| hmrc.gov.uk | HMRC |"

    text = f"""# Competitors — {data['client_name']}

*Domains to never link to. Skills read this to avoid referencing or validating competitor content.*

---

## Direct competitors

| Domain | Notes |
|---|---|
{direct_rows}

---

## Indirect competitors / domains to avoid

| Domain | Why |
|---|---|
{avoid_rows}

---

## Domains we trust and can link to

*Primary sources, government bodies, official publications.*

| Domain | Type |
|---|---|
{trusted_rows}
"""
    (brand_dir / "competitors.md").write_text(text, encoding="utf-8")


def write_glossary(brand_dir: Path, data: dict):
    explain_rows = "\n".join(
        f"| {t['term']} | {t['explanation']} |"
        for t in data.get("explain_terms", [])
    ) or "| | |"

    avoid_rows = "\n".join(
        f"| {t['avoid']} | {t['use_instead']} |"
        for t in data.get("avoid_terms", [])
    ) or "| utilize | use |\n| leverage (verb) | use, apply, draw on |"

    text = f"""# Glossary — {data['client_name']}

*Approved terms, preferred spellings, and definitions. Skills use this to stay consistent across all articles.*

---

## Preferred spellings and capitalisation

| Term | Use this | Not this |
|---|---|---|
| | | |

---

## Terms to explain on first use

*Technical or legal terms that require a brief explanation when introduced.*

| Term | How to explain it |
|---|---|
{explain_rows}

---

## Terms to avoid

| Avoid | Use instead |
|---|---|
{avoid_rows}
"""
    (brand_dir / "glossary.md").write_text(text, encoding="utf-8")


def write_cta_library(brand_dir: Path, data: dict):
    consultation_cta = data.get("consultation_cta") or \
        "Book a call with a specialist — we'll tell you exactly where you stand in the first 30 minutes."

    text = f"""# CTA Library — {data['client_name']}

*Reusable CTA formats approved for this client. Writing skill picks the most relevant one for each article's angle and reader.*

---

## Format rules

- One CTA per article, at the end only
- Must connect directly to the article's angle and reader's core problem
- Never vague ("get in touch", "learn more", "contact us")
- Always low-pressure — earned, not pushed

---

## Approved CTAs

### Consultation
> {consultation_cta}

### Specific problem
> [Specific offer tied to article topic — fill in per article]

### Resource download
> [If a relevant resource exists — link to it here]

---

## CTAs to never use

- "Contact us to learn more"
- "Get in touch today"
- "Find out how we can help"
- "Start your journey"
- Any CTA that could appear on any article regardless of topic
"""
    (brand_dir / "cta-library.md").write_text(text, encoding="utf-8")


def write_content_index(content_dir: Path):
    index_path = content_dir / "_index.md"
    if not index_path.exists():
        index_path.write_text(
            "| Keyword | Status | Last edited |\n|---|---|---|\n",
            encoding="utf-8",
        )
