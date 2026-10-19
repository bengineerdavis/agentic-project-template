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
    Backend prefixes belong in tool keys, not values.
    """
    dst = tmp_path / "fresh-project"
    dst.mkdir()
    _stamp(dst)
    tools = tomllib.loads((dst / "mise.toml").read_text())["tools"]
    for key, value in tools.items():
        assert ":" not in str(value), (
            f"tools[{key!r}] = {value!r} carries a colon: mise resolves the "
            "value as a version and fails — put the backend prefix in the "
            'key (e.g. "github:org/repo") instead'
        )
