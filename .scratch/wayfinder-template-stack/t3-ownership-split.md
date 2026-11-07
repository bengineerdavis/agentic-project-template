# T3 — Ownership split: agentic layer inherits from the python repo — what moves, what's removed, when?

Type: grilling (HITL) · Blocked by: T1 · Blocks: nothing (graduated to T2, T5, T6, T7, T8, T9)
Status: RESOLVED (2026-11-06) · Claimed: Ben Davis (2026-11-04)

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

## Round 3 answers (maintainer, 2026-11-04)

- A named template stack selects a base, compatible overlays, and recommended
  compatible versions; an exact lock is optional. A project retains its chosen
  composition rather than automatically adopting later stack definitions.
- Task import preserves existing backlog history and quarantines imported
  external stores before migration. Idempotent, reviewable reports expose
  unsupported fields and conflicts; existing tasks are neither overwritten nor
  silently renumbered. Deterministic import is required, with agent-assisted
  semantic translation available where needed.
- The base owns task storage, identifiers, lifecycle, import boundaries, and
  the base task-operation contract. Agentic owns worktree-per-task enforcement,
  review integration, task claiming, and its other agent-specific rules.
- Fresh start is a replacement of workflow composition that preserves code and
  knowledge and quarantines replaced state behind a restorable backup. The
  maintainer requested a verb fitting alongside `adopt` and `migrate`; `reset`
  was selected after considering and rejecting `recompose`.
- Shared stack knowledge covers architecture and composition; domain and
  implementation expertise stays in the owning repository. Cross-reference
  knowledge rather than duplicating it.
- Cross-project coordination is split by operation, not by which repositories
  happen to be involved. Copier-cat helps set up and coordinate template
  composition. Redge coordinates repository presence and safe synchronization,
  including additional repositories or submodules in other directories. Redge
  itself need not push changes, create pull requests, or propagate updates.
  A separate push-it-forward effort may coordinate change propagation, calling
  the domain experts rather than embedding their logic. Each domain repository
  remains the expert for its domain: Python owns opinionated Python project
  creation; agentic owns adding agent processes to any suitable project.

## Round 4 refinements (maintainer, 2026-11-04)

- `recompose` overstates reuse of the previous workflow configuration. Use
  `reset` as the working verb beside `adopt` and `migrate`, with an explicit
  backup, preserved code and knowledge, and quarantined replaced state.
- Domain-specific expertise should be published as tool-agnostic operation
  contracts. Copier-cat consumes those contracts for template composition.
- The generic composition operation model is provisionally accepted, subject
  to concrete command and ownership examples.
- Redge is not the owner of template-driven pull requests or change propagation;
  its safe-sync boundary remains intact.

## Round 5 refinement (maintainer, 2026-11-04)

- Copier also records how improvements, refactors, and fixes from a generated
  project can return to the template stack that produced it.
- Copier-cat owns that template-feedback operation: classify the change against
  provenance, select the destination template, prepare reviewable changes, and
  require human approval before publication.
- Push-it-forward is a candidate reusable delivery mechanism underneath that
  operation, not the owner of template semantics. Copier-cat supplies the
  domain-specific mapping; the delivery mechanism must not assume one template,
  require fork management, or force synchronous fleet updates.
- Existing copier-cat C2 already calls this phone home. Its prepare-then-publish
  flow, per-file changesets, render-derived ownership map, and use of the
  maintainer's own authentication remain compatible with this boundary.

## Round 6 answers (maintainer, 2026-11-05)

- Push-it-forward is delivery-only. It makes sharing reviewable PR changes
  easier for human and agent contributors and maintainers, with a community
  software-improvement goal. Its contract accepts a prepared changeset,
  destination, verification policy, and publication policy without Copier or
  template semantics.
- Human approval is required before publication now. A future change class may
  permit automatic PR creation, but that is distinct from automatic acceptance
  or merging. The scale model remains open.
- Multi-domain feedback splits into independently reviewable proposals by
  default. Explicit grouped proposals and dependency ordering are reserved for
  genuinely cross-domain changes.
- Copier-cat distinguishes project-specific, template-worthy, and needs-review
  changes. Classification and labels are ultimately configurable.
- Stack definitions are versioned artifacts with tested compatibility records.
  Compatibility-affecting changes update that record as well as the affected
  overlay.

## Round 7 answers (maintainer, 2026-11-06)

Verified corrections to T1 and to the charting session's claims, made before
answering. Each is evidence-backed (see "Verification log" below).

- **The meta stamps template repositories, not projects.**
  `meta_template/<<template_dir>>/` holds only the answers-file placeholder, so
  a base's project-facing artifacts are hand-written today. Every "meta owns
  X" verdict must name its target: template repo, or stamped project.
