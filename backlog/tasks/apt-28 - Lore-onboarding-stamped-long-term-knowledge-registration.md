---
id: APT-28
title: 'Lore onboarding: stamped long-term-knowledge registration'
status: In Progress
created_date: 2026-11-04 16:43
assignee:
- Ben Davis
labels:
- agentic-layer
updated_date: 2026-11-04 16:43
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The layer has zero lore coverage. Ships include_lore (default on, opt-out): a seeded .lore.md carrying only lore's managed header, and one gated ai-rules line pointing agents at .lore.md. AGENTS.md's lore-managed Long-term Knowledge section is NOT layer-managed — lore owns it and writes it itself. Layer placement: L2 knowledge tier (third tier beside ai-rules and @docs). Update path: flag off leaves .lore.md (accumulated knowledge, never deleted); no re-stamp. Machine-level lore setup (installer, lore run/lore setup, plugin) is chezmoi/user territory — the layer stamps repo-side artifacts only.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 `include_lore` is a copier question (bool, default true, L2 grouping in copier.yml) with help text stating what gates on it
- [ ] #2 include_lore on: a fresh stamp carries `.lore.md` containing exactly lore's managed header line (seed; lore imports/merges into it), and `.context/ai-rules.md` carries one line pointing agents at `.lore.md`
- [ ] #3 include_lore off: a fresh stamp carries no lore trace beyond `.agentic-answers.yml` (sweep test at artifact level: no `.lore.md` file, no `.lore.md` mention in ai-rules)
- [ ] #4 the AGENTS.md lore-managed "Long-term Knowledge" section is never stamped or managed by the layer (lore owns its markers); the layer's managed section content is unchanged by include_lore
- [ ] #5 update path: a project stamped with lore and updated with the flag off keeps `.lore.md` untouched and stops referencing it (ai-rules loses the line); no stale layer wiring
- [ ] #6 spec (L2 row / Decision record) and ARCHITECTURE.md (L2 owned-by) name the lore tier; stamp matrix green
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
