- **Isolation:** one worktree per task — `wt switch <task-id-slug>` creates
  it and bootstraps via the post-create hook; merge and clean up when done.
