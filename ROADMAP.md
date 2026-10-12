# Roadmap

> Early-stage, single-maintainer project. Items outside **Landed** are
> directions, not commitments; priorities move with what the loops teach us.

## Landed

- (nothing yet — v0.1 work is tracked as backlog tasks `apt-1`…`apt-8`)

## Current priorities

### v0.1 — Loop-complete stamp

The layer stamps end-to-end for its original purpose: play with roborev and
fast/slow looping on real projects.

- Template + CLI skeleton (this scaffold), merge logic for shared files
- roborev wired (install/init/status/fix tasks, post-commit hook)
- slow loop (`review-deep` agent + `docs/reviews/` report + retro section)
- dotagents project wiring (2–3 default skills, MCP question, `add-mcp` skill)
- alint config + prek wiring + AGENTS.md sync
- stamp matrix green (layer-only, with-base, existing-project merge)

### v0.2 — Absorb the sandbox

- Port git-ai opt-in from copier-mise-sandbox (tasks, docs, glossary)
- copier-mise-sandbox becomes a thin consumer of this template
- consult-llm opt-in verified against the opencode backend

## Planned work

### Automation endgame (skill + CLI)

- dotagents-installable skill wrapping the CLI: an agent applies the layer
  to a project with no human typing
- `update` command exercising both answers files on a real stamped project

### Wider agent surface

- Second agent target (claude or codex) via dotagents targets, once
  opencode-first proves the shape

### Agentic-context linting (the layer enforcing itself)

- Lint the layer's own artifacts — `AGENTS.md`, stamped skills, prompts —
  against the prompt-spec standard (promptlint) and skillet grammar
  (`skillet validate`), wired through the same prek + agent-output plumbing
- Reconcile with alint's `agent-context` ruleset per the no-overlap rule:
  whatever promptlint covers, alint stops enforcing

### Prose & docs linting (base-template lane)

- vale / flowmark / codespell / lychee wired by BASE templates that want
  documentation quality gates, per the house writing standard; the agentic
  layer does not stamp prose linters

### Layer growth, only when earned

- File-isolation tooling (worktree manager) if the convention proves limiting
- Stronger environment isolation (containers/nix) as an L0 strategy

## Deferred

- PyPI publication (git + uvx is enough until a second machine needs it)
- Multi-model review panels (roborev multi-agent PR review) — evaluate after
  the fast loop has run on real work
