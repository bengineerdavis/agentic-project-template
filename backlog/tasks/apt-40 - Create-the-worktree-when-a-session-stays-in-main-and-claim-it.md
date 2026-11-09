---
id: APT-40
title: Create the worktree when a session stays in main, and claim it
status: To Do
created_date: 2026-11-09 01:00
labels:
- worktrees
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
APT-32 shipped the commit-time guard: it refuses an agent commit from the main
checkout. That is one half of the isolation guarantee. It catches the mistake
at the last possible moment, after the work exists in the wrong place.

The other half is remediation: when a session is working in the main checkout,
create the worktree it should have been in and move it there. The guard's
message already names the command (`wt switch --create <branch>`); this task is
about doing it rather than printing it.

Reading Worktrunk's source (2026-11-08) narrowed the work considerably:

- **Worktree creation is already covered** for OpenCode 2. The documented
  Worktrunk plugin registers a worktree strategy through OpenCode's worktree
  lifecycle hooks, routing creation and removal through `wt switch --create`
  and `wt remove`, so agent-created worktrees get the project's `worktree-path`
  and lifecycle hooks. Do not build this.
- **The ownership record is done.** `template/scripts/wt-owners.sh` (merged,
  PR #8) provides `claim`/`release`/`holder`/`check` over `refs/wt-owners/*`,
  with stale claims resolved by session liveness.

So what remains is the wiring between them: a session in the main checkout
gets told, gets moved, and its branch gets claimed — rather than being refused
at commit time with nothing else happening.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 An agent session working in the main checkout can be moved into a correctly named worktree without a human retyping `wt switch --create`.
- [ ] #2 The branch it lands on is claimed via `wt-owners claim`, so a second writer is refused by the guard already in place.
- [ ] #3 The mechanism is separable from the commit-time guard: disabling it leaves the guard's behaviour unchanged, and vice versa.
- [ ] #4 A repository that has adopted neither script is unaffected — no worktree is created and nothing blocks.
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Raised 2026-11-09 from the session that built the guard and the ownership
module. Mechanism 2 was named in APT-32's acceptance criteria as "a separate
change that can be reverted without touching mechanism 1"; no task existed for
it until now, so it would have died with that session.

The open design question, which the ownership module's author left explicitly
unresolved: should the claim be taken at claim-creation time (the new worktree
claims its own branch immediately) or lazily (the first commit takes it)? A
claim at creation is simpler and matches the invariant; a lazy claim avoids
holding a branch nobody is writing to yet.

Prerequisite for one route: verifying whether the OpenCode worktree strategy
fires on a session that *starts* in the main checkout, or only when the session
explicitly asks for a worktree. That is marked UNVERIFIED in
`copier-template-copier-template/docs/research/worktrunk-guard.md` and decides
whether this task needs to build the trigger at all.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 A session that starts in the main checkout ends up in a claimed worktree, with the guard still refusing anything that is not, and both behaviours independently revertible.
<!-- DOD:END -->
