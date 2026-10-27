## Agent skills

### Issue tracker

`backlog/` via `backlog-py` and `backlog-py-mcp`. See
`docs/agents/issue-tracker.md`.

### Triage labels

The five canonical roles, label strings unchanged. See
`docs/agents/triage-labels.md`.

### Domain docs

Single-context: `.context/glossary.md`; ADRs in `backlog/decisions/`. See
`docs/agents/domain.md`.

The engineering flows (`/to-spec`, `/to-tickets`, `/implement`, `/triage`) use
the `backlog-workflow` skill, which detects whether `backlog/` is present and
maps the flow onto it.
