"""apt-29: the CI workflow runs the merge-logic tests and the stamp matrix.

The workflow is config, so the tests pin its shape — the things a silent
edit could regress: triggers, the two verification stages, and that the
stamp matrix runs with a scratch root inside the runner workspace (never
/tmp, per apt-18/19).
"""

import tomllib
from pathlib import Path

import yaml

WORKFLOW = Path(".github/workflows/ci.yml")


def _workflow() -> dict:
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def test_ci_workflow_triggers_on_push_to_main_and_pr() -> None:
    triggers = _workflow()[True]  # PyYAML parses bare `on:` as boolean True
    assert set(triggers) == {"push", "pull_request"}
    assert triggers["push"]["branches"] == ["main"]


def test_ci_checks_out_full_history() -> None:
    """The fragment-history tripwire's vacuity guard fails shallow clones
    by design — CI must hand the suite a full checkout."""
    step = next(
        s for s in _workflow()["jobs"]["ci"]["steps"]
        if s.get("uses", "").startswith("actions/checkout")
    )
    assert step.get("with", {}).get("fetch-depth") == 0


def test_ci_runs_pytest_then_stamp_matrix() -> None:
    steps = _workflow()["jobs"]["ci"]["steps"]
    names = [s["name"] for s in steps if "name" in s]
    assert "pytest (merge logic)" in names
    assert "stamp matrix" in names


def test_stamp_matrix_scratch_root_inside_runner_workspace() -> None:
    """TEMPLATE_STAMP_ROOT must land inside the runner workspace: shared
    /tmp is the root-owned-hazard class (apt-18/19), and the runner's temp
    dir is per-job and self-clearing."""
    steps = _workflow()["jobs"]["ci"]["steps"]
    matrix_step = next(s for s in steps if s.get("name") == "stamp matrix")
    env = matrix_step.get("env", {})
    assert env.get("TEMPLATE_STAMP_ROOT") == "${{ runner.temp }}/stamp-matrix"
