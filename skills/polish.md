---
name: polish
description: "Step 7 — editorial pass + mechanical cleanup in one session. Merges revision and audit. Writes final polished draft.md."
---

# Skill: Polish
*Step 7 of the SEO Content System*

---

## Your job

You are editor and copy cleaner in one session. First, do a genuine editorial pass — cold read, fix logic gaps, weak sections, angle drift. Then work through the audit script outputs and fix everything they flag. Fix everything directly. Do not leave flags for another session.

---

## Inputs — read all of these before starting

| File | What it contains |
|---|---|
| `EDITORIAL_DIR/draft.md` | The draft — may include human edits made after the writing step |
| `EDITORIAL_DIR/work-log.md` | Prior step notes — scan for workarounds and human gate decisions |
| `EDITORIAL_DIR/writer-notes.md` | Writer observations — act on anything in your remit |
| `EDITORIAL_DIR/outline.md` | The approved outline — check the draft still honours structure and intent |
| `EDITORIAL_DIR/angle.md` | The editorial test everything is measured against |
| `BRAND_DIR/brand-voice-card.md` | Brand voice — final check that voice is consistent throughout |
| `BRAND_DIR/voice-dna.md` | Observed voice patterns — check opening, rhythm, teaching style (read if it exists) |
| `BRAND_DIR/audience-profiles.md` | Reader segments — use in the reader filter check (read if it exists) |
| `BRAND_DIR/de-ai-rules-card.md` | Banned vocabulary, structural anti-patterns, em dash rewriting patterns |
| `DATA_DIR/sources/index.json` | Research index — verify all claims are supported |
| `DATA_DIR/keyword.json` | Target keyword and PAA questions |
| `DATA_DIR/audit-flags.json` | Output of `scan_banned_phrases.py` — exact locations of HIGH and MEDIUM flags |
| `DATA_DIR/rhythm-analysis.json` | Output of `analyse_rhythm.py` — burstiness score, em dash count, sentence length data |

The audit scripts were run before this session launched. Read the output files directly — do not re-run them.

---

## Part 1 — Editorial pass

### Step 1 — Check human edits

Read `draft.md` and note anything that looks like a recent human edit. For each human edit, check: is it consistent with the angle, on-voice, and supported by sources? If an edit has a problem, flag it inline with `<!-- REVISION FLAG: [what the issue is] -->`. Do not silently fix human edits.

### Step 2 — Cold read

Read the article start to finish as a first-time reader. Write your cold read impressions at the top of `revision-notes.md` before running any other check:

- Did the opening make you want to keep reading?
- Is the insight present and clear by the halfway point?
- Is there anything that makes you want to click away?
- Does it end in the right place, or does it keep going after it's done?

These are your most honest signal. Write them before the checklist.

### Step 3 — Editorial checks

**Reader filter** (if `audience-profiles.md` exists): does the opening hit their trust signals? Does anything in the first 200 words trigger their bounce conditions? Does the article address their specific content frustrations?

**Angle delivery:** is the editorial position visible throughout, or does it fade after the introduction? Does the article actually do what the angle promises?

**Content devices:** find each device section. Is it executed fully and specifically — vivid, surprising, real? If it feels phoned in, flag it.

**Logic gaps:** does each section follow logically from the one before? Are there claims a sceptical reader would push back on that the article doesn't address?

**Voice DNA match** (if `voice-dna.md` exists): does the opening pattern, teaching style, and signature vocabulary match what was observed in real posts?

**Conclusion:** does it consolidate the angle, or just summarise sections? Is the CTA specific and genuinely useful?

**PAA coverage:** are all PAA questions from `keyword.json` answered clearly and findably?

### Step 4 — Fix editorial issues

Make direct edits to `draft.md` for everything you can fix. Fix, don't just flag. Only escalate to the human via `revision-notes.md` when fixing requires information only the brand has, or would reverse a deliberate human decision.

---

## Part 2 — Mechanical cleanup

**Scope:** banned phrases, rhythm, and structural standards only. Do not make editorial changes in this part — if you notice an editorial issue while working, note it in `work-log.md` and move on.

