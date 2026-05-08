"""Git repository analysis utilities."""

from __future__ import annotations

import datetime
from pathlib import Path

from git import InvalidGitRepositoryError, Repo


def get_repo(path: str | Path) -> Repo:
    """Open a Git repository at *path*, raising on failure."""
    return Repo(str(path), search_parent_directories=True)


def get_first_commit_date(repo: Repo) -> datetime.date:
    """Return the author date of the very first commit in the repo."""
    commits = list(repo.iter_commits(max_count=1, reverse=True))
    if not commits:
        raise ValueError("Le dépôt ne contient aucun commit.")
    first = commits[0]
    return datetime.date.fromtimestamp(first.authored_date)


def get_commit_date(repo: Repo, rev: str) -> datetime.date:
    """Return the author date for a given commit hash or ref."""
    commit = repo.commit(rev)
    return datetime.date.fromtimestamp(commit.authored_date)
