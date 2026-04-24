import json
from pathlib import Path

from validate_meta import (
    DESC_MAX,
    DESC_MIN,
    TITLE_MAX,
    TITLE_MIN,
    extract_first_paragraph,
    extract_title,
    run,
)

# ---------------------------------------------------------------------------
# extract_title
# ---------------------------------------------------------------------------

def test_extract_title_basic():
    assert extract_title("# My Article Title\n\nSome text.") == "My Article Title"


def test_extract_title_strips_whitespace():
    assert extract_title("#  Padded Title  \n\nText.") == "Padded Title"


def test_extract_title_returns_first_h1():
    text = "# First\n\n# Second\n\nText."
    assert extract_title(text) == "First"


def test_extract_title_no_h1():
    assert extract_title("## Section\n\nSome text.") is None


def test_extract_title_empty():
    assert extract_title("") is None


# ---------------------------------------------------------------------------
# extract_first_paragraph
# ---------------------------------------------------------------------------

def test_extract_first_paragraph_basic():
    text = "# Title\n\nThis is the first paragraph."
    assert extract_first_paragraph(text) == "This is the first paragraph."


def test_extract_first_paragraph_skips_headings():
    text = "# H1\n## H2\n\nFirst real paragraph."
    result = extract_first_paragraph(text)
    assert result == "First real paragraph."


def test_extract_first_paragraph_skips_code_blocks():
    text = "```python\ncode here\n```\n\nActual paragraph."
    result = extract_first_paragraph(text)
    assert result == "Actual paragraph."


def test_extract_first_paragraph_no_content():
    assert extract_first_paragraph("# Only a heading") is None


# ---------------------------------------------------------------------------
# run — happy path and flag cases
# ---------------------------------------------------------------------------

def _make_draft(tmp_path: Path, title: str, body: str) -> Path:
    p = tmp_path / "draft.md"
    p.write_text(f"# {title}\n\n{body}", encoding="utf-8")
    return p


def test_run_missing_draft(tmp_path):
    assert run(tmp_path / "nonexistent.md", tmp_path / "out") is False


def test_run_writes_meta_json(tmp_path):
    title = "A" * TITLE_MIN  # exactly at min
    desc = "B" * DESC_MIN    # exactly at min
    draft = _make_draft(tmp_path, title, desc)
    out = tmp_path / "out"

    assert run(draft, out) is True
    meta = json.loads((out / "meta.json").read_text())
    assert meta["title"] == title
    assert meta["passed"] is True
    assert meta["flags"] == []


def test_run_title_too_short(tmp_path):
    draft = _make_draft(tmp_path, "Short", "B" * DESC_MIN)
    meta = json.loads((tmp_path / "out" / "meta.json").read_text()) if False else None
    run(draft, tmp_path / "out")
    meta = json.loads((tmp_path / "out" / "meta.json").read_text())
    assert any("Title too short" in f for f in meta["flags"])
    assert meta["passed"] is False


def test_run_title_too_long(tmp_path):
    long_title = "W" * (TITLE_MAX + 1)
    draft = _make_draft(tmp_path, long_title, "B" * DESC_MIN)
    run(draft, tmp_path / "out")
    meta = json.loads((tmp_path / "out" / "meta.json").read_text())
    assert any("Title too long" in f for f in meta["flags"])


def test_run_description_too_short(tmp_path):
    title = "A" * TITLE_MIN
    draft = _make_draft(tmp_path, title, "Too short.")
    run(draft, tmp_path / "out")
    meta = json.loads((tmp_path / "out" / "meta.json").read_text())
    assert any("Description too short" in f for f in meta["flags"])


def test_run_description_too_long(tmp_path):
    title = "A" * TITLE_MIN
    draft = _make_draft(tmp_path, title, "B" * (DESC_MAX + 1))
    run(draft, tmp_path / "out")
    meta = json.loads((tmp_path / "out" / "meta.json").read_text())
    assert any("Description too long" in f for f in meta["flags"])


def test_run_override_title_and_description(tmp_path):
    draft = _make_draft(tmp_path, "Original Title", "Original body content.")
    custom_title = "A" * TITLE_MIN
    custom_desc = "B" * DESC_MIN
    run(draft, tmp_path / "out", title=custom_title, description=custom_desc)
    meta = json.loads((tmp_path / "out" / "meta.json").read_text())
    assert meta["title"] == custom_title
    assert meta["description"] == custom_desc


def test_run_url_stored_in_meta(tmp_path):
    title = "A" * TITLE_MIN
    draft = _make_draft(tmp_path, title, "B" * DESC_MIN)
    run(draft, tmp_path / "out", url="https://example.com/article/")
    meta = json.loads((tmp_path / "out" / "meta.json").read_text())
    assert meta["url"] == "https://example.com/article/"
