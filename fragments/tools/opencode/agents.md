- **Slow loop:** `mise run review-deep` reviews the branch and writes a dated
  report to `docs/reviews/`.
- **Language intelligence:** run `pyright` (python types) and
  `alint check` (repo-structure rules) directly — they are mise-pinned and
  fast; wire their diagnostics into your loop instead of waiting for
  editor-style feedback. opencode V2 runs pyright as a builtin LSP (no
  config entry); the `lsp` section in `.opencode/opencode.json` declares
  alint (whose server covers `.md`/`.yaml`/`.toml` among others). V2 parses
  the section but does not yet run servers — treat it as forward wiring.
