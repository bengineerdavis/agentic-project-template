# Handoff — wayfinder-template-stack: next session works a frontier ticket

Written 2026-11-06, after T3 closed. Local planning noise by design (see map
Notes); not committed.

## Load order

1. `.scratch/wayfinder-template-stack/map.md` — the low-res index
2. The ticket you claim
3. `.scratch/wayfinder-template-stack/t3-ownership-split.md` — **resolved**;
   its per-concern verdict table is now the ownership authority for every
   other ticket
4. `.scratch/wayfinder-template-stack/t1-inventory.md` — resolved research,
   **but see the corrections below**

## The session

Wayfinder "work through the map". Claim your ticket first (assign before any
work). Grilling tickets — always call the Skill tool twice ("grilling" +
"domain-modeling"). One ticket per session. Refer to tickets by name, never
bare id; decisions live in the ticket, the map only gists.

## Frontier (pick one)

| Ticket | Why it is next |
|---|---|
| **T2 — Standards composition** | Designs the layered-file merge mechanism once, for all nine shared files. Blocks T4. Largest blast radius. |
| **T5 — Structure as spine** | alint bundle layering; carries two verified defects (below). Needs no other ticket. |
| **T6 — Agent operation surface** | Unblocked by T3. Decides what the per-project skill wraps. |
| **T8 — Project-type taxonomy** | Blocked nothing; blocks T7. Four axes already settled in principle. |
| **T9 — License guidance** | Independent. Smallest scope. |

T4 and T7 stay blocked until the above land (T4 needs T2; T7 needs T8).

**Recommended:** T2 — it is the mechanism every other concern move consumes,
and it is what T4 has been waiting on.

## Vocabulary (settled by T3 — use it, don't re-litigate)

- **meta** — makes bases. Not a layer in the project.
- **base** — the NOUN. What kind of repo this is (python, chezmoi).
- **overlay** — an ADJECTIVE. Plural, peer domains, composable (python and
  agentic are both adjectives).

  ⚠️ **"base" was used two ways before T3.** T3 R2/R3 said "the shared base"
  meaning the meta-provided agnostic scaffold; ADR-0002 means the noun
  template. T3's Resolution now uses the ADR-0002 sense throughout. If a
  ticket says "base" ambiguously, it is stale prose — fix it.
- **stack** — one base + one or more base-compatible overlays + composition
  provenance.
- **bound vs portable overlay** — a bound overlay ships with one base and only
  works there; a portable overlay declares requirements and works on any base
  that publishes them. Only portable overlays need the composition contract.

⚠️ **The class analogy is a trap.** Base = class, overlay = mixin, project =
instance is the right *instinct*, but a Copier overlay does not inherit the
base's implementation — it receives the base's **output files**. It decorates
an instance; there is no `super()`. Nothing inherited means nothing guaranteed,
which is why T7's contract must be written down rather than assumed.

## Corrections to T1 (verified empirically 2026-11-06 — do not re-derive)

T1 was written before anyone stamped anything. Four of its claims are wrong:

1. **The meta stamps template repos, NOT projects.**
   `meta_template/<<template_dir>>/` holds only an answers-file placeholder.
   Everything else in `meta_template/` is template-authoring harness. Any
   "meta owns X" claim must name its target — template repo or stamped
   project.
2. **`.gitignore` IS stamped** by python (`template/.gitignore`, confirmed in
   a stamp) and partly composed by agentic per-tool `gitignore.txt`. T1 said
   "not stamped".
3. **`renovate.json` already has its conditional** (`tool_update_strategy`,
   gated on `vcs_platform == 'github'`). T1 said meta doesn't stamp one.
4. **LICENSE is not a simple duplicate.** Meta stamps the *template repo's*
   license; python's `template/LICENSE.jinja` stamps the *project's*. Dropping
   python's would leave generated projects unlicensed.

Also: the LICENSE choice sets run **downhill** — meta asks 16, python's
project renderer handles 2. Nothing to import upward.

