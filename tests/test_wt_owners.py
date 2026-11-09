"""One writer per branch, unlimited readers — the ownership state machine.

Why git refs rather than a file: `git update-ref <ref> <sha> ""` is an
atomic compare-and-swap that creates only if absent. These tests pin that
property directly, because it is the load-bearing claim the whole design
rests on. A file-backed version would pass every test below except
`test_only_one_of_many_concurrent_claims_wins`.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "template" / "scripts" / "wt-owners.sh"


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A repository, because the state lives in git refs."""
    root = tmp_path / "repo"
    root.mkdir()
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@t",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@t",
    }
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=env)
    subprocess.run(
        # --no-verify: this repo stamps its own worktree guard, and these
        # fixtures are scratch repos created from inside an agent session.
        # The guard is not what is under test here.
        ["git", "-C", str(root), "commit", "-q", "--no-verify", "--allow-empty", "-m", "init"],
        check=True,
        env=env,
    )
    return root


@pytest.fixture
def stub_harness(tmp_path: Path):
    """A fake harness whose answer we control per test.

    The module asks one harness-specific question: is this session alive?
    Stubbing it keeps these tests hermetic and lets them pin all three
    answers — live, dead, and cannot-tell.
    """

    counter = {"n": 0}

    def _install(live: bool, dead_ids: tuple[str, ...] = ()) -> dict[str, str]:
        # A fresh directory per call. Sharing one would let a later
        # `_install(live=True)` overwrite the stub an earlier
        # `_install(live=False)` put on PATH, and the dead-session tests
        # would silently assert against a live one.
        #
        # `dead_ids` matters: liveness is asked about the *holder*, not
        # about the caller, and a stub with one answer for every id cannot
        # express "ses_dead is gone but I am running".
        counter["n"] += 1
        bin_dir = tmp_path / f"bin{counter['n']}"
        bin_dir.mkdir(exist_ok=True)
        # Answer per id: name a dead id and get a 404 for it, else live.
        dead_list = " ".join(dead_ids)
        (bin_dir / "opencode").write_text(
            "#!/usr/bin/env bash\n"
            # Match against every argument: `opencode api get /api/session/<id>`
            # puts the id inside $3, but the module does not promise an arity.
            'requested="$*"\n'
            'for dead in ' + (dead_list or "") + '; do\n'
            # An empty pattern matches everything, so an absent dead-list
            # must not run at all. Guarding here rather than inside the
            # case: `*""*` matches any string.
            '  [ -n "$dead" ] || continue\n'
            '  case "$requested" in *"$dead"*) printf \'%s\' \'{"_tag":"SessionNotFoundError"}\'; exit 0;; esac\n'
            "done\n"
            + (
                'printf \'%s\' \'{"data": {"id": "ses_x"}}\'\n'
                if live
                else 'printf \'%s\' \'{"_tag":"SessionNotFoundError"}\'\n'
            )
        )
        (bin_dir / "opencode").chmod(0o755)
        return {"PATH": f"{bin_dir}:{os.environ['PATH']}"}

    return _install


def run(cwd: Path, *args: str, env: dict[str, str] | None = None):
    base = {"PATH": os.environ["PATH"], "HOME": os.environ.get("HOME", "/root")}
    base.update(env or {})
    return subprocess.run(
        ["bash", str(SCRIPT), *args],
        cwd=str(cwd),
        env=base,
        capture_output=True,
        text=True,
        timeout=60,
    )


def run_with_tty(cwd: Path, *args: str, env: dict[str, str] | None = None):
    """Run with a real controlling terminal.

    `has_terminal` opens /dev/tty, which a plain subprocess has no access to
    — so without this, every --force path is refused for the wrong reason:
    "no terminal" rather than "no reason". Given one, the higher gates
    become reachable and the grant can actually be exercised.

    pty.openpty() plus setsid and TIOCSCTTY is the portable replacement for
    GNU `script -c`, which BSD `script` does not implement.
    """
    import fcntl
    import pty
    import termios

    base = {"PATH": os.environ["PATH"], "HOME": os.environ.get("HOME", "/root")}
    base.update(env or {})

    master, slave = pty.openpty()

    def _child_setup() -> None:
        os.setsid()
        fcntl.ioctl(slave, termios.TIOCSCTTY, 0)

    proc = subprocess.Popen(
        ["bash", str(SCRIPT), *args],
        cwd=str(cwd),
        env=base,
        stdin=slave,
        stdout=slave,
        stderr=slave,
        preexec_fn=_child_setup,
    )
    os.close(slave)
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
    proc.wait(timeout=60)
    return subprocess.CompletedProcess(
        args=proc.args,
        returncode=proc.returncode,
        stdout=b"".join(chunks).decode(errors="replace"),
        stderr="",
    )


