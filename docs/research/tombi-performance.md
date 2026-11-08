# Tombi performance investigation (APT-39)

Investigated directly in the main session (Nov 8 2026) after all three research
sub-sessions returned session recaps instead of findings files (known failure
mode, 8th instance). Measurements below are primary evidence taken on this
machine; tombi 1.5.5, prek 0.5.2, repo at 69d68c7.

## Question

Why do `git commit` calls exceed the 120s tool timeout while completing, and can
format-on-commit survive without the pain?

## Measurements (scratch worktree at ~/.cache/tmp/opencode/apt39-timing, detached at 69d68c7)

| Probe | Wall time |
|---|---|
| Full `uv run prek run --all-files` (warm, 8 hooks) | 0.38s |
| `tombi-lint` alone (warm) | 0.15s |
| `tombi-format` alone (warm) | 0.30s |
| Scratch commit, no .toml staged (tombi skipped) | 0.39s |
| Scratch commit, .toml staged (tombi active) | 0.29s |
| roborev job enqueue after scratch commit | same second (daemon log) |
| Job 499 (the historical 120s commit 69d68c7) enqueued | same second as commit (17:47:40 UTC = 09:47:40 -08:00) |

Cold-start context: the scratch worktree's first prek run created a venv and
installed 35 packages in 16ms (warm uv cache) — full cold run still under
2s, nowhere near 120s.

## Findings

1. **Tombi is exonerated for warm runs.** tombi-lint + tombi-format together
   cost under half a second on this repo's 18 TOML files.
2. **The commit path is fast end to end** — pre-commit (prek) plus the roborev
   post-commit hook all complete in ~0.3-0.4s in a scratch worktree.
3. **The roborev worktree-blindness gotcha is obsolete.** Jobs 500/501 were
   enqueued for the two scratch-worktree commits; the v4 post-commit hook
   fires in worktrees and is instant. Branch commits now enter the fast loop
   immediately.
4. **The 120s timeouts are not reproducible today.** Warm commit path, tombi,
   and roborev enqueue are all sub-second. Remaining unverified hypotheses,
   in order of plausibility: (a) one-time cold costs at the historical
   moments (fresh hook environments, tool downloads); (b) the roborev
   post-commit hook blocking while the daemon was down or draining
   (2>/dev/null hides the failure mode; daemon_state shows
   `shutdown_draining` was set 2026-11-05, the day of the first observed
   timeouts).

## Recommendation

Keep tombi-format on commit. No change to move formatting to CI/lint is
warranted — the measured cost is 0.3s. Keep the existing habit (already in
lore): on a commit timeout, check `git log` before re-running; if the commit
landed, do not re-commit. If a 120s commit recurs, capture `pgrep -fl roborev`
and daemon_state at that moment to confirm or kill hypothesis (b).

## Open questions

- None blocking. (b) above stays unverified until a recurrence is observed.
