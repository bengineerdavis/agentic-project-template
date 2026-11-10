import os
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
    assert 'repo = "https://github.com/asamarts/alint-pre-commit"' in (
        fresh_stamp / "prek.toml"
    ).read_text()
    assert 'rev = "v0.22.0"' in (fresh_stamp / "prek.toml").read_text()
    assert 'id = "alint"' in (fresh_stamp / "prek.toml").read_text()
    assert 'id = "alint-check"' not in (fresh_stamp / "prek.toml").read_text()
    agents = (fresh_stamp / "agents.toml").read_text()
    assert 'name = "structure-authoring"' in agents
    assert 'name = "aboyeur"' in agents
    assert agents.count('source = "bengineerdavis/ai-prompt-library"') == 4


def test_stamped_project_gets_context_ai_rules(fresh_stamp: Path) -> None:
    assert (fresh_stamp / ".context" / "ai-rules.md").exists()


def test_stamped_project_gets_a_runnable_worktree_guard(fresh_stamp: Path) -> None:
    """APT-32: the guard must arrive executable and wired, or it fails open.

    The hook entry is repo-root-relative, so a missing file or a lost
    executable bit leaves every stamped project's `prek` run unable to
    enforce the isolation rule -- silently, which is the failure mode the
    guard exists to end.
    """
    guard = fresh_stamp / "scripts" / "check-worktree.sh"
    assert guard.exists(), "the guard script must be stamped"
    assert os.access(guard, os.X_OK), "a non-executable hook entry never runs"

    prek = (fresh_stamp / "prek.toml").read_text()
    assert "worktree-guard" in prek, "the hook must be wired, not merely present"
    assert "scripts/check-worktree.sh" in prek, "the entry must name the stamped path"


def test_stamped_project_gets_opencode_surface(fresh_stamp: Path) -> None:
    assert (fresh_stamp / ".opencode" / "opencode.json").exists()
    assert (fresh_stamp / ".opencode" / "agents" / "review-deep.md").exists()


def test_stamped_opencode_json_wires_lsp(fresh_stamp: Path) -> None:
    """apt-10 AC2: the lsp section rides the RENDERED_SHARED merge — a
    stamped project gets the alint server wired into opencode.json."""
    import json

    config = json.loads((fresh_stamp / ".opencode" / "opencode.json").read_text())
    assert config["lsp"]["alint"]["command"] == ["alint", "lsp"]
    assert ".md" in config["lsp"]["alint"]["extensions"]


def test_stamped_mise_pins_python_lsp(fresh_stamp: Path) -> None:
    """apt-10 AC1: the python language server is pinned via the layer
    fragment so opencode's builtin pyright resolves it on PATH."""
    import tomllib

    mise = tomllib.loads((fresh_stamp / "mise.toml").read_text())
    assert mise["tools"]["npm:pyright"] == "1.1.414"


def test_update_merge_keeps_project_lsp_entries(tmp_path: Path) -> None:
    """apt-10 AC2 (update path): a project's own lsp servers survive the
    layer merge — deep_merge is additive, the layer only adds its own."""
    import json

    from agentic_project_template.merge import merge_json_file

    dst = tmp_path / "opencode.json"
    dst.write_text(json.dumps({
        "lsp": {"rust": {"command": ["rust-analyzer"], "extensions": [".rs"]}},
    }, indent=2))
    merge_json_file(dst, {
        "lsp": {"alint": {"command": ["alint", "lsp"], "extensions": [".md"]}},
    })
    merged = json.loads(dst.read_text())
    assert merged["lsp"]["rust"]["command"] == ["rust-analyzer"]
    assert merged["lsp"]["alint"]["command"] == ["alint", "lsp"]


def test_lsp_servers_resolve_through_shims(tmp_path: Path) -> None:
    """apt-10 AC3 smoke: the pinned binaries actually start — pyright
    reports a version, alint lsp speaks LSP over stdio."""
    import json
    import subprocess

    root = Path(__file__).resolve().parents[1]
    pyright = subprocess.run(
        ["mise", "x", "npm:pyright@1.1.414", "--", "pyright", "--version"],
        cwd=root, capture_output=True, text=True, timeout=60,
    )
    assert pyright.returncode == 0, pyright.stderr

    p = subprocess.Popen(
        ["mise", "x", "github:asamarts/alint@0.21.0", "--", "alint", "lsp"],
        cwd=root, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL, text=True,
    )
    try:
        init = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                "params": {"processId": None, "rootUri": f"file://{root}",
                           "capabilities": {}}}
        data = json.dumps(init)
        p.stdin.write(f"Content-Length: {len(data)}\r\n\r\n{data}")
        p.stdin.flush()
        header = p.stdout.readline()
        length = int(header.split(":")[1].strip())
        while p.stdout.readline().strip():
            pass
        result = json.loads(p.stdout.read(length))
        assert "capabilities" in result.get("result", {})
    finally:
        p.terminate()


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
    assert "BEGIN managed: overlay" in agents_md
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
    assert "BEGIN managed: overlay" in agents_md

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
    # APT-32 added a second `local` repo (the worktree guard, from the
    # worktrunk fragment). The merge keys on (repo, hook ids), so the two
    # local repos coexist instead of collapsing. worktrunk is declared
    # before tombi, so the guard's local entry leads — cheapest check
    # first, before any linter runs.
    assert repos[0] == "local", f"declared order puts worktrunk's local first, got {repos}"
    assert "tombi" in repos[1], f"tombi follows worktrunk, got {repos}"
    assert repos[2] == "https://github.com/asamarts/alint-pre-commit"
    assert repos[3] == "local"  # alint instruction refresh follows the check

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
    assert text.count("<!-- BEGIN managed: overlay -->") == 1
    assert text.count("<!-- END managed: overlay -->") == 1
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


