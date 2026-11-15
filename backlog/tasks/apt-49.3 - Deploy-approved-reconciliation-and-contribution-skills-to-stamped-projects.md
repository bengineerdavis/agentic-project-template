---
id: APT-49.3
title: Deploy approved reconciliation and contribution skills to stamped projects
status: To Do
created_date: 2026-11-15 06:10
parent_task_id: APT-49
references:
- https://github.com/bengineerdavis/ai-prompt-library/blob/main/backlog/tasks/apl-26%20-%20Create-a-reusable-reconcile-and-workflow-routing-skill.md
- https://github.com/bengineerdavis/ai-prompt-library/blob/main/backlog/tasks/apl-27%20-%20Prepare-upstream-conformant-contribution-candidates.md
updated_date: 2026-11-15 06:10
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The library’s reconciliation/routing and contribution-candidate skills need an opt-in deployment path into maintained and newly stamped projects once their authored components are approved. Template deployment is distinct from library skill authoring.

Ship:

- An opt-in installation design for the approved reconciliation/routing and contribution-candidate skills in stamped projects.
- agents.toml declarations for the new skill references in the implementation change.
- Isolated stamp-matrix verification covering both maintained and newly stamped projects.

Constraints:

- APL-26 and APL-27 in ai-prompt-library own the skill content; this task does not author or modify those skills. Start only after those components are approved.
- Reuse the existing backlog-workflow adapter and installation harness rather than adding another workflow system.
- Do not block copier-cat’s first usable assembly workflow.
- Preserve other sessions’ edits and keep template changes separately reviewed and approved.

Agreed with the maintainer 2026-11-14: split the template skill-deployment deliverable from the APT-49 umbrella into a focused child task.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The opt-in deployment design covers approved reconciliation/routing and contribution-candidate skills for maintained and newly stamped projects
- [ ] #2 agents.toml declares the new skill references in the same implementation change
- [ ] #3 Isolated stamp-matrix verification covers maintained existing projects and new stamps
- [ ] #4 The task references APL-26 and APL-27 as its external skill-content prerequisites and does not duplicate skill authoring
- [ ] #5 backlog-py board shows APT-49.3 with its full description and acceptance criteria
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
