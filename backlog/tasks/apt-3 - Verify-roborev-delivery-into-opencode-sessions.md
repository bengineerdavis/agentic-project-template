---
id: APT-3
title: Verify roborev delivery into opencode sessions
status: Done
created_date: 2026-10-12 18:19
updated_date: 2026-10-20 15:18
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Documented agent-hook list may not include opencode. Resolves spec open question 2.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Findings delivery into live opencode sessions verified, or the fallback (mise task + skill instruction) confirmed as the v1 path
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Fallback confirmed as the v1 path 2026-10-18 on the redge stamp: roborev daemon + hooks installed via the layer install task; findings surface through mise tasks roborev-status/roborev-fix plus the stamped review-findings skill (project-local, committed, verified present). Background reviews queue and run with agent=opencode; some jobs failed (execution reliability to watch), so the fallback stays primary until that is diagnosed.
2026-10-20: diagnosis landed via apt-21 — every job failed pre-start because the opencode agent resolved to the mise-pinned V1 binary, which rejects the V2 global config. After the http-backend pin (7e07e72) background reviews run end-to-end (job 116 completed with findings). The mise roborev-status/roborev-fix tasks + review-findings skill demote to the outage path.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
