"""Guided Q&A flow — collects client data for onboarding."""

from __future__ import annotations

from seo_system.onboard.prompts import ask, ask_list, confirm, header


def run_qa(client_slug: str) -> dict:
    data = {"slug": client_slug}

    header("PART 1 — Basic information")
    data["name"] = ask("Client name (e.g. Monx):")
    data["website"] = ask("Website URL (e.g. https://monx.team):")
    data["industry"] = ask("Industry / niche (e.g. US/UK tax advisory):")
    data["primary_market"] = ask("Primary market — who reads their content?")
    data["sitemap_url"] = ask(
        "Sitemap index URL (e.g. https://example.com/sitemap_index.xml):",
        default=f"{data['website'].rstrip('/')}/sitemap_index.xml",
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
        default="Explain on first use",
    )
    data["extra_voice_notes"] = ask("Anything else about their voice or writing style? (Enter to skip):")
    data["opening_pattern"] = ask(
        "How do they typically open a piece? Describe the pattern or give an example first sentence:"
    )
    data["opinion_style"] = ask(
        "Do they take strong positions or hedge? How opinionated are they?"
    )
    data["teaching_style"] = ask(
        "How do they explain complex things — analogies, worked examples, direct assertion, comparisons?"
    )
    data["editorial_asides"] = ask(
        "Does this brand inject brief informal opinion phrases mid-article — 'honestly', 'frankly', "
        "'let's be honest'? If yes, give 1-2 examples of how they'd sound in a sentence "
        "(Enter to skip):"
    )
    data["howto_format"] = ask(
        "For step-by-step content (how-to guides, planning pieces), does the brand prefer numbered "
        "steps or flowing prose?",
        default="Numbered steps with short active labels",
    )
    data["preferred_formats"] = ask(
        "What content formats work best for their audience? (e.g. guides, listicles, comparisons, "
        "news-style) — list them:",
        default="Guides",
    )
    data["article_depth"] = ask(
        "Preferred article depth? (e.g. concise 1000-1500 words / standard 1500-2500 / "
        "in-depth 2500+):",
        default="Standard (1500-2500 words)",
    )
    data["structural_defaults"] = ask(
        "Any structural rules — e.g. 'no listicles', 'tables for data only', 'always use "
        "comparison sections'? (Enter to skip):"
    )

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
        segment["trust_signals"] = ask(
            f"  [{segment_name}] What makes them trust a source vs. dismiss it as AI slop?"
        )
        segment["bounce_triggers"] = ask(
            f"  [{segment_name}] What would make them close the tab in the first 30 seconds?"
        )
        segment["content_frustrations"] = ask(
            f"  [{segment_name}] What frustrates them about other content on this topic?"
        )
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
    extra_trusted = ask_list("Additional trusted domains to add (one per line) — Enter to skip:")
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
        default="Book a call — we'll tell you exactly where you stand in the first 30 minutes.",
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
- What makes them trust a source: {seg.get('trust_signals', '')}
- What makes them bounce: {seg.get('bounce_triggers', '')}
- What frustrates them about existing content: {seg.get('content_frustrations', '')}
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
Opening pattern: {data.get('opening_pattern', '')}
Opinion style: {data.get('opinion_style', '')}
Teaching style: {data.get('teaching_style', '')}
Editorial asides: {data.get('editorial_asides', '')}
How-to content format: {data.get('howto_format', '')}
Preferred content formats: {data.get('preferred_formats', '')}
Article depth: {data.get('article_depth', '')}
Structural defaults: {data.get('structural_defaults', '')}

Audience segments:
{segments_text}

Content goals:
{data.get('content_goals', '')}
"""
