---
name: audit
description: "Step 8 — mechanical cleanup: banned phrases, rhythm, sentence length. Runs scan_banned_phrases.py and analyse_rhythm.py then resolves all flags."
---

# Skill: Audit
*Step 8 of the SEO Content System — runs after the revision step*

---

## Scope

**Mechanical cleanup only.** The draft has been editorially reviewed and approved. Your job is banned phrases, rhythm, and structural standards — not editorial judgment. If you notice an editorial problem the revision step missed, note it in `work-log.md` and move on.

**What counts as substance (do not change):**
- The factual claim, statistic, or figure
- The source being referenced
- The logical argument or conclusion of a paragraph
- The position taken on a contested point

**What counts as language (yours to fix):**
- The specific words used
- Sentence structure and length
- Transitions between sentences
- Phrasing that triggers a flag

**Em dashes require sentence rewrites, not punctuation patches.** Do not fix em dashes in this step. Flag each one with an inline comment and let revision handle the rewrite:

```
<!-- AUDIT FLAG: em dash — sentence needs rewriting in revision -->
```

Place the comment on the line immediately after the flagged sentence. Do not touch the sentence itself.

---

## Inputs — read all of these before touching the draft

| File | What it contains |
|---|---|
| `EDITORIAL_DIR/draft.md` | The article draft to audit and revise |
| `DATA_DIR/audit-flags.json` | Output of `scan_banned_phrases.py` — exact locations of HIGH and MEDIUM flags |
| `DATA_DIR/rhythm-analysis.json` | Output of `analyse_rhythm.py` — burstiness score, em dash count, sentence length data |
| `BRAND_DIR/de-ai-guidelines.md` | Full de-AI rules — your editing standard |
| `BRAND_DIR/brand-voice-card.md` | Brand voice — ensure revisions stay on-voice |
| `BRAND_DIR/voice-dna.md` | Observed rhythm and opening patterns — reference when rewriting to stay consistent (read if it exists) |
| `EDITORIAL_DIR/angle.md` | The approved angle — ensure revisions don't drift from it |
| `skills/content-standards.md` | Structural standards — reference for sentence cap, paragraph length, intro rules, CTA |

---

## Step 0 — Run the audit scripts

Run both scripts before reading any outputs:

```bash
python3 scripts/scan_banned_phrases.py \
    --draft "EDITORIAL_DIR/draft.md" \
    --out-dir "DATA_DIR"

python3 scripts/analyse_rhythm.py \
    --draft "EDITORIAL_DIR/draft.md" \
    --out-dir "DATA_DIR"
```

Substitute actual paths for `EDITORIAL_DIR` and `DATA_DIR`. Both scripts write their output files directly to `DATA_DIR`.

---

## Step 1 — Read the audit outputs

**Read `DATA_DIR/audit-flags.json` fully.**
- HIGH severity flags must all be resolved — no exceptions
- MEDIUM severity flags should be resolved unless fixing them would damage the sentence more than leaving them
- Note the exact line numbers and phrases flagged

**Read `DATA_DIR/rhythm-analysis.json` fully.**
- `burstiness_score` — target above 1.2. Below 1.0 means the writing is too uniform.
- `em_dash_count` — must be zero. Any em dash gets an AUDIT FLAG comment (see Scope above).
- `mean_length` — flag if above 22 words
- `uniform_runs` — runs of 3+ same-length sentences need breaking up

---

## Step 2 — Resolve banned phrase flags

Work through every HIGH flag first, then MEDIUM flags.

For each flag:
1. Read the full sentence in context — not just the flagged phrase
2. Understand what the sentence is trying to say
3. Rewrite the sentence to say the same thing without the flagged word or pattern
4. Verify the rewrite sounds natural and stays on-voice

If fixing a phrase requires restructuring the idea rather than swapping a word, make the minimum change necessary and add: `<!-- SUBSTANCE NOTE: [what changed and why] -->`. This flags it for human review without blocking the audit.

**Common fixes:**

| Flagged pattern | Fix approach |
|---|---|
| "delve into" | "look at", "walk through", "break down" |
| "it's important to note" | Delete the phrase, start with the actual point |
| "in conclusion / in summary" | Delete. Start the conclusion with the substance directly. |
| "leverage" (verb) | "use", "apply", "draw on" |
| "nuanced" | Say what the nuance actually is instead |
| "comprehensive" | Cut it — if the content is comprehensive, that will be obvious |
| "seamlessly" | Cut or replace with what actually happens |
| Throat-clearing transitions | Delete the transition, join directly to the next point |

---

## Step 3 — Fix rhythm issues

If `burstiness_score` is below 1.2, find the sections with the most uniform sentence lengths.

**Rhythm fixes:**
- Break a long sentence into two, or add a short punchy sentence after a long one
- Merge two very short sentences if they read as choppy
- Move a clause to its own sentence for emphasis
- Vary the opening word of consecutive sentences — avoid starting 3+ in a row the same way

Target: no run of more than 3 sentences of similar length in the same paragraph.

---

## Step 4 — Final check

After resolving all flags and rhythm issues, verify the draft still passes `skills/content-standards.md`. Three rules most commonly broken during editing:
- No sentence exceeds 35 words (introduced when rewriting complex flags)
- No new AI structural patterns (throat-clearing, symmetrical sections)
- Brand voice maintained — no on-voice sentences broken by edits

Then confirm:
- [ ] All HIGH severity flags resolved
- [ ] MEDIUM severity flags resolved or noted
- [ ] Rhythm issues addressed
- [ ] Em dashes flagged with AUDIT FLAG comments (not fixed — revision owns those)
- [ ] Angle from `angle.md` still clear

---

## Step 5 — Save the revised draft

Overwrite `EDITORIAL_DIR/draft.md` with the revised content. Update the frontmatter:

```markdown
---
title: [headline]
keyword: [keyword]
date: [original date]
revised: [today's date YYYY-MM-DD]
status: audited
---
```

Write one entry to `work-log.md`:

```
---
step: audit | [timestamp] | status: [complete | partial | error]
---
[HIGH severity flags: count and description. MEDIUM flags: count. Rhythm: burstiness score, em dash count. Any flags requiring human judgment. Overall assessment in one sentence.]
```

Write to `writer-notes.md` only for qualitative observations the scripts cannot catch:
- A passage that passes all checks but still reads as AI to a human reader
- A structural issue that is technically compliant but feels wrong
- A place where the content is technically sourced but the claim feels overstated

Do not duplicate what is already in `audit-flags.json` or `rhythm-analysis.json`.
