---
id: APT-47
title: Install shared workflow plugins in stamped projects
status: Done
created_date: 2026-11-12 04:40
assignee:
- opencode-dotagents-projection
updated_date: 2026-11-19 21:14
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Stamped projects need both a declaration and a real source refresh for reviewed shared workflow plugins. A missing projection can otherwise persist after an agentic update. Make source synchronization, refresh, and observable OpenCode projection durable; then propagate the validated update to stamped children. Keep tool source definitions in one composition mechanism shared with COPCAT-1 planning.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The public stamp declares the reviewed Matt Pocock plugin and requires an explicit refresh plus dotagents install in every bootstrap path.
- [x] #2 A real isolated stamped child refreshes and installs the plugin, projecting tdd, grilling, and writing-for-agents where the selected OpenCode scope expects them.
- [x] #3 Update propagation consumes the same composition path into an isolated real child and preserves its customizations; failures are not claimed as success.
- [x] #4 Documentation distinguishes project projection from native Claude/Codex activation and unsupported VS Code plugin output; the dotfiles client installer is named as the native-activation owner.
- [x] #5 Focused tests fail before implementation and pass afterward; suite and lint outcomes are reported exactly.
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
2026-11-17: Template CI is green after 0781de2 declared dotagents in the repository development harness. PR #17 mergeStateStatus=CLEAN. Child PR #3 passed its full Python matrix and pre-commit after the tomli fallback and repository Ruff style fix. Both remain draft for author review; no merges executed.
Owned scope for this wrap-up: commits 36dc1cf and 0781de2 on apt-47-dotagents-projection. No other session PR was merged. Parent is now merged; child CTCT-15 / PR #3 must be tested against this parent before its own merge.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Merged PR #17 as d8d3bf1561a5ebfca728cc6691ff9f3026d06ed5 on 2026-11-19 after reviewing the refresh-versus-pure-install contract. Fresh verification in the moved worktree: 115 tests passed, all prek hooks passed, stamp matrix passed. Rebuilt the stale moved venv before rerunning; no test was skipped or assumed green.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
