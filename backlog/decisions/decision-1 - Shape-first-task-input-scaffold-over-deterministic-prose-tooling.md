---
id: decision-1
title: Shape-first task-input scaffold over deterministic prose tooling
date: 2026-10-27 15:08
status: accepted
---

## Context

Task records kept failing two ways: a dense single paragraph buried the
deliverables, and the done-definition drifted across description, acceptance
criteria, and the Definition of Done section. APT-22 and APT-24 were reshaped
by hand on 2026-10-26, and the `backlog-task` skill was authored to enforce
the shape at creation time. The alternative was deterministic tooling now:
vale with the Google style ruleset plus flowmark, codespell, and lychee in
prek — the prose lane sketched in ARCHITECTURE.md.

## Decision

Task-input quality is enforced by shape and skill, not linting. The
description follows why / Ship / Constraints / dated decision record; every
Ship bullet gets one acceptance criterion; the AC block is the single done
source (the DOD section stays empty, matching store convention); prose edits
stay inside the section markers backlog-py parses. The `backlog-task` skill
in ai-prompt-library, declared in `agents.toml`, carries the rules and
applies plain-english and writing-for-agents as the writing standards.

## Consequences

The vale prose lane in ARCHITECTURE.md stays future until the skill proves
insufficient — the revisit trigger is repeated shape violations that the
skill fails to prevent. Task records commit to the shape going forward;
existing dense records get reshaped only when touched. Decisions of this
kind are recorded here, in backlog/decisions/, rather than only inside task
files.
