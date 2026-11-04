from agentic_project_template.merge import (
    append_gitignore_lines,
    deep_merge,
    load_toml,
    merge_json_file,
    merge_mise_fragment,
    merge_prek_config,
    merge_toml_file,
    upsert_marked_section,
)


def test_deep_merge_fills_gaps_and_keeps_base() -> None:
    base = {"tools": {"python": "3.13", "uv": "latest"}, "tasks": {}}
    overlay = {"tools": {"roborev": "latest", "python": "3.12"}}
    merged, warnings = deep_merge(base, overlay)
    assert merged["tools"]["python"] == "3.13"
    assert merged["tools"]["uv"] == "latest"
    assert merged["tools"]["roborev"] == "latest"
    assert any("python" in w for w in warnings)


def test_deep_merge_named_lists_by_name() -> None:
    base = {"skills": [{"name": "a", "source": "x/a"}]}
    overlay = {
        "skills": [{"name": "a", "source": "OTHER"}, {"name": "b", "source": "x/b"}]
    }
    merged, _ = deep_merge(base, overlay)
    assert {s["name"] for s in merged["skills"]} == {"a", "b"}
    assert merged["skills"][0]["source"] == "x/a"


def test_merge_toml_file_is_idempotent(tmp_path) -> None:
    target = tmp_path / "mise.toml"
    target.write_text('[tools]\npython = "3.13"\n')
    overlay = {"tools": {"roborev": "latest"}, "tasks": {"review-deep": {"run": "x"}}}
    first = merge_toml_file(target, overlay)
    snapshot = load_toml(target)
    second = merge_toml_file(target, overlay)
    assert load_toml(target) == snapshot
    assert not second
    assert not [w for w in first if "python" in w]


def test_merge_mise_fragment_migrates_legacy_registry_pin(tmp_path) -> None:
    """The layer moved its opencode pin from the bare registry key to the
    http-backend key. deep_merge never removes keys, so a pre-bump stamp
    would keep `opencode = "1.18.32"` next to the new `http:opencode`
    table — mise treats them as separate backend instances and shim
    dispatch resolves the first provider, i.e. the stale V1 binary wins
    (verified 2026-10-20). The bare key was written by an earlier layer
    stamp, not chosen by the project, so the merge migrates layer-owned
    state instead of preserving it.
    """
    target = tmp_path / "mise.toml"
    target.write_text('[tools]\npython = "3.13"\nopencode = "1.18.32"\n')
    overlay = {
        "tools": {
            "http:opencode": {"version": "2.0.32"},
            "worktrunk": "0.80.0",
        },
    }
    warnings = merge_mise_fragment(target, overlay)
    doc = load_toml(target)
    assert "opencode" not in doc["tools"]  # stale registry pin gone
    assert doc["tools"]["python"] == "3.13"  # project pins untouched
    assert doc["tools"]["http:opencode"]["version"] == "2.0.32"
    assert any("opencode" in w for w in warnings)

    # idempotent: second run is a no-op
    assert not merge_mise_fragment(target, overlay)
    assert load_toml(target) == doc


def test_merge_mise_fragment_keeps_bare_key_without_backend_move(tmp_path) -> None:
    """If the layer no longer ships an http-form pin, the merge must not
    invent a migration: a bare key with no backend replacement stays."""
    target = tmp_path / "mise.toml"
    target.write_text('[tools]\nopencode = "1.18.32"\n')
    overlay = {"tools": {"prek": "0.5.2"}}
    warnings = merge_mise_fragment(target, overlay)
    assert load_toml(target)["tools"]["opencode"] == "1.18.32"
    assert not warnings


