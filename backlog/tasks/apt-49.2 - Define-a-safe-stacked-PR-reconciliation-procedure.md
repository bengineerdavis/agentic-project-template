---
id: APT-49.2
title: Define a safe stacked-PR reconciliation procedure
status: To Do
created_date: 2026-11-15 06:10
parent_task_id: APT-49
updated_date: 2026-11-15 06:10
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Session work produced stacked PRs, divergent branches, and duplicate migration commits that require semantic reconciliation rather than mechanical force-updates. The template needs a reusable procedure that preserves established work while making each resulting PR reviewable.

Ship:

- A documented stacked-PR reconciliation procedure covering base/branch synchronization, semantic supersession, aggregate-diff verification, and preservation of unmerged evidence.
- A worked example demonstrating a replacement PR without losing work.
- Guidance that keeps the small MVP contract beside exploration notes and classifies new ideas as usage-blocking or deferred before entering the active milestone.

Constraints:

- Reuse the existing backlog-workflow adapter and its durable tracker conventions; do not invent another tracker system.
- Preserve other sessions’ edits, worktrees, and unpushed commits; this procedure does not authorize resolving their current conflicts.
- Use existing Git tooling and review guidance rather than a new orchestration framework.
- Keep library skill authoring in APL-26 and APL-27; this task owns only the reusable reconciliation procedure and references to it.
- Any new skill reference introduced by implementation is declared in agents.toml in the same change.

Agreed with the maintainer 2026-11-14: split the reconciliation and workflow-boundary deliverable from the APT-49 umbrella into a focused child task.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The procedure covers base/branch synchronization, semantic supersession, aggregate-diff verification, and preservation of unmerged evidence
- [ ] #2 A worked example demonstrates a replacement PR without losing established work
- [ ] #3 The guidance includes the MVP/exploration boundary and applies the existing tracker adapter rather than inventing a new system
- [ ] #4 The plan references APL-26 for reusable reconciliation/routing and APL-27 for upstream-conformant contribution candidates without claiming to author those skills
- [ ] #5 backlog-py board shows APT-49.2 with its full description and acceptance criteria
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
