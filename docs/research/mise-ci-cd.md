# Mise in CI/CD (APT-36 research)

Primary sources read Nov 8 2026: mise.jdx.dev/continuous-integration,
mise.jdx.dev/dev-tools/mise-lock, jdx/mise-action action.yml (v5, node24),
and this repo's `.github/workflows/ci.yml` (read from origin/main at 78fa24b;
local main is diverged and lacks it).

## Current state (ci.yml on origin/main)

- mise via curl installer, `MISE_VERSION=2026.10.5` pinned
- steps: checkout (fetch-depth: 0) → setup-uv@v5 → curl mise → `mise run
  install` / `test` / `test-template`
- constraint (apt-29): no third-party actions beyond checkout + setup-uv
- no `mise.lock` in the repo; `mise.toml` pins `uv = "latest"`, `python = "3.12"`

## What the docs recommend (cited)

1. **Official integration is `jdx/mise-action@v5`** (mise.jdx.dev/continuous-
   integration §GitHub Actions). Maintained by mise's own author, runs on
   node24, installs mise + `mise install` (auto-adds `--locked` when
   `mise.lock` exists), caches tools, adds shims to PATH, exports env.
   Adopting it would relax the apt-29 constraint — maintainer decision.
2. **Lockfile is the reproducibility lever** (mise-lock page): commit
   `mise.lock` (generate with `mise lock --platform linux-x64`) and install
   with `mise install --locked`. `--locked` fails if a tool has no lock entry
   instead of resolving. Also skips per-runner version lookups. Lockfiles
   verify DOWNLOADS (checksums), not restored installs.
3. **Caching: trust boundary matters** (§Cache downloads, not installs):
   restored *installs* are trusted as-is (mise never validates installed
   trees against the lock). Safer pattern = cache `~/.cache/mise/downloads-cas`
   (Linux) keyed on lockfile hash; mise hash-checks restored downloads.
   Restore costs: installs re-unpack; source-compiled tools recompile.
4. **Trust is automatic in CI** (§Trust and untrusted branches): mise detects
   CI and trusts checked-out config without prompting (unless paranoid mode).
   No `mise trust` step needed in the workflow — corrects an earlier plan
   note. `MISE_SAFE=1` exists for jobs that read untrusted branches (bots
   resolving versions from PRs); not applicable to our trusted self-CI.
5. **Version lists cost**: without a lockfile, every fresh runner fetches
   version lists per tool (1h stale window). `uv = "latest"` pays this cost
   every run; a lockfile eliminates it.

## Recommendation for this repo

Ranked (incumbent first — installer approach is the baseline to beat):

**(a) Keep the curl installer, add lockfile + downloads-cache + lint step
(recommended).** Preserves the apt-29 constraint untouched. Concretely:
`mise lock --platform linux-x64` + commit `mise.lock`; swap `uv = "latest"`
for a locked pin during the lock; add `actions/cache` on
`~/.cache/mise/downloads-cas` keyed on `hashFiles('mise.lock')`; add
`mise run lint` step (retro finding #2 — CI tests but never lints). Stays
within ~45 lines.

**(b) Adopt jdx/mise-action@v5.** Fewer hand-rolled steps, node24 (kills the
Node 20 deprecation warnings from checkout@v4/setup-uv@v5), free tool
caching. Cost: relaxes the "checkout + setup-uv only" constraint to admit a
first-party action — the constraint's spirit ("minimal third-party surface")
would need restating, e.g. "actions maintained by the tool's own authors".

Rejected: curl installer with no lockfile (status quo pays version-lookup
latency on every run); caching installs (trust boundary the docs warn
against).

## Sequencing note

Implementation is blocked by the local/origin main divergence (ci.yml exists
only on origin/main; local HEAD has no .github/). Research and this artifact
land regardless; the ci.yml edits wait for reconciliation.

## Open questions for the maintainer

1. Relax apt-29's constraint for a first-party action (mise-action)? (b
   above) — or hold the line (a)?
2. Lock `uv = "latest"` at lock time — acceptable freeze cadence
   (`mise lock --bump` on a schedule, PRs when the lock changes)?
