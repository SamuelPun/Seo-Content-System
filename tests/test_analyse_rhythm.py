import json

from analyse_rhythm import burstiness, run, split_sentences


def test_split_sentences_drops_short_fragments():
    text = "This is a real sentence. Ok. Another real sentence here."
    assert split_sentences(text) == [
        "This is a real sentence.",
        "Another real sentence here.",
    ]


def test_burstiness_zero_for_uniform_lengths():
    assert burstiness([5, 5, 5, 5]) == 0.0


def test_burstiness_nonzero_for_varied_lengths():
    assert burstiness([2, 20, 3, 18]) > 0.4


def test_run_reports_em_dash_count_without_redundant_flag(tmp_path):
    draft = tmp_path / "draft.md"
    draft.write_text(
        "# Title\n\n"
        "This sentence has an em dash — right here in it. "
        "Here is another normal sentence with no dash at all today.\n",
        encoding="utf-8",
    )
    out = tmp_path / "out"

    assert run(draft, out) is True
    result = json.loads((out / "rhythm-analysis.json").read_text())
    assert result["em_dash_count"] == 1
    # em dash policy lives once, in scan_banned_phrases.py — no duplicate flag here.
    assert "em_dash_overuse" not in result["flags"]
    assert "low_burstiness" in result["flags"]
    assert "no_short_sentences" in result["flags"]


def test_run_missing_draft(tmp_path):
    assert run(tmp_path / "nonexistent.md", tmp_path / "out") is False
