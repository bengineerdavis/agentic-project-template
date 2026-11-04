---
id: APT-31
title: 'Commit wrapper: retry once after formatter restage'
status: To Do
created_date: 2026-11-04 19:58
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
tombi-format modifies files during git commit (redge hits: 3+ during apt-22), aborting the commit and forcing a manual restage-and-recommit loop every time. Retro 2026-11-04 finding #3.

Ship:

- A mise task in the layer repo that runs the prek hook pass, stages any files the hooks reformatted, and retries the commit once — the agent calls one command instead of looping

Constraints:

- mise task names cannot contain colons (repo rule) — name it commit-safe or similar
- Only one retry; a second formatting failure surfaces to the caller as an error
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Committing through the task lands a commit that needed tombi reformatting, without a manual restage loop (single retry)
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
