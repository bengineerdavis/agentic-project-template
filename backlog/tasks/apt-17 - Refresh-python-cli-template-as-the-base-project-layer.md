---
id: APT-17
title: Refresh python-cli-template as the base project layer
status: To Do
created_date: 2026-10-13 06:00
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
bengineerdavis/python-cli-template exists but predates the house conventions. Refresh it so the agentic layer composes onto it: mise harness (no Task), prek.toml, two-tier .context convention compatibility, and the composition contract from ARCHITECTURE.md. Note: copier-template-copier-template fork (cbrown1234's, now customized with mise + SPDX licensing) covers the make-a-template side; this covers the python project side.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Template renders and stamp-tests cleanly
- [ ] #2 apt layer stamps over it with both answers files intact
- [ ] #3 Resolves apt-2 (with-base composition against a real base)
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
