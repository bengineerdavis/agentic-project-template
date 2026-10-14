# agentic-project-template

## Intent

This repository is a copier template that adds an agentic layer to any project,
new or existing, plus a small Python CLI that composes it with a base template.

The layer exists so the maintainer can discover, explore, research, experiment,
test, and apply agentic processes across all projects, and so preferences and
learnings about those processes accumulate in one place instead of per-project
scattered state.

Three principles govern every behavior below. They are principles, not firm
rules; a behavior may be revisited when they conflict.

1. **Tools extend the human, not replace.** The layer equips a maintainer; it
   does not act unattended on their behalf.
2. **Shrink AI to the best tradeoff.** Repeated AI usage is refactored into
   deterministic tooling (hooks, tasks, linters) whenever a deterministic
   alternative exists. AI remains only where it is the best tradeoff or adds
   adaptability deterministic code lacks.
3. **Experiment tolerance.** While a workflow is experimental, a wider surface
   for AI usage is accepted. The opportunity to shrink is looked for, not
   forced. `docs/experiments.md` (inherited from copier-mise-sandbox) is where
   the opportunity is recorded and the slow loop acts on it.

Document division. `README.md` explains and shows usage. `ROADMAP.md` says what
is likely next. `backlog/` is the task store (backlog-py; ids `apt-…`). This
file constrains. Where a doc
and this file disagree, the doc is describing and this file is constraining —
fix the doc.

