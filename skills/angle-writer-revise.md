---
name: angle-writer-revise
description: "Angle stage, revision pass (one loop max) — Writer revises angle.md based on the Editor's verdict and the Reader Advocate's feedback. Only run when the Editor did not approve."
---

# Skill: Angle — Writer revision
*Angle stage — one revision pass, triggered only when the Editor did not approve*

---

## Your job

Revise `angle.md` in place to address the Editor's verdict. This is your one revision pass — there is no second round, so resolve everything in `editor-verdict.json` now. If anything in the notes is ambiguous, make the strongest reasonable judgement call rather than leaving it half-addressed.

If the original angle was built on an EDITOR SEED (an agreed concept from the chat brainstorm — check `meeting-notes.md` for "Writer — angle draft" to confirm), fix the execution problem within that concept — sharpen the insight, cover a missed table-stakes item, address a trust concern. Don't swap to a different gap from `research-brief.md` to sidestep the verdict; that's a silent pivot away from what the human agreed to. If you genuinely believe the concept itself is unworkable, keep the revision minimal and say so plainly in the handoff and `meeting-notes.md` so it's visible at the human review point right after this stage — don't quietly redirect it yourself.

---

## Inputs

| File | What it contains |
|---|---|
| `EDITORIAL_DIR/angle.md` | Your previous draft |
| `EDITORIAL_DIR/editor-verdict.json` | What must change and why |
| `EDITORIAL_DIR/reader-feedback.md` | Reader concerns, for context on the Editor's notes |
| `EDITORIAL_DIR/research-brief.md` | Original research — use only to fill a specific factual/table-stakes hole the Editor flagged, not to swap to a different concept |

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
