import json

from seo_system.steps import RunContext, _seed_publisher_meta


def _make_profile(tmp_path):
    brand_dir = tmp_path / "brand"
    brand_dir.mkdir()
    (tmp_path / "profile.md").write_text(
        "**Client name:** Monx\n**Website:** https://monx.team/\n",
        encoding="utf-8",
    )
    return brand_dir


def test_seed_publisher_meta_builds_article_url(tmp_path):
    brand_dir = _make_profile(tmp_path)
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    ctx = RunContext(content_dir=tmp_path, brand_dir=brand_dir)

    _seed_publisher_meta(ctx, data_dir, "us-expat-tax")

    meta = json.loads((data_dir / "meta.json").read_text(encoding="utf-8"))
    assert meta["site_url"] == "https://monx.team"
    assert meta["url"] == "https://monx.team/blog/us-expat-tax/"


def test_seed_publisher_meta_preserves_existing_url(tmp_path):
    brand_dir = _make_profile(tmp_path)
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "meta.json").write_text(
        json.dumps({"url": "https://monx.team/blog/custom-slug/"}), encoding="utf-8"
    )
    ctx = RunContext(content_dir=tmp_path, brand_dir=brand_dir)

    _seed_publisher_meta(ctx, data_dir, "us-expat-tax")

    meta = json.loads((data_dir / "meta.json").read_text(encoding="utf-8"))
    assert meta["url"] == "https://monx.team/blog/custom-slug/"
