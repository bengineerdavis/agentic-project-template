---
id: APT-21
title: 'Unblock roborev reviews on this machine: opencode V1 cannot parse the V2 global
  config'
status: Done
created_date: 2026-10-18 23:08
updated_date: 2026-10-20 15:18
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Diagnosed 2026-10-18 via roborev check-agents: every background review fails because the opencode agent resolves to the mise-pinned V1 binary (1.18.32), which rejects the V2 permissions array in the global ~/.config/opencode/opencode.jsonc ('V2 permissions are not supported by OpenCode V1. Use V1 permission rules or run opencode2'). No opencode2 binary exists on PATH yet. The fast loop is wired (hooks, daemon, queue) but review execution fails before starting on this machine; the open-question note on apt-3 is this. Fix is the opencode-v2 migration (chezmoi dot_config/opencode + the opencode-v2 PLAN.md thread): ship or point roborev at a V2-capable opencode, or scope roborev's agent config away from the V2 global config. Until then the stamped fallback (mise roborev-status/roborev-fix + review-findings skill) is the only findings path, and reviews are not actually running.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A V2-capable opencode binary is installed and roborev check-agents passes for the opencode agent
- [x] #2 A fresh commit on a stamped project produces a completed roborev review, not a failed job
- [x] #3 The fix lands with the chezmoi opencode-v2 migration rather than as a hand edit to the live global config
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->

<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Cleared 2026-10-20. AC1: roborev check-agents passes for the opencode agent — it now resolves to http-opencode/2.0.32 (V2, served from opencode.ai because the registry's aqua backend 404s on V2 tags); codex still fails 401 (no OpenAI auth, agent not in use). AC2: fresh commit 7e07e72 produced a completed review (job 116, 7m30s) with 3 real findings, all fixed same-session: d5620c2 migrates the legacy bare registry pin on update (deep_merge never removes keys; verified in a sandbox that coexisting opencode + http:opencode keys resolve the stale V1 first), a962809 adds the version-url invariant to the stamp matrix, 12e46bb corrects the HANDOFF escape hatch (mise use with a bare string replaces the whole table entry; fixed URLs treat version as a label). AC3: global config is the chezmoi-deployed V2 shape; the pin landed as template commits, no hand edits. Fast loop is the primary findings path again; follow-up commits d5620c2/a962809/12e46bb were themselves reviewed concurrently (jobs 118-120).
<!-- SECTION:FINAL_SUMMARY:END -->
## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
