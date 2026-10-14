---
id: APT-14
title: Worktree-per-task workflow wired into tasking
status: In Progress
created_date: 2026-10-12 18:30
updated_date: 2026-10-14 14:19
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
One worktree per backlog task: starting APT-N creates/switches wt named from the task id; work happens isolated; loops run there; done means merged and cleaned. Dogfood target: execute APT-9 (LSP design) inside its own worktree using this workflow.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Start-task procedure documented in stamped .context (or a stamped skill if it earns one)
- [ ] #2 Finish-task procedure documented (merge, status update, cleanup)
- [ ] #3 APT-9 demonstrably executed inside its own worktree via this workflow
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->

<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
