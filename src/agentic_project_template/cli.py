"""agentic-project-template CLI: composition, layering, update.

Thin by design (spec: Constraint — the CLI stays thin). It invokes copier
and owns only the deterministic merges.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import copier
import typer
import yaml
from copier.errors import UserMessageError

from .stamp import apply_fragments, apply_layer, default_data, render_layer

app = typer.Typer(
    help="Add the agentic layer to a project, composed over a base template.",
    no_args_is_help=True,
)


def _parse_set(pairs: list[str]) -> dict:
    data: dict = {}
    for pair in pairs:
        key, _, value = pair.partition("=")
        data[key] = yaml.safe_load(value)
    return data


def _stamp_base(
    base: str, destination: Path, defaults: bool, data: dict | None = None
) -> None:
    copier.run_copy(base, str(destination), data=data or {}, defaults=defaults, quiet=False)


def _stamp_layer(
    destination: Path, data: dict, defaults: bool
) -> None:
    tmp = render_layer(destination, data, defaults=defaults)
    warnings = apply_layer(tmp, destination)
    for warning in warnings:
        typer.secho(f"warning: {warning}", fg=typer.colors.YELLOW)
    typer.secho(
        f"agentic layer stamped into {destination} "
        f"(answers: .agentic-answers.yml)",
        fg=typer.colors.GREEN,
    )


def _maybe_ask_base(destination: Path, non_interactive: bool) -> None:
    """Existing project + TTY: ask whether to stamp a base template first.

    Non-interactive without a flag defaults to layer-only (spec: Behavior
    Composition — the CLI orchestrates, copier stamps).
    """
    if non_interactive or not sys.stdin.isatty():
        return
    if not destination.exists() or not any(destination.iterdir()):
        return
    if typer.confirm(
        "Stamp a base template onto this existing project first?",
        default=False,
    ):
        base = typer.prompt("Base template ref (copier source)")
        _stamp_base(base, destination, defaults=False, data=default_data(destination))


@app.command()
def new(
    destination: Path = typer.Argument(..., help="New project directory"),
    base: Optional[str] = typer.Option(
        None, "--base", help="Base template ref (copier source), stamped first"
    ),
    non_interactive: bool = typer.Option(False, "--non-interactive"),
    set_data: Optional[list[str]] = typer.Option(None, "--set"),
) -> None:
    """New project: stamp the base template (if given), then the layer."""
    if destination.exists() and not destination.is_dir():
        typer.secho(
            f"error: {destination} exists and is not a directory",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(2)
    if destination.is_dir() and any(destination.iterdir()):
        typer.secho(
            f"error: {destination} is not empty; use 'layer' for existing projects",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(2)
    data = default_data(destination) | _parse_set(set_data or [])
    if base:
        _stamp_base(base, destination, defaults=non_interactive, data=data)
    _stamp_layer(destination, data, defaults=non_interactive)


@app.command()
def layer(
    destination: Path = typer.Argument(..., help="Existing project directory"),
    non_interactive: bool = typer.Option(False, "--non-interactive"),
    set_data: Optional[list[str]] = typer.Option(None, "--set"),
) -> None:
    """Stamp only the agentic layer onto an existing project."""
    _maybe_ask_base(destination, non_interactive)
    data = default_data(destination) | _parse_set(set_data or [])
    _stamp_layer(destination, data, defaults=non_interactive)


@app.command()
def update(
    destination: Path = typer.Argument(..., help="Stamped project directory"),
) -> None:
    """Update the agentic layer in a stamped project (layer answers file).

    copier re-renders with the stored answers; afterwards only the fragment
    merges run. A defaults re-render here would reset the user's layer
    choices (spec: two answers files).
    """
    answers = destination / ".agentic-answers.yml"
    if not answers.exists():
        typer.secho(
            f"error: {answers} not found; is this a layer-stamped project?",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(2)
    try:
        copier.run_update(
            str(destination),
            defaults=True,
            overwrite=True,
            quiet=True,
            answers_file=".agentic-answers.yml",
        )
    except UserMessageError as error:
        typer.secho(f"error: {error}", fg=typer.colors.RED, err=True)
        raise typer.Exit(2)
    warnings = apply_fragments(destination)
    for warning in warnings:
        typer.secho(f"warning: {warning}", fg=typer.colors.YELLOW)
    typer.secho("agentic layer updated", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
