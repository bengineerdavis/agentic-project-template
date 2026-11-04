---
id: APT-27
title: Re-validate opencode lsp stanza when V2 restores LSP runtime
status: To Do
created_date: 2026-11-04 07:18
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The stamped opencode.json lsp stanza (alint over .md/.markdown/.yaml/.yml/.py/.toml/.json) is forward wiring: opencode V2 parses the section but runs no LSP servers (verified 2026-11-04, apt-10). When opencode V2 ships a working LSP runtime, the stanza must be re-validated against real server behavior — extension coverage, pyright-builtin coexistence, and whether the accepted CLIs-directly substitute still applies.

Ship:

- Re-validated lsp stanza: a planted type error and an alint finding surface as real LSP diagnostics in an opencode V2 session, or the stanza is corrected/removed with findings recorded

Constraints:

- Extension list edits must keep the server's actual claim (alint lsp extension list), not per-language splits
- pyright stays builtin-from-PATH unless opencode V2 changes its auto-start behavior

Decision record: Recorded 2026-11-04 per roborev review 259 (Medium) on e96ea97 — the apt-10 scenario's accepted substitute is documented in spec.md; this task closes the loop when upstream changes.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 An opencode V2 session surfaces a planted type error and an alint finding as real LSP diagnostics, or the stanza is corrected/removed with the outcome recorded in ARCHITECTURE.md
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
