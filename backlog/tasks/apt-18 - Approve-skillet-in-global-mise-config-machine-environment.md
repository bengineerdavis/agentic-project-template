---
id: APT-18
title: Approve skillet in global mise config (machine environment)
status: In Progress
created_date: 2026-10-15 08:45
updated_date: 2026-10-15 13:37
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
aube refuses npm:@sentry/skillet (7 weekly downloads vs 1000 threshold); it is declared in ~/.config/mise/config.toml, so every mise run on this machine aborts at auto-install until approved. Requires user verification of the package, then allow_low_downloads = true on the tool entry. Related: /tmp/fslock root-owned (sudo chown needed, or TMPDIR inline as workaround). Verified: TMPDIR=/tmp/opencode unblocks aube; dotagents installs fine.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 mise run completes without tool-install errors on this machine
- [ ] #2 Durable fix recorded (chown and/or allow_low_downloads)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
skillet approved in global mise config (user-approved, allow_low_downloads applied 2026-10-14); mise run install verified end-to-end with TMPDIR=/tmp/opencode. Remaining: durable /tmp/fslock fix — sudo chown -R bdavis:bdavis /tmp/fslock (needs user password) or TMPDIR in shell env.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
