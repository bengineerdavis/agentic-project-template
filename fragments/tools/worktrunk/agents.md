- **Isolation:** one worktree per task — `wt switch <task-id-slug>` creates
  it and bootstraps via the post-create hook; merge and clean up when done.
  A commit hook enforces this: from a main checkout it blocks subagents and
  unattended runs outright, and for an interactive session it warns and only
  proceeds if you type `main`.
