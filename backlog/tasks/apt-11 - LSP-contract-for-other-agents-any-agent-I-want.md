---
id: APT-11
title: LSP contract for other agents (any agent I want)
status: To Do
created_date: 2026-10-12 18:26
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Generalize beyond opencode: documented per-agent LSP wiring map (claude, codex, cursor...) with what dotagents can and cannot abstract. At least one non-opencode agent wired or explicitly deferred with a stated reason.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Per-agent wiring map committed in ARCHITECTURE.md
- [ ] #2 One non-opencode agent demonstrably consumes the same servers, or the deferral is recorded with its reason
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Note 2026-11-03 (from apt-9, decision-2): the LSP contract is
"mise-pinned binary on PATH (L0, per-tool fragment) + per-agent config
stanza (L2)". opencode wiring is done (apt-10: `lsp` section in
`.opencode/opencode.json` via RENDERED_SHARED, alint + pyright).
For each future agent (claude, codex, cursor, ...): add its config surface
to the layer the same way — pin the server in the tool fragment, wire it
in that agent's native config, document the stanza in ARCHITECTURE.md.
No cross-agent abstraction: the shared contract is the pin, not the stanza.
The alint server is agent-agnostic by design (speaks plain LSP over stdio),
so a new agent only needs a new stanza pointing at the same binaries.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
