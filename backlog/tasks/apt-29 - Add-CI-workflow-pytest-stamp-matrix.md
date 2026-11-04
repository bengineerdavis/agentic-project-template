---
id: APT-29
title: Add CI workflow (pytest + stamp matrix)
status: To Do
created_date: 2026-11-04 19:58
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The repo has prek hooks but no CI: mise run test / test-template only run when someone remembers, so regressions the suite already catches (tripwire, merge logic) go unverified between local runs. Retro 2026-11-04 finding #1.

Ship:

- GitHub Actions workflow running pytest on every push/PR
- The workflow runs the stamp matrix (test-template) with a pinned TEMPLATE_STAMP_ROOT inside the runner workspace

Constraints:

- Workflow triggers on push to main and pull_request; no scheduled jobs
- Keep the workflow under ~40 lines; no third-party actions beyond checkout + setup-uv
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Workflow runs pytest and test-template on push to main and on pull_request, green on a clean checkout
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
