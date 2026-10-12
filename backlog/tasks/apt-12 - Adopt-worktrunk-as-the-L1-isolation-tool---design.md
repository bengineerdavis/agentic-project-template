---
id: APT-12
title: Adopt worktrunk as the L1 isolation tool - design
status: In Progress
created_date: 2026-10-12 18:30
updated_date: 2026-10-12 21:37
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
max-sixty/worktrunk (wt): branch-as-identifier worktree management, post-create hooks, copy-on-write caches; built for parallel agent workflows. Design: config location (project-committed vs user), post-create hook running mise install, branch naming derived from backlog task ids (apt-N), loop behavior inside worktrees (roborev reviews commits there), how the layer stamps it (mise pin + config), mise backend probe (registry > aqua: > github:).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Design recorded in ARCHITECTURE.md L1 with concern stated
- [ ] #2 Spec L1 behavior/open question resolved in the same change
- [ ] #3 Mise backend for wt probed and pinned or the gap recorded
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
assigned to branch apt-12-worktrunk-design
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
