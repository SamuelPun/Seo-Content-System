# 183-Day Rule Netherlands — Monx HK Article Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a publication-ready 1,400–1,600 word guide for Monx HK targeting Dutch people planning to relocate to Hong Kong who want a clear, unambiguous account of what the 183-day rule means for their Dutch tax exit.

**Architecture:** Spec → keyword + angle files → outline → research sources → draft → polish. Each file feeds the next. The spec at `docs/superpowers/specs/2026-06-15-183-day-rule-netherlands-dutch-expat-hk.md` is the single source of truth — refer back to it at every step.

**Content Stack:** Monx HK brand files (`brand/brand-voice-card.md`, `brand/voice-dna.md`, `brand/de-ai-guidelines.md`, `brand/audience-profiles.md`, `brand/content-prefs.md`), SEO content system skills (`skills/writing.md`, `skills/research-authority.md`, `skills/polish.md`, `skills/content-standards.md`).

---

## File map

| File | Created in | Purpose |
|------|-----------|---------|
| `content/183-day-rule-netherlands/data/keyword.json` | Task 1 | Keyword, PAA questions, intent |
| `content/183-day-rule-netherlands/editorial/angle.md` | Task 2 | Editorial angle and insight sentence |
| `content/183-day-rule-netherlands/editorial/headline.md` | Task 3 | Selected headline |
| `content/183-day-rule-netherlands/editorial/outline.md` | Task 4 | Section-by-section writer brief |
| `content/183-day-rule-netherlands/editorial/work-log.md` | Task 4 | Step tracking (initialised empty) |
| `content/183-day-rule-netherlands/editorial/writer-notes.md` | Task 4 | Editorial notes (initialised empty) |
| `content/183-day-rule-netherlands/data/sources/index.json` | Task 5 | Research index |
| `content/183-day-rule-netherlands/data/sources/[slug].md` | Task 5 | Individual source files (one per source) |
| `content/183-day-rule-netherlands/editorial/draft.md` | Task 6 | Full article draft |
| `content/183-day-rule-netherlands/editorial/draft.md` | Task 7 | Polished final draft (overwrites) |

**Base paths:**
- Article root: `/Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/`
- Brand files: `/Users/sam/Documents/SEO-content/monx-hk/brand/`
- Skills: `/Users/sam/Documents/seo-content-system/skills/`
- Spec: `/Users/sam/Documents/seo-content-system/docs/superpowers/specs/2026-06-15-183-day-rule-netherlands-dutch-expat-hk.md`

---

## Task 1: Set up directory structure and keyword.json

**Files:**
- Create: `content/183-day-rule-netherlands/data/sources/` (directory)
- Create: `content/183-day-rule-netherlands/editorial/` (directory)
- Create: `content/183-day-rule-netherlands/data/keyword.json`

- [ ] **Step 1: Create the directory structure**

```bash
mkdir -p /Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/data/sources
mkdir -p /Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/editorial
```

- [ ] **Step 2: Write keyword.json**

Write to `/Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/data/keyword.json`:

```json
{
  "keyword": "183 day rule Netherlands",
  "intent": "informational",
  "target_reader": "Dutch person planning relocation to Hong Kong, researching when they stop being a Dutch taxpayer",
  "locale": "Dutch expats, Dutch-language-background readers searching in English",
  "paa_questions": [
    "What is the 183 day rule in the Netherlands?",
    "Do I still pay Dutch taxes if I move to Hong Kong?",
    "How do I stop being a Dutch tax resident?",
    "What is the M-form in the Netherlands?",
    "How does the Netherlands–Hong Kong double tax arrangement work?"
  ],
  "competitor_sources": []
}
```

- [ ] **Step 3: Verify and commit**

Check both directories exist and keyword.json is valid JSON:
```bash
ls /Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/
cat /Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/data/keyword.json | python3 -m json.tool
```
Expected: directory tree printed, JSON validates without error.

```bash
git add /Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/
git commit -m "feat(monx-hk): scaffold 183-day-rule-netherlands article folder and keyword.json"
```

---

## Task 2: Create angle.md

**Files:**
- Create: `content/183-day-rule-netherlands/editorial/angle.md`

