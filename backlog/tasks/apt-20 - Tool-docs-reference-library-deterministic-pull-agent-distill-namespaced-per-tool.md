---
id: APT-20
title: 'Tool-docs reference library: deterministic pull + agent distill, namespaced
  per tool'
status: To Do
created_date: 2026-10-18 23:03
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
When the layer adds a tool (a mise pin, an agents.toml source), resolving it - backend, flags, version churn - costs live web search every time. Found adding alint/roborev/dotagents to the fragment while stamping redge: alint's mise backend took a web search; the bare names had to be probed blind. Build the reference library those additions consult: a deterministic command pulls a tool's official docs into docs/references/<tool>/ (namespaced by tool, subfolder-organized for indexing), an agent distills the pulled docs into a per-tool reference page pinned to the tool's mise pin, and a user-level schedule re-pulls regularly so the library never goes stale. The pull stays deterministic CLI (curl/gh); only the distill is agent work (the shrink division). Design decides placement: library in this repo vs hoisted per the nothing-personal boundary.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A mise task pulls official docs for a named tool into docs/references/<tool>/ deterministically; no agent in the pull path
- [ ] #2 References namespaced per tool under docs/references/<tool>/; docs/references.md links into the trees with no orphans
- [ ] #3 An agent procedure distills each pulled tool into a per-tool reference page citing the pinned tool version
- [ ] #4 Regular refresh from a user-level schedule (chezmoi) invoking the shared task; never a project-stamped schedule
- [ ] #5 Re-pull is idempotent: unchanged upstream docs produce no diff
- [ ] #6 Adding a tool to the layer ([tools] or agents.toml) lands its docs tree in the same change
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
