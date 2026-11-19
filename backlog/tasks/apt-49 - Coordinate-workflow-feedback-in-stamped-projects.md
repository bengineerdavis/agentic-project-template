---
id: APT-49
title: Coordinate workflow feedback in stamped projects
status: To Do
created_date: 2026-11-14 18:55
dependencies:
- APT-32
updated_date: 2026-11-15 06:11
references:
- ../copier-cat/backlog/tasks/ccc-20 - Validate-task-record-integrity-at-commit-time.md
- ../copier-cat/backlog/tasks/ccc-21 - Make-contribution-candidates-follow-upstream-contributor-conventions.md
- ../personal/ai-prompt-library/backlog/tasks/apl-26 - Create-a-reusable-reconcile-and-workflow-routing-skill.md
- ../personal/ai-prompt-library/backlog/tasks/apl-27 - Prepare-upstream-conformant-contribution-candidates.md
orchestration:
  version: 1
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The agentic layer owns the backlog workflow adapter, skill declarations, and harness stamped into maintained and new projects. Copier-cat’s migration and workflow sessions exposed missing record guards and fragile contribution and branch-reconciliation practices that should return through this layer’s established task and stamp-test process.

Ship:

- Coordination of the focused child tasks APT-49.1, APT-49.2, and APT-49.3 against the existing backlog-workflow adapter and harness.

Constraints:

- APT-49.1 owns deterministic backlog-record integrity; APT-49.2 owns safe stacked-PR reconciliation and the MVP/exploration boundary; APT-49.3 owns deployment of approved library skills.
- Parent main divergence and the APT-32 collision remain with their existing owners, not this integration record.
- Preserve established work and other sessions’ dirty files. Reuse the existing backlog-workflow adapter and harness rather than adding another workflow system.
- Deterministic record violations belong in a commit-time or CI check; judgement-only workflow rules remain review guidance.
- Keep library skill authoring separate from stamped deployment and do not block copier-cat’s first usable assembly workflow.
- Contributor conventions govern every external communication; publication and source-template modifications require separate approval.
- Every new skill reference is declared in agents.toml in the same implementation change.

Agreed with the maintainer 2026-11-14: retain the original workflow-feedback rationale as integration context while the implementation graph carries its focused deliverables.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #5 The integration record links APT-49.1, APT-49.2, and APT-49.3 and preserves their scope boundaries and external owners
- [ ] #2 The integration record links APT-49.1, APT-49.2, and APT-49.3 and preserves their scope boundaries and external owners
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Original umbrella rationale preserved: return backlog-integrity, reconciliation, workflow-boundary, and upstream-contribution lessons to the parent agentic template so subprojects inherit them. The original broad deliverables were repository/task reconciliation, red-first integrity tests, reconciliation/contribution planning, and skill deployment. Repository reconciliation and APT-32 conflict resolution were deliberately excluded from the focused tasks because they already have owners.

Native split performed with backlog-py orchestration split --mode child. Temporary top-level APT-42–44 records were removed before publication because this checkout already contains established tasks with those IDs; the generated APT-49.1–3 child records are the authoritative focused tasks. Cross-repository APL-26/27 prerequisites are references in APT-49.3, not invalid native dependency IDs.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->

## Run History
<!-- SECTION:RUN_HISTORY:BEGIN -->
<!-- RUN_HISTORY_ENTRY:BEGIN -->
```yaml
event_id: run-1ccf13e2c93e471f931cdf6b286bda1a
type: split_task
actor: OpenCode
timestamp: '2026-11-15T06:10:31.071785Z'
result: succeeded
task_id: APT-49
split_mode: child
metadata:
  created_task_ids: '["APT-49.1","APT-49.2","APT-49.3"]'
  inherit_dependencies: 'false'
  link_sequence: 'true'
  split_items_count: '3'
  split_items_hash: c2a960ee3773a16a7b04d9daa9f6a36d7633c7dc27bd77f9e33e0e051a5008fb
  transition_to_status: ''
```
Replace the umbrella deliverables with focused implementation tasks while retaining APT-49 as integration context
<!-- RUN_HISTORY_ENTRY:END -->
<!-- SECTION:RUN_HISTORY:END -->
