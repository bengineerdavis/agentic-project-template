# T8 — Project-type taxonomy: which axes exist, who asks them, and what acts on them

Type: grilling (HITL) · Blocked by: T3 (resolved) · Blocks: T7
Status: IN PROGRESS · Claimed: Ben Davis (2026-11-07)

## Facts verified before this round (2026-11-07)

The prior session's axis research (`copier-template-copier-template/docs/research/repo-types.md`)
was **re-verified rather than inherited**, and the load-bearing claim checked
against a live toolchain:

- **The axes are orthogonal and combinable.** `cargo init --lib` plus a
  `src/main.rs` yields one package whose metadata reports **both** `['lib']`
  and `['bin']` targets. So project type is not an enum; a single repo can
  occupy several cells at once.
- **Python's CLI is unconditional — this is the defect.** `template/pyproject.toml.jinja`
  emits `[project.scripts]` with `{{ cli_name }} = "{{ project_slug }}.cli:app"`
  with no conditional, and `template/src/*/cli.py.jinja` is stamped
  unconditionally. `copier.yml` asks 15 questions and **none** is about project
  type. `cli_name` is always asked.
- **`python-project-template` scaffolds no GUI** — no `gui_scripts`, no `gui`
  question, nothing in `template/`. **Corrected 2026-11-08:** an earlier
  version of this line read "Python has no GUI support at all", which was a
  category error — one grep of a *template repo* was reported as a fact about
  the *language*. Python ships GUI support in the standard library (`tkinter`,
  Tk 8.6 verified on the maintainer's machine) and has a large third-party
  ecosystem; the *template* emits only `[project.scripts]`. Verified against
  docs.python.org and the PyPA entry-points spec; recorded in the python repo's
  `docs/research/python-gui-support.md`.
- The research doc's own **UNVERIFIED** list stands (Cookiecutter Data Science,
  Nx, Yeoman, `cargo-generate` were never fetched). They are not cited here.

## Round 1 answers (maintainer, 2026-11-08)

- **Q1 (a) — meta asks at creation; existing projects get inferred.** Conditional
  on resolving the staleness question: *what happens when a new key appears, or
  a key's meaning moves enough that the next update must re-ask?* See the
  prototype below; the answer is not settled and Q1 cannot be implemented
  without it.
- **Q2 (c) — meta records `owns_service_lifecycle`; the layer owning service
  wiring acts on it.** Same staleness caveat.
- **Q3 (c) — record `gui`, and file the missing support as its own ticket.**
  With a correction: the premise of the question was wrong (see the GUI
  correction above). The axis is real and python *can* act on it.
- **Q4 — yes**, capturing the build work T8 generates is correct. T8 owns the
  design; the build goes to backlog tasks.
- **Q5 — organize via the backlog tool, spec-driven.** Build work T8 generates
  is filed as backlog tasks (not the wayfinder tickets themselves — the map
  stays coherent until it clears and hands off to `/to-spec`). HITL
  confirmation is requested before build work is finalized as a backlog draft.

## The staleness state machine (prototype, 2026-11-08)

`prototype/answer-staleness.html` — throwaway, double-click, no persistence.
It crosses **8 template changes** against **6 project answer states** (48
cells, 39 modelled, 9 impossible) and marks every cell where today's shipped
behaviour disagrees with what it should be: **18 disagreements**. Those 18 are
the bug surface.

Template changes: unchanged · new question · renamed · removed · semantics
bumped · default changed · allowed values changed · became conditional.

Answer states: no answer · explicit-and-valid · explicit-but-stale ·
accepted-the-default · value-no-longer-allowed · question-gone.

Actions: keep · fill default · **re-ask** · migrate · drop + warn.

### What today actually does

`_include_flag` is the only staleness logic in the codebase: a missing key
takes the default, so a stamp predating a question never breaks. Everything
else is kept silently, forever. That is correct for feature toggles and wrong
for structural facts about a project.

### The five cases that break the naive design

1. **"Chose it" vs "accepted it" are indistinguishable.** The answers file
   stores values only, so two projects with `include_git_ai: false` — one typed,
   one defaulted — are byte-identical. Any rule that treats them differently
   needs provenance the file does not carry. The real choice is *which of the
   two you are willing to be wrong about*.
2. **The semantics trap is the only class where keeping is actively wrong.**
   When a key's meaning moves, "preserve the user's answer" applies consent
   given for one thing to another. It is silent and consent-free, and the file
   still looks correct.
