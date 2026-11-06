# T9 — License guidance: a choosealicense-style surface for the licensing decision

Type: grilling (HITL) · Blocked by: T3 (resolved) · Consumed by: T2, T7
Status: OPEN — frontier · Claimed: nobody

## Question

The meta already asks `license_type` with 16 choices
(`copier-template-copier-template/copier.yml:182-202`, SPDX texts verbatim
from `spdx/license-list-data`). The maintainer's ask (2026-11-06) is not more
choices — it is **help deciding**. A choosealicense-style surface, either an
interactive menu or an agent-assisted session, that reasons about the choice.

The maintainer's stated position, which the surface should serve:

- Personal default is **FSL** (Functional Source License) — the least-privilege
  starting point, with a roadmap step to consider something more permissive
  later. FSL-1.1 converts to MIT (or Apache-2.0) after two years.
- Two decision axes named: **monetisation** ("I want to make the tool and
  decide if I want to make money from it, or be paid by those who want to make
  money from it, or not care") and **copyleft** ("whether I want to force users
  to make modifications/combinations available to me as contributions").

## Open questions

1. **Where does the guidance live?** Three candidates: (a) additional
   `copier.yml` questions — a decision-tree of intents that derives
   `license_type`; (b) an agent-assisted interactive session that reasons and
   writes the answer; (c) both — questions for the scripted path, an agent
   skill for the reasoning path. Note the `license_type` question is asked by
   the **meta**, but the consequence lands in a **project** — so T7's variable
   flow constrains which is possible.
2. **Does the meta's default change from MIT to FSL-1.1-MIT?** Today
   `license_type` defaults to MIT. The maintainer's stated default is FSL. This
   is a one-line change with a large blast radius (every future base and
   project), so it needs an explicit decision, not an inference.
3. **Is the reasoning aid a noun or an adjective?** Legal/licensing guidance is
   not language-specific; by T3's rule it is meta-owned. But an agent skill is
   agentic-shaped. Candidate answer: the *content* (decision tree, intent →
   license mapping) is meta-owned; a skill that delivers it is one possible
   consumer.
4. **What maps to what?** Needs an intent table: least-privilege / no
   monetisation concern / copyleft / permissive / patent grant / "I don't
   care" → SPDX identifier. `repo-types.md`-style sourcing applies: cite
   choosealicense.com and the SPDX list, not memory.
5. **Does the surface warn about the FSL pyproject gap?** Verified: FSL
   identifiers are not in the SPDX list, so the generated `pyproject.toml`
   omits the `license` key for them. A chooser that recommends FSL should say
   so.

## Not in scope

The licence *texts* (already present, verbatim, all 16) and the propagation
chain (T3's verdict: meta owns corpus + choice set, base owns the project
renderer). This ticket is the decision aid only.
