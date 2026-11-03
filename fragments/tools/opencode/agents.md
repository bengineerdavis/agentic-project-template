- **Slow loop:** `mise run review-deep` reviews the branch and writes a dated
  report to `docs/reviews/`.
- **Language intelligence:** run `pyright` (python types) and
  `alint check` (repo-structure rules) directly — they are mise-pinned and
  fast; wire their diagnostics into your loop instead of waiting for
  editor-style feedback. The `lsp` section in `.opencode/opencode.json`
  pre-wires both servers for opencode builds that run LSP (V2 parses the
  section but does not yet run servers — treat it as forward wiring).
