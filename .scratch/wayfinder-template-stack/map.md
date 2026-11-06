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
- Criterion fixed at charting (Q4 rec, accepted), **superseded by T3
  (2026-11-06)**: a concern moves to the meta-template iff it is
  language-agnostic AND every stamped project wants it. Layer-specific
  concerns stay down-stack. Replaced by the layered rule — meta owns what
  every base needs, base owns what every project needs, overlay owns what only
  a domain needs. Kept here so the change of criterion is visible rather than
  silently rewritten.
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
- [T3 — Ownership split: agentic layer inherits from the python repo](t3-ownership-split.md): meta owns agnostic structure, generic tools, and task storage; Python and agentic supply domain expertise through operation contracts; copier-cat orchestrates composition and phone home; redge retains safe sync. All nine of T1's concerns now have an owner (see the ticket's per-concern verdict table). Vocabulary fixed: meta makes bases, base is the noun, overlays are adjectives, a stack is one base plus base-compatible overlays. Placement rule: layered by who needs the concern — meta for what every base needs, base for what every project needs, overlay for what only a domain needs. Layering is the norm: nine shared files need it, so T2 designs the mechanism once. Licensing propagates three ways — meta owns the choice set and SPDX corpus and asks each new base which licenses its projects may offer; the base owns the project renderer. That chain is broken today at the base's `template/`.

## Not yet specified (fog)

- **Removal sequence per concern**: T3 resolved ownership. Each concern's
  implementation order and removal plan now belongs to T4, so no ownership
  decision remains fogged.
- **Migration mechanics for concern moves**: when a shared file's owner
  changes, what happens to (a) the migration table provenance comments, (b)
  stamped answers files pointing at the old layer, (c) the tripwire test's
  fragments-walk scope. Fog until the inventory names the movers.
- **Per-language convention file set**: which languages beyond PYTHON.md
  earn a file (JAVASCRIPT/TYPESCRIPT named by maintainer), and what the
  merge rule is when a project stamps two language sections. (T2 territory;
  noted here because it is still greenfield.)
- **The project-type taxonomy**: four axes (is_distributed, has_entry_point,
  gui, owns_service_lifecycle), flags not an enum, noun/adjective model.
  Decided in principle; placement and mechanics are T8.
- **License guidance**: a choosealicense-style reasoning surface, since more
  choices do not help the decision. T9.
- **Base×overlay compatibility matrix**: which base-and-overlay pairs are
  actually verified. T3 R6 says stacks carry "tested compatibility records";
  nobody produces them yet. Copier-cat owns this when it exists — under T7's
  contract, and out of scope until then.
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
| [T2 — Layered-file composition: where does CODING_STANDARDS.md live, and how do sections merge?](t2-standards-composition.md) | grilling | T1, T3 | OPEN — frontier |
| [T3 — Ownership split: agentic layer inherits from the python repo](t3-ownership-split.md) | grilling | T1 | RESOLVED |
| [T4 — Migration mechanics for concern moves](t4-migration-mechanics.md) | grilling | T2, T7 | OPEN (blocked) |
| [T5 — Structure as spine: alint bundles enforce the expected layout, for the template repo and stamped projects](t5-structure-as-spine.md) | grilling | — | OPEN — frontier |
| [T6 — Agent-facing operation surface: each stamped project carries a skill for layer operations](t6-agent-operation-surface.md) | grilling | — | OPEN — frontier |
| [T7 — Meta↔base composition contract: how do a base's answers compose with the meta's?](t7-meta-base-composition-contract.md) | grilling | T3, T8 | OPEN (blocked) |
| [T8 — Project-type taxonomy: which axes exist, who asks them, and what acts on them](t8-project-type-taxonomy.md) | grilling | T3 | OPEN — frontier |
| [T9 — License guidance: a choosealicense-style surface for the licensing decision](t9-license-guidance.md) | grilling | T3 | OPEN — frontier |

**Frontier:** T2, T5, T6, T8, T9.
