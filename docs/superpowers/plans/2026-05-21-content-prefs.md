# Content Preferences File Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate a `brand/content-prefs.md` file during client onboarding that captures structural content preferences, and have the `headline-and-outline` and `keyword-and-angle` skills read it alongside the existing brand files.

**Architecture:** Add three Q&A questions (preferred formats, depth, structural defaults) to `qa.py`, a new `generate_content_prefs()` function to `claude.py` mirroring the existing `generate_claude_files` pattern, wire it into `cli/onboard.py`, and update the two skills to include `content-prefs.md` in their inputs tables and reference it at the relevant decision points.

**Tech Stack:** Python 3.11+, pytest, Claude CLI (`claude --print`), markdown skill files

---

## File Map

| File | Change |
|---|---|
| `src/seo_system/onboard/qa.py` | Add 3 questions to `run_qa()`; add fields to `build_qa_text()` |
| `src/seo_system/onboard/claude.py` | Add `CONTENT_PREFS_PROMPT` constant and `generate_content_prefs()` function |
| `src/seo_system/cli/onboard.py` | Import and call `generate_content_prefs()` |
| `skills/headline-and-outline.md` | Add `content-prefs.md` to inputs table; reference at Steps 1 and 4 |
| `skills/keyword-and-angle.md` | Add `content-prefs.md` to inputs table; reference in format/structure analysis |
| `tests/test_content_prefs.py` | New — tests for `build_qa_text` additions and `generate_content_prefs()` |

---

### Task 1: Add content structure Q&A questions

**Files:**
- Modify: `src/seo_system/onboard/qa.py`
- Test: `tests/test_content_prefs.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_content_prefs.py
from seo_system.onboard.qa import build_qa_text


def test_build_qa_text_includes_content_prefs():
    data = {
        "name": "Acme",
        "website": "https://acme.com",
        "industry": "Tax advisory",
        "primary_market": "UK SMEs",
        "voice_style": "direct",
        "reader_feeling": "confident",
        "voice_phrases": ["clarity", "no jargon"],
        "voice_never": ["vague advice"],
        "differentiator": "real practitioners",
        "jargon_policy": "explain on first use",
        "extra_voice_notes": "",
        "opening_pattern": "Situation first",
        "opinion_style": "Opinionated",
        "teaching_style": "Worked examples",
        "editorial_asides": "Honestly, that's the bar.",
        "howto_format": "Numbered steps",
        "preferred_formats": "Guides and comparisons",
        "article_depth": "In-depth (2000+ words)",
        "structural_defaults": "No listicles; tables for data only",
        "audience_segments": [],
        "content_goals": "- Organic traffic",
    }
    result = build_qa_text(data)
    assert "Preferred content formats: Guides and comparisons" in result
    assert "Article depth: In-depth (2000+ words)" in result
    assert "Structural defaults: No listicles; tables for data only" in result
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/sam/Documents/seo-content-system && python -m pytest tests/test_content_prefs.py::test_build_qa_text_includes_content_prefs -v
```

Expected: FAIL — `KeyError` or assertion error because fields not in `build_qa_text` yet.

- [ ] **Step 3: Add questions to `run_qa()` and fields to `build_qa_text()`**

In `src/seo_system/onboard/qa.py`, add a new part after the existing `howto_format` question (still inside `run_qa`, before Part 4 — Audience):

```python
    data["preferred_formats"] = ask(
        "What content formats work best for their audience? (e.g. guides, listicles, comparisons, "
        "news-style) — list them:",
        default="Guides",
    )
    data["article_depth"] = ask(
        "Preferred article depth? (e.g. concise 1000-1500 words / standard 1500-2500 / "
        "in-depth 2500+):",
        default="Standard (1500-2500 words)",
    )
    data["structural_defaults"] = ask(
        "Any structural rules — e.g. 'no listicles', 'tables for data only', 'always use "
        "comparison sections'? (Enter to skip):"
    )
```

Then in `build_qa_text()`, add these lines after the `howto_format` line:

```python
Preferred content formats: {data.get('preferred_formats', '')}
Article depth: {data.get('article_depth', '')}
Structural defaults: {data.get('structural_defaults', '')}
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /Users/sam/Documents/seo-content-system && python -m pytest tests/test_content_prefs.py::test_build_qa_text_includes_content_prefs -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/seo_system/onboard/qa.py tests/test_content_prefs.py
git commit -m "feat: add content structure Q&A questions and build_qa_text fields"
```

---

### Task 2: Add `generate_content_prefs()` to claude.py

**Files:**
- Modify: `src/seo_system/onboard/claude.py`
- Test: `tests/test_content_prefs.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_content_prefs.py`:

