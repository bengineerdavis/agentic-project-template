import tomllib
from pathlib import Path

from agentic_project_template.stamp import apply_layer, default_data, render_layer


def _stamp(destination: Path, **overrides) -> list[str]:
    data = default_data(destination) | overrides
    tmp = render_layer(destination, data, defaults=True)
    return apply_layer(tmp, destination)


def test_layer_stamp_fresh(tmp_path: Path) -> None:
    dst = tmp_path / "fresh-project"
    dst.mkdir()
    warnings = _stamp(dst)
    assert warnings == []

    assert (dst / ".agentic-answers.yml").exists()
    agents = (dst / "agents.toml").read_text()
    assert "commit-hygiene" in agents and "bengineerdavis/ai-prompt-library" in agents
    assert "consult" not in agents  # opt-in default off
    assert (dst / ".alint.yml").exists()
    assert "agent-hygiene" in (dst / ".alint.yml").read_text()
    assert (dst / ".context" / "ai-rules.md").exists()
    assert (dst / ".opencode" / "opencode.json").exists()
    assert (dst / ".opencode" / "agents" / "review-deep.md").exists()
    assert (dst / "docs" / "experiments.md").exists()

    mise = (dst / "mise.toml").read_text()
    assert "roborev" in mise and "review-deep" in mise
    assert ":" not in mise.split("[tasks.")[1].split("]")[0]  # mise forbids colons

    agents_md = (dst / "AGENTS.md").read_text()
    assert "BEGIN managed: agentic-project-template" in agents_md
    assert "mise run review-deep" in agents_md


def test_layer_stamp_existing_project_preserves_base(tmp_path: Path) -> None:
    dst = tmp_path / "existing"
    dst.mkdir()
    (dst / "mise.toml").write_text(
        '[tools]\npython = "3.13"\n\n[tasks.build]\nrun = "make"\n'
    )
    (dst / ".gitignore").write_text("node_modules/\n")
    (dst / "AGENTS.md").write_text("# Existing\n\nOriginal router content.\n")
    (dst / ".pre-commit-config.yaml").write_text(
        "repos:\n"
        "  - repo: https://github.com/astral-sh/ruff-pre-commit\n"
        "    rev: v0.15.21\n"
        "    hooks:\n"
        "      - id: ruff-check\n"
    )
    warnings = _stamp(dst)

    mise = (dst / "mise.toml").read_text()
    assert 'python = "3.13"' in mise and "roborev" in mise and "make" in mise
    assert "node_modules/" in (dst / ".gitignore").read_text()
    assert ".roborev/" in (dst / ".gitignore").read_text()

    agents_md = (dst / "AGENTS.md").read_text()
    assert "Original router content." in agents_md
    assert "BEGIN managed: agentic-project-template" in agents_md

    prek_text = (dst / ".pre-commit-config.yaml").read_text()
    assert "ruff-check" in prek_text and "tombi-format" in prek_text
    assert not (dst / "prek.toml").exists()

    assert not [w for w in warnings if "mise.toml" in w]


def test_apply_fragments_migrates_legacy_registry_pin(tmp_path: Path) -> None:
    """A project stamped before the http-backend bump carries the layer's
    old bare `opencode` pin. apply_fragments (the update path) must remove
    it — coexisting with `http:opencode` makes mise resolve the stale
    registry binary first, so the apt-21 failure would persist there.
    """
    from agentic_project_template.stamp import apply_fragments

    dst = tmp_path / "pre-bump-stamp"
    dst.mkdir()
    (dst / "mise.toml").write_text(
        '[tools]\npython = "3.13"\nopencode = "1.18.32"\n'
    )
    apply_fragments(dst)
    tools = tomllib.loads((dst / "mise.toml").read_text())["tools"]
    assert "opencode" not in tools
    assert "http:opencode" in tools
    assert tools["python"] == "3.13"


