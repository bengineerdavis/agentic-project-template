---
id: APT-19
title: 'Report aube lock dir upstream: default to user space, not shared /tmp'
status: Done
created_date: 2026-10-16 19:28
updated_date: 2026-10-24 22:35
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
Issue filed 2026-10-24: jdx/mise#14946 (https://github.com/jdx/mise/issues/14946). Title: aube npm backend defaults its lock dir to shared /tmp/fslock - a root run poisons it for every user. Body carries the repro (sudo mise install of any npm: tool creates root-owned /tmp/fslock), evidence (/tmp on this machine never self-clears; the poisoned dir persisted for days), the verified user-side fix (~/.zshenv TMPDIR redirect), the finding that mise.toml [env] TMPDIR does not reach the auto-install phase, and the suggested defaults (XDG_CACHE_HOME/aube or XDG_RUNTIME_DIR/aube). No duplicates found in jdx/mise or jdx/aube before filing.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
