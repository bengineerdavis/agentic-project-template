# T7 — Meta↔base composition contract: how do a base's answers compose with the meta's?

Type: grilling (HITL) · Blocked by: T3 (resolved), T8 · Blocks: T2, T4
Status: OPEN (blocked on T8) · Claimed: nobody

## Question

T1 called this "the refactor's hardest decision": the meta and the base have
**no composition contract**. T3's per-concern verdicts assume one exists —
every row says "meta owns X, base owns Y" — but nothing yet defines how the
meta's answers reach a base, or how a base declares what it accepts.

Three mechanics are missing, and they are separable:

1. **Variable flow.** How does a value the meta asked reach the base's
   renderer? ADR-0002 §3 names two channels: a shared answers file seeded via
   `--data` (target, copier-cat C3) and `external_data` (the fallback that
   works in plain Copier 9.18.2 today). Neither is wired.
2. **The manifest.** ADR-0002 §2 requires a base to publish `provides:` and
   `extends:` in its `copier.yml`. Verified 2026-11-06: **neither python nor
   agentic declares either field**, and no tooling checks them. The contract
   exists only as review-enforced prose in an unmerged ADR.
3. **Seed vs hand-write.** The meta currently seeds template repos with
   authoring harness (`meta_template/*.tmpl`) but leaves
   `meta_template/<<template_dir>>/` empty. Anything project-facing in a base
   is hand-written, which is why python's project license renderer covers 2 of
   the meta's 16 licenses. Deciding what the meta seeds into `<<template_dir>>`
   is deciding the contract's teeth.

This ticket decides the mechanics **once**, so each concern move is a pattern
instance rather than a new design. T4 (migration mechanics) cannot plan moves
until this lands.

## Status note

Round 1 answered 2026-11-06: the shape of the contract is decided (option c).
What remains is (a) T8's axes, which populate `provides:`, and (b) the open
sub-decisions below — where the convention lives, which channel carries
values, and whether enforcement is tooling or review. Still blocked on T8 for
the manifest's contents.

## Why blocked on T8