- [ ] **Step 1: Read the spec and brand voice card before writing**

Read both:
- `/Users/sam/Documents/seo-content-system/docs/superpowers/specs/2026-06-15-183-day-rule-netherlands-dutch-expat-hk.md`
- `/Users/sam/Documents/SEO-content/monx-hk/brand/brand-voice-card.md`

- [ ] **Step 2: Write angle.md**

Write to `/Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/editorial/angle.md`:

```markdown
---
keyword: 183 day rule Netherlands
target_reader: Dutch person actively researching a planned relocation to Hong Kong — already knows the 183-day rule is relevant, wants a precise and unambiguous account of what it means and what to do
insight: After reading this article, the reader will understand that the 183-day rule appears in two distinct places in Dutch tax law — the Netherlands–HK double tax arrangement and Dutch domestic residency determination — and that properly closing Dutch tax residency requires concrete emigration steps that go beyond simply crossing the 183-day threshold.
angle: Dutch tax exit guide with the 183-day rule as the anchor. Teaching frame, not correction frame — the reader is competent and researching; the article delivers clarity and removes ambiguity, not correction of a mistake.
reader_question: I'm moving to Hong Kong. I've come across the 183-day rule. When exactly do I stop being a Dutch taxpayer, and what steps do I need to take to make that exit stick?
source_strategy: evidence
---

## What this article does

Explains exactly what the 183-day rule triggers and where it appears — both in the Netherlands–HK Arrangement for the Avoidance of Double Taxation (Article 15, taxing rights over employment income) and in Dutch domestic tax residency determination (as a supporting signal that the reader has left). Then walks through the practical emigration checklist that formally closes Dutch tax residency: BRP de-registration, M-form filing, and severing Dutch ties. Ends with a brief contrast of what the reader is arriving into in Hong Kong (territorial tax, no capital gains, no Box 3 equivalent), and a Monx CTA.

## What this article does NOT cover

- The Dutch 30% ruling (incoming foreign workers — reverse direction)
- Dutch pension transfer mechanics on emigration
- HK company registration
- The Netherlands–HK arrangement beyond Article 15 (employment income)
- Tax treatment of Dutch property retained after emigration (mention that review is needed, do not go deep)
```

- [ ] **Step 3: Verify the insight sentence is present and the scope is tight**

Re-read `angle.md`. Confirm:
- `insight:` field is one clear sentence that passes this test: "If the article delivers nothing else, does it at least deliver this?"
- `source_strategy: evidence` is set (this is a regulatory/tax topic — primary sources only)
- The "does NOT cover" list matches the spec

- [ ] **Step 4: Commit**

```bash
git add /Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/editorial/angle.md
git commit -m "feat(monx-hk): add angle.md for 183-day-rule-netherlands"
```

---

## Task 3: Select headline and create headline.md

**Files:**
- Create: `content/183-day-rule-netherlands/editorial/headline.md`

- [ ] **Step 1: Read content-prefs.md headline preferences**

Read `/Users/sam/Documents/SEO-content/monx-hk/brand/content-prefs.md` — specifically the "Headline preferences" section. Key rules: specificity hook first priority, under 60 characters where possible, direct and informational, never vague or clickbait-y.

- [ ] **Step 2: Evaluate candidate headlines**

Score each against content-prefs.md:

| Candidate | Characters | Type | Notes |
|-----------|-----------|------|-------|
| The 183-Day Rule for Dutch Expats Moving to Hong Kong | 53 | Specificity hook | Clean, on-keyword, reader situation named |
| 183-Day Rule Netherlands: Your Dutch Tax Exit Guide | 51 | Specificity + outcome | Keyword-first, outcome named, under 60 chars |
| When Do Dutch Expats Stop Paying Dutch Tax? The 183-Day Rule Explained | 71 | Problem-first | Over 60 chars, question format |
| Moving to Hong Kong? How the 183-Day Rule Affects Your Dutch Taxes | 66 | Scenario-first | Over 60 chars |

Recommended selection: **"183-Day Rule Netherlands: Your Dutch Tax Exit Guide"** — hits the exact target keyword naturally at the start, names the outcome ("Tax Exit Guide"), stays under 55 characters, matches the specificity-hook priority from content-prefs.md.

