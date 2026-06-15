---
name: revision
description: "Step 7 — editorial cold read and quality pass on the draft. Fix-not-flag mandate. Runs before audit."
---

# Skill: Revision
*Step 7 of the SEO Content System — runs before the audit step*

---

## Order note

Revision runs *before* the audit step. The audit fixes mechanical issues (banned phrases, rhythm, structural standards). Your job is editorial quality — not language cleanup. If you spot a banned phrase or rhythm issue while editing, note it in `work-log.md` for the audit to handle. Do not fix mechanical issues in this step.

---

## Your job

You are an active editor. The human has reviewed the draft and may have made their own edits directly to `draft.md`. Your job is to:

1. Check that any human edits are consistent with the angle, brand voice, and article structure
2. Do a full editorial pass — redundancy, weak hooks, thin device execution, buried insights, conclusions that don't land
3. Fix what you can directly. Ensure the article is genuinely ready to publish, not just technically compliant.

**Fix, don't just flag.** Document every substantive change in `work-log.md`. Only escalate to the human via `revision-notes.md` when fixing requires information only the brand has, or would reverse a deliberate human decision.

---

## Inputs — read all of these

| File | What it contains |
|---|---|
| `EDITORIAL_DIR/draft.md` | The draft — may include human edits |
| `EDITORIAL_DIR/work-log.md` | Prior step notes — scan for workarounds and human gate decisions |
| `EDITORIAL_DIR/writer-notes.md` | Writer observations — act on what's in revision's remit |
| `EDITORIAL_DIR/outline.md` | The approved outline — check the draft still honours structure and intent |
| `EDITORIAL_DIR/angle.md` | The editorial test everything is measured against |
| `BRAND_DIR/brand-voice-card.md` | Brand voice — final check that voice is consistent throughout |
| `BRAND_DIR/voice-dna.md` | Observed voice patterns — check opening, rhythm, teaching style match (read if it exists) |
| `BRAND_DIR/audience-profiles.md` | Reader segments — calibrate intro and tone checks (read if it exists) |
| `DATA_DIR/sources/index.json` | Research index — verify all claims are supported |
| `DATA_DIR/keyword.json` | Target keyword and PAA questions — final SEO check |

---

## Step 1 — Identify any human edits

Read `draft.md` and note anything that looks like a recent human edit — sections differing from the outline, new content added, passages rewritten in a different register.

For each human edit, check: is it consistent with the angle, on-voice, and supported by sources? If an edit has a problem, flag it inline with `<!-- REVISION FLAG: [what the issue is] -->`. Do not silently fix human edits.

---

## Step 2 — Cold read first

Read the article start to finish as a first-time reader who knows nothing about how it was built. Note genuine reactions:
- Did the opening make you want to keep reading?
- Is the insight present and clear by the halfway point?
- Did anything make you want to click away — a vague section, throat-clearing?
- Does it end in the right place, or does it keep going after it's done?

Write your cold read impressions at the top of `revision-notes.md` before running any other check. These are your most honest signal.

---

## Step 3 — Editorial quality pass

Run each check below. Fix directly where you can. Flag for human attention only when fixing requires brand-specific information.

### Intro pressure test

The introduction is the highest-leverage part of the article. Fix it first.

**Redundancy.** Does the intro say the same thing more than once across paragraphs? If the same point — "this thing is different from the familiar thing," "most people don't know this exists," "you are about to learn something" — appears in two or more forms before the first H2, collapse it into the strongest version. Four paragraphs establishing the same premise is one paragraph that needs editing.

**Curiosity gap.** Does the intro close with something that compels the reader forward? "This article covers X, Y, and Z" is not a curiosity gap — it is a table of contents. The closing line of the intro should name something the reader does not yet know, set up a tension that requires reading to resolve, or make a claim specific enough to demand explanation. If the closing line could be cut without the reader noticing, rewrite it.

**Opening hook.** Does the first sentence do work? It should place the reader in a situation or create an immediate problem. If it begins with a definition, a generic orientation statement, or a question, rewrite it.

**Cultural and geographic references.** Are all examples and comparisons immediately legible to the target audience? A reference that is obvious to one regional audience may be opaque or irrelevant to another. Flag any example a reader outside the reference's origin country or culture would not instantly understand. Replace it with a direct, audience-local equivalent, or cut it.

---

### Structure audit

**Section redundancy.** Does any section substantially repeat what the intro, or a prior section, has already established? If a section opens by restating a distinction or premise already made, cut the restatement and begin with what is new. This is most common in the second major section of articles with a strong establishing intro: the writer restated the setup because it felt needed — but the reader already has it.

**Formatting consistency.** If a structural element appears more than once — venue names, product entries, tip callouts, people profiles — it must be formatted consistently throughout. Bold in one place and H3 in another is a problem. Pick the treatment that best serves readability and apply it uniformly to every instance.

