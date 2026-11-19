- **Agent dependencies:** skills, subagents, and MCP servers are declared in
  `agents.toml` and installed with `mise run dotagents-install`. Do not
  hand-edit dotagents-managed files.
- **Deliberate exploration:** Invoke `/adhd` explicitly for open-ended design,
  naming, and fuzzy debugging. The skill does not auto-trigger; its parallel
  exploration costs several agent calls.
