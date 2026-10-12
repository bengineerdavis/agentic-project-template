from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def template_src(monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("AGENTIC_TEMPLATE_SRC", str(REPO_ROOT))
    return REPO_ROOT