- [ ] **Step 3: Write headline.md**

Write to `/Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/editorial/headline.md`:

```markdown
# Headline

**Selected:** 183-Day Rule Netherlands: Your Dutch Tax Exit Guide

**Rationale:** Keyword-first (matches target keyword exactly), names the outcome in the subtitle ("Tax Exit Guide"), 51 characters, specificity hook — consistent with content-prefs.md priority 1. Avoids question format and stays direct.

**Rejected candidates:**
- "The 183-Day Rule for Dutch Expats Moving to Hong Kong" — 53 chars, good but doesn't name the outcome
- "When Do Dutch Expats Stop Paying Dutch Tax? The 183-Day Rule Explained" — 71 chars, too long
- "Moving to Hong Kong? How the 183-Day Rule Affects Your Dutch Taxes" — 66 chars, scenario-first but over 60
```

- [ ] **Step 4: Commit**

```bash
git add /Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/editorial/headline.md
git commit -m "feat(monx-hk): add headline.md for 183-day-rule-netherlands"
```

---

## Task 4: Create outline.md and initialise work-log/writer-notes

**Files:**
- Create: `content/183-day-rule-netherlands/editorial/outline.md`
- Create: `content/183-day-rule-netherlands/editorial/work-log.md`
- Create: `content/183-day-rule-netherlands/editorial/writer-notes.md`

- [ ] **Step 1: Write outline.md**

Write to `/Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/editorial/outline.md`:

