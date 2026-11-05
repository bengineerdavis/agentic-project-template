# T3 — Ownership split: agentic layer inherits from the python repo — what moves, what's removed, when?

Type: grilling (HITL) · Blocked by: T1 · Blocks: fog graduation (per-concern tickets)
Status: OPEN · Claimed: Ben Davis (2026-11-04)

## Scope added at resumption

Include the lore knowledge tier and cross-project entity links in the ownership
boundary. Machine-level lore setup remains user-scoped; this ticket decides
where stamped knowledge seeds and shared stack knowledge belong.

## Question

The maintainer's Q5 challenge: "this template should be inheriting from the
python repo, including backlog-py; otherwise what is the map about?" Using
T1's inventory, decide per concern whether the agentic layer still owns it,
inherits it from python-project-template, or hands it to the meta-template —
with an explicit removal plan and timing for each concern that moves
(incremental: on next touch, unless an expedite exception is granted).
backlog-py wiring is the named first case: where does its mise pin, the
backlog-init task, and the backlog/ scaffold belong in the stack?

This ticket graduates the fog entry "ownership split" into per-concern
decisions; each mis-owned concern found here either gets a resolution line
or spawns a new ticket.

## Round 2 answers (maintainer, 2026-11-04)

- The meta-template owns the agnostic base artifact. Python provides language
  specialization; agentic provides agent-specific specialization. Standalone
  Python rendering remains supported during migration.
- The base owns the backlog-py scaffold, tool pin, and idempotent
  initialization. Agentic owns only the workflow that consumes it. One
  canonical task-management choice replaces independent installation switches.
- Adoption must also support importing an external task store or an existing
  backlog-based agent workflow into the base's compliant structure.
- Each overlay handles only the Python- or agent-specific aspects of generic
  tools. Generic tool ownership does not follow the agent that happens to
  invoke it.
- Lore remains agentic-owned in stamped projects. The template repositories
  share stack-level knowledge through the parent templates scope and retain
  local implementation knowledge in their own scopes. Cross-reference existing
  repo entities rather than duplicate entries.
- Track named template stacks by their base, selected overlays, and
  composition provenance, analogous to selecting a combination on gitignore.io.
- Migration is compatibility-first, with explicit start-fresh, backup,
  restore, and import options. Both deterministic code and agent-assisted
  workflows must be supported for full migration.

## Open ownership questions

Resolve the distinction between a stack's definition and a project's recorded
composition, then settle import conflict policy, fresh-start guarantees,
knowledge ownership, and the operation contract before implementation.
