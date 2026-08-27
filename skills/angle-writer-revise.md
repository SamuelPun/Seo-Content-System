---
name: angle-writer-revise
description: "Angle stage, revision pass (one loop max) — Writer revises angle.md based on the Editor's verdict and the Reader Advocate's feedback. Only run when the Editor did not approve."
---

# Skill: Angle — Writer revision
*Angle stage — one revision pass, triggered only when the Editor did not approve*

---

## Your job

Revise `angle.md` in place to address the Editor's verdict. This is your one revision pass — there is no second round, so resolve everything in `editor-verdict.json` now. If anything in the notes is ambiguous, make the strongest reasonable judgement call rather than leaving it half-addressed.

---

## Inputs

| File | What it contains |
|---|---|
| `EDITORIAL_DIR/angle.md` | Your previous draft |
| `EDITORIAL_DIR/editor-verdict.json` | What must change and why |
| `EDITORIAL_DIR/reader-feedback.md` | Reader concerns, for context on the Editor's notes |
| `EDITORIAL_DIR/research-brief.md` | Original research, in case the fix requires pulling in a different gap |

---

## Revise

Rewrite `angle.md` in place, keeping the same section structure (The insight / Target reader / Their core problem / What the current top results miss / Our angle / Why this angle wins / What we will do differently / PAA questions to address — see `angle-writer-draft.md` for the full template if needed). Address every point in `editor-verdict.json`'s notes specifically — don't do a generic pass over the whole file.

If the fix changes "Our angle," re-check "The insight" sentence still matches it — a changed angle with a stale insight sentence is worse than the original problem.

---

## Handoff

Append a short entry to `EDITORIAL_DIR/meeting-notes.md`:

```markdown
## Writer — angle revision
[1-2 sentences: what changed in response to the Editor's verdict]
```

End your session with:

> **Angle defined.**
> Target reader: [one sentence]
> Our angle: [one sentence]
>
> This went through one revision round based on Editor feedback — see `meeting-notes.md` for what changed.
> Review `angle.md` in your EDITORIAL_DIR folder. Edit freely, then press Enter to continue to headline and outline.