def test_merge_mise_fragment_migrates_stale_layer_install_script(tmp_path) -> None:
    """A pre-bump stamp keeps the layer's earlier install.run verbatim
    (base wins on the tasks.install.run conflict, warning only). The old
    script installs `opencode` as a bare registry pin — the V1 line apt-21
    blocked — and misses tools the current layer installs. Like the
    registry-pin migration, the script was authored by an earlier layer
    stamp, not chosen by the project: an exact match against a known
    layer-authored variant migrates to the current fragment's script;
    anything else stays untouched (base wins for hand-tuned content).
    """
    legacy_script = (
        '#!/usr/bin/env bash\nset -euo pipefail\n'
        ': "${TMPDIR:=/tmp}"\n'
        'if [ -d "$TMPDIR/fslock" ] && [ ! -w "$TMPDIR/fslock" ]; then\n'
        '  echo "ERROR: $TMPDIR/fslock is not writable by $(whoami) — aube (mise npm backend) will fail to lock." >&2\n'
        '  echo "  fix: sudo chown -R \\"$(id -un):$(id -gn)\\" \\"$TMPDIR/fslock\\"   # or: export TMPDIR=<user-owned dir>" >&2\n'
        '  exit 1\n'
        'fi\n'
        'mise install prek tombi opencode\n'
        'mise install "npm:@sentry/dotagents"\n'
        'dotagents --project install\n'
        'prek install --force\n'
        'if ! mise install "github:kenn-io/roborev"; then\n'
        '  echo "warn: roborev install failed (backend unverified)" >&2\n'
        'fi\n'
        'if ! roborev init; then\n'
        '  echo "warn: roborev init failed (no git repo yet, or daemon unavailable)" >&2\n'
        'fi\n'
        'mise run backlog-init\n'
    )
    current_script = (
        '#!/usr/bin/env bash\nset -euo pipefail\n'
        'mise install prek tombi "http:opencode" "github:asamarts/alint"\n'
    )
    target = tmp_path / "mise.toml"
    target.write_text(
        f'[tasks.install]\nrun = {tomli_w_dumps(legacy_script)}\n'
    )
    overlay = {"tasks": {"install": {"run": current_script}}}
    warnings = merge_mise_fragment(target, overlay)
    merged = load_toml(target)
    assert merged["tasks"]["install"]["run"] == current_script
    assert any("install" in w for w in warnings)

    # hand-tuned variant: never touched
    target.write_text(
        f'[tasks.install]\nrun = {tomli_w_dumps("make install")}\n'
    )
    warnings = merge_mise_fragment(target, overlay)
    assert load_toml(target)["tasks"]["install"]["run"] == "make install"
    assert not [w for w in warnings if "replaced layer-authored" in w]

    # already-current script: no warning, no churn (idempotent)
    target.write_text(f'[tasks.install]\nrun = {tomli_w_dumps(current_script)}\n')
    assert not merge_mise_fragment(target, overlay)


def tomli_w_dumps(value: str) -> str:
    import tomli_w

    return tomli_w.dumps({"v": value})[len("v = ") :].strip()


def _fragment_task_scripts_at(sha: str, root: Path) -> dict[str, str]:
    """Every tasks.<name>.run the layer's mise fragments carried at `sha`."""
    import subprocess
    import tomllib

    listing = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", sha, "fragments"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    scripts: dict[str, str] = {}
    for path in listing.stdout.splitlines():
        # mise-layer.toml (pre-reorg history) and tools/<tool>/mise.toml
        # (post-reorg) both carry task scripts
        if not path.endswith(("mise.toml", "mise-layer.toml")):
            continue
        blob = subprocess.run(
            ["git", "show", f"{sha}:{path}"],
            cwd=root,
            capture_output=True,
            check=True,
        ).stdout
        doc = tomllib.loads(blob.decode("utf-8"))
        for name, task in doc.get("tasks", {}).items():
            run = task.get("run") if isinstance(task, dict) else None
            if isinstance(run, str):
                scripts[name] = run
    return scripts


