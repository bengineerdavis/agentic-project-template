# Map: Refactor the template stack — reusable basic layers in the meta-template

Label: `wayfinder:map` (local-markdown tracker, this file is the map)
Effort opened: 2026-11-04 · Driver: Ben Davis

## Destination

A spec (via /to-spec) for the three-repo template-stack refactor: coding
standards composed into every stamped project (agnostic defaults from
copier-template-copier-template, per-language sections like PYTHON.md from
base templates, judgement-call layers appended), and the basic git-project
layers that copier currently builds duplicated across the stack refactored
into reusable patterns in the meta-template. The map ends when the way to
that spec is clear — every concern has a decided home, an inheritance rule,
and a removal plan — with nothing left to decide before ticketing.

## Notes

- Domain: copier composition. Stack is 3 deep: copier-template-copier-template
  (meta, owns meta_template/ with conditional jinja layers) →
  python-project-template (base layer) → agentic-project-template (agentic
  layer, owns fragments/ + merge engine). Downstream consumers: redge, ballet.
- Criterion fixed at charting: a concern moves to the meta-template **iff**
  it is language-agnostic AND every stamped project wants it. Layer-specific
  concerns stay down-stack. (Q4 rec, accepted)
- Standards composition (Q3, accepted): one CODING_STANDARDS.md per stamped
  project assembled like every other shared file (RENDERED_SHARED /
  marked-section merges); language conventions refactoring into separate
  convention files (PYTHON.md, JAVASCRIPT/TYPESCRIPT.md, …) as needed.
- Sequencing (Q6, accepted): incremental — a concern migrates when next
  touched; maintainer may exempt specific projects to expedite, exemptions
  do not change the designed workflow.
- copier-mise-sandbox is OUT of scope (experimental, may be deleted).
- Skills every session should consult: grilling, domain-modeling (per
  wayfinder); writing-for-agents governs any doc this effort writes.
- Sequencing plan across repos must respect the merge-engine migrations
  already shipped (legacy-pin removal, install.run migration) — a concern
  moving repos rewrites migration-table provenance.
- Agent-operation constraint (maintainer, 2026-11-04): every stamped
  project gets a skill so an agent session can operate the layer directly;
  the long-term end-state is copier-cat abstracting operations into one
  MCP service / AGENTS.md instruction section for fleet-wide intelligent
  project creation and stamped-project use. The per-project skill (T6)
  and that future surface must share one operation contract — MCP
  implementation itself is out of scope.

## Decisions so far

- [T1 — Inventory: what does each stack repo own today?](t1-inventory.md): five multi-repo overlaps (AGENTS.md, backlog wiring, LICENSE, CONTRIBUTING, alint split) + four meta-should-own gaps (CODING_STANDARDS, CHANGELOG, .gitignore, renovate); hardest open fact: meta↔python have no composition contract.

## Not yet specified (fog)

- **Ownership split — what does the agentic layer still own vs inherit from
  the python repo (incl. backlog-py wiring), and what is removed when?**
  (maintainer Q5: "this template should be inheriting from python repo,
  including backlog-py; otherwise what is the map about?") Too coarse to
  ticket until the inventory research lands; graduates into one ticket per
  mis-owned concern.
- **Migration mechanics for concern moves**: when a shared file's owner
  changes, what happens to (a) the migration table provenance comments, (b)
  stamped answers files pointing at the old layer, (c) the tripwire test's
  fragments-walk scope. Fog until the inventory names the movers.
- **Per-language convention file set**: which languages beyond PYTHON.md
  earn a file (JAVASCRIPT/TYPESCRIPT named by maintainer), and what the
  merge rule is when a project stamps two language sections.
- **What the map hands /to-spec**: the spec's shape (per-concern decision
  table? one section per concern?) — clear once two or three concerns have
  resolved; not specifiable now.
- **The copier-cat MCP service** (fleet-level intelligent project creation
  + stamped-project operation): the destination of the agent-operation
  constraint but beyond this map — graduates into its own effort once the
  operation contract (T6) is stable. Fog records the dependency, not the
  design.

## Out of scope

- copier-mise-sandbox (experimental, may be deleted — maintainer, 2026-11-04)
- copier-cat, copier-template-stack, dotfile-topic-copier (pull in only if a
  decision forces it — Q2 rec, accepted)
- The copier-cat MCP service / fleet-level agent operation surface: the
  end-state the operation contract (T6) must survive, but implementing it —
  an MCP server or instruction section that intelligently creates and
  operates stamped projects across the fleet — is a separate future effort
  (its own map when the contract is stable)

## Tickets (frontier + blocked)

<!-- child issues; local-markdown tracker = one file per ticket -->

| Ticket | Type | Blocked by | Status |
|---|---|---|---|
| [T1 — Inventory: what does each stack repo own today?](t1-inventory.md) | research | — | RESOLVED |
| [T2 — Where does CODING_STANDARDS.md live, and how do sections merge?](t2-standards-composition.md) | grilling | T1 | OPEN — frontier |
| [T3 — Ownership split: agentic layer inherits from the python repo](t3-ownership-split.md) | grilling | T1 | OPEN — frontier |
| [T4 — Migration mechanics for concern moves](t4-migration-mechanics.md) | grilling | T1, T2, T3 | OPEN (blocked) |
| [T5 — Structure as spine: alint bundles enforce the expected layout, for the template repo and stamped projects](t5-structure-as-spine.md) | grilling | — | OPEN — frontier |
| [T6 — Agent-facing operation surface: each stamped project carries a skill for layer operations](t6-agent-operation-surface.md) | grilling | T3 | OPEN (blocked) |

**Frontier:** T2, T3, T5.
