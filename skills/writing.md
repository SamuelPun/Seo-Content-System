---
name: writing
description: "Step 6 — writes the article draft from outline, angle, research, and brand voice files."
---

# Skill: Writing
*Step 6 of the SEO Content System*

---

## Anchor on the insight first

Before reading anything else, open `EDITORIAL_DIR/writer-notes.md` and write this as the first line:

```
Insight: [copy the insight sentence from angle.md exactly — the "After reading this article, the reader will understand..." sentence]
```

If `angle.md` does not have a clear insight sentence, write: `Insight: UNCLEAR — angle.md needs sharpening.` and flag it before proceeding.

Every section you write should move the reader toward understanding this insight. If a section doesn't, ask whether it belongs in the article at all.

---

## Your job

Write the full article draft in `draft.md`, following the outline and applying brand voice throughout.

The outline is your brief — not a contract. If you discover mid-draft that a section works better split into two, or that an H3 would break the flow, use your judgement and note the deviation in `writer-notes.md`. What is fixed: section order, H2 headings, PAA assignments, authority source placements. What is yours: how you open each section, how arguments develop, whether H3s help or hurt.

---

## Inputs — read all of these before writing a single word

| File | What it contains |
|---|---|
| `EDITORIAL_DIR/outline.md` | Your section-by-section brief — follow this structure |
| `EDITORIAL_DIR/angle.md` | The editorial position — every paragraph must serve this angle |
| `DATA_DIR/sources/index.json` | Research index — which sources support which sections |
| `DATA_DIR/sources/[slug].md` | Individual source files — read before writing the section that uses each one |
| `DATA_DIR/keyword.json` | Target keyword and PAA questions |
| `BRAND_DIR/brand-voice-card.md` | Brand voice — tone, vocabulary, sentence patterns |
| `BRAND_DIR/voice-dna.md` | Observed patterns from real posts: openings, rhythm, teaching moves (read if it exists) |
| `BRAND_DIR/de-ai-rules-card.md` | De-AI rules — banned vocab, structural anti-patterns, em dash rewriting |
| `BRAND_DIR/audience-profiles.md` | Reader segments — calibrate tone and assumed knowledge (read if it exists) |
| `skills/content-standards.md` | Structural standards — word count, sentence length, paragraph length, headings, links, CTA |

Do not begin writing until you have read all of the above.

---

## The advisor frame

Write as a knowledgeable advisor giving a client the briefing they need — not a document writer covering a topic for completeness.

- **Advisor:** "Here's the thing most people get wrong about this — and here's what to do instead."
- **Document:** "This article covers the rules, exemptions, and compliance requirements for X."

The opening sentence should make the reader feel they are already getting something. Use "we" when speaking as the firm. Use "you" and "your" when addressing the reader. The body informs fully and doesn't sell. The CTA at the end should feel like the reader's natural next step.

**Bad opening:** "UK withholding tax on payments to foreign companies is a complex area of tax law that affects many businesses..."
**Good opening:** "Your company is about to transfer money to a foreign parent, lender, or licensor. The question is whether to deduct UK withholding tax before the payment leaves. Get it wrong and HMRC holds the UK company liable."

---

## Writing rules

### Structural standards
Apply `skills/content-standards.md` in full. Five rules that most commonly need attention:
- Never pad to hit a word count. Never cut substance to stay under one.
- No sentence over 35 words. No paragraph over 5 sentences.
- Never open the introduction with a question or a definition.
- The angle must be visible by sentence 3 of the introduction.
- One specific CTA at the end — not vague, not generic, not repeated mid-article.

### Content devices
The outline flags certain sections with a **Content device** instruction. Before writing any such section, read the execution sketch in the outline for that device — it gives you the scenario, numbers, and key moment for this specific article. That is your brief. Execute it fully. Device sections should be the most generously paced sections in the article — give them room.

### Fixed vs flexible
**Fixed — do not deviate:**
- The sections and their order
- The H2 heading text
- Which PAA question is answered in which section
- Which authority source is used in which section

**Flexible — use your judgement:**
- How you open each section
- Whether a point becomes one paragraph or three
- Whether an H3 helps or the section flows better without it
- How you weave in sources

If a section's word count genuinely cannot be hit without padding, write it well at a shorter length and note it. A tight 180 words beats a padded 220.

