---
id: APT-13
title: Stamp worktrunk wiring into projects
status: Done
created_date: 2026-10-12 18:30
updated_date: 2026-10-14 14:19
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Layer stamps wt: mise tool pin, worktrunk config (post-create hook: mise run install), .context docs for the per-task workflow, ai-rules rule.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Fresh stamp: wt switch <task-branch> works and post-create hook runs mise install
- [ ] #2 Config merge never clobbers an existing worktrunk config
- [ ] #3 Stamp matrix asserts the wiring
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Merged 23f8862: wt pin + .config/wt.toml merge (never-clobber tested), dogfood config adopted, e2e smoke passed (worktree at .worktrees/<branch> per user config; post-start hook fired). Squash pin lives in chezmoi user config (wt scopes merge policy at user level) — user config written to chezmoi source and applied. Hook full completion left to real use (apt-14).
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