def test_per_tool_fragments_are_declared() -> None:
    """apt-22 AC3: the merge order is declared once in the CLI (single
    source), and it covers every fragment directory on disk — a new
    fragments/tools/<tool>/ dir fails the suite until the engine declares
    it, so no tool contribution can silently join the merge unsorted.
    """
    from agentic_project_template.stamp import TOOL_FRAGMENT_ORDER, repo_root

    tools_dir = repo_root() / "fragments" / "tools"
    on_disk = {p.name for p in tools_dir.iterdir() if p.is_dir()}
    assert len(TOOL_FRAGMENT_ORDER) == len(set(TOOL_FRAGMENT_ORDER)), (
        "a tool appears twice in the declared merge order"
    )
    assert on_disk == set(TOOL_FRAGMENT_ORDER), (
        f"fragment dirs and the declared order disagree: "
        f"on-disk={sorted(on_disk)} declared={list(TOOL_FRAGMENT_ORDER)}"
    )


def test_grab_bag_fragments_are_drained() -> None:
    """apt-22 AC1: every tool contribution moved to fragments/tools/<tool>/;
    the top-level fragments carry only layer-composition content."""
    import tomllib

    from agentic_project_template.stamp import repo_root

    fragments = repo_root() / "fragments"
    assert not (fragments / "prek-layer.toml").exists()
    assert not (fragments / "gitignore-layer.txt").exists()
    assert not (fragments / "wt-layer.toml").exists()
    assert (fragments / "tools" / "worktrunk" / "wt.toml").exists()
    mise_layer = tomllib.loads((fragments / "mise-layer.toml").read_text())
    assert "tools" not in mise_layer, "tool pins must live per tool"
    assert set(mise_layer.get("tasks", {})) == {"install", "check"}, (
        "mise-layer.toml carries only the layer-composition tasks "
        "(bootstrap install + the check gate)"
    )


def test_stamp_merges_fragments_in_declared_order(tmp_path: Path) -> None:
    """apt-22 AC2: the CLI merge applies per-tool fragments in one declared,
    tested order — prek [[repos]] hook order and AGENTS.md bullet order both
    follow it."""
    dst = tmp_path / "ordered"
    dst.mkdir()
    _stamp(dst)

    prek = tomllib.loads((dst / "prek.toml").read_text())["repos"]
    repos = [entry["repo"] for entry in prek]
    assert "tombi" in repos[0], f"declared order puts tombi first, got {repos}"
    assert repos[1] == "local"  # alint-check follows tombi

    agents_md = (dst / "AGENTS.md").read_text()
    positions = {
        bullet: agents_md.index(bullet)
        for bullet in (
            "- **Experiments:**",
            "- **Fast loop:**",
            "- **Slow loop:**",
            "- **Agent dependencies:**",
            "- **Isolation:**",
            "- **Tasks:**",
        )
    }
    ordered = sorted(positions, key=positions.get)
    assert ordered == [
        "- **Experiments:**",  # layer-owned bullet leads the section
        "- **Fast loop:**",
        "- **Slow loop:**",
        "- **Agent dependencies:**",
        "- **Isolation:**",
        "- **Tasks:**",
    ], f"AGENTS.md bullets do not follow the declared order: {ordered}"


def test_layer_stamp_skips_unmanaged_context(tmp_path: Path) -> None:
    dst = tmp_path / "sandbox-consumer"
    (dst / ".context").mkdir(parents=True)
    original = "# My hand-written rules\n"
    (dst / ".context" / "ai-rules.md").write_text(original)
    dst.mkdir(exist_ok=True)
    warnings = _stamp(dst)
    assert (dst / ".context" / "ai-rules.md").read_text() == original
    assert any("ai-rules.md" in w for w in warnings)


def test_agents_md_section_no_marker_growth(tmp_path: Path) -> None:
    """The real fragment must produce exactly one marker pair, ever.

    Regression: the fragment used to carry its own BEGIN/END markers while
    upsert_marked_section added a second pair, and the non-greedy regex left
    the outer END unmatched — every update appended an orphan END line.
    """
    from agentic_project_template.merge import upsert_marked_section

    fragment = Path(__file__).parents[1] / "fragments" / "agents-md-section.md"
    section = fragment.read_text(encoding="utf-8")
    assert "<!-- BEGIN managed" not in section
    target = tmp_path / "AGENTS.md"
    target.write_text("# Existing\n")
    upsert_marked_section(target, section)
    upsert_marked_section(target, section)
    upsert_marked_section(target, section)
    text = target.read_text()
    assert text.count("<!-- BEGIN managed: agentic-project-template -->") == 1
    assert text.count("<!-- END managed: agentic-project-template -->") == 1
    assert "# Existing" in text


