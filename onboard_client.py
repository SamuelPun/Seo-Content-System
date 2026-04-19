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
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import os

REPO_DIR   = Path(__file__).parent
BRAND_TMPL = REPO_DIR / "brand"  # repo brand/ — de-ai-guidelines.md lives here


# ---------------------------------------------------------------------------
# Terminal helpers
# ---------------------------------------------------------------------------

def header(text: str):
    width = 54
    print()
    print(f"  {'─' * width}")
    print(f"  {text}")
    print(f"  {'─' * width}")
    print()


def ask(prompt: str, default: str = "") -> str:
    """Single-line prompt. Returns stripped input, or default if empty."""
    hint = f" [{default}]" if default else ""
    try:
        raw = input(f"  {prompt}{hint}\n  → ").strip()
    except KeyboardInterrupt:
        print("\n\n  Onboarding cancelled.")
        sys.exit(0)
    return raw if raw else default


def ask_multiline(prompt: str) -> str:
    """Multi-line prompt. User types lines, blank line to finish."""
    print(f"  {prompt}")
    print("  (blank line to finish)")
    lines = []
    try:
        while True:
            line = input("  → ")
            if line == "":
                break
            lines.append(line.strip())
    except KeyboardInterrupt:
        print("\n\n  Onboarding cancelled.")
        sys.exit(0)
    return "\n".join(lines)


def ask_list(prompt: str) -> list[str]:
    """Ask for one item per line. Returns list of non-empty strings."""
    raw = ask_multiline(prompt)
    return [l for l in raw.splitlines() if l.strip()]


def confirm(prompt: str) -> bool:
    try:
        raw = input(f"  {prompt} [y/N] → ").strip().lower()
    except KeyboardInterrupt:
        print("\n\n  Onboarding cancelled.")
        sys.exit(0)
    return raw in ("y", "yes")


# ---------------------------------------------------------------------------
# File generators
# ---------------------------------------------------------------------------

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
            encoding="utf-8"
        )


# ---------------------------------------------------------------------------
# Claude-generated files
# ---------------------------------------------------------------------------

BRAND_VOICE_PROMPT = """\
You are a brand strategist. Based on the client Q&A below, write a brand voice reference card
for a content team. The card will be read by a writer before every article.

Output ONLY the brand-voice-card.md file content. No preamble, no explanation outside the file.

The card must have these exact sections (use this structure):
# {client_name} — Voice Reference Card
*Version 1.0 | {month_year} | Paste at the top of any writing prompt*

---

## Core character
[2-3 sentences. What kind of voice is this? What's the register? What should the reader feel?]

---

## Voice patterns (apply always)
[5-7 bullet points. Each starts with a bolded principle, then 1-2 sentences of instruction.]

---

## Never do this
[Bullet list of specific things to avoid — tone, phrasing, structure. Be concrete, not vague.]

---

## Vocabulary
**Reach for:** [words and phrases that sound like this client]
**Avoid with alternatives:** [word → use instead | word → use instead]
**Jargon policy:** [when to use technical terms, when to explain them]

---

## Register by content type
[Short table or list: Blog / Service pages / CTAs / Technical / Social — one line each]

---

## The one thing
[One sentence. What should every piece of content leave the reader feeling?]

---

CLIENT Q&A
==========
{qa_text}
"""

AUDIENCE_PROMPT = """\
You are a content strategist. Based on the client Q&A below, write an audience profiles document.

Output ONLY the audience-profiles.md file content. No preamble, no explanation outside the file.

Write 2 profiles (or 3 if the Q&A clearly describes 3 distinct segments). Each profile must follow
this structure exactly:

## Profile N — [Descriptive name for this segment]

**Who they are:**
[1-2 sentences — demographics, occupation, life situation]

**Their situation right now:**
[2-3 sentences — what just happened or is happening that brought them to this topic]

**What they know already:**
[1-2 sentences — assumed prior knowledge]

**What they are confused or anxious about:**
[2-3 sentences — their specific worry or blind spot]

**What a successful article does for them:**
[1-2 sentences — what they leave knowing or feeling]

---

Start the file with:
# Audience Profiles — {client_name}

*Each profile describes a specific reader segment. Skills read this to calibrate tone, assumed knowledge, and what the reader actually needs resolved.*

---

CLIENT Q&A
==========
{qa_text}
"""


