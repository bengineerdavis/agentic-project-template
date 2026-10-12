from agentic_project_template.merge import (
    append_gitignore_lines,
    deep_merge,
    load_toml,
    merge_json_file,
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