## Verified defects to pick up (not yet ticketed as code work)

- `agentic-project-template/template/.alint.yml` hardcodes
  `alint://bundled/python@v1` + a second `ci/github-actions` entry — the
  agentic overlay asserting the Python noun and duplicating the meta's
  `vcs_platform` handling. → T5.
- Both template repos' **root** `prek.toml` run `end-of-file-fixer` and
  `trailing-whitespace` while the alint fragment claims alint owns those.
  Stamped projects are clean; the template repos' self-hosting contradicts its
  own prose. → T5 decision 3.
- **Sharpest one:** a python-only project (base, no overlays) gets **no**
  trailing-whitespace / final-newline / merge-marker enforcement, because
  python's stamped `prek.toml.jinja` is deliberately ruff-only and defers
  hygiene to alint. A base must be correct standalone. `spec.md:280` already
  says the dedicated tool wins and the alint rule is turned off — so the base
  owns hygiene and alint narrows. → T5.
- `python-project-template` cannot produce a non-CLI project
  (`template/pyproject.toml.jinja:31` + `cli.py.jinja` unconditional).
  → T8 (or python's own backlog, T8 decides which).
- `meta_template/copier.yml.tmpl` seeds **no license keys** into a new base,
  so licensing cannot propagate. → T7.
- `cli.py` accepts `--base` as an opaque copier ref with **no validation**;
  `merge.py:deep_merge` is base-wins, so an incompatible base is neither
  detected nor refused. Agentic is multi-base compatible today only by never
  declaring what it needs. → T7.

## State lore may not carry (volatile)

- `backlog/drafts/draft-1` (Reddit multi-agent patterns, five of them incl.
  compaction discipline) is UNCOMMITTED, pending user review — don't commit or
  edit without being asked.
- Commit `6a298fb` (retro outcomes: CODING_STANDARDS.md, apt-29/30/31) sits
  LOCAL on main, NOT pushed. A parallel session/merge owns origin — NEVER
  push, even when a merge-type approval is granted elsewhere.
- `.lore.md` left modified by design (daemon auto-updates it; never stash).
- APT-29/30/31 exist as To Do (CI workflow, dirty-template stamp guard, commit
  wrapper) — unrelated, don't pull them in.
- `branch apt-worktree-guard` carries `f0b6e61` + `d46fe2a` (worktree guard,
  mechanism A), NOT PUSHED. Mechanism B approved, not built; its open
  sub-decision is where the ownership marker lives.
- `copier-template-copier-template/docs/research/repo-types.md` is
  UNCOMMITTED; its own UNVERIFIED warning stands (Cookiecutter Data Science,
  Nx, Yeoman, cargo-generate were never fetched — do not cite them).
- `.scratch/wayfinder-template-stack/prototype/composition-contract.html` is a
  throwaway prototype (T7). Double-click to open. Per the prototype skill, it
  moves to a throwaway branch as a primary source when T7 lands; main keeps
  only the decision.
- ADR-0002 exists ONLY in the unmerged worktree
  `.worktrees/ctct-12-template-taxonomy/`. Meta's `docs/adr/` on main has only
  ADR-0001. CTCT-12 (In Progress) is the task that would land it — check its
  status before T7 does any work, or T7 duplicates it.

## Session rules in force

- Ask the user before any model/subagent call (costs money).
- Research-subagent gotcha: subagents report completed but write no artifact
  file (verified 3×) — do primary-source research directly in the session.
- User has ADD: scannable output; decision points as labeled options with
  recommendations; terse approvals ("continue", bare letters) accept the
  suggested path.
- Never hand-edit backlog/ files (AC-checkbox edits inside markers are
  sanctioned; everything else via the backlog CLI).

## When the map clears

Hand off to the ask-matt main flow: `/to-spec` collapses the linked decisions
into a buildable plan → `/to-tickets` → `/implement`. Don't loop the map
straight into `/implement` — that discards the linked detail.
