---
id: APT-25
title: 'Backlog-task skill: task-creation shape and AC coverage'
status: To Do
created_date: 2026-10-27 05:20
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Task descriptions keep failing two ways: a dense single paragraph buries the deliverables, and the done-definition drifts (deliverables in prose, ACs under-scoped, DOD duplicating ACs). APT-22 and APT-24 were fixed by hand on 2026-10-26. The fix should not depend on remembering it.

Ship:

- a `backlog-task` skill in `bengineerdavis/ai-prompt-library` that runs on task create and edit: it hands over the fill-in shape (why, Ship, Constraints, decision record), checks that every Ship bullet has an acceptance criterion, applies plain-english, and carries the repo rules (agents.toml skill declaration, mise task naming, ambiguity marked)
- the skill declared in `agents.toml` here, in the same change that first references it
- dogfood: the first task created after the skill lands uses the shape

Constraints:

- the skill lives in `ai-prompt-library` so dotagents can pin it
- the backlog-md-py marker structure is the contract: the skill edits prose inside the markers, never the frame
- plain-english and writing-for-agents are the writing standards; no new standard is invented here

Agreed with the maintainer 2026-10-26: shape-first over tooling. The vale prose lane in ARCHITECTURE.md stays future until the skill proves insufficient.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 `backlog-task` skill exists in `bengineerdavis/ai-prompt-library`; its SKILL.md carries the description shape (why, Ship, Constraints, decision record), the AC-coverage rule, and the repo rules (agents.toml declaration, mise task naming, ambiguity marked)
- [ ] #2 `agents.toml` here declares the skill and `mise run dotagents-install` installs it
- [ ] #3 a task created through the skill parses in `task_board` and carries one AC per Ship bullet
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
