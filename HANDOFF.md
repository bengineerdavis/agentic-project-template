# HANDOFF — session context (2026-10-11 → 2026-10-13)

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
| worktrunk | not installed | adoption decided, design pending (apt-12) |

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
7. **worktrunk adopted for L1** — one worktree per backlog task; design
   details pending in apt-12.
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
- **aube (npm backend) locks**: lock dir derives from TMPDIR; a stale
  root-owned `/tmp/fslock` blocked ALL npm: installs. Skillet was
  user-approved 2026-10-14 (`allow_low_downloads = true` in global mise
  config, apt-18). Residual user-side item: the durable chown
  (`sudo chown -R bdavis:bdavis /tmp/fslock`) or a TMPDIR decision in
  their shell env; until then run mise with `TMPDIR=/tmp/opencode`.
- **aube supply-chain threshold**: refuses npm packages below 1,000
  weekly downloads unless `allow_low_downloads = true` is set on the tool
  entry. Hit with `@sentry/skillet` (declared globally — apt-18 tracks it).
  Stamped projects pinning niche npm tools may hit the same gate on fresh
  machines; the approval is the user's consent decision, not the layer's.
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

### Tests
- plumbum `local.env` propagates env fine — the mise isolation failure was
  mise's own global-config resolution, not env propagation.

## Current state

- `main`: foundation, template, CLI (deterministic merges), backlog
  adoption; `apt-12-worktrunk-design` branch exists in a sibling worktree
  (repair after the `templates/` move: run `git worktree repair` here).
- Board: apt-1 done; apt-2..17 queued; apt-12 in progress (not started).
- Review rounds: two full reviews done; all findings fixed (update
  overwrite+choices preservation, wheel packaging incl. copier.yml, prek
  rev dedupe, AGENTS.md marker growth, overwrite heuristic).

## Next actions

1. apt-12 (worktrunk design) — inside its worktree; run `/grill-with-docs`
   (skill pending user install) against ARCHITECTURE L1.
2. apt-3 roborev↔opencode verification; apt-4 publish aboyeur skill.
3. apt-15 publish to GitHub; apt-16 evaluate cc relationship; apt-17
   refresh python-cli-template as the base layer (unblocks apt-2).
4. User-side: install the mattpocock skills (7-skill copy + dotagents
   sync), `sudo chown -R bdavis:bdavis /tmp/fslock`.

## Related repos (scoped handoffs in each)

- `../copier-cat` — template manager; this CLI is the prototype of its
  C1 adopt mechanics (decision tracked as apt-16).
- `../copier-template-copier-template` — customized fork (mise + SPDX/
  BlueOak/FSL licensing); the make-a-template base for this family.
- `../copier-mise-sandbox` — absorbed substrate; becomes a consumer.
