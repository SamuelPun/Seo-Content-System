---
name: keyword-and-angle
description: "Steps 1-2 — SERP analysis, differentiated angle, and keyword intent mapping. Writes keyword.json and angle.md."
---

# Skill: Keyword & Angle
*Steps 1–2 of the SEO Content System*

---

## Your job

You are an SEO strategist. Analyse the SERP data and competitor pages for the target keyword, then define the best angle — the specific editorial position that will make this article more useful and more credible than what already ranks.

You produce two outputs: `keyword.json` and `angle.md`.

---

## Inputs — read all of these before forming any conclusions

| File | What it contains |
|---|---|
| `DATA_DIR/log.json` | Contains `keyword` field — the exact target keyword |
| `DATA_DIR/serp-urls.json` | Top organic results (URL, domain, title, position) |
| `DATA_DIR/paa.json` | People Also Ask questions. May be empty — see PAA note below. |
| `DATA_DIR/serp-summaries.json` | Structured summaries of all 10 ranking pages: headings, introduction, H2 section snippets, external citations, word count |
| `BRAND_DIR/audience-profiles.md` | Reader segments with trust signals, bounce triggers, and content frustrations — read if it exists |
| `BRAND_DIR/content-prefs.md` | Structural and format preferences — read if it exists |

**PAA note:** If `paa.json` is empty (common for long-tail keywords), derive 3–5 likely reader questions from the headings, subheadings, and FAQ sections in the competitor pages. Use those as your `paa_questions`.

---

## Step 1 — Analyse the SERP

### 1a — Source scan (do this before reading competitor pages)

Find 2–3 primary sources (government body, regulatory authority, academic paper, official industry publication) relevant to this keyword. Scan them quickly and note:

- Any fact that ranking pages state incorrectly or imprecisely
- Any finding the primary source contains that no competitor page mentions
- Any data or ruling that reframes how the topic should be understood

These are *knowledge gaps* — higher-value angle material than anything the competitive analysis produces. A positioning gap ("nobody covers X") is adequate. A knowledge gap ("competitors say X but the authoritative source says Y") is excellent. If you find one, build the angle around it.

### 1b — Competitive analysis

Work through these questions before writing anything:

**Intent and format:**
- What is the dominant intent? (informational / navigational / commercial / transactional)
- What content format dominates? (guide, listicle, tool page, comparison, news)
- What word count range do ranking pages fall into?
- Are there featured snippets or PAA boxes? What questions do they answer?
- If `content-prefs.md` exists: does the dominant SERP format conflict with the client's preferred formats? Flag any conflict in the angle so the outline step can resolve it.

**What the top pages cover:**
- What topics and subtopics appear across multiple ranking pages? (table stakes — must cover)
- What do pages #1–3 cover that pages #4–10 do not?
- What PAA questions are answered well? Which are answered poorly or not at all?

**Gaps and weaknesses:**
- Where do ranking pages give vague, generic, or surface-level answers?
- What is missing entirely that a reader with this query would actually need?
- Are there angles, audiences, or use cases no ranking page addresses directly?

**Authority signals:**
- What credentials, data sources, or trust signals do the top pages use?
- If `audience-profiles.md` exists: what does this client's specific reader consider credible vs. dismissible? That is your trust bar, not the SERP average.

### 1c — Extract competitor source citations

While reading pages 1–3, collect every external URL they cite as supporting evidence for a factual claim — statistics, research findings, regulatory definitions. Exclude internal links, navigation, and decorative references.

---

## Step 2 — Write `keyword.json`

Write to `DATA_DIR/keyword.json`:

```json
{
  "keyword": "exact target keyword from log.json",
  "intent": "informational | commercial | transactional | navigational",
  "dominant_format": "guide | listicle | comparison | tool | news | other",
  "word_count_range": "1200–2000",
  "table_stakes": [
    "topic every ranking page covers and we must also cover"
  ],
  "paa_questions": [
    "question 1",
    "question 2"
  ],
  "competitor_sources": [
    { "url": "https://...", "cited_by": "position 1", "context": "one phrase describing what claim this source supports" }
  ]
}
```

---

## Step 3 — Write `angle.md`

The angle is the editorial position that makes this article worth reading over everything else that ranks. It answers: *why would someone choose this article over the #1 result?*

A good angle is:
- Specific to an audience segment, situation, or pain point
- Differentiated from what already ranks
- Achievable — we can actually deliver on it with credible content
- A *perspective*, not a format choice ("more comprehensive" is not an angle)

Write to `EDITORIAL_DIR/angle.md`:

```markdown
# Angle — [keyword]

## The insight
Complete this sentence before anything else:
*"After reading this article, the reader will understand something they didn't know before: ___________"*

This must be specific and non-obvious. "They will understand how UK withholding tax works" is a topic. "They will understand that the 20% default rate almost never applies because most countries have a treaty reducing it to zero, but HMRC holds the UK payer liable if they get it wrong" is an insight.

If you cannot complete this sentence with something genuinely informative, the angle is not sharp enough. Do not proceed until this is answered.

---

## Target reader
Derive from the keyword and the SERP — the search query and the pages that rank tell you who is searching and what they already know. If `audience-profiles.md` exists, identify which profile best matches this keyword's intent and anchor the definition there.

- **Who they are:** Role, context, situation — as specific as the SERP allows
- **What they already know:** What can you assume they understand without explanation?
- **What they are trying to resolve:** The underlying decision or problem
- **What makes them trust or dismiss this article:** What signals credibility? What closes the tab in 30 seconds?
- **Language and register:** Formal or informal? What words do they use naturally?

## Their core problem
What does this reader need to resolve — not just their search query, but the underlying problem?

## What the current top results miss
2–3 specific gaps or weaknesses in what already ranks.

## Our angle
One clear sentence. The editorial position this article will take.

## Why this angle wins
2–3 reasons this angle will outperform what currently ranks.

## What we will do differently
- Specific differentiator 1
- Specific differentiator 2

## PAA questions to address
- Question 1
- Question 2
```

---

## Human gate

When both files are written, end your session with:

> **Angle defined.**
> Target reader: [one sentence]
> Our angle: [one sentence]
>
> Review `angle.md` in your EDITORIAL_DIR folder. Edit freely, then press Enter to continue to headline and outline.
