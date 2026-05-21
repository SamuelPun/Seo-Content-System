---
name: headline-and-outline
description: "Steps 3-4 — generates headline options and full article outline with content devices, word counts, and reader pathways."
---

# Skill: Headline & Outline
*Steps 3–4 of the SEO Content System*

---

## Your job

You are an SEO content strategist. Your job is to take the approved angle and produce two things: a set of headline options for human review, and a detailed article outline that the writer will follow exactly.

You do not write the article. You produce `headline.md` and `outline.md`.

---

## Inputs — read all of these before writing anything

Editorial files are in EDITORIAL_DIR. Data files are in DATA_DIR. `skills/` files are at the project root.

| File | What it contains |
|---|---|
| `EDITORIAL_DIR/angle.md` | The approved editorial angle — your brief for everything in this session |
| `DATA_DIR/keyword.json` | Target keyword, intent, format, word count range, table stakes, PAA questions |
| `DATA_DIR/serp-urls.json` | Competitor titles — for headline differentiation |
| `skills/content-devices.md` | Library of original content devices — read this fully before building the outline |
| `BRAND_DIR/audience-profiles.md` | Reader segments with emotional triggers and frustrations — read if it exists; use in Step 2 |

Read `angle.md` and `content-devices.md` fully before writing anything. Every headline and every outline section must serve the angle.

---

## Step 1 — Write headlines

Produce 5 headline options — **one of each type below.** These are not five wordings of the same idea. They are five genuinely different ways to attack the angle. A reader should look at all five and see distinct value propositions.

| Type | What it does |
|---|---|
| **1. Keyword-forward, value-explicit** | States the topic + the specific value the reader gets. Best for readers searching this exact term already. |
| **2. Problem-first** | Leads with the reader's situation, mistake, or pain. The headline speaks to the reader before naming the topic. |
| **3. Counterintuitive or surprising** | The thing that sounds wrong but is true once you understand it. Generates genuine curiosity, not just clicks. |
| **4. Specificity hook** | A number, threshold, date, or named detail in the title. Signals this is a real article, not a generic guide. |
| **5. Outcome-first** | Leads with what the reader will be able to do, decide, or avoid after reading. |

Rules for all five:
- Include the target keyword naturally (front-loaded where possible)
- Under 65 characters (Yoast / Google title tag limit)
- Not duplicating the framing of any top-3 competitor title
- Write a one-sentence trade-off note for each

If the topic or angle genuinely prevents one type (e.g. no counterintuitive angle exists), use the closest approximation and note why. **Producing five variants of Type 1 is a failure of this step.**

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

Before selecting devices or building sections, answer this question from `angle.md`:

**Does this keyword attract meaningfully different reader types with different information needs?**

Check the Target reader section of `angle.md`. If `BRAND_DIR/audience-profiles.md` exists, cross-reference it — the profiles may reveal pathway distinctions (different situations, different questions, different stopping points) that the SERP alone would not surface. If the angle identifies more than one reader type, map each one:

- Who are they?
- What is their single question?
- What do they need to read to get their answer?
- What can they stop reading once they have it?

**If reader types need substantially different information** (their questions diverge, their answers diverge, or the steps they need to take differ): structure the outline around reader types, not topics. Each reader-type section should contain everything that reader needs. Table-stakes topics belong inside the reader-type sections that use them — not as standalone topical sections that every reader must traverse.

**If all readers need the same information in the same order**: proceed with a standard topic-ordered structure.

Write your reader pathway map as a section in `EDITORIAL_DIR/outline.md` (see Step 4 format below).

---

## Step 3 — Select content devices

Read `skills/content-devices.md` in full.

Based on the angle, the target reader, and the topic — select 2–4 devices that will produce genuinely original content for this article. For each device you select:

- Name it
- Write one sentence explaining why it fits this specific angle and reader
- Write one sentence on where in the article it belongs

Do not select devices because they sound impressive. Select them because they will produce content this reader cannot get from any ranking page.

**For each device you select, write an execution sketch before moving to the outline:**

- What is the specific scenario, character, or example this device will use in *this* article?
- What specific numbers, thresholds, or concrete details will appear?
- What is the key moment or insight the device should deliver to the reader?

These sketches go below the device selection table. The writer reads them before writing the device section. Vague device selection ("Fiction Character Walkthrough — because it makes the topic relatable") without a sketch produces thin execution. A sketch like "Character: UK Ltd company director discovering a cross-border interest payment is overdue. Numbers: £85,000 payment, 20% WHT = £17,000 exposure. Key moment: realising the treaty route could have reduced this to zero" produces a real section.

Write your selected devices and their sketches as a section in `EDITORIAL_DIR/outline.md` (see Step 4 format below).

---

## Step 4 — Build the outline

The outline is the writer's brief. It must be detailed enough that the writer never has to guess what goes in a section.

