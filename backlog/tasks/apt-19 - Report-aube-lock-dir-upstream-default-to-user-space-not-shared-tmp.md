---
id: APT-19
title: 'Report aube lock dir upstream: default to user space, not shared /tmp'
status: To Do
created_date: 2026-10-16 19:28
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
aube (mise npm backend) derives its lock dir from TMPDIR and defaults to /tmp/fslock — shared, first-user-wins, poisoned by any root run, and /tmp persists on root-fs machines. Correct default: $XDG_CACHE_HOME/aube or $XDG_RUNTIME_DIR (per-user, per-boot). Repro + evidence in agentic-project-template HANDOFF (zshenv TMPDIR redirect verified as user-side fix; [env] TMPDIR does NOT reach mise's auto-install phase — upstream should fix the default, not rely on env). File at github.com/jdx/mise/issues.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Issue filed with repro, evidence, and suggested default
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
