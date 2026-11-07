---
id: APT-39
title: Tombi performance investigation
status: To Do
created_date: 2026-11-07 21:49
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Retro/wayfinder item 4. Understand why tombi-format is slow locally (commit hooks exceeding the 120s tool timeout while completing). We should NOT have to give up format-on-save/format-on-commit. Measure wall-time per hook, isolate tombi's cost (cold start? server? file glob?), find the fix. Findings + decisions pushed back to the maintainer here.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Measured breakdown of prek hook wall-time (per hook)
- [ ] #2 Root cause identified with evidence
- [ ] #3 Fix decided or trade-off documented
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