**Self-referential labels.** Does the article use abstract labels ("Type 1," "Type 2," "Option A") in running prose as substitutes for the thing's actual name? Labels can exist in a summary table where they aid comparison. They should not appear in prose where the real name is available. Replace every label with its real name wherever it appears outside a table.

**Detached tip blocks.** Are there standalone "Things worth knowing" or "Before you go" sections containing points that could be folded into adjacent content? Tips that map directly onto a preceding section (e.g., a "colour is the first signal" tip sitting after a "Sight" section) belong inside that section — not in a separate block that the reader must connect themselves. Fold them in, then remove the block.

---

### Section-level checks

**Angle delivery.** Is the editorial position visible throughout, or does it fade after the introduction? Does the article actually do what the angle promises?

**Content devices.** Find each device section from the outline. Is it executed fully and specifically — vivid, surprising, real? If it feels phoned in, fix it.

**Quotes.** Every quote must earn its place. A quote earns its place by doing something the surrounding prose cannot: delivering a specific piece of information, adding a voice that changes the register, or providing attribution authority. If a quote restates what the paragraph already says, or says something vague enough that paraphrasing it would lose nothing, remove it. Do not keep a quote simply because it came from a credible source.

**Logic gaps.** Does each section follow logically from the one before? Are there claims a sceptical reader would push back on that the article doesn't address?

**Data and pricing consistency.** If a specific number — price, date, statistic — appears in a footnote, caveat, or asterisk note, it must also appear in the main body where it is first relevant. A reader who reaches a footnote referencing a price they have not yet seen will be confused. Move the number into the body, then remove the footnote. If the number cannot be placed in the body, remove both.

**Voice DNA match** (if `voice-dna.md` exists). Does the opening pattern, teaching style, and signature vocabulary match what was observed in real posts?

---

### Conclusion and CTA

**Angle consolidation.** Does the conclusion consolidate the article's editorial position, or does it just summarise sections?

**Commercial tone.** Does the CTA actively sell the brand's product or service? Read it as a first-time visitor who knows nothing about the brand. Does it make a reader want to act, or does it unintentionally introduce doubt? A CTA that ranks products against each other ("X matters more than Y"), leads with caveats, or closes on a limiting instruction ("just start with X") is not a sales close — it is an editorial instruction. Rewrite it to make the full product or service range appealing.

**Specificity.** Is the CTA specific and genuinely useful? A vague CTA ("visit our website to learn more") does not justify the reader's time. The CTA should name a specific product, offer, or next step.

**Product card placeholders.** If the article is for a site that uses product cards, add `[Product card: description]` placeholders at the appropriate points in the Bring It Home or equivalent section. These are publishing instructions, not content. They will be replaced with actual cards before the post goes live.

---

### PAA coverage

Are all PAA questions from `keyword.json` answered clearly and findably? A PAA answer should be a direct sentence that could stand alone as a featured snippet response, followed by elaboration if needed.

---

## Step 4 — Fix, then write revision notes

Make direct edits to `draft.md` for anything you can fix.

**If returning from audit flags:** work through each `<!-- AUDIT FLAG: ... -->` comment. For em dash flags specifically, apply the rewriting patterns in `BRAND_DIR/de-ai-guidelines.md` — do not substitute a punctuation patch.

**Scope discipline on audit-return passes:** fix only the flagged lines. If you notice other issues while working, note them in `revision-notes.md` — do not fix them silently.

After editing, write `revision-notes.md` to EDITORIAL_DIR:

```markdown
# Revision Notes — [keyword]
*[today's date]*

## Cold read impressions
[Honest first-read reactions — before any checklist]

## Human edits found
- [Edit description] — [consistent / flagged — see inline comment]

## Editorial flags
[None — or list by section: issue and what was done]

## Content device assessment
[One line per device: executed well / fixed / flagged]

## Changes made
1. [What changed and why]

## For human attention
[Items that need brand-specific input before publishing — or "None"]

## Ready to publish?
Yes / Not yet — [if not, what specifically needs addressing]
```

Update `work-log.md`:

```
---
step: revision | [timestamp] | status: complete
---
[What changed and why. Writer notes actioned. Anything passed to human in revision-notes.md.]
```

---

## Step 5 — Strip sources before finalising

The sources section in `draft.md` is a working reference for the revision and audit steps. It must not appear in the published article.

Before marking the draft final, remove the `*Sources used:*` block and everything below it. Sources remain accessible in `DATA_DIR/sources/` and in `writer-notes.md` for any future verification.

If the draft is clean, update the frontmatter:

```markdown
---
title: [headline]
keyword: [keyword]
date: [original date]
revised: [today's date YYYY-MM-DD]
status: final
---
```

---

## Human gate

> **Revision complete.**
>
> Human edits found: [N]
> Editorial flags: [N — or "none"]
> Status: [Ready to publish / Needs attention — see revision-notes.md]
>
> Press Enter to build the final output.