```markdown
---
title: 183-Day Rule Netherlands: Your Dutch Tax Exit Guide
keyword: 183 day rule Netherlands
target_length: 1400–1600 words
source_strategy: evidence
---

# Outline

## Introduction (~150 words)

**Opening strategy:** Teaching frame. Open inside the reader's research moment — they are planning the move to Hong Kong, they have come across the 183-day rule, and they want a precise answer to one question: when and how do you stop being a Dutch taxpayer? Name that question directly. Then state what this guide covers: what the 183-day rule actually triggers, where it appears, and what steps formally close Dutch tax residency. No definition in sentence one. No "most people get this wrong" hook.

**Angle visible by sentence 3:** The reader will leave with a clear, unambiguous picture — not a summary, not a "it depends."

**PAA to answer:** None assigned to intro.

**Authority signal needed:** None — framing only.

---

## What It Means to Be a Dutch Tax Resident (~200 words)

The Belastingdienst (Dutch Tax and Customs Administration) taxes Dutch residents on their **worldwide income** — Box 1 (employment income and business profits), Box 2 (income from substantial shareholdings), Box 3 (savings and investments). Explain each Box briefly on first use.

The key point: Dutch tax residency is determined by the **totality of your ties** to the Netherlands — not simply by how many days you are present. The Belastingdienst looks at: where you have your permanent home, where your family lives, where your bank accounts and financial interests are, where your social life is centred. Days are one signal in that picture, not the only one.

**PAA to answer:** "What is the 183 day rule in the Netherlands?" — answer partially here (days are one signal), complete in the next section.

**Authority signal needed:** Belastingdienst official guidance on tax residency — cite the specific criterion list.

---

## Where the 183-Day Rule Actually Appears (~250 words)

The rule shows up in two distinct places. Most articles conflate them. This section separates them.

**Place 1 — The Netherlands–HK Arrangement for the Avoidance of Double Taxation (Article 15)**

If you work in Hong Kong for a Dutch employer and spend **more than 183 days in Hong Kong** within a 12-month period, Hong Kong gets primary taxing rights over your employment income. Under 183 days, the Netherlands may still tax that income. Use the full official name of the arrangement on first reference — not just "tax treaty."

**Place 2 — Dutch domestic residency determination**

Spending more than 183 days outside the Netherlands in a calendar year is used by the Belastingdienst as a supporting signal in residency determination. It does not automatically end Dutch tax residency — you still need the formal exit steps (covered in the next section) — but it significantly strengthens your position.

**Content device: Worked numeric example**

Dutch employee. Annual salary €120,000. Moves to HK on 1 July (183rd day of the year approximately).

- **Before the move (Jan–Jun, 181 days in NL):** NL taxes this €60,000 portion. Box 1 rate: 36.97% up to €75,518, 49.50% above. On €60,000: approximately €22,182 Dutch income tax.
- **After the move (Jul–Dec, crosses 183 days in HK by year-end):** HK gets taxing rights on the Jul–Dec €60,000 (approximately HK$660,000). After basic HK allowance (HK$132,000), taxable income ~HK$528,000. HK salaries tax at effective ~13%: approximately HK$68,640 (≈€6,240).
- **Full-year comparison:** If still in NL for the full year, Box 1 tax on €120,000 ≈ €49,923. After the move: NL portion (~€22,182) + HK portion (~€6,240) = ~€28,422. Difference: ~€21,500 in the transition year alone.

Note the figures are illustrative — actual liability depends on deductions, allowances, and the exact departure date. Flag this briefly.

**PAA to answer:** "How does the Netherlands–Hong Kong double tax arrangement work?" — answer here.

**Authority signal needed:** Official text of the Netherlands–HK Arrangement, Article 15. Belastingdienst page on working abroad / emigration.

---

## How to Close Your Dutch Tax Residency: The Emigration Checklist (~300 words)

Four concrete steps. Use numbered step format (H3 or numbered list) — this is a process section.

**Step 1 — De-register from the BRP**
The BRP (Basisregistratie Personen — the Dutch municipal population register) is the administrative record of where you live. De-register at your local gemeente (municipality) before you leave. This is the official signal to Dutch authorities that you have departed. Without it, the Belastingdienst has no administrative basis to treat you as non-resident. Explain "gemeente" on first use.

**Step 2 — File the M-form (M-biljet)**
The M-form (M-biljet) is the departure-year tax return filed with the Belastingdienst for the year you leave. It covers income earned in the Netherlands up to your departure date and formally declares you stopped being a Dutch resident mid-year. Explain "M-biljet" on first use.

**Step 3 — Sever Dutch ties**
The Belastingdienst looks at the full picture. Ties that keep a residency claim alive: Dutch property you own or rent (sell, transfer, or let commercially), Dutch bank accounts (close or restructure), Dutch-registered vehicles, frequent return visits (frequency and duration both matter). Review each category before you go.

**Step 4 — Review Dutch pension and investment accounts**
Dutch pension products (pensioen) and certain investment accounts have specific emigration treatment. This is worth a dedicated review with a cross-border tax adviser before departure — mention it, don't go deep.

**Closing note:** De-registering from the BRP is necessary but not sufficient on its own. The Belastingdienst can and does challenge non-residency claims when Dutch ties remain active. Steps 3 and 4 are what make Step 1 stick.

**PAA to answer:** "How do I stop being a Dutch tax resident?" and "What is the M-form Netherlands?" — answer both here.

**Authority signal needed:** Belastingdienst official guidance on emigration/M-form. RVO or gemeente official guidance on BRP de-registration.

---

## What Happens If You Don't Complete the Exit (~200 words)

If the Belastingdienst rules you never fully left Dutch tax residency, the outcome is dual-residency status — filing obligations in both the Netherlands and Hong Kong, with potential back-tax claims on your HK income for every year the NL residency claim holds.

The Netherlands–HK Arrangement provides double taxation relief, but it does not eliminate the filing burden or the risk of penalties for non-disclosure of foreign income.

**Short scenario (1 paragraph):** Dutch expat, three years in Hong Kong, never filed the M-form, retained a Dutch apartment generating rental income, returned to the Netherlands six times per year for work. Belastingdienst audit: Dutch tax residency upheld for all three years. Back taxes on HK salary at Box 1 rates (up to 49.5%), plus 4% belastingrente (interest on late payment), plus a potential verzuimboete (negligence penalty). On a €150,000 annual HK salary, back-tax exposure over three years could exceed €100,000 before penalties.

**Editorial aside:** Permitted here — a short dry reaction to the scale of the penalty figure.

**End note:** The exit process is straightforward when done properly. This section exists so you know what "not properly" looks like.

**PAA to answer:** "Do I still pay Dutch taxes if I move to Hong Kong?" — answer definitively here.

**Authority signal needed:** Belastingdienst page on belastingrente. General NL-HK arrangement double taxation relief provisions.

---

## What You're Landing Into: Hong Kong's Tax System (~200 words)

Contrast section. Punchy, not promotional.

Hong Kong uses **territorial taxation**: only income sourced in Hong Kong is taxed. Foreign income — including income from investments outside HK, foreign bank interest, or overseas business profits — is not taxed in Hong Kong at all. No capital gains tax. No equivalent of Box 3 (no annual wealth tax on savings and investments). No inheritance tax.

**Salaries tax rates:** Progressive: 2%, 6%, 10%, 14%, 17% on successive HK$50,000 bands. Standard rate capped at **15%** of net income (after deductions). If the standard rate calculation is lower than the progressive rate, you pay the standard rate. For most Dutch relocators earning a typical professional salary, the effective HK salaries tax rate will be significantly below the Dutch Box 1 effective rate.

Short comparison table:

| | Netherlands | Hong Kong |
|---|---|---|
| Worldwide income taxed? | Yes | No — territorial only |
| Capital gains tax | No (but Box 3 on wealth) | No |
| Wealth / savings tax | Yes (Box 3, ~1.2–1.71%) | No |
| Top income tax rate | 49.5% | 17% (or 15% standard) |

**Authority signal needed:** HKIRD salaries tax rates page.

---

## How Monx Can Help (~100 words)

Monx sets up Hong Kong employment structures and company arrangements so that your income is properly HK-sourced from day one. That matters in two directions: it determines your Hong Kong salaries tax treatment, and it strengthens your Dutch residency exit argument by making it clear where your economic activity is now based.

If you're planning the move and want to make sure your structure is set up correctly from the start, get in touch: hello@monx.team.

---

*End of outline.*
```

