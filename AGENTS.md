# AGENTS.md

Copier template repo: the agentic layer, composed over base templates.
The spec constrains (`@spec.md`); the layer map describes
(`@ARCHITECTURE.md`). Read both before changing template behavior.

## Commands

- `mise run install` — tools, venv, hooks
- `mise run test` — merge-logic unit tests
- `mise run test-template` — stamp matrix (layer-only, with-base, existing)
- `mise run lint` — prek hooks (tombi formats all `*.toml`)

## Repo map

- `copier.yml` — layer stamp questions (`_answers_file: .agentic-answers.yml`)
- `template/` — the product: what the layer stamps (clean paths only)
- `src/agentic_project_template/` — CLI: composition + deterministic merges
- `fragments/` — shared-file layer fragments (mise, prek, gitignore, AGENTS.md
  section) applied by the CLI merge step; single source for those merges

## Context loading (on demand)

- Why the layer looks this way / decisions → @spec.md (Decision record)
- Layer map, merge table, composition flow → @ARCHITECTURE.md
- Task store → `backlog/` (`uv run backlog-py board`)

## Project rules

Read `.context/ai-rules.md` — auto-loaded in opencode sessions via
`opencode.json` `instructions`.