**How-to articles:** When the article walks the reader through a genuine process, use numbered step headers: `## Step N. [Short active label]`. Do not use numbered steps for educational articles where sections are independent.

### Voice and tone
- Apply `brand-voice-card.md` throughout — non-negotiable
- Write for the target reader in `angle.md` — their situation, vocabulary, expertise level
- **Editorial asides at decision points:** At each key decision — a counterintuitive choice, a common mistake, a technique the reader must commit to — inject one short editorial sentence that signals you have a position. "Honestly, that's the bar." / "This is the decision most recipes skip." Rules: one per section maximum; use before or after the explanation, never in the middle of it; use "Honestly", "Frankly", "Let's be honest" — never "It's worth noting."

### De-AI
Apply `BRAND_DIR/de-ai-rules-card.md` in full. Three patterns that most commonly appear in first drafts:
- Banned vocabulary — see the full list in `de-ai-rules-card.md`
- Throat-clearing transitions ("Now that we've covered X, let's look at Y")
- Uniform sentence rhythm — mix short punchy sentences with longer ones; burstiness above 1.2
- **Zero em dashes.** Every em dash is a HIGH audit flag. Write around them from the start.

After a dense explanatory paragraph, consider a short connector sentence that re-anchors the reader before the next point. Use sparingly: one per section at most.

### Authority
- Use sources from `sources/` — cite naturally in prose, not as footnotes
- Use exact figures from source files — do not round or paraphrase statistics
- Do not invent data. If you cannot support a claim with a source, write around it or flag it with `[SOURCE NEEDED]`

**Moving from source extract to natural prose — three approaches:**
1. **Claim first, figure second:** State the point in your own words, then ground it with the specific number. *"Most expats underestimate their filing obligations. According to HMRC, X% of..."*
2. **Attribution as opener:** Lead the sentence with the source, then deliver the finding. *"The IRS reported that... which means in practice..."*
3. **Short direct quote:** When the exact wording matters (a legal definition, a policy statement), quote the key phrase briefly — under 10 words — and move on.

Never paraphrase in a way that shifts the meaning. If the source says "up to 30%" do not write "nearly a third."

### SEO mechanics
- Use the target keyword in the first 100 words, naturally
- Use the keyword or close variants in at least 2–3 H2 headings
- Do not keyword-stuff — if it reads awkwardly, rephrase
- Answer PAA questions with a direct sentence followed by elaboration

---

## Live capture during writing

**work-log.md** — write one entry when the draft is complete:

```
---
step: writing | [timestamp] | status: [complete | partial | error]
---
[Word count. Any sections that deviated from outline.md and why. Any data gaps that affected the writing.]
```

**writer-notes.md** — write only when a genuine instinct fires. Ask before each potential entry: "Would a thoughtful editor want to know this before the final pass?" Write a note when:
- A section feels thin despite being structurally sound
- The intro is doing something against the SERP grain — and it is working
- A device landed well or failed
- A structural decision went against the outline
- A claim feels overstated relative to the source it rests on

Do not write a note to confirm the draft is done or to summarise what was written.

---

## Draft format

Write `draft.md` to EDITORIAL_DIR:

```markdown
---
title: [chosen headline from headline.md]
keyword: [target keyword]
date: [today's date YYYY-MM-DD]
status: draft
---

# [Chosen headline]

[Introduction]

## [H2 Section heading]

[Section content]

[Continue for all sections in outline]

---

*Sources used:*
- [Source title]: [URL]
```

---

## Quality check before finishing

Before writing the final line, re-read the full draft and verify:

- [ ] Every section from the outline is present
- [ ] Every PAA question is answered
- [ ] The angle from `angle.md` is visible throughout — not just in the intro
- [ ] No banned vocabulary (see `de-ai-rules-card.md`)
- [ ] No AI structural patterns (throat-clearing, parallel list overuse, restated questions)
- [ ] No em dashes
- [ ] Brand voice consistent with `brand-voice-card.md`
- [ ] All sources cited are from `DATA_DIR/sources/` — no invented data
- [ ] Word count within 10% of target

---

## End of session

When `draft.md` is written and the quality check is complete, end with:

> **Draft complete.**
> Word count: [N words]
> Sections: [N]
> Sources cited: [N]
>
> No human gate — workflow continues automatically to audit.
