---
id: APT-49.1
title: Validate backlog task-record integrity at commit time
status: To Do
created_date: 2026-11-15 06:10
parent_task_id: APT-49
updated_date: 2026-11-15 06:10
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Backlog migrations can leave filename/frontmatter IDs inconsistent, duplicate IDs, unresolved dependencies, or task paths that disagree with status. The existing harness needs a deterministic record check so these failures do not enter stamped-project queues silently.

Ship:

- A deterministic backlog task-record integrity check for filename/frontmatter ID agreement, duplicate IDs, dependency resolution, and task-path/status consistency.
- Red-first template fixtures demonstrating each invalid record and a passing valid case.
- Integration with the existing prek/CI harness that rejects invalid records without blocking valid ones.

Constraints:

- Reuse the existing backlog-workflow adapter and harness; do not add another workflow framework.
- Verify claims about backlog-py doctor against the installed version before relying on them.
- Keep this task limited to record invariants; repository reconciliation, stacked-PR maintenance, and skill deployment have separate owners.
- Any new skill reference introduced by implementation is declared in agents.toml in the same change.

Agreed with the maintainer 2026-11-14: split the deterministic backlog-integrity deliverable from the APT-49 umbrella into a focused child task.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The integrity check detects filename/frontmatter ID mismatches, duplicate IDs, unresolved dependencies, and task-path/status mismatches
- [ ] #2 Red-first template fixtures demonstrate every failure plus a passing valid case
- [ ] #3 The existing prek/CI harness rejects invalid records without blocking valid ones
- [ ] #4 Installed backlog-py behavior is verified before any doctor coverage claim
- [ ] #5 backlog-py board shows APT-49.1 with its full description and acceptance criteria
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
