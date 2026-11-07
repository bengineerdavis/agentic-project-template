# Glossary

Tier 1. Terms used across this repository; link on first use in docs.

- **agentic layer** — the set of stamped concerns this template owns
  (L0–L7); everything an agent needs to work in a project that is not
  language, build, or personal configuration. As a composition unit it is an
  **overlay** (see below); "layer" names the inner concern set only.
- **base** — the noun: what kind of repo a project is. A base decides that;
  overlays adjust to it. Not to be confused with the meta's agnostic scaffold,
  which every base inherits. **Transitional:** python currently plays the noun
  role because it is the only template that produces a project. The target is
  an agnostic base with language (python) as an adjective over it — language
  describes the project, it is not the project.
- **overlay** — an adjective over a base: one composable sub-domain (language,
  agent practice). Plural, peer domains — no overlay outranks another. The
  agentic concerns are one overlay; so are python's.
- **bound overlay** — ships with one base and extends only that base
  (a `django` overlay bound to python). Needs no cross-base contract; the
  author knows the base.
- **portable overlay** — extends any base that publishes its extension points
  (agentic is one). Must declare what it requires; refuses to stamp on a base
  that does not provide it.
- **composition contract** — what makes a portable overlay safe: the base
  publishes its extension points and the overlay declares its requirements.
  Composition happens over the base's *output files*, not its implementation
  — an overlay decorates an instance, it does not subclass a class.
- **stack** — one base, its base-compatible overlays, and the composition
  provenance recording which versions were used.
- **fast loop** — per-commit background review (roborev): findings ledger,
  fix while context is fresh.
- **slow loop** — scheduled deep review (`review-deep`): branch-vs-base,
  dated report in `docs/reviews/`, retro section naming AI usage to shrink.
- **layer fragment** — a small file in `fragments/` that the CLI merges into
  a shared file deterministically.
- **shrink** — converting repeated AI usage into deterministic tooling
  (tasks, hooks, linter rules); the retro loop proposes it, Pareto filters it.
- **stamp matrix** — the test that renders the template's branches
  (layer-only, with-base, existing-project merge) and asserts invariants.
- **two answers files** — base's `.copier-answers.yml` + layer's
  `.agentic-answers.yml`, keeping both layers independently `copier
  update`-able.
- **layered file** — a shared file assembled from all three ranks (e.g.
  CONTRIBUTING.md, .gitignore, AGENTS.md, .alint.yml, CODING_STANDARDS.md).
  The norm for shared files, not an exception; the merge mechanism is designed
  once.
