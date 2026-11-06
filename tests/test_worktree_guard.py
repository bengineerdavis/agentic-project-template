"""APT-32: the worktree guard must decline AND relent, by audience.

A guard that blocks everything and a guard that blocks nothing both "pass"
a naive test — the first looks strict, the second looks safe. These tests
pin every branch of the decision, which is what `docs/TESTING.md` means by
proving the test fails against a deliberately broken copy.

The guard's contract (amended 2026-11-06 for the audience split):

  subagent (parentID set)      + main checkout -> BLOCK
  unattended agent (no tty)    + main checkout -> BLOCK
  interactive agent            + main checkout -> WARN, prompt, obey
  any agent                    + worktree      -> permit
  no agent marker (human)      + main checkout -> permit
  outside any git repository                    -> permit
"""

from __future__ import annotations

import fcntl
import json
import os
import pty
import subprocess
import termios
from pathlib import Path

import pytest

# The guard ships in template/, so copier stamps it into every project at
# scripts/check-worktree.sh -- the path the prek fragment points at.
SCRIPT = Path(__file__).resolve().parents[1] / "template" / "scripts" / "check-worktree.sh"

# Environment markers any supported agent sets. The guard must treat the
# presence of ANY of them as "this is an agent session".
AGENT_MARKERS = ("AGENT", "AI_AGENT", "CLAUDE_CODE", "CURSOR_AGENT")


def _base_env(extra: dict[str, str]) -> dict[str, str]:
    env = {"PATH": os.environ["PATH"], "HOME": os.environ.get("HOME", "/root")}
    env.update(extra)
    return env


