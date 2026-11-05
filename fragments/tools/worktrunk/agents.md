- **Isolation:** one worktree per task — `wt switch --create <task-id-slug>`
  fast-forwards clean `main` before creating it; existing worktrees and
  explicitly stacked parents are preserved. See `docs/branch-sync.md`.
