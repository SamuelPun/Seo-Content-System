import json

from generate_schema import (
    build_article_schema,
    build_faq_schema,
    build_howto_schema,
    detect_type,
    extract_headings,
    extract_questions,
    extract_title,
    run,
)

# ---------------------------------------------------------------------------
# extract_title
# ---------------------------------------------------------------------------

def test_extract_title_found():
    assert extract_title("# Tax Treaties Explained\n\nSome content.") == "Tax Treaties Explained"


def test_extract_title_none():
    assert extract_title("## Section only\n\nContent.") is None


# ---------------------------------------------------------------------------
# extract_headings
# ---------------------------------------------------------------------------

def test_extract_headings_h2_and_h3():
    text = "# H1\n## Section A\n### Sub-section\n#### H4 ignored"
    assert extract_headings(text) == ["Section A", "Sub-section"]


def test_extract_headings_none():
    assert extract_headings("# Only H1\n\nParagraph.") == []


# ---------------------------------------------------------------------------
# extract_questions
# ---------------------------------------------------------------------------

def test_extract_questions_filters_by_question_mark():
    text = "## What is a tax treaty?\n## How does it work?\n## Overview"
    assert extract_questions(text) == ["What is a tax treaty?", "How does it work?"]


def test_extract_questions_none():
    assert extract_questions("## Overview\n## Details") == []


# ---------------------------------------------------------------------------
# detect_type
# ---------------------------------------------------------------------------

def test_detect_type_article_default():
    text = "# Title\n\n## Overview\n\nContent."
    assert detect_type(text) == "Article"


def test_detect_type_faqpage():
    text = (
        "# Title\n\n"
        "## What is a tax treaty?\n\nAnswer one.\n\n"
        "## How do dividends work?\n\nAnswer two."
    )
    assert detect_type(text) == "FAQPage"


def test_detect_type_howto_via_step_headings():
    text = (
        "# Guide\n\n"
        "## Step 1: Register\n\nDo this.\n\n"
        "## Step 2: Submit\n\nDo that.\n\n"
        "## Step 3: Confirm\n\nDone."
    )
    assert detect_type(text) == "HowTo"


def test_detect_type_howto_via_numbered_list():
    text = "# Guide\n\n1. First thing\n2. Second thing\n3. Third thing"
    assert detect_type(text) == "HowTo"


def test_detect_type_howto_beats_faq():
    # Steps take priority — checked first in detect_type
    text = (
        "1. First\n2. Second\n3. Third\n\n"
        "## What is X?\n\nAnswer.\n\n"
        "## What is Y?\n\nAnswer."
    )
    assert detect_type(text) == "HowTo"


# ---------------------------------------------------------------------------
# build_article_schema
# ---------------------------------------------------------------------------

def test_build_article_schema_structure():
    schema = build_article_schema("My Title", "https://example.com/page/", "2026-04-24")
    assert schema["@type"] == "Article"
    assert schema["@context"] == "https://schema.org"
    assert schema["headline"] == "My Title"
    assert schema["url"] == "https://example.com/page/"
    assert schema["datePublished"] == "2026-04-24"
    assert schema["dateModified"] == "2026-04-24"
    assert schema["publisher"]["@type"] == "Organization"


# ---------------------------------------------------------------------------
# build_faq_schema
# ---------------------------------------------------------------------------

FAQ_TEXT = (
    "# Title\n\n"
    "## What is a tax treaty?\n\n"
    "A tax treaty is an agreement between two countries.\n\n"
    "## How are dividends taxed?\n\n"
    "Dividends may be taxed at a reduced rate under treaty rules."
)


def test_build_faq_schema_structure():
    schema = build_faq_schema(FAQ_TEXT)
    assert schema is not None
    assert schema["@type"] == "FAQPage"
    assert len(schema["mainEntity"]) == 2
    q = schema["mainEntity"][0]
    assert q["@type"] == "Question"
    assert "?" in q["name"]
    assert q["acceptedAnswer"]["@type"] == "Answer"
    assert len(q["acceptedAnswer"]["text"]) > 0


def test_build_faq_schema_returns_none_when_no_pairs():
    assert build_faq_schema("## No questions here\n\nJust a section.") is None


