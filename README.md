# SEO Content System

AI-assisted SEO content production pipeline. Chains SERP research, Claude Code skill sessions, and utility scripts into a repeatable article workflow.

---

## Project structure

```
seo-content-system/
  run_workflow.py          ← CLI launcher (python3 run_workflow.py ...)
  onboard_client.py        ← CLI launcher (python3 onboard_client.py ...)
  pyproject.toml           ← dependencies, CLI entry points, lint/test config

  src/seo_system/          ← installed Python package
    config.py              ← env loading, path constants, pipeline constants
    workspace.py           ← article log I/O, step state tracking
    runner.py              ← subprocess wrappers (scripts + Claude Code)
    gates.py               ← interactive human-gate prompts
    steps.py               ← RunContext + all 9 step functions
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
    audit.md
    revision.md
    output.md
    content-devices.md     ← shared content device library
    content-standards.md   ← universal structural standards

  scripts/                 ← standalone utility scripts
    fetch_serp.py
    fetch_url.py
    fetch_sitemap.py
    scan_banned_phrases.py
    analyse_rhythm.py
    match_internal_links.py
    build_page_index.py
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

```bash
# 1. Install dependencies (creates CLI commands)
pip install -e .

# 2. Set required env vars in .env
CONTENT_BASE=/path/to/your/client/data
AHREFS_API_KEY=your_key_here

# 3. Confirm Claude Code CLI is available
which claude
```

---

## Onboard a new client

```bash
python3 onboard_client.py --client monx
# or
onboard-client --client monx
```

Creates the full client folder structure and generates brand voice + audience profile files via Claude.

---

## Run the article workflow

```bash
# Full run
python3 run_workflow.py --client monx --article "us expat tax" --step all

# Single step
python3 run_workflow.py --client monx --article "us expat tax" --step keyword

# Resume from a step
python3 run_workflow.py --client monx --article "us expat tax" --from headline-outline

# Force re-run a completed step
python3 run_workflow.py --client monx --article "us expat tax" --step audit --force
```

Installed CLI commands work identically:

```bash
run-workflow --client monx --article "us expat tax" --step all
```

---

## Pipeline steps

| Step | What it does |
|---|---|
| `keyword` | Fetches SERP data and top-10 pages via Ahrefs + fetch_url |
| `angle` | **[GATE]** Claude proposes angle; you review/override |
| `headline-outline` | **[GATE]** Fetches sitemap; Claude generates headline options |
| `research` | **[GATE]** Claude gathers authoritative sources |
| `writing` | Claude writes the full draft |
| `audit` | Scans banned phrases + rhythm; Claude self-audits |
| `revision` | **[GATE]** Claude applies final revisions |
| `links` | Matches internal link candidates from page index |
| `output` | Generates meta, schema, and final.html |

---

## Tests

```bash
pytest tests/
```

19 tests covering `normalise_slug`, log I/O, step state tracking, index generation, and article file initialisation. No external dependencies — runs in under 0.1s.