**What counts as language (yours to fix):** specific words used, sentence structure and length, transitions, phrasing that triggers a flag.

**What counts as substance (do not change):** factual claims, sources referenced, logical conclusions, positions taken.

### Step 5 — Resolve banned phrase flags

Read `DATA_DIR/audit-flags.json` fully.
- HIGH severity flags must all be resolved — no exceptions
- MEDIUM severity flags should be resolved unless fixing them would damage the sentence more than leaving them

Work through every HIGH flag first, then MEDIUM flags.

For each flag:
1. Read the full sentence in context
2. Understand what the sentence is trying to say
3. Rewrite the sentence to say the same thing without the flagged word or pattern
4. Verify the rewrite sounds natural and stays on-voice

If fixing requires restructuring the idea rather than swapping a word, make the minimum change necessary and add: `<!-- SUBSTANCE NOTE: [what changed and why] -->`.

**Common fixes:**

| Flagged pattern | Fix approach |
|---|---|
| "delve into" | "look at", "walk through", "break down" |
| "it's important to note" | Delete the phrase, start with the actual point |
| "in conclusion / in summary" | Delete. Start the conclusion with the substance directly. |
| "leverage" (verb) | "use", "apply", "draw on" |
| "nuanced" | Say what the nuance actually is instead |
| "comprehensive" | Cut it |
| Throat-clearing transitions | Delete the transition, join directly to the next point |

### Step 6 — Fix rhythm and em dashes

Read `DATA_DIR/rhythm-analysis.json`:
- `burstiness_score` — target above 1.2. Below 1.0 means the writing is too uniform.
- `em_dash_count` — must be zero. Fix every em dash directly using the rewriting patterns in `de-ai-rules-card.md`. Do not leave flags — rewrite them now.
- `mean_length` — flag if above 22 words
- `uniform_runs` — runs of 3+ same-length sentences need breaking up

If `burstiness_score` is below 1.2, find the sections with the most uniform sentence lengths.

**Rhythm fixes:**
- Break a long sentence into two, or add a short punchy sentence after a long one
- Merge two very short sentences if they read as choppy
- Vary the opening word of consecutive sentences — avoid starting 3+ in a row the same way

Target: no run of more than 3 sentences of similar length in the same paragraph.

### Step 7 — Final check

Verify the draft still passes `skills/content-standards.md`. Three rules most commonly broken during editing:
- No sentence exceeds 35 words
- No new AI structural patterns (throat-clearing, symmetrical sections)
- Brand voice maintained throughout

Confirm:
- [ ] All HIGH severity flags resolved
- [ ] MEDIUM severity flags resolved or noted
- [ ] All em dashes rewritten directly (not flagged — rewritten)
- [ ] Rhythm issues addressed
- [ ] Angle from `angle.md` still clear

---

## Step 8 — Save and write notes

Overwrite `EDITORIAL_DIR/draft.md` with the revised content. Update the frontmatter:

```markdown
---
title: [headline]
keyword: [keyword]
date: [original date]
revised: [today's date YYYY-MM-DD]
status: polished
---
```

Write `revision-notes.md` to EDITORIAL_DIR:

```markdown
# Revision Notes — [keyword]
*[today's date]*

## Cold read impressions
[Honest first-read reactions — before any checklist]

## Human edits found
- [Edit description] — [consistent / flagged — see inline comment]

## Ready to publish?
Yes / Not yet — [if not, what needs addressing]
```

Write one entry to `work-log.md`:

```
---
step: polish | [timestamp] | status: [complete | partial | error]
---
[Editorial changes made and why. HIGH severity flags: count and description. MEDIUM flags: count. Burstiness score, em dash count. Any items escalated to human in revision-notes.md. Overall assessment in one sentence.]
```

---

## Human gate

> **Polish complete.**
>
> Human edits found: [N]
> Editorial flags: [N — or "none"]
> HIGH severity fixes: [N]
> Em dashes rewritten: [N]
> Status: [Ready to publish / Needs attention — see revision-notes.md]
>
> Press Enter to build final output.
