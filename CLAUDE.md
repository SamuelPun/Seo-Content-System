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
- `angle` and `headline-outline` are multi-role stages checkpointed role by
  role in `data/log.json`. If a run stops partway (usage limit, crash,
  anything), just re-run the exact same command — it resumes at the next
  unfinished role automatically. Don't pass `--force` unless you actually
  want to restart the whole stage from scratch.

## Review points — exactly three, in chat

After each of these steps completes, read the output file yourself and show
the key content directly in your reply — don't tell the user to go open the
file. Wait for one round of feedback, then continue.

| Step | What to show |
|---|---|
| `angle` | target reader + angle statement (`editorial/angle.md`) |
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
