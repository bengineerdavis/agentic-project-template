---
id: APT-54
title: Reconcile stale local task records and duplicate IDs
status: Done
created_date: 2026-11-16 01:04
updated_date: 2026-11-16 01:10
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Why: the shared main checkout is behind origin/main and contains stale or edited task files whose IDs shadow canonical records. Backlog warnings hide one record for APT-32, APT-49, APT-50, and APT-51, so queue and dependency reads are not trustworthy there.

Ship:
- Preserve the other session's APT-46 edit and unrelated dirty files before reconciling the shared checkout.
- Compare each stale local record with the canonical origin/main record, retaining unique evidence or explicitly recording semantic supersession.
- Reconcile the shared main checkout with origin/main through its owning workstream, then verify Backlog resolves one record per ID without duplicate warnings.
- Record the outcome and remaining ownership in this task; keep the deterministic prevention guard in APT-49.1.

Constraints:
- Do not discard, stash, or commit another session's edits.
- Do not merge or close APT-32, APT-46, or their PRs as part of this bookkeeping cleanup.
- Use backlog-py for task mutations and verify the installed behavior rather than assuming doctor detects duplicates.
- Canonical records on origin/main are the baseline; preserve any unique local evidence before removal.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The shared main checkout resolves exactly one record for each task ID without duplicate-ID warnings
- [x] #2 Every superseded local record is compared with its canonical record and unique evidence is preserved
- [x] #3 Other sessions’ APT-46 and unrelated working-tree changes remain intact or explicitly owned through a preservation handoff
- [x] #4 The reconciliation outcome and remaining owners are recorded through backlog-py
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Evidence compared 2026-11-15 against origin/main at 5206723.

- APT-32: local apt-46 file has frontmatter id APT-32, so it shadows the canonical branch-sync task. Its body is the distinct APT-46 worktree-enforcement task. Preserve the edited file and its ownership; do not resolve by renaming or deleting the other session's edit. APT-52 owns the related first-commit initialization defect.
- APT-49: local Adopt-upstream-conformant... is the pre-split umbrella. Canonical Coordinate-workflow-feedback... supersedes it with focused children APT-49.1/2/3 and excludes the already-owned repository reconciliation. Unique local evidence is only the superseded umbrella rationale.
- APT-50: local Route-incoming... is the earlier broad draft. Canonical Define-incoming... supersedes it with unavailable-channel and reporter-routing cases.
- APT-51: local Design-upstream... is the earlier draft. Canonical Research-fork-based... supersedes it and keeps the research-only boundary.
- APT-52 and APT-53: local untracked files are byte-identical to origin/main; remove only those exact duplicate copies during reconciliation.

Preservation handoff: the shared main checkout remains another session's dirty workspace. Its .lore.md, apt-46, .agent-budget.toml, .roborev.toml, draft-2, and other local task files must not be stashed, reset, committed, or deleted by this task. The owner may either commit the distinct APT-46 work through its own branch or explicitly transfer ownership of a preservation patch before main is fast-forwarded. No silent main reset or blanket task-file deletion is permitted.

Verification requirement: after the owning workstream reconciles main, run backlog-py board and task views in that checkout and confirm no duplicate-ID warning remains for APT-32, APT-49, APT-50, or APT-51. backlog-py doctor is not a substitute for this semantic check. The isolated branch preserves this cleanup record; it does not claim the shared main is already clean.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Resolved canonical APT-46/APT-32 metadata collision in PR #25 and reconciled the shared main checkout to origin/main. Removed only compared superseded local task records; APT-52/53 copies were byte-identical. Preserved .lore.md, .agent-budget.toml, draft-2, APT-47, and APT-48. The earlier local .roborev.toml differed from canonical only in quote style; its preserved copy is in the approved temporary directory. backlog-py doctor --json now reports duplicateIds: [], ok: true; all affected task IDs resolve through Backlog.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
