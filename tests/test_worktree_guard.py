"""APT-32: the worktree guard must decline AND relent.

A guard that blocks everything and a guard that blocks nothing both "pass"
a naive test — the first looks strict, the second looks safe. These tests
pin both directions, which is what `docs/TESTING.md` means by proving the
test fails against a deliberately broken copy.

The guard's contract:
  - agent session (env marker set) + main checkout  -> BLOCK
  - agent session + worktree                       -> permit
  - no agent marker (human) + main checkout        -> permit
  - outside any git repository                     -> permit
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

# The guard ships in template/, so copier stamps it into every project at
# scripts/check-worktree.sh -- the path the prek fragment points at.
SCRIPT = Path(__file__).resolve().parents[1] / "template" / "scripts" / "check-worktree.sh"

# Environment markers any supported agent sets. The guard must treat the
# presence of ANY of them as "this is an agent session".
AGENT_MARKERS = ("AGENT", "AI_AGENT", "CLAUDE_CODE", "CURSOR_AGENT")


def run_guard(cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess:
    """Run the guard in `cwd` with a clean environment plus `env`."""
    base = {
        "PATH": os.environ["PATH"],
        "HOME": os.environ.get("HOME", "/root"),
    }
    base.update(env)
    return subprocess.run(
        ["bash", str(SCRIPT)],
        cwd=str(cwd),
        env=base,
        capture_output=True,
        text=True,
        timeout=30,
    )


@pytest.fixture
def main_checkout(tmp_path: Path) -> Path:
    """A repository's main checkout: git-dir == git-common-dir."""
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-q", "--allow-empty", "-m", "init"],
        check=True,
        env={
            **os.environ,
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@t",
        },
    )
    return repo


@pytest.fixture
def worktree(main_checkout: Path, tmp_path: Path) -> Path:
    """A linked worktree: git-dir lives under <common>/worktrees/<name>."""
    branch_dir = tmp_path / "wt"
    subprocess.run(
        [
            "git",
            "-C",
            str(main_checkout),
            "worktree",
            "add",
            "-q",
            "-b",
            "task-branch",
            str(branch_dir),
        ],
        check=True,
    )
    return branch_dir


def test_blocks_an_agent_commit_from_the_main_checkout(main_checkout: Path) -> None:
    """The failure this guard exists for: agent session, main checkout."""
    result = run_guard(main_checkout, {"AGENT": "1"})
    assert result.returncode != 0, (
        "an agent session committing from the main checkout must be blocked"
    )
    assert "wt switch --create" in result.stderr, (
        "the block message must name the fix, not just the failure"
    )


def test_permits_an_agent_commit_inside_a_worktree(worktree: Path) -> None:
    """The rule's whole point: agent work in its own worktree is allowed."""
    result = run_guard(worktree, {"AGENT": "1"})
    assert result.returncode == 0, (
        f"agent work in a worktree must be permitted, got: {result.stderr}"
    )


def test_permits_a_human_commit_from_the_main_checkout(main_checkout: Path) -> None:
    """The maintainer commits to main legitimately; the guard must not bind them."""
    result = run_guard(main_checkout, {})
    assert result.returncode == 0, (
        f"a human commit from the main checkout must be permitted, got: {result.stderr}"
    )


def test_permits_commit_outside_any_repository(tmp_path: Path) -> None:
    """A guard that breaks commits in non-git directories is worse than none."""
    plain = tmp_path / "plain"
    plain.mkdir()
    result = run_guard(plain, {"AGENT": "1"})
    assert result.returncode == 0, (
        f"outside a repository the guard must not interfere, got: {result.stderr}"
    )


@pytest.mark.parametrize("marker", AGENT_MARKERS)
def test_every_supported_agent_marker_triggers_the_guard(
    main_checkout: Path, marker: str
) -> None:
    """A guard that only knows one agent's env var is a guard with a hole."""
    result = run_guard(main_checkout, {marker: "1"})
    assert result.returncode != 0, (
        f"{marker} is an agent session; committing from the main checkout must block"
    )
    # Nonzero alone is not enough: a missing or unreadable script also exits
    # nonzero, which would let these pass while the guard does nothing.
    assert "wt switch --create" in result.stderr, (
        f"{marker} must produce the guard's own block message, not a shell "
        f"error; got: {result.stderr}"
    )
