---
id: APT-43
title: Stamp structure and setup skills into the agentic layer
status: In Progress
created_date: 2026-11-10 00:33
labels:
- skills
updated_date: 2026-11-10 00:41
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Declare structure-authoring and aboyeur from bengineerdavis/ai-prompt-library in the stamped agents.toml, so dotagents installs the authored skills into every project. Keep the library as the authoring home.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 fresh stamps declare structure-authoring and aboyeur from the library
- [ ] #2 the real stamp test verifies both declarations and dotagents installation
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
2026-11-09: agentic-project-template draft PR #11. 114 tests passed, including a real prek hook run in a fresh Git-backed stamp. The simplified tests follow the meta-template decision-1: test the contract we own, not the dependency.

Integration verification: a fresh project must be a Git repository before dotagents resolves its own agents.toml rather than the parent worktree. With git init, three existing library skills install successfully. structure-authoring exists at ai-prompt-library PR #2 head 1acc258 but not yet on library main, so its fresh install fails until that PR merges. This acceptance criterion remains open; do not mark the task complete yet. CTCT-14 records the post-stamp repository-initialization workflow.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
