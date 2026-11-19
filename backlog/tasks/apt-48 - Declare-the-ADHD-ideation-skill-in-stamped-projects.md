---
id: APT-48
title: Declare the ADHD ideation skill in stamped projects
status: To Do
created_date: 2026-11-12 21:11
updated_date: 2026-11-12 21:11
orchestration:
  status_key: inprogress
  lease_owner: opencode-apt-48-adhd-skill
  lease_expires_at: '2026-11-19T21:45:41.597008Z'
  version: 1
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
APT-47 gives stamped projects the reviewed Matt Pocock workflow plugin. The other skill reaching this maintainer's agents daily is ADHD (UditAkhourii/adhd, MIT), which arrives only through a personal Claude plugin sync, so a stamped project never sees it. ADHD costs roughly ten agent calls per run, which makes auto-triggering the wrong default even where the skill is worth having.

Ship:

- an `UditAkhourii/adhd` plugin declaration in `template/agents.toml.jinja`, alongside the Matt Pocock entry
- `UditAkhourii/adhd` added to the trust loop and the `dotagents --project add` line in `fragments/tools/dotagents/mise.toml`
- a stamped AGENTS.md line naming `/adhd` as explicit invocation for open-ended design, naming, and fuzzy debugging
- a stamp test asserting the declaration and the trust entry reach a stamped child
- a merge-path mapping in `src/agentic_project_template/merge.py` so projects stamped before this change pick the new source up on update

Constraints:

- branch off `apt-47-dotagents-projection`, not main: both changes edit `agents.toml.jinja` and the same trust loop
- no new copier question; ADHD is declared unconditionally like commit-hygiene and review-best-practices
- the stamped docs describe explicit `/adhd` invocation only, and do not claim auto-trigger behavior
- plain-english and writing-for-agents are the writing standards for the stamped prose
- report test and lint outcomes exactly; a projection that does not appear in a real stamped child is not a pass

Agreed with the maintainer 2026-11-12: declared by default, explicit invocation only, no copier flag.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 template/agents.toml.jinja declares UditAkhourii/adhd as a plugin source
- [ ] #2 fragments/tools/dotagents/mise.toml trusts UditAkhourii/adhd in both scopes and adds it in dotagents-add
- [ ] #3 The stamped AGENTS.md names /adhd as explicit invocation for open-ended design work and does not claim auto-trigger
- [ ] #4 A stamp test fails before the change and asserts the declaration and trust entry in a stamped child afterward
- [ ] #5 merge.py maps the prior dotagents-add body so an existing project picks up the new source on update
- [ ] #6 mise run test and mise run check pass; outcomes reported exactly
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->

<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->

## Run History
<!-- SECTION:RUN_HISTORY:BEGIN -->
<!-- RUN_HISTORY_ENTRY:BEGIN -->
```yaml
event_id: run-6616384e708d45dab94715983ef78c3c
type: claim_task
actor: opencode-apt-48-adhd-skill
timestamp: '2026-11-19T20:45:41.597105Z'
result: succeeded
task_id: APT-48
from_status: todo
to_status: inprogress
metadata:
  lease_ttl_seconds: '3600'
```
<!-- RUN_HISTORY_ENTRY:END -->
<!-- SECTION:RUN_HISTORY:END -->
