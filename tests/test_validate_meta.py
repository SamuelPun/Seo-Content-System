import json
from pathlib import Path

from validate_meta import (
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
# run — extraction only; length/pass judgment lives in generate_checklist.py
# ---------------------------------------------------------------------------

def _make_draft(tmp_path: Path, title: str, body: str) -> Path:
    p = tmp_path / "draft.md"
    p.write_text(f"# {title}\n\n{body}", encoding="utf-8")
    return p


def test_run_missing_draft(tmp_path):
    assert run(tmp_path / "nonexistent.md", tmp_path / "out") is False


def test_run_writes_meta_json(tmp_path):
    draft = _make_draft(tmp_path, "A Reasonable Article Title", "A reasonably long description paragraph.")
    out = tmp_path / "out"

    assert run(draft, out) is True
    meta = json.loads((out / "meta.json").read_text())
    assert meta["title"] == "A Reasonable Article Title"
    assert meta["description"] == "A reasonably long description paragraph."
    assert "flags" not in meta
    assert "passed" not in meta


def test_run_override_title_and_description(tmp_path):
    draft = _make_draft(tmp_path, "Original Title", "Original body content.")
    custom_title = "A Custom Override Title"
    custom_desc = "A custom override description."
    run(draft, tmp_path / "out", title=custom_title, description=custom_desc)
    meta = json.loads((tmp_path / "out" / "meta.json").read_text())
    assert meta["title"] == custom_title
    assert meta["description"] == custom_desc


def test_run_url_stored_in_meta(tmp_path):
    draft = _make_draft(tmp_path, "A Title", "A description paragraph here.")
    run(draft, tmp_path / "out", url="https://example.com/article/")
    meta = json.loads((tmp_path / "out" / "meta.json").read_text())
    assert meta["url"] == "https://example.com/article/"


def test_run_preserves_existing_fields(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    (out / "meta.json").write_text(json.dumps({"author": "Jane Doe"}), encoding="utf-8")
    draft = _make_draft(tmp_path, "A Title", "A description paragraph here.")
    run(draft, out)
    meta = json.loads((out / "meta.json").read_text())
    assert meta["author"] == "Jane Doe"
    assert meta["title"] == "A Title"
