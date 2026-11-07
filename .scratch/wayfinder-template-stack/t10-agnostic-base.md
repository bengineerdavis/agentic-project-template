# T10 — The agnostic base: build the noun python is currently standing in for

Type: grilling → build (HITL) · Blocked by: T7, T8 · Blocks: nothing (enables the target model)
Status: OPEN (blocked) · Claimed: nobody

## Why this ticket exists

T2 Q5 (option iii, adopted 2026-11-06) settled that **language is an adjective,
not the noun**. Python describes a project; it is not what the project is. The
target model is an agnostic base with language supplied as an overlay.

But no agnostic base exists. `python-project-template` is the only template
that produces a working project, so it currently *plays* the noun role — and
that role is recorded everywhere as temporary scaffolding (glossary, T3's
verdict column, the handoff).

This ticket is the exit from that scaffolding. Without it the transitional
ruling in T2 has no destination, and the model's own claim ("python and agentic
are peers, both adjectives") stays false in practice.

## The question

What does an agnostic base contain, and what makes it usable alone?

The tension is already recorded: an agnostic base with no language, build, or
test runner stamps almost nothing and cannot be used on its own. Ping through
either:

- **(a)** The agnostic base is not a standalone product. It is the layer
  python composes over, and its "usability" is the fact that every base built
  on it is complete. Nobody stamps it directly.
- **(b)** The agnostic base must be usable alone, which forces it to pick a
  default language — which makes it not agnostic.
- **(c)** The agnostic base ships a minimal toolkit (mise, prek, alint, git
  hygiene, docs skeletons) that is genuinely useful with no language at all
  (a dotfiles repo, a docs repo, a monorepo root).

## Starting inventory (from T3's verdict table)

Rows currently sitting in the **meta** column that are really *base* concerns
once an agnostic base exists:

- agnostic structure and generic project tools
- task storage and the task-operation contract (backlog scaffold, pin, init)
- the language-agnostic halves of AGENTS.md, CONTRIBUTING.md,
  CODING_STANDARDS.md, .gitignore, LICENSE, .alint.yml
- hygiene enforcement (the T5 finding: a base must be correct standalone, so
  hygiene cannot be delegated to an overlay)

## Dependencies

- **T7** — the meta↔base composition contract. An agnostic base is the first
  real consumer: it must publish extension points for language overlays.
- **T8** — the type axes. An agnostic base is the layer that acts on them.

## Non-goals

Not a rewrite of `python-project-template`. Under option (iii) python keeps
working as it does today; this ticket adds the layer beneath it and records the
split, so python can later shed its noun role incrementally.
