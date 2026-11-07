---
id: APT-35
title: Ruff in prek (F821 catches undefined names)
status: To Do
created_date: 2026-11-07 21:49
dependencies:
- APT-37
updated_date: 2026-11-07 21:50
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Retro 2026-11-07 Fix B. Add ruff to prek so the undefined-name class (Path NameError, f60a9cf) is caught at commit time on ANY interpreter. Ruff is base-owned (ARCHITECTURE.md:157): work lands as a branch in ../python-project-template, merges there, then the layer consumes it. Blocked by APT-36 (template update merge).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 prek config includes ruff with pyflakes rules incl F821
- [ ] #2 Depends on python-project-template ruff merge (APT-36)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Correction: blocked by APT-37 (python-project-template ruff adoption + update merge), not APT-36. Dependency edge already set correctly via --dep.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
