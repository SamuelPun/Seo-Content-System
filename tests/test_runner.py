import subprocess

from seo_system import runner


class _FakeCompletedProcess:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _fake_ws(tmp_path):
    ws = tmp_path / "workspace"
    (ws / "editorial").mkdir(parents=True)
    (ws / "data").mkdir()
    (ws / "publish").mkdir()
    return ws


# ---------------------------------------------------------------------------
# run_script — timeout handling
# ---------------------------------------------------------------------------

def test_run_script_returns_false_on_timeout(monkeypatch):
    def fake_run(cmd, timeout=None):
        raise subprocess.TimeoutExpired(cmd=cmd, timeout=timeout)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)
    assert runner.run_script("some_script.py", ["--x", "1"], timeout=5) is False


def test_run_script_returns_true_on_success(monkeypatch):
    monkeypatch.setattr(runner.subprocess, "run", lambda cmd, timeout=None: _FakeCompletedProcess(returncode=0))
    assert runner.run_script("some_script.py", [], timeout=5) is True


def test_run_script_returns_false_on_nonzero_exit(monkeypatch):
    monkeypatch.setattr(runner.subprocess, "run", lambda cmd, timeout=None: _FakeCompletedProcess(returncode=1))
    assert runner.run_script("some_script.py", [], timeout=5) is False


# ---------------------------------------------------------------------------
# run_claude_skill — SkillRunResult status classification
# ---------------------------------------------------------------------------

def test_run_claude_skill_missing_skill_file(tmp_path):
    ws = _fake_ws(tmp_path)
    result = runner.run_claude_skill("does-not-exist.md", ws, tmp_path / "brand")
    assert result.status == "failed"
    assert not result.ok


def test_run_claude_skill_timeout(tmp_path, monkeypatch):
    def fake_run(*a, **kw):
        raise subprocess.TimeoutExpired(cmd=a[0], timeout=kw.get("timeout"))

    monkeypatch.setattr(runner.subprocess, "run", fake_run)
    ws = _fake_ws(tmp_path)
    result = runner.run_claude_skill("writing.md", ws, tmp_path / "brand", timeout=5)
    assert result.status == "timeout"
    assert not result.ok


def test_run_claude_skill_detects_usage_limit_in_output(tmp_path, monkeypatch):
    monkeypatch.setattr(
        runner.subprocess, "run",
        lambda *a, **kw: _FakeCompletedProcess(returncode=1, stdout="Claude usage limit reached, try again later."),
    )
    ws = _fake_ws(tmp_path)
    result = runner.run_claude_skill("writing.md", ws, tmp_path / "brand")
    assert result.status == "usage_limit"
    assert not result.ok


def test_run_claude_skill_ok(tmp_path, monkeypatch):
    monkeypatch.setattr(
        runner.subprocess, "run",
        lambda *a, **kw: _FakeCompletedProcess(returncode=0, stdout="done"),
    )
    ws = _fake_ws(tmp_path)
    result = runner.run_claude_skill("writing.md", ws, tmp_path / "brand")
    assert result.status == "ok"
    assert result.ok


def test_run_claude_skill_generic_failure(tmp_path, monkeypatch):
    monkeypatch.setattr(
        runner.subprocess, "run",
        lambda *a, **kw: _FakeCompletedProcess(returncode=2, stdout="", stderr="some unrelated crash"),
    )
    ws = _fake_ws(tmp_path)
    result = runner.run_claude_skill("writing.md", ws, tmp_path / "brand")
    assert result.status == "failed"
    assert not result.ok


# ---------------------------------------------------------------------------
# _skill_model — optional per-skill model override via frontmatter
# ---------------------------------------------------------------------------

def test_skill_model_absent_by_default():
    assert runner._skill_model("---\nname: foo\ndescription: bar\n---\n\n# Skill\n") is None


def test_skill_model_read_from_frontmatter():
    content = "---\nname: foo\nmodel: claude-haiku-4-5-20251001\n---\n\n# Skill\n"
    assert runner._skill_model(content) == "claude-haiku-4-5-20251001"


def test_run_claude_skill_passes_model_flag(tmp_path, monkeypatch, tmp_path_factory):
    captured = {}

    def fake_run(cmd, **kw):
        captured["cmd"] = cmd
        return _FakeCompletedProcess(returncode=0)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)
    monkeypatch.setattr(runner, "SKILLS_DIR", tmp_path)
    (tmp_path / "cheap-role.md").write_text(
        "---\nname: cheap-role\nmodel: claude-haiku-4-5-20251001\n---\n\nBody.\n", encoding="utf-8"
    )
    ws = _fake_ws(tmp_path_factory.mktemp("ws"))

    result = runner.run_claude_skill("cheap-role.md", ws, tmp_path / "brand")

    assert result.ok
    assert "--model" in captured["cmd"]
    assert captured["cmd"][captured["cmd"].index("--model") + 1] == "claude-haiku-4-5-20251001"
