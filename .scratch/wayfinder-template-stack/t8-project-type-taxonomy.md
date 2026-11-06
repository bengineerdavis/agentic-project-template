# T8 — Project-type taxonomy: which axes exist, who asks them, and what acts on them

Type: grilling (HITL) · Blocked by: T3 (resolved) · Blocks: T7
Status: OPEN — frontier · Claimed: nobody

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
2. **`owns_service_lifecycle` — meta or base?** The prior session argued it is
   a noun claim, so it belongs to the layer establishing the noun. But the
   meta-placement rule T3 just adopted ("meta owns what every base needs")
   makes it a candidate for up-top. Unresolved.
3. **Which base acts on `gui`?** Python maps it to `gui_scripts`. What does a
   chezmoi base do with it — nothing? Is an axis a base ignores still asked?
4. **Does T8 own the python base's CLI generalisation**, or does that become
   a python-repo task? The python base's unconditional CLI is a real defect
   under the new model, but it may belong to python's own backlog.
5. **Where does this taxonomy live in the stack's documentation** — the meta's
   GLOSSARY.md, ADR-0002 (unmerged), or a new ADR? The prior session listed
   ADR candidates: noun/adjective model, four axes, raw-axes-only, decision 4.

## Artifacts

- `copier-template-copier-template/docs/research/repo-types.md` — 197 lines,
  per-claim sourced, **UNCOMMITTED**. Its own "UNVERIFIED" warning stands:
  Cookiecutter Data Science, Nx, Yeoman, and cargo-generate were never
  fetched — do not cite them as evidence.
