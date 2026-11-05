# T2 — Where does CODING_STANDARDS.md live, and how do sections merge?

Type: grilling (HITL) · Blocked by: T1 · Blocks: T3 (partly)
Status: OPEN · Claimed: nobody

## Question

T1 will name the overlaps; this ticket decides the composition design for
the standards file specifically (the maintainer's core ask): does the
meta-template own the file + agnostic defaults via a marked section, do base
templates append a `## Language` pointer to convention files (PYTHON.md etc.),
and does the agentic layer's vacuity-guard rule move up or stay down-stack?
Decide the merge mechanics (which existing merge kind: RENDERED_SHARED,
marked section, append) and the removal plan for the current agentic-only
file (what happens on `update` to a project already carrying
CODING_STANDARDS.md with the vacuity rule — base-wins keeps it stale).
