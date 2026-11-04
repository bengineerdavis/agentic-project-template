---
id: APT-22
title: Reorganize layer fragments per tool with a declared merge order
status: Done
created_date: 2026-10-18 23:13
updated_date: 2026-11-04 16:39
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
- [x] #1 fragments/tools/<tool>/ exists for each stamped tool; no tool contribution remains in a cross-tool grab-bag fragment
- [x] #2 The CLI merge applies per-tool fragments in one declared, tested order (a test asserts merged prek repos and AGENTS.md section order)
- [x] #3 The order is declared in one place (single source), not sorted-directory inference
- [x] #4 Stamp matrix green: layer-only, with-base, existing-project merge, update path
- [x] #5 tombi lint and mise parse the merged mise.toml/prek.toml on a stamped project (redge)
- [x] #6 agentic-project-template update on redge lands the reorganization without clobbering local state
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Taken 2026-10-27: worktree apt-22-per-tool-fragments.
Merged apt-24 backlog workflow into the reorg 2026-11-02 (4aa50b3): TOOL_FRAGMENT_ORDER + include_backlog gating coexist; 46 tests, lint, stamp matrix green (AC #4 update path OK). Fast-forwarded main.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Closed 2026-11-04. Fragments reorganized per tool under fragments/tools/<tool>/ in a declared order (TOOL_FRAGMENT_ORDER in stamp.py — single source, tested); merge engine keeps one deep_merge primitive + thin wrappers, with merge_mise_fragment carrying two provenance migrations (legacy bare opencode pin removal; layer-authored install.run exact-match replacement via _LAYER_AUTHORED_SCRIPTS, derived verbatim from git history and guarded by a tripwire test — hardened against shallow-clone vacuity per review 265). Stamp matrix green (layer-only, with-base, existing merge, update-with-choices-preserved). Redge verification: tombi lint passes, mise parses the merged config, alint gate green; the update landed both migrations with warnings (commits fc2c5e4/17bd645). All fast-loop findings resolved: 258+259 (LSP doc drift, 1ec7def), 261 (tripwire), 263 (comment leak 0ecccee, roborev warning 02a0191), 265/266 (edc86a7). Follow-ups: APT-26 (stamp roborev wiring smoke), APT-27 (re-validate lsp stanza when V2 restores LSP).
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