# ---------------------------------------------------------------------------
# build_howto_schema
# ---------------------------------------------------------------------------

HOWTO_TEXT = (
    "# File Your Taxes\n\n"
    "## Step 1: Gather Documents\n\nCollect your W-2 and 1099 forms.\n\n"
    "## Step 2: Choose a Filing Method\n\nDecide between online and paper.\n\n"
    "## Step 3: Submit Your Return\n\nMail or e-file."
)


def test_build_howto_schema_structure():
    schema = build_howto_schema("File Your Taxes", HOWTO_TEXT)
    assert schema is not None
    assert schema["@type"] == "HowTo"
    assert schema["name"] == "File Your Taxes"
    assert len(schema["step"]) == 3
    assert schema["step"][0]["@type"] == "HowToStep"
    assert schema["step"][0]["position"] == 1
    assert schema["step"][1]["position"] == 2


def test_build_howto_schema_returns_none_when_no_steps():
    assert build_howto_schema("Title", "## Overview\n\nNo steps here.") is None


# ---------------------------------------------------------------------------
# run — file I/O
# ---------------------------------------------------------------------------

def test_run_missing_draft(tmp_path):
    assert run(tmp_path / "missing.md", None, tmp_path / "out") is False


def test_run_preserves_date_published_across_reruns(tmp_path, monkeypatch):
    """Regression test: regenerating output (e.g. after fixing a typo) must move
    dateModified forward but never rewrite the original datePublished to today."""
    draft = tmp_path / "draft.md"
    draft.write_text("# My Article\n\n## Overview\n\nContent.", encoding="utf-8")
    meta_path = tmp_path / "meta.json"
    meta_path.write_text(json.dumps({"url": "https://example.com/"}), encoding="utf-8")
    out = tmp_path / "out"

    import generate_schema

    class _FixedDate:
        def __init__(self, iso):
            self._iso = iso

        def isoformat(self):
            return self._iso

    class _FakeDateModule:
        def __init__(self, iso):
            self._iso = iso

        def today(self):
            return _FixedDate(self._iso)

    monkeypatch.setattr(generate_schema, "date", _FakeDateModule("2026-01-01"))
    assert run(draft, meta_path, out) is True
    first = json.loads((out / "schema.json").read_text())[0]
    assert first["datePublished"] == "2026-01-01"
    assert first["dateModified"] == "2026-01-01"
    assert json.loads(meta_path.read_text())["date_first_published"] == "2026-01-01"

    # Re-run later, as if fixing a typo and regenerating output.
    monkeypatch.setattr(generate_schema, "date", _FakeDateModule("2026-03-15"))
    assert run(draft, meta_path, out) is True
    second = json.loads((out / "schema.json").read_text())[0]
    assert second["datePublished"] == "2026-01-01"   # unchanged
    assert second["dateModified"] == "2026-03-15"     # moved forward


def test_run_article_schema(tmp_path):
    draft = tmp_path / "draft.md"
    draft.write_text("# My Article\n\n## Overview\n\nContent.", encoding="utf-8")
    out = tmp_path / "out"
    assert run(draft, None, out, url="https://example.com/") is True
    schemas = json.loads((out / "schema.json").read_text())
    assert schemas[0]["@type"] == "Article"
    assert len(schemas) == 1


def test_run_faq_schema(tmp_path):
    draft = tmp_path / "draft.md"
    draft.write_text(FAQ_TEXT, encoding="utf-8")
    out = tmp_path / "out"
    run(draft, None, out, url="https://example.com/")
    schemas = json.loads((out / "schema.json").read_text())
    types = [s["@type"] for s in schemas]
    assert "Article" in types
    assert "FAQPage" in types


def test_run_howto_schema(tmp_path):
    draft = tmp_path / "draft.md"
    draft.write_text(HOWTO_TEXT, encoding="utf-8")
    out = tmp_path / "out"
    run(draft, None, out, url="https://example.com/")
    schemas = json.loads((out / "schema.json").read_text())
    types = [s["@type"] for s in schemas]
    assert "Article" in types
    assert "HowTo" in types
