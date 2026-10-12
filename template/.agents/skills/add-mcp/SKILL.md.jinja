---
name: add-mcp
description: Add or remove an MCP server declaration for this project via dotagents; never hand-edit generated agent configs.
---

# add-mcp

Use when the user asks to wire an MCP server into this project.

## Procedure

1. Establish the source (GitHub `owner/repo`, git URL, or local `path:`) and
   the servers it provides. If the user gave only a name, ask for the source.
2. Add the declaration at project scope:

   ```bash
   dotagents mcp add <name> <source> --project
   ```

3. Run `dotagents --project install` and confirm the server appears where the
   target agent expects it.
4. Commit the resulting `agents.toml` change in the same commit as whatever
   feature needed the server.

## Rules

- Project scope only (`--project`); never touch global state from a project
  session.
- Never put secrets in `agents.toml`. Credentials belong in the user's own
  config or environment, per the server's documented mechanism.
- If `dotagents mcp` is unavailable in the installed version, add the
  `[[mcp]]` entry to `agents.toml` by hand, run `dotagents --project
  install`, and note the fallback in `docs/experiments.md` as `[harness]`.

<!-- managed by agentic-project-template -->
