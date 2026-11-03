---
id: decision-2
title: LSP support is L0 pins plus per-agent wiring, not a new layer
date: 2026-11-03 09:20
status: accepted
---

## Context

Language intelligence for agents was sketched as a candidate layer
(apt-9): LSP servers as environment tools plus per-agent wiring, with the
open question "own layer vs L0/L2 components". The requirement is "any
agent I want"; opencode is the first proof.

## Decision

LSP support is not a new layer. Language servers are environment tools:
pinned in the layer's per-tool mise fragments (L0), resolved on PATH via
mise shims like every other binary. Wiring them into an agent is that
agent's orchestration concern (L2): the stamped `opencode.json` carries
the `lsp` section, merged additively through the existing
`RENDERED_SHARED` path.

Two rules keep it reproducible. First, the layer wires only servers it
also pins — a server the agent would auto-install or resolve outside mise
is not wired, so diagnostics do not silently depend on machine state.
Second, there is no cross-agent abstraction: the contract ("mise-pinned
binary on PATH plus a per-agent config stanza") is too thin to abstract
usefully; each agent adopted later gets its own wiring note in the spec
and ARCHITECTURE.md (tracked as apt-11).

Verified before deciding (2026-11-03): opencode V2 keeps LSP disabled by
default and enables it via the `lsp` config section; its builtin pyright
server starts when `pyright` is on PATH, which the mise pin provides;
`alint lsp` (0.21.0) is a stdio server publishing `.alint.yml` rule
diagnostics on document open/save — probed end-to-end over raw JSON-RPC,
9 diagnostics published for a planted violation.

## Consequences

apt-10 implements the opencode wiring (python via pyright, alint via
`alint lsp`) on top of this placement. When a second agent is adopted,
its wiring lands as a per-agent note, not an abstraction layer. If a
server cannot be mise-pinned, that is a blocker to wiring it, not an
exception to the pin rule.
