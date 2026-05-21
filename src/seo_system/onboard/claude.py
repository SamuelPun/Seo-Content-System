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

## Opening pattern
[1-2 sentences describing how pieces typically open. Not a principle — a pattern. E.g. "Opens by placing the reader in their specific situation before naming the topic."]

---

## Teaching style
[1-2 sentences. How does this brand explain complex things — direct assertion, worked examples, analogies, comparisons? What's the default move?]

---

## Opinion handling
[1-2 sentences. Does this brand commit to positions or hedge? How opinionated is it, and how does that show up in the writing?]

---

## Editorial asides
[Does this brand inject short informal opinion sentences at decision points — "honestly", "frankly", "let's be honest"? Describe when these appear (at a key decision, a surprising fact, a moment of validation) and what form they take. If this brand doesn't use editorial asides, say so explicitly.]

---

## How-to content format
[For step-by-step content, does this brand use numbered steps with short active headers, or flowing prose with descriptive section headers? Which register is more natural to their voice?]

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

**What makes them trust a source:**
[1-2 sentences — what signals credibility to this reader; what makes them dismiss content as generic or AI-generated]

**What makes them bounce:**
[1-2 sentences — what would make them close the tab in the first 30 seconds]

**What frustrates them about other content on this topic:**
[1-2 sentences — what existing content gets wrong; the gap this brand can fill]

---

Start the file with:
# Audience Profiles — {client_name}

*Each profile describes a specific reader segment. Skills read this to calibrate tone, assumed knowledge, and what the reader actually needs resolved.*

---

CLIENT Q&A
==========
{qa_text}
"""


CONTENT_PREFS_PROMPT = """\
You are a content strategist. Based on the client Q&A below, write a content preferences \
reference file for a content team. This file is read by skills before generating headlines, \
outlines, and keyword strategies — it records structural and format preferences so every \
article feels consistent with this brand's publishing approach.

Output ONLY the content-prefs.md file content. No preamble, no explanation outside the file.

Structure the file exactly as follows:

# Content Preferences — {client_name}
*Generated from onboarding data. Edit if anything is wrong.*

---

## Preferred content formats
[Which formats suit this brand and audience — guides, comparisons, listicles, news-style, \
tool/calculator pages? For each format mentioned, note when to use it and when to avoid it.]

---

## Article depth and length
[Short and targeted (1000–1500 words) / Standard (1500–2500) / In-depth (2500+)? \
Is there a strong preference or does it depend on topic complexity?]

---

## Structural defaults
- **How-to content:** [numbered steps with short labels / flowing prose with descriptive headers]
- **Lists and tables:** [use freely / restrict to data-heavy sections / avoid]
- **Comparison sections:** [include by default / include when competitors differ / avoid]
- **Reader pathways:** [single reader per article / structure by reader type when segments diverge]

---

## Headline preferences
- **Preferred types:** [e.g. problem-first, outcome-first, specificity hook — list in priority order]
- **Tone:** [direct and informational / curious / authoritative / conversational]
- **Length:** [under 55 characters / under 65 characters]

---

## What this client never publishes
[Format or structural patterns this brand avoids — e.g. no pure listicles, no click-bait \
headlines, no "10 things" framing.]

---

CLIENT Q&A
==========
{qa_text}
"""

VOICE_DNA_PROMPT = """\
You are a voice and style analyst. Read the article excerpts below and extract the writing DNA \
of this brand.

Your job is to observe patterns — not to describe what the brand claims to be, but what the \
writing actually does. Base every observation on evidence from the articles. If you cannot find \
clear evidence for something, say so rather than inventing a pattern.

Output ONLY the voice-dna.md file content. No preamble, no explanation outside the file.

Structure the file exactly as follows:

# Voice DNA — {client_name}
*Derived from analysis of {post_count} published articles. Observed patterns, not stated \
principles — edit if anything is wrong.*

---

## Opening patterns
[How do articles typically open? Describe the move — e.g. "Places the reader in their specific \
situation before naming the topic." Include 1-2 short direct examples quoted from the articles.]

---

## Sentence rhythm
[What is the sentence length pattern? Short bursts, long explanatory sentences, or mixed? \
What is the dominant register? Cite a short passage as evidence.]

---

## Editorial asides
[Do short informal opinion injections appear — "Honestly", "Frankly", "Let's be honest"? If so, \
quote an example. Note what triggers them — a key decision point, a surprising fact, a validation \
moment. If none appear in the articles, state that explicitly.]

---

## Teaching moves
[When this brand explains something complex, what do they do — direct assertion, worked example, \
analogy, comparison? Include a short quoted example of each pattern you observe.]

---

## Opinion and position
[Does this brand commit to positions or hedge? When they have a take, how is it signalled? \
Quote a short example of a strong position if you find one.]

---

## Signature vocabulary
[Words, phrases, or constructions that recur or feel distinctly theirs — not industry jargon, \
but the choices that reveal personality. List with brief notes on how each is used.]

---

## What this writing never does
[Observed absences — things you would expect to see in generic content on these topics that this \
brand consistently avoids. Be specific: "never opens with a rhetorical question", not "avoids clichés".]

---

ARTICLES
========
{articles_text}
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


def generate_voice_dna(brand_dir: Path, posts: list[dict], client_name: str):
    articles_text = "\n\n---\n\n".join(
        f"URL: {p['url']}\n\n{p['text']}" for p in posts
    )
    prompt = VOICE_DNA_PROMPT.format(
        client_name=client_name,
        post_count=len(posts),
        articles_text=articles_text,
    )
    print(f"  → Analysing {len(posts)} posts with Claude to extract Voice DNA...")
    content = call_claude(prompt)
    if content:
        (brand_dir / "voice-dna.md").write_text(content + "\n", encoding="utf-8")
        print("  ✓ voice-dna.md written")
    else:
        print("  ✗ Claude failed — voice-dna.md not generated")


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


def generate_content_prefs(brand_dir: Path, qa_text: str, client_name: str):
    print("  → Generating content-prefs.md with Claude...")
    content = call_claude(CONTENT_PREFS_PROMPT.format(
        client_name=client_name,
        qa_text=qa_text,
    ))
    if content:
        (brand_dir / "content-prefs.md").write_text(content + "\n", encoding="utf-8")
        print("  ✓ content-prefs.md written")
    else:
        print("  ✗ Claude failed — writing placeholder content-prefs.md")
        (brand_dir / "content-prefs.md").write_text(
            f"# Content Preferences — {client_name}\n\n"
            "*Generated from onboarding Q&A — Claude was not available. Fill in manually.*\n\n"
            "## Preferred content formats\n\n"
            "## Article depth and length\n\n"
            "## Structural defaults\n\n"
            "## Headline preferences\n\n"
            "## What this client never publishes\n",
            encoding="utf-8",
        )
