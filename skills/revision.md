# Skill: Revision
*Step 8 of the SEO Content System*

---

## Before you begin revision: read these two files

**1. Read work-log.md in full.**
Scan every entry from `init` through `audit`. You are looking for:
- Steps that ran partial or with errors — what data might be degraded or missing
- Workarounds that were used — decisions that may need to be revisited
- Human gate decisions — what the editor approved or changed and why

**2. Read writer-notes.md in full.**
These are observations from the writing and audit sessions. Some will be directly actionable (a flagged section to tighten, a claim to verify). Some will be context (why a structural decision was made). Some will be signals for the human editor rather than for you.

Act on notes that fall within the revision skill's remit. Pass the rest to the human via revision-notes.md.

**After revision, write one entry to work-log.md:**

```
---
step: revision | [timestamp] | status: complete
---
[What changed and why. Sections tightened, claims adjusted, structural moves made. Any writer notes that were actioned. Any writer notes passed to human in revision-notes.md.]
```

Do not write to writer-notes.md during revision. That file's writing phase is closed.

---

## Your job

You are a collaborative editor. The human has just reviewed the audited draft and may have made their own edits directly to `draft.md`. Your job is to:

1. Check that any human edits are consistent with the angle, brand voice, and article structure
2. Do a final editorial pass for anything the audit step didn't catch — logic gaps, weak sections, claims that need support
3. Ensure the article is genuinely ready to publish, not just technically compliant

This is a different job from the audit step. The audit fixed mechanical issues. This step is about editorial quality. You are allowed to suggest improvements, flag weak sections, and surface anything the human should consider — but you do not make substantive changes without flagging them first.

---

## Inputs — read all of these

All files are in the WORKSPACE path provided at the top of this prompt.

| File | What it contains |
|---|---|
| `draft.md` | The audited draft — may include human edits since the audit step |
| `outline.md` | The approved outline — check the final draft still honours the structure and intent |
| `angle.md` | The approved angle — the editorial test everything is measured against |
| `brand/brand-voice-card.md` | Brand voice — final check that voice is consistent throughout |
| `sources/index.json` | Research index — verify all claims in the draft are supported |
| `keyword.json` | Target keyword and PAA questions — final SEO check |

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

Read the full draft as the target reader described in `angle.md`. Ask:

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

**Is the conclusion earning its place?**
- Does it consolidate the angle, or just summarise the sections?
- Is the CTA specific and genuinely useful to the target reader?

**PAA questions:**
- Are all PAA questions from `keyword.json` answered clearly?
- Is the answer to each one findable quickly — a direct sentence, not buried in a paragraph?

---

## Step 3 — Write your revision notes

Do not edit the draft directly in this step unless fixing something minor and mechanical (a broken sentence, a missing word, an obvious error).

Instead, write `revision-notes.md` to the workspace:

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

## Ready to publish?
Yes / Not yet — [if not, list what needs addressing before pressing Enter]
```

---

## Step 4 — If changes are needed

If your revision notes identify issues the human needs to address, end your session with the notes visible and wait. Do not proceed.

If the draft is clean and ready, make any minor mechanical fixes directly in `draft.md`, update the frontmatter status to `final`, and end your session.

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
> Status: [Ready to publish / Needs attention]
>
> Review `revision-notes.md` for any flags that need your decision.
> When you're satisfied, press Enter to build the final output.
