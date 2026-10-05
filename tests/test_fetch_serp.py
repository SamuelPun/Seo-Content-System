import json

import fetch_serp


def test_run_records_duckduckgo_provenance(tmp_path, monkeypatch):
    """No API key → DDG fallback path. serp-meta.json must say so, since a DDG run
    has no domain_rating/traffic/PAA and looks identical to a genuinely sparse
    Ahrefs result unless provenance is recorded somewhere."""
    monkeypatch.setattr(
        fetch_serp, "fetch_serp_ddg",
        lambda keyword, top: [{"position": 1, "url": "https://example.com", "title": "Example",
                                "snippet": "x", "domain_rating": None, "url_rating": None,
                                "traffic": None, "keywords": None, "backlinks": None, "refdomains": None}],
    )

    ok = fetch_serp.run(keyword="test kw", country="us", top=10, out_dir=tmp_path, api_key=None)

    assert ok is True
    meta = json.loads((tmp_path / "serp-meta.json").read_text())
    assert meta == {"keyword": "test kw", "country": "us", "source": "duckduckgo"}


def test_run_records_ahrefs_provenance(tmp_path, monkeypatch):
    monkeypatch.setattr(
        fetch_serp, "fetch_serp",
        lambda keyword, country, top, api_key: [
            {"position": 1, "url": "https://example.com", "title": "Example",
             "domain_rating": 80, "url_rating": 50, "traffic": 1000,
             "keywords": 10, "backlinks": 5, "refdomains": 3},
        ],
    )

    ok = fetch_serp.run(keyword="test kw", country="us", top=10, out_dir=tmp_path, api_key="fake-key")

    assert ok is True
    meta = json.loads((tmp_path / "serp-meta.json").read_text())
    assert meta == {"keyword": "test kw", "country": "us", "source": "ahrefs"}