3. **A rename silently reverses a deliberate choice.** With no mapping, the new
   key is absent, defaults fill, the human's opt-in is undone, and the old key
   lingers unowned. Fix shape: a declared old→new mapping — the
   `_LAYER_AUTHORED_SCRIPTS` pattern applied to keys.
4. **A new question is not always safe to default.** "Missing key takes the
   default" is right for toggles and wrong for structural facts. The distinction
   is not old-vs-new key; it is *is this key a claim about the project?*
5. **An answer can outlive its gate.** When a question becomes conditional and
   the gate goes false, the answer is unreachable but present; flip the gate
   back and a choice made in a different world re-applies. Dropping is right
   only if the update records *why*.

### Consequence for Q1/Q2 — the design is not implementable yet

The maintainer's Q1 answer (a) requires distinguishing "human chose" from
"template defaulted". **The answers file cannot express that**, so (a) needs a
provenance field or a sidecar before inference can be safe. That is a design
decision this ticket now carries, not a build detail. Recorded, not silently
deferred.

### Provenance decision — AGREED 2026-11-08: sidecar file

Maintainer chose **(b) sidecar**: a `.agentic-provenance.yml` written only by
the layer CLI, recording which answer keys a human set. Rejected: (a) an
in-file `_provenance` map, because copier overwrites `.agentic-answers.yml` on
every copy and update, so that map would have to fight the tool that owns the
file; (c) inferring from git history, wrong whenever the answers file was
committed alongside unrelated edits.

**Verified empirically before recording** (scratch dir, not the repo):

1. A file the template does not render is **not** ignored by `copier update`.
   A hand-written `.agentic-provenance.yml` survived an update byte-identical.
   copier only rewrites the paths it renders; anything else in the destination
   is untouched.
2. The `.gitignore` the layer stamps does **not** match it (`git check-ignore`
   reports no match), so it is committed and travels with the project.
3. Bare `copier copy` writes `.agentic-answers.yml` but applies **no
   fragments** — no `mise.toml`, no `prek.toml`, no `AGENTS.md`, no
   `backlog/`. See "Pure-copier viability" below; this is why it matters.

### Pure-copier viability — ASKED BY MAINTAINER, ANSWERED 2026-11-08

The maintainer asked whether (b) still works "if the user only uses the copier
templates, minus future copier-cat management". It does not, and the reason is
not the sidecar — it is that **the layer is not usable through copier alone
today**. Verified against the repo, not assumed:

- **`copier update` needs `.copier-answers.yml`; the layer writes
  `.agentic-answers.yml`.** A bare `copier update --defaults` in a layer-stamped
  project fails with *"Cannot update because cannot obtain old template
  references from `.copier-answers.yml`"*. The update only proceeds when the
  invocation is told `-a .agentic-answers.yml`, i.e. when it is driven by the
  layer CLI (`cli.py:133-139` passes `answers_file=".agentic-answers.yml"`).
- **`copier.yml` declares no `_tasks`.** Fragments (`fragments/mise-layer.toml`,
  `fragments/tools/*`, the AGENTS.md sections) are merged by
  `apply_fragments()` in `stamp.py`. Bare `copier copy` therefore produces a
  project missing `mise.toml`, `prek.toml`, `AGENTS.md`, and `backlog/` — the
  layer's own wiring.
- **`_answers_file` is declared, `_tasks` is not.** So there is no
  copier-native hook that could apply the fragments or write a provenance file.

**Conclusion for (b):** the sidecar is written by the layer CLI, and today the
layer CLI is the only supported entry point anyway. So the decision is
*consistent* with a pure-copier world — but it does not make the layer
pure-copier-capable. If a future goal is "usable through `copier copy` and
`copier update` with no CLI", two things must be added to `copier.yml`
independently of provenance: `_tasks` entries that run the fragment merge, and
a first-render path that writes the sidecar. That is a separate ticket, not a
provenance detail, and it is recorded on the map rather than folded in here.

The inverse also holds and is worth naming: because the CLI owns the entry
point, the sidecar has no competing writer. Neither copier nor a future
copier-cat would touch it, since neither renders that path.


## Question

Every stamping layer needs to know what kind of repo it is stamping. Today
nothing records it. Verified 2026-11-06: the meta's 27 `copier.yml` questions
configure the template and repo governance; **none is a project-type axis**. A
stamped project cannot tell a downstream overlay whether it is a library, a
CLI, or a repo that owns a service's lifecycle. Meanwhile
`python-project-template/template/pyproject.toml.jinja:31` emits
`[project.scripts]` unconditionally and always stamps `cli.py`, so the python
base cannot produce a non-CLI project at all.

This is the generalisation the chezmoi base depends on.

