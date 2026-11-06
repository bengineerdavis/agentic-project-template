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
# The guard binds ONLY agent sessions, identified by environment. The
# maintainer commits to main from the main checkout legitimately, and the
# task-store carve-out sends coordination writes to main — a blanket
# check would block the person it is meant to protect. `--no-verify`
# remains a deliberate, visible escape; this script does not try to
# defeat it.
#
# Exit codes: 0 permit, 1 block.

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
  # A linked worktree: the agent is where it should be.
  exit 0
fi

# Main checkout from here on.
if ! is_agent_session; then
  exit 0
fi

cat <<'MSG' >&2
Blocked: this is an agent session committing in the main checkout.

Task work belongs in a worktree whose branch is named from the task id:

    wt switch --create <task-id-slug>

That creates the branch and worktree and moves the session into it. If the
work is mid-flight here, move it:

    git stash push -u -m wip
    wt switch --create <branch>      # or: git worktree add .worktrees/<sid> -b <branch>
    git stash pop

A guard that could be satisfied by habit would not be a guard, so this
blocks. `git commit --no-verify` bypasses it deliberately and visibly.
MSG
exit 1
