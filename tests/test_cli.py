"""Tests for the CLI commands."""

import os

import pytest
from git import Repo
from typer.testing import CliRunner

from bimd.cli import app
from bimd.i18n import set_lang

runner = CliRunner()


@pytest.fixture(autouse=True)
def _force_french():
    """Default tests to French for backward compat, reset after."""
    set_lang("fr")
    yield
    set_lang("fr")


@pytest.fixture()
def tmp_repo(tmp_path):
    """Create a temporary git repo with a backdated commit."""
    repo = Repo.init(tmp_path)
    repo.config_writer().set_value("user", "name", "Test").release()
    repo.config_writer().set_value("user", "email", "test@test.com").release()
    f = tmp_path / "main.py"
    f.write_text("print('hello')")
    repo.index.add(["main.py"])
    # Backdate the commit to GPT-4 era
    os.environ["GIT_AUTHOR_DATE"] = "2023-04-01T12:00:00"
    os.environ["GIT_COMMITTER_DATE"] = "2023-04-01T12:00:00"
    repo.index.commit("init")
    del os.environ["GIT_AUTHOR_DATE"]
    del os.environ["GIT_COMMITTER_DATE"]
    return tmp_path


class TestScanCommand:
    def test_scan_valid_repo(self, tmp_repo):
        result = runner.invoke(app, ["scan", str(tmp_repo)], color=False)
        assert result.exit_code == 0
        assert "GPT-4" in result.output

    def test_scan_invalid_path(self, tmp_path):
        empty = tmp_path / "nope"
        empty.mkdir()
        result = runner.invoke(app, ["scan", str(empty)])
        assert result.exit_code == 1


class TestEraCommand:
    def test_era_with_date(self):
        result = runner.invoke(app, ["era", "2023-03-15"])
        assert result.exit_code == 0
        assert "GPT-4" in result.output

    def test_era_with_old_date(self):
        result = runner.invoke(app, ["era", "2015-01-01"])
        assert result.exit_code == 0
        assert "Silencieuse" in result.output

    def test_era_with_future_date(self):
        result = runner.invoke(app, ["era", "2027-01-01"])
        assert result.exit_code == 0
        assert "Terra Incognita" in result.output

    def test_era_english_with_flag(self):
        result = runner.invoke(app, ["--lang", "en", "era", "2015-01-01"])
        assert result.exit_code == 0
        assert "Silent Era" in result.output

    def test_era_english_gpt4(self):
        result = runner.invoke(app, ["--lang", "en", "era", "2023-03-15"])
        assert result.exit_code == 0
        assert "GPT-4 Revolution" in result.output

    def test_era_with_commit_hash(self, tmp_repo):
        repo = Repo(tmp_repo)
        sha = repo.head.commit.hexsha[:8]
        result = runner.invoke(app, ["era", sha, "--path", str(tmp_repo)])
        assert result.exit_code == 0
        assert "GPT-4" in result.output

    def test_era_bad_hash(self):
        result = runner.invoke(app, ["era", "zzzzzz"])
        assert result.exit_code == 1


class TestBadgeCommand:
    def test_badge_generates_markdown(self, tmp_repo):
        result = runner.invoke(app, ["badge", str(tmp_repo)], color=False)
        assert result.exit_code == 0
        assert "shields.io" in result.output
        assert "BackInMyDay" in result.output

    def test_badge_invalid_repo(self, tmp_path):
        empty = tmp_path / "nope"
        empty.mkdir()
        result = runner.invoke(app, ["badge", str(empty)])
        assert result.exit_code == 1
