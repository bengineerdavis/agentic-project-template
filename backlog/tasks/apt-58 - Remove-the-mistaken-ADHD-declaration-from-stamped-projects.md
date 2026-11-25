---
id: APT-58
title: Remove the mistaken ADHD declaration from stamped projects
status: To Do
created_date: 2026-11-21 22:13
updated_date: 2026-11-23 18:59
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->

PR #26 declared `UditAkhourii/adhd` in every stamped project. The maintainer never asked for that skill: it runs parallel ideation at roughly ten agent calls per invocation. The request was `ayghri/i-have-adhd`, which formats output. APT-48 recorded the wrong source, was never corrected, and a later session implemented it faithfully. Every stamped project now declares and trusts a skill nobody chose.

Removing it is the whole change. The skill the maintainer does want belongs to chezmoi DOT-349, which owns the native i-have-adhd OpenCode integration and requires always-on to stay off unless the author enables it. Declaring an always-on output style per stamped project would contradict that task and duplicate a setting that already applies to every repository.

Ship:

- `template/agents.toml.jinja` with the `adhd` plugin block deleted
- `fragments/tools/dotagents/mise.toml` with `UditAkhourii/adhd` removed from the trust loop and the add line
- `fragments/tools/dotagents/agents.md` with the `/adhd` exploration bullet removed
- `tests/test_dotagents_projection.py` updated so the expected sources and skills no longer include ADHD, and a stamped child is asserted free of it
- the ADHD entry removed from the `merge.py` refresh-body migration table, or the table left able to carry an already-stamped project off the old body

Constraints:

- do not revert PR #26 or rewrite published history; remove the declaration going forward
- add no Copier question, no managed AGENTS.md block, and no new conditional path: APT-53 and copier-cat CCC-31 are reviewing the template's merge intent and this change must not enlarge that surface
- do not declare `ayghri/i-have-adhd` here; DOT-349 owns it, and its acceptance criteria require the always-on flag to stay absent by default
- an existing project that already took the ADHD wiring must lose it through the normal update path, not through manual edits
- report test and lint outcomes exactly; a stamped child still carrying ADHD is not a pass

Agreed with the maintainer 2026-11-23: narrow this task to removing the mistaken declaration, deferring to the copier-cat machine's in-flight template review and to DOT-349's ownership of the ADHD output style.

<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria

<!-- AC:BEGIN -->

- [ ] #1 template/agents.toml.jinja no longer declares the adhd plugin
- [ ] #2 fragments/tools/dotagents/mise.toml no longer trusts or adds UditAkhourii/adhd
- [ ] #3 fragments/tools/dotagents/agents.md no longer instructs agents to invoke /adhd
- [ ] #4 tests/test_dotagents_projection.py asserts a stamped child declares no ADHD source or skill, and fails before the removal
- [ ] #5 An already-stamped project loses the ADHD wiring through agentic-project-template update
- [ ] #6 No new copier question, managed AGENTS.md block, or conditional path is added
- [ ] #7 mise run test and mise run check pass; outcomes reported exactly

<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->

Related work owned elsewhere:

- chezmoi DOT-349 owns the native i-have-adhd OpenCode integration, including the plugin, the `/i-have-adhd` command, and the always-on flag. The output style the maintainer wants reaches every repository from there, so no stamped project needs its own copy.
- APT-53 and copier-cat CCC-31 are settling which template intent belongs in Copier artifacts and which belongs in the imperative runner. APT-53 states it changes no stamp behavior. This removal shrinks that surface and adds nothing to it, which is why it does not wait for those discussions.

An earlier draft of this task added an `include_adhd` question, a managed AGENTS.md rules block, a `.adhd-off` marker, and a merge mapping. All four were dropped on 2026-11-23: they would have contradicted DOT-349's always-on default and enlarged the merge layer under review.

<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done

<!-- DOD:BEGIN -->

<!-- DOD:END -->
