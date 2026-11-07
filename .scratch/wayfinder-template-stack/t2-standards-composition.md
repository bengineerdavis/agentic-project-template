# T2 — Layered-file composition: where does CODING_STANDARDS.md live, and how do sections merge?

Type: grilling (HITL) · Blocked by: T1, T3 (resolved) · Blocks: T4
Status: RESOLVED (2026-11-07) · Claimed: Ben Davis (2026-11-06)

## Question

This ticket decides the **layered-file merge mechanism** once. It starts with
CODING_STANDARDS.md (the maintainer's core ask) but T3 established that
layering is the norm, not the exception: nine shared files need it
(AGENTS.md, CONTRIBUTING.md, .gitignore, CODING_STANDARDS.md, .alint.yml,
LICENSE, mise.toml, prek.toml, opencode.json). The mechanism decided here is
the one all nine use.

For CODING_STANDARDS.md specifically: does the meta own the file + agnostic
defaults via a marked section, do bases append a `## Language` pointer to
convention files (PYTHON.md etc.), and does the agentic layer's vacuity-guard
rule move up or stay down-stack?

Decide the merge mechanics (which existing merge kind: RENDERED_SHARED, marked
section, append) and the removal plan for the current agentic-only file (what
happens on `update` to a project already carrying CODING_STANDARDS.md with the
vacuity rule — base-wins keeps it stale).

## Ownership already settled by T3 (do not re-decide)

- **CODING_STANDARDS.md** — meta: agnostic defaults. Base: language
  conventions pointer. Overlay: judgement-call / vacuity-guard section.
- **CONTRIBUTING.md** — meta: base shape (dev setup, test suites, quality
  gate). Base: language-specific contribution + style sections. Overlay:
  domain sections. Composition required by maintainer (2026-11-06).
- **.gitignore** — meta: agnostic lines. Base: language lines. Overlay: tool
  lines. Composition partly exists (agentic merges per-tool `gitignore.txt`).
- **AGENTS.md** — meta: agnostic shape + backlinks. Base: language commands.
  Overlay: agentic managed section (marked-section upsert already implemented).

## Open questions carried in

- `python-project-template/template/.gitignore` exists and is stamped
  (verified), and also carries `.worktrees/` — an agentic concern sitting in
  the base. Under T3's verdict that line moves to the overlay.
- Per-language convention files do not exist anywhere yet — greenfield shape
  this ticket designs. What is the merge rule when a project stamps two
  language sections?
- Does the mechanism handle *ordering* (base section before overlay section),
  or is order by convention?

## Constraint from T7

The merge mechanism must work given whatever T7 decides about variable flow
(`external_data` vs a shared answers file). If T7's channel changes, a
mechanism keyed on it changes. Coordinate; do not settle T7's question here.

## Round 1 answers (maintainer, 2026-11-06)

- **Q1 (a) — per-writer markers.** The marker names its writer:
  `<!-- BEGIN managed: meta -->`, `:base`, `:overlay`. Each writer replaces
  only its own block. **Prior art confirmed by research** (review-best-practices
  skill): Ansible `blockinfile` is the established tool for this exact problem
  and its docs state the rule plainly — *"When more than one block should be
  handled in one file you must change the `marker` per task"* — with the
  documented multi-block pattern `marker: "# {mark} ANSIBLE MANAGED BLOCK
  {{ item.name }}"` and the warning *"if you do not set a unique mark the block
  will be overwritten on each iteration"*. That warning describes precisely the
  defect proved in `upsert_marked_section`. Matching the established convention
  beats inventing one. **Rejected:** (b) fixed three slots — fails when a
  project has no overlay; (c) append-only ordered by rank — cannot re-render
  idempotently; (d) concatenate inside one marker — cannot remove a
  contribution when an overlay is dropped. **Also researched and rejected:**
  cog (`cogapp`, Ned Batchelder) — content generation into `[[[cog]]]` blocks,
  not multi-owner section ownership; same single-slot shape. No normative
  markdown standard for section ownership exists; that absence is the finding.
- **Q2 (a) — the base creates CODING_STANDARDS.md** with its own section now;
  the meta's agnostic defaults arrive through the same mechanism once T7 gives
  the meta a channel to project files. Keeps T2 unblocked and leaves no
  scaffolding T7 must undo.
- **Q3 (a) — the vacuity-guard rule belongs to the base.** It is a statement
  about tests, not about agents, and applies to any test suite. The overlay
  keeps only genuinely agentic judgement calls.
- **Q4 (a) — pointer only.** `PYTHON.md` is a separate file the base stamps;
  CODING_STANDARDS.md carries `## Language` pointing at it. **Rejected:**
  (b) inline — makes the file the union of every language and defeats separate
  files; (c) pointer + summary — guarantees drift between summary and source.
- **Q5 — polyglot merge is out of scope**, recorded on T8. See the vocabulary
  correction below, which is a bigger change than the deferral.
- **Q6 (a) — a named migration** in `merge.py` that detects the legacy
  agentic-only file by exact content match and moves the vacuity rule under the
  new base marker. Precedent: `_LAYER_AUTHORED_SCRIPTS` in
  `merge_mise_fragment`. **Rejected:** (b) warn only — the rule is
  load-bearing; a stale copy that looks maintained is worse than a knowingly
  stale one, and it warns forever; (c) rewrite — cannot distinguish layer
  content from project content, and would be the only place in the merge engine
  that discards project edits.

### Vocabulary correction prompted by Q5 (option iii, adopted)

The maintainer challenged "base = python": *"isn't a python project in our case
an agnostic base with a python overlay as the extension (python describes the
project, it isn't the project itself)?"* **The maintainer is right, and the
earlier recording was wrong.**

Evidence for the maintainer's model:

1. The four type axes are language-agnostic (`is_distributed`,
   `has_entry_point`, `gui`, `owns_service_lifecycle`). A language-bound base
   would make a python CLI and a rust CLI different *nouns*.
2. The model's own claim — "python and agentic are BOTH adjectives, neither
   outranks the other" — only holds if neither is the base. Recording python as
   the base quietly re-demoted agentic, the same error the earlier session made
   in the opposite direction.
3. It explains the T5 defect: a python-only project has no hygiene enforcement
   because python assumed agentic would supply it and nothing owned it. An
   agnostic base owning hygiene makes both python-only and python+agentic
   projects correct.

Honest costs: no agnostic base exists yet (`python-project-template` is the only
template that produces a project); ADR-0002 defines base as "a regular Copier
template that produces a project"; the shipped CLI flag is
`--base python-project-template`; and an agnostic base with no language, build,
or test runner is not usable alone.

**Adopted: option (iii), transitional.** The maintainer's model is the target
end state. Python's *base* role stays documented as **temporary scaffolding**
until an agnostic base exists, with the reason recorded. This reaches the
correct end state without shipping a vocabulary that contradicts the flags in
the CLI today.

Consequence for this ticket: "base creates CODING_STANDARDS.md" (Q2) means the
**current** base (python), i.e. what becomes the language overlay once the
agnostic base exists. The mechanism must not assume language-specificity —
whoever writes the agnostic section is whichever layer plays the noun role at
the time.

## Implementation (2026-11-06)

Built, not just decided.

**`merge.py`** — `WRITER_MARKERS = {"meta": 0, "base": 1, "overlay": 2}` is the
rank map; document order follows it, independent of write order.
`managed_block(writer, section)` renders one block and rejects an unknown
writer. `_split_blocks` separates managed blocks from project prose and
**adopts the legacy un-named marker as the overlay block**, so a project
stamped before this change migrates on its next update instead of keeping a
stray block. `upsert_marked_section(destination, section, writer="overlay")`
keeps its old signature for existing call sites and now touches only its own
writer's block. `remove_managed_section(destination, writer)` drops one block
and deletes the file only when nothing (no block, no prose) remains.

**`stamp.py`** — writes `CODING_STANDARDS.md` when absent, using
`CODING_STANDARDS_HEADER` (written **once**, never rewritten: it is the
project's prose), then upserts the base block from
`fragments/coding-standards-base.md`. Verified idempotent across repeated
stamps.

**TDD.** `tests/test_layered_markers.py` — 11 tests, written first and seen to
fail on the missing API. Mutation-tested: forcing every writer onto one marker
(the old defect) fails 7 of them, so they test the mechanism rather than
restating it. Full suite 66 passed.

### The Q6 migration had no subject — corrected

Q6 assumed projects carry a legacy agentic-only `CODING_STANDARDS.md`.
**Verified false:** neither layer stamped the file. A fresh stamp produced no
`CODING_STANDARDS.md`, and python's `template/` has no standards file either —
it existed only inside this repo. So the migration Q6 selected has nothing to
migrate *for CODING_STANDARDS.md*.

The mechanism still earns its place, because the same problem exists for
**AGENTS.md**, which *is* stamped and *does* carry the legacy marker. Verified
end to end: a project with the old
`<!-- BEGIN managed: agentic-project-template -->` block, re-stamped, ends up
with exactly one `overlay` block, the stale body gone, and project prose
preserved. That is the legacy-adoption branch in `_split_blocks`.

Recorded rather than silently reinterpreted: Q6's decision stands, its stated
subject was wrong, and the real subject (AGENTS.md) is now proven to work.

## Facts established before this round (verified 2026-11-06)

### The marker mechanism cannot hold three writers — proven

`merge.upsert_marked_section` uses a single global marker
(`MARKER_BEGIN = "<!-- BEGIN managed: agentic-project-template -->"`) and
replaces the whole block on every call. Verified by running it twice:

```
after writer A:  <!-- BEGIN managed -->  ## Testing / - meta rule  <!-- END -->
after writer B:  <!-- BEGIN managed -->  ## Language / - python rule  <!-- END -->
```

Writer B **silently destroys** writer A's section. `MARKED_SECTION_RE` is
non-greedy and matches the first block, so there is exactly one slot per file.
This is a second-instance defect of the T1 "three writers, no contract" class,
and it means the current mechanism *cannot* serve a layered file as-is.

### List-merge is cross-domain safe, not collision-safe

`deep_merge` concatenates lists and dedupes only by exact item (or by `name`
for named lists). Verified: merging a base's `.alint.yml` `extends` with the
overlay's yields the union with **no warning** — so the duplicated
`python` bundle from T3's defect would have been invisible. Lists merge; they
do not detect a second claim on one concern.

### The surface area is manageable

`CODING_STANDARDS.md` is 18 lines and contains exactly one section
(`## Testing`, the vacuity-guard rule). Whatever mechanism is chosen has a
tiny first customer — no migration risk in the file's own content.

### The four merge primitives that already exist

| Primitive | Kind | Used for today |
|---|---|---|
| `upsert_marked_section` | markdown, one marker, replace | AGENTS.md managed section |
| `deep_merge` / `merge_toml_file` / `merge_json_file` | structural, base-wins | mise.toml, opencode.json |
| `merge_prek_config` | append `[[repos]]`, dedupe | prek.toml |
| `append_gitignore_lines` | append unseen lines | .gitignore |

Two of the nine layered files (`.gitignore`, `prek.toml`) already have
satisfactory mechanisms. Two markdown files (AGENTS.md, CODING_STANDARDS.md)
are stuck on the single-slot marker. `CONTRIBUTING.md` and `LICENSE` have no
mechanism at all.

## Resolution

The layered-file merge mechanism is built and merged (`4b0348f`). Per-writer
markers with rank order meta → base → overlay; `upsert_marked_section` keeps
its signature and defaults to the overlay writer; `remove_managed_section`
removes one rank without touching the others or the project's prose; the
legacy un-named mark is adopted as the overlay block, so a project stamped
before the change migrates on update.

`CODING_STANDARDS.md` is created when absent, with `CODING_STANDARDS_HEADER`
written once as the project's prose and the base block upserted from
`fragments/coding-standards-base.md`.

**This unblocks T4**, which now has both the mechanism to migrate projects
onto and a worked, tested example of a migration (the legacy-adoption branch).

What the mechanism does *not* decide, and T7/T4 still own:

- the meta's channel into project files, so `meta` blocks can be written at
  all (today only `base` and `overlay` have writers);
- whether the overlay adds a CODING_STANDARDS section — today it adds none;
- AGENTS.md's `overlay` content and CODING_STANDARDS' `base` content are the
  only two writers wired to real fragments. The other layered files
  (`.alint.yml`, `CONTRIBUTING.md`, `LICENSE`, `opencode.json`, `mise.toml`,
  `prek.toml`, `.gitignore`) still use their own primitives and are unchanged
  by this ticket.
