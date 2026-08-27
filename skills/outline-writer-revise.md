---
name: outline-writer-revise
description: "Outline stage, revision pass (one loop max) — Writer revises headline.md/outline.md based on the Editor's verdict and the Reader Advocate's feedback. Only run when the Editor did not approve."
---

# Skill: Outline — Writer revision
*Outline stage — one revision pass, triggered only when the Editor did not approve*

---

## Your job

Revise `outline.md` (and `headline.md` if needed) in place to address the Editor's verdict. This is your one revision pass — there is no second round, so resolve everything in `editor-verdict.json` now.

---

## Inputs

| File | What it contains |
|---|---|
| `EDITORIAL_DIR/angle.md` | The approved angle — source of truth |
| `EDITORIAL_DIR/outline.md` | Your previous draft |
| `EDITORIAL_DIR/editor-verdict.json` | What must change and why |
| `EDITORIAL_DIR/reader-feedback.md` | Reader concerns, for context on the Editor's notes |
| `DATA_DIR/keyword.json` | Table stakes and PAA questions, if coverage was the issue |

---

## Revise

Fix exactly what `editor-verdict.json` flagged:
- **Angle-line mismatch:** copy `angle.md`'s `## Our angle` sentence into `outline.md`'s `**Angle:**` field verbatim.
- **Section(s) not tracing to the angle:** either rewrite the section's `Purpose` to genuinely connect to the angle, cut it, or mark it explicitly `(table-stakes only — does not serve the angle)` if it's required coverage that can't be angle-driven.
- **Missing required coverage:** add the missing table-stakes topic or PAA question as a section, reconciled with the angle the same way.
- **Fact-duplication or forward-dependency:** reorder or consolidate sections so each fact is owned by exactly one section and no section depends on a later one.

Don't do a generic pass over the whole outline — fix what was flagged.

---

## Handoff

Append a short entry to `EDITORIAL_DIR/meeting-notes.md`:

```markdown
## Writer — outline revision
[1-2 sentences: what changed in response to the Editor's verdict]
```

End your session with:

> **Headline options and outline ready.**
> Structure type: [Reader-pathway / Topic-ordered, from outline.md]
> This went through one revision round based on Editor feedback — see `meeting-notes.md` for what changed.
>
> Three things to do before pressing Enter:
> 1. Open `headline.md` — write your chosen headline in the "Chosen headline" field.
> 2. Open `outline.md` — copy your chosen headline into the **Chosen headline** field at the top.
> 3. Review the reader pathway map — confirm sections don't repeat the same core fact across pathways.
>
> The writer works from `outline.md` only. Changes made here are the last chance to fix structure before the draft is written.
>
> Press Enter when both files are updated and you're satisfied with the outline.