**Outline rules:**
- If reader pathways diverge (Step 2): structure by reader type, not topic. A reader who found their answer should be able to identify the next section as "not for me" and skip it — signpost this explicitly in section purposes.
- If reader pathways converge: structure must match the dominant SERP format from `DATA_DIR/keyword.json`
- Every table-stakes topic from `DATA_DIR/keyword.json` must appear somewhere — but in the section where the relevant reader actually needs it, not as a standalone topical section
- Every PAA question from `DATA_DIR/keyword.json` must be addressed in a named section or subsection
- Each section must state which reader type(s) it primarily serves
- Include a suggested word count per section (total must match `word_count_range` in keyword.json)
- Flag where external authority sources, data, or expert quotes should go
- Content devices must be embedded as named sections or subsections — not added as an afterthought

**Redundancy check — run this after drafting all sections:**
Identify any core fact that appears in more than two sections. If found, consolidate. One explanation, done well, is better than three explanations across different formats. Repetition is not comprehensiveness — it is a signal that the section structure needs merging.

Write `outline.md` to EDITORIAL_DIR:

```markdown
# Outline — [keyword]

**Chosen headline:** [paste from headline.md once confirmed]
**Target keyword:** [from keyword.json]
**Angle:** [one sentence from angle.md]
**Total target word count:** [from keyword.json]
**Structure type:** [Reader-pathway / Topic-ordered — from Step 2 decision]

---

## Reader pathways

| Reader type | Their question | Sections they need | Can stop after |
|---|---|---|---|
| [Reader type 1] | [Their single question] | [Section names] | [Section name] |
| [Reader type 2] | [Their single question] | [Section names] | [Section name] |

*If only one reader type: note that here and proceed with topic-ordered structure.*

---

## Selected content devices

| Device | Why it fits this angle | Where it goes |
|---|---|---|
| [Device name] | [One sentence] | [Section name or position] |
| [Device name] | [One sentence] | [Section name or position] |

**Execution sketches:**

*[Device name]:* Scenario/character: [specific]. Numbers/details: [specific]. Key moment: [what the reader understands at the end of this device section].

*[Device name]:* Scenario/character: [specific]. Numbers/details: [specific]. Key moment: [what the reader understands at the end of this device section].

---

## Table of contents
*Include for articles above 2,000 words or with multiple reader pathways. List section headings only — no descriptions. The writer renders this as a linked list in the draft.*

---

## Introduction (~[N] words)
**Purpose:** Hook the reader, establish the problem, signal what is different about this article.
**Serves:** All reader types
**Key points:**
- ...
**Note:** No preamble. First sentence should land the angle immediately.

---

## [Section heading] (~[N] words)
**Purpose:** [What this section does for the reader — not just what it covers]
**Serves:** [Which reader type(s) — be specific. If not all readers, flag: "Readers who [description] can skip this."]
**Key points:**
- ...
- ...
**PAA question addressed:** [if applicable — exact question from keyword.json]
**Authority signal needed:** [specific data point, statistic, or source type]
**Content device:** [if a device belongs here — name it and describe what it should produce]

---

## [Repeat for each section]

---

## Conclusion (~[N] words)
**Purpose:** Land one clear action per reader type. Do not summarise what the article already said.
**Serves:** All reader types
**Key points:**
- [One action or takeaway per reader type — no more]
**CTA:** [Specific — what should the reader do next?]

---

```

---

## Human gate

When both files are written, end your session with:

> **Headline options and outline ready.**
> Structure type: [Reader-pathway / Topic-ordered]
> Reader types mapped: [list them, or "single reader type"]
> Sections: [N] — approximately [total word count] words
> Content devices selected: [list them]
>
> Four things to do before pressing Enter:
> 1. Open `EDITORIAL_DIR/headline.md` — write your chosen headline in the "Chosen headline" field at the bottom.
> 2. Open `EDITORIAL_DIR/outline.md` — copy your chosen headline into the **Chosen headline** field at the top.
> 3. Review the reader pathway map — confirm the sections assigned to each reader type are complete and don't repeat core facts across pathways. If a reader type's sections contain the same core fact twice, consolidate before continuing.
> 4. Set the source strategy. Add a `source_strategy` field to the `outline.md` frontmatter and choose one:
>    - `evidence` — article makes factual claims requiring verifiable citations: medical dosing, legal rules, financial regulations, safety claims. Academic, government, and regulatory sources are the default.
>    - `lifestyle` — article is advisory, experiential, or cultural: recipes, wellness practices, travel, fashion, gift guides. Quality editorial sources (named-author magazine pieces, specialist editorial brands) are as valid as academic ones.
>    - `lifestyle+evidence` — article does both (e.g. a wellness piece that also cites pharmacology). Expands the source pool without restricting the primary tier.
>
> The writer works from `EDITORIAL_DIR/outline.md` only. Changes made here are the last chance to fix structure before the draft is written.
>
> Press Enter in the terminal when both files are updated and you're happy with the outline.