- [ ] **Step 2: Initialise work-log.md and writer-notes.md**

Write to `/Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/editorial/work-log.md`:

```markdown
# Work Log — 183-Day Rule Netherlands
```

Write to `/Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/editorial/writer-notes.md`:

```markdown
# Writer Notes — 183-Day Rule Netherlands
```

- [ ] **Step 3: Self-check the outline**

Before committing, verify:
- Every section from the spec is covered (7 sections including intro ✓)
- Every PAA question from keyword.json is assigned to a section ✓
- The worked numeric example in Section 3 has real numbers (not "e.g., X%") ✓
- The comparison table in Section 6 has real values ✓
- No section says "TBD" or "cover this topic" without specifying what to say ✓

- [ ] **Step 4: Commit**

```bash
git add /Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/editorial/
git commit -m "feat(monx-hk): add outline, work-log, and writer-notes for 183-day-rule-netherlands"
```

---

## Task 5: Research — gather and verify sources

**Files:**
- Create: `content/183-day-rule-netherlands/data/sources/index.json`
- Create: `content/183-day-rule-netherlands/data/sources/belastingdienst-tax-residency.md`
- Create: `content/183-day-rule-netherlands/data/sources/nl-hk-arrangement-article15.md`
- Create: `content/183-day-rule-netherlands/data/sources/belastingdienst-m-form.md`
- Create: `content/183-day-rule-netherlands/data/sources/brp-deregistration.md`
- Create: `content/183-day-rule-netherlands/data/sources/hkird-salaries-tax.md`

Read `skills/research-authority.md` in full before starting this task.

- [ ] **Step 1: Build a research brief**

Before searching, list every specific fact in the outline that needs a primary source:

1. **Belastingdienst tax residency criteria** — the official list of ties used to determine Dutch tax residency (home, family, bank accounts, social life). Source: belastingdienst.nl.
2. **Netherlands–HK Arrangement, Article 15** — the exact 183-day threshold and the taxing-rights rule for employment income. Source: official treaty text or Dutch government publication.
3. **Dutch Box 1 tax rates** — the current rates (36.97% / 49.50%) and their income thresholds. Source: belastingdienst.nl.
4. **M-form (M-biljet) guidance** — the official description of the M-form, who must file it, and when. Source: belastingdienst.nl.
5. **BRP de-registration process** — how to de-register at the gemeente. Source: government.nl or rijksoverheid.nl.
6. **HK salaries tax rates** — the current progressive rates, standard rate cap (15%), and basic allowance (HK$132,000). Source: hkird.gov.hk.
7. **Belastingrente rate** — the current interest rate on late Dutch tax payment (used in Section 5 scenario). Source: belastingdienst.nl.

