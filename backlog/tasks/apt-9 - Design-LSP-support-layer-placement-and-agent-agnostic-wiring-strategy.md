---
id: APT-9
title: 'Design LSP support: layer placement and agent-agnostic wiring strategy'
status: Done
created_date: 2026-10-12 18:26
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Language intelligence for agents: LSP servers as environment tools (mise-pinned) + per-agent wiring (opencode.json lsp section merges via the existing RENDERED_SHARED json path). open question: own layer vs L0/L2 components. alint lsp is a first-class candidate server (repo-structure diagnostics reach any LSP consumer). 'Any agent I want' is the requirement, opencode is the proof.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Layer placement decided and recorded in ARCHITECTURE.md with the concern stated
- [x] #2 Agent-agnostic wiring strategy written (what generalizes, what is per-agent)
- [x] #3 Spec open question or behavior updated in the same change
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Decided 2026-11-03, recorded in backlog/decisions/decision-2.
Placement: L0 pins language servers in per-tool mise fragments; L2 wires
them into each agent's config (opencode.json lsp via RENDERED_SHARED).
No cross-agent abstraction — per-agent notes as agents are adopted (apt-11).
Probes: opencode V2 lsp section (docs), pyright via npm:pyright on PATH,
alint lsp 0.21.0 JSON-RPC round-trip → 9 diagnostics published.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
No new layer: L0 owns pins, L2 owns wiring, contract is per-agent notes.
Spec gains the LSP behavior section; ARCHITECTURE.md annotates L0 and L2.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
