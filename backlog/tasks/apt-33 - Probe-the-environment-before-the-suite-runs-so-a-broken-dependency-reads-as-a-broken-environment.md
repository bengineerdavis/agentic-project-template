---
id: APT-33
title: Probe the environment before the suite runs, so a broken dependency reads as a broken environment
status: To Do
created_date: 2026-11-07 09:20
labels:
- testing
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A suite that fails because a service it depends on is not running is not a
failed test suite. It is a failing environment, and the two look identical in
the output: red tests, no hint which one you are looking at.

The telling case is the worktree guard (APT-32). Its subagent branch calls
`opencode api get` — an HTTP request inside a commit hook. When the daemon is
unreachable the guard fails closed and blocks the commit, which is the right
behaviour, but the failure reads like a policy violation when it is an
environment fault. The same shape recurs anywhere a test needs a daemon, a
server, a socket, or a binary that the machine may or may not have running.

This is a grey area and the maintainer's framing is deliberately loose: what
is needed is fast feedback that the environment is broken, before the suite
spends its time testing code that was never reached. The treatment is
case-by-case; the durable part is the habit of asking whether a given failure
is a code fault or an environment fault, and surfacing it loudly when it is
the latter.

Two candidate shapes, neither chosen:

1. A pre-flight probe at session or suite start: cheapest conceivable check
   per dependency (socket open, process present, version answers), reported as
   an environment verdict rather than a test result.
2. A distinguished failure class in the suite itself: when a prerequisite is
   missing, fail with a message naming the environment, never a bare
   assertion.

A pre-flight probe that silently passes when it cannot determine the answer
would repeat the defect it exists to catch, so whichever shape lands must be
mutation-proven in both directions.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A dependency that is down is reported as an environment fault, in words that distinguish it from a failing test.
- [ ] #2 The check is proven to decline AND to relent: removing the dependency fails it with the environment message, restoring the dependency passes it.
- [ ] #3 The guard's `opencode api get` call is covered by whichever shape is chosen, since it is the case that motivated this.
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Raised 2026-11-07 from the retro on the worktree-guard session. Maintainer
note: "we should fail a test suite early before the suite starts running to
make sure prerequisite conditions like the daemon/server we depend on or a
service is running, as that's not a failed test suite, but a failing
environment -- this is a grey area ... we'll have to address this on a
case-by-case basis".

The general instruction that survives regardless of implementation: when a
failure might be environmental, surface it as a question and bring it up
loudly rather than silently attributing it to the code.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 At least the motivating case (the guard's API call) distinguishes environment from policy in its output, with the distinction mutation-proven.
<!-- DOD:END -->
