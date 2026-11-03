import tomllib
from pathlib import Path

import pytest

from agentic_project_template.stamp import (
    apply_fragments,
    apply_layer,
    default_data,
    render_layer,
)


def _stamp(destination: Path, **overrides) -> list[str]:
    data = default_data(destination) | overrides
    tmp = render_layer(destination, data, defaults=True)
    return apply_layer(tmp, destination)


@pytest.fixture(scope="module")
def fresh_stamp(tmp_path_factory) -> Path:
    """One default layer stamp shared by behavior tests (read-only)."""
    dst = tmp_path_factory.mktemp("fresh-stamp") / "fresh-project"
    dst.mkdir()
    _stamp(dst)
    return dst


def test_fresh_stamp_emits_no_warnings(tmp_path: Path) -> None:
    dst = tmp_path / "fresh-project"
    dst.mkdir()
    assert _stamp(dst) == []


def test_stamped_project_records_layer_answers(fresh_stamp: Path) -> None:
    assert (fresh_stamp / ".agentic-answers.yml").exists()


def test_stamped_agents_toml_declares_core_skills(fresh_stamp: Path) -> None:
    agents = (fresh_stamp / "agents.toml").read_text()
    assert "commit-hygiene" in agents
    assert "bengineerdavis/ai-prompt-library" in agents


def test_consult_llm_is_opt_in_default_off(fresh_stamp: Path) -> None:
    assert "consult" not in (fresh_stamp / "agents.toml").read_text()


def test_stamped_project_gets_alint_config(fresh_stamp: Path) -> None:
    assert "agent-hygiene" in (fresh_stamp / ".alint.yml").read_text()


def test_stamped_project_gets_context_ai_rules(fresh_stamp: Path) -> None:
    assert (fresh_stamp / ".context" / "ai-rules.md").exists()


def test_stamped_project_gets_opencode_surface(fresh_stamp: Path) -> None:
    assert (fresh_stamp / ".opencode" / "opencode.json").exists()
    assert (fresh_stamp / ".opencode" / "agents" / "review-deep.md").exists()


def test_stamped_project_gets_experiments_doc(fresh_stamp: Path) -> None:
    assert (fresh_stamp / "docs" / "experiments.md").exists()


def test_stamped_mise_carries_fast_and_slow_loop(fresh_stamp: Path) -> None:
    mise = (fresh_stamp / "mise.toml").read_text()
    assert "roborev" in mise and "review-deep" in mise


def test_stamped_mise_task_names_have_no_colons(fresh_stamp: Path) -> None:
    mise = (fresh_stamp / "mise.toml").read_text()
    assert ":" not in mise.split("[tasks.")[1].split("]")[0]  # mise forbids colons


def test_stamped_agents_md_carries_managed_section(fresh_stamp: Path) -> None:
    agents_md = (fresh_stamp / "AGENTS.md").read_text()
    assert "BEGIN managed: agentic-project-template" in agents_md
    assert "mise run review-deep" in agents_md


@pytest.mark.parametrize("doc", ["issue-tracker", "triage-labels", "domain"])
def test_stamped_project_gets_agent_doc(fresh_stamp: Path, doc: str) -> None:
    assert (fresh_stamp / "docs" / "agents" / f"{doc}.md").exists()


def test_stamped_project_gets_backlog_workflow_skill(fresh_stamp: Path) -> None:
    assert (fresh_stamp / ".agents" / "skills" / "backlog-workflow" / "SKILL.md").exists()


def test_stamped_agents_toml_declares_backlog_mcp(fresh_stamp: Path) -> None:
    assert "backlog-py-mcp" in (fresh_stamp / "agents.toml").read_text()


def test_stamped_agents_md_links_backlog_docs(fresh_stamp: Path) -> None:
    agents_md = (fresh_stamp / "AGENTS.md").read_text()
    assert "docs/agents/issue-tracker.md" in agents_md
    assert "backlog-workflow" in agents_md


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


def test_wt_config_stamped_fresh(fresh_stamp: Path) -> None:
    wt = (fresh_stamp / ".config" / "wt.toml").read_text()
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


def test_task_workflow_doc_stamped(fresh_stamp: Path) -> None:
    doc = fresh_stamp / "docs" / "task-workflow.md"
    text = doc.read_text()
    assert "wt switch --create" in text
    assert "wt merge" in text


def test_apply_fragments_merges_without_re_render(tmp_path: Path) -> None:
    """After copier update, only fragments run — choices must survive."""
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


def test_backlog_opt_out_leaves_no_trace(tmp_path: Path) -> None:
    """include_backlog=false must stamp a project with no backlog trace:
    no store wiring, no agent docs, no MCP, no backlog word in anything
    the layer writes (the answers file itself is the one legitimate
    carrier of the flag).
    """
    dst = tmp_path / "quiet-project"
    dst.mkdir()
    _stamp(dst, include_backlog=False)
    offenders = [
        p.relative_to(dst).as_posix()
        for p in sorted(dst.rglob("*"))
        if p.is_file()
        and p.name != ".agentic-answers.yml"
        and "backlog" in p.read_text(encoding="utf-8", errors="replace").lower()
    ]
    assert offenders == []
    assert not (dst / "docs" / "agents").exists()
    assert not (dst / ".agents" / "skills" / "backlog-workflow").exists()


def test_backlog_opt_out_update_removes_stale_wiring(tmp_path: Path) -> None:
    """A project stamped with backlog, then updated with the flag off:
    apply_fragments must strip the stale wiring from the shared files it
    owns (full-section replacement + mise strip) instead of leaving both
    states merged.
    """
    dst = tmp_path / "toggled-off"
    dst.mkdir()
    _stamp(dst)
    (dst / ".agentic-answers.yml").write_text("include_backlog: false\n")
    apply_fragments(dst)
    mise = tomllib.loads((dst / "mise.toml").read_text())
    assert "backlog-init" not in mise.get("tasks", {})
    assert "backlog" not in (dst / "AGENTS.md").read_text().lower()


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
