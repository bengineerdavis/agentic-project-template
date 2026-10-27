---
id: APT-22
title: Reorganize layer fragments per tool with a declared merge order
status: To Do
created_date: 2026-10-18 23:13
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The layer's shared-file fragments are grab-bags:

- `fragments/mise-layer.toml` carries every tool's `[tools]` pin and every tool-specific task (`roborev-*`, `backlog-init`, `dotagents-install`, `review-deep`, `check`, `install`) in one file
- `fragments/agents-md-section.md` carries every tool's AGENTS.md lines in one block

The spec's layering rule (one layer or one component, never a grab-bag) holds only because the CLI merge is deterministic.

Reorganize per tool. Each stamped tool (alint, backlog-py, dotagents, opencode, prek, roborev, tombi, worktrunk) owns `fragments/tools/<tool>/` with its mise pin and tasks, prek hooks, gitignore lines, and AGENTS.md lines. The CLI merge engine applies the fragments in a declared order.

Ordering matters: prek `[[repos]]` hook order and AGENTS.md section order must be declared once, not inferred from a directory listing.

Confirmed with the maintainer 2026-10-18: per-tool layering plus a declared order is the simplest first cut. Revisit the design if it fights the merge engine.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 fragments/tools/<tool>/ exists for each stamped tool; no tool contribution remains in a cross-tool grab-bag fragment
- [ ] #2 The CLI merge applies per-tool fragments in one declared, tested order (a test asserts merged prek repos and AGENTS.md section order)
- [ ] #3 The order is declared in one place (single source), not sorted-directory inference
- [ ] #4 Stamp matrix green: layer-only, with-base, existing-project merge, update path
- [ ] #5 tombi lint and mise parse the merged mise.toml/prek.toml on a stamped project (redge)
- [ ] #6 agentic-project-template update on redge lands the reorganization without clobbering local state
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
