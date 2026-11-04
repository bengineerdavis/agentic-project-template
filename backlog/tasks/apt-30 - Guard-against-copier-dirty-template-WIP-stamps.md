---
id: APT-30
title: Guard against copier dirty-template WIP stamps
status: To Do
created_date: 2026-11-04 19:58
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Uncommitted template edits make copier record an ephemeral WIP-commit SHA from a temporary clone into the stamped .agentic-answers.yml (_commit); every later update fails with 'pathspec did not match' until hand-repaired. Hit twice in the apt-22 session (d12d740, 8b1cce4). Retro 2026-11-04 finding #2.

Ship:

- test-template asserts, after its update scenario, that the recorded _commit resolves via git cat-file -e (fails when the dirty-template trap fired)

Constraints:

- The check lives inside the stamp-matrix task, not a separate manual step
- Keep the failure message naming the trap ('dirty template produced an ephemeral WIP SHA; commit template work before stamping')
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 test-template's update scenario asserts the stamped _commit resolves (git cat-file -e) and names the dirty-template trap in its failure output
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