# --- the load-bearing property ------------------------------------------


def test_only_one_of_many_concurrent_claims_wins(repo: Path) -> None:
    """The reason this is git refs and not a file.

    Twenty sessions claim the same branch at once. Exactly one may win.
    A read-modify-write on a file passes single-threaded tests and fails
    this one.
    """
    # Every racer's session must read as LIVE, or the losers would each
    # reclaim from a "dead" holder and the test would prove the opposite of
    # what it claims. A stub that always answers "live" holds liveness
    # fixed while the race runs.
    bin_dir = repo.parent / "racebin"
    bin_dir.mkdir()
    (bin_dir / "opencode").write_text(
        '#!/usr/bin/env bash\nprintf \'%s\' \'{"data": {"id": "ses_x"}}\'\n'
    )
    (bin_dir / "opencode").chmod(0o755)
    env = {
        "PATH": f"{bin_dir}:{os.environ['PATH']}",
        "HOME": os.environ.get("HOME", "/root"),
    }

    procs = []
    for i in range(20):
        procs.append(
            subprocess.Popen(
                ["bash", str(SCRIPT), "claim", "feature/x", "--session", f"ses_{i}"],
                cwd=str(repo),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        )
    results = [(p.wait(), p.stdout.read(), p.stderr.read()) for p in procs]
    winners = [r for r in results if r[0] == 0]
    assert len(winners) == 1, (
        f"exactly one claim may win, got {len(winners)}: {results}"
    )

    holder = run(repo, "holder", "feature/x")
    assert holder.returncode == 0
    assert "session:" in holder.stdout


# --- claim ---------------------------------------------------------------


def test_claiming_an_unheld_branch_succeeds(repo: Path) -> None:
    result = run(repo, "claim", "feature/a", "--session", "ses_1")
    assert result.returncode == 0, result.stderr
    assert "claimed" in result.stdout


def test_claiming_works_with_no_configured_git_identity(tmp_path: Path) -> None:
    """A claim is machine state, not a human commit.

    CI caught this: `git commit-tree` inherits the user identity requirement,
    so on a runner with no user.email every claim failed with "Author
    identity unknown" -- which reads like a concurrency bug and is not one.
    HOME is redirected so git cannot pick up this machine's config.
    """
    root = tmp_path / "noident"
    root.mkdir()
    home = tmp_path / "home"
    home.mkdir()
    # Redirecting HOME is not enough on its own: git derives an identity
    # from the local username and hostname, so a test that only hides
    # ~/.gitconfig passes whether or not the fix is present -- a vacuous
    # test. Emptying user.name/user.email reproduces the CI runner, which
    # has no such fallback.
    env = {
        "PATH": os.environ["PATH"],
        "HOME": str(home),
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": str(home / ".gitconfig"),
        "GIT_AUTHOR_NAME": "",
        "GIT_AUTHOR_EMAIL": "",
        "GIT_COMMITTER_NAME": "",
        "GIT_COMMITTER_EMAIL": "",
    }
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=env)
    (home / ".gitconfig").write_text(
        "[user]\n\tname =\n\temail =\n"
    )
    result = subprocess.run(
        ["bash", str(SCRIPT), "claim", "feature/noident", "--session", "ses_1"],
        cwd=str(root),
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, (
        f"the claim must not need a human identity; got: {result.stderr}"
    )
    assert "claimed" in result.stdout


def test_a_second_writer_is_refused_while_the_first_is_live(repo: Path, stub_harness) -> None:
    env = stub_harness(live=True)
    assert run(repo, "claim", "feature/b", "--session", "ses_1", env=env).returncode == 0

    second = run(repo, "claim", "feature/b", "--session", "ses_2", env=env)
    assert second.returncode != 0
    assert "still running" in second.stderr, second.stderr


def test_readers_do_not_conflict_with_readers(repo: Path, stub_harness) -> None:
    """Unlimited readers: the invariant permits any number."""
    env = stub_harness(live=True)
    assert run(repo, "claim", "feature/c", "--session", "ses_1", "--role", "reader", env=env).returncode == 0
    for i in range(2, 6):
        result = run(repo, "claim", "feature/c", f"--session", f"ses_{i}", "--role", "reader", env=env)
        assert result.returncode == 0, result.stderr


def test_a_writer_blocks_a_reader(repo: Path, stub_harness) -> None:
    """A reader may not join a branch someone is writing."""
    env = stub_harness(live=True)
    assert run(repo, "claim", "feature/d", "--session", "ses_1", "--role", "writer", env=env).returncode == 0
    result = run(repo, "claim", "feature/d", "--session", "ses_2", "--role", "reader", env=env)
    assert result.returncode != 0


def test_reclaiming_from_a_dead_session_succeeds(repo: Path, stub_harness) -> None:
    """A crashed session must not block a branch forever."""
    env = stub_harness(live=True, dead_ids=("ses_dead",))
    assert run(repo, "claim", "feature/e", "--session", "ses_dead", env=env).returncode == 0

    result = run(repo, "claim", "feature/e", "--session", "ses_new", env=env)
    assert result.returncode == 0, result.stderr
    assert "reclaimed" in result.stdout, result.stdout


def test_an_unknown_harness_is_treated_as_live(repo: Path, tmp_path: Path) -> None:
    """Fail closed: a claim we cannot disprove is a claim we respect.

    The session id is present but no harness is recorded, so liveness is
    unknown. Refusing is the safe answer -- taking a claim we cannot verify
    is how two writers end up on one branch.
    """
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "opencode").write_text("#!/usr/bin/env bash\nexit 1\n")
    (bin_dir / "opencode").chmod(0o755)
    env = {"PATH": f"{bin_dir}:{os.environ['PATH']}"}
    assert run(repo, "claim", "feature/f", "--session", "ses_1", env=env).returncode == 0
    result = run(repo, "claim", "feature/f", "--session", "ses_2", env=env)
    assert result.returncode != 0, "an unverifiable claim must still block"