def run_guard(cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess:
    """Run the guard in `cwd` with no controlling terminal."""
    return subprocess.run(
        ["bash", str(SCRIPT)],
        cwd=str(cwd),
        env=_base_env(env),
        capture_output=True,
        text=True,
        timeout=30,
    )


def run_guard_with_tty(
    cwd: Path, env: dict[str, str], answer: str
) -> subprocess.CompletedProcess:
    """Run the guard attached to a real controlling terminal.

    `pty.openpty()` plus `setsid` + TIOCSCTTY is the portable replacement
    for GNU `script -c`, which BSD `script` does not implement.
    """
    master, slave = pty.openpty()

    def _child_setup() -> None:
        os.setsid()
        fcntl.ioctl(slave, termios.TIOCSCTTY, 0)

    proc = subprocess.Popen(
        ["bash", str(SCRIPT)],
        cwd=str(cwd),
        env=_base_env(env),
        stdin=slave,
        stdout=slave,
        stderr=slave,
        preexec_fn=_child_setup,
    )
    os.close(slave)
    os.write(master, (answer + "\n").encode())

    chunks: list[bytes] = []
    try:
        while True:
            chunk = os.read(master, 4096)
            if not chunk:
                break
            chunks.append(chunk)
    except OSError:
        pass
    os.close(master)
    proc.wait(timeout=30)
    return subprocess.CompletedProcess(
        args=proc.args,
        returncode=proc.returncode,
        stdout=b"".join(chunks).decode(errors="replace"),
        stderr="",
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


@pytest.fixture
def stub_opencode(tmp_path: Path):
    """Put a fake `opencode` on PATH that answers the session-lineage query.

    Writing the stub rather than hitting the real API keeps the test
    hermetic and lets it pin both shapes: a top-level session (no
    `parentID` key at all) and a subagent (`parentID` present).
    """

    def _install(parent_id: str | None) -> dict[str, str]:
        bin_dir = tmp_path / "bin"
        bin_dir.mkdir(exist_ok=True)
        doc = {"id": "ses_test"}
        if parent_id is not None:
            doc["parentID"] = parent_id
        (bin_dir / "opencode").write_text(
            "#!/usr/bin/env bash\n"
            "if [ \"$1\" = api ] && [ \"$2\" = get ]; then\n"
            f"  printf '%s' '{json.dumps(doc)}'\n"
            "  exit 0\n"
            "fi\n"
            "exit 1\n"
        )
        (bin_dir / "opencode").chmod(0o755)
        return {
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "OPENCODE_SESSION_ID": "ses_test",
            # Without an agent marker the guard treats the caller as a human
            # and exits before any of these rules run — which would make
            # every test below pass vacuously.
            "AGENT": "1",
        }

    return _install


# --- who is asking -------------------------------------------------------


def test_blocks_a_subagent_even_with_a_terminal(
    main_checkout: Path, stub_opencode
) -> None:
    """A subagent is never the single writer, terminal or not.

    Given a terminal on purpose: the subagent rule must win over the
    interactive override, otherwise a spawned helper could talk its way in.
    """
    env = stub_opencode("ses_parent")
    result = run_guard_with_tty(main_checkout, env, answer="main")
    assert result.returncode != 0, (
        "a subagent must be blocked even when it could prompt"
    )
    assert "subagent" in result.stdout.lower(), (
        f"the message must name the subagent rule; got: {result.stdout}"
    )


def test_blocks_an_unattended_agent_commit(main_checkout: Path, stub_opencode) -> None:
    """No terminal means nobody can approve; fail closed."""
    env = stub_opencode(None)
    result = run_guard(main_checkout, env)
    assert result.returncode != 0
    assert "unattended" in result.stderr.lower(), result.stderr
    assert "wt switch --create" in result.stderr, (
        "the block message must name the fix, not just the failure"
    )


def test_interactive_agent_is_permitted_when_the_human_types_main(
    main_checkout: Path, stub_opencode
) -> None:
    """The maintainer keeps an escape hatch, typed rather than inherited."""
    env = stub_opencode(None)
    result = run_guard_with_tty(main_checkout, env, answer="main")
    assert result.returncode == 0, (
        f"typing 'main' must permit the commit; got: {result.stdout}"
    )
    assert "MAIN CHECKOUT" in result.stdout, (
        "the warning must be loud even when the human proceeds"
    )


def test_interactive_agent_is_blocked_when_the_human_declines(
    main_checkout: Path, stub_opencode
) -> None:
    """Enter alone aborts: silence is not consent."""
    env = stub_opencode(None)
    result = run_guard_with_tty(main_checkout, env, answer="")
    assert result.returncode != 0
    assert "Aborted" in result.stdout, result.stdout


# --- where they are ------------------------------------------------------


def test_permits_an_agent_commit_inside_a_worktree(
    worktree: Path, stub_opencode
) -> None:
    """The rule's whole point: agent work in its own worktree is allowed."""
    env = stub_opencode(None)
    result = run_guard(worktree, env)
    assert result.returncode == 0, (
        f"agent work in a worktree must be permitted, got: {result.stderr}"
    )


def test_permits_a_human_commit_from_the_main_checkout(main_checkout: Path) -> None:
    """The maintainer commits to main legitimately; the guard must not bind them."""
    result = run_guard(main_checkout, {})
    assert result.returncode == 0, (
        f"a human commit from the main checkout must be permitted, got: {result.stderr}"
    )


def test_permits_commit_outside_any_repository(tmp_path: Path, stub_opencode) -> None:
    """A guard that breaks commits in non-git directories is worse than none."""
    plain = tmp_path / "plain"
    plain.mkdir()
    result = run_guard(plain, stub_opencode("ses_parent"))
    assert result.returncode == 0, (
        f"outside a repository the guard must not interfere, got: {result.stderr}"
    )


@pytest.mark.parametrize("marker", AGENT_MARKERS)
def test_every_supported_agent_marker_triggers_the_guard(
    main_checkout: Path, stub_opencode, marker: str
) -> None:
    """A guard that only knows one agent's env var is a guard with a hole."""
    env = stub_opencode(None)
    env[marker] = "1"
    result = run_guard(main_checkout, env)
    assert result.returncode != 0, (
        f"{marker} is an agent session; committing from the main checkout must block"
    )
    # Nonzero alone is not enough: a missing or unreadable script also exits
    # nonzero, which would let these pass while the guard does nothing.
    assert "wt switch --create" in result.stderr, (
        f"{marker} must produce the guard's own message, not a shell "
        f"error; got: {result.stderr}"
    )
