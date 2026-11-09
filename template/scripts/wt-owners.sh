#!/usr/bin/env bash
# Per-branch write ownership for concurrent agent sessions.
#
# The invariant: one writer per branch, unlimited readers. Multiple
# interactive sessions may share a branch, but a subagent must never become
# a second writer.
#
# State lives in git refs, not files, because git already implements the
# hard part: `git update-ref <ref> <sha> ""` is an atomic compare-and-swap
# that creates only if absent. Verified 2026-11-08: 20 concurrent claims
# against one ref produced exactly one winner, and the loser gets
# "reference already exists" (rc 128) rather than silently overwriting.
# A file appeared to be simpler and is not -- read-modify-write needs
# flock, and a crash mid-write leaves a stale lock behind.
#
# Refs live under refs/wt-owners/, which is:
#   - shared by every worktree (they share the common dir, so no syncing)
#   - invisible to git push and to git fetch (not a transmitted namespace)
#   - untouched by git gc --prune=now (verified)
#   - separate from refs/notes/*, where git-ai already writes
#
# This machine only, by decision: no push, no fetch refspec to configure.
#
# Usage:
#   wt-owners claim   <branch> [--role writer|reader] [--session ID]
#   wt-owners release <branch> [--session ID]
#   wt-owners holder  <branch>
#   wt-owners check   <branch> [--session ID]
#
# `check` exits 0 when the caller may write, 1 when another live session
# holds the branch. It is the operation the commit guard uses.

set -euo pipefail

REF_PREFIX="refs/wt-owners"

die() {
  printf 'wt-owners: %s\n' "$1" >&2
  exit 2
}

# Branch names contain slashes; ref components may not end in .lock and
# cannot contain .. A percent-encoding would be unreadable, so collapse the
# unsafe characters into dashes and accept the tiny chance of collision
# between two branches differing only there.
ref_for() {
  local branch="$1" slug
  [ -n "$branch" ] || die "a branch name is required"
  slug="$(printf '%s' "$branch" | sed -e 's#[/ ]+#-#g' -e 's#\.\.#-#g')"
  printf '%s/%s' "$REF_PREFIX" "$slug"
}

session_id() {
  printf '%s' "${OPENCODE_SESSION_ID:-${WT_SESSION_ID:-}}"
}

# Which harness produced the session id. Recorded in the payload so that
# adding a second harness later is a new reader, not a schema change. An
# unknown harness is treated as live (fail closed): a claim we cannot
# disprove is a claim we respect.
session_harness() {
  local session="${1:-}"
  if [ -n "${OPENCODE_SESSION_ID:-}" ]; then
    printf 'opencode'
  elif [ -n "$session" ] && [ "${session#ses_}" != "$session" ]; then
    # An explicit --session can arrive without the environment that
    # produced it. opencode's ids have a stable prefix, so the id itself
    # tells us which probe to use. Guess wrong here and liveness reads as
    # unknown, which blocks a dead claim forever.
    printf 'opencode'
  elif [ -n "${WT_SESSION_ID:-}" ]; then
    printf 'other'
  else
    printf 'none'
  fi
}

# Is a session still live?
#
# This is the one harness-specific operation in the module. It answers:
# would a 404 mean "this agent is gone" or "this harness cannot tell"? An
# unreachable service answers "cannot tell", which must read as live.
session_is_live() {
  local session="$1" harness="$2" doc
  [ -n "$session" ] || return 1

  case "$harness" in
    opencode)
      command -v opencode >/dev/null 2>&1 || return 0
      doc="$(opencode api get "/api/session/$session" 2>/dev/null || true)"
      [ -n "$doc" ] || return 0
      case "$doc" in
        *SessionNotFoundError*) return 1 ;;
        *) return 0 ;;
      esac
      ;;
    *)
      # Unknown harness: we cannot disprove liveness, so assume live.
      return 0
      ;;
  esac
}

# The task a branch serves, so a claim answers "whose work is this" and not
# only "which session".
#
# Deliberately tracker-agnostic: the directory is configuration, not a
# hardcoded convention. A repo with no tracker leaves it unset and the field
# simply stays empty, which is why this module works anywhere.
WT_TASKS_DIR_DEFAULT="tasks"
task_for_branch() {
  local branch="$1" explicit="${2:-}" dir t root
  if [ -n "$explicit" ]; then
    printf '%s' "$explicit"
    return 0
  fi
  root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
  [ -n "$root" ] || return 0
  dir="$root/${WT_TASKS_DIR:-$WT_TASKS_DIR_DEFAULT}"
  [ -d "$dir" ] || return 0
  # Match the branch name in the task's frontmatter or body, and print the
  # file name, which is what a reader opens.
  t="$(grep -rlF -- "$branch" "$dir" 2>/dev/null | head -1)"
  [ -n "$t" ] && printf '%s' "$(basename "$t")"
  return 0
}

