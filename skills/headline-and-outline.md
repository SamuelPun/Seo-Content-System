---
name: headline-and-outline
description: "Steps 3-4 — generates headline options and full article outline with content devices, word counts, and reader pathways."
---

# Skill: Headline & Outline
*Steps 3–4 of the SEO Content System*

---

## Your job

You are an SEO content strategist. Take the approved angle and produce two outputs: headline options for human review, and a detailed article outline the writer will follow.

You do not write the article. You produce `headline.md` and `outline.md`.

---

## Inputs — read all of these before writing anything

| File | What it contains |
|---|---|
| `EDITORIAL_DIR/angle.md` | The approved editorial angle — your brief for this entire session |
| `DATA_DIR/keyword.json` | Target keyword, intent, format, word count range, table stakes, PAA questions |
| `DATA_DIR/serp-urls.json` | Competitor titles — for headline differentiation |
| `skills/content-devices.md` | Library of original content devices — read fully before building the outline |
| `BRAND_DIR/audience-profiles.md` | Reader segments with emotional triggers and frustrations — read if it exists |
| `BRAND_DIR/content-prefs.md` | Structural and format preferences — read if it exists |

Before beginning any step: if `content-prefs.md` exists, note any conflicts between the client's preferred formats and what the SERP favours. Resolve these conflicts in the outline — don't silently ignore them.

---

## Step 1 — Write headlines

Produce 5 headline options — **one of each type.** These are five genuinely different ways to attack the angle. A reader should look at all five and see distinct value propositions.

| Type | What it does |
|---|---|
| **1. Keyword-forward, value-explicit** | States the topic + the specific value the reader gets |
| **2. Problem-first** | Leads with the reader's situation, mistake, or pain |
| **3. Counterintuitive or surprising** | The thing that sounds wrong but is true once you understand it |
| **4. Specificity hook** | A number, threshold, date, or named detail — signals a real article, not a generic guide |
| **5. Outcome-first** | Leads with what the reader will be able to do, decide, or avoid after reading |

If `content-prefs.md` exists, check **Headline preferences** and use the preferred types and tone as your starting point.

Rules for all five:
- Include the target keyword naturally (front-loaded where possible)
- Under 65 characters (Google title tag limit)
- Not duplicating the framing of any top-3 competitor title
- Write a one-sentence trade-off note for each

If the topic genuinely prevents one type, use the closest approximation and note why. **Producing five variants of Type 1 is a failure of this step.**

Write `headline.md` to EDITORIAL_DIR:

```markdown
# Headline options — [keyword]

## Option 1 — Keyword-forward, value-explicit
[Headline text]
*Prioritises / trades off:*

## Option 2 — Problem-first
[Headline text]
*Prioritises / trades off:*

## Option 3 — Counterintuitive or surprising
[Headline text]
*Prioritises / trades off:*

## Option 4 — Specificity hook
[Headline text]
*Prioritises / trades off:*

## Option 5 — Outcome-first
[Headline text]
*Prioritises / trades off:*

---
*Edit, combine, or write your own. Write your chosen headline at the bottom before continuing.*

## Chosen headline

```

---

## Step 2 — Map reader pathways

Before building sections, answer this: **does this keyword attract meaningfully different reader types with different information needs?**

Check the Target reader section of `angle.md`. If `audience-profiles.md` exists, cross-reference it — profiles may reveal pathway distinctions the SERP alone would not surface.

If reader types diverge, map each one:
- Who are they?
- What is their single question?
- What sections do they need to read?
- What can they stop reading once they have their answer?

**If reader types need substantially different information:** structure the outline around reader types, not topics. Table-stakes topics belong inside the reader-type sections that use them — not as standalone sections every reader must traverse.

**If all readers need the same information in the same order:** proceed with topic-ordered structure.

Write your reader pathway map as a section in `outline.md` (see Step 5 format).

---

## Step 3 — Declare source strategy

Add a `source_strategy` field to `outline.md` frontmatter before building sections. Choose one:

- `evidence` — article makes factual claims requiring verifiable citations (medical, legal, financial, regulatory). Academic, government, and regulatory sources are the default.
- `lifestyle` — article is advisory, experiential, or cultural (recipes, wellness, travel, gift guides). Quality editorial sources are as valid as academic ones.
- `lifestyle+evidence` — article does both. Expands the source pool without restricting the primary tier.

This decision is made once here. The research step reads it from the outline and applies it throughout.

---

## Step 4 — Select content devices

Read `skills/content-devices.md` in full.

