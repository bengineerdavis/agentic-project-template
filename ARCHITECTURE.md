# Architecture

This document is the descriptive source of truth for the agentic layer's
sub-layers. The spec constrains (one concern per layer; deterministic merges
through the CLI); this file maps the layers to what gets stamped and which
tool owns each concern. Where this file and the spec disagree, the spec wins
and this file is fixed.

## The stack

A stamped project is read from the bottom up. Base templates own everything
about the language and the code. The agentic layer stacks on top and owns only
the concerns below.

```
┌──────────────────────────────────────────────────────────────┐
│ L7 attribution        git-ai (opt-in), experiments log       │
│ L6 enforcement        alint + prek/tombi, AGENTS.md sync     │
│ L5 task management    backlog/ store (backlog-py), apt- ids │
│ L4 review loops       fast: roborev · slow: review-deep      │
│ L3 LLM dependencies   agents.toml, dotagents, MCP, skills    │
│ L2 agent orchestration AGENTS.md router, .context, agents    │
│ L1 file isolation     worktrunk (wt): one worktree per task  │
│ L0 environment        mise.toml, mise.local.toml, aboyeur    │
├──────────────────────────────────────────────────────────────┤
│ BASE                language · build · test · code linting   │
└──────────────────────────────────────────────────────────────┘
```

## Layers

### L0 — Environment & sandboxing

One concern: how the project's tools and runtime environment are declared,
installed, and verified.

- Owned by: `mise.toml` (layer fragment, merged), `mise.local.toml`
  (personal, gitignored), `[bootstrap.packages]` host deps.
- Compatible with: aboyeur (agent-driven headless mise configuration) and
  `mise doctor project` — the fragment stays minimal and conventionally
  shaped so a configurer extends it rather than rewrites it.
- Stamped: always.
- Deferred strategies: containers, nix — a project may need stronger
  isolation than mise provides; that would be an additional strategy inside
  this layer, not a new layer.

### L1 — File isolation & worktrees

One concern: parallel agent work without stepping on each other's files.

- Owned by: worktrunk (the `wt` binary, pinned `0.80.0` via the mise
  registry name) plus the one-worktree-per-task convention.
- Layout: `{{ repo_path }}/.worktrees/{{ branch | sanitize }}` — inside
  the repository, gitignored. The path template is **user-level config**
  (`~/.config/worktrunk/config.toml`, chezmoi-managed): worktrunk
  deliberately treats worktree placement as personal, so the layer cannot
  and should not stamp it. Set once, applies to every repo.
- Stamped (apt-13): `.config/wt.toml` — committed project config — with
  `post-start = "mise trust && mise run install"` (bootstrap on first
  entry) and `pre-merge = "mise run check"` (verify before merging), plus
  the tool pin and workflow docs. Project hooks run only after first-run
  approval; consent is built into the tool and must not be bypassed.
- Merge policy: `merge.squash = false` pinned in project config. A task's
  commit series survives the merge — one reviewable decision per commit is
  the house rule, and the fast loop reviewed each commit individually.
- Branch naming: branches are worktree addresses; task branches are named
  from the backlog task id (`apt-N-slug`), so `wt switch apt-12-…` is the
  entire navigation model.
- Deferred: LLM commit generation (supported by worktrunk; user-level,
  opt-in per the shrink principle); per-worktree dev-server URLs
  (`hash_port`) where projects have servers.
- Rationale: isolation is what makes the loops trustworthy; a review of a
  dirty shared worktree reviews noise. Adopted 2026-10-12; design
  confirmed with the maintainer 2026-10-13.

### L2 — Agent orchestration

One concern: how agents learn to work here and who does what.

- Owned by: `AGENTS.md` (router section, merged), `.context/` two-tier
  knowledge (Tier 1 injected, Tier 2 lazy `@docs/` references), `.opencode/`
  agent definitions, dotagents subagents.
- Stamped: always.
- consult-llm (second opinions, `/consult`, `/debate`) lives here, opt-in.

### L3 — LLM dependency management

One concern: every skill, subagent, and MCP server an agent could be asked to
use is declared, pinned, and installable.

- Owned by: `agents.toml` (project scope), `dotagents --project install`
  mise task, stamp-time MCP question, `add-mcp` skill.
- Stamped: always (2–3 default skills; consult skills only with consult-llm).

### L4 — Review loops

One concern: work is reviewed continuously at two speeds.

- Fast loop: roborev — daemon + post-commit hook, findings ledger, fix while
  context is fresh. Stamped: always.
