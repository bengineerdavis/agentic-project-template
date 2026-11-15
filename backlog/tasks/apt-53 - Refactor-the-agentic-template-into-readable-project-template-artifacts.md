---
id: APT-53
title: Refactor the agentic template into readable project-template artifacts
status: To Do
created_date: 2026-11-15 16:25
references:
- https://github.com/bengineerdavis/copier-cat/blob/main/backlog/tasks/ccc-31%20-%20Design-a-ccc-driven-project-template-specification.md
- https://github.com/bengineerdavis/copier-cat/blob/main/GLOSSARY.md
- https://github.com/bengineerdavis/copier-cat/commit/c16c279de6a4d1a4d4bd40f97bb2671897c048a8
- template/.alint.yml
- src/agentic_project_template/stamp.py
- https://github.com/bengineerdavis/copier-cat/blob/main/backlog/docs/cc-assembly-mvp-spec.md
- https://github.com/bengineerdavis/copier-cat/tree/prototype/cc-composition-evidence/prototype/cc-composition-evidence
updated_date: 2026-11-15 16:29
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Agentic-project-template currently expresses much of its stamping and composition behavior through Python scripts. This makes template intent, artifact ownership, and merge behavior difficult to review and contributes to uncertainty about why configuration such as .alint.yml is absent from some stamped projects.

Ship:

- A grill-with-docs refactor discussion using copier-cat CCC-31 and its research evidence as the shared design input; settle artifact ownership before changing template representation.
- A representation and interface plan that distinguishes ordinary Copier/Jinja project-template content, declarative composition data, imperative compatibility logic, and generated or manually maintained artifacts.
- An alint provenance investigation that traces template/.alint.yml, stamp.py clean-path and conditional-path rules, answers files, and the actual stamp matrix before assigning defect ownership.
- Focused follow-up tasks for approved refactors and any demonstrated missing-artifact defect, with stamp-matrix and generated-output evidence.

Constraints:

- Do not assume the current Python implementation should all become declarative or disappear. Determine which behavior belongs in a project template and which behavior is a rendering or composition runner.
- Keep agentic-project-template independently renderable and language-independent; preserve each stamped project’s native Copier update path and existing local artifact conventions.
- Use copier-cat’s community research and review-best-practices evidence before choosing a new specification or manifest. Do not make APT implementation wait for the full research project.
- Investigate why .alint.yml is absent in copier-cat and present in copier-testkit without assuming copier-cat was agentic-stamped. Its recorded .copier-answers.copier-cat.yml currently names only python-project-template. Preserve each project’s actual provenance and do not add agentic answers as a workaround.
- Start with a fresh refactor discussion and grill-with-docs; record decisions in GLOSSARY.md and ADRs as they settle. Follow with focused to-spec/to-tickets work only for approved changes.
- Reconcile main and other sessions’ work before implementation; preserve their dirty files, branches, and worktrees. New skill references require an agents.toml declaration in the same implementation change.
- This task captures discussion and investigation only; it does not implement the refactor, change stamp behavior, or modify downstream projects.

Agreed with the maintainer 2026-11-15: move artifact ownership and template-readability feedback into a fresh agentic-template refactor discussion with copier-cat attribution.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The fresh grill-with-docs discussion addresses artifact ownership, readable project-template intent, and the boundary between declarative composition data and imperative runner logic
- [ ] #2 The interface and representation plan covers ordinary Copier artifacts, generated or manually maintained artifacts, independent rendering, and native updates
- [ ] #3 The alint investigation traces actual provenance, stamp rules, answers files, and stamp-matrix evidence before assigning ownership
- [ ] #4 Approved refactors and demonstrated defects have focused follow-up tasks without modifying downstream projects in this task
- [ ] #5 backlog-py board shows the refactor task with its full description and acceptance criteria
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Attribution: this task came from the copier-cat template-readability and stamping-consistency review. CCC-31 and copier-cat’s glossary are the upstream research and vocabulary resources this discussion can integrate.

Current source evidence: template/.alint.yml contains the managed-by-agentic-project-template marker and alint bundle extensions. src/agentic_project_template/stamp.py owns clean-path, conditional-path, managed-overwrite, and fragment-merge application. tests/test_stamp.py includes an alint-config assertion for fresh stamps. Those facts show where to investigate; they do not establish why any particular project lacks the artifact.

Additional reusable resources: copier-cat’s DOC-9 assembly contract and prototype evidence branches prototype/cc-assembly-ux and prototype/cc-composition-evidence. This task does not copy or modify those artifacts; it references them so the refactor can use their composition findings.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