```python
from pathlib import Path
from unittest.mock import patch
from seo_system.onboard.claude import generate_content_prefs


def test_generate_content_prefs_writes_file(tmp_path):
    fake_content = "# Content Preferences — Acme\n\n## Preferred content formats\nGuides\n"
    with patch("seo_system.onboard.claude.call_claude", return_value=fake_content):
        generate_content_prefs(tmp_path, "some Q&A text", "Acme")
    result = (tmp_path / "content-prefs.md").read_text()
    assert result.strip() == fake_content.strip()


def test_generate_content_prefs_placeholder_on_failure(tmp_path):
    with patch("seo_system.onboard.claude.call_claude", return_value=None):
        generate_content_prefs(tmp_path, "some Q&A text", "Acme")
    result = (tmp_path / "content-prefs.md").read_text()
    assert "Acme" in result
    assert "Fill in manually" in result
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /Users/sam/Documents/seo-content-system && python -m pytest tests/test_content_prefs.py::test_generate_content_prefs_writes_file tests/test_content_prefs.py::test_generate_content_prefs_placeholder_on_failure -v
```

Expected: FAIL — `ImportError: cannot import name 'generate_content_prefs'`

- [ ] **Step 3: Add `CONTENT_PREFS_PROMPT` and `generate_content_prefs()` to `claude.py`**

Add after the `AUDIENCE_PROMPT` constant (before `VOICE_DNA_PROMPT`):

```python
CONTENT_PREFS_PROMPT = """\
You are a content strategist. Based on the client Q&A below, write a content preferences \
reference file for a content team. This file is read by skills before generating headlines, \
outlines, and keyword strategies — it records structural and format preferences so every \
article feels consistent with this brand's publishing approach.

Output ONLY the content-prefs.md file content. No preamble, no explanation outside the file.

Structure the file exactly as follows:

# Content Preferences — {client_name}
*Generated from onboarding data. Edit if anything is wrong.*

---

## Preferred content formats
[Which formats suit this brand and audience — guides, comparisons, listicles, news-style, \
tool/calculator pages? For each format mentioned, note when to use it and when to avoid it.]

---

## Article depth and length
[Short and targeted (1000–1500 words) / Standard (1500–2500) / In-depth (2500+)? \
Is there a strong preference or does it depend on topic complexity?]

---

## Structural defaults
- **How-to content:** [numbered steps with short labels / flowing prose with descriptive headers]
- **Lists and tables:** [use freely / restrict to data-heavy sections / avoid]
- **Comparison sections:** [include by default / include when competitors differ / avoid]
- **Reader pathways:** [single reader per article / structure by reader type when segments diverge]

---

## Headline preferences
- **Preferred types:** [e.g. problem-first, outcome-first, specificity hook — list in priority order]
- **Tone:** [direct and informational / curious / authoritative / conversational]
- **Length:** [under 55 characters / under 65 characters]

---

## What this client never publishes
[Format or structural patterns this brand avoids — e.g. no pure listicles, no click-bait \
headlines, no "10 things" framing.]

---

CLIENT Q&A
==========
{qa_text}
"""
```

Add the function after `generate_claude_files`:

```python
def generate_content_prefs(brand_dir: Path, qa_text: str, client_name: str):
    print("  → Generating content-prefs.md with Claude...")
    content = call_claude(CONTENT_PREFS_PROMPT.format(
        client_name=client_name,
        qa_text=qa_text,
    ))
    if content:
        (brand_dir / "content-prefs.md").write_text(content + "\n", encoding="utf-8")
        print("  ✓ content-prefs.md written")
    else:
        print("  ✗ Claude failed — writing placeholder content-prefs.md")
        (brand_dir / "content-prefs.md").write_text(
            f"# Content Preferences — {client_name}\n\n"
            "*Generated from onboarding Q&A — Claude was not available. Fill in manually.*\n\n"
            "## Preferred content formats\n\n"
            "## Article depth and length\n\n"
            "## Structural defaults\n\n"
            "## Headline preferences\n\n"
            "## What this client never publishes\n",
            encoding="utf-8",
        )
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /Users/sam/Documents/seo-content-system && python -m pytest tests/test_content_prefs.py::test_generate_content_prefs_writes_file tests/test_content_prefs.py::test_generate_content_prefs_placeholder_on_failure -v
```

Expected: PASS

- [ ] **Step 5: Run the full test suite to check nothing broke**

```bash
cd /Users/sam/Documents/seo-content-system && python -m pytest -v
```

Expected: all tests PASS

- [ ] **Step 6: Commit**

```bash
git add src/seo_system/onboard/claude.py tests/test_content_prefs.py
git commit -m "feat: add generate_content_prefs() for brand/content-prefs.md"
```

---

### Task 3: Wire `generate_content_prefs` into the onboarding CLI

**Files:**
- Modify: `src/seo_system/cli/onboard.py`

- [ ] **Step 1: Update the import line in `onboard.py`**

Current import (line 19):
```python
from seo_system.onboard.claude import generate_claude_files, generate_voice_dna
```

Replace with:
```python
from seo_system.onboard.claude import generate_claude_files, generate_content_prefs, generate_voice_dna
```

- [ ] **Step 2: Call `generate_content_prefs` after `generate_claude_files`**

Current block (around line 104–105):
```python
    header("Generating brand voice files with Claude")
    generate_claude_files(brand_dir, build_qa_text(data), data["name"])
```

