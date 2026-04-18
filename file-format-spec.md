# work-log.md and writer-notes.md — Format Specification
*Reference for all skill files and run_workflow.py*

---

## work-log.md

### Purpose
A complete technical record of what actually happened during each step. Exists so any session — human or Claude Code — can pick up an article mid-run with full context. Not a summary of what should happen. A record of what did.

### Location
`workspace/article/[slug]/work-log.md`

### Who writes it
Every skill step writes at least one entry. The orchestrator writes entries on step start, step completion, and any error or skip.

### When to write
- Orchestrator: on step start, on step end (with status)
- Skills: whenever something notable happens — missing data, a workaround, a decision, an unexpected result, an error

If a step ran cleanly with no surprises, one entry from the orchestrator is sufficient. Skills only add entries when there is something worth recording.

### Entry format

```
---
step: [step-name] | [YYYY-MM-DD HH:MM] | status: [complete | partial | skipped | error]
---
[Plain prose. 1–5 sentences. What happened, what was missing, what decision was made, what a future session needs to know. No bullet lists required.]
```

**Status values:**
- `complete` — step ran as expected, all outputs produced
- `partial` — step ran but some data was missing or degraded (specify what)
- `skipped` — step did not run (specify why — e.g. `--from` flag, already complete)
- `error` — step failed (specify what failed and what was done about it)

### Rules
1. Append only. Never edit or delete a previous entry.
2. One entry per notable event, not one entry per sentence.
3. Write for a future reader who has no memory of this run. Don't assume they know what went wrong — say it plainly.
4. If a workaround was used, record both the problem and the workaround.
5. If a human decision was made at a gate, record what the decision was and why (if known).

### Example entries

```
---
step: keyword | 2025-01-15 09:12 | status: complete
---
Ahrefs SERP returned 10 results. 2 null URLs filtered (SERP features). 1 duplicate domain removed (sitelinks). keyword.json and serp-urls.json written. PAA: 6 questions extracted.
```

```
---
step: research | 2025-01-15 11:47 | status: partial
---
Fetched 8 of 10 SERP pages. Pages 4 and 9 returned 403 — skipped. sources/index.json written with 8 entries. Human gate: editor to review before writing begins.
```

```
---
step: research | 2025-01-15 12:03 | status: complete
---
Human gate cleared. Editor removed 2 sources (thin content, no original data). 6 sources approved. Writing step unblocked.
```

```
---
step: writing | 2025-01-15 13:22 | status: error
---
draft.md not written. Claude Code session timed out at section 3. Partial output saved to draft-partial.md manually. Resuming with --step writing --force.
```

---

## writer-notes.md

### Purpose
A passive capture file for real-time observations during writing and audit. Exists in two timeframes: immediately (revision skill reads it before the final pass) and long-term (patterns across articles reveal what to improve in the skills).

### Location
`workspace/article/[slug]/writer-notes.md`

### Who writes it
- Writing skill — observations during drafting
- Audit skill — observations during audit
- Human editor — during revision gate (optional but encouraged)

### When to write
Only when a genuine instinct fires. Not on a schedule, not to prove the step ran, not to fill space. If nothing notable comes up during a writing session, no entry is written.

Ask: "Would a thoughtful editor want to know this before doing the final pass?" If yes, write it. If not, don't.

### Entry format

```
[HH:MM] [Observation in plain language. One to three sentences. Written as a note to a future editor, not to the system.]
```

No step header. No status field. Just a timestamp and the thought.

### Rules
1. Append only.
2. Write for the revision editor, not for the log. Phrase it as: "here's something you should know before you touch this."
3. Short and honest. Unpolished is fine. This is not a deliverable — it is a thinking tool.
4. Do not use writer-notes to flag things that belong in audit-flags.json (banned phrases, rhythm violations). Those are handled by the audit scripts. Writer notes are for qualitative observations the scripts can't catch.
5. Human editor may append during the revision gate. Mark with `[editor]` prefix if desired for later analysis.

### What belongs here (examples)
- A section that is structurally sound but feels thin — the device ran out before the substance
- An intro that is working unusually hard against the SERP pattern — worth protecting
- A claim that is technically sourced but feels overstated — flag for the editor to judge
- A device that landed well — worth noting for system improvement
- A structural decision that went against the outline and why
- Anything the editor should read with extra attention

### What does not belong here
- Banned phrase flags (→ audit-flags.json)
- Rhythm violations (→ rhythm-analysis.json)
- Internal link candidates (→ internal-link-candidates.json)
- Meta title / description issues (→ meta.json)
- Anything the scripts already capture

### Example entries

```
[13:44] The intro avoids the definition-first pattern all 10 SERP pages use. The angle lands by sentence 2. Worth protecting — don't let revision smooth it into something safer.

[14:02] Section 3 (tax residency rules) ran long. Content is solid but the device overstays its welcome by about 200 words. Suggest tightening the last two paragraphs or merging with section 4.

[14:31] The CTA is functional but generic. The brief didn't give us a specific offer to anchor it to — this is a brand voice card gap, not a writing gap. Flag for human after revision gate.
```

```
[15:18] [editor] Approved draft with one cut — removed the third paragraph of section 2 (restated what section 1 already said). Everything else clean.
```

---

## Initialisation

Both files are created by `run_workflow.py` when a new article workspace is set up.

`work-log.md` gets a single initialisation entry:
```
---
step: init | [timestamp] | status: complete
---
Workspace created for [slug]. work-log.md and writer-notes.md initialised.
```

`writer-notes.md` is created empty (header only). No entry is written until a skill has something genuine to record.