# --- release -------------------------------------------------------------


def test_release_frees_the_branch(repo: Path, stub_harness) -> None:
    env = stub_harness(live=True)
    assert run(repo, "claim", "feature/g", "--session", "ses_1", env=env).returncode == 0
    assert run(repo, "release", "feature/g", "--session", "ses_1", env=env).returncode == 0
    assert run(repo, "holder", "feature/g", env=env).stdout.strip() == "none"


def test_release_refuses_to_free_another_sessions_claim(repo: Path, stub_harness) -> None:
    """Releasing someone else's claim would be theft, not cleanup."""
    env = stub_harness(live=True)
    assert run(repo, "claim", "feature/h", "--session", "ses_1", env=env).returncode == 0
    result = run(repo, "release", "feature/h", "--session", "ses_2", env=env)
    assert result.returncode != 0
    assert "refusing" in result.stderr, result.stderr
    assert "session: ses_1" in run(repo, "holder", "feature/h", env=env).stdout


# --- check: what the commit guard calls ----------------------------------


def test_check_permits_an_unclaimed_branch(repo: Path) -> None:
    """A guard that blocks unclaimed branches breaks every adopter."""
    assert run(repo, "check", "feature/never", "--session", "ses_1").returncode == 0


def test_check_permits_the_holder(repo: Path, stub_harness) -> None:
    env = stub_harness(live=True)
    assert run(repo, "claim", "feature/i", "--session", "ses_1", env=env).returncode == 0
    assert run(repo, "check", "feature/i", "--session", "ses_1", env=env).returncode == 0


def test_check_blocks_a_different_session(repo: Path, stub_harness) -> None:
    env = stub_harness(live=True)
    assert run(repo, "claim", "feature/j", "--session", "ses_1", env=env).returncode == 0
    result = run(repo, "check", "feature/j", "--session", "ses_2", env=env)
    assert result.returncode == 1
    assert "held by writer" in result.stderr, result.stderr


