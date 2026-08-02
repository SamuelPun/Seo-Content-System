import json

from generate_checklist import _generate


def _write_workspace(tmp_path, *, with_author):
    data_dir = tmp_path / "data"
    publish_dir = tmp_path / "publish"
    data_dir.mkdir()
    publish_dir.mkdir()

    meta = {
        "title": "Some Article Title About Tax For SEO Testing Here",
        "description": "A" * 150,
    }
    data_dir.joinpath("meta.json").write_text(json.dumps(meta), encoding="utf-8")

    article_schema = {
        "@type": "Article",
        "headline": meta["title"],
        "datePublished": "2026-01-01",
        "publisher": {"@type": "Organization", "name": "Monx"},
        "description": meta["description"],
    }
    if with_author:
        article_schema["author"] = {"@type": "Person", "name": "Jane Doe"}
    data_dir.joinpath("schema.json").write_text(json.dumps([article_schema]), encoding="utf-8")

    schema_script_tag = json.dumps([article_schema])
    publish_dir.joinpath("final.html").write_text(
        "<html><head><title>{t}</title>"
        '<meta name="description" content="x">'
        '<script type="application/ld+json">{s}</script>'
        "</head><body><h1>{t}</h1></body></html>".format(t=meta["title"], s=schema_script_tag),
        encoding="utf-8",
    )
    return publish_dir


def test_checklist_ready_without_author(tmp_path):
    publish_dir = _write_workspace(tmp_path, with_author=False)
    _generate(tmp_path)
    checklist = publish_dir.joinpath("publish-checklist.md").read_text(encoding="utf-8")
    assert "None — ready to publish." in checklist
    assert "missing: author" not in checklist


def test_checklist_flags_actually_missing_field(tmp_path):
    publish_dir = _write_workspace(tmp_path, with_author=False)
    schema = json.loads(publish_dir.parent.joinpath("data", "schema.json").read_text(encoding="utf-8"))
    del schema[0]["publisher"]
    publish_dir.parent.joinpath("data", "schema.json").write_text(json.dumps(schema), encoding="utf-8")

    _generate(tmp_path)
    checklist = publish_dir.joinpath("publish-checklist.md").read_text(encoding="utf-8")
    assert "missing: publisher" in checklist
