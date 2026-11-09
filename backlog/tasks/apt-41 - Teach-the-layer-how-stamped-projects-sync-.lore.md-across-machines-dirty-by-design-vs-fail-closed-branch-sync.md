---
id: APT-41
title: Teach the layer how stamped projects sync .lore.md across machines (dirty-by-design
  vs fail-closed branch sync)
status: To Do
created_date: 2026-11-09 20:29
ordinal: 1
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
WHY: APT-28 stamps .lore.md (include_lore, seeded managed header) and APT-32's branch-sync workflow fails closed on dirty local main — but on any machine where lore runs, .lore.md is modified between commits by lore's own background export. Observed live 2026-11-09 in bengineerdavis/dotfiles: git pull --ff-only (203 commits behind) aborted solely on .lore.md (local and incoming rewrites were both lore's auto-generated content — the memory gateway's own file, not agent or human work); the session could not sync main without an author ruling on a file the repo's own governance says must never be touched by tooling.

Upstream intent (withlore.ai/docs/team-memory/, fetched 2026-11-09): .lore.md is designed to be git-version-controlled, PR-reviewable, and merge-friendly — entries sorted alphabetically per category with stable <!-- lore:UUID --> markers so conflicts are rare and legible; hand edits are first-class and imported on the next session; export skips the write entirely when nothing changed. The design expects .lore.md to flow through normal git merges — but the observed failure is BEFORE the merge: a working tree dirty with lore's own export blocks ff-only pulls and branch switches, which APT-32 treats as fail-closed.

FEATURE: the layer ships a documented (and where possible tooling-supported) .lore.md sync policy for stamped projects: when a pull/branch-sync is blocked ONLY by a modified .lore.md (not by any other dirty path), the workflow should distinguish lore-managed churn from real unlanded work — e.g. commit lore's export as its own queue-style commit before syncing, or stash/restore just .lore.md, or defer to lore's next export pass — with the fail-closed rule preserved for every other file. Ship: a decision record + a section in the branch-sync spec/task naming the .lore.md carve-out, tests pinning the carve-out behavior, and a real-world validated example from the dotfiles repo. Constraints: never modify .lore.md's content outside lore's own writes; never sweep it into an unrelated commit (git add -p discipline); the carve-out must be mechanical (path-scoped), not judgment-based; agent tooling may not read .lore.md for any other purpose (LINK-CHECKING precedent).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
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
