---
id: APT-24
title: Backlog-friendly Matt Pocock workflow
status: To Do
created_date: 2026-10-26 18:35
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Matt Pocock's engineering skills assume a generic issue tracker. This layer already uses backlog-md-py. Ship the adapter between the two:

- `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `docs/agents/domain.md`
- an Agent skills block in `AGENTS.md`
- a `backlog-workflow` skill that detects `backlog/` and maps spec, tickets, claims, and decisions onto it

Keep the adapter small enough to upstream to mattpocock/skills later.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 `docs/agents/issue-tracker.md` names `backlog-py-mcp` and the spec/ticket/claim mapping
- [ ] #2 `AGENTS.md` links all three docs
- [ ] #3 the `backlog-workflow` skill exists, detects `backlog/`, and maps spec, tickets, claims, and decisions onto it
- [ ] #4 a stamped project gets the three `docs/agents` files, the skill, and the `AGENTS.md` references
- [ ] #5 stamp tests assert all of the above; `mise run test` and `mise run test-template` pass
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
