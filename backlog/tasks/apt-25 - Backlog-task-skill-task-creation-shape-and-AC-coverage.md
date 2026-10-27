---
id: APT-25
title: 'Backlog-task skill: task-creation shape and AC coverage'
status: Done
created_date: 2026-10-27 05:20
updated_date: 2026-10-27 06:23
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
- [x] #1 `backlog-task` skill exists in `bengineerdavis/ai-prompt-library`; its SKILL.md carries the description shape (why, Ship, Constraints, decision record), the AC-coverage rule, and the repo rules (agents.toml declaration, mise task naming, ambiguity marked)
- [x] #2 `agents.toml` here declares the skill and the dotagents project install (`npx -y @sentry/dotagents@latest --project install`) installs it
- [x] #3 a task created through the skill parses in `task_board` and carries one AC per Ship bullet
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Skill authored through the skillet flow in ai-prompt-library: spec.md (6 behaviors, 3 constraints) written from the session draft, SKILL.md rendered from the validated spec (spec_hash 355b7ec32838); validate green; no evals (not requested). Committed there as 4a0027b and pushed (0f7b7dc..4a0027b) — dotagents resolves the source from GitHub, so push precedes install. Declared in agents.toml here; installed with npx -y @sentry/dotagents@latest --project install (2 skills: commit-hygiene, backlog-task). This repo has no dotagents-install mise task — that name belongs to the stamped layer fragment; the project-scope CLI is the install path here. AC3 verified by demo: APT-26 created through the skill process (CLI, shape, one AC per Ship bullet), confirmed on task_board, then its file deleted — never committed.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
The backlog-task skill ships in ai-prompt-library (spec + SKILL.md, skillet-valid) and is declared and installed here. Task creation now has a scaffold: the why/Ship/Constraints shape, one AC per Ship bullet, single done source, marker-frame preservation. First real use is the next task created in this repo (dogfood clause in the description).
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
