---
id: APT-24
title: Backlog-friendly Matt Pocock workflow
status: Done
created_date: 2026-10-26 18:35
updated_date: 2026-10-27 08:25
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Matt Pocock's engineering skills assume a generic issue tracker. This layer already uses backlog-md-py. Ship the adapter between the two:

- `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `docs/agents/domain.md`
- an Agent skills block in `AGENTS.md`
- a `backlog-workflow` skill that detects `backlog/` and maps spec, tickets, claims, and decisions onto it

Constraints:

- plain-english and writing-for-agents are the writing standards; no new standard is invented here
- the adapter gates on `include_backlog` (default on): a full opt-out stamps no backlog trace, and the update path strips stale wiring
- stamped commands run through uvx; the finish flow is `wt merge`, not a PR

Keep the adapter small enough to upstream to mattpocock/skills later.

Agreed with the maintainer 2026-10-27: full opt-out via include_backlog (default on); uvx command forms; stamped docs teach the wt merge finish flow.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `docs/agents/issue-tracker.md` names `backlog-py-mcp` and the spec/ticket/claim mapping
- [x] #2 `AGENTS.md` links all three docs
- [x] #3 the `backlog-workflow` skill exists, detects `backlog/`, and maps spec, tickets, claims, and decisions onto it
- [x] #4 a stamped project gets the three `docs/agents` files, the skill, and the `AGENTS.md` references
- [x] #5 stamp tests assert all of the above; `mise run test` and `mise run test-template` pass
- [x] #6 `include_backlog: false` stamps with no backlog trace (sweep test), and updating an opted-in project with the flag off strips the stale wiring (AGENTS.md section, backlog-init task, managed files under gated prefixes)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Review of this PR flagged six findings; all fixed on this branch. Toggle: include_backlog question (default true); CONDITIONAL_PATHS skip in apply_layer — copier renders path segments independently, so whole-file exclusion is a CLI skip list keyed by the render's own answers; fragment split (agents-md-section core + agents-md-backlog-section, concatenated at apply time — the managed section is replaced whole, which makes the ON-to-OFF update self-healing); mise strip is text-level on fresh stamps and doc-level on merges, because deep_merge never removes keys. The four new stamped files carry the managed comment — without it, re-stamps would skip them forever. Commands: uvx forms everywhere (backlog-py is not on PATH in a fresh stamp); backlog-py task complete does not exist — closing is task edit -s Done; the skill teaches the wt merge finish flow; issue-tracker.md renders task_prefix instead of pointing at copier.yml, which is not stamped into projects. mise run test (43 passed) and mise run test-template (stamp matrix OK, choices preserved) green on this branch.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
The adapter ships gated: include_backlog (default on) stamps the three docs/agents files, the backlog-workflow skill, the MCP declaration, and the AGENTS.md skills section; false stamps with no backlog trace and the update path strips stale wiring. Stamped commands are uvx-form and verified against the CLI. Spec v1-scope row amended. mise run test (43) and the stamp matrix green.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