def test_check_permits_when_the_holder_is_only_a_reader(repo: Path, stub_harness) -> None:
    """Unlimited readers: a reader must not block another reader.

    Found by mutation: deleting the reader branch from `check` left every
    test green, because the reader rule was only covered on the `claim`
    path. The guard calls `check`, so an untested branch there is a branch
    that can regress without a failure.
    """
    env = stub_harness(live=True)
    assert run(repo, "claim", "feature/r", "--session", "ses_1", "--role", "reader", env=env).returncode == 0
    assert run(repo, "check", "feature/r", "--session", "ses_2", env=env).returncode == 0


def test_check_permits_when_the_holder_is_dead(repo: Path, stub_harness) -> None:
    """Nobody is writing, so nobody is being blocked by a ghost."""
    env = stub_harness(live=True, dead_ids=("ses_dead",))
    assert run(repo, "claim", "feature/k", "--session", "ses_dead", env=env).returncode == 0
    assert run(repo, "check", "feature/k", "--session", "ses_new", env=env).returncode == 0


# --- state locality ------------------------------------------------------


def test_the_claim_lives_outside_refs_heads_and_notes(repo: Path) -> None:
    """Not pushed, not fetched, and not sharing refs/notes with git-ai."""
    run(repo, "claim", "feature/l", "--session", "ses_1")
    refs = subprocess.run(
        ["git", "-C", str(repo), "for-each-ref", "--format=%(refname)"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    owned = [r for r in refs if "wt-owners" in r]
    assert owned, "the claim must be stored as a ref"
    assert all(r.startswith("refs/wt-owners/") for r in owned), refs
    assert not any(r.startswith("refs/notes/") for r in owned), (
        "ownership must not collide with the notes namespace"
    )


# --- the override, for a session that is alive but stuck -----------------


def test_force_is_refused_from_an_agent_session(repo: Path, stub_harness) -> None:
    """An agent may never take write access from another session.

    Liveness covers a crashed holder. --force exists for one that is ALIVE
    and stuck, which is a judgement only a person can make -- so the gate is
    the one signal an agent's tool call cannot produce.
    """
    env = stub_harness(live=True)
    assert run(repo, "claim", "feature/force", "--session", "ses_held", env=env).returncode == 0
    result = run(
        repo,
        "release",
        "feature/force",
        "--session",
        "ses_taker",
        "--force",
        "--reason",
        "stuck",
        env={**env, "AGENT": "1"},
    )
    assert result.returncode != 0
    assert "agent" in result.stderr.lower(), result.stderr
    # And the claim is untouched.
    assert "ses_held" in run(repo, "holder", "feature/force", env=env).stdout


def test_force_without_a_reason_is_refused(repo: Path, stub_harness) -> None:
    """An unreasoned override is indistinguishable from a bug later."""
    env = stub_harness(live=True)
    assert run(repo, "claim", "feature/noreason", "--session", "ses_held", env=env).returncode == 0
    result = run(repo, "release", "feature/noreason", "--session", "ses_taker", "--force", env=env)
    assert result.returncode != 0
    assert "reason" in result.stderr.lower(), result.stderr


def test_force_without_a_terminal_is_refused(repo: Path, stub_harness) -> None:
    """Nobody can confirm an override from a non-interactive shell."""
    env = stub_harness(live=True)
    assert run(repo, "claim", "feature/notty", "--session", "ses_held", env=env).returncode == 0
    result = run(
        repo, "release", "feature/notty", "--session", "ses_taker", "--force", "--reason", "stuck",
        env=env,
    )
    assert result.returncode != 0
    assert "terminal" in result.stderr.lower(), result.stderr


def test_the_refusal_names_the_exact_override_command(repo: Path, stub_harness) -> None:
    """A refusal that does not say how to proceed just blocks work."""
    env = stub_harness(live=True)
    assert run(repo, "claim", "feature/hint", "--session", "ses_held", env=env).returncode == 0
    result = run(repo, "release", "feature/hint", "--session", "ses_taker", env=env)
    assert result.returncode != 0
    assert "--force" in result.stderr and "--reason" in result.stderr, result.stderr


# --- the task a branch serves --------------------------------------------


def test_a_claim_records_the_task_that_names_the_branch(repo: Path) -> None:
    """A claim should answer "whose work is this", not only "which session"."""
    tasks = repo / "tasks"
    tasks.mkdir(parents=True)
    (tasks / "dot-42 - Do-the-thing.md").write_text(
        "---\nid: DOT-42\ntitle: Do the thing\nworktree_branch: feature/tasked\n---\n"
    )
    assert run(repo, "claim", "feature/tasked", "--session", "ses_1").returncode == 0
    holder = run(repo, "holder", "feature/tasked").stdout
    assert "task:" in holder
    assert "dot-42" in holder


def test_a_claim_works_with_no_backlog_at_all(repo: Path) -> None:
    """Ownership must not depend on a task tracker being present."""
    assert not (repo / "tasks").exists()
    result = run(repo, "claim", "feature/plain", "--session", "ses_1")
    assert result.returncode == 0, result.stderr
    assert "task:" not in run(repo, "holder", "feature/plain").stdout


def test_an_explicit_task_overrides_the_search(repo: Path) -> None:
    assert run(repo, "claim", "feature/explicit", "--session", "ses_1", "--task", "DOT-99").returncode == 0
    assert "DOT-99" in run(repo, "holder", "feature/explicit").stdout


# --- coexistence with git notes -----------------------------------------


def test_a_notes_writer_leaves_ownership_untouched(repo: Path) -> None:
    """git-ai (and anything else) writes refs/notes/*; we must be outside it.

    Verified live against git-ai: it installs a pre-commit hook and writes
    refs/notes/ai. A tool that iterates refs/notes/* therefore never sees
    refs/wt-owners/*, and a notes rewrite cannot reach a claim. This test
    pins the namespace boundary mechanically rather than by convention.
    """
    import subprocess as sp

    assert run(repo, "claim", "feature/notes", "--session", "ses_1").returncode == 0
    before = run(repo, "holder", "feature/notes").stdout

    head = sp.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    sp.run(
        ["git", "-C", str(repo), "notes", "--ref=ai", "add", "-m", "ai authorship", head],
        capture_output=True,
        text=True,
        check=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
    )

    # Both namespaces exist, separately.
    refs = sp.run(
        ["git", "-C", str(repo), "for-each-ref", "--format=%(refname)"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    assert any(r.startswith("refs/notes/") for r in refs), "the notes writer did write"
    assert any(r.startswith("refs/wt-owners/") for r in refs), "the claim survived"

    # And a glob over refs/notes/* cannot see the claim.
    notes_glob = sp.run(
        ["git", "-C", str(repo), "for-each-ref", "--format=%(refname)", "refs/notes/"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    assert not any("wt-owners" in r for r in notes_glob), (
        f"a notes-ref sweep must not reach ownership: {notes_glob}"
    )

    # The claim is byte-identical, not merely present.
    assert run(repo, "holder", "feature/notes").stdout == before


def test_force_succeeds_from_a_human_terminal_and_records_the_takeover(
    repo: Path, stub_harness
) -> None:
    """The grant path, which the three refusal tests cannot reach.

    A refusal-only test suite is satisfied by a mechanism that never works:
    every gate refuses, and every assertion about refusing passes. This is
    the counterpart — an override that actually lands, with the record to
    prove who was displaced and why.
    """
    env = stub_harness(live=True)
    assert run(repo, "claim", "feature/takeover", "--session", "ses_stuck", env=env).returncode == 0

    # No agent markers: this is a human at a terminal.
    human = {k: v for k, v in env.items() if k not in ("AGENT", "AI_AGENT", "CLAUDE_CODE", "CURSOR_AGENT")}
    result = run_with_tty(
        repo,
        "release",
        "feature/takeover",
        "--session",
        "ses_human",
        "--force",
        "--reason",
        "holder hung in a retry loop for 40 minutes; user confirmed",
        env=human,
    )

    assert result.returncode == 0, f"the takeover must land; got: {result.stdout}"
    assert "took over" in result.stdout

    holder = run(repo, "holder", "feature/takeover", env=env).stdout
    # The record must name the new holder, the displaced one, and the reason.
    assert "session: ses_human" in holder, holder
    assert "supersedes: ses_stuck" in holder, holder
    assert "reason: holder hung in a retry loop" in holder, holder

    # And the new holder now controls the branch.
    assert run(repo, "check", "feature/takeover", "--session", "ses_human", env=env).returncode == 0
    assert run(repo, "check", "feature/takeover", "--session", "ses_stuck", env=env).returncode == 1
