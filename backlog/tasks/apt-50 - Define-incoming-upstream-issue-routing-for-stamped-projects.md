---
id: APT-50
title: Define incoming upstream-issue routing for stamped projects
status: To Do
created_date: 2026-11-14 18:56
updated_date: 2026-11-15 06:11
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Projects stamped from the agentic template may receive reports about behavior owned by a base template, a third-party dependency, or another source project. Reviewers need a routing contract that preserves evidence and respects reporters without silently redirecting them or publishing their findings by default.

Ship:

- An ownership-routing policy that classifies reports as stamped-project behavior, agentic-layer behavior, base-template behavior, third-party upstream behavior, or unresolved ownership.
- A reporter-facing response pattern that explains the owning project, preserves reproduction and affected-version evidence, and points to the appropriate upstream tracker or support channel.
- An upstream-communication path that checks the receiving project’s contributor, issue, security, support, and duplicate-report conventions before proposing a submission.
- A consent and privacy boundary covering reporter permission, redaction, confidential or security-sensitive reports, and preservation of the original local reference.
- Stamped guidance and evaluation cases covering unknown ownership, coordinated downstream/upstream changes, duplicate reports, and unavailable submission channels.

Constraints:

- Do not implement this routing policy in copier-cat or treat it as part of the assembly MVP.
- The agentic layer owns the reusable guidance; downstream projects may link or delegate but must not silently redirect reporters.
- Naming an upstream component is not sufficient proof of ownership or grounds for an upstream issue.
- Obtain explicit approval before any upstream publication. Do not expose third-party report contents, credentials, private paths, or security details without authorization and required redaction.
- Any new skill reference introduced by implementation is declared in agents.toml in the same change.

Agreed with the maintainer 2026-11-14: publish incoming-report ownership and response routing as one focused parent-template concern.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The policy classifies downstream, agentic-layer, base-template, third-party upstream, and unresolved ownership
- [ ] #2 The reporter response preserves evidence and points to the appropriate upstream channel without silent redirection
- [ ] #3 The upstream path follows the receiving project’s contributor, issue, security, and support conventions
- [ ] #4 Third-party consent, privacy, redaction, and original-reference preservation are explicit
- [ ] #5 Stamped guidance and evaluations cover duplicates, unknown ownership, and coordinated downstream/upstream changes
- [ ] #6 backlog-py board shows the routing task with its full description and acceptance criteria
- [ ] #7 A reviewer can classify downstream, agentic-layer, base-template, third-party upstream, and unresolved ownership and determine the appropriate response
- [ ] #8 The reporter response preserves evidence and points to the appropriate upstream channel without silent redirection
- [ ] #9 The upstream path checks contributor, issue, security, support, and duplicate-report conventions before proposing a submission
- [ ] #10 Third-party consent, privacy, redaction, security handling, and original-reference preservation are explicit
- [ ] #11 Stamped guidance and evaluations cover unknown ownership, coordinated downstream/upstream changes, duplicate reports, and unavailable submission channels
- [ ] #12 backlog-py board shows the incoming-report routing task with its full description and acceptance criteria
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
