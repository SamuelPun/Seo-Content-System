import json
from pathlib import Path

import match_internal_links as mil

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def reset_stopwords():
    mil._site_stopwords = set()


# ---------------------------------------------------------------------------
# phrase_hits
# ---------------------------------------------------------------------------

class TestPhraseHits:
    def setup_method(self):
        reset_stopwords()

    def test_single_word_always_false(self):
        assert mil.phrase_hits("treaty", ["us-uk tax treaty"]) is False

    def test_multiword_exact_substring_match(self):
        assert mil.phrase_hits("tax treaty", ["the us-uk tax treaty explained"]) is True

    def test_multiword_word_overlap_match(self):
        assert mil.phrase_hits("dividend withholding", ["withholding tax on dividends"]) is True

    def test_multiword_no_match(self):
        assert mil.phrase_hits("capital gains", ["income tax rates"]) is False

    def test_all_words_are_stopwords_returns_false(self):
        mil._site_stopwords = {"tax", "rate"}
        assert mil.phrase_hits("tax rate", ["the tax rate applies"]) is False

    def test_partial_stopwords_still_matches(self):
        mil._site_stopwords = {"tax"}
        assert mil.phrase_hits("tax treaty", ["the us-uk tax treaty"]) is True


# ---------------------------------------------------------------------------
# score_page
# ---------------------------------------------------------------------------

class TestScorePage:
    def setup_method(self):
        reset_stopwords()

    def _page(self, title="", headings=None, keyphrases=None):
        return {"title": title, "headings": headings or [], "keyphrases": keyphrases or []}

    def test_title_match_scores_3(self):
        page = self._page(title="US-UK tax treaty dividends")
        score, matched = mil.score_page(["tax treaty"], page)
        assert score == 3
        assert "tax treaty" in matched

    def test_heading_match_scores_2(self):
        page = self._page(title="Unrelated page", headings=["Understanding tax treaty rules"])
        score, matched = mil.score_page(["tax treaty"], page)
        assert score == 2

    def test_keyphrase_match_scores_1(self):
        page = self._page(keyphrases=["tax treaty benefits"])
        score, matched = mil.score_page(["tax treaty"], page)
        assert score == 1

    def test_no_match_scores_0(self):
        page = self._page(title="Pension planning guide", headings=["Pension rules"])
        score, matched = mil.score_page(["tax treaty"], page)
        assert score == 0
        assert matched == []

    def test_multiple_phrases_accumulate(self):
        page = self._page(
            title="US-UK tax treaty dividends explained",
            headings=["withholding tax on dividends"],
        )
        score, matched = mil.score_page(["tax treaty", "withholding tax"], page)
        assert score >= 5  # 3 (title) + 2 (heading)
        assert len(matched) == 2


# ---------------------------------------------------------------------------
# extract_keyphrases
# ---------------------------------------------------------------------------

class TestExtractKeyphrases:
    def setup_method(self):
        reset_stopwords()

    def test_short_text_returns_empty(self):
        assert mil.extract_keyphrases("Too short") == []

    def test_normal_text_returns_phrases(self):
        text = (
            "The US-UK tax treaty reduces withholding tax on dividends paid to UK residents. "
            "Under Article 10, qualified residents pay a 15% dividend tax rate. "
            "This treaty has significant implications for expat investors holding US stocks."
        )
        result = mil.extract_keyphrases(text)
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(p, str) for p in result)

    def test_code_blocks_stripped_before_extraction(self):
        text = (
            "```python\ndef secret_function(): pass\n```\n\n"
            "The tax treaty between the US and UK covers dividend withholding rates "
            "for qualified residents investing abroad.\n" * 3
        )
        result = mil.extract_keyphrases(text)
        assert not any("secret_function" in p for p in result)

    def test_heading_lines_stripped(self):
        text = (
            "# Heading Should Not Appear\n\n"
            "The dividend withholding rate under the treaty is fifteen percent "
            "for qualifying UK residents who hold US securities.\n" * 3
        )
        result = mil.extract_keyphrases(text)
        assert not any("heading should not appear" in p for p in result)


# ---------------------------------------------------------------------------
# run — file I/O
# ---------------------------------------------------------------------------

def _make_page_index(tmp_path: Path, pages: list) -> Path:
    p = tmp_path / "page-index.json"
    p.write_text(json.dumps({"pages": pages}), encoding="utf-8")
    return p


def test_run_missing_draft(tmp_path):
    index = _make_page_index(tmp_path, [])
    assert mil.run(tmp_path / "missing.md", index, tmp_path / "out") is False


def test_run_missing_index(tmp_path):
    draft = tmp_path / "draft.md"
    draft.write_text("Some content.", encoding="utf-8")
    assert mil.run(draft, tmp_path / "missing-index.json", tmp_path / "out") is False


def test_run_empty_index_writes_empty_json(tmp_path):
    draft = tmp_path / "draft.md"
    draft.write_text("Some content about tax treaties.", encoding="utf-8")
    index = _make_page_index(tmp_path, [])
    out = tmp_path / "out"
    assert mil.run(draft, index, out) is True
    candidates = json.loads((out / "internal-link-candidates.json").read_text())
    assert candidates == []


def test_run_returns_ranked_candidates(tmp_path):
    draft = tmp_path / "draft.md"
    draft.write_text(
        "The US-UK tax treaty reduces withholding tax on dividends. "
        "Qualified UK residents benefit from lower dividend rates under Article 10. "
        "This has major implications for expats holding US equities abroad.\n" * 5,
        encoding="utf-8",
    )
    pages = [
        {"url": "/tax-treaty/", "title": "US-UK Tax Treaty Guide", "headings": ["Dividend rules"], "keyphrases": ["tax treaty", "withholding"], "lastmod": None},
        {"url": "/pension/", "title": "Pension Planning", "headings": ["Retirement savings"], "keyphrases": ["pension", "retirement"], "lastmod": None},
    ]
    index = _make_page_index(tmp_path, pages)
    out = tmp_path / "out"
    mil.run(draft, index, out)
    candidates = json.loads((out / "internal-link-candidates.json").read_text())
    # Tax treaty page should rank above pension page
    assert len(candidates) >= 1
    assert candidates[0]["url"] == "/tax-treaty/"
