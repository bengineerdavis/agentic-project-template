# HANDOFF — session context (2026-10-11 → 2026-10-18)

Scope: this repository — the agentic-layer copier template and its CLI.
Decisions here govern THIS repo; sibling repos carry their own scoped
handoffs (copier-cat, copier-template-copier-template fork,
copier-mise-sandbox, python-project-template).

## Session 2026-10-18 — redge bootstrap (read this first)

This HANDOFF is written for the next session, which restarts under
opencode V2 to verify roborev end-to-end (apt-21's test) — see
"Next actions".

The `redge` repository now exists (public, pushed):
scaffold + migrated research + seeded backlog. This repo's last session
performed the first real with-base stamp onto it, which caught six
template defects the fixture matrix could not (closed apt-2/3/6/17 with
that evidence) and confirmed the maintainer's per-tool-fragment direction
(apt-20 stamped, apt-22 queued).

### Commit map (2026-10-18)

| Repo | Commits | What |
| --- | --- | --- |
| `../../redge` (pushed) | f6ea2ba scaffold (base+layer, two answers files); 013afa8 research migrated wholesale; bc09cdd backlog seeded (redge-1..11) + role/ placeholder; cba0529 layer docs + uv.lock; 6a9fac2 dotagents ignores | first real with-base stamp |
| `../python-project-template` (local, no remote) | ac7d6da materialized base (uv, prek, ruff, typer; MIT/FSL-1.1-MIT question); 307c928 stamped answers template; 791aacf `:app` entry point + mypy dev group | unblocks apt-2/apt-17 |
| this repo (unpushed) | 93f10df `task_prefix` question; 4a3e0ea real mise backends; b561750 description period; ffcb4d5 dotagents ignores; 4662f55 backlog bookkeeping | five session fixes + bookkeeping |

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
| opencode | 2.0.32 (V2) | http-backend pin (V2 ships from opencode.ai, not GitHub releases — the registry's aqua backend 404s on V2 tags), stamped by the layer. Bumped 2026-10-18 from 1.18.32 (V1): V1 cannot parse the V2 `permissions` in the global `~/.config/opencode/opencode.jsonc` and dies at TUI boot with "Unexpected server error" (apt-21). roborev end-to-end still to verify |
| prek / tombi | 0.5.2 / 1.5.5 | pinned in mise.toml |
| backlog-md-py | uv-run | dev dependency, task store + MCP |
| roborev | `github:kenn-io/roborev` (0.72.0) | hooks/daemon wired by the layer install task; agent=opencode; execution blocked on this machine (apt-21) |
| alint | `github:asamarts/alint` | stamped rulesets: oss-baseline, agent-hygiene, agent-context, python, ci/github-actions |
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
9. **Per-tool fragments** — confirmed 2026-10-18 (apt-22): each stamped
   tool owns `fragments/tools/<tool>/` (pin + tasks + hooks + gitignore +
   AGENTS.md lines); the CLI merge applies them in one declared, tested
   order. Replaces the cross-tool grab-bag fragments (`mise-layer.toml`
   carries every tool's pin today). Revisit if it fights the merge engine.
10. **Tool-docs reference library is stamped, not hoisted** — confirmed
    2026-10-18 (apt-20): `docs/references/<tool>/` per project;
    deterministic pull (mise task) + agent distill; refreshed from a
    user-level schedule (chezmoi), never a project-stamped schedule.

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

### copier (base-template side)
- A base template must ALSO carry its own answers template
  (`template/.copier-answers.yml.jinja`) — copier synthesizes no answers
  file without it, and `copier update` then cannot run for the base layer.
  Same rule as the layer's own decision #4; found on the redge stamp.

### typer (stamped CLI)
- `[project.scripts]` must point at the app object (`cli:app`), never the
  callback (`cli:main`): the callback is not a Typer command; the installed
  console script crashes outside Click.
- A standalone `--version` needs `invoke_without_command=True` on the
  callback or "Missing command" exits 2.

### uv / dev group
- Every tool a stamped mise task invokes must be in the dev dependency
  group: the base's `type-check` task ran `uv run mypy` while the group
  carried only pytest. Found on the redge stamp (fixed 791aacf).

### mise (tool backends)
- Bare `[tools]` names absent from the mise registry break config parsing
  in EVERY stamped project (mise refuses the whole mise.toml):
  `roborev = "latest"` and `alint = "latest"` were dead on arrival, and
  `dotagents = "npm:@sentry/dotagents"` is invalid as a version string.
  Use `github:owner/repo` for release binaries (roborev: `kenn-io`,
  alint: `asamarts`) and `"npm:@sentry/dotagents"` as the full tool key.
  Probe with `mise ls-remote <backend>:<repo>` before pinning (fix 4a3e0ea).

### roborev
- `roborev check-agents` is the diagnosis entry point (per-agent pass/fail
  with stderr). On this machine hooks install and queue fine, but every
  job fails pre-start: the opencode agent invokes the mise-pinned V1
  binary, which rejects the V2 `permissions` array in the global
  `~/.config/opencode/opencode.jsonc` (chezmoi-managed). apt-21.
- `roborev show <sha>` for a failed job prints "no review found" (nothing
  was produced); `roborev status` shows the job table. A green
  "hooks installed" is NOT a working fast loop — check for failed jobs.

### Sessions
- Task sessions sweep uncommitted files into their commits (observed:
  an unrelated main-checkout `.gitignore` edit was absorbed into
  607a05c). Keep the checkout clean — or expect edits to be committed
  by the running session — while a task session is active.

### Tests
- plumbum `local.env` propagates env fine — the mise isolation failure was
  mise's own global-config resolution, not env propagation.

## Current state (2026-10-18)

- `main` ahead of origin (unpushed): five session fixes
  (93f10df/4a3e0ea/b561750/ffcb4d5) + bookkeeping (4662f55) + apt-22 +
  this HANDOFF. Push is an author action; SSH is the working protocol
  (`git@github.com:bengineerdavis/…`).
- Board: apt-1, 2, 3, 6, 8, 12–18 **done** (apt-2/3/6/17 closed on the
  redge stamp's evidence). Open: apt-4, 5, 7, 9–11, 16, 19 (aube
  upstream report), 20 (tool-docs library), 21 (roborev unblock),
  22 (per-tool fragments).
- The fast loop is wired but **NOT reviewing on this machine** (apt-21):
  every roborev job fails pre-start. The stamped fallback
  (`mise run roborev-status` / `roborev-fix` + `review-findings` skill)
  is the only findings path until apt-21 clears.
- Review history: two full review rounds done before this session (all
  findings fixed); this session's findings came from the live stamp
  instead (six template defects, all fixed same-session).

## Next actions — the opencode v2 restart (read first)

You are the next session, started under opencode V2 to verify roborev
end-to-end (apt-21's test). In order:

1. Confirm the harness: `opencode --version` reports 2.x and the session
   starts cleanly — the global `~/.config/opencode/opencode.jsonc`
   (chezmoi: `opencode.jsonc.tmpl`) is V2-shaped (`permissions` array)
   and only V1 chokes on it. Do not hand-edit the global config; chezmoi
   owns it.
2. Give roborev a V2 binary: its opencode agent resolves `opencode` via
   mise shims → the repo pin (2.0.32, V2) in `mise.toml`, now served by the
   http backend (V2 ships from opencode.ai, not GitHub releases) — bumped
   2026-10-18, so no local override is needed anymore. The escape hatch
   remains `mise use -p mise.local.toml "http:opencode@<ver>"` — keep the
   prefix: a bare `opencode@<ver>` resolves the registry (V1), not the http
   tool (mise.local.toml is gitignored and overrides mise.toml per mise's
   config layering).
3. Restart the daemon so it picks up the new resolution
   (`roborev daemon restart`), then `roborev check-agents` — expect the
   opencode agent to PASS.
4. Make one commit (here or in redge) and watch it: `roborev status`
   → job completes (not failed); `roborev show <sha>` → a review with
   findings. Fix what is real, once, while fresh.
5. If green: close apt-21 with that evidence; the durable fix is the
   layer fragment's opencode pin → 2.x (every stamped project then gets
   a working fast loop), and apt-3's fallback note simplifies to
   "delivery verified".
6. If red: capture `roborev check-agents` stderr verbatim into apt-21
   and stop — do not tune the global config by hand.
7. Push this repo (author action), then the queued work proceeds:
   apt-19 (aube upstream report), apt-20 + apt-22 (per-tool fragments +
   tool-docs library), apt-4/5/7/9–11/16. redge implementation starts at
   redge-1 (`normalize`) in its own worktree:
   `wt switch redge-1-implement-the-R7-remote-normalizer`.
8. User-side, still outstanding from before: install the mattpocock
   skills (7-skill copy + dotagents sync) — a maintainer action, not
   agent work.

## Related repos (scoped handoffs in each)

- `../../redge` — bootstrap complete (public, pushed): scaffold, migrated
  research thread (`docs/research/repo-manager/`), seeded backlog
  (`redge-1..11`). Its AGENTS.md routes to the SPEC and BOOTSTRAP.
- `../python-project-template` — materialized base template (local repo,
  no remote): uv + prek + ruff + typer, MIT/FSL-1.1-MIT question, stamped
  answers template. Publishing it lets stamps use `gh:` refs instead of
  local paths (open decision, see apt-16/17).
- `../copier-cat` — template manager; this CLI is the prototype of its
  C1 adopt mechanics (decision tracked as apt-16).
- `../copier-template-copier-template` — customized fork (mise + SPDX/
  BlueOak/FSL licensing); the make-a-template base for this family.
- `../copier-mise-sandbox` — absorbed substrate; becomes a consumer.
