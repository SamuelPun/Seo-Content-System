"""Claude Code integration for onboarding — generates brand voice and audience files."""

from __future__ import annotations

import subprocess
from datetime import date
from pathlib import Path

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
    month_year = date.today().strftime("%B %Y")

    print("  → Generating brand-voice-card.md with Claude...")
    bv_content = call_claude(BRAND_VOICE_PROMPT.format(
        client_name=client_name,
        month_year=month_year,
        qa_text=qa_text,
    ))
    if bv_content:
        (brand_dir / "brand-voice-card.md").write_text(bv_content + "\n", encoding="utf-8")
        print("  ✓ brand-voice-card.md written")
    else:
        print("  ✗ Claude failed — writing placeholder brand-voice-card.md")
        (brand_dir / "brand-voice-card.md").write_text(
            f"# {client_name} — Voice Reference Card\n\n"
            "*Generated from onboarding Q&A — Claude was not available. Fill in manually.*\n\n"
            "## Core character\n\n## Voice patterns\n\n## Never do this\n\n## Vocabulary\n\n## The one thing\n",
            encoding="utf-8",
        )

    print("  → Generating audience-profiles.md with Claude...")
    ap_content = call_claude(AUDIENCE_PROMPT.format(client_name=client_name, qa_text=qa_text))
    if ap_content:
        (brand_dir / "audience-profiles.md").write_text(ap_content + "\n", encoding="utf-8")
        print("  ✓ audience-profiles.md written")
    else:
        print("  ✗ Claude failed — writing placeholder audience-profiles.md")
        (brand_dir / "audience-profiles.md").write_text(
            f"# Audience Profiles — {client_name}\n\n*Fill in manually.*\n\n"
            "## Profile 1 — [Name]\n\n**Who they are:**\n\n**Their situation right now:**\n\n"
            "**What they know already:**\n\n**What they are confused or anxious about:**\n\n"
            "**What a successful article does for them:**\n",
            encoding="utf-8",
        )
