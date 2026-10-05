import json

from seo_system.runner import SkillRunResult
from seo_system.steps import RunContext, _run_substeps, _seed_publisher_meta
from seo_system.workspace import mark_substep_complete


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


_FAKE_SUBSTEPS = [("role-a", "role-a.md", False, ("out.md",))]


def _fake_run_claude_skill(skill_file, ws, brand_dir, seed=None):
    """Stand in for a Claude session: writes the draft substep's expected output,
    never touches editor-verdict.json (a revision pass doesn't re-run the Editor —
    only a human, or a fresh Editor role, can actually change approval)."""
    if skill_file == "role-a.md":
        (ws / "editorial" / "out.md").write_text("draft", encoding="utf-8")
    return SkillRunResult("ok")


def _make_substep_workspace(tmp_path, article, approved):
    content_dir = tmp_path
    ws = content_dir / article
    (ws / "editorial").mkdir(parents=True)
    (ws / "editorial" / "editor-verdict.json").write_text(
        json.dumps({"approved": approved, "notes": "test"}), encoding="utf-8"
    )
    return content_dir, ws


def test_run_substeps_rejected_after_revision_needs_human(tmp_path, monkeypatch):
    """Editor rejects, the one revision pass runs, editor-verdict.json is still
    approved:false (nothing re-runs the Editor) — must come back needs_human, not
    silently complete."""
    monkeypatch.setattr("seo_system.steps.run_claude_skill", _fake_run_claude_skill)
    content_dir, ws = _make_substep_workspace(tmp_path, "art", approved=False)
    ctx = RunContext(content_dir=content_dir, brand_dir=tmp_path / "brand", seed="test seed")

    result = _run_substeps(
        ctx, "art", "fake-step", _FAKE_SUBSTEPS,
        draft_name="role-a", revise_name="role-a-revise",
        revise_skill="role-a-revise.md", seed_prompt="  seed: ",
    )

    assert result.status == "needs_human"


def test_run_substeps_resumed_run_still_rejected_needs_human(tmp_path, monkeypatch):
    """Regression test for the teapot-hong-kong bug: on a re-run where the draft AND
    the revision substep are already checkpointed complete from a prior invocation,
    but editor-verdict.json is still approved:false, the step must not be marked
    complete just because there's nothing left to run."""
    monkeypatch.setattr("seo_system.steps.run_claude_skill", _fake_run_claude_skill)
    content_dir, ws = _make_substep_workspace(tmp_path, "art", approved=False)
    mark_substep_complete(content_dir, "art", "fake-step", "role-a")
    mark_substep_complete(content_dir, "art", "fake-step", "role-a-revise")
    ctx = RunContext(content_dir=content_dir, brand_dir=tmp_path / "brand")

    result = _run_substeps(
        ctx, "art", "fake-step", _FAKE_SUBSTEPS,
        draft_name="role-a", revise_name="role-a-revise",
        revise_skill="role-a-revise.md", seed_prompt="  seed: ",
    )

    assert result.status == "needs_human"


def test_run_substeps_approved_is_complete(tmp_path, monkeypatch):
    monkeypatch.setattr("seo_system.steps.run_claude_skill", _fake_run_claude_skill)
    content_dir, ws = _make_substep_workspace(tmp_path, "art", approved=True)
    ctx = RunContext(content_dir=content_dir, brand_dir=tmp_path / "brand", seed="test seed")

    result = _run_substeps(
        ctx, "art", "fake-step", _FAKE_SUBSTEPS,
        draft_name="role-a", revise_name="role-a-revise",
        revise_skill="role-a-revise.md", seed_prompt="  seed: ",
    )

    assert result.status == "complete"
