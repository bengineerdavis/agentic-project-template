---
id: APT-10
title: Stamp opencode LSP wiring (python + alint lsp)
status: To Do
created_date: 2026-10-12 18:26
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Wire LSP into stamped projects: python language server via mise pin, alint lsp as stdio server so structure diagnostics reach agents.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Python LSP server pinned in the layer mise fragment and available in stamped projects
- [ ] #2 opencode.json carries the lsp section via merge (existing project configs never clobbered)
- [ ] #3 alint lsp wired and serves diagnostics
- [ ] #4 Smoke: an agent session sees a planted type error and an alint finding as diagnostics
- [ ] #5 Stamp matrix asserts the merge
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
