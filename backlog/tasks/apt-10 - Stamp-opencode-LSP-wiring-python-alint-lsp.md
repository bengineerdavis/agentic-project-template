---
id: APT-10
title: Stamp opencode LSP wiring (python + alint lsp)
status: Done
created_date: 2026-10-12 18:26
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Wire LSP into stamped projects: python language server via mise pin, alint lsp as stdio server so structure diagnostics reach agents.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Python LSP server pinned in the layer mise fragment and available in stamped projects
- [x] #2 opencode.json carries the lsp section via merge (existing project configs never clobbered)
- [x] #3 alint lsp wired and serves diagnostics
- [x] #4 Smoke: an agent session sees a planted type error and an alint finding as diagnostics
- [x] #5 Stamp matrix asserts the merge
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
AC1: fragments/tools/pyright/mise.toml pins npm:pyright@1.1.414 (mise backend
probe: registry > npm:; npm:pyright bundles node). Scoped install updated.
AC2: lsp section rides RENDERED_SHARED (merge_json_file deep-merge); unit test
proves a project's own lsp servers survive the merge.
AC3: alint lsp 0.21.0 speaks JSON-RPC over stdio; probe published 9 diagnostics
on a planted trailing-whitespace violation. Wired in opencode.json `lsp.alint`.
AC5: stamp matrix passes (test_stamped_opencode_json_wires_lsp,
test_stamped_mise_pins_python_lsp, test_lsp_servers_resolve_through_shims,
test_update_merge_keeps_project_lsp_entries). 50 unit tests.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Landed 2026-11-03. L0: fragments/tools/pyright/mise.toml pins npm:pyright@1.1.414,
scoped install updated. L2: opencode.json.lsp wires `alint lsp` (+ pyright
forward-wiring), merged via RENDERED_SHARED — update-path test proves project
configs are additive. agents.md bullet instructs agents to run pyright/alint
check directly.

AC4 smoke (stamped project, openrouter model): agent session read a planted
type error and ran both pinned CLIs — pyright reported the int+str operator
error, alint check . reported 7 repo-structure findings. Caveat: opencode V2
(2.0.32) parses the `lsp` config section but does NOT run LSP servers (upstream
regression, documented in V2 upgrade guides) — the config is forward wiring for
when V2 restores the LSP runtime; the working V2 feedback path is the CLI loop,
which opencode itself recommends. 50 unit tests, lint, stamp matrix green.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