- **Python's `template/LICENSE.jinja` is the project's license**, not a
  duplicate of the meta's repo-root `LICENSE`. Stamping the python base
  produced a `LICENSE` rendered from it. Dropping it would leave generated
  projects unlicensed.
- **The license choice sets run downhill, not uphill.** The meta asks 16
  (`license_type`, `copier.yml:182-202`); python's project renderer handles 2
  (MIT, FSL-1.1-MIT). Python is a strict subset — nothing to import upward.
  The gap is that a stamped project cannot receive Apache-2.0 or any of the
  other 14 even though the meta asks for them.
- **`renovate.json` already has its conditional** (`tool_update_strategy`,
  gated on `vcs_platform == 'github'`, default `'none'` otherwise).
- **`.gitignore` is stamped by python** (`template/.gitignore`, verified in a
  stamp) and composed by agentic per-tool `gitignore.txt` fragments. T1's
  "not stamped" was wrong; composition exists in part already.
- **The word "base" has two referents.** ADR-0002: the noun template (python).
  T3 R2/R3: "the shared base" meaning the meta-provided agnostic artifact.
  Resolved below by adopting the ADR-0002 vocabulary throughout.
- **Real defect found:** `agentic-project-template/template/.alint.yml`
  hardcodes `alint://bundled/python@v1` (and a second `ci/github-actions`
  entry). The agentic overlay asserts the Python noun and duplicates the
  meta's `vcs_platform` responsibility — two overlays claiming one concern.

Answers:

- **Vocabulary (Q2):** meta → makes bases. base → the NOUN. overlay →
  ADJECTIVES, plural, peer domains. A **stack** is one base plus one or more
  base-compatible overlays plus composition provenance. Adopted as the single
  vocabulary for this effort.
- **Placement rule (Q3), replacing the two competing criteria:** *meta owns
  what every base needs to make a base; base owns what every project needs;
  overlay owns what only a domain needs.* The earlier pair (concerns move to
  meta iff language-agnostic AND every project wants it | concerns move down
  to base if that yields fewer, less complex overlays) is superseded. Both
  survive as intuitions, neither as the rule.
- **Layering is the norm, not the exception (Q5).** Files needing the
  meta-base-overlay chain: CONTRIBUTING.md, .gitignore, CODING_STANDARDS.md,
  .alint.yml, LICENSE, AGENTS.md, mise.toml, prek.toml, opencode.json. T3
  records the ownership per file; T2 designs the merge mechanism once.
- **Licensing propagates three ways (Q1).** The meta owns the choice set and
  the SPDX text corpus. It must ask, at base-creation, which licenses that
  base's projects may choose from (default: the full set), and seed the corpus
  plus a renderer into `<<template_dir>>`. A base may narrow the set; it must
  not reimplement the corpus. Today the chain breaks at hop 2:
  `meta_template/copier.yml.tmpl` seeds no license keys at all.
- **New tickets approved (Q4):** T7 (meta↔base composition contract), T8
  (project-type taxonomy), T9 (license guidance surface).
- **alint layering (Q6):** alint is a layered file like the rest — the bundle
  set is conditional on the chosen base and overlays. The hardcoded `python`
  bundle is a T5 defect.

## Correction (2026-11-06, adopted from T2 Q5 option iii)

The Round 7 vocabulary put **python** in the "base (noun)" column. The
maintainer challenged that in T2 and is right: language is an adjective over
the noun, not the noun. The four type axes are language-agnostic, and the
model's own claim ("python and agentic are BOTH adjectives") only holds if
neither is the base.

**Transitional ruling.** An agnostic base is the target end state. Until one
exists, python plays the noun role, and that role is **temporary scaffolding**,
recorded as such. Read the "Base (noun)" column below as *"the layer currently
playing the noun role"* — today python, eventually an agnostic base that owns
the language-independent rows now sitting in the meta column.

## Per-concern verdicts

Each of T1's nine concerns plus lore gets an owner and the round that settles
it. Cells name the artifact each rank owns in that row; "—" means the rank has
no stake.

