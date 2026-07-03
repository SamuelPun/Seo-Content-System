# Content Standards
*Universal structural and technical standards — applies to every article regardless of topic, client, or angle*

These are not style guidelines (see `brand-voice-card.md`) and not de-AI rules (see `de-ai-guidelines.md`). These are structural guardrails. They apply to every article, every time, without exception unless explicitly overridden in the outline.

---

## Word Count

**Floor:** 1,200 words. Below this, the article is unlikely to cover an informational topic with enough depth to compete.

**Target:** Match the word count range in `keyword.json` — this is derived from actual ranking pages for this keyword. Stay within ±15% of that range.

**Ceiling:** 3,500 words. Going above this requires a specific reason noted in the outline — either the SERP demands it or a content device genuinely requires the space.

**The override rule — applies in both directions:**
- Never pad to hit a number. Repetition, over-explanation, and summary-before-conclusion all signal padding. If a section is complete at 160 words and the outline says 200, write 160.
- Never cut substance to stay under a number. If a content device or a complex topic needs more space than the outline allocated, take it and note the overage at the end of the draft.

A tight 1,400 words beats a padded 1,800 every time.

---

## Sentence Length

**Soft target:** Average sentence length of 16–20 words across the article.

**Hard cap:** No sentence should exceed 35 words. A sentence over 35 words almost always contains two ideas that should be separated.

**Minimum variation required:** No run of more than 3 consecutive sentences of similar length in the same paragraph. This is enforced at audit by `rhythm-analysis.json`.

**Short sentence rule:** At least 15% of sentences should be under 10 words. These carry emphasis and break up density. They are not optional decoration.

---

## Paragraph Length

**Standard paragraphs:** 2–4 sentences. 5 sentences is the absolute maximum before a paragraph becomes a wall of text on mobile.

**One-sentence paragraphs:** Allowed and encouraged — but only when the sentence genuinely deserves emphasis. No more than 2 per article section. Overuse kills the effect.

**Opening paragraph of any section:** Never longer than 3 sentences. The reader should be inside the section's argument within 40 words.

---

## Introduction

The introduction is the highest-value real estate in the article. It must earn the reader's attention in the first sentence and hold it for 120–180 words before the first H2.

**Hard rules:**
- **Never open with a question.** It is the most recognisable AI writing pattern and the weakest possible hook. Start with a statement, a fact, a scenario, or a direct address to the reader's situation.
- **Never open with a definition.** "X is a process by which..." signals a generic article immediately.
- **Target keyword in the first 100 words** — naturally, not forced.
- **The angle must be visible by sentence 3.** The reader should know within 3 sentences why this article is different from every other result they could have clicked.
- **No preamble.** Do not tell the reader what the article will cover. Cover it.
- **Maximum length:** 200 words. If the introduction exceeds 200 words, it is doing the wrong job — it is summarising instead of hooking.

---

## Headings

**H1:** One per article. Matches the chosen headline exactly.

**H2s:** Minimum 3, maximum 8 per article. Fewer than 3 means the article has no real structure. More than 8 means the topic is either too broad or the sections are too thin.

**H3s:** Always nest under an H2. Never use an H3 as a standalone section break. Only use an H3 when the content genuinely shifts to a sub-topic — not to break up a long section for visual relief.

**The heading test:** Every heading should tell the reader what they will learn or be able to do after reading that section. If a heading only names a topic ("Tax Obligations") it is weaker than one that signals value ("What You Are Actually Required to File"). Prefer value-signalling headings.

**Never use a heading tag for non-heading content** — pull quotes, callout boxes, emphasis. Use bold or formatting instead.

---

## Links

**Internal links:**
- 3–5 per article — enough to support site structure, not so many it looks manipulative
- Anchor text must be descriptive and natural — never "click here" or "read more"
- Only link to pages that are genuinely relevant to the surrounding sentence — do not force links

**External links:**
- Link to primary sources cited in the article — government sites, official bodies, academic papers
- Do not link to competitors or other SEO blogs
- Do not link to sources that require a login or paywall to access
- Maximum 5 external links per article
- All external links open in a new tab (handled in `build_output.py`)

---

## CTAs

Every article must end with one clear, specific CTA. Vague CTAs are not acceptable.

**Not acceptable:**
- "Contact us to learn more"
- "Get in touch today"
- "Find out how we can help"

**Acceptable:**
- "Download our [specific resource] to [specific outcome]"
- "Book a [specific type] consultation — we'll [specific thing] in the first call"
- "Use our [specific tool] to calculate your [specific result] in under 5 minutes"

The CTA must connect directly to the article's angle and the reader's core problem as defined in `angle.md`. It should feel like the logical next step for someone who just read the article — not a generic prompt bolted on at the end.

One CTA per article. Do not add secondary CTAs mid-article unless the outline explicitly specifies one.

---

## Reading Level

Reading level is determined per article based on the target reader defined in `angle.md` and the keyword context in `keyword.json`.

**As a general guide:**
- General consumer audience (personal finance, lifestyle, health): aim for plain language — short words, active voice, no jargon without explanation
- Professional or B2B audience (legal, accounting, technical): industry terms are acceptable but should still be explained on first use
- Expert audience: write peer-to-peer — no hand-holding, assume background knowledge

**Active voice rule:** Default to active voice. Passive voice is acceptable when the actor is unknown or irrelevant. If more than 1 in 5 sentences is passive, rewrite.

**Jargon rule:** Any term that would confuse a smart non-specialist must be explained on first use — in the same sentence if possible, not in a separate definition paragraph.

---

## What These Standards Do Not Cover

- Tone, personality, vocabulary preferences → `{BRAND_DIR}/brand-voice-card.md`
- Banned AI phrases and patterns → `{BRAND_DIR}/de-ai-guidelines.md`
- SEO keyword placement and PAA coverage → `writing.md` writing rules
- Content device execution → `skills/content-devices.md`
- Schema, meta, and HTML output → `skills/output.md`
