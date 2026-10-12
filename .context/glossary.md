# Glossary

Tier 1. Terms used across this repository; link on first use in docs.

- **agentic layer** — the set of stamped concerns this template owns
  (L0–L7); everything an agent needs to work in a project that is not
  language, build, or personal configuration.
- **base template** — a copier template owning language/framework/build
  concerns; composed underneath this layer by the CLI.
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