- [ ] **Step 2: Fetch and verify each source**

For each source in the research brief, web-search and/or fetch the primary URL. Extract verbatim the specific passages that support each claim in the outline. Do not paraphrase. Flag any claim you cannot verify with `[SOURCE NEEDED]`.

Priority order: sources 1, 2, 4, 6 are essential (used in multiple sections). Sources 3, 5, 7 are supporting.

- [ ] **Step 3: Write individual source files**

For each verified source, write a file to `data/sources/[slug].md` in this format:

```markdown
---
slug: [filename without .md]
title: [Page title from source]
url: [exact URL]
fetched: 2026-06-15
type: government / official
sections_used: [list of outline sections this source supports]
---

## Relevant extracts

[Verbatim quoted passages from the source, with enough context to cite accurately. Use > blockquote format.]

## Key facts for the article

- [Bullet list of specific figures, dates, or policy statements extracted from the source]
```

- [ ] **Step 4: Write sources/index.json**

Write to `data/sources/index.json` once all source files are created:

```json
{
  "sources": [
    {
      "slug": "belastingdienst-tax-residency",
      "title": "[actual title]",
      "url": "[actual URL]",
      "sections": ["What It Means to Be a Dutch Tax Resident", "Where the 183-Day Rule Actually Appears"]
    },
    {
      "slug": "nl-hk-arrangement-article15",
      "title": "[actual title]",
      "url": "[actual URL]",
      "sections": ["Where the 183-Day Rule Actually Appears"]
    },
    {
      "slug": "belastingdienst-m-form",
      "title": "[actual title]",
      "url": "[actual URL]",
      "sections": ["How to Close Your Dutch Tax Residency: The Emigration Checklist"]
    },
    {
      "slug": "brp-deregistration",
      "title": "[actual title]",
      "url": "[actual URL]",
      "sections": ["How to Close Your Dutch Tax Residency: The Emigration Checklist"]
    },
    {
      "slug": "hkird-salaries-tax",
      "title": "[actual title]",
      "url": "[actual URL]",
      "sections": ["What You're Landing Into: Hong Kong's Tax System"]
    }
  ],
  "gaps": []
}
```

Replace `[actual title]` and `[actual URL]` with the real values from the fetched sources. If any source could not be verified, add it to the `"gaps"` array with a note.

- [ ] **Step 5: Verify the worked example numbers**

The outline contains a worked numeric example (Section 3). Before the writing step, verify:
- Dutch Box 1 rate for €60,000 income is correct (36.97% on amounts up to €75,518) — check belastingdienst.nl for the current tax year
- HK basic allowance is HK$132,000 — check hkird.gov.hk
- HK progressive salaries tax bands — confirm the 2%/6%/10%/14%/17% structure and the HK$50,000 band widths
- The example note that figures are illustrative is included in the outline ✓

If any figure has changed from what the outline states, update the outline before the writing step.

- [ ] **Step 6: Commit**

```bash
git add /Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/data/
git commit -m "feat(monx-hk): add research sources for 183-day-rule-netherlands"
```

---

## Task 6: Write draft.md

**Files:**
- Create: `content/183-day-rule-netherlands/editorial/draft.md`
- Modify: `content/183-day-rule-netherlands/editorial/work-log.md`
- Modify: `content/183-day-rule-netherlands/editorial/writer-notes.md`

Read `skills/writing.md` in full before starting this task. Then read ALL of these before writing a single word:
1. `editorial/outline.md` — your section-by-section brief
2. `editorial/angle.md` — the editorial position
3. `data/sources/index.json` + all individual source files
4. `data/keyword.json`
5. `brand/brand-voice-card.md`
6. `brand/voice-dna.md`
7. `brand/de-ai-guidelines.md`
8. `brand/audience-profiles.md`
9. `skills/content-standards.md`

- [ ] **Step 1: Anchor on the insight**

Write the insight sentence as the first line of `writer-notes.md`:

