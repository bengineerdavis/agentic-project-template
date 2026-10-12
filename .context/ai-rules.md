# ai-rules

Tier 1 — injected in every opencode session. Keep under 100 lines.

## What this repository is

A copier template that stamps an agentic layer onto projects, plus a thin
Python CLI that composes it with base templates. Language concerns belong to
base templates; personal concerns belong to chezmoi; this repo owns the
agentic layer only.

## Working rules

- The spec (`spec.md`) governs. SHAs of truth: layer map in `ARCHITECTURE.md`,
  task store in `backlog/`. Fix a descriptive doc when it disagrees with the
  spec.
- One concern per layer (L0–L7, see ARCHITECTURE.md). A new capability that
  matches no layer needs a layer defined first, or is declined.
- Shared files (`mise.toml`, `prek.toml`, `.gitignore`, `AGENTS.md`) are
  only modified through the CLI merge path, never hand-edit in `template/`.
- Ambiguity is marked, not resolved: record it in spec open questions with a
  safe default and an owner instead of guessing.
- Every referenced skill must be declared in `agents.toml` in the same change.
- Every behavior added to the spec carries the scenario that justifies it —
  a rule without its failure gets argued away.
- Verification: stamp matrix before claiming template work done; a new test
  is not trusted until seen to fail; a command's exit status is read from the
  command, not through a pipe.
- mise task names cannot contain colons (colon-named calls fail); use
  hyphens: `review-deep`, not `review:deep`.
- tombi-format expands long inline tables across lines, which standard TOML
  rejects; write multi-key hook entries as `[[repos.hooks]]` sub-tables, not
  inline tables.
- Commits: one reviewable decision, paths named, message sized to the change
  (commit-hygiene skill — declared dependency).
- Plain language in docs, commits, and conversation; prose proportional to
  its subject.