def test_layer_authored_script_table_covers_fragment_history() -> None:
    """Tripwire for the exact-match script migration: when a fragment task
    script changes, the outgoing layer-authored script must join
    _LAYER_AUTHORED_SCRIPTS — otherwise stamped projects keep the stale
    script forever (deep_merge base-wins). Walks the fragments' git history
    and asserts every script the layer ever shipped is either still current
    or registered in the migration table. Repo-only: needs git history.
    """
    import subprocess

    import pytest

    from agentic_project_template.merge import _LAYER_AUTHORED_SCRIPTS
    from agentic_project_template.stamp import repo_root

    root = repo_root()
    try:
        shas = subprocess.run(
            ["git", "rev-list", "HEAD", "--", "fragments"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("git history unavailable (not a repo checkout)")

    import tomllib

    historical: set[str] = set()
    for sha in shas:
        historical.update(_fragment_task_scripts_at(sha, root).values())

    current: set[str] = set()
    fragments = root / "fragments"
    for fragment in [fragments / "mise-layer.toml", *fragments.glob("tools/*/mise.toml")]:
        doc = tomllib.loads(fragment.read_text(encoding="utf-8"))
        for task in doc.get("tasks", {}).values():
            run = task.get("run") if isinstance(task, dict) else None
            if isinstance(run, str):
                current.add(run)

    # vacuity guard: the walker must have seen real history — a shallow
    # clone (fetch-depth 1) sees only HEAD's fragments, where the count of
    # distinct scripts alone already exceeds 7. The tripwire's substance is
    # the STALE set: history must contain at least one script that is no
    # longer current (today: the six registered variants).
    assert len(historical) >= 7, f"history walk suspiciously small: {len(historical)}"
    assert historical - current, (
        "history walk saw no stale scripts — shallow checkout? The tripwire "
        "is vacuous without pre-current history to check the table against."
    )

    unknown = {
        s for s in historical if s not in current and s not in _LAYER_AUTHORED_SCRIPTS
    }
    assert not unknown, (
        "fragment task scripts changed without joining the migration table — "
        "stamped projects would keep the stale script forever (base wins). "
        f"Append these to _LAYER_AUTHORED_SCRIPTS: {sorted(unknown)!r}"
    )


def test_deep_merge_allows_toml_types() -> None:
    merged, _ = deep_merge({"a": 1}, {"b": [1, 2], "c": {"d": True}})
    assert merged["a"] == 1 and merged["b"] == [1, 2] and merged["c"]["d"] is True


def test_merge_prek_native(tmp_path) -> None:
    native = tmp_path / "prek.toml"
    native.write_text('default_stages = ["pre-commit"]\n')
    entries = [
        {"repo": "builtin", "hooks": [{"id": "end-of-file-fixer"}]},
        {"repo": "local", "hooks": [{"id": "alint-check"}]},
    ]
    path, warnings = merge_prek_config(tmp_path, entries)
    assert path == native
    doc = load_toml(native)
    assert doc["default_stages"] == ["pre-commit"]
    assert doc["repos"][0]["hooks"][0]["id"] == "end-of-file-fixer"
    # idempotent
    path2, _ = merge_prek_config(tmp_path, entries)
    assert path2 == native
    assert len(load_toml(native)["repos"]) == 2


def test_merge_prek_native_dedupes_same_repo_different_rev(tmp_path) -> None:
    native = tmp_path / "prek.toml"
    native.write_text(
        '[[repos]]\n'
        'repo = "https://github.com/tombi-toml/tombi-pre-commit"\n'
        'rev = "v1.1.0"\n'
        'hooks = [\n'
        '  { id = "tombi-lint", args = ["--offline"] },\n'
        '  { id = "tombi-format", args = ["--offline"] },\n'
        ']\n'
    )
    fragment_entry = {
        "repo": "https://github.com/tombi-toml/tombi-pre-commit",
        "rev": "v1.2.0",
        "hooks": [
            {"id": "tombi-lint", "args": ["--offline"]},
            {"id": "tombi-format", "args": ["--offline"]},
        ],
    }
    path, warnings = merge_prek_config(tmp_path, [fragment_entry])
    assert path == native
    tombi_entries = [
        repo
        for repo in load_toml(native)["repos"]
        if "tombi" in repo["repo"]
    ]
    assert len(tombi_entries) == 1
    assert tombi_entries[0]["rev"] == "v1.1.0"
    assert any("already present" in w for w in warnings)


def test_merge_prek_legacy_yaml_gets_appended(tmp_path) -> None:
    legacy = tmp_path / ".pre-commit-config.yaml"
    legacy.write_text(
        "repos:\n"
        "  - repo: https://github.com/astral-sh/ruff-pre-commit\n"
        "    rev: v0.15.21\n"
        "    hooks:\n"
        "      - id: ruff-check\n"
    )
    entries = [{"repo": "local", "hooks": [{"id": "alint-check"}]}]
    path, warnings = merge_prek_config(tmp_path, entries)
    assert path == legacy
    text = legacy.read_text()
    assert "ruff-check" in text and "alint-check" in text
    assert any("prek reads prek.toml" in w for w in warnings)


def test_gitignore_append_is_idempotent(tmp_path) -> None:
    target = tmp_path / ".gitignore"
    target.write_text("node_modules/\n")
    lines = ["node_modules/", ".roborev/", "mise.local.toml"]
    append_gitignore_lines(target, lines)
    once = target.read_text()
    append_gitignore_lines(target, lines)
    assert target.read_text() == once
    assert "node_modules/" in once and ".roborev/" in once


def test_marked_section_replaces_and_preserves_surroundings(tmp_path) -> None:
    target = tmp_path / "AGENTS.md"
    target.write_text("# Existing\n\nBody text.\n")
    upsert_marked_section(target, "## Agentic layer\n\nv1")
    text = target.read_text()
    assert "# Existing" in text and "v1" in text
    upsert_marked_section(target, "## Agentic layer\n\nv2")
    text = target.read_text()
    assert "v2" in text and "v1" not in text
    assert "# Existing" in text and "Body text." in text
    assert target.read_text().count("BEGIN managed") == 1


def test_merge_json_unions_instructions(tmp_path) -> None:
    target = tmp_path / "opencode.json"
    target.write_text('{"instructions": [".context/old.md"], "mode": "build"}\n')
    merge_json_file(target, {"instructions": [".context/ai-rules.md"]})
    import json

    doc = json.loads(target.read_text())
    assert doc["mode"] == "build"
    assert set(doc["instructions"]) == {".context/old.md", ".context/ai-rules.md"}