The manifest's contents depend on the type axes: if a base `provides:
[is_distributed, has_entry_point, gui, owns_service_lifecycle]`, that is a
different manifest from one that provides none. T8 settles the axes; T7
settles how they travel.

## Round 1 answers (maintainer, 2026-11-06)

- **Where compatibility lives — option (c), approved** ("open to c"): the meta
  owns the *convention*; bases publish *extension points*; overlays declare
  *requirements*. The meta providing the convention is consistent with T3's
  placement rule ("meta owns what every base needs"). The meta must **not**
  build the overlays themselves — that would push language knowledge up, which
  is what the whole model resists. One genuine exception: an overlay whose
  domain is truly language-agnostic (services, CI) is a legitimate
  meta-provision candidate. Agentic is not — not every base wants agent
  practices.
- **Two overlay kinds, approved.** A **bound overlay** ships with a base and
  extends only that base; it needs no cross-base contract. A **portable
  overlay** extends any base that publishes the contract. The trunk question
  exists **only for portable overlays**. Recorded in `.context/glossary.md`.
- **Copier-cat owns the compatibility matrix, approved.** Testing the
  base × overlay matrix and recording which pairs are verified is the stack
  manager role. Grounded in T3 R6: "stack definitions are versioned artifacts
  with tested compatibility records."
- **The trunk is the contract, not shared data, approved for now.** The
  contract (plus T8's type axes) is the trunk. Shared *values* are a separate
  concern — this ticket's variable-flow channel. Conflating them is what made
  "a shared trunk of data" sound like a meta-owned artifact.

### The model, and why the class analogy needs one correction

The maintainer's analogy: a base is like a Python base class that enforces
typing for its instances; overlays are like classes that extend or define the
base for a given project. **Right instinct, wrong mechanism.** A Copier
overlay does not inherit the base's *implementation* — it receives the base's
*output files*. So it decorates an **instance**, not subclasses a class. There
is no `super()`. Nothing is inherited, therefore nothing is guaranteed. That
gap is precisely why the contract has to be written down.

Consequence for the multi-base problem: N bases × M overlays stays tractable
without centralising language knowledge, because the contract is the only
shared thing. Bases publish their extension points; overlays ship per-base
adapters where behaviour genuinely differs.

### What agentic does today (verified, and it is the problem)

- `merge.py:deep_merge` is pure, idempotent, **base-wins** — fills gaps,
  overwrites nothing.
- `cli.py` takes `--base` as an opaque copier ref. **No validation, no
  requirement check.**
- `test_layer_stamp_existing_project_preserves_base` proves quiet
  compatibility: a python-flavoured `mise.toml`, a `node_modules/` gitignore,
  and a `.pre-commit-config.yaml` all accept the overlay silently.

Agentic is multi-base compatible today **by never declaring what it needs**.
Quiet compatibility detects nothing and applies everything. The measured cost
is already in T3/T5: python-only projects get no hygiene enforcement because
the overlay was supposed to supply it and never said so.

## Prototype — does (c) actually catch our failures?

`prototype/composition-contract.html` (throwaway, single file, double-click to
open). It models the convention — base publishes `axes` /
`extension_points` / `bundles`; overlay declares the subset it requires — and
toggles between **today (quiet)** and **with contract**.

Verified by running its logic headlessly:

| Mode | Base | Overlays | Result |
|---|---|---|---|
| contract | python | agentic | applied |
| contract | python | agentic_bug¹ | **refused** — claims bundle `python` already claimed by base |
| contract | python | django (bound) | applied |
| contract | chezmoi | agentic | applied |
| contract | chezmoi | django (bound) | **refused** — bound to python |
| contract | chezmoi | services | **refused** — requires axis `owns_service_lifecycle` |
| quiet | python | agentic_bug¹ | stamped, **1 silent gap** |
| quiet | chezmoi | django (bound) | stamped, **3 silent gaps** |
| quiet | python | services | stamped, **1 silent gap** |

¹ `agentic_bug` is shaped like the real defect — `template/.alint.yml`
hardcoding `alint://bundled/python@v1`.

Two things the prototype established:

1. **The contract catches all three failure classes we actually found**
   (overlay claiming the base's language concern, bound overlay on the wrong
   base, missing axis) — all before a file is written.
2. **Agentic is genuinely portable** — it applies cleanly to `chezmoi` too,
   because it declares workflow requirements, not language ones. The model is
   sound; only the declaration is missing.

Its second effect is the more useful one: in quiet mode every gap is
*invisible*, which is exactly why these defects survived to T3.

Capture: when T7 lands, fold the verdict into the ticket and commit the
prototype to a throwaway branch as a primary source (prototype skill rule 6).
Main keeps only the decision.

## Open sub-decisions

- Does the stack put `provides:`/`extends:` in each base's `copier.yml`
  (ADR-0002 as written), or in a separate manifest file the meta reads?
- Does the meta seed a base's *project-facing* files, or only its authoring
  harness? (T3's license verdict presumes seeding.)
- Which channel ships first: `external_data` (works today) or the shared
  answers file (needs copier-cat C3)?
- Is enforcement tooling in scope here, or review-only until copier-cat
  Phase 3?
- Where does the **convention** live so both bases and overlays read the same
  schema — the meta's `GLOSSARY.md`, a JSON Schema the meta stamps, or ADR-0002?

## Context

- `.scratch/wayfinder-template-stack/t3-ownership-split.md` — the verdicts
  this contract must make real.
- `.worktrees/ctct-12-template-taxonomy/docs/adr/0002-template-taxonomy-and-composition-contract.md`
  (copier-template-copier-template, **unmerged**) — `provides:`/`extends:`,
  variable-flow channels.
- CTCT-12 (meta repo backlog, In Progress) already records the taxonomy
  decisions. T7 must not duplicate it: **if CTCT-12 lands ADR-0002 on main,
  T7's scope shrinks to enforcement + mechanism.** Check CTCT-12's status
  before starting.
