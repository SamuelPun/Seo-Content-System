import json

from scan_banned_phrases import run, scan

# ---------------------------------------------------------------------------
# scan — clean text
# ---------------------------------------------------------------------------

def test_scan_clean_text():
    assert scan("This is a plain, clean sentence with no issues.") == []


def test_scan_empty_string():
    assert scan("") == []


# ---------------------------------------------------------------------------
# scan — HIGH severity
# ---------------------------------------------------------------------------

def test_scan_em_dash_detected():
    hits = scan("The rate — which applies here — is 15%.")
    assert any(h["phrase"] == "—" and h["severity"] == "HIGH" for h in hits)


def test_scan_em_dash_not_in_clean_line():
    hits = scan("The rate - which applies here - is 15%.")
    assert not any(h["phrase"] == "—" for h in hits)


def test_scan_single_word_high_word_boundary():
    hits = scan("We should delve into this topic.")
    assert any(h["phrase"] == "delve" for h in hits)


def test_scan_single_word_no_partial_match():
    hits = scan("Theindelvement of stakeholders.")
    assert not any(h["phrase"] == "delve" for h in hits)


def test_scan_multiword_phrase_case_insensitive():
    hits = scan("Let's Dive Into the details of this guide.")
    assert any(h["phrase"] == "let's dive into" for h in hits)


def test_scan_multiword_phrase_not_matched_in_clean_text():
    hits = scan("Let us look at the details of this guide.")
    assert not any(h["phrase"] == "let's dive into" for h in hits)


# ---------------------------------------------------------------------------
# scan — MEDIUM severity
# ---------------------------------------------------------------------------

def test_scan_medium_word_boundary():
    hits = scan("This is a comprehensive guide to tax planning.")
    assert any(h["phrase"] == "comprehensive" and h["severity"] == "MEDIUM" for h in hits)


def test_scan_medium_no_partial_match():
    # "comprehensively" should not trigger "comprehensive"
    hits = scan("This is comprehensively explained.")
    assert not any(h["phrase"] == "comprehensive" for h in hits)


# ---------------------------------------------------------------------------
# scan — metadata accuracy
# ---------------------------------------------------------------------------

def test_scan_line_number_correct():
    text = "Line one is fine.\nLine two has delve in it.\nLine three is fine."
    hits = scan(text)
    delve_hits = [h for h in hits if h["phrase"] == "delve"]
    assert delve_hits[0]["line_number"] == 2


def test_scan_line_text_included():
    text = "We should delve into this."
    hits = scan(text)
    assert hits[0]["line_text"] == "We should delve into this."


def test_scan_multiple_phrases_same_line():
    text = "This comprehensive guide will delve into the ecosystem."
    hits = scan(text)
    phrases = {h["phrase"] for h in hits}
    assert "comprehensive" in phrases
    assert "delve" in phrases
    assert "ecosystem" in phrases


# ---------------------------------------------------------------------------
# run — file I/O
# ---------------------------------------------------------------------------

def test_run_missing_draft(tmp_path):
    assert run(tmp_path / "missing.md", tmp_path / "out") is False


def test_run_clean_draft_writes_empty_json(tmp_path):
    draft = tmp_path / "draft.md"
    draft.write_text("This is a clean article with no banned terms.", encoding="utf-8")
    out = tmp_path / "out"
    assert run(draft, out) is True
    hits = json.loads((out / "audit-flags.json").read_text())
    assert hits == []


def test_run_flagged_draft_writes_hits(tmp_path):
    draft = tmp_path / "draft.md"
    draft.write_text("We should delve into the synergy here.", encoding="utf-8")
    out = tmp_path / "out"
    run(draft, out)
    hits = json.loads((out / "audit-flags.json").read_text())
    assert len(hits) > 0
    assert any(h["phrase"] == "delve" for h in hits)
