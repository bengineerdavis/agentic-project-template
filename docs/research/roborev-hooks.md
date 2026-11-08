# Roborev hook mechanics (APT-38 research)

Primary evidence Nov 8 2026: roborev v0.74.0 CLI (`--help` surfaces, `doctor`),
`.git/hooks/` contents, `~/.roborev/post-commit.log`, reviews.db, daemon logs.
Several premises in the task brief turned out stale — corrections first.

## Corrected premises

1. **Worktree blindness: OBSOLETE.** The v4 post-commit hook fires in
   worktrees. Verified three ways: the two apt-39 scratch-worktree commits
   enqueued instantly (post-commit.log `outcome: ok`, jobs 500/501);
   chezmoi-worktree and other-session worktree commits appear as `ok` rows;
   doctor reports "git hooks are installed and current". No task is needed
   to wire worktrees — wiring already works.
2. **The one real fast-loop failure in 7 days** was
   `acquire post-commit lock: context deadline exceeded` — the daemon was
   busy/down at commit time and the enqueue timed out. Same failure class
   explains the historical 120s-commit-era mysteries. Not a hook-logic bug.
3. **`roborev init` is the whole install surface** (verified help): creates
   `~/.roborev/`, optionally `.roborev.toml`, installs git hooks, starts the
   daemon. The layer's stamped bootstrap (fragments/mise-layer.toml) already
   runs `roborev init` with failure fallbacks — so stamped projects DO get
   the post-commit hook at stamp time. What they lack is anything else.

## Hook taxonomy (v0.74.0)

- **Git hooks** (repo-level): `install-hook` writes/repairs post-commit +
  post-rewrite; hooks call `roborev post-commit`, which enqueues a review
  job (async; the daemon owns execution). `install-hook repair` fixes
  version-managed binaries baked into hooks.
- **Agent harness hooks** (`agent-hook` subfamily): UserPromptSubmit/
  SessionStart hooks for agents that support them (claude-code et al).
  OpenCode does NOT support PreToolUse hooks (verified error), so the
  OpenCode surface here is nil; the relevant agent integration remains
  the MCP server (`roborev mcp`).
- **Enqueue is cheap and off the commit path** — post-commit.log shows
  same-second enqueues, including during batch-pending skips.

## Observed operational facts (for the skill)

- 7 failed jobs in 7 days were `no-verdict: empty output` (agent died
  mid-review) — re-run, don't redesign. Doctor surfaces this in
  "Recent failures".
- Reviews.db lookup beats the CLI when the daemon hangs (standing lore).
- Repo self-registers on first review; doctor says "repository is not
  registered yet" for fresh repos — benign.
- No REVIEW.md exists here — doctor warns reviews run on generic
  instructions. This is the layer's biggest real gap.

## What a stamped skill should wrap (operating contract)

1. **Status/open findings**: `roborev status` (exists as mise task
   roborev-status in stamped projects).
2. **Fix loop**: `roborev fix` (exists as roborev-fix task) — hands open
   findings back to the live agent.
3. **Close/comment**: `roborev close` / `roborev comment <job|sha> [msg]`
   (positional; no --job-id flag).
4. **Triage**: read via DB when CLI hangs; `roborev log <job>` for agent
   output; `roborev doctor` as the first diagnostic.
5. **Guidelines**: create REVIEW.md (or `.roborev.toml review_guidelines`)
   so stamped projects get project-specific review posture. This is the
   piece the layer should seed.

## Recommendation

The stamped skill (skill-shaped, dotagents-installable via agents.toml) =
thin wrapper over the above six verbs + a REVIEW.md seeding step.
The mise tasks already stamp status/fix; the missing stamped artifacts
are (a) the skill file itself and (b) REVIEW.md seeding at stamp time.
Both feed APT-26 (stamp roborev wiring).

## Open questions for the maintainer

1. Should the layer seed a minimal REVIEW.md (overlay-managed block) at
   stamp time, or leave it project-authored and just document it?
2. Since the worktree gap is closed upstream, should APT-26 drop its
   "worktree wiring" scope entirely? (Recommend: yes — reduces to the
   skill + REVIEW.md.)
