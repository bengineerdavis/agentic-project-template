import os
import shutil
import subprocess
import tomllib
from pathlib import Path

import pytest

from agentic_project_template.stamp import apply_layer, default_data, render_layer


REVIEWED_SOURCES = (
    "mattpocock/skills",
    "UditAkhourii/adhd",
    "bengineerdavis/ai-prompt-library",
)
EXPECTED_SKILLS = ("tdd", "grilling", "writing-for-agents", "adhd")


def _dotagents(
    project: Path, home: Path, scope: str, *args: str
) -> subprocess.CompletedProcess:
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
    apply_layer(
        render_layer(destination, default_data(destination), defaults=True), destination
    )


def test_bootstrap_refreshes_the_shared_workflow_source(tmp_path: Path) -> None:
    project = tmp_path / "stamped"
    _stamp(project)
    manifest = tomllib.loads((project / "agents.toml").read_text())
    assert manifest["plugins"] == [
        {"name": "mattpocock-skills", "source": "mattpocock/skills"},
        {"name": "adhd", "source": "UditAkhourii/adhd"},
    ]
    mise = tomllib.loads((project / "mise.toml").read_text())
    refresh = mise["tasks"]["dotagents-add"]["run"]
    for source in REVIEWED_SOURCES:
        assert source in refresh
    assert refresh.index("add mattpocock/skills --all") < refresh.index(
        "--project install"
    )
    assert refresh.index("add UditAkhourii/adhd --all") < refresh.index(
        "--project install"
    )
    assert "mise run dotagents-add" in mise["tasks"]["install"]["run"]
    instructions = (project / "AGENTS.md").read_text()
    assert "Invoke `/adhd` explicitly for open-ended design" in instructions
    assert "does not auto-trigger" in instructions


def test_failed_catalog_refresh_restores_existing_manifest(tmp_path: Path) -> None:
    """A new catalog failure must not remove unrelated declared dependencies."""
    project = tmp_path / "stamped"
    _stamp(project)
    manifest = project / "agents.toml"
    manifest.write_text(
        'version = 1\nagents = ["opencode"]\n\n[[plugins]]\n'
        'name = "mattpocock-skills"\nsource = "mattpocock/skills"\n'
    )
    before = manifest.read_bytes()
    refresh = tomllib.loads((project / "mise.toml").read_text())["tasks"][
        "dotagents-add"
    ]["run"]
    script = project / "refresh.sh"
    script.write_text("#!/usr/bin/env bash\nset -euo pipefail\n" + refresh)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "calls"
    fake = bin_dir / "dotagents"
    fake.write_text(
        "#!/usr/bin/env bash\n"
        f"printf '%s\\n' \"$*\" >> {calls}\n"
        "if [[ \"$*\" == *'trust add'* ]]; then exit 0; fi\n"
        "if [[ \"$*\" == *'add mattpocock/skills'* ]]; then\n"
        "  printf 'version = 1\\nagents = [\\\"opencode\\\"]\\n' > agents.toml\n"
        "  exit 0\n"
        "fi\n"
        "exit 1\n"
    )
    fake.chmod(0o755)
    result = subprocess.run(
        ["bash", str(script)],
        cwd=project,
        env={**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert manifest.read_bytes() == before
    assert "restored the existing agents.toml" in result.stderr


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
        for source in ("mattpocock/skills", "UditAkhourii/adhd"):
            result = _dotagents(project, home, "project", "add", source, "--all")
            assert result.returncode == 0, result.stdout + result.stderr
        result = _dotagents(project, home, "project", "install")
        assert result.returncode == 0, result.stdout + result.stderr
        for name in EXPECTED_SKILLS:
            assert (project / ".opencode/skills" / name / "SKILL.md").is_file(), (
                f"Missing {name} on convergence iteration {iteration + 1}: "
                f"{result.stdout}\n{result.stderr}"
            )
