# agentic-project-template

A [copier](https://copier.readthedocs.io) template that adds an **agentic
layer** to any project — new or existing — plus a small Python CLI that
composes it with a base template.

The layer installs review loops (fast: roborev per commit; slow: scheduled
deep review), agent orchestration (AGENTS.md router, `.context` knowledge,
opencode agents), LLM dependency management (dotagents `agents.toml`, skills,
MCP), structure enforcement (alint), and the task/attribution conventions —
and nothing about your language or build. Those live in base templates.

- Layer map and merge rules: [ARCHITECTURE.md](ARCHITECTURE.md)
- What must stay true: [spec.md](spec.md)
- What's next: [ROADMAP.md](ROADMAP.md)

## Usage

```bash
# new project: base template first, agentic layer on top
uvx --from git+https://github.com/bengineerdavis/agentic-project-template \
  agentic-project-template new my-project --base gh:bengineerdavis/python-project-template

# existing project: layer only (asks before stamping a base)
uvx --from git+https://github.com/bengineerdavis/agentic-project-template \
  agentic-project-template layer .

cd my-project && mise run install
```

Direct copier works too, onto an empty directory:

```bash
copier copy gh:bengineerdavis/agentic-project-template my-project
```

## What a stamped project gets

| Layer | Files |
| --- | --- |
| Environment | `mise.toml` fragment merged in (roborev, alint, dotagents, prek, tombi, opencode pins + tasks) |
| File isolation | worktrunk (`wt`) + one-worktree-per-task workflow docs |
| Orchestration | `AGENTS.md` section, `.context/ai-rules.md` + `glossary.md`, `.opencode/agents/review-deep.md` |
| LLM deps | `agents.toml` (pinned skills, subagents, MCP), `dotagents --project install` task, `add-mcp` skill |
| Review loops | roborev tasks + hook, `mise run review-deep`, `docs/reviews/` |
| Task management | `backlog/` task store (backlog-py), initialized by the `backlog-init` task |
| Enforcement | `.alint.yml`, prek hooks |
| Attribution | `docs/experiments.md`; git-ai tasks/docs (opt-in) |

Opt-in: `include_consult_llm` (second opinions via consult-llm), `include_git_ai`,
`mcp_servers`, `extra_skills` — see `copier.yml`.

## Developing this template

```bash
mise run install
mise run test           # merge-logic unit tests
mise run test-template  # stamp matrix into /tmp/opencode/stamp-matrix
mise run lint           # prek hooks, tombi formats TOML
```

Every template change must pass the stamp matrix — see spec, Behavior:
Verification.
