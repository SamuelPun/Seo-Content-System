---
name: revision
description: "Step 7 — editorial cold read and quality pass on the draft. Fix-not-flag mandate. Runs before audit."
---

# Skill: Revision
*Step 7 of the SEO Content System — runs before the audit step*

---

## Order note

Revision runs *before* the audit step. The audit fixes mechanical issues (banned phrases, rhythm, structural standards) in a draft that has already been editorially reviewed. Your job is editorial quality — not language cleanup. Do not conflate the two. If you find a banned phrase or rhythm issue while editing, note it in `work-log.md` for the audit to handle. Do not fix mechanical issues yourself in this step.

---

## Before you begin revision: read these two files

**1. Read `EDITORIAL_DIR/work-log.md` in full.**
Scan every entry from `init` through `writing`. You are looking for:
- Steps that ran partial or with errors — what data might be degraded or missing
- Workarounds that were used — decisions that may need to be revisited
- Human gate decisions — what the editor approved or changed and why

**2. Read `EDITORIAL_DIR/writer-notes.md` in full.**
These are observations from the writing and audit sessions. Some will be directly actionable (a flagged section to tighten, a claim to verify). Some will be context (why a structural decision was made). Some will be signals for the human editor rather than for you.

Act on notes that fall within the revision skill's remit. Pass the rest to the human via revision-notes.md.

**After revision, write one entry to `EDITORIAL_DIR/work-log.md`:**

```
---
step: revision | [timestamp] | status: complete
---
[What changed and why. Sections tightened, claims adjusted, structural moves made. Any writer notes that were actioned. Any writer notes passed to human in revision-notes.md.]
```

Do not write to writer-notes.md during revision. That file's writing phase is closed.

---

## Your job

You are an active editor. The human has reviewed the draft and may have made their own edits directly to `draft.md`. Your job is to:

1. Check that any human edits are consistent with the angle, brand voice, and article structure
2. Do a full editorial pass — logic gaps, weak sections, thin device execution, buried insights, conclusions that don't land
3. Fix what you can directly. Ensure the article is genuinely ready to publish, not just technically compliant

**Fix, don't just flag.** Document every substantive change in `work-log.md` with one sentence explaining why. Only escalate to the human via `revision-notes.md` when:
- Fixing requires information only the brand has: a real case, a specific stat, experience you cannot fabricate
- You would be reversing a claim the human deliberately made

Don't flag things you can fix. Flags are for genuine blockers, not abdication.

---

## Inputs — read all of these

Editorial files are in EDITORIAL_DIR. Data files are in DATA_DIR. Brand files are in BRAND_DIR.

| File | What it contains |
|---|---|
| `EDITORIAL_DIR/draft.md` | The audited draft — may include human edits since the audit step |
| `EDITORIAL_DIR/outline.md` | The approved outline — check the final draft still honours the structure and intent |
| `EDITORIAL_DIR/angle.md` | The approved angle — the editorial test everything is measured against |
| `BRAND_DIR/brand-voice-card.md` | Brand voice — final check that voice is consistent throughout |
| `BRAND_DIR/voice-dna.md` | Observed voice patterns from real posts — check opening, rhythm, and teaching style match (read if it exists) |
| `BRAND_DIR/audience-profiles.md` | Reader segments with trust signals and bounce triggers — use in Step 2 reader filter check (read if it exists) |
| `DATA_DIR/sources/index.json` | Research index — verify all claims in the draft are supported |
| `DATA_DIR/keyword.json` | Target keyword and PAA questions — final SEO check |

---

## Step 1 — Identify any human edits

Read `draft.md` and note anything that looks like a recent human edit — sections that differ from the outline structure, new content added, passages rewritten in a different register.

For each human edit, check:
- Is it consistent with the angle?
- Does it stay on-voice with `brand-voice-card.md`?
- Does it introduce any unsupported claims (i.e. no source in `sources/`)?
- Does it break the flow or logic of the surrounding content?

If an edit has a problem, flag it inline with: `<!-- REVISION FLAG: [what the issue is] -->`

Do not silently fix human edits. Flag them and let the human decide.

---

## Step 2 — Editorial quality pass

**Cold read first — do this before any checklist.**
Read the article start to finish without looking at the outline or angle. Read it as a first-time reader who knows nothing about how it was built. Note your genuine reactions:
- Did the opening make you want to keep reading, or did it feel like setup?
- Is the insight present and clear by the halfway point?
- Did anything make you want to click away — a vague section, a slow passage, throat-clearing?
- Does it end in the right place, or does it keep going after it's done?

Write your cold read impressions at the top of `revision-notes.md` before running any other check. These are your most honest signal — a structural checklist cannot replace them.

---

**Does it pass the reader filter?**
If `BRAND_DIR/audience-profiles.md` exists, find the profile matching this article's target reader. Then check:
- Does the opening hit their trust signals — does the first paragraph signal the credibility they're looking for?
- Does anything in the first 200 words trigger their bounce conditions? (Generic framing, AI-sounding opener, no signal that this is different)
- Does the article address their specific content frustrations — the thing other content on this topic gets wrong?

