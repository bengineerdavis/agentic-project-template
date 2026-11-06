# T6 — Agent-facing operation surface: each stamped project carries a skill for layer operations

Type: grilling (HITL) · Blocked by: — (T3 resolved 2026-11-06) · Consumes: T5 (skills are stamped structure alint checks)
Status: OPEN — frontier · Claimed: nobody

## From T3 (resolved 2026-11-06)

T3 settled what the skill wraps, so this ticket is unblocked:

- **Base owns the task-operation contract** (storage, identifiers, lifecycle,
  import boundaries). **Agentic owns the agentic-specific rules**:
  worktree-per-task enforcement, review integration, task claiming.
- The per-project skill is **agentic overlay wiring** — it is an adjective's
  artifact, stamped like the rest of the layer's fragments.
- What the skill wraps is therefore the agentic-domain half plus a consumer
  view of the base's contract — **not** the whole composition surface. Copier
  runs, stack selection, and provenance belong to copier-cat (T7's contract).
- The skill must not present itself as the owner of task storage, or it will
  duplicate the base's contract and drift — the same "two owners, no
  contract" defect T1 found in backlog wiring.

## Question

Maintainer direction (2026-11-04): part of the design is giving each
project its own skill so the template can be used directly from an agent
session — eventually copier-cat abstracts the whole thing (a single MCP
service or AGENTS.md instruction section) so agents can intelligently
create new projects and utilize stamped projects.

Decide the per-project skill design that survives both ends:

1. **What the skill wraps**: today the agent-facing operations are the
   thin CLI (cli.py: new/layer/update — thin by design, the copier-cat C1
   prototype). Does the stamped skill expose exactly that surface
   (`update`, wiring checks, task context) or a richer one? T3's ownership
   split determines what belongs in the skill vs inherited tooling.
2. **Authoring + stamping home**: the skill lives where the operations
   live (agentic layer's fragments/ — it is layer wiring, T3's answer
   decides), stamped like any other artifact (dotagents --project
   install already exists in the bootstrap). Name the skill, its
   description (the context pointer), and what it instructs the agent to
   do for each operation.
3. **Copier-cat convergence (constraint, not scope here)**: the skill and
   the future copier-cat MCP/instruction surface must target the SAME
   operation contract — design once, two consumers (per-project skill
   now, fleet-level MCP service later). Decisions in this map must not
   preclude that abstraction; no MCP work in this effort.
4. **Create-vs-operate split**: "agents can intelligently create new
   projects" is the copier-cat end-state. Does the per-project skill
   carry anything about creation (e.g. pointing back at the template
   stack) or only in-project operations? Default: in-project only;
   creation waits for copier-cat.

Out-of-scope reminder: the MCP service itself is a future copier-cat
effort (see map Out of scope) — this ticket designs the contract it will
reuse.