def call_claude(prompt: str) -> str | None:
    """Run Claude in print mode and return stdout."""
    result = subprocess.run(
        ["claude", "--print", "--dangerously-skip-permissions"],
        input=prompt,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def generate_claude_files(brand_dir: Path, qa_text: str, client_name: str):
    from datetime import date
    month_year = date.today().strftime("%B %Y")

    print("  → Generating brand-voice-card.md with Claude...")
    bv_prompt = BRAND_VOICE_PROMPT.format(
        client_name=client_name,
        month_year=month_year,
        qa_text=qa_text
    )
    bv_content = call_claude(bv_prompt)
    if bv_content:
        (brand_dir / "brand-voice-card.md").write_text(bv_content + "\n", encoding="utf-8")
        print("  ✓ brand-voice-card.md written")
    else:
        print("  ✗ Claude failed — writing placeholder brand-voice-card.md")
        (brand_dir / "brand-voice-card.md").write_text(
            f"# {client_name} — Voice Reference Card\n\n*Generated from onboarding Q&A — Claude was not available. Fill in manually.*\n\n## Core character\n\n## Voice patterns\n\n## Never do this\n\n## Vocabulary\n\n## The one thing\n",
            encoding="utf-8"
        )

    print("  → Generating audience-profiles.md with Claude...")
    ap_prompt = AUDIENCE_PROMPT.format(client_name=client_name, qa_text=qa_text)
    ap_content = call_claude(ap_prompt)
    if ap_content:
        (brand_dir / "audience-profiles.md").write_text(ap_content + "\n", encoding="utf-8")
        print("  ✓ audience-profiles.md written")
    else:
        print("  ✗ Claude failed — writing placeholder audience-profiles.md")
        (brand_dir / "audience-profiles.md").write_text(
            f"# Audience Profiles — {client_name}\n\n*Fill in manually.*\n\n## Profile 1 — [Name]\n\n**Who they are:**\n\n**Their situation right now:**\n\n**What they know already:**\n\n**What they are confused or anxious about:**\n\n**What a successful article does for them:**\n",
            encoding="utf-8"
        )


# ---------------------------------------------------------------------------
# Q&A flow
# ---------------------------------------------------------------------------

def run_qa(client_slug: str) -> dict:
    data = {"slug": client_slug}

    header("PART 1 — Basic information")
    data["name"] = ask("Client name (e.g. Monx):")
    data["website"] = ask("Website URL (e.g. https://monx.team):")
    data["industry"] = ask("Industry / niche (e.g. US/UK tax advisory):")
    data["primary_market"] = ask("Primary market — who reads their content?")
    data["sitemap_url"] = ask(
        "Sitemap index URL (e.g. https://example.com/sitemap_index.xml):",
        default=f"{data['website'].rstrip('/')}/sitemap_index.xml"
    )

    header("PART 2 — Content goals")
    print("  What should this content achieve? List goals, one per line.")
    goals = ask_list("Content goals:")
    data["content_goals"] = "\n".join(f"- {g}" for g in goals) if goals else "- TBD"

    header("PART 3 — Brand voice")
    print("  Answer these to help Claude generate the brand voice card.\n")

    data["voice_style"] = ask("Describe their writing style in 2-3 words:")
    data["reader_feeling"] = ask("What should a reader feel after reading their content?")
    data["voice_phrases"] = ask_list(
        "List 5 words or phrases that sound distinctly 'them' (one per line):"
    )
    data["voice_never"] = ask_list(
        "List 3-5 things they NEVER do in writing — tone, structure, phrasing (one per line):"
    )
    data["differentiator"] = ask("What makes them different from other providers in this space?")
    data["jargon_policy"] = ask(
        "Technical terms — explain on first use, or assume the reader knows them?",
        default="Explain on first use"
    )
    data["extra_voice_notes"] = ask("Anything else about their voice or writing style? (Enter to skip):")

    header("PART 4 — Audience")
    print("  Describe who reads their content.\n")

    data["audience_segments"] = []
    for i in range(1, 4):
        segment_name = ask(f"Segment {i} name (e.g. 'US expat in London') — Enter to stop:")
        if not segment_name:
            break
        segment = {"name": segment_name}
        segment["who"] = ask(f"  [{segment_name}] Who are they? (demographics, situation):")
        segment["situation"] = ask(f"  [{segment_name}] What just happened that brought them to this topic?")
        segment["anxiety"] = ask(f"  [{segment_name}] What are they confused or anxious about?")
        segment["success"] = ask(f"  [{segment_name}] What does a successful article do for them?")
        data["audience_segments"].append(segment)

    header("PART 5 — Competitors and trusted domains")

    data["direct_competitors"] = ask_list(
        "Direct competitor domains to NEVER link to (one per line, e.g. competitor.com):"
    )
    data["avoid_domains"] = ask_list(
        "Other domains to avoid linking to (one per line) — Enter to skip:"
    )

    print()
    print("  Default trusted domains: gov.uk, irs.gov, hmrc.gov.uk")
    extra_trusted = ask_list(
        "Additional trusted domains to add (one per line) — Enter to skip:"
    )
    data["trusted_domains"] = ["gov.uk", "irs.gov", "hmrc.gov.uk"] + extra_trusted

    header("PART 6 — Glossary")

    print("  Technical terms that need a brief explanation on first use.\n")
    data["explain_terms"] = []
    terms_raw = ask_list("Term | explanation (pipe-separated, one per line, e.g. 'FTC | Foreign Tax Credit'):")
    for line in terms_raw:
        if "|" in line:
            parts = [p.strip() for p in line.split("|", 1)]
            data["explain_terms"].append({"term": parts[0], "explanation": parts[1]})

    print()
    data["avoid_terms"] = []
    avoid_raw = ask_list("Terms to avoid | use instead (pipe-separated, e.g. 'utilize | use'):")
    for line in avoid_raw:
        if "|" in line:
            parts = [p.strip() for p in line.split("|", 1)]
            data["avoid_terms"].append({"avoid": parts[0], "use_instead": parts[1]})

    header("PART 7 — CTA")

    data["consultation_cta"] = ask(
        "Main consultation CTA text (the sentence readers click or act on):",
        default="Book a call — we'll tell you exactly where you stand in the first 30 minutes."
    )

    header("PART 8 — Asana (optional)")

    if confirm("Do you have an Asana project URL for this client?"):
        data["asana_url"] = ask("Asana project URL:")
        data["asana_id"] = ask("Asana project ID (if known):")
    else:
        data["asana_url"] = ""
        data["asana_id"] = ""

    data["notes"] = ask("Any other notes about this client? (Enter to skip):")

    return data


def build_qa_text(data: dict) -> str:
    """Format Q&A answers into a readable block for Claude prompts."""
    segments_text = ""
    for seg in data.get("audience_segments", []):
        segments_text += f"""
Segment: {seg['name']}
- Who they are: {seg['who']}
- Their situation: {seg['situation']}
- Their anxiety: {seg['anxiety']}
- What a successful article does: {seg['success']}
"""

    return f"""
Client name: {data['name']}
Website: {data['website']}
Industry: {data['industry']}
Primary market: {data['primary_market']}

Brand voice style: {data.get('voice_style', '')}
What reader should feel: {data.get('reader_feeling', '')}
Phrases that sound like them: {', '.join(data.get('voice_phrases', []))}
Things they never do: {'; '.join(data.get('voice_never', []))}
What makes them different: {data.get('differentiator', '')}
Jargon policy: {data.get('jargon_policy', '')}
Additional voice notes: {data.get('extra_voice_notes', '')}

Audience segments:
{segments_text}

Content goals:
{data.get('content_goals', '')}
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Onboard a new client for the SEO Content System")
    parser.add_argument("--client", default=None, help="Client slug (e.g. monx)")
    args = parser.parse_args()

    content_base_env = os.environ.get("CONTENT_BASE", "").strip()
    if not content_base_env:
        print("ERROR: CONTENT_BASE is not set. Add it to .env or export it before running.")
        sys.exit(1)

    content_base = Path(content_base_env)

    print()
    print("  ┌─────────────────────────────────────────────────┐")
    print("  │  SEO Content System — Client Onboarding         │")
    print("  └─────────────────────────────────────────────────┘")

    client_slug = args.client
    if not client_slug:
        client_slug = ask("Client slug (lowercase, hyphenated, e.g. monx):")
    client_slug = re.sub(r'[^a-z0-9]+', '-', client_slug.lower().strip()).strip('-')

    client_dir = content_base / client_slug
    if client_dir.exists():
        print(f"\n  WARNING: {client_dir} already exists.")
        if not confirm("Continue and overwrite existing files?"):
            print("  Cancelled.")
            sys.exit(0)

    # Run the Q&A
    data = run_qa(client_slug)
    data["client_name"] = data["name"]

    # Build folder structure
    header("Building folder structure")
    brand_dir   = client_dir / "brand"
    content_dir = client_dir / "content"
    brand_dir.mkdir(parents=True, exist_ok=True)
    content_dir.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ {client_dir}")
    print(f"  ✓ {brand_dir}")
    print(f"  ✓ {content_dir}")

    # Write structured files
    write_profile(client_dir, data)
    print(f"  ✓ profile.md")

    write_competitors(brand_dir, data)
    print(f"  ✓ brand/competitors.md")

    write_glossary(brand_dir, data)
    print(f"  ✓ brand/glossary.md")

    write_cta_library(brand_dir, data)
    print(f"  ✓ brand/cta-library.md")

    write_content_index(content_dir)
    print(f"  ✓ content/_index.md")

    # Copy de-ai-guidelines from repo (universal)
    de_ai_src = BRAND_TMPL / "de-ai-guidelines.md"
    if de_ai_src.exists():
        shutil.copy2(de_ai_src, brand_dir / "de-ai-guidelines.md")
        print(f"  ✓ brand/de-ai-guidelines.md (copied from repo)")
    else:
        print(f"  ✗ de-ai-guidelines.md not found in repo brand/ — copy manually")

    # Claude-generated files
    header("Generating brand voice files with Claude")
    qa_text = build_qa_text(data)
    generate_claude_files(brand_dir, qa_text, data["name"])

    # Done
    print()
    print("  ┌─────────────────────────────────────────────────┐")
    print(f"  │  {data['name']} onboarded successfully{'':>21}│")
    print("  └─────────────────────────────────────────────────┘")
    print()
    print(f"  Client folder : {client_dir}")
    print(f"  Brand folder  : {brand_dir}")
    print()
    print("  Next steps:")
    print(f"    1. Review brand/brand-voice-card.md — edit anything Claude got wrong")
    print(f"    2. Review brand/audience-profiles.md — fill any gaps")
    print(f"    3. Run your first article:")
    print(f"       python3 run_workflow.py --client {client_slug} --article \"your keyword\" --step all")
    print()


if __name__ == "__main__":
    main()
