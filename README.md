# SEO Content System

AI-assisted SEO content production pipeline. Chains SERP research, Claude Code skill sessions, and utility scripts into a repeatable article workflow.

---

## Project structure

```
seo-content-system/
  pyproject.toml           ← dependencies, CLI entry points, lint/test config

  src/seo_system/          ← installed Python package
    config.py              ← env loading, path constants, pipeline constants
    workspace.py           ← article log I/O, step state tracking
    runner.py              ← subprocess wrappers (scripts + Claude Code)
    gates.py               ← interactive human-gate prompts
    steps.py               ← RunContext + all 7 step functions
    cli/
      workflow.py          ← main() for run_workflow
      onboard.py           ← main() for onboard_client
    onboard/
      prompts.py           ← terminal I/O helpers (ask, confirm, header)
      writers.py           ← brand/content file generators
      claude.py            ← Claude-generated brand voice + audience files
      qa.py                ← guided Q&A flow

  skills/                  ← Claude Code skill prompts (one per pipeline step)
    keyword-and-angle.md
    headline-and-outline.md
    research-authority.md
    writing.md
    polish.md
    output.md
    content-devices.md     ← shared content device library
    content-standards.md   ← universal structural standards

  scripts/                 ← standalone utility scripts
    fetch_serp.py
    fetch_url.py
    scan_banned_phrases.py
    analyse_rhythm.py
    generate_schema.py
    validate_meta.py
    build_output.py

  brand/                   ← repo-level brand templates (copied to client on onboard)
    de-ai-guidelines.md
    brand-voice-card.md

  tests/
    test_config.py
    test_workspace.py
```

Client data lives **outside** the repo, under a path set by `CONTENT_BASE`:

```
$CONTENT_BASE/
  monx/
    profile.md
    brand/
      brand-voice-card.md
      audience-profiles.md
      competitors.md
      glossary.md
      cta-library.md
      de-ai-guidelines.md
      page-index.json
    content/
      _index.md
      us-uk-tax-treaty-dividends/
        editorial/  ← draft.md, outline.md, work-log.md, writer-notes.md
        data/       ← log.json, serp-urls.json, sources/, meta.json, schema.json
        publish/    ← final.html, publish-checklist.md
```

---

## Setup

There are no `run_workflow.py` / `onboard_client.py` scripts anymore — installing the
package puts `run-workflow` and `onboard-client` commands on your PATH.

```bash
# 1. Install the package (creates the CLI commands below)
pip install -e .

# 2. Set required env vars in .env (repo root)
CONTENT_BASE=/path/to/your/client/data
AHREFS_API_KEY=your_key_here

# 3. Confirm the Claude Code CLI is installed and logged in —
#    every skill-based step (angle, headline-outline, writing, polish)
#    shells out to `claude --print`
which claude
```

**Run these commands in a real terminal window** (Terminal.app, iTerm, etc.), not
through a tool that can't provide interactive stdin. The `keyword` step and every
`[GATE]` step below call Python's `input()` to prompt you — if stdin isn't a TTY
you'll get `EOFError: EOF when reading a line` instead of a prompt.

---

## Onboard a new client

```bash
onboard-client --client monx
```

Creates the full client folder structure and generates brand voice + audience profile files via Claude. Prompts you through a Q&A session, so run it interactively.

---

## Run the article workflow

```bash
# Full run — will pause at each [GATE] step below for your input
run-workflow --client monx --article "us expat tax" --step all

# Single step
run-workflow --client monx --article "us expat tax" --step keyword

# Resume from a step (skips earlier completed steps)
run-workflow --client monx --article "us expat tax" --from headline-outline

# Force re-run a step that's already marked complete
run-workflow --client monx --article "us expat tax" --step polish --force
```

The article name (`--article`) can be plain English — it's slugified automatically
(e.g. `"us expat tax"` → `us-expat-tax`).

---

## Pipeline steps

| Step | What it does |
|---|---|
| `keyword` | Prompts for the target keyword, fetches SERP data + top-10 pages via Ahrefs |
| `angle` | **[GATE]** Claude proposes an angle; you review/override |
| `headline-outline` | **[GATE]** Claude generates headline options + outline |
| `research` | **[GATE]** Claude gathers authoritative sources into `data/sources/` |
| `writing` | Claude writes the full draft (hard-fails on HIGH severity banned phrases) |
| `polish` | **[GATE]** Scans banned phrases + rhythm, then Claude does an editorial pass |
| `output` | Generates meta, schema.json, final.html, and the publish checklist |

---

## Tests

```bash
pytest tests/
```

19 tests covering `normalise_slug`, log I/O, step state tracking, index generation, and article file initialisation. No external dependencies — runs in under 0.1s.