| Concern | Meta | Base (noun) | Overlay (adjective) | Settled by |
|---|---|---|---|---|
| **AGENTS.md** | agnostic base shape + "what is this repo" backlinks | language commands section (mise tasks, test/lint) | agentic managed section (workflow rules, tool bullets) | R2 + R7 (Q5) |
| **backlog / task mgmt** | — | scaffold, tool pin, idempotent init, storage + ids + lifecycle + import boundaries, task-operation contract | worktree-per-task enforcement, review integration, task claiming | R2, R3 |
| **LICENSE** | choice set + SPDX corpus + which-set-does-this-base-offer question | project renderer `template/LICENSE.jinja` over the inherited corpus; may narrow the set | — | R7 (Q1) |
| **CONTRIBUTING.md** | base shape (dev setup, test suites, quality gate) | language-specific contribution + style sections | domain contribution sections (agent workflow et al.) | R7 (Q5) → mechanics in T2 |
| **alint** | `.alint.yml` scaffold + profile/bundle questions + `ci/<vcs>` bundle | language bundle (`python`, `node`, …) | agentic structure bundles (`agent-hygiene`, `agent-context`), binary pin, hook | R2 + R7 (Q6) → defect to T5 |
| **CODING_STANDARDS.md** | agnostic defaults | language conventions pointer (PYTHON.md, …) | judgement-call / vacuity-guard section | T2 |
| **CHANGELOG.md** | template-repo changelog (today hand-maintained, not stamped); optional project changelog scaffold | project changelog renderer (`template/CHANGELOG.md.jinja`, exists), release semantics for the language | — | derived, not maintainer-decided |
| **.gitignore** | agnostic lines (editor, OS, secrets) | language lines (caches, build dirs) | tool lines (`.roborev/`, dotagents) | R7 (Q5) |
| **renovate.json** | existing `tool_update_strategy`, gated on `vcs_platform == 'github'` | language-tool update managers (uv, cargo, npm) contribute their regex managers | — | R7 (C4: already built) |
| **lore knowledge** | stack-level architecture + composition knowledge in the parent templates scope | — | stamped-project `.lore.md` seed; domain expertise stays agentic-owned | R2 |

**Exception in the .gitignore row:** `python-project-template/template/.gitignore`
carries `.worktrees/` ("one worktree per task; gitignored"). That is
agentic-overlay content sitting in the base. It moves to the overlay — a base
stamped with no overlays should not know about worktrees.

No concern is left unowned. Five spawn work rather than verdicts: T2 (merge
mechanics for the layered files), T5 (alint bundle layering + the hardcoded
`python` defect), T7 (composition contract), T8 (type taxonomy), T9 (license
guidance).

## Verification log (2026-11-06)

Empirical, reproducible from the repos:

- `meta_template/<<template_dir>>/` listing → one answers-file placeholder.
- `meta_template/copier.yml.tmpl` grep for `license|copyright` → no matches;
  question keys are `template_name` + the pydantic example only.
- `uvx copier copy python-project-template <tmp> --defaults` (with
  `project_name`/`author_name`/`author_email` supplied) → `LICENSE`,
  `.gitignore`, `CHANGELOG.md`, `prek.toml`, `mise.toml`, `pyproject.toml`,
  `src/<slug>/cli.py`, `tests/test_cli.py`. Confirms python stamps the project
  license, the gitignore, and an unconditional CLI.
- `python copier.yml` `license` choices → MIT, FSL-1.1-MIT (2).
- `copier-template-copier-template copier.yml:182-202` `license_type` → 16
  choices including both FSL variants.
- `python template/prek.toml.jinja` → ruff only, with a comment stating alint
  owns trailing whitespace, final newlines, and merge markers.
- Root-level `prek.toml` files in python and agentic DO carry
  end-of-file-fixer / trailing-whitespace — so the overlap alleged against
  stamped projects does not exist, but the template repos' own self-hosting
  does contradict the alint fragment's own claim. Self-hosting contradiction
  belongs to T5.

## Resolution

Language-independent structure, generic project tools, task storage, and the
task-operation contract belong to the meta's agnostic scaffold (the artifact
every base inherits) and to the base that acts on it. Python and agentic
contribute only their respective domain expertise through tool-agnostic
contracts. They do not implement separate stack-management systems.

Ownership is by domain, not by layer position. Python and agentic are peers,
both adjectives over the base's noun.

Copier-cat orchestrates composition and owns phone home: provenance analysis,
classification, destination selection, and preparation of reviewable template
changes. It may use push-it-forward for delivery, but the delivery layer does
not decide ownership. Redge keeps repository presence and safe-sync
responsibilities, without being made a PR or propagation owner.

Named stacks select compatible versions. A project's composition record fixes
its chosen provenance. Adopt, migrate, and reset preserve the accepted safety
boundaries; reset replaces workflow configuration after a restorable backup,
quarantines replaced state, and preserves code and knowledge. External task
stores enter through quarantine with reviewable migration reports.

Lore remains agentic-owned in stamped projects. The parent templates scope
holds shared architecture and composition decisions; repository scopes retain
domain expertise. Copier-cat's C2 and later chooser work consume this boundary
through their own plans.

A **stack** is one base plus one or more base-compatible overlays plus
composition provenance. The placement rule is layered by who needs the
concern: meta for what every base needs, base for what every project needs,
overlay for what only a domain needs.

Every one of T1's nine concerns now has an owner (see "Per-concern verdicts").
The work T3 unblocks is ticketed, not fogged: T2 (merge mechanics for layered
files), T5 (alint bundle layering), T7 (meta↔base composition contract), T8
(project-type taxonomy), T9 (license guidance). No ownership decision remains.

Status: RESOLVED (2026-11-06) · Claimed: Ben Davis