The name. The repository, PyPI package, and CLI are all
`agentic-project-template`. No short alias is shipped; personal ergonomics
(such as a shell abbreviation) belong to the user's chezmoi, not to the
project. Chosen 2026-10-11 after a namespace check: free on PyPI, npm, crates,
and under `bengineerdavis` on GitHub. Rejected alternatives and their reasons:
`agentize`/`farrier`/`retinue` (npm or PyPI squatters in this exact concept
space), `agency`/`agentic` (taken by substantial agent frameworks), `equiper`
(free, lost to the user's preference for explicit naming).

## Triggers

- **SHOULD** apply to any change to this repository, its template, or its CLI,
  by a human or an agent, including documentation-only changes.
- **SHOULD** apply when deciding what belongs in the agentic layer versus a
  base template, chezmoi, or a stamped project's local files.
- **SHOULD** apply when a rule here appears to block reasonable work — the
  scenario on that rule records what it cost to learn, which is the input to
  changing it.
- **SHOULD NOT** be treated as a checklist satisfied after the fact.
- **SHOULD NOT** be extended by analogy to cases it does not name. A new
  failure earns a new behavior with its scenario.

## Behaviors

### Behavior: Layering — the layer stamps agentic concerns only

The template SHALL stamp only the agentic layer: agent configuration, review
loops, knowledge context, dependency declarations for agent tooling, and the
tasks that run them. Language, framework, build, and lint concerns for the
code itself SHALL live in base templates (for example
`python-project-template`), not here. Shared project-agnostic logic that is
personal rather than project-shaped (bootstrap conveniences, personal tools)
SHALL be hoisted to the user's chezmoi repository instead of stamped here.

#### Scenario: A change wants a Python dev tool pinned

- **GIVEN** a wish that every stamped Python project also run a formatter
- **WHEN** the author chooses where it lives
- **THEN** it goes to the base template; stamping it here would force every
  non-Python project to carry Python concerns. The conversation that produced
  this repository already separated the two templates for exactly this reason.

### Behavior: Layering — two answers files, two independent update paths

The layer SHALL declare a custom `_answers_file` (for example
`.agentic-answers.yml`) so that a project stamped as base-then-layer holds two
answers files and each layer remains independently `copier update`-able. The
answers files SHALL be committed in stamped projects.

#### Scenario: The base template is updated in an existing project

- **WHEN** `copier update` runs for the base template
- **THEN** the agentic layer's answers and files are untouched. A single
  shared answers file would make the second stamp clobber the first, and the
  maintainer would lose their layer choices on every base update.

### Behavior: Layering — the agentic layer is itself layered

The layer SHALL be organized into named sub-layers, each owning one concern,
with `ARCHITECTURE.md` as the descriptive source of truth for the map. The
concerns are: environment & sandboxing; file isolation & worktrees; agent
orchestration; LLM dependency management; review loops; task management;
structure enforcement; attribution. A copier variable or CLI flag SHALL map to
one layer (or one component of one layer), never to a grab-bag. When two
layers touch the same shared file, the merge SHALL be deterministic and owned
by the CLI, not by hand edits.

#### Scenario: Two features both need to extend mise.toml

- **GIVEN** a stamped task and an environment tool both want entries in a
  project's `mise.toml`
- **WHEN** either is stamped or updated
- **THEN** both go through the same environment-layer merge path. Ad-hoc
  writes to shared files from separate features are how clobbering returns.

#### Scenario: A new capability does not fit a named layer

- **WHEN** a proposed feature matches no layer
- **THEN** either a layer is defined first (with its concern stated) or the
  feature is declined. A feature that lives "everywhere" is a grab-bag and
  becomes unmaintainable.

### Behavior: Composition — the CLI orchestrates, copier stamps

The CLI SHALL be the composition mechanism: it stamps the base template (when
one is wanted), then the agentic layer, into one destination. For a new
project the base stamp is the default. For an existing project the CLI SHALL
ask whether to stamp a base template, unless a flag answers for it
(`--base <ref>` to include, non-interactive without a flag defaults to
layer-only). The CLI SHALL NOT re-implement what copier does; it invokes
copier.

#### Scenario: An agent runs the CLI non-interactively on an existing repo

- **WHEN** the CLI is invoked with no base flag and no TTY
- **THEN** only the agentic layer is stamped. Asking a question that cannot be
  answered, or guessing a base template, are both failures; the first hangs,
  the second stamps the wrong foundation.

### Behavior: Composition — the layer never clobbers what it lands on

When stamping onto a directory that already has files (an existing project, or
a base stamp), the layer SHALL add its own files and SHALL NOT overwrite
existing ones of the same name. Where the layer must modify a shared file
(for example appending tasks to an existing `mise.toml`), it SHALL do so
additively and idempotently, and it SHALL verify the merge in the stamp test.

#### Scenario: A project already has a hand-tuned mise.toml

- **WHEN** the layer is stamped onto it
- **THEN** the existing tool pins, env, and tasks survive. Copier's default
  overwrite would destroy them; this is the difference between adopting the
  layer on ten existing projects and being unable to.

### Behavior: Loops — the fast loop reviews every commit

The fast loop SHALL be roborev: its daemon and post-commit hook queue a
background review of each commit with the project's agent, findings accrue in
a ledger until fixed, and a stamped skill instructs the live agent to consult
and fix findings while context is fresh. Roborev SHALL be pinned via mise like
every other tool.

#### Scenario: An agent commits six times without review

- **WHEN** the session ends
- **THEN** every commit has queued a review and open findings are visible via
  a mise task, not lost. "Agents write fast and move on before reviewing their
  own mistakes" is the failure this loop exists for.

### Behavior: Loops — the slow loop is a scheduled deep review

The slow loop SHALL be a stamped mise task that runs a non-interactive opencode
review agent over the working branch (against its base) and writes a dated
report to `docs/reviews/`. It SHALL be runnable by hand and schedulable by
cron at the user level (chezmoi), never by project stamp. A consult-llm second
opinion on the report is opt-in via the consult-llm flag.

#### Scenario: The slow loop is scheduled inside a project

- **WHEN** someone adds the cron entry in the repository rather than chezmoi
- **THEN** every collaborator and every stamp of the template inherits a
  machine-specific schedule. Scheduling is personal; the task it invokes is
  shared.

### Behavior: Dependencies — every referenced skill is declared

Whenever the layer stamps a reference to a skill, agent, or subagent — in
`AGENTS.md`, docs, or agent configuration — that skill SHALL be declared in
the stamped `agents.toml` in the same change, pinned to a ref, with `dotagents
--project install` wired as a mise task. Removing the last reference SHALL
remove the declaration.

#### Scenario: A doc tells the agent to use a skill

- **GIVEN** a stamped doc that says "run the review skill before pushing"
- **WHEN** the stamp lands
- **THEN** `agents.toml` declares that skill from its source repo. A method
  referenced but not installed is a rule that reads as enforceable and is not.
  This behavior is inherited from the dotfiles spec, where it was learned the
  hard way.

### Behavior: Dependencies — MCP setup is one question and one command

The stamp SHALL seed `[[mcp]]` server declarations from a copier question, and
a stamped `add-mcp` skill SHALL wrap `dotagents mcp` for post-stamp additions,
so adding an MCP server never requires hand-editing generated files.

#### Scenario: A collaborator clones a stamped project

- **WHEN** they run the install mise task
- **THEN** dotagents installs declared skills and MCP wiring for their agent
  tool. Per-user secrets SHALL NOT enter the committed config; they live in
  the user or local config layer of the tool that consumes them.

### Behavior: Enforcement — alint holds the layer's own shape

The stamp SHALL include `.alint.yml` extending the bundled `agent-hygiene`,
`agent-context`, and `oss-baseline` rulesets (plus ecosystem rulesets gated on
what the base template stamped), wired as a prek hook. `alint
export-agents-md` SHALL be run when `.alint.yml` changes, so `AGENTS.md` and
the enforced rules do not drift apart.

#### Scenario: An agent leaves a scratch planning doc at the repo root

- **WHEN** the next commit runs
- **THEN** alint reports it and the agent output format carries the fix
  instruction. Structure conventions that live only in a reviewer's head fail
  exactly when review volume is highest.

### Behavior: Enforcement — checkers do not overlap

Enforcement tools SHALL divide by concern, and the division SHALL be
recorded where both sides can see it: alint owns repository structure and
content hygiene (files that should or should not exist, naming, whitespace,
newlines, merge markers); language linters and formatters own code and
config-file semantics; code formatters own formatting. The layer's hook
fragment SHALL NOT add generic pre-commit builtins that duplicate alint's
content checks, and `.alint.yml` SHALL NOT add rules that duplicate a
dedicated linter the project already runs. When the layer lands on a project
whose existing hooks already cover something alint enforces, the dedicated
tool wins and the alint rule is turned off rather than both running.

#### Scenario: A base template already runs a whitespace fixer

- **GIVEN** a base template whose hook config fixes trailing whitespace
- **WHEN** the layer's hook fragment is merged in
- **THEN** the fragment adds no second whitespace fixer, and
  `docs/references.md` records the division: alint = shape, the base's
  linters = semantics. Two tools fixing the same bytes fight in commits and
  teach agents to ignore one of them.

Enforcement families are named in `ARCHITECTURE.md` (structure & hygiene;
code/config semantics; prose & docs; agentic context) and each has one rule
source. A new checker joins through a family — with its rule source named —
or it is declined. Families govern disjoint subjects: when a richer linter
arrives for a subject alint already covers (agentic-context linting over
`AGENTS.md` and skills, for instance), the covered alint rules are switched
off, never left running twice.

### Behavior: Boundary — nothing personal is stamped

The layer SHALL NOT stamp user-level state: global opencode config,
consult-llm user config, personal skills, personal binaries (aboyeur), or
shell aliases. Project stamps carry what a collaborator needs; user config
lives in chezmoi and dotagents global scope.

#### Scenario: A stamped project contains a personal default model

- **WHEN** a collaborator opens the project
- **THEN** they see project policy, not the author's machine. consult-llm
  makes the seam explicit: `~/.config/consult-llm/config.yaml` (user, chezmoi)
  versus `.consult-llm.yaml` (project, stamped) versus
  `.consult-llm.local.yaml` (personal, gitignored).

### Behavior: Boundary — the stamped mise.toml stays extendable

The stamped `mise.toml` SHALL be minimal and conventionally shaped so aboyeur
(an agent-driven, headless mise configurer) and `mise doctor project` can
extend or verify it without clobbering. Local overrides SHALL use mise's
canonical local file convention. The layer SHALL NOT bake in a monolithic
configuration that a configurer would have to rewrite wholesale.

#### Scenario: aboyeur configures a freshly stamped repository

- **WHEN** the user asks aboyeur to "set up mise for this repository"
- **THEN** the agent extends the existing file rather than replacing it, and
  `aboyeur --check` passes. The aboyeur skill is not yet published; until it
  is, this contract is a design assumption tracked in open questions.

### Behavior: Opt-ins — experimental integrations default off

consult-llm and git-ai SHALL be stamped behind opt-in variables, default off.
The loops, dotagents wiring, and alint are the default layer.

#### Scenario: A collaborator stamps the layer for a boring project

- **WHEN** they accept defaults
- **THEN** they get the review loops and structure enforcement, and none of
  the experimental surfaces. The experiments belong to the maintainer's
  chosen projects, not to every project.

### Behavior: Shrink — the retro looks for the deterministic replacement

The slow loop's report SHALL include a section that names AI usage observed in
the period and whether a deterministic replacement (task, hook, linter rule,
script) now exists or is worth building, applying Pareto judgment to what is
worth converting.

#### Scenario: A repeated manual AI step appears in three reports

- **WHEN** the retro runs the third time
- **THEN** it names the pattern and proposes the deterministic tool, and the
  finding becomes a backlog task. Without this section the layer only ever
  grows its AI surface; with it, growth and shrinkage are both visible.

### Behavior: Verification — the template is stamp-tested, not assumed

Every change to the template SHALL pass a stamp test that renders the matrix
(new project with base, existing project layer-only, defaults and opt-ins)
into a temporary directory and asserts the critical invariants: two answers
files, no clobbered pre-existing files, install task runs. The matrix SHALL
run locally via a mise task and in CI.

#### Scenario: A template edit breaks only the existing-project path

- **WHEN** the stamp matrix runs
- **THEN** the failing branch is named. A template that is only tested by
  stamping fresh directories will still destroy existing projects, which are
  the majority of real uses.

### Behavior: Isolation — one worktree per task, merged without squashing

Task work SHALL happen in a worktree whose branch is named from the
backlog task id (`apt-N-slug`), created and addressed through worktrunk
(`wt switch`). The layer SHALL stamp `.config/wt.toml` carrying the
post-start bootstrap hook and the pre-merge verify hook, and SHALL pin
`merge.squash = false` so a task's commit series survives the merge.
Worktree placement (the path template) SHALL remain user-level
configuration and SHALL NOT be stamped. Project hooks run only after
first-run approval; the layer SHALL NOT bypass the approval gate.

#### Scenario: An agent edits the shared checkout

- **WHEN** task work appears in the main checkout instead of a worktree
- **THEN** this behavior is violated; the work moves to
  `wt switch <task-branch>` before continuing. The current session itself
  worked in `.worktrees/apt-12` for the design that produced this rule.

#### Scenario: A task produced five reviewed commits

- **WHEN** the task merges to main
- **THEN** all five commits land un-squashed, each still individually
  reviewable and each already reviewed by the fast loop. Squashing would
  discard the granularity the loops exist to create.

### Behavior: Work — agent work is assigned before it starts

Work carried out by an agent SHALL have a task in the backlog task store
(`backlog-py`, markdown files under `backlog/`) stating what done means —
acceptance criteria or a definition of done — and who is doing it, before the
work begins. Work fanned out across several agents SHALL be several tasks,
one per unit of work. Adopted 2026-10-12, replacing the TASKS.md convention;
the backlog-py MCP server is the agent-facing surface. Inherited from the
dotfiles spec; the failure it prevents (reconstructable only from
transcripts) has already happened there.

### Behavior: Change records — one commit is one reviewable decision

Commits SHALL follow the commit-hygiene skill (one logical change, paths
named, message sized to the change). The skill SHALL be a declared dependency
in this repository's own `agents.toml`. A human-readable `CHANGELOG.md`
SHALL be kept for changes a user of the template would notice.

#### Scenario: A template change and a CLI change are ready together

- **WHEN** the working tree holds both
- **THEN** they are two commits, or the template change is held back. A
  stamped project pinning the template ref should be able to take the CLI fix
  without taking template behavior changes.

## Constraints

### Constraint: Ambiguity is marked, not resolved

An unclear rule MUST NOT be guessed. It goes in Open questions with a safe
default. A guess produces a compliance artifact that reads as authoritative
and is not.

### Constraint: Shared tooling does not assume one agent

Stamped wiring MUST NOT hardcode a model name or assume exactly one agent
tool. Agent targets are declared in `agents.toml`; model choices come from
user-level configuration (consult-llm selectors, opencode defaults). The
project declares policy; the user declares models.

### Constraint: Findings and reports have owners and homes

The roborev ledger is local machine state (gitignored); `docs/reviews/` and
`docs/experiments.md` are committed project artifacts. No tool MAY begin
storing derived data anywhere else. This follows the dotfiles rule that data
ownership precedes data.

### Constraint: The CLI stays thin

The CLI MUST NOT grow project-generation features that copier or a base
template owns. Its surface is composition, layering, and update. A feature
that tempts the CLI to know a language's project shape belongs in a base
template.

## Open questions

Each open question carries a safe default until resolved; resolution happens
by experiment, not by discussion alone.

- **aboyeur contract.** The aboyeur skill is unpublished; the exact file shape
  it expects from a project `mise.toml` is unverified. Default: minimal,
  conventionally shaped `mise.toml`; verify against the skill when it lands.
  Owner: bdavis.
- **roborev delivery into opencode sessions.** Documented agent-hook delivery
  lists several agents; opencode support is unverified. Default: findings
  surface via a mise task and a stamped skill instruction; revisit when
  verified. Owner: bdavis.
- **Slow-loop cadence.** Default: manual (`mise run review-deep`) plus an
  optional chezmoi cron example. A real cadence should be chosen from use, not
  invented. Owner: bdavis.
- **Roborev reviewer agent and model.** Default: the project's default opencode
  agent; pin only after measuring. Owner: bdavis.
- **PyPI publication.** The CLI may ship only via git + pipx/uvx initially.
  Default: publish when a second machine needs it. Owner: bdavis.



## Decision record

Decisions confirmed with the maintainer, 2026-10-11:

| Decision | Choice |
| --- | --- |
| Composition | Sequential stamp (base, then layer) with custom `_answers_file`; Python CLI orchestrates; interactive ask for existing projects, `--base` flag, non-interactive default layer-only |
| copier-mise-sandbox | Absorbed as the substrate; the sandbox becomes a thin consumer |
| Fast loop | roborev (daemon, post-commit hook, findings ledger, fix-while-fresh) |
| Slow loop | Scheduled non-interactive opencode deep review writing `docs/reviews/` |
| Agent surface | opencode-first, wired through dotagents targets |
| dotagents scope | Project-scope `agents.toml`, skills + subagents pinned to refs; MCP via stamp question plus `add-mcp` skill |
| v1 scope | Loop-complete: harness + fast loop + one slow loop + dotagents + alint; consult-llm and git-ai opt-in, default off |
| alint | `.alint.yml` with agent-hygiene, agent-context, oss-baseline + gated ecosystem rulesets; prek hook; AGENTS.md kept in step |
| consult-llm | raine/consult-llm; opencode backend; user config in chezmoi, project config stamped only when opted in |
| User/project boundary | Personal tools and user config to chezmoi and dotagents global; shared project-agnostic logic also hoisted to chezmoi |
| Base templates | Separate repositories; this layer defines only the composition contract |
| Name | agentic-project-template (see Intent) |
| Task management | backlog-md-py is the store (`backlog/`, ids `apt-…`); TASKS.md retired; backlog-py MCP wired for agents (2026-10-12) |
| File isolation | worktrunk `wt` @ 0.80.0 (mise registry name); `.worktrees/` inside-repo layout via user config (chezmoi); stamped `.config/wt.toml`: post-start bootstrap + pre-merge check, `merge.squash = false` pinned; branch names from task ids. Design confirmed 2026-10-13 (apt-12) |
