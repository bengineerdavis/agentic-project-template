---
id: APT-36
title: 'Mise-driven CI/CD: research + rollout'
status: In Progress
created_date: 2026-11-07 21:49
dependencies:
- APT-29
updated_date: 2026-11-08 21:36
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Retro/wayfinder item 2. /research + /aboyeur study how to add mise to CI/CD (bootstrap, trust, caching); implement mise-in-CI for THIS repo and prove it; then carry learnings to copier-template-copier-template (meta) and python-project-template (base). Supersedes parts of APT-29's checkout+setup-uv-only constraint.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Research file with primary-source citations exists (docs/research/)
- [ ] #2 This repo's CI runs via mise with proof (green run)
- [ ] #3 Meta + python templates carry the mise CI pattern
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Research COMPLETE (Nov 8, docs/research/mise-ci-cd.md, primary sources: mise.jdx.dev CI + lockfile pages, jdx/mise-action v5 action.yml). Key findings: (1) mise-action is official+node24 but relaxes apt-29's checkout+setup-uv constraint — maintainer call; (2) lockfile is the reproducibility lever: mise.lock --platform linux-x64 + install --locked eliminates per-runner version lookups; (3) cache downloads-cas not installs (trust boundary); (4) CI auto-trusts config — no mise trust step needed; (5) uv=latest pays version-lookup latency every run. Recommendation (a): keep curl installer + add lockfile + downloads cache + lint step (folds retro #2). BLOCKED on implementation by local/origin main divergence (ci.yml only exists on origin/main).
DECISION (maintainer, 2026-11-08): option (a) for now — keep the apt-29 curl installer; add mise.lock + actions/cache on downloads-cas + mise run lint step. Revisit jdx/mise-action later if CI minutes become a real cost.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
