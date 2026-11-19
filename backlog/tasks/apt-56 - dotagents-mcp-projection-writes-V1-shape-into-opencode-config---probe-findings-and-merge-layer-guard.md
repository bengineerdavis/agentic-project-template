---
id: APT-56
title: dotagents mcp projection writes V1 shape into opencode config - probe findings and merge-layer guard
status: To Do
created_date: 2026-11-19 20:53
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->

dotagents 3.4.0 (npm latest as of 2026-11-19) hardcodes its opencode target MCP rootKey as `mcp` (V1 bare-server-map shape) in targets/definitions/opencode.js — it has no support for opencode V2's `mcp.servers` nesting. Probes against a V2-shaped `opencode.json` in worktree .worktrees/dotagents-v2-probe showed `mcp add` writes `mcp.<name>` as a sibling of `mcp.servers`, and add+remove+sync left a stale projected duplicate. opencode V2 tolerates the mixed members in memory, so nothing breaks today, but the template merge layer must not treat dotagents' opencode MCP projection as V2-safe.

Ship:

- A merge-layer guard (or declared incompatibility note in ARCHITECTURE.md/spec) covering dotagents' opencode MCP projection so a stamped project's V2-shaped opencode config never silently gains V1-shaped `mcp.<name>` siblings of `mcp.servers`.
- A probe-evidence appendix in the task Implementation Notes (add/remove/sync behavior on V1-shaped and V2-shaped files) so re-probing a newer dotagents has a baseline.
- An upstream-facing issue draft for @sentry/dotagents documenting the V2 rootKey gap with the probe transcript.

Constraints:

- Do not pin or downgrade dotagents to dodge the gap; the layer declares behavior, not a workaround version.
- Findings verified against dotagents 3.4.0 source (dist/targets/definitions/opencode.js, dist/targets/mcp-writer.js), not docs.
- Every referenced skill is declared in agents.toml in the same change.

Decision record: Agreed with the maintainer 2026-11-19: record findings and guard the merge layer rather than adopting dotagents' MCP projection for opencode in the layer.

Handoff (session wrap-up 2026-11-19): probes ran in worktree .worktrees/dotagents-v2-probe on branch dotagents-v2-probe (no commits — worktree restored to neutral). Probe A (V1-shaped file): mcp add/remove edit the file surgically and preserve unrelated content; sync does NOT prune a projection whose declaration was removed (writer early-returns when zero servers are declared). Probe B (V2-shaped file): mcp list reads mcp.servers correctly; mcp add writes mcp.<name> as a sibling of mcp.servers (V1 shape). Probe C: add+remove+sync on a one-server V2 file leaves a stale duplicate mcp.backlog-py entry next to mcp.servers. UNVERIFIED: whether opencode V2 actually spawns servers declared at the V1 position in an otherwise-V2 file (tolerance observed in docs/config schema only, not runtime). Resume: re-run probes from the worktree, then implement the guard.

Blocked adjacent work (session wrap-up 2026-11-19): the requested V2/`.jsonc` conversion of the repo-root dev `opencode.json` was NOT performed — its working tree carries a foreign uncommitted edit (backlog-py command switched uvx→bare `backlog-py-mcp`, `enabled` dropped) that pairs with the dirty `mise.toml` pipx pin; committing a conversion would capture those edits. Ownership unclear, left untouched per house rules. Safe to defer: opencode V2 normalizes V1-shaped configs in memory without rewriting (migration guide). Next action: confirm the edit's owner, then convert root config to V2 `mcp.servers` + rename to `opencode.jsonc` (dotagents discovers the root `.jsonc` via fallback paths — verified in dist/targets/definitions/opencode.js). Global `~/.config/opencode/opencode.jsonc` already V2-functional (mcp.servers, permissions array, update key); residual V1 keys (agent/provider/small_model/plugin) are chezmoi-managed and accepted-but-normalized by V2 — no action required.

<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria

<!-- AC:BEGIN -->

- [ ] #1 The merge layer refuses or clearly documents dotagents' opencode MCP projection against a V2-shaped opencode config (no silent `mcp.<name>` siblings of `mcp.servers` can be stamped).
- [ ] #2 Implementation Notes carry the full A/B/C probe baseline (V1 add/remove/sync, V2 add shape, empty-state duplicate) for re-probing newer dotagents.
- [ ] #3 Upstream issue draft for @sentry/dotagents exists in the task or a linked file, citing the probe transcript and dotagents 3.4.0 source paths.
- [ ] #4 Focused test red-proves the guard: with dotagents-shaped V1 output applied to a V2 config, the guard fails before the fix and passes after.

<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->

Session retro (2026-11-19, wrap-up; probe commit 138d7ff pushed to main):

- Went right: worktree isolation (dotagents-v2-probe) kept all probing off main and was removed neutral; findings landed as APT-56 with a re-probe baseline; the foreign-dirty-file gate correctly stopped the root opencode.json conversion from capturing another session's edits.
- Went wrong: the repo moved (~/code/templates → ~/code/personal/templates) mid-session, stranding the old path as a husk and breaking worktree paths plus .venv shebangs; several probe commands were lost to location restarts and re-run.
- Negative results (verified, not just observed): dotagents `mcp remove` edits only agents.toml; `sync` never prunes a projection whose declaration was removed (mcp-writer early-returns at zero declarations); against a V2 file, add+remove+sync leaves a stale duplicate entry beside mcp.servers.
- Lesson for any session in this repo: after a directory move, .venv/bin/\* shebangs still point at the old absolute path and every venv command fails with "bad interpreter" — rebuild with `uv venv --clear && uv sync` before reporting commands as unrunnable; check the shebangs first.
- Open follow-ups: ACs #1–#4 below. No other work opened.

<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done

<!-- DOD:BEGIN -->

<!-- DOD:END -->
