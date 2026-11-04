---
id: APT-26
title: Stamp roborev wiring into projects
status: To Do
created_date: 2026-11-04 07:09
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The layer stamps roborev wiring (mise pin, roborev-start/-status/-fix tasks, .roborev/ ignore, AGENTS.md fast-loop bullet) but no stamp-matrix or fresh-project verification exists for it: apt-3 verified delivery on this repo, apt-22 moved the fragment into fragments/tools/roborev/ without a stamped-end-to-end check.

Ship:

- Fresh stamp carries the full roborev wiring: mise pin (github: backend), tasks.roborev-start/-status/-fix, .roborev/ gitignore line, AGENTS.md fast-loop bullet
- Stamp-matrix assertion covers the roborev fragment merge
- Fresh-project smoke: roborev init + roborev status run on a stamped project with a git repo

Constraints:

- Stamp-matrix assertion lives in the stamp-matrix fixture, not a one-off script
- Smoke runs against a disposable stamp root, never the layer repo

Decision record: Agreed with the maintainer 2026-11-04: verify via stamp matrix plus one fresh-project smoke, mirroring apt-13's worktrunk verification.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Fresh stamp carries the full roborev wiring: mise pin (github: backend), tasks.roborev-start/-status/-fix, .roborev/ gitignore line, AGENTS.md fast-loop bullet
- [ ] #2 Stamp-matrix assertion covers the roborev fragment merge
- [ ] #3 roborev init + roborev status run on a fresh stamped project with a git repo
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
