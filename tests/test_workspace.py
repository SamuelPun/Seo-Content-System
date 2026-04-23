"""Tests for workspace log I/O and step tracking."""

import json
from pathlib import Path

import pytest

from seo_system.workspace import (
    workspace, log_path, load_log, save_log,
    mark_complete, mark_pending, is_complete,
    update_content_index, init_article_files, log_step_start, log_step_end,
)
from seo_system.config import STEPS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_content_dir(tmp_path: Path) -> Path:
    d = tmp_path / "content"
    d.mkdir()
    return d


# ---------------------------------------------------------------------------
# workspace / log_path
# ---------------------------------------------------------------------------

def test_workspace_returns_correct_path(tmp_path):
    content_dir = make_content_dir(tmp_path)
    assert workspace(content_dir, "us-expat-tax") == content_dir / "us-expat-tax"


def test_log_path_is_inside_data(tmp_path):
    content_dir = make_content_dir(tmp_path)
    p = log_path(content_dir, "my-article")
    assert p == content_dir / "my-article" / "data" / "log.json"


# ---------------------------------------------------------------------------
# load_log / save_log
# ---------------------------------------------------------------------------

def test_load_log_returns_default_when_missing(tmp_path):
    content_dir = make_content_dir(tmp_path)
    log = load_log(content_dir, "new-article")
    assert log["article"] == "new-article"
    assert log["steps"] == {}
    assert log["keyword"] == ""


def test_save_and_load_roundtrip(tmp_path):
    content_dir = make_content_dir(tmp_path)
    (content_dir / "my-article" / "data").mkdir(parents=True)
    original = {"article": "my-article", "keyword": "expat tax", "steps": {}}
    save_log(content_dir, "my-article", original)
    loaded = load_log(content_dir, "my-article")
    assert loaded == original


def test_save_log_creates_parent_dirs(tmp_path):
    content_dir = make_content_dir(tmp_path)
    # No pre-created dirs — save_log should create them
    save_log(content_dir, "brand-new", {"article": "brand-new", "steps": {}})
    assert log_path(content_dir, "brand-new").exists()


# ---------------------------------------------------------------------------
# mark_complete / mark_pending / is_complete
# ---------------------------------------------------------------------------

def test_mark_complete_sets_status(tmp_path):
    content_dir = make_content_dir(tmp_path)
    mark_complete(content_dir, "article-a", "keyword")
    log = load_log(content_dir, "article-a")
    assert log["steps"]["keyword"]["status"] == "complete"
    assert "completed_at" in log["steps"]["keyword"]


def test_is_complete_true_after_mark(tmp_path):
    content_dir = make_content_dir(tmp_path)
    mark_complete(content_dir, "article-a", "keyword")
    assert is_complete(content_dir, "article-a", "keyword") is True


def test_is_complete_false_when_not_run(tmp_path):
    content_dir = make_content_dir(tmp_path)
    assert is_complete(content_dir, "article-a", "keyword") is False


def test_mark_pending_resets_status(tmp_path):
    content_dir = make_content_dir(tmp_path)
    mark_complete(content_dir, "article-a", "keyword")
    mark_pending(content_dir, "article-a", "keyword")
    assert is_complete(content_dir, "article-a", "keyword") is False
    log = load_log(content_dir, "article-a")
    assert log["steps"]["keyword"]["status"] == "pending"


# ---------------------------------------------------------------------------
# update_content_index
# ---------------------------------------------------------------------------

def test_update_content_index_creates_index(tmp_path):
    content_dir = make_content_dir(tmp_path)
    mark_complete(content_dir, "expat-tax", "keyword")
    save_log(content_dir, "expat-tax", {
        "article": "expat-tax",
        "display_name": "US Expat Tax",
        "keyword": "us expat tax",
        "steps": {"keyword": {"status": "complete"}},
    })
    update_content_index(content_dir)
    index = (content_dir / "_index.md").read_text()
    assert "US Expat Tax" in index
    assert "keyword" in index


def test_update_content_index_skips_underscore_dirs(tmp_path):
    content_dir = make_content_dir(tmp_path)
    (content_dir / "_ignored").mkdir()
    update_content_index(content_dir)
    index = (content_dir / "_index.md").read_text()
    assert "_ignored" not in index


# ---------------------------------------------------------------------------
# init_article_files
# ---------------------------------------------------------------------------

def test_init_article_files_creates_work_log(tmp_path):
    ws = tmp_path / "my-article"
    ws.mkdir()
    init_article_files("my-article", ws, "My Article")
    work_log = ws / "editorial" / "work-log.md"
    assert work_log.exists()
    assert "My Article" in work_log.read_text()


def test_init_article_files_creates_writer_notes(tmp_path):
    ws = tmp_path / "my-article"
    ws.mkdir()
    init_article_files("my-article", ws, "My Article")
    assert (ws / "editorial" / "writer-notes.md").exists()


def test_init_article_files_does_not_overwrite(tmp_path):
    ws = tmp_path / "my-article"
    ws.mkdir()
    init_article_files("my-article", ws, "First")
    first_content = (ws / "editorial" / "work-log.md").read_text()
    init_article_files("my-article", ws, "Second")
    assert (ws / "editorial" / "work-log.md").read_text() == first_content
