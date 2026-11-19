---
id: APT-57
title: Verify stale worktree environments before declaring tests blocked
status: To Do
created_date: 2026-11-19 21:01
labels:
- testing
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Retro 2026-11-19 follow-up. After a repository or worktree moves, inspect and rebuild stale .venv shebangs before reporting tests unrun. Probe mise trust at the new path rather than bypassing it. Capture this as a reusable preflight check without building a general environment framework.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A synthetic moved worktree with stale venv shebangs is rebuilt and its focused suite runs, proving the environment rather than product code was the blocker.
- [ ] #2 The probe reports an untrusted moved mise config clearly and does not alter global trust or bypass the gate.
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Session evidence: repository moved from code/templates to code/personal/templates; registered worktrees initially appeared missing. Main has foreign mise.toml and opencode.json changes that must not be used to manufacture a passing test. Scope: preflight behavior only, not a broad environment refactor.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
