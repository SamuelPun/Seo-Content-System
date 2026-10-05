# Running the pipeline

Drive every step through the CLI, never by invoking `skills/*.md` files
inline in this conversation:

```
run-workflow --client <client> --article "<article>" --step <step> --keyword "<keyword>"
```

Invoking skills inline drags the whole prior conversation into every
subsequent role's context and multiplies token cost with each one. The CLI
avoids that — each role (`skills/angle-writer-draft.md`, etc.) runs as its
own isolated `claude --print` subprocess, seeded only with the files it
needs.

- Pass `--keyword` once, the first time you touch a new article. It's cached
  in `data/log.json` from then on — never ask for it again.
- Before starting `angle`, run the **Brainstorm** phase below in chat — don't
  invoke `--step angle` until it's produced a seed. Before `headline-outline`,
  just ask in chat for a headline idea (they can say "none") and pass it as
  `--seed "<idea>"`. The interactive prompt never reaches the user when the
  CLI runs headlessly, so `--seed` is the only way either question lands.
- `angle` and `headline-outline` are multi-role stages checkpointed role by
  role in `data/log.json`. If a run stops partway (usage limit, crash,
  anything), just re-run the exact same command — it resumes at the next
  unfinished role automatically. Don't pass `--force` unless you actually
  want to restart the whole stage from scratch.
- If the Editor still hasn't approved after the one automatic revision pass,
  the CLI stops with status `needs_human` — it will never mark a rejected
  stage `complete` and march on. Read `editor-verdict.json` and the draft,
  then either fix the file by hand and re-run (it'll pick up from there once
  `approved: true`), or re-run with `--force` to redo the stage from scratch.

## Brainstorm — chat-only, right after `keyword`, before `angle`

The SEO Manager's SERP-gap finding is a useful sanity check, not a starting
point — left unattended it fixates on "what competitors are missing" and
every angle ends up sounding the same. So the angle gets picked with the user
*first*, in chat, before any pipeline subprocess touches it:

1. Pitch a handful of concepts — one sentence or short paragraph each, high
   level, no SERP research yet. Draw from varied lenses so they actually feel
   different from each other, not five flavors of the same gap:
   narrative/personal, contrarian/myth-busting, format innovation (comparison,
   decision-tree, ranked tiers, before/after), emotional/psychological,
   practical/how-to, timely/seasonal hook, depth-level swap (beginner vs.
   expert). Gap-hunting from the SERP is one option in the mix, never the
   default.
2. Go back and forth with the user until you agree on one simple, high-level
   concept — a sentence, not a fleshed-out angle.
3. That agreed concept is the seed: run `--step angle --seed "<concept>"`.
   Inside the stage, the SEO Manager checks it against the SERP/table-stakes/
   PAA and the Writer fleshes it out in detail — they validate and detail the
   concept, they don't replace it.

No file writes, no `run-workflow` call, during step 1–2 — it's a plain
conversation.

## Review points — exactly three, in chat

After each of these steps completes, read the output file yourself and show
the key content directly in your reply — don't tell the user to go open the
file. Wait for one round of feedback, then continue.

| Step | What to show |
|---|---|
| `angle` | target reader + angle statement — the SERP-validated, detailed version of the concept already agreed in the Brainstorm phase (`editorial/angle.md`) |
| `headline-outline` | headline options + outline shape (`editorial/headline.md`, `editorial/outline.md`) |
| `writing` | a summary/excerpt of the draft, not the full text (`editorial/draft.md`) |

`keyword`, `research`, `polish`, and `output` run with no stop — report a
one-line status and move on.

## Stopping before a usage-limit cutoff

There's no API to check how much of the usage limit is left. As a
best-effort heuristic: if anything in this session has already failed or
warned about a rate/usage limit, don't start another heavy role (SEO
research, writer-draft roles — the biggest sub-steps in `angle`/
`headline-outline`). Stop and tell the user plainly: "stopped after N of M
roles in `<step>` — re-run the same command whenever you're ready, it'll
resume at `<next role>`." That's a real resume, not a restart, so stopping
early costs nothing.
