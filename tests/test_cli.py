from pathlib import Path

from typer.testing import CliRunner

from agentic_project_template.cli import app

runner = CliRunner()


def test_new_rejects_file_destination(tmp_path: Path) -> None:
    target = tmp_path / "afile"
    target.write_text("x")
    result = runner.invoke(app, ["new", str(target), "--non-interactive"])
    assert result.exit_code == 2
    assert "not a directory" in result.output


def test_update_requires_layer_answers(tmp_path: Path) -> None:
    result = runner.invoke(app, ["update", str(tmp_path)])
    assert result.exit_code == 2
    assert "not found" in result.output
