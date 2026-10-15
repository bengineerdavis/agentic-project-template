---
id: APT-14
title: Worktree-per-task workflow wired into tasking
status: Done
created_date: 2026-10-12 18:30
updated_date: 2026-10-15 08:44
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
Workflow doc stamped+tested (8843995); dogfood executed the full loop: wt switch --create with post-start fire, isolated work, wt merge with approval gate + pre-merge check (the approval prompt correctly stopped a non-interactive merge). Hook completion verified piecewise (dotagents shim OK, prek OK); full completion on this machine blocked by user-side skillet approval in global mise config (backlog apt-18).
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
