---
id: APT-28
title: 'Lore onboarding: stamped long-term-knowledge registration'
status: Done
created_date: 2026-11-04 16:43
assignee:
- Ben Davis
labels:
- agentic-layer
updated_date: 2026-11-04 17:19
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The layer has zero lore coverage. Ships include_lore (default on, opt-out): a seeded .lore.md carrying only lore's managed header, and one gated ai-rules line pointing agents at .lore.md. AGENTS.md's lore-managed Long-term Knowledge section is NOT layer-managed — lore owns it and writes it itself. Layer placement: L2 knowledge tier (third tier beside ai-rules and @docs). Update path: flag off leaves .lore.md (accumulated knowledge, never deleted); no re-stamp. Machine-level lore setup (installer, lore run/lore setup, plugin) is chezmoi/user territory — the layer stamps repo-side artifacts only.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `include_lore` is a copier question (bool, default true, L2 grouping in copier.yml) with help text stating what gates on it
- [x] #2 include_lore on: a fresh stamp carries `.lore.md` containing exactly lore's managed header line (seed; lore imports/merges into it), and `.context/ai-rules.md` carries one line pointing agents at `.lore.md`
- [x] #3 include_lore off: a fresh stamp carries no lore trace beyond `.agentic-answers.yml` (sweep test at artifact level: no `.lore.md` file, no `.lore.md` mention in ai-rules)
- [x] #4 the AGENTS.md lore-managed "Long-term Knowledge" section is never stamped or managed by the layer (lore owns its markers); the layer's managed section content is unchanged by include_lore
- [x] #5 update path: a project stamped with lore and updated with the flag off keeps `.lore.md` untouched and stops referencing it (ai-rules loses the line); no stale layer wiring
- [x] #6 spec (L2 row / Decision record) and ARCHITECTURE.md (L2 owned-by) name the lore tier; stamp matrix green
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Registration model verified against lore v0.40.0 and withlore.ai/docs: there is no per-repo register command — lore identifies projects by cwd and itself creates .lore.md (plus the AGENTS.md section and optional .lore.json) "inside projects where those features are used". The layer therefore pre-stages repo-side artifacts instead of invoking lore. The seed is a single-segment conditional path ({% if include_lore %}.lore.md{% endif %}); probe-verified that copier renders it on true and skips it on false, so no CLI skip list is needed. Update path probe-verified with the template ref actually moving: copier update patches only template evolution rendered with the stored answers — flipping an answer changes nothing in the destination — so the ai-rules pointer is stripped by apply_fragments (text-level, continuation-line aware) and .lore.md survives by copier never touching it. Constraint recorded in the spec: the seed file must stay in template/ permanently, or a later update patch deletes project .lore.md files.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
include_lore (default on) stamps the .lore.md seed (lore's managed header only) and one ai-rules line pointing at it; lore's AGENTS.md section stays lore-owned. Opt-out stamps no lore trace; flag-off on update strips the pointer and leaves .lore.md. spec Decision record + ARCHITECTURE L2 updated. mise run test 55 passed; stamp matrix OK (choices preserved). Commits: 0b0c426 (seed+gate), 2c1ba71 (update strip), 8fae41f (docs).
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
