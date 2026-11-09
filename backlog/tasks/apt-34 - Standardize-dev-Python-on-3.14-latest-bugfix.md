---
id: APT-34
title: Standardize dev Python on 3.14 latest bugfix
status: In Progress
created_date: 2026-11-07 21:49
updated_date: 2026-11-09 04:15
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Retro 2026-11-07 Fix A (amended by maintainer: standardize on 3.14 latest bugfix, not 3.12). Align mise.toml [tools] python, .python-version, and CI UV_PYTHON on 3.14 so dev venv, stamp matrix, and runner resolve the same interpreter. Context: 3.14 deferred annotation evaluation hid the Path NameError that CI's 3.12 caught (f60a9cf).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Dev venv, stamp matrix, and CI all resolve the same 3.14 bugfix version
- [ ] #2 Full suite and stamp matrix green under the aligned pin
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Agreed with the maintainer (Nov 8 2026): floating pin — mise [tools] python = "3.14", .python-version = 3.14, CI python-version 3.14; mise/uv resolve the latest 3.14 bugfix. NOT 3.12, NOT exact-bugfix pinning.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