def test_wt_config_stamped_fresh(tmp_path: Path) -> None:
    dst = tmp_path / "with-wt"
    dst.mkdir()
    _stamp(dst)
    wt = (dst / ".config" / "wt.toml").read_text()
    assert "mise trust && mise run install" in wt
    assert "mise run check" in wt


def test_wt_config_merge_never_clobbers(tmp_path: Path) -> None:
    dst = tmp_path / "has-wt"
    (dst / ".config").mkdir(parents=True)
    (dst / ".config" / "wt.toml").write_text(
        'post-start = "npm run dev"\n\n[aliases]\ndeploy = "make deploy"\n'
    )
    warnings = _stamp(dst)
    wt = (dst / ".config" / "wt.toml").read_text()
    assert 'post-start = "npm run dev"' in wt  # base wins
    assert '[aliases]' in wt and 'deploy = "make deploy"' in wt
    assert 'pre-merge = "mise run check"' in wt  # layer fills the gap
    assert any("post-start" in w for w in warnings)


def test_task_workflow_doc_stamped(tmp_path: Path) -> None:
    dst = tmp_path / "with-workflow"
    dst.mkdir()
    _stamp(dst)
    doc = dst / "docs" / "task-workflow.md"
    text = doc.read_text()
    assert "wt switch --create" in text
    assert "wt merge" in text


def test_apply_fragments_merges_without_re_render(tmp_path: Path) -> None:
    """After copier update, only fragments run — choices must survive."""
    from agentic_project_template.stamp import apply_fragments

    dst = tmp_path / "post-update"
    dst.mkdir()
    (dst / "mise.toml").write_text('[tools]\npython = "3.13"\n')
    answers = dst / ".agentic-answers.yml"
    answers.write_text("include_git_ai: true\n")
    apply_fragments(dst)
    assert 'python = "3.13"' in (dst / "mise.toml").read_text()
    assert "roborev" in (dst / "mise.toml").read_text()
    assert answers.read_text() == "include_git_ai: true\n"
    assert "BEGIN managed" in (dst / "AGENTS.md").read_text()


def test_opt_in_flags_render(tmp_path: Path) -> None:
    dst = tmp_path / "opted"
    dst.mkdir()
    _stamp(
        dst,
        include_consult_llm=True,
        include_git_ai=True,
        mcp_servers=[{"name": "context7", "source": "upstash/context7"}],
    )
    agents = (dst / "agents.toml").read_text()
    assert "raine/consult-llm" in agents
    assert "[[mcp]]" in agents and "context7" in agents
    assert (dst / ".consult-llm.yaml").exists() is False  # consult config is a follow-up task


def test_tools_values_are_versions_not_backend_specs(tmp_path: Path) -> None:
    """A backend prefix in a tool VALUE is TOML-valid but mise-fatal: mise
    reads the value as a version and dies resolving it before any task runs
    (dotagents = "npm:@sentry/dotagents" broke every stamped project).
    Backend prefixes belong in tool keys, not values. Table-shaped entries
    are the exception: the http backend's platforms/urls carry colons by
    design — guard only their embedded `version` field.
    """
    dst = tmp_path / "fresh-project"
    dst.mkdir()
    _stamp(dst)
    tools = tomllib.loads((dst / "mise.toml").read_text())["tools"]
    for key, value in tools.items():
        if isinstance(value, dict):
            assert isinstance(value.get("version"), str) and ":" not in value["version"], (
                f"tools[{key!r}] table entry: `version` must be a bare "
                "version string (backend prefixes in the version break mise)"
            )
            # with fixed http URLs the version is only a label: a bump that
            # updates `version` but misses a url silently installs the OLD
            # artifact under the NEW label (checksum still matches)
            for platform, spec in (value.get("platforms") or {}).items():
                url = spec.get("url", "") if isinstance(spec, dict) else ""
                assert value["version"] in url, (
                    f"tools[{key!r}].platforms.{platform}: url does not carry "
                    f"version {value['version']!r} — bump urls and checksums "
                    "together with the version"
                )
            continue
        assert ":" not in str(value), (
            f"tools[{key!r}] = {value!r} carries a colon: mise resolves the "
            "value as a version and fails — put the backend prefix in the "
            'key (e.g. "github:org/repo") instead'
        )