LORE_HEADER = (
    "<!-- Managed by lore (https://github.com/BYK/loreai) "
    "— manual edits are imported on next session. -->"
)


def test_lore_on_stamps_seed_and_pointer(fresh_stamp: Path) -> None:
    """include_lore (default on) seeds .lore.md with lore's own managed
    header — nothing else — and points agents at it from ai-rules.
    Lore imports and merges into the file; the layer never curates it.
    """
    seed = fresh_stamp / ".lore.md"
    assert seed.read_text(encoding="utf-8") == LORE_HEADER + "\n"
    ai_rules = (fresh_stamp / ".context" / "ai-rules.md").read_text()
    assert ".lore.md" in ai_rules


def test_help_flag_rule_is_stamped(fresh_stamp: Path) -> None:
    """The --help rule must reach every stamped project.

    Regression driver: two CLIs treat `--help` as an ordinary argument once a
    subcommand is present, so the command runs instead of printing help. The
    probe looks identical to an intentional run, which is what makes it worth
    a rule rather than a convention.
    """
    ai_rules = (fresh_stamp / ".context" / "ai-rules.md").read_text()
    assert "--help" in ai_rules
    assert "broken command" in ai_rules


def test_help_flag_rule_needs_no_optional_flag(tmp_path: Path) -> None:
    """It is unconditional: the hazard is in a third-party CLI, not in any
    opt-in feature of this layer."""
    dst = tmp_path / "minimal"
    dst.mkdir()
    _stamp(dst, include_lore=False)
    ai_rules = (dst / ".context" / "ai-rules.md").read_text()
    assert "--help" in ai_rules


def test_lore_pointer_states_the_file_is_a_derived_render(fresh_stamp: Path) -> None:
    """The pointer must say .lore.md is a render of a database.

    Regression driver: `.lore.md` was hand-merged between checkouts containing
    diverged stores. Content the database never held was discarded on the next
    export, and one worktree had forked into a second project row holding
    entries invisible from the main checkout. 'Treat as read-only' alone does
    not warn against merging it across branches.
    """
    ai_rules = (fresh_stamp / ".context" / "ai-rules.md").read_text()
    assert "render" in ai_rules
    assert "lore data merge" in ai_rules


def test_lore_opt_out_leaves_no_trace(tmp_path: Path) -> None:
    """include_lore=false must stamp a project with no lore trace:
    no seed file, no ai-rules mention (the answers file itself is the
    one legitimate carrier of the flag). Artifact-level, not substring:
    "lore" false-positives on "explore".
    """
    dst = tmp_path / "quiet-project"
    dst.mkdir()
    _stamp(dst, include_lore=False)
    assert not (dst / ".lore.md").exists()
    assert ".lore.md" not in (dst / ".context" / "ai-rules.md").read_text()


def test_lore_opt_out_keeps_lore_out_of_experiments_log(tmp_path: Path) -> None:
    """include_lore=false must not inject vendor-specific evidence.

    Regression driver: the shipped --help entry names one CLI and its command
    surface. That is useful evidence for a project using that tool and noise
    for one that is not, and it leaks a dependency the project opted out of.
    Caught by stamping with the flag off and counting occurrences.
    """
    dst = tmp_path / "quiet-probe"
    dst.mkdir()
    _stamp(dst, include_lore=False)
    exp = dst / "docs" / "experiments.md"
    assert exp.exists()
    assert "lore" not in exp.read_text()


def test_lore_opt_out_update_leaves_seeded_file(tmp_path: Path) -> None:
    """A project stamped with lore, then updated with the flag off:
    .lore.md is accumulated project knowledge, not wiring — it stays
    (copier's update never re-renders on answer changes; probe-verified).
    The ai-rules pointer IS wiring: apply_fragments strips it, like the
    backlog wiring strip.
    """
    dst = tmp_path / "toggled-off"
    dst.mkdir()
    _stamp(dst)
    seed_text = (dst / ".lore.md").read_text(encoding="utf-8")
    (dst / ".agentic-answers.yml").write_text("include_lore: false\n")
    apply_fragments(dst)
    assert (dst / ".lore.md").read_text(encoding="utf-8") == seed_text
    assert ".lore.md" not in (dst / ".context" / "ai-rules.md").read_text()


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