**Does it deliver on the angle?**
- Is the editorial position visible throughout, or does it fade after the introduction?
- Does the article actually do what the angle promises — or does it drift into generic coverage?

**Are the content devices working?**
- Find each section marked as a content device in the outline
- Is the device executed fully and well, or is it thin?
- A fiction character walkthrough should feel vivid and specific. A counterintuitive take should feel genuinely surprising. A dialogue should feel real. If a device feels like it was phoned in, flag it.

**Are there logic gaps?**
- Does each section follow logically from the one before it?
- Are there claims that feel unsupported even if no `[SOURCE NEEDED]` tag is present?
- Is there anything a sceptical reader would push back on that the article doesn't address?

**Does the voice match the DNA?**
If `BRAND_DIR/voice-dna.md` exists, check three things:
- Does the opening pattern match what was observed in real posts — or does it feel like a different brand?
- Does the teaching style match — if the brand uses direct assertion and worked examples, is that what's in the draft?
- Are the signature vocabulary and patterns present, or has the draft drifted into generic register?

**Is the conclusion earning its place?**
- Does it consolidate the angle, or just summarise the sections?
- Is the CTA specific and genuinely useful to the target reader?

**Does it produce an action?**
After reading this article, what does the reader *do* differently — not what do they know, but what do they decide, what do they stop doing, what specific step do they take? If the answer is "nothing specific", the conclusion isn't earning its place. Sharpen it until the behavioral outcome is clear.

**PAA questions:**
- Are all PAA questions from `keyword.json` answered clearly?
- Is the answer to each one findable quickly — a direct sentence, not buried in a paragraph?

---

## Step 3 — Fix, then write your revision notes

Make direct edits to `EDITORIAL_DIR/draft.md` for anything you can fix: thin sections, weak conclusions, buried insights, device sections that feel phoned in, arguments that don't follow logically.

**If returning from audit flags**, work through each `<!-- AUDIT FLAG: ... -->` comment in the draft. For em dashes specifically — do not substitute a colon, comma, or parenthesis and call it done. Read the whole sentence and decide what it actually needs:

- **Parenthetical aside** (`X — detail — continues`): Ask whether the aside earns its place. If yes, restructure as a relative clause (`X, which detail, continues`) or pull it out as its own sentence. If no, cut it.
- **Dramatic pause or contrast** (`claim — punchline`): Split into two sentences. Let the second carry the weight on its own.
- **Inline definition** (`term — what it means`): Rephrase as a subordinate clause: `term, which means...`
- **Clarification after a quote** (`"quote" — explanation`): Start a new sentence. `"Quote." The explanation follows.`

The rewritten sentence must read naturally with no punctuation patch. If it still feels awkward, rewrite further.

**Scope discipline on audit-return passes:** Only fix the flagged lines. If you find unflagged issues worth addressing while working through the flags, note them in revision-notes.md under "Additional flags found" — do not fix them silently. If you do fix them, mark the scope as "beyond surgical" in your revision notes — a re-audit will be required.

After editing, write `revision-notes.md` to EDITORIAL_DIR documenting what changed and what needs human input:

```markdown
# Revision Notes — [keyword]
*[today's date]*

## Human edits found
- [Edit description] — [status: consistent / flagged — see inline comment]

## Editorial flags
- [Section name]: [what the issue is and what to consider doing about it]

## Content device assessment
- [Device name] in [section]: [working well / needs strengthening — specific suggestion]

## Logic gaps
- [Description of gap and suggested fix]

## Additional flags found
- [Any unflagged issues noticed during an audit-return pass — do not fix silently]

## Scope
Surgical (flagged lines only) / Beyond surgical (unflagged content changed — re-audit required)

## Ready to publish?
Yes / Not yet — [if not, list what needs addressing before pressing Enter]
```

---

## Step 4 — If changes are needed

If your revision notes identify issues the human needs to address, end your session with the notes visible and wait. Do not proceed.

If the draft is clean and ready, make any minor mechanical fixes directly in `EDITORIAL_DIR/draft.md`, update the frontmatter status to `final`, and end your session.

Update frontmatter:

```markdown
---
title: [headline]
keyword: [keyword]
date: [original date]
revised: [audit date]
finalised: [today's date YYYY-MM-DD]
status: final
---
```

---

## Human gate

End your session with:

> **Revision complete.**
>
> Human edits found: [N]
> Editorial flags: [N — or "none"]
> Device sections: [working well / flagged — see revision-notes.md]
> Scope: [Surgical / Beyond surgical]
> Re-audit needed: [Yes / No]
> Status: [Ready to publish / Needs attention]
>
> Review `EDITORIAL_DIR/revision-notes.md` for any flags that need your decision.
> When you're satisfied, press Enter to build the final output.
