#!/usr/bin/env bash
# APT-32 — refuse an agent commit made from a main checkout.
#
# The layer already states this rule twice (spec.md § Behavior: Isolation,
# fragments/tools/worktrunk/agents.md). Both are prose, and prose did not
# bind: a session read them, created worktrees, used them as command
# targets rather than as its home, and worked from the main checkout for
# hours. This is the binding form.
#
# Detection is mechanical. In a main checkout `git rev-parse --git-dir`
# and `--git-common-dir` name the same path; in a linked worktree the
# git-dir is <common>/worktrees/<name>, so they differ.
#
# Response depends on who is asking, not on which agent is running:
#
#   subagent        -> block. A subagent is never the single writer.
#   non-interactive -> block. A tool call cannot reach a terminal, so it
#                      cannot be given an override by a human.
#   interactive     -> warn loudly and offer a prompted override. The
#                      maintainer keeps their escape hatch; it is typed,
#                      not inherited.
#
# The maintainer commits to main from the main checkout legitimately, and
# the task-store carve-out sends coordination writes to main. That is why
# the interactive branch exists at all rather than a blanket block.
#
# `--no-verify` remains a deliberate, visible escape; this script does not
# try to defeat it.
#
# Exit codes: 0 permit, 1 block, 3 block-and-remediated (see below).

set -euo pipefail

# Any supported agent sets one of these. Copied from observed session
# environments, not from documentation — see APT-32.
is_agent_session() {
  local marker
  for marker in AGENT AI_AGENT CLAUDE_CODE CURSOR_AGENT; do
    if [ -n "${!marker:-}" ]; then
      return 0
    fi
  done
  return 1
}

# A subagent carries a parent session id; a top-level session does not.
#
# Verified 2026-11-06 against opencode 2.2.5: GET /api/session/<id> omits
# `parentID` entirely for a session the human started, and sets it to the
# parent session id for a session spawned by a subagent call. Absence, not
# null, is the top-level signal.
#
# When the API is unreachable we cannot prove top-level, so we treat the
# session as a subagent. Failing closed here costs a retry; failing open
# lets a subagent write from the main checkout, which is the bug.
#
# The failure is reported as an ENVIRONMENT fault, not a policy violation.
# A downed daemon and a subagent both block, but they need different fixes,
# and a message that names the wrong one sends the reader after the wrong
# problem. This is the distinction APT-33 generalises.
session_is_subagent() {
  local sid="${OPENCODE_SESSION_ID:-}" doc
  [ -n "$sid" ] || return 1

  if ! command -v opencode >/dev/null 2>&1; then
    printf 'Cannot determine session type: the opencode CLI is not on PATH.\n' >&2
    printf 'This is an environment problem, not a worktree violation.\n' >&2
    return 0
  fi

  doc="$(opencode api get "/api/session/$sid" 2>/dev/null || true)"
  if [ -z "$doc" ]; then
    printf 'Cannot determine session type: the opencode service is unreachable.\n' >&2
    printf 'This is an environment problem, not a worktree violation.\n' >&2
    return 0
  fi

  case "$doc" in
    *parentID*) return 0 ;;
    *) return 1 ;;
  esac
}

# A human's terminal is reachable; a tool call's is not. Verified
# 2026-11-06: from an opencode tool call /dev/tty is readable but CANNOT be
# opened, so an override prompt there would fail rather than hang.
has_terminal() {
  { exec </dev/tty; } 2>/dev/null || return 1
  return 0
}

# Outside a repository there is nothing to guard. A check that breaks
# commits in plain directories is worse than no check.
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  exit 0
fi

git_dir="$(git rev-parse --git-dir 2>/dev/null || true)"
common_dir="$(git rev-parse --git-common-dir 2>/dev/null || true)"

# Both absent: not a checkout we understand — stay out of the way.
if [ -z "$git_dir" ] || [ -z "$common_dir" ]; then
  exit 0
fi

# Normalise before comparing: one command may return ".git" and the other
# an absolute path to the same directory.
normalise() {
  ( cd "$1" 2>/dev/null && pwd -P ) || printf '%s' "$1"
}

if [ "$(normalise "$git_dir")" != "$(normalise "$common_dir")" ]; then
  # A linked worktree: the agent is where it should be. Ownership is
  # enforced here, at the one place a worktree commit happens, rather than
  # at commit time in general -- the main-checkout rules above are a
  # different question from "may this session write to this branch".
  branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
  owners="$(dirname "$0")/wt-owners.sh"
  if [ -n "$branch" ] && [ -x "$owners" ]; then
    # A missing owner script means the project did not adopt ownership;
    # that must not block, or this hook breaks every project that has not.
    "$owners" check "$branch" || {
      printf 'Run: %s release %s   (only the holder may do this)\n' "$owners" "$branch" >&2
      exit 1
    }
  fi
  exit 0
fi

# Main checkout from here on.
if ! is_agent_session; then
  exit 0
fi

remedy() {
  cat <<'MSG'
Task work belongs in a worktree whose branch is named from the task id:

    wt switch --create <task-id-slug>

That creates the branch and worktree and moves the session into it. If the
work is mid-flight here, move it:

    git stash push -u -m wip
    wt switch --create <branch>
    git stash pop

`git commit --no-verify` bypasses this deliberately and visibly.
MSG
}

# Terminal reachability is checked BEFORE the session query, and the query
# only runs on the interactive path. Two reasons:
#
#   1. Cost. A tool call has no terminal, so it is decided here without a
#      network round trip. Only a human-driven commit pays for the query.
#   2. Blast radius. The query needs the opencode daemon. Consulting it on
#      every path meant an unreachable daemon blocked every agent commit in
#      the main checkout, including a human's, with a message that read like
#      a policy violation. An environment fault must not masquerade as one.
if ! has_terminal; then
  cat <<'MSG' >&2
Blocked: this is an unattended agent commit in the main checkout.

No terminal is attached, so nobody can approve main-checkout work here.
Run it interactively if that is really what you want.

MSG
  remedy >&2
  exit 1
fi

# Interactive from here on, so the session query is affordable. A subagent
# that somehow has a terminal is still never the single writer.
if session_is_subagent; then
  cat <<'MSG' >&2
Blocked: a subagent tried to commit in the main checkout.

A subagent is never the single writer for a branch. Hand the work back to
the session that spawned you; that session owns the worktree and commits.

MSG
  remedy >&2
  exit 1
fi

# Interactive agent session: warn loudly, then let a human decide.
cat <<'MSG' >&2

  WARNING — you are committing in the MAIN CHECKOUT from an agent session.

  Everything else waits its turn behind this working tree. A worktree keeps
  this task's branch and the main checkout's cleanliness separate.

MSG
remedy >&2
printf '\nType "main" to commit here anyway, or press Enter to abort: ' >&2
read -r answer </dev/tty || answer=''
if [ "$answer" = "main" ]; then
  printf 'Proceeding in the main checkout, as instructed.\n' >&2
  exit 0
fi
printf 'Aborted. Use a worktree.\n' >&2
exit 1
