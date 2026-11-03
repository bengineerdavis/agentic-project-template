- **Slow loop:** `mise run review-deep` reviews the branch and writes a dated
  report to `docs/reviews/`.
- **Language intelligence:** opencode's LSP runs pyright (python) and
  `alint lsp` (repo-structure diagnostics) — both mise-pinned; enable or
  extend via the `lsp` section in `.opencode/opencode.json`.