## Settled before this ticket (2026-11-06, prior session)

Recorded here so the ticket is self-contained; not re-opened.

1. **Two ranks, not three.** meta makes bases; base is the noun; overlays are
   adjectives (plural, peer domains, composable). Python and agentic are both
   adjectives — orthogonal domains, neither outranks the other.
2. **Four axes, as flags not an enum:** `is_distributed`, `has_entry_point`,
   `gui`, `owns_service_lifecycle` (renamed from `is_service` — the axis asks
   whether the repo installs and owns a unit's lifecycle, not whether it "is"
   a service). Flags because verified Cargo behaviour holds a library and a
   binary simultaneously: `cargo metadata` reports `[['lib'], ['bin']]`.
3. **Base asserts the noun; overlays adjust.** Overlays declare what they
   require and refuse to stamp on mismatch.
4. **Adopt-time nouns: option (b)** — overlays declare, base does not
   reconstruct. Revisit after usage data.
5. **`gui`: meta asks, base acts.** It is a noun, and only the base has a
   consequence (Windows-only).
6. **Raw axes only; bases derive.** Do not stamp `cli` / `library` — one
   source of truth.
7. **Agentic tool vs agentic practice needs no new axis.** "The product is an
   agent" is a noun (→ base); "how the project is built" is an adjective
   (→ agentic overlay).
8. **Ask centrally, act locally.** The meta seeds type questions into a new
   base's `copier.yml`; the base owns acting on them.

## Open questions

1. **Where do the axes get asked of an existing project?** The meta asks at
   *base-creation* (what kind of projects does this base make?). But a project
   stamped from that base needs its own values. Does the base re-ask them, or
   does the base's `template/copier.yml` inherit them as fixed defaults?
2. ~~**`owns_service_lifecycle` — meta or base?**~~ **RESOLVED 2026-11-07:**
   base. It is a noun claim, and the decisive argument is structural rather
   than a popularity test: the base establishes the noun, so the base acts on
   it. The maintainer's placement refinement (below) points the same way —
   putting it in the base keeps overlays fewer and simpler, and it is
   something asked of every git project in an agnostic way. The meta *may*
   ask it when seeding a new base's `copier.yml` (decision 8, ask centrally,
   act locally); asking and owning are different.

   The maintainer's provisional refinement to T3's placement rule: if a
   concern in the BASE means fewer and less complex overlays, and it is
   something we would ask ourselves for every git project agnostically, the
   base should own it. Note this pulls DOWN toward base while T3's "every
   stamped project wants it" pulls UP toward meta — the tension between the
   two is recorded, not resolved.

3. ~~**Which base acts on `gui`?**~~ **RESOLVED 2026-11-07, REFINED 2026-11-08:**
   meta asks, python base acts. It is a noun, and only the base has a
   consequence for it. **The "Windows-only" gloss is accurate** — verified
   against the PyPA entry-points spec, which says plainly: "The difference
   between `console_scripts` and `gui_scripts` only affects Windows systems."
   A base that ignores an axis simply does not read it — that is what
   `extends:` declares.

   **Corrected 2026-11-08 (second time).** An earlier revision of this line
   said the Windows-only gloss "was too strong" — that was wrong, and the spec
   says so directly. What is genuinely open is narrower: whether the python
   template *should* scaffold GUI. The language supports it (stdlib `tkinter`,
   no dependency) and `gui_scripts` exists for it; the template emits only
   `[project.scripts]`. That is a template-design question, not a
   language-capability one. See the python repo's
   `docs/research/python-gui-support.md`.
4. ~~**Does T8 own the python base's CLI generalisation**~~ **SPLIT
   2026-11-07:** T8 owns the *contract* (which axes exist, who asks, who
   acts); the python repo owns the *implementation* of `has_entry_point`
   gating its unconditional `cli_name`. The defect is real either way — see
   `python-project-template/template/pyproject.toml.jinja:31`, which emits
   `[project.scripts]` for every stamp — but it is a python-repo change, not
   a T8 decision.
5. **Where does this taxonomy live in the stack's documentation** — the meta's
   GLOSSARY.md, ADR-0002 (unmerged), or a new ADR? The prior session listed
   ADR candidates: noun/adjective model, four axes, raw-axes-only, decision 4.

## Artifacts

- `copier-template-copier-template/docs/research/repo-types.md` — 197 lines,
  per-claim sourced, **UNCOMMITTED**. Its own "UNVERIFIED" warning stands:
  Cookiecutter Data Science, Nx, Yeoman, and cargo-generate were never
  fetched — do not cite them as evidence.
