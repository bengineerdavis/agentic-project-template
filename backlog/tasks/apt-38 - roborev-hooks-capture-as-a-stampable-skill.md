---
id: APT-38
title: 'roborev hooks: capture as a stampable skill'
status: In Progress
created_date: 2026-11-07 21:49
updated_date: 2026-11-08 18:03
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Retro/wayfinder item 3. Work with roborev to pin down its hooks and rules (post-commit firing, worktree blindness finding from 2026-11-07: branch commits got zero reviews). Capture the operating knowledge as a skill stamped projects can utilize via the agentic template. Links to APT-26 (stamp roborev wiring into projects).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Hook/rule mechanics documented from primary sources
- [ ] #2 Skill exists in fragments/dotagents installable by stamped projects
- [ ] #3 Worktree fast-loop gap is addressed or explicitly scoped out
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Research COMPLETE (Nov 8, docs/research/roborev-hooks.md, primary evidence: roborev 0.74.0 CLI + doctor + post-commit.log + hooks on disk). MAJOR PREMISE CORRECTIONS: (1) worktree blindness OBSOLETE — v4 post-commit fires in worktrees, verified via scratch commits + chezmoi worktree rows; (2) sole real failure in 7d was post-commit LOCK timeout when daemon busy/down — not hook logic; (3) roborev init already stamps hooks in stamped projects via fragments/mise-layer.toml — what's missing is the SKILL and REVIEW.md seeding. Skill contract: wrap 6 verbs (status/fix/close/comment/log/doctor) + REVIEW.md seeding. Open Qs for maintainer: seed REVIEW.md at stamp time? drop worktree scope from APT-26 (recommend yes)?
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