claim_commit() {
  local session="$1" harness="$2" role="$3" branch="$4"
  local supersedes="${5:-}" reason="${6:-}" task="${7:-}"
  local payload empty_tree
  payload="$(printf 'session: %s\nharness: %s\nrole: %s\nbranch: %s\nclaimed_at: %s\n' \
    "$session" "$harness" "$role" "$branch" "$(date -Iseconds)")"
  if [ -n "$task" ]; then
    payload="$(printf '%s\ntask: %s' "$payload" "$task")"
  fi
  # Only a forced takeover carries these, so an ordinary claim stays short
  # and the exceptions are visible as exceptions.
  if [ -n "$supersedes" ]; then
    payload="$(printf '%s\nsupersedes: %s\nreason: %s' "$payload" "$supersedes" "$reason")"
  fi
  empty_tree="$(git hash-object -t tree /dev/null)"
  # A claim is machine state, not a human commit, so it must not inherit the
  # user's identity requirement. Without this, `git commit-tree` fails on any
  # machine with no configured user.email -- a fresh container, a CI runner,
  # a bot account -- and the failure looks like a concurrency bug.
  printf '%s\n' "$payload" |
    GIT_AUTHOR_NAME="${GIT_AUTHOR_NAME:-wt-owners}" \
    GIT_AUTHOR_EMAIL="${GIT_AUTHOR_EMAIL:-wt-owners@localhost}" \
    GIT_COMMITTER_NAME="${GIT_COMMITTER_NAME:-wt-owners}" \
    GIT_COMMITTER_EMAIL="${GIT_COMMITTER_EMAIL:-wt-owners@localhost}" \
    git commit-tree "$empty_tree" -F -
}

read_claim() {
  local ref="$1"
  git cat-file -p "$ref" 2>/dev/null | sed -n '/^$/,$p' | sed '1d'
}

field() {
  printf '%s\n' "$1" | sed -n "s/^$2: *//p" | head -1
}

cmd_claim() {
  local branch="${1:-}" role="writer" session task_arg=""
  shift || true
  while [ $# -gt 0 ]; do
    case "$1" in
      --role) role="${2:-}"; shift 2 ;;
      --session) session="${2:-}"; shift 2 ;;
      --task) task_arg="${2:-}"; shift 2 ;;
      *) die "unknown argument: $1" ;;
    esac
  done
  session="${session:-$(session_id)}"
  [ -n "$branch" ] || die "usage: wt-owners claim <branch> [--role writer|reader]"
  [ -n "$session" ] || die "no session id: set OPENCODE_SESSION_ID or pass --session"

  local ref harness claim payload holder
  ref="$(ref_for "$branch")"
  harness="$(session_harness "$session")"
  claim="$(claim_commit "$session" "$harness" "$role" "$branch" "" "" "$(task_for_branch "$branch" "$task_arg")")"

  if git update-ref "$ref" "$claim" "" 2>/dev/null; then
    printf 'claimed %s as %s (%s)\n' "$branch" "$role" "$session"
    return 0
  fi

  # Contended. Re-read and decide.
  holder="$(read_claim "$ref")"
  local holder_session holder_harness holder_role
  holder_session="$(field "$holder" session)"
  holder_harness="$(field "$holder" harness)"
  holder_role="$(field "$holder" role)"

  if [ "$holder_session" = "$session" ]; then
    printf 'already claimed by this session (%s)\n' "$role"
    return 0
  fi

  # Readers never conflict with each other; only a writer blocks a writer.
  if [ "$role" = "reader" ] && [ "$holder_role" != "writer" ]; then
    printf 'reading %s alongside %s\n' "$branch" "$holder_session"
    return 0
  fi

  if session_is_live "$holder_session" "$holder_harness"; then
    printf 'held by %s (%s), which is still running\n' "$holder_session" "$holder_role" >&2
    return 1
  fi

  # The holder is gone. Reclaim: delete only if the value is still the one
  # we judged dead, then create. Two reclaimers both delete; one create wins.
  git update-ref -d "$ref" "$(git rev-parse "$ref")" 2>/dev/null || true
  if git update-ref "$ref" "$claim" "" 2>/dev/null; then
    printf 'reclaimed %s from dead session %s\n' "$branch" "$holder_session"
    return 0
  fi
  printf 'lost the reclaim race for %s\n' "$branch" >&2
  return 1
}

# A human's terminal, as opposed to an agent's tool call. Same test the
# commit guard uses: /dev/tty is readable but cannot be opened from a tool
# call, so a prompt there fails rather than hangs.
has_terminal() {
  { exec </dev/tty; } 2>/dev/null || return 1
  return 0
}

