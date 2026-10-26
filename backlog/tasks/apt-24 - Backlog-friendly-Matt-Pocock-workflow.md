---
id: APT-24
title: Backlog-friendly Matt Pocock workflow
status: To Do
created_date: 2026-10-26 18:35
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Matt Pocock's engineering skills assume a generic issue tracker. This layer already uses backlog-md-py, so ship the adapter: docs/agents/{issue-tracker,triage-labels,domain}.md, an Agent skills block in AGENTS.md, and a backlog-workflow skill that detects backlog/ and maps spec, tickets, claims and decisions onto it. Keep it small enough to upstream to mattpocock/skills later.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 docs/agents/issue-tracker.md names backlog-py-mcp and the spec/ticket/claim mapping
- [ ] #2 AGENTS.md links all three docs
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->

<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 A stamped project gets the three docs/agents files and the backlog-workflow skill; AGENTS.md references them; stamp tests assert it; mise run test and mise run test-template pass.
<!-- DOD:END -->