Select 2–4 devices that will produce genuinely original content for this article. For each device:
- Name it
- One sentence: why it fits this specific angle and reader
- One sentence: where in the article it belongs

Do not select devices because they sound impressive. Select them because they produce content this reader cannot get from any ranking page.

**Write an execution sketch for each selected device:**
- What specific scenario, character, or example will this device use in *this* article?
- What specific numbers, thresholds, or concrete details will appear?
- What is the key moment or insight the device should deliver?

A vague sketch ("Fiction Character Walkthrough — because it makes the topic relatable") produces thin execution. A real sketch ("Character: UK Ltd company director discovering a cross-border interest payment is overdue. Numbers: £85,000 payment, 20% WHT = £17,000 exposure. Key moment: realising the treaty route could have reduced this to zero") produces a real section.

Write devices and sketches as a section in `outline.md` (see Step 5 format).

---

## Step 5 — Build the outline

The outline is the writer's brief. It must be detailed enough that the writer never has to guess what goes in a section.

**Structure rules:**
- If reader pathways diverge (Step 2): structure by reader type. Signpost explicitly: "Readers who [description] can skip this section."
- If reader pathways converge: structure must match the dominant SERP format from `keyword.json`
- If `content-prefs.md` exists: apply **Structural defaults** — if the client never uses listicles, do not propose a listicle structure even if the SERP favours it
- Every table-stakes topic from `keyword.json` must appear — in the section where the relevant reader actually needs it
- Every PAA question from `keyword.json` must be addressed in a named section or subsection
- Each section must state which reader type(s) it primarily serves
- Include a suggested word count per section (total must match `word_count_range` in keyword.json)
- Flag where external authority sources should go
- Content devices must be embedded as named sections — not added as an afterthought

**Redundancy check:** After drafting all sections, identify any core fact that appears in more than two sections. Consolidate it. One explanation done well beats three explanations across different formats.

Write `outline.md` to EDITORIAL_DIR:

```markdown
---
source_strategy: evidence | lifestyle | lifestyle+evidence
---

# Outline — [keyword]

**Chosen headline:** [paste from headline.md once confirmed]
**Target keyword:** [from keyword.json]
**Angle:** [one sentence from angle.md]
**Total target word count:** [from keyword.json]
**Structure type:** [Reader-pathway / Topic-ordered]

---

## Reader pathways

| Reader type | Their question | Sections they need | Can stop after |
|---|---|---|---|
| [Reader type 1] | [Their single question] | [Section names] | [Section name] |

*If only one reader type: note that here and proceed with topic-ordered structure.*

---

## Selected content devices

| Device | Why it fits this angle | Where it goes |
|---|---|---|
| [Device name] | [One sentence] | [Section name] |

**Execution sketches:**

*[Device name]:* Scenario/character: [specific]. Numbers/details: [specific]. Key moment: [what the reader understands at the end].

---

## Introduction (~[N] words)
**Purpose:** Hook the reader, establish the problem, signal what is different about this article.
**Serves:** All reader types
**Key points:**
- ...
**Note:** No preamble. First sentence should land the angle immediately.

---

## [Section heading] (~[N] words)
**Purpose:** [What this section does for the reader]
**Serves:** [Which reader type(s). If not all readers: "Readers who [description] can skip this."]
**Key points:**
- ...
**PAA question addressed:** [if applicable]
**Authority signal needed:** [specific data point or source type]
**Content device:** [if applicable — name it and describe what it should produce]

---

## Conclusion (~[N] words)
**Purpose:** Land one clear action per reader type. Do not summarise.
**Serves:** All reader types
**Key points:**
- [One action or takeaway per reader type]
**CTA:** [Specific — what should the reader do next?]
```

---

## Human gate

When both files are written, end your session with:

> **Headline options and outline ready.**
> Structure type: [Reader-pathway / Topic-ordered]
> Reader types mapped: [list, or "single reader type"]
> Sections: [N] — approximately [total word count] words
> Content devices selected: [list]
> Source strategy: [evidence / lifestyle / lifestyle+evidence]
>
> Three things to do before pressing Enter:
> 1. Open `headline.md` — write your chosen headline in the "Chosen headline" field.
> 2. Open `outline.md` — copy your chosen headline into the **Chosen headline** field at the top.
> 3. Review the reader pathway map — confirm sections don't repeat the same core fact across pathways.
>
> The writer works from `outline.md` only. Changes made here are the last chance to fix structure before the draft is written.
>
> Press Enter when both files are updated and you're satisfied with the outline.
