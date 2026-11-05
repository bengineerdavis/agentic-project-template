---
id: draft-1
title: Multi-agent workflow patterns from r/ClaudeCode guide (Room, SOTs, Spines,
  Team)
status: Draft
created_date: 2026-11-04 22:40
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Draft follow-up task: grab agent-workflow patterns from u/allemaar's multi-agent guide (r/ClaudeCode, 1vphazv) and land them as agentic-layer capabilities. The five patterns: Room (shared folder of timestamped .md messages with email-style frontmatter — durable cross-session timeline), SOTs (authoritative docs provided per-task for progressive context discovery), Spines (annotated indexes that orient from any node — what is this, what owns it, what to read next), Team roles (driver/reviewer leads, Shadow advisor, Scribe dashboard cartographer, Keeper archivist), and compaction/recovery discipline (checkpoint ~70% context, recover from disk).

Priority per maintainer: the spine principle is the one to enforce in how the layer is built — better document fetching and progressive disclosure over search-only navigation. Everything else is candidate.

Scope check for the layer: spines map onto AGENTS.md navigation pointers, ARCHITECTURE.md, and per-doc "read next" conventions (already partly there); Room is a per-task protocol the layer could stamp (docs/.room/ + message schema); SOTs discipline could formalize how tasks declare their SOT set; Team roles and Scribe are heavier — evaluate against the layer's 'shrink AI to the best tradeoff' principle before stamping anything.

Constraints:

- Spine principle enforced first; the rest evaluated against spec.md principle 2 (shrink AI to the best tradeoff)
- Nothing stamped until a pattern survives a fresh-stamp smoke; consult-llm is the only existing cross-model pattern
- This draft graduates to a real task with Ship bullets after the wayfinder template-stack map settles what the layer inherits vs owns (avoid double-planning)

Decision record: Maintainer direction 2026-11-04 — follow-up to the template-stack wayfinder effort; spine principle is the enforceable core.
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
