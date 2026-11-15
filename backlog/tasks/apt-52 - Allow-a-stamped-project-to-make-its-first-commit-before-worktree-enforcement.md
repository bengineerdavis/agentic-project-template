---
id: APT-52
title: Allow a stamped project to make its first commit before worktree enforcement
status: To Do
created_date: 2026-11-15 02:31
updated_date: 2026-11-15 02:35
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A fresh copier-testkit stamp could not make its initial main commit after mise run install installed the worktree guard. Unattended commits are rejected; the supported interactive prompt also failed under PTY and expect automation. The project required an explicitly approved --no-verify initialization commit despite its content checks passing.

Ship:

- A stamp-time initialization design that selects either initializing the Backlog and creating the project’s strategic first commits before installing the worktree guard, or a bounded initialization-only activation path for those commits.
- Red-first template tests reproducing the blocked initial main commit in a fresh stamped project, followed by verification that an unattended agent can complete the approved initialization without a hook bypass.
- Verification that subsequent agent commits remain protected by the worktree guard, including the interactive maintainer override and normal worktree path.

Constraints:

- Choose the activation order from observed behavior and template tests; do not assume a fixed number of initial commits.
- Preserve the guard for ordinary task work; do not weaken it into a general main-checkout exemption or recommend --no-verify as the normal initialization path.
- Keep the Backlog queue and its configured task prefix available before the first project task commit if that route is selected.
- Record any new skill reference in agents.toml in the same implementation change.
- This is parent-template work, not copier-cat or testkit implementation.

Agreed with the maintainer 2026-11-14: the agentic template must support a clean first project initialization before enforcing its ongoing worktree workflow.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The initialization design chooses between early Backlog/strategic main commits and a bounded pre-activation path
- [ ] #2 A red-first fresh-stamp test reproduces the initial-commit deadlock and then passes without a hook bypass
- [ ] #3 The worktree guard still protects subsequent agent commits and retains its human override
- [ ] #4 backlog-py board shows the initialization issue with its full description and acceptance criteria
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Ownership and inheritance check 2026-11-14: the guard is owned by this agentic layer (template/scripts/check-worktree.sh plus fragments/tools/worktrunk/prek.toml); the Python base does not own it. copier-template-copier-template is an agentic-stamped downstream template, with .agentic-answers.yml recording agentic revision 9c25e94. Its checkout has no scripts/check-worktree.sh and no worktree-guard hook, so it does not currently reproduce the exact deadlock. After updating to the affected layer, the same initialization behavior and its fix flow through the agentic Copier update path.

The meta-template already has CTCT-14 (Offer repository initialization after stamping) for optional Git initialization and explicit publication. Its CLI/stamp-seam tests are relevant consumer evidence for APT-52; do not duplicate a second initialization workflow in the meta-template.

Maintainer rule 2026-11-14: for template defects, reproduce the failure at successive source layers and fix the earliest layer that still exhibits it. That root fix lets downstream projects and subproject templates inherit it through their declared update mechanisms. Provenance alone is not proof of a live defect: verify the affected revision and behavior before claiming inheritance or moving ownership upstream.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
