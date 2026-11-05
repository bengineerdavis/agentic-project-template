# T1 resolution — Inventory: what does each stack repo own today?

Type: research (AFK) · Blocks: T2, T3, T4
Status: RESOLVED 2026-11-04 (in-session primary-source research; the
research subagent recapitulated session history and wrote no artifact —
known gotcha, work done directly)

## Answer

Per-repo inventories, then overlaps.

### 1. copier-template-copier-template (meta — owns language-agnostic conditional layers)

| Concern | Stamped artifact | Conditional? | Mechanism |
|---|---|---|---|
| Template authoring | whole-repo scaffolding (copier.yml.tmpl, CONTRIBUTING.md.tmpl, answers_file) | always | jinja render |
| Repo-structure linting | `.alint.yml` + bundle aliases/profile | `include_alint` | jinja render |
| Spec-driven changes | `openspec/` | `include_openspec` | jinja render |
| AGENTS.md base shape | `AGENTS.md.tmpl` | include_openspec OR task_management != none OR include_alint | jinja render |
| Pydantic validation | `models.py` | `include_pydantic_validation` | jinja render |
| Template extensions | `extensions/` | `include_template_extensions` | jinja render |
| License | `LICENSE` | `license` | jinja render |
| Task management | `backlog/` (backlog.md OR backlog-md-py choice) | `task_management != 'none'` | jinja render |
| alint profile/bundles | copier.yml questions (alint_profile, alint_bundle_aliases) | hidden vars | copier answers |

Not stamped today (no artifact in meta_template/): CODING_STANDARDS.md,
.gitignore composition, CHANGELOG.md, renovate.json, prek.toml, mise.toml,
per-language conventions.

### 2. python-project-template (base layer — language concerns only)

| Concern | Stamped artifact | Conditional? | Mechanism |
|---|---|---|---|
| Python harness | `template/mise.toml.jinja` ([tools] python+installer, tasks lock/sync/test/quality/format) | installer/type_checker choices | jinja render |
| pre-commit shape | `template/prek.toml.jinja` | unconditional | jinja render |
| AGENTS.md commands section | `template/AGENTS.md.jinja` (mise run install/lock/sync/test/quality/format) | unconditional | jinja render |
| Packaging | `pyproject.toml.jinja` (installer, type_checker, python_version) | choices | jinja render |
| License/README/CHANGELOG | LICENSE.jinja, README.md.jinja, CHANGELOG.md.jinja | license choice | jinja render |
| Task mgmt config sample | `backlog/config.yml` in repo (not yet in template/ — layering gap) | — | — |

Not stamped: .gitignore, renovate.json, CODING_STANDARDS.md, convention
files (PYTHON.md etc. do not exist).

### 3. agentic-project-template (agentic layer)

| Concern | Stamped artifact | Conditional? | Mechanism |
|---|---|---|---|
| Layer composition engine | stamp.py (TOOL_FRAGMENT_ORDER, RENDERED_SHARED, MANAGED_COMMENT) + merge.py (deep_merge, migrations) | — | CLI post-copier |
| Per-tool wiring | fragments/tools/<tool>/ (mise pin, prek hooks, agents.md bullet, gitignore, wt.toml) | per-tool dirs; backlog-py skipped if include_backlog=false | deterministic merge |
| Layer tasks | fragments/mise-layer.toml (install bootstrap, check gate) | — | TOML merge |
| AGENTS.md managed section | fragments/agents-md-section.md + per-tool agents.md | — | marked-section upsert |
| opencode wiring | template/.opencode/opencode.json.jinja (lsp stanza) | — | RENDERED_SHARED (json) |
| agents.toml | template/agents.toml.jinja | — | RENDERED_SHARED (toml) |
| Backlog wiring | fragments/tools/backlog-py/ (mise pin + backlog-init in install.run) | include_backlog gate | merge + _strip_backlog_wiring |
| Knowledge tier | .lore.md seed (include_lore) | include_lore | copier gate (apt-28) |
| Opt-in skills | consult-llm (include_consult_llm) | default off (tested) | copier answers |
| CODING_STANDARDS.md | repo root, NOT stamped | — | n/a (review-agent convention) |
| git-ai attribution | include_git_ai | opt-in | copier answers |

### Overlaps (the refactor's raw material)

**(a) Delivered by more than one repo**

1. **AGENTS.md** — meta (conditional base shape) + python (commands section)
   + agentic (managed section upsert). Three writers, no declared composition
   contract between meta and python.
2. **backlog/ task management** — meta owns backlog.md vs backlog-md-py
   scaffolding via task_management; agentic layer separately wires backlog-py
   (mise pin + backlog-init) gated by its own include_backlog. Two gates,
   two owners, no wiring contract. (Maintainer: "should be inheriting from
   the python repo" — today the python repo doesn't wire it at all.)
3. **LICENSE** — meta (generic, license choice) + python (LICENSE.jinja with
   MIT/FSL choices). Duplicate, different choice sets.
4. **CONTRIBUTING.md** — meta (CONTRIBUTING.md.tmpl) + python
   (CONTRIBUTING.md at repo root, not in template/). Unclear if stamped.
5. **alint** — meta owns .alint.yml + profile questions; agentic layer pins
   the binary + prek hooks. Concern split across two repos without a
   declared seam.

**(b) Down-stack concerns that plausibly fail the criterion (language-agnostic AND every stamped project wants it)**

- python's `mise run quality/format/test` tasks and prek.toml are
  language-specific but sit in the *base* layer — correct per criterion.
- agentic's .gitignore additions (dotagents artifacts, .roborev/) are
  agentic-owned — correct.
- No clear criterion-violating misplacement found in (b); the real finding
  is in (a) and (c).

**(c) Meta should own but doesn't**

1. **CODING_STANDARDS.md** — exists only in the agentic repo, unstamped.
   Per Q3 decision: meta ships agnostic defaults, bases append language
   sections (PYTHON.md …), layers append judgement calls. Nothing owns this
   today.
2. **CHANGELOG.md** — python has it; meta-template-repo has one for itself;
   meta doesn't stamp one. Fails the "every project wants it" half only for
   non-released projects — candidate for meta with a conditional.
3. **.gitignore composition** — every repo hand-maintains its own; no layer
   owns a composition mechanism (python's template/ has no .gitignore.jinja;
   agentic merges gitignore lines per-tool). Language-agnostic; candidate.
4. **renovate.json** — meta-template-repo uses one for itself; python
   doesn't stamp one. Language-agnostic; candidate (every project wants it
   is the open half).
5. **Per-language convention files (PYTHON.md, JAVASCRIPT.md…)** — do not
   exist anywhere yet; this ticket's finding is the greenfield shape that
   T2 must design.

Key structural fact for T2/T3/T4: the meta and python repos have **no
composition contract** — python doesn't inherit from meta at stamp time
(no documented layering of answers files); the agentic layer composes onto
python's outputs via its merge engine. The refactor's hardest decision is
defining how the three repos' copier.yml answers compose.
