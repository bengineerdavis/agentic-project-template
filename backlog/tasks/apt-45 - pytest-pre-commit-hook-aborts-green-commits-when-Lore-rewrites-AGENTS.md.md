---
id: APT-45
title: pytest pre-commit hook aborts green commits when Lore rewrites AGENTS.md
status: To Do
created_date: 2026-11-10
ordinal: 1
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A stamped child project that adds a full-suite pytest pre-commit hook hits a
silent commit abort the first time the Lore-managed section of AGENTS.md goes
stale. The template sets the trap: it stamps the Lore section into every
child's AGENTS.md (`include_lore`, default on) but its own `prek.toml` ships no
pytest hook, so nothing in the template exercises — or guards against — the
interaction. The support repo (a stamped child) hit this in production.

**Root cause, verified:** a pytest hook with `pass_filenames = false` +
`language = "system"` makes prek stash the unstaged tree, run the full suite,
then restore. The suite itself is green — but running the agent environment
makes Lore append/refresh its "Long-term Knowledge" section in AGENTS.md (a
**tracked** file). prek's stash-restore then sees a modified tracked file and
aborts the commit with "files were modified by this hook" even though every
test passed. It is the C45 prek-stash collision variant, triggered by an
agent-side write rather than a parallel session.

**What it is NOT:** `.pytest_cache` — that is gitignored and prek's stash never
sees it. A cache-redirect "fix" was built and correctly abandoned when the real
mechanism was found.

**Failure shape:** the hook reports all green, the commit silently does not
land, and HEAD is unchanged. Cost the support repo several debugging rounds
across two sessions before the Lore write was identified as the dirtying
artifact (the only post-suite change was AGENTS.md, and its diff was exactly
the Lore section being re-appended).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria

<!-- SECTION:ACCEPTANCE_CRITERIA:BEGIN -->
- [ ] A stamped child that adds a full-suite pytest hook does not abort green
      commits when the Lore section of AGENTS.md is stale or rewritten mid-run.
- [ ] The fix preserves Lore managing AGENTS.md (chosen over disabling
      agentsFile — the operator wants Lore's knowledge section kept).
- [ ] The mechanism is documented so a child repo author understands WHY the
      hook config is shaped the way it is (the Lore write is the constraint).
<!-- SECTION:ACCEPTANCE_CRITERIA:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Candidate directions, in rough order of preference — decide at implementation
time, not here:

1. **Keep the section stable + hook ignores the Lore write.** If AGENTS.md's
   Lore section is committed and current, Lore does not rewrite it. Pair with a
   hook that tolerates an agent-side AGENTS.md touch (e.g. the pytest hook
   runs with the Lore write suppressed, or the section is restored before the
   stash-restore diff is taken).
2. **Stamp a per-project `.lore.json`** scoping what Lore writes during
   automated runs, so a headless `pytest` invocation does not trigger an
   AGENTS.md sync. Requires confirming Lore honors a "no agentsFile write in
   non-interactive runs" knob — verify against installed lore, not the README.
3. **Template ships the pytest hook itself**, pre-configured to coexist with
   the Lore write, so children inherit a working combination instead of each
   rediscovering the trap.

Related: APT-41 (.lore.md sync across machines) is a different concern — that
is about the knowledge file, this is about the AGENTS.md pointer section
colliding with the commit-time stash.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
