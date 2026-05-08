"""Tests for git_utils (using temp repos)."""

import datetime
import os
import tempfile

import pytest
from git import Repo

from bimd.git_utils import get_commit_date, get_first_commit_date, get_repo


@pytest.fixture()
def tmp_repo(tmp_path):
    """Create a temporary git repo with a single commit."""
    repo = Repo.init(tmp_path)
    repo.config_writer().set_value("user", "name", "Test").release()
    repo.config_writer().set_value("user", "email", "test@test.com").release()
    # Create a file and commit
    f = tmp_path / "hello.txt"
    f.write_text("hello")
    repo.index.add(["hello.txt"])
    repo.index.commit("initial commit")
    return repo


class TestGetRepo:
    def test_valid_repo(self, tmp_repo):
        repo = get_repo(tmp_repo.working_dir)
        assert repo.working_dir == tmp_repo.working_dir

    def test_invalid_path_raises(self, tmp_path):
        empty = tmp_path / "empty"
        empty.mkdir()
        with pytest.raises(Exception):
            get_repo(empty)


class TestGetFirstCommitDate:
    def test_returns_date(self, tmp_repo):
        d = get_first_commit_date(tmp_repo)
        assert isinstance(d, datetime.date)
        assert d == datetime.date.today()


class TestGetCommitDate:
    def test_by_hash(self, tmp_repo):
        sha = tmp_repo.head.commit.hexsha
        d = get_commit_date(tmp_repo, sha)
        assert isinstance(d, datetime.date)

    def test_by_short_hash(self, tmp_repo):
        short = tmp_repo.head.commit.hexsha[:7]
        d = get_commit_date(tmp_repo, short)
        assert isinstance(d, datetime.date)

    def test_bad_hash_raises(self, tmp_repo):
        with pytest.raises(Exception):
            get_commit_date(tmp_repo, "deadbeef1234567890")
