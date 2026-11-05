---
id: APT-32
title: Keep task branches synchronized with main
status: To Do
created_date: 2026-11-05 18:27
orchestration:
  status_key: inprogress
  lease_owner: opencode-branch-sync
  lease_expires_at: '2026-11-05T19:28:42.575656Z'
  version: 1
updated_date: 2026-11-05 18:52
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Start every new worktree from a fetched, fast-forwarded default branch; update same-repository PR branches using the native clean merge API after pushes and on a regular pulse. Fail closed on dirty local main, conflicts, missing forge capabilities, or concurrent updates. Do not rewrite history or execute PR code.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Document the portable start and sync contract and the GitHub adapter boundary
- [x] #2 Stamp a fresh-base helper and a tested branch-sync workflow
- [x] #3 Run on main pushes and every 15 minutes with expected-head protection and explicit failure reporting
- [ ] #4 Publish a draft PR for review without enabling the workflow on main
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Draft published 2026-11-05: agentic-project-template PR #4; dotfiles adoption PR #131. Local fresh-base behavior verified through real Worktrunk creation; dirty/diverged main fails closed. 66 template tests and 11 dotfiles focused tests pass; actionlint passes. Live dotfiles dry-run identified six behind PRs and sent no updates. GitHub allow_update_branch enabled for template, dotfiles, and loreai. PR #4 remains unmerged; no workflow is active from these drafts.
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
event_id: run-ff1f5cf37f63431d88c9f42289b4621e
type: claim_task
actor: opencode-branch-sync
timestamp: '2026-11-05T18:28:42.575739Z'
result: succeeded
task_id: APT-32
from_status: todo
to_status: inprogress
metadata:
  lease_ttl_seconds: '3600'
```
Implement the fresh-base contract and decentralized GitHub clean-merge pulse in a fresh worktree.
<!-- RUN_HISTORY_ENTRY:END -->
<!-- SECTION:RUN_HISTORY:END -->
