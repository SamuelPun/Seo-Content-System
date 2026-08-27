# Design: Multi-role angle & outline process

## Problem

The angle/outline stage (formerly `keyword-and-angle.md` then `headline-and-outline.md`)
was a single Claude Code session per stage, one persona ("You are an SEO strategist").
A holistic review (Fable model agent reading the skill files plus 4 real production
`angle.md`/`outline.md` pairs across different clients) found a real, narrow failure
mode: `monx-uk/how-to-avoid-amazon-dropshipping-taxes-uk` shipped an outline whose
`**Angle:**` line was a different claim than `angle.md`'s actual insight — the outline
punted the real insight (Amazon's "deemed supplier" VAT rule) to an imaginary
"companion article" that was never part of the pipeline, and nothing caught it.

The mechanical hole: the old `headline-and-outline.md` Step 5 mandated that every
table-stakes topic and PAA question **must** appear, unconditionally — independent of
whether it served the angle. The "Sequence & Ownership check" only audited
fact-duplication and section ordering; nothing verified the outline's angle line
against `angle.md`, and nothing checked a section's `Purpose` traced back to the angle.

Brand onboarding files (`audience-profiles.md`, `content-prefs.md`) were confirmed to
already be pulling real weight (angles closely paraphrase specific reader-profile
language) — not part of this fix.

## Design

Replaced the two single-session skills with role-scoped sessions, run sequentially
inside `steps.py::step_angle` / `step_headline_outline`. Each role is a separate
`claude --print` subprocess call via the existing `run_claude_skill` (`runner.py`) —
genuine context separation, not one session role-playing multiple personas. The human
gate still fires once per stage, externally, in `workflow.py` — unchanged.

**Roles:** SEO Manager (SERP/competitive research + primary-source knowledge-gap hunt,
writes `research-brief.md` — deliberately not framed as "here's the angle") → Writer
(creative synthesis) → Reader Advocate (reacts to the draft blind to SERP data, reading
only the draft + `audience-profiles.md`, so it can't just parrot the SEO Manager's
framing) → Editor (the check-and-balance gate: insight test, angle-line verbatim match,
per-section fidelity trace, table-stakes reconciliation).

**Angle stage:** SEO Manager → Writer → Reader Advocate → Editor → [Writer revises
once, if not approved].

**Outline stage:** Writer → Editor (fidelity + `keyword.json` coverage check) → Reader
Advocate (pathway/resonance spot-check) → [Writer revises once, if not approved].

Revision is capped at one round per stage. If the Editor still has concerns after the
single revision, those concerns are logged in `meeting-notes.md` for the human to see
and fix by hand at the existing gate — no open-ended retry loop.

Control flow between roles uses `editorial/editor-verdict.json`
(`{"approved": bool, "notes": "..."}`), read back in Python by
`steps.py::_read_editor_verdict` — same pattern already used by `step_research`
(`data/sources/index.json`) and `_validate_banned_phrases` (`audit-flags.json`).

## Files

- New: `skills/angle-seo-research.md`, `angle-writer-draft.md`, `angle-reader-check.md`,
  `angle-editor-review.md`, `angle-writer-revise.md`, `outline-writer-draft.md`,
  `outline-editor-review.md`, `outline-reader-check.md`, `outline-writer-revise.md`.
- Removed: `skills/keyword-and-angle.md`, `skills/headline-and-outline.md` (content
  redistributed, not reinvented — the insight test, headline-type rules,
  content-devices step, and Sequence & Ownership check all carried over).
- Final output paths unchanged (`angle.md`, `headline.md`, `outline.md`), so
  `research-authority.md`, `writing.md`, `polish.md`, `output.md` need no changes.
- `steps.py`: `step_angle`/`step_headline_outline` now run a sequence of
  `run_claude_skill()` calls instead of one, with `_read_editor_verdict` branching to
  the conditional revise skill. `workflow.py`, `gates.py`, `config.py` unchanged.

## Cost tradeoff

~2 Claude sessions per article at this stage becomes ~7–9 (4–5 for angle, 3–4 for
outline). Accepted as worthwhile given this is the highest-leverage stage in the
pipeline (operator decision, 2026-08-07).

## Known follow-up (not part of this change)

`gates.py::_parse_angle` looks for literal `target_reader:`/`angle:` frontmatter lines
in `angle.md`, but the actual template uses `## Target reader`/`## Our angle` markdown
headers — the regex never matches, so the ANGLE REVIEW gate prints nothing under
"Target reader"/"Our angle". Pre-existing before this change; left as-is since fixing
it wasn't in scope.
