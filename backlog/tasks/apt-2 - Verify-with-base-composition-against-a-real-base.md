---
id: APT-2
title: Verify with-base composition against a real base
status: Done
created_date: 2026-10-12 18:19
updated_date: 2026-10-18 23:04
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The smoke test uses this template as its own base, so both stamps share one answers filename. Blocked by: a real base template existing (python-project-template).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Stamp against a base with the default answers name leaves both .copier-answers.yml and .agentic-answers.yml committed
- [ ] #2 Both layers independently copier-update-able
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Verified on the redge composition 2026-10-18 (first real with-base stamp): base-then-layer leaves .copier-answers.yml and .agentic-answers.yml side by side; each answers file carries its own template commit so each layer re-renders independently (the layer CLI update path re-renders layer answers only, then fragment merges; base updates through its own answers file). Stamp matrix green (21 tests).
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
