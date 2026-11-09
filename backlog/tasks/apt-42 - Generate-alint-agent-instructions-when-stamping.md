---
id: APT-42
title: Generate alint agent instructions when stamping
status: In Progress
created_date: 2026-11-09 23:22
labels:
- enforcement
- bug
updated_date: 2026-11-09 23:42
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The agentic layer carries .alint.yml and prek enforcement, but AGENTS.md does not include the generated alint block. The spec requires the block to be regenerated when alint rules change.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A fresh stamp with alint enabled contains the alint-generated AGENTS.md block.
- [x] #2 Updating the layer refreshes the block from the active .alint.yml without touching project-owned prose.
- [x] #3 A project without alint receives no generated alint block.
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
The stamp/update seam now calls alint export-agents-md --inline --output AGENTS.md through mise exec --yes github:asamarts/alint@latest, matching the stamped mise fragment. It does not require a global alint shim. The prek hook refreshes the block before checks. CI initially failed because the implementation still required a global shim; the generator now bootstraps through the declared tool instead. Full local suite: 114 passed; prek passed.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Focused tests and the full test suite pass.
- [x] #2 The new test fails before the implementation change.
<!-- DOD:END -->