- Slow loop: `mise run review-deep` — non-interactive opencode review agent,
  branch-vs-base, dated report in `docs/reviews/`, retro section naming AI
  usage worth shrinking to deterministic tooling. Stamped: always; scheduled
  at user level (chezmoi cron), never in the project.

### L5 — Task management

One concern: agent work is defined and assigned before it starts.

- Owned by: backlog (backlog-md-py) — markdown task files under `backlog/`,
  ids prefixed `apt-`; acceptance criteria and definition-of-done state what
  done means; `backlog-py board`/`overview` for scanning; `backlog-py-mcp`
  is the agent-facing surface.
- Stamped: `backlog init` via the idempotent `backlog-init` mise task.
- Adopted 2026-10-12, replacing the TASKS.md convention.

### L6 — Structure enforcement

One concern: the repository keeps its shape without a reviewer remembering it.

- Owned by: `.alint.yml` (agent-hygiene, agent-context, oss-baseline, gated
  ecosystem rulesets), prek wiring, `alint export-agents-md` sync so
  `AGENTS.md` matches the enforced rules.
- Stamped: always.
- Division of labor (no overlapping checkers). One wiring mechanism — prek
  hooks, CI, the `agent` output format — carries four checker families, each
  with its own concern and rule source:

  | Family | Concern | Rule source | Tools | v1 |
  | --- | --- | --- | --- | --- |
  | Structure & content hygiene | repo shape, file existence/naming, whitespace, newlines, merge markers | alint bundled rulesets + project `.alint.yml` | alint | stamped |
  | Code/config semantics | language correctness of code and config files | base template | tombi (gate stamped by the layer), ruff, … | base-owned |
  | Prose & docs | documentation quality: plain language, spelling, links | house writing standard (dotfiles spec) | vale, flowmark, codespell, lychee | future lane |
  | Agentic context | quality of the layer's own artifacts: `AGENTS.md`, skills, prompts | prompt-spec standard; skillet grammar for skills | promptlint; skillet validate; alint `agent-context` (structural subset) | future lane |

  The layer's hook fragment contributes only the tombi gate and the alint
  gate. Generic pre-commit builtins are the base template's business. Where a
  project already runs a dedicated tool for something alint enforces, that
  tool wins and the alint rule is switched off.

- Agentic-context linting is the layer enforcing itself: same wiring as every
  other family, but its rule sources are the prompt-spec standard (prompts,
  agent files) and skillet grammar (skills). It is layer-owned because it
  governs layer artifacts. When it lands, alint `agent-context` rules it
  supersedes are switched off in `.alint.yml` — the no-overlap rule applies
  inside this table too.

### L7 — Attribution & provenance

One concern: who wrote what, and what was learned.

- Owned by: git-ai (line-level attribution), opt-in; `docs/experiments.md`
  method and log (the [harness]/[variable] discipline inherited from
  copier-mise-sandbox).
- Stamped: opt-in flag; experiments log always.

## Shared files and the merge rule

Several layers legitimately touch the same file. The rule (spec: Composition
— the layer never clobbers what it lands on) is that the CLI owns every such
merge deterministically:

| Shared file | Touched by | Merge |
| --- | --- | --- |
| `mise.toml` | L0 fragment | TOML deep-merge of `[tools]`/`[tasks]` |
| `prek.toml` | L6 hooks | TOML `[[repos]]` merge; a legacy `.pre-commit-config.yaml` is appended to in its own format instead, so prek never drops existing hooks |
| `.config/wt.toml` | L1 worktree hooks | TOML deep-merge (base wins per key), created when absent |
| `.gitignore` | L0, L4, L7 entries | append missing lines |
| `AGENTS.md` | L2 router | insert marked section, idempotent |

Everything else the layer stamps lives in paths no base template owns
(`.context/`, `.opencode/`, `.agents/`, `agents.toml`, `.alint.yml`,
`docs/reviews/`, `docs/experiments.md`), so pure `copier copy` onto an empty
directory works without the CLI, and the CLI exists to make cohabitation with
existing and base-stamped projects safe.

## Composition flow

```
agentic-project-template new  --base gh:bengineerdavis/python-project-template dst
  1. copier copy base   → dst            (base's own .copier-answers.yml)
  2. copier copy layer  → dst            (.agentic-answers.yml, clean paths)
  3. deterministic merges               (mise/prek/gitignore/AGENTS.md)
  4. stamp test asserts invariants

agentic-project-template layer dst            # existing project, layer only
agentic-project-template update dst           # copier update, layer answers only;
                                              # the base layer is updated separately
                                              # with its own answers file
```

The CLI invokes copier; it does not reimplement it. The endgame is a dotagents
skill driving this CLI so setup is fully automated.