# An agent must never override the invariant that stops two writers. This is
# the one escape hatch in the module, so it is gated on the one signal an
# agent cannot forge from a tool call.
is_agent_session() {
  local marker
  for marker in AGENT AI_AGENT CLAUDE_CODE CURSOR_AGENT; do
    [ -n "${!marker:-}" ] && return 0
  done
  return 1
}

cmd_release() {
  local branch="${1:-}" session force=0 reason=""
  shift || true
  while [ $# -gt 0 ]; do
    case "$1" in
      --session) session="${2:-}"; shift 2 ;;
      --force) force=1; shift ;;
      --reason) reason="${2:-}"; shift 2 ;;
      *) die "unknown argument: $1" ;;
    esac
  done
  session="${session:-$(session_id)}"
  [ -n "$branch" ] || die "usage: wt-owners release <branch> [--force --reason TEXT]"

  local ref holder holder_session
  ref="$(ref_for "$branch")"
  git rev-parse --verify --quiet "$ref" >/dev/null || {
    printf 'no claim on %s\n' "$branch"
    return 0
  }
  holder="$(read_claim "$ref")"
  holder_session="$(field "$holder" session)"

  if [ "$holder_session" = "$session" ]; then
    git update-ref -d "$ref" "$(git rev-parse "$ref")"
    printf 'released %s\n' "$branch"
    return 0
  fi

  # Not ours. Taking it is an override, and overrides have conditions.
  if [ "$force" -ne 1 ]; then
    printf 'refusing to release %s: held by %s\n' "$branch" "$holder_session" >&2
    printf 'If that session is stuck, a human can override:\n' >&2
    printf '  wt-owners release %s --force --reason "why"\n' "$branch" >&2
    return 1
  fi

  # Liveness already covers a crashed session; --force exists for a session
  # that is ALIVE and stuck, which is a judgement only a person can make.
  if is_agent_session; then
    printf 'refusing --force from an agent session.\n' >&2
    printf 'An agent may never take write access from another session.\n' >&2
    printf 'A human must run this, and it needs a terminal.\n' >&2
    return 1
  fi
  if [ -z "$reason" ]; then
    printf 'refusing --force without --reason.\n' >&2
    printf 'An unreasoned override is indistinguishable from a bug later.\n' >&2
    return 1
  fi
  if ! has_terminal; then
    printf 'refusing --force without a terminal: nobody can confirm it.\n' >&2
    return 1
  fi

  # Record the takeover on the claim that replaces it, since a custom ref
  # gets no reflog to carry a message.
  local claim
  claim="$(claim_commit "$session" "$(session_harness "$session")" "writer" "$branch" \
    "$holder_session" "$reason" "$(task_for_branch "$branch")")"
  if git update-ref "$ref" "$claim" "$(git rev-parse "$ref")"; then
    printf 'took over %s from %s\n' "$branch" "$holder_session"
    printf 'reason: %s\n' "$reason"
    return 0
  fi
  printf 'the claim changed while we looked; nothing taken\n' >&2
  return 1
}

cmd_holder() {
  local branch="${1:-}"
  [ -n "$branch" ] || die "usage: wt-owners holder <branch>"
  local ref
  ref="$(ref_for "$branch")"
  git rev-parse --verify --quiet "$ref" >/dev/null || {
    printf 'none\n'
    return 0
  }
  read_claim "$ref"
}

cmd_check() {
  local branch="${1:-}" session
  shift || true
  while [ $# -gt 0 ]; do
    case "$1" in
      --session) session="${2:-}"; shift 2 ;;
      *) die "unknown argument: $1" ;;
    esac
  done
  session="${session:-$(session_id)}"
  [ -n "$branch" ] || die "usage: wt-owners check <branch>"

  local ref
  ref="$(ref_for "$branch")"
  # No claim at all: nothing to enforce. A guard that blocks unclaimed
  # branches would break every repository that has not adopted this.
  git rev-parse --verify --quiet "$ref" >/dev/null || exit 0

  local holder holder_session holder_harness holder_role
  holder="$(read_claim "$ref")"
  holder_session="$(field "$holder" session)"
  holder_harness="$(field "$holder" harness)"
  holder_role="$(field "$holder" role)"

  [ "$holder_session" = "$session" ] && exit 0
  [ "$holder_role" = "reader" ] && exit 0

  if session_is_live "$holder_session" "$holder_harness"; then
    printf 'branch %s is held by writer %s\n' "$branch" "$holder_session" >&2
    exit 1
  fi
  # Holder is dead: nobody is writing. Permitting is right; the claim will
  # be reclaimed on the next explicit `claim`.
  exit 0
}

main() {
  local cmd="${1:-}"
  shift || true
  case "$cmd" in
    claim) cmd_claim "$@" ;;
    release) cmd_release "$@" ;;
    holder) cmd_holder "$@" ;;
    check) cmd_check "$@" ;;
    *) die "usage: wt-owners {claim|release|holder|check} <branch>" ;;
  esac
}

main "$@"
