# Task workflow — worktree per task

Every backlog task runs in its own worktree; `main` stays mergeable and
clean. Worktrunk (`wt`) manages worktrees; the layer stamps
`.config/wt.toml` so worktrees bootstrap themselves.

## Start a task

1. Assign it: `uvx --from backlog-md-py backlog-py task edit <ID> -s
   "In Progress"`. Commit the status change on `main`.
2. `wt switch --create <task-id-slug> --yes` — creates the branch and the
   worktree at `.worktrees/<branch>`, then the post-start hook runs
   `mise trust && mise run install`. Tool state is machine-shared, so the
   bootstrap is fast after the first time.
3. Do the work only inside the worktree. The shared checkout is not for
   task work.

## Finish a task

1. Commit on the task branch (commit-hygiene skill: one reviewable
   decision per commit; the fast loop has reviewed each one).
2. `wt merge <branch>` — the pre-merge hook gates it (`mise run check`:
   alint + tombi; full tests run in CI and via the fast loop), then the
   series merges un-squashed (`merge.squash = false` is pinned at user
   level) and the worktree cleans up.
3. Back on `main`: `backlog-py task edit <ID> -s Done --append-notes
   "<merged commit + evidence>"`; commit the task store.

## Why

Isolation is what makes the loops trustworthy: roborev reviews commits on
task branches without stepping on parallel work, and the slow loop reviews
a branch instead of a moving checkout.
