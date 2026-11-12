import os
import shutil
import subprocess
import tomllib
from pathlib import Path

import pytest

from agentic_project_template.stamp import apply_layer, default_data, render_layer


REVIEWED_SOURCES = ("mattpocock/skills", "bengineerdavis/ai-prompt-library")
EXPECTED_SKILLS = ("tdd", "grilling", "writing-for-agents")


def _dotagents(project: Path, home: Path, scope: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["dotagents", f"--{scope}", *args],
        cwd=project,
        env={
            **os.environ,
            "HOME": str(home),
            "MISE_TRUSTED_CONFIG_PATHS": str(home / "no-config"),
        },
        capture_output=True,
        text=True,
        timeout=180,
    )


def _stamp(destination: Path) -> None:
    destination.mkdir()
    apply_layer(render_layer(destination, default_data(destination), defaults=True), destination)


def test_bootstrap_refreshes_the_shared_workflow_source(tmp_path: Path) -> None:
    project = tmp_path / "stamped"
    _stamp(project)
    manifest = tomllib.loads((project / "agents.toml").read_text())
    assert manifest["plugins"] == [
        {"name": "mattpocock-skills", "source": "mattpocock/skills"}
    ]
    mise = tomllib.loads((project / "mise.toml").read_text())
    refresh = mise["tasks"]["dotagents-add"]["run"]
    assert refresh.index("add mattpocock/skills --all") < refresh.index(
        "--project install"
    )
    assert "mise run dotagents-add" in mise["tasks"]["install"]["run"]


def test_fresh_user_bootstrap_converges_and_projects_skills(tmp_path: Path) -> None:
    """The public refresh must work without an already-trusted global config.

    Catches missing source trust and non-idempotent bootstrap. It does not
    assert that upstream's skill files are valid, or activate another client.
    """
    if shutil.which("dotagents") is None:
        pytest.fail("The real dotagents CLI is required for this bootstrap test.")
    project = tmp_path / "stamped"
    _stamp(project)
    home = tmp_path / "home"
    home.mkdir()
    (project / ".opencode/skills").mkdir(parents=True)
    subprocess.run(["git", "init", "-q"], cwd=project, check=True)
    refresh = tomllib.loads((project / "mise.toml").read_text())["tasks"][
        "dotagents-add"
    ]["run"]

    # Execute the real reviewed remote refresh. No source substitution and no
    # inherited user trust: this proves a fresh collaborator's public path.
    for iteration in range(2):
        for repo in REVIEWED_SOURCES:
            project_config = project / "agents.toml"
            if repo not in project_config.read_text():
                result = _dotagents(project, home, "project", "trust", "add", repo)
                assert result.returncode == 0, result.stdout + result.stderr
            user_config = home / ".agents/agents.toml"
            if not user_config.exists() or repo not in user_config.read_text():
                result = _dotagents(project, home, "user", "trust", "add", repo)
                assert result.returncode == 0, result.stdout + result.stderr
        result = _dotagents(
            project, home, "project", "add", "mattpocock/skills", "--all"
        )
        assert result.returncode == 0, result.stdout + result.stderr
        result = _dotagents(project, home, "project", "install")
        assert result.returncode == 0, result.stdout + result.stderr
        for name in EXPECTED_SKILLS:
            assert (project / ".opencode/skills" / name / "SKILL.md").is_file(), (
                f"Missing {name} on convergence iteration {iteration + 1}: "
                f"{result.stdout}\n{result.stderr}"
            )