Replace with:
```python
    header("Generating brand voice files with Claude")
    qa_text = build_qa_text(data)
    generate_claude_files(brand_dir, qa_text, data["name"])
    generate_content_prefs(brand_dir, qa_text, data["name"])
```

- [ ] **Step 3: Update the "Next steps" message to mention content-prefs.md**

Current block (around lines 116–120):
```python
    print("  Next steps:")
    print("    1. Review brand/brand-voice-card.md — edit anything Claude got wrong")
    print("    2. Review brand/audience-profiles.md — fill any gaps")
    print("    3. Run your first article:")
    print(f"       python3 run_workflow.py --client {client_slug} --article \"your keyword\" --step all")
```

Replace with:
```python
    print("  Next steps:")
    print("    1. Review brand/brand-voice-card.md — edit anything Claude got wrong")
    print("    2. Review brand/audience-profiles.md — fill any gaps")
    print("    3. Review brand/content-prefs.md — confirm format and headline preferences")
    print("    4. Run your first article:")
    print(f"       python3 run_workflow.py --client {client_slug} --article \"your keyword\" --step all")
```

- [ ] **Step 4: Run the full test suite**

```bash
cd /Users/sam/Documents/seo-content-system && python -m pytest -v
```

Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/seo_system/cli/onboard.py
git commit -m "feat: wire generate_content_prefs into onboarding CLI"
```

---

### Task 4: Update `headline-and-outline` skill

**Files:**
- Modify: `skills/headline-and-outline.md`

- [ ] **Step 1: Add `content-prefs.md` to the inputs table**

Find the inputs table (around line 26). The current last row is:
```
| `BRAND_DIR/audience-profiles.md` | Reader segments with emotional triggers and frustrations — read if it exists; use in Step 2 |
```

Add a new row directly after it:
```
| `BRAND_DIR/content-prefs.md` | Structural and format preferences — read if it exists; use in Steps 1 and 4 |
```

- [ ] **Step 2: Reference content-prefs in Step 1 (Write headlines)**

Find the line (around line 47):
```
Rules for all five:
```

Add a sentence before the rules list:
```
If `BRAND_DIR/content-prefs.md` exists, check **Headline preferences** — use the preferred types and tone as the starting point when selecting which of the five variants to favour.
```

- [ ] **Step 3: Reference content-prefs in Step 4 (Build the outline)**

Find the **Outline rules** bullet list (around line 138). After the bullet:
```
- If reader pathways converge: structure must match the dominant SERP format from `DATA_DIR/keyword.json`
```

Add:
```
- If `BRAND_DIR/content-prefs.md` exists: cross-reference **Structural defaults** — if the client never uses listicles, do not propose a listicle structure even if the SERP favours it; if they prefer reader-pathway structure when segments diverge, apply that here
```

- [ ] **Step 4: Commit**

```bash
git add skills/headline-and-outline.md
git commit -m "feat: update headline-and-outline skill to read content-prefs.md"
```

---

### Task 5: Update `keyword-and-angle` skill

**Files:**
- Modify: `skills/keyword-and-angle.md`

- [ ] **Step 1: Add `content-prefs.md` to the inputs table**

Find the inputs table (around line 18). The current last row is:
```
| `BRAND_DIR/audience-profiles.md` | Client's reader segments with trust signals, bounce triggers, and content frustrations — read if it exists |
```

Add a new row directly after it:
```
| `BRAND_DIR/content-prefs.md` | Structural and format preferences — read if it exists; use when assessing dominant format fit |
```

- [ ] **Step 2: Reference content-prefs in the format/structure analysis**

Find the **Intent and format** block (around line 52):
```
**Intent and format:**
- What is the dominant intent? (informational / navigational / commercial / transactional)
- What content format dominates? (guide, listicle, tool page, comparison, news)
```

Add a bullet after the format line:
```
- If `BRAND_DIR/content-prefs.md` exists: note whether the dominant SERP format conflicts with the client's preferred formats — flag any conflict in the angle so the outline step can resolve it
```

- [ ] **Step 3: Commit**

```bash
git add skills/keyword-and-angle.md
git commit -m "feat: update keyword-and-angle skill to read content-prefs.md"
```

---

## Self-Review

**Spec coverage:**
- ✅ New Q&A questions captured in `qa.py`
- ✅ `build_qa_text` includes new fields
- ✅ `generate_content_prefs()` added to `claude.py` with placeholder fallback
- ✅ Wired into `cli/onboard.py`
- ✅ `headline-and-outline.md` inputs table + headline step + outline step updated
- ✅ `keyword-and-angle.md` inputs table + format analysis updated
- ✅ Tests cover `build_qa_text` additions and `generate_content_prefs()` (success + failure)

**Placeholder scan:** None found.

**Type consistency:** `generate_content_prefs(brand_dir: Path, qa_text: str, client_name: str)` — matches the signature of `generate_claude_files` and is called with the same arguments in Task 3.
