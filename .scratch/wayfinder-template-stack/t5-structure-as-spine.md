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
