# HANDOFF — session context (2026-10-11 → 2026-10-16)

Scope: this repository — the agentic-layer copier template and its CLI.
Decisions here govern THIS repo; sibling repos carry their own scoped
handoffs (copier-cat, copier-template-copier-template fork,
copier-mise-sandbox).

## What this is

A copier template that stamps an agentic layer (review loops, tasking,
isolation, orchestration, enforcement) onto any project, composed over a
base template by a thin Python CLI. `spec.md` constrains;
`ARCHITECTURE.md` describes L0–L7 and the merge table; tasks live in
`backlog/` (backlog-py, ids apt-N).

## Versions in use at handoff time

| Tool | Version | Note |
| --- | --- | --- |
| copier | 9.18.2 | pipx user tool |
| opencode | 1.18.32 | mise shim |
| prek / tombi | 0.5.2 / 1.5.5 | pinned in mise.toml |
| backlog-md-py | uv-run | dev dependency, task store + MCP |
| roborev | unpinned | backend unprobed (apt-3) |
| worktrunk | 0.80.0 | mise pin; design (apt-12) + wiring (apt-13) done |

## Design decisions (do not flip casually)

1. **Sequential stamp + custom `_answers_file`**: CLI stamps base then
   layer; layer uses `.agentic-answers.yml` so both layers stay
   independently `copier update`-able.
2. **copier cannot merge** — fragments/ + CLI own shared-file merges
   (base-wins deep-merge, prek repo-signature dedupe, gitignore append,
   marked AGENTS.md section). First-adoption is exactly copier#2486's gap;
   the merge engine is the prototype for copier-cat's C1.
3. **`update` = stored answers + fragments only** — a defaults re-render
   would reset layer choices; copier 9.18.2 requires `overwrite=True`.
4. **The template must carry its own answers template**
   (`template/.agentic-answers.yml.jinja`) — copier never synthesizes it.
5. **Checker families** (ARCHITECTURE L6): alint owns structure+hygiene;
   the layer's hook fragment carries only tombi + alint gate; prose/docs
   and agentic-context linting are future lanes with named rule sources.
6. **backlog-md-py is the task store** (L5): TASKS.md retired;
   `backlog-py-mcp` wired in opencode.json.
7. **worktrunk adopted for L1** — one worktree per backlog task; task
   worktrees live in-repo at `.worktrees/` via user-level wt config;
   the layer stamps `.config/wt.toml` (post-start bootstrap, pre-merge
   verify hooks, `merge.squash = false` so a task's reviewed commit
   series survives); branches named from backlog ids. Design in
   apt-12, wiring in apt-13, workflow dogfooded in apt-14.
8. **consult-llm and git-ai are opt-in flags, default off.**

## Gotchas learned (per tool)

### copier
- `_tasks` intentionally unused: merge logic is tested Python; bootstrap
  runs later via stamped mise tasks (stamp stays side-effect-free).
- `_migrations` is the sanctioned future path for update-time file surgery.

### mise
- Task names cannot contain colons — hyphens (`review-deep`).
- `mise run` auto-installs **every declared tool in every config it sees**,
  including the user's global config; if a global tool cannot install,
  tasks fail even when the task needs none of them.
- **aube (npm backend) locks — resolved in depth (2026-10-14)**: aube
  derives its lock dir from TMPDIR and defaults to shared `/tmp/fslock`;
  a root-run once created it, poisoning every user (and /tmp here is on
  the root fs — it never self-clears). Resolution, no memory required:
  (1) chezmoi-deployed `~/.zshenv` exports `TMPDIR="$HOME/.cache/tmp"`
  for every zsh incl. non-interactive agent shells — aube now locks in
  user space, immune even if root recreates /tmp/fslock (verified:
  lock file landed in ~/.cache/tmp/fslock, /tmp untouched);
  (2) the install tasks carry a writability preflight that turns any
  recurrence into the exact fix command; (3) root-cause hygiene rule:
  never run mise installs under sudo. Upstream report queued (apt-19):
  aube should default its lock dir to user space.
- **aube supply-chain threshold**: refuses npm packages below 1,000
  weekly downloads unless `allow_low_downloads = true` is set on the tool
  entry. Hit with `@sentry/skillet` — user-approved 2026-10-14 in global
  mise config (apt-18). Stamped projects pinning niche npm tools may hit
  the same gate on fresh machines; the approval is the user's consent
  decision, not the layer's.
- `MISE_GLOBAL_CONFIG_ROOT` does NOT stop tool loading by itself.

### worktrunk
- Project hooks and `template-append` prompt for approval on first run;
  `--yes` grants consent for one run only, `wt config approvals add --yes`
  persists it. Non-interactive merges stop at the prompt by design.
- `wt merge` on an unmerged-into-main branch runs the project's pre-merge
  hooks in the worktree; `--no-hooks` skips (spec: Isolation — do not
  bypass the gate casually).

### tombi / prek
- tombi-format expands long inline TOML tables across lines, which
  standard TOML rejects — use `[[repos.hooks]]` sub-tables for multi-key
  hook entries.
- prek native config is `prek.toml`; if a legacy `.pre-commit-config.yaml`
  exists, append there instead of writing prek.toml, or prek silently
  drops the legacy hooks.
- prek repo entries dedupe by repo + hook-id set (rev mismatch must not
  duplicate).

### backlog-py
- `task edit <ID> --status "In Progress"` needs at least one edit flag;
  `--append-notes` plus the status works.
- backlog "Done" ≠ archived; `cleanup` moves Done into backlog/completed.

### Sessions
- Task sessions sweep uncommitted files into their commits (observed:
  an unrelated main-checkout `.gitignore` edit was absorbed into
  607a05c). Keep the checkout clean — or expect edits to be committed
  by the running session — while a task session is active.

### Tests
- plumbum `local.env` propagates env fine — the mise isolation failure was
  mise's own global-config resolution, not env propagation.

## Current state

- `main`: foundation, template, CLI (deterministic merges), backlog
  adoption; isolation designed (apt-12, 363c15f), wired (apt-13), and
  dogfooded end-to-end (apt-14: worktree-per-task loop with approval
  gate + pre-merge checks). The old `apt-12-worktrunk-design` branch
  and sibling worktree were removed at closure; task worktrees now
  live in `.worktrees/` per the design.
- Board: apt-1, apt-8, apt-12–14, apt-18 done; apt-19 queued (upstream
  aube lock-dir report); apt-2..11 and apt-15..17 queued.
- Review rounds: two full reviews done; all findings fixed (update
  overwrite+choices preservation, wheel packaging incl. copier.yml, prek
  rev dedupe, AGENTS.md marker growth, overwrite heuristic).

## Next actions

1. apt-19 — file the upstream report: aube should default its lock dir
   to user space (fslock resolved via `~/.zshenv` TMPDIR; hygiene rule:
   never run mise installs under sudo).
2. apt-3 roborev↔opencode verification; apt-4 publish aboyeur skill.
3. apt-15 publish to GitHub; apt-16 evaluate cc relationship; apt-17
   refresh python-cli-template as the base layer (unblocks apt-2).
4. User-side: install the mattpocock skills (7-skill copy + dotagents
   sync).

## Related repos (scoped handoffs in each)

- `../copier-cat` — template manager; this CLI is the prototype of its
  C1 adopt mechanics (decision tracked as apt-16).
- `../copier-template-copier-template` — customized fork (mise + SPDX/
  BlueOak/FSL licensing); the make-a-template base for this family.
- `../copier-mise-sandbox` — absorbed substrate; becomes a consumer.
