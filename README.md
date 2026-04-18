# SEO Content System
*Session 3 complete*

## Structure

```
seo-content-system/
  run_workflow.py              ← orchestrator
  README.md

  skills/
    keyword-and-angle.md      ← steps 1–2
    headline-and-outline.md   ← steps 3–4
    research-authority.md     ← step 5
    writing.md                ← step 6
    audit.md                  ← step 7
    revision.md               ← step 8
    output.md                 ← steps 9–10
    content-devices.md        ← 22 original content devices (shared library)
    content-standards.md      ← universal structural standards (shared library)

  brand/                      ← build once, used by all articles
    brand-voice-card.md       ← PLACEHOLDER — run brand-voice-discovery skill
    de-ai-guidelines.md       ← PLACEHOLDER — move de-aiwriting.md here

  scripts/                    ← all 9 utility scripts (built in session 2)
    fetch_url.py
    fetch_serp.py
    fetch_sitemap.py
    scan_banned_phrases.py
    analyse_rhythm.py
    match_internal_links.py
    generate_schema.py
    validate_meta.py
    build_output.py

  workspace/article/[slug]/   ← created per article by run_workflow.py
```

## Before first live run

1. Complete brand voice sessions → save output to brand/brand-voice-card.md
2. Move de-aiwriting.md from repo root → brand/de-ai-guidelines.md
3. Set up VS Code + Claude Code CLI (see handoff doc)
4. Confirm `which claude` works in terminal
5. Run: python3 run_workflow.py --article "your-slug" --step keyword

## Human gates (where workflow pauses for your review)

- angle
- headline
- research
- revision

## Usage

```bash
# Run full workflow
python3 run_workflow.py --article "us-expat-tax" --step all

# Run single step
python3 run_workflow.py --article "us-expat-tax" --step keyword

# Resume from a step
python3 run_workflow.py --article "us-expat-tax" --from outline

# Force re-run a completed step
python3 run_workflow.py --article "us-expat-tax" --step audit --force
```
