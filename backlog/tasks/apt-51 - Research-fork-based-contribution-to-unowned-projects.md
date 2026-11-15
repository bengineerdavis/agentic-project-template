---
id: APT-51
title: Research fork-based contribution to unowned projects
status: To Do
created_date: 2026-11-14 19:00
updated_date: 2026-11-15 06:12
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Maintained projects need a contributor-conformant path for submitting findings to repositories the maintainer does not own. This is a research question about approved routes and unresolved choices, not a contribution implementation.

Ship:

- Research comparing fork-based pull requests, direct upstream branches where authorized, patch/email workflows, and portable contribution candidates against upstream contributor requirements and available permissions.
- An open-decision record covering fork ownership and reuse, branch naming, authentication and credential scope, remote configuration, target/base selection, draft-versus-ready publication, and source-project finding provenance.
- A reusable candidate-to-submission workflow proposal separating approved local preparation from explicitly approved upstream mutations and reporting the resulting upstream reference.
- Evaluation scenarios for unowned repositories, existing forks, permission failures, protected branches, signed-off commit requirements, sensitive findings, and non-GitHub contribution routes.

Constraints:

- The receiving project’s contributor, security, support, and submission documentation determines the correct route.
- Do not create forks, branches, issues, or pull requests while researching the question.
- Do not prescribe a skill, CLI, or template feature before the research identifies a justified owner.
- Preserve credential boundaries, reporter consent, and security-report privacy.
- Any new skill introduced by a later implementation is declared in agents.toml in the same change.

Agreed with the maintainer 2026-11-14: retain fork-based contribution to unowned projects as a separate parent-template research question.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Research compares supported upstream contribution routes and records rejected options against contributor requirements and permissions
- [ ] #2 The decision record identifies fork, authentication, remote, branch, base, publication, and provenance questions with safe defaults and owners
- [ ] #3 The proposed workflow separates candidate preparation from explicitly approved upstream mutations and records the resulting reference
- [ ] #4 Evaluation scenarios cover unowned projects, existing forks, permission and branch restrictions, commit requirements, sensitive reports, and non-GitHub contribution
- [ ] #5 backlog-py board shows this research task with its full description and acceptance criteria
- [ ] #6 Research compares supported upstream contribution routes and records rejected options against contributor requirements and permissions
- [ ] #7 The decision record identifies approved routes and unresolved choices for fork, authentication, remote, branch, base, publication, and provenance handling
- [ ] #8 The proposed workflow separates candidate preparation from explicitly approved upstream mutations and records the resulting upstream reference
- [ ] #9 Evaluation scenarios cover unowned projects, existing forks, permission and branch restrictions, commit requirements, sensitive findings, and non-GitHub routes
- [ ] #10 backlog-py board shows this research-only task with its full description and acceptance criteria
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