```
Insight: After reading this article, the reader will understand that the 183-day rule appears in two distinct places in Dutch tax law — the Netherlands–HK double tax arrangement and Dutch domestic residency determination — and that properly closing Dutch tax residency requires concrete emigration steps that go beyond simply crossing the 183-day threshold.
```

- [ ] **Step 2: Write the draft**

Write `draft.md` to `editorial/`. Follow the outline exactly for section order and H2 headings. Apply brand voice throughout.

Voice reminders specific to this article:
- Teaching frame throughout — the reader is competent. Never condescend.
- Every Dutch term (Belastingdienst, BRP, M-biljet, gemeente, Box 1/2/3) explained on **first use only** — then use normally.
- The worked numeric example in the "Where the 183-Day Rule Actually Appears" section must be fully executed with real numbers from the verified sources.
- The comparison table in "What You're Landing Into" must use real HK salaries tax rates from `hkird-salaries-tax.md`.
- One editorial aside in the "What Happens If You Don't Complete the Exit" section — short, dry, at the moment the penalty figure lands.
- Zero em dashes. Write around every one.
- No throat-clearing transitions ("Now that we've covered X, let's look at Y").
- No sentence over 35 words.
- Target keyword ("183-day rule Netherlands" or close variant) in the first 100 words.
- Keyword or close variant in at least 2–3 H2 headings.

Draft format:

```markdown
---
title: 183-Day Rule Netherlands: Your Dutch Tax Exit Guide
keyword: 183 day rule Netherlands
date: 2026-06-15
status: draft
---

# 183-Day Rule Netherlands: Your Dutch Tax Exit Guide

[Introduction]

## What It Means to Be a Dutch Tax Resident

[...]

## Where the 183-Day Rule Actually Appears

[...]

## How to Close Your Dutch Tax Residency: The Emigration Checklist

[...]

## What Happens If You Don't Complete the Exit

[...]

## What You're Landing Into: Hong Kong's Tax System

[...]

## How Monx Can Help

[...]

---

*Sources used:*
- [Source title] — [URL]
```

- [ ] **Step 3: Quality check before finishing**

Before writing the last line, re-read the full draft and verify:

- [ ] Every section from outline.md is present
- [ ] Every PAA question from keyword.json is answered
- [ ] The insight from angle.md is visible throughout — not just in the intro
- [ ] No banned vocabulary (check brand/de-ai-guidelines.md)
- [ ] No AI structural patterns (throat-clearing, parallel list overuse, restated questions)
- [ ] No em dashes
- [ ] Brand voice consistent with brand-voice-card.md
- [ ] All sources cited are from data/sources/ — no invented data
- [ ] Word count is between 1,260 and 1,760 words (10% either side of 1,400–1,600)
- [ ] Target keyword appears in the first 100 words
- [ ] Keyword or close variant appears in at least 2–3 H2 headings

- [ ] **Step 4: Update work-log.md**

Append to `editorial/work-log.md`:

```
---
step: writing | 2026-06-15 | status: complete
---
[Word count]. [Any sections that deviated from outline.md and why. Any data gaps that affected the writing.]
```

- [ ] **Step 5: Commit**

```bash
git add /Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/editorial/
git commit -m "feat(monx-hk): add draft.md for 183-day-rule-netherlands"
```

---

## Task 7: Polish — editorial pass and de-AI cleanup

**Files:**
- Modify: `content/183-day-rule-netherlands/editorial/draft.md`
- Modify: `content/183-day-rule-netherlands/editorial/work-log.md`

Read `skills/polish.md` in full before starting this task. Then read:
1. `editorial/draft.md`
2. `editorial/work-log.md` — scan for workarounds and decisions
3. `editorial/writer-notes.md` — act on anything in your remit
4. `editorial/outline.md` — verify structure is still honoured
5. `editorial/angle.md`
6. `brand/brand-voice-card.md`
7. `brand/voice-dna.md`
8. `brand/audience-profiles.md`
9. `brand/de-ai-guidelines.md`

- [ ] **Step 1: Cold read**

