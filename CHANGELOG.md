# Changelog

Written for readers, at the time of the change, in their terms — not
reconstructed from `git log`.

## Unreleased

- Added: backlog/workflow adapter for the Matt Pocock engineering skills.
  Stamped projects get `docs/agents/issue-tracker.md`, `triage-labels.md` and
  `domain.md`, a `backlog-workflow` skill that detects `backlog/` and maps
  spec, tickets, claims and decisions onto backlog-md-py, an `Agent skills`
  block in the managed AGENTS.md section, and a default `backlog-py-mcp`
  declaration in `agents.toml`.
- Added: initial scaffold — spec, architecture layer map (L0–L7 plus the
  checker-family table with prose/docs and agentic-context lanes), copier
  template (agentic layer), CLI with deterministic shared-file merges, stamp
  matrix including an update smoke.
- Changed: the layer's hook fragment no longer adds generic pre-commit
  builtins — alint owns content hygiene (spec: checkers do not overlap).
- Fixed: `update` passes `overwrite` (copier 9.18.2 requires it), reports
  copier errors cleanly, and re-applies only fragment merges so layer
  choices in `.agentic-answers.yml` survive an update.
- Fixed: the installed wheel ships `copier.yml`, `template/`, and
  `fragments/`, so `uvx` installs can stamp.
- Fixed: prek repo entries dedupe by repo + hook ids; a rev mismatch no
  longer duplicates an entry and runs hooks twice.
- Fixed: AGENTS.md managed section no longer doubles its markers on stamp or
  grows an orphan END marker on every update; the fragment carries content
  only and `upsert_marked_section` owns the markers (regression test feeds
  the real fragment through three times).
- Fixed: the stamp overwrite heuristic requires the actual managed comment,
  so a project file that merely mentions the tool is skipped, not clobbered;
  `install` fails loudly for required tools and names what it tolerates.
- Changed: task management adopted backlog-md-py — `backlog/` is the task
  store (ids `apt-…`), TASKS.md retired, the backlog-py MCP server is wired,
  and the layer stamps `backlog-init` (spec L5 + Work behavior amended).
