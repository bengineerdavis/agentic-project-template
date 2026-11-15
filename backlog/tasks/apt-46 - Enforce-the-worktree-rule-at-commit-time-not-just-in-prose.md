---
id: APT-32
title: Enforce the worktree rule at commit time, not just in prose
status: To Do
created_date: 2026-11-06 10:30
labels:
- enforcement
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The layer states the worktree rule twice already: `spec.md` § Behavior:
Isolation ("Task work SHALL happen in a worktree") and
`fragments/tools/worktrunk/agents.md` ("one worktree per task"). APT-14
documented the start/finish procedure and dogfooded it. None of that
prevents the failure it describes — a session that never leaves the main
checkout.

Observed 2026-11-06 in the dotfiles repo: a session read the rule, created
worktrees, used them as command targets (`workdir=…`) rather than as its
home, and did all its work from the main checkout for hours — including
committing, then reporting the worktree question answered "yes" when the
answer was no. Prose did not bind; a check would have.

Two mechanisms, landed separately so either can be reverted alone:

1. **Commit-time guard (prek hook)** — the binding one. Blocks a commit made
   from a main checkout when the process is an agent session.
2. **Session-start assertion** — the early-warning one. Reports at session
   start, before work begins.

Detection is mechanical, not heuristic: in a main checkout
`git rev-parse --git-dir` and `--git-common-dir` resolve to the same path;
in a worktree the git-dir is `<common>/worktrees/<name>`. Agent sessions are
identifiable by environment (`AGENT`, `AI_AGENT`, `CLAUDE_*`, `CURSOR_*`),
which is what keeps the guard from ever blocking the maintainer.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A prek hook blocks a commit from a main checkout when an agent-session environment variable is set, naming `wt switch --create` in the message.
- [ ] #2 The same hook permits: an agent session inside a worktree, any commit when no agent marker is set, and any commit outside a git repository.
- [ ] #3 The check is proven to decline AND to relent: a mutation that makes it always-block fails the permit tests, and one that makes it never-block fails the block tests.
- [ ] #4 The guard ships as `fragments/tools/worktrunk/prek.toml` so every stamped project gets it through the existing fragment merge, and the fragment is declared in `TOOL_FRAGMENT_ORDER`.
- [ ] #5 `--no-verify` remains a deliberate, visible escape: the hook does not try to defeat it.
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->

<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Mechanism 1 (commit-time guard) shipped, tested both directions, and mutation-proven; mechanism 2 (session-start assertion) is a separate change that can be reverted without touching mechanism 1.
<!-- DOD:END -->
