---
id: APT-39
title: Tombi performance investigation
status: In Progress
created_date: 2026-11-07 21:49
updated_date: 2026-11-08 17:59
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
Findings (Nov 8, measured in scratch worktree at 69d68c7): tombi EXONERATED for warm runs — full prek 0.38s, tombi-format 0.30s, commits 0.29-0.39s even with .toml staged. Roborev v4 post-commit hook ALSO fires in worktrees now (scratch commits got jobs 500/501 instantly) — the old worktree-blindness gotcha is obsolete. Historical 120s timeouts NOT reproducible; leading unverified hypothesis: daemon down/draining at the time (daemon_state shutdown_draining was set 2026-11-05). Recommendation: KEEP tombi-format on commit; on timeout check git log before re-running. Full evidence: docs/research/tombi-performance.md
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
