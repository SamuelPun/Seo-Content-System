# Design: Preventing cross-section repetition and disconnected sections

*2026-08-01*

## Problem

Articles produced by this pipeline sometimes repeat the same point across multiple
sections (restated in different words, not verbatim — a keyword/n-gram scan across
real drafts found no verbatim repeats, only false positives like repeated source
citation URLs), and sections read as disconnected islands rather than one flowing
argument.

## Root cause

This is the same architecture bug already found and fixed once this session in
`skills/article-to-html.md`: checks exist, but they are reactive (run after the
decision is already made) and too weak to catch the real failure.

Specifically, in `skills/headline-and-outline.md` and `skills/polish.md`:

1. **The outline's "Redundancy check"** (`headline-and-outline.md` Step 5) only
   fires when a fact appears in "more than two sections" — a fact repeated in
   exactly two sections passes uncaught. It also runs against the outline's
   planned Key Points bullets, not actual prose, and never re-runs after the
   draft is written.
2. **The outline template** specifies each section in total isolation (Purpose /
   Serves / Key points / PAA / Authority / Content device) — no field records
   what a section assumes was already covered, and nothing records whether the
   order of sections actually builds understanding incrementally.
3. **`writing.md`** gives the writer no instruction to check prior sections
   before drafting the next one, and its de-AI rules only ban bad transitions
   ("throat-clearing") without ever giving positive guidance for how a section
   should connect to what came before.
4. **`polish.md`**'s only relevant check — "Logic gaps: does each section follow
   logically from the one before?" — is a single cold-read judgment at the very
   end of the whole pipeline (Step 7), after the full draft already exists. It
   has no repetition check at all, verbatim or semantic.

## Design

Three changes, one per pipeline stage, each doing the part of the job that
actually belongs at that stage — not one stage trying to catch everything late.

### 1. Outline stage (`skills/headline-and-outline.md`, Step 5)

**New field per section:** `New in this section` — the one fact, claim, or
mechanism this section is exclusively responsible for explaining in full. This
replaces the current "Key points" bullets as the source of truth for what a
section owns.

*(A "Builds on" field, pre-scripting each section's transition into the prior
one, was considered and dropped — real writers don't script a transition before
the prose exists; they discover it while writing. That responsibility moves to
the writing stage instead, section 2 below.)*

**Replace the old Redundancy check with a Sequence & Ownership check,** run once
against the section skeleton (`Purpose` + `New in this section`, read in section
order) immediately after all sections have that field filled in — before any
prose is written:

1. **No two sections claim the same fact.** Every fact named in a "New in this
   section" field appears in exactly one section. If a second section needs the
   same fact, it must reference the owning section, not claim the fact as its
   own.
2. **No section depends on something not yet established.** If section N's
   content requires understanding concept X, X must already be an earlier
   section's "New in this section" — never a later one's.

This check operates purely on the skeleton, so it costs nothing to run before a
single sentence is drafted, and catches structural problems (duplicate ownership,
out-of-order dependencies) while they are still free to fix by reordering or
consolidating sections — not after 2,000 words are already sunk into the wrong
structure.

### 2. Writing stage (`skills/writing.md`)

**Discovered transitions, not pre-scripted ones.** Before opening each section
(after the first), the writer rereads what has been written so far in
`draft.md` and opens the new section by using the most relevant established
fact as a load-bearing premise — not by announcing the transition. This is a
real distinction, not a stylistic nuance: the wrong version of this *is* the
already-banned throat-clearing pattern.

- Wrong (announces the transition — banned): *"Now that we've covered the 30%
  default, let's look at the two routes to zero."*
- Right (uses the prior fact as a premise, doesn't restate or announce it):
  *"Two separate mechanisms can take that 30% to zero — a tax treaty, and a
  domestic exemption that doesn't need one."*

**Ownership boundary.** A section may only fully explain the fact assigned to it
in the outline's "New in this section" field. It may reference a fact owned by
another section in short form, never re-explain it from scratch.

**Quality Check addition** (the existing list at the end of `writing.md`): add
*"Each section's content stays within its outline-assigned 'New in this
section' scope — no fact fully explained in more than one section."*

### 3. Polish stage (`skills/polish.md`)

**Narrow "Logic gaps" from a vague cold-read guess to a scoped verification.**
The heavy structural work (does the order make sense, does anything duplicate
ownership) already happened at the outline stage, before writing began. By
polish time, the only open question is whether the *actual prose* — including
any point where the writer deviated from the outline, which `writing.md`
explicitly permits and logs in `writer-notes.md` — faithfully executed the
sequence the outline already validated. Reword the check accordingly:

> **Logic gaps:** does the draft's actual section order and content match the
> sequence validated in `outline.md`? For any point where `writer-notes.md`
> logs a deviation from the outline, check specifically whether that deviation
> reintroduced a duplicated fact or an out-of-order dependency the outline check
> had already ruled out.

This keeps a genuine late-stage check (prose only exists by this point) but
scopes it to verifying execution against an already-validated plan, rather than
re-deriving structural soundness from scratch via a cold read.

## What gets removed

- The old ">more than two sections" Redundancy check in `headline-and-outline.md`
  Step 5 — fully replaced by the Sequence & Ownership check.
- The current unscoped wording of "Logic gaps" in `polish.md` — replaced by the
  narrower execution-verification wording above.

## Files touched

- `skills/headline-and-outline.md` — Step 5 outline template (new field, new
  check replacing the old redundancy check)
- `skills/writing.md` — new reread-before-writing instruction, new ownership
  boundary rule, one Quality Check line added
- `skills/polish.md` — narrowed "Logic gaps" check wording

## Verification

- Re-read all three rewritten skill files end to end and confirm the old
  Redundancy check and the old "Logic gaps" wording are fully replaced, not
  left duplicated alongside the new versions.
- Walk through the outline for a real past article (e.g.
  `u-s-withholding-tax-on-interest`) against the new Sequence & Ownership check
  by hand: would it have caught anything the old ">2 sections" threshold would
  have missed?
- Confirm `writing.md`'s new transition instruction does not conflict with the
  existing zero-throat-clearing de-AI rule — the design must read as a single
  coherent instruction, not two rules pulling in different directions.
