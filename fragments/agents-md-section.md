## Agentic layer

This repository carries an agentic layer managed by
`agentic-project-template`. The rules live in `.context/ai-rules.md`
(injected into opencode sessions); terms in `.context/glossary.md`.

- **Fast loop:** every commit is queued for background review by roborev;
  check open findings with `mise run roborev-status` before claiming work
  done (skill: `review-findings`).
- **Slow loop:** `mise run review-deep` reviews the branch and writes a dated
  report to `docs/reviews/`.
- **Agent dependencies:** skills, subagents, and MCP servers are declared in
  `agents.toml` and installed with `mise run dotagents-install`. Do not
  hand-edit dotagents-managed files.
- **Isolation:** one worktree per task — `wt switch apt-…` creates it and
  bootstraps via the post-create hook; merge and clean up when done.
- **Tasks:** agent work starts only after a backlog task exists stating what
  done means (`uvx --from backlog-md-py backlog-py task create …`).
- **Experiments:** record repeated AI usage worth converting to deterministic
  tooling in `docs/experiments.md`.
