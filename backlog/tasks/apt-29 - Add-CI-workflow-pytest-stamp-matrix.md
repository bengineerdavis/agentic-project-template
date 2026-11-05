---
id: APT-29
title: Add CI workflow (pytest + stamp matrix)
status: Done
created_date: 2026-11-04 19:58
updated_date: 2026-11-05 05:31
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The repo has prek hooks but no CI: mise run test / test-template only run when someone remembers, so regressions the suite already catches (tripwire, merge logic) go unverified between local runs. Retro 2026-11-04 finding #1.

Ship:

- GitHub Actions workflow running pytest on every push/PR
- The workflow runs the stamp matrix (test-template) with a pinned TEMPLATE_STAMP_ROOT inside the runner workspace

Constraints:

- Workflow triggers on push to main and pull_request; no scheduled jobs
- Keep the workflow under ~40 lines; no third-party actions beyond checkout + setup-uv
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Workflow runs pytest and test-template on push to main and on pull_request, green on a clean checkout
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Design: one job, two verification steps — the stamp matrix renders three projects, so a two-job split would duplicate the bootstrap block for no isolation benefit. mise tasks remain the single source of truth for what "tested" means: CI installs mise via the mise.run shell script (an installer, not an action — keeps third-party actions to checkout + setup-uv as constrained) and calls mise run test / mise run test-template. TEMPLATE_STAMP_ROOT pinned to ${{ runner.temp }}/stamp-matrix per the Ship bullet and the apt-18/19 shared-/tmp hazard. Shape tests (tests/test_ci_workflow.py) pin triggers, both stages, and the scratch-root env so silent workflow edits fail loudly (note: PyYAML parses bare `on:` as boolean True — the trigger key is checked as True).
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
.github/workflows/ci.yml (36 lines): triggers push→main + pull_request; steps = checkout, setup-uv (python 3.12), mise installer, mise run install, mise run test, mise run test-template with TEMPLATE_STAMP_ROOT inside the runner workspace. Verified: shape tests red→green; full suite 58 passed; clean-clone simulation of the exact CI steps green end-to-end (install → 58 passed → update smoke OK → stamp matrix OK at the pinned root). Commit f46b259.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
