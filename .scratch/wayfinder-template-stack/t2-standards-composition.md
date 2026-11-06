# T2 — Layered-file composition: where does CODING_STANDARDS.md live, and how do sections merge?

Type: grilling (HITL) · Blocked by: T1, T3 (resolved) · Blocks: T4
Status: OPEN — frontier · Claimed: nobody

## Question

This ticket decides the **layered-file merge mechanism** once. It starts with
CODING_STANDARDS.md (the maintainer's core ask) but T3 established that
layering is the norm, not the exception: nine shared files need it
(AGENTS.md, CONTRIBUTING.md, .gitignore, CODING_STANDARDS.md, .alint.yml,
LICENSE, mise.toml, prek.toml, opencode.json). The mechanism decided here is
the one all nine use.

For CODING_STANDARDS.md specifically: does the meta own the file + agnostic
defaults via a marked section, do bases append a `## Language` pointer to
convention files (PYTHON.md etc.), and does the agentic layer's vacuity-guard
rule move up or stay down-stack?

Decide the merge mechanics (which existing merge kind: RENDERED_SHARED, marked
section, append) and the removal plan for the current agentic-only file (what
happens on `update` to a project already carrying CODING_STANDARDS.md with the
vacuity rule — base-wins keeps it stale).

## Ownership already settled by T3 (do not re-decide)

- **CODING_STANDARDS.md** — meta: agnostic defaults. Base: language
  conventions pointer. Overlay: judgement-call / vacuity-guard section.
- **CONTRIBUTING.md** — meta: base shape (dev setup, test suites, quality
  gate). Base: language-specific contribution + style sections. Overlay:
  domain sections. Composition required by maintainer (2026-11-06).
- **.gitignore** — meta: agnostic lines. Base: language lines. Overlay: tool
  lines. Composition partly exists (agentic merges per-tool `gitignore.txt`).
- **AGENTS.md** — meta: agnostic shape + backlinks. Base: language commands.
  Overlay: agentic managed section (marked-section upsert already implemented).

## Open questions carried in

- `python-project-template/template/.gitignore` exists and is stamped
  (verified), and also carries `.worktrees/` — an agentic concern sitting in
  the base. Under T3's verdict that line moves to the overlay.
- Per-language convention files do not exist anywhere yet — greenfield shape
  this ticket designs. What is the merge rule when a project stamps two
  language sections?
- Does the mechanism handle *ordering* (base section before overlay section),
  or is order by convention?

## Constraint from T7

The merge mechanism must work given whatever T7 decides about variable flow
(`external_data` vs a shared answers file). If T7's channel changes, a
mechanism keyed on it changes. Coordinate; do not settle T7's question here.
