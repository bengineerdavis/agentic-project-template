---
id: APT-21
title: 'Unblock roborev reviews on this machine: opencode V1 cannot parse the V2 global
  config'
status: To Do
created_date: 2026-10-18 23:08
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Diagnosed 2026-10-18 via roborev check-agents: every background review fails because the opencode agent resolves to the mise-pinned V1 binary (1.18.32), which rejects the V2 permissions array in the global ~/.config/opencode/opencode.jsonc ('V2 permissions are not supported by OpenCode V1. Use V1 permission rules or run opencode2'). No opencode2 binary exists on PATH yet. The fast loop is wired (hooks, daemon, queue) but review execution fails before starting on this machine; the open-question note on apt-3 is this. Fix is the opencode-v2 migration (chezmoi dot_config/opencode + the opencode-v2 PLAN.md thread): ship or point roborev at a V2-capable opencode, or scope roborev's agent config away from the V2 global config. Until then the stamped fallback (mise roborev-status/roborev-fix + review-findings skill) is the only findings path, and reviews are not actually running.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A V2-capable opencode binary is installed and roborev check-agents passes for the opencode agent
- [ ] #2 A fresh commit on a stamped project produces a completed roborev review, not a failed job
- [ ] #3 The fix lands with the chezmoi opencode-v2 migration rather than as a hand edit to the live global config
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
