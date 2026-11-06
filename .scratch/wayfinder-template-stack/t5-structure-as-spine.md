# T5 — Structure as spine: alint bundles enforce the expected layout, for the template repo and stamped projects

Type: grilling (HITL) · Blocked by: — (T1 resolved) · Sibling: T2 (mechanical vs judgement split)
Status: OPEN — frontier · Claimed: nobody

## Question

Maintainer direction (2026-11-04): expected repo structure is one kind of
spine — it tells an agent where files can be found *and* where they are
supposed to be — and it should be enforced via alint bundles, both for the
template repos themselves and for stamped projects. Decide:

1. **Bundle layering**: which bundles are agnostic (meta: oss-baseline,
   agent-context, agent-hygiene, docs/adr, hygiene/*), which are language
   (python, node, rust…), and which are layer-specific (agentic structure:
   docs/agents/, .agents/skills/, docs/reviews/, backlog conventions,
   .context/ content). T1 found the meta template already owns
   `.alint.yml` + profile questions (alint_profile: minimal / python /
   python-agentic / custom) — how do layer-added bundles compose with that
   profile and with a project's custom `.alint.yml` rules (the yaml
   deep-merge path exists via RENDERED_SHARED)?
2. **Who ships which structure rules**: the rules checking a layout must
   live with the layer that stamps that layout (meta checks the agnostic
   structure it stamps; python checks the python layout; the agentic layer
   checks docs/agents/, skills, reviews). Where the current bundles fall
   short of the stamped structure, name the rules to add.
3. **Self-hosting**: the template repos themselves enforce the same
   bundles (alint on agentic-project-template already gates via
   `mise run check` + prek) — decide which bundle profile each template
   repo runs on itself.
4. **Mechanical vs judgement boundary**: a rule alint can enforce belongs
   in bundles, never in CODING_STANDARDS.md (T2's file) — record the split
   so a rule doesn't get double-owned. Over time, entries may graduate
   from standards prose to bundle rules; that graduation path is the fog.

### Spine principle (source: u/allemaar's multi-agent guide, r/ClaudeCode 1vphazv — maintainer directive 2026-11-04)

The spine concept this ticket implements comes from the guide the
maintainer filed as backlog draft-1. The guide's distinction is the
design target:

- **Search** answers "where is the matching file?" — lands on a node,
  loses the surrounding structure. Compression-based context reduction
  fails the same way: lossy, and a cut small constraint silently changes
  a later decision.
- **A spine** is an *annotated index*: for every path it lists, it adds
  the bit of context explaining what's on the other side — what is this,
  where am I in the larger structure, what owns this, what should I read
  next, how do I reach the SOT. It improves orientation and cold
  navigation; it does not make search faster.

Alint bundles are the **mechanical tier** of that idea: bundles don't just
annotate — they *enforce* that a node is where the structure says it
should be, so the annotation can never silently drift from the layout.
The guide's skill pattern (a spine listing a skill's name + short
description, full instructions unloaded until triggered) is the same
progressive-disclosure ladder the layer already uses for AGENTS.md
pointers, ARCHITECTURE.md, and skill descriptions. Map each spine tier to
an enforcement owner here:

- **Where files can be found (existing layout)** — agnostic + language
  bundles check structure mechanically (decision 2).
- **Where they are supposed to be (owned structure)** — bundles encode
  the ownership seams T3 decides, so a file stamped by a layer must sit
  in that layer's structure or the check fails.
- **What to read next (annotation)** — the human/agent-facing half:
  AGENTS.md pointers, ARCHITECTURE.md, skill descriptions. Kept honest
  by the mechanical tier; out of this ticket's scope except that bundle
  rules must not duplicate annotations (writing-for-agents: an
  environment-estating doc is a cache).

Context pointer: T1's inventory (alint split across meta/agentic, no
declared seam) is the raw material. Companion artifact:
backlog/drafts/draft-1 (the five patterns; this ticket carries only the
spine principle).

## From T3 (resolved 2026-11-06)

- **alint is a layered file**, like the other shared files: the bundle set is
  conditional on which base and which overlays a project stamps. Bundle
  ownership per T3's verdict: **meta** owns the `.alint.yml` scaffold, the
  profile/bundle questions, and the `ci/<vcs>` bundle; the **base** owns
  language bundles (`python`, `node`, …); the **overlay** owns agentic
  structure bundles (`agent-hygiene`, `agent-context`), the binary pin, and
  the hook.
- **Defect to fix in this ticket (verified 2026-11-06):**
  `agentic-project-template/template/.alint.yml` hardcodes the full bundle
  list including `alint://bundled/python@v1`, and appends a second
  `ci/github-actions` entry. That is the agentic adjective asserting the
  Python noun and duplicating the meta's `vcs_platform` handling — the same
  class of error as two overlays claiming one concern. The agentic layer must
  emit only its own bundles and let the meta's scaffold supply the rest.
- **Self-hosting contradiction (verified):** the alint fragment's own comment
  says "no generic builtin hooks here: alint owns trailing whitespace, final
  newlines, and merge markers — checkers do not overlap." Both template repos'
  **root** `prek.toml` nevertheless run `end-of-file-fixer` and
  `trailing-whitespace`. Stamped projects are clean (python's stamped
  `prek.toml.jinja` is ruff-only); the template repos' own self-hosting is
  what contradicts the claim. Decision 3 (self-hosting) must resolve this:
  either the prose is wrong or the root configs are.
- **Base depends on overlay for hygiene (verified — the sharpest finding).**
  `python-project-template/template/prek.toml.jinja` is ruff-only by design,
  with a comment saying "in layer-stamped projects alint owns trailing
  whitespace, final newlines, and merge markers." So a **python-only** project
  — a base with no overlays — gets **no** whitespace, newline, or merge-marker
  enforcement at all. Under T3's model the base is the noun and must be
  correct standalone; a base cannot outsource its own hygiene to an adjective.
  `spec.md:280` already anticipates the right shape: "when the layer lands on
  a project whose existing hooks already cover something alint enforces, the
  dedicated tool wins and the alint rule is turned off rather than both
  running." The base's dedicated hooks are therefore the primary owner, and
  alint narrows to structure. This reverses the current comment on both
  sides; decide it here.
