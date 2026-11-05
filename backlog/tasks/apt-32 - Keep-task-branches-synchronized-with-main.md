---
id: APT-32
title: Keep task branches synchronized with main
status: To Do
created_date: 2026-11-05 18:27
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Start every new worktree from a fetched, fast-forwarded default branch; update same-repository PR branches using the native clean merge API after pushes and on a regular pulse. Fail closed on dirty local main, conflicts, missing forge capabilities, or concurrent updates. Do not rewrite history or execute PR code.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Document the portable start and sync contract and the GitHub adapter boundary
- [ ] #2 Stamp a fresh-base helper and a tested branch-sync workflow
- [ ] #3 Run on main pushes and every 15 minutes with expected-head protection and explicit failure reporting
- [ ] #4 Publish a draft PR for review without enabling the workflow on main
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