Read the article start to finish as a first-time Dutch reader planning a move to Hong Kong. Write cold-read impressions in `editorial/writer-notes.md` under a `## Polish pass — cold read` header:
- Did the opening make you want to keep reading?
- Is the insight clear by the halfway point?
- Does any section feel like filler?
- Does the worked example land?
- Does the CTA feel like a natural next step or a bolt-on?

- [ ] **Step 2: Editorial fixes**

Fix any structural or logic gaps surfaced by the cold read directly in `draft.md`. Note each fix in `writer-notes.md` under `## Polish pass — editorial fixes`.

Common issues to check for this article specifically:
- Dutch terms: are all 6 terms in the spec (Belastingdienst, BRP, M-biljet, gemeente, Box 1/2/3, Arrangement) explained on first use and then used naturally?
- Does the worked numeric example have a clear "therefore" takeaway sentence after the numbers?
- Does the "What Happens If You Don't Complete the Exit" section end on the reassuring note ("straightforward when done properly") and not on doom?
- Does the comparison table in Section 6 render correctly in Markdown?

- [ ] **Step 3: De-AI sweep**

Apply `brand/de-ai-guidelines.md` in full. Four levels to check:

1. **Vocabulary level** — scan for banned words. Common ones to watch for in a tax/regulatory article: "delve," "leverage," "utilize," "robust," "holistic," "in order to," "ensure," "game-changer," "navigate the complexities of," "in today's fast-paced," "it is important to note."
2. **Sentence rhythm** — check for uniform sentence length. Use `brand/voice-dna.md` rhythm patterns: long setup → short payoff fragments is the Monx HK move. Burstiness should be above 1.2.
3. **Structural patterns** — check for: throat-clearing transitions, parallel list overuse (three bullet lists in a row with identical structure), sections that open by restating their own heading.
4. **Human signals** — check for: at least one dry editorial aside in Section 5, at least one "no X, no Y, no Z" triple construction (fits the HK tax section), at least one "Translation:" or analogy for an abstract mechanism.

Fix everything directly in `draft.md`. Do not leave flags.

- [ ] **Step 4: Final word count check**

Count the words in `draft.md`. Target: 1,400–1,600 words. If over 1,760 or under 1,260, revisit.

- [ ] **Step 5: Update work-log.md**

Append to `editorial/work-log.md`:

```
---
step: polish | 2026-06-15 | status: complete
---
[What was fixed. Word count after polish.]
```

- [ ] **Step 6: Commit**

```bash
git add /Users/sam/Documents/SEO-content/monx-hk/content/183-day-rule-netherlands/editorial/
git commit -m "feat(monx-hk): polish pass complete for 183-day-rule-netherlands"
```

---

## Self-review checklist

**Spec coverage:**

| Spec requirement | Covered in |
|-----------------|-----------|
| 7 sections including intro | Tasks 4, 6 |
| Teaching frame opening (not correction frame) | Task 4 outline, Task 6 writing instruction |
| Dutch worldwide taxation / Box 1/2/3 explained | Task 4 outline Section 2 |
| 183-day rule in both treaty (Article 15) and domestic law | Task 4 outline Section 3 |
| Worked numeric example €120,000 salary | Task 4 outline Section 3, Task 5 verification |
| BRP, M-form, severing ties checklist | Task 4 outline Section 4 |
| Incomplete exit scenario with real numbers | Task 4 outline Section 5 |
| HK territorial tax contrast table | Task 4 outline Section 6 |
| Monx CTA at end only | Task 4 outline Section 7 |
| All 6 Dutch terms explained on first use | Task 6 voice reminders |
| Evidence source strategy (primary sources only) | Task 2 angle.md, Task 5 |
| De-AI pass | Task 7 |
| Target keyword in first 100 words + H2 headings | Task 6 voice reminders |
| 1,400–1,600 word target | Task 6 quality check, Task 7 |

**Placeholder scan:** No TBD, TODO, or vague instruction in any task. The worked example numbers are specific. The source slugs are named. The checklist items are exact.

**Consistency check:** `source_strategy: evidence` set in both `angle.md` (Task 2) and `outline.md` frontmatter (Task 4). H2 headings used in the outline match the headings in the draft format template (Task 6). The insight sentence in `writer-notes.md` (Task 6 Step 1) matches the insight in `angle.md` (Task 2).
