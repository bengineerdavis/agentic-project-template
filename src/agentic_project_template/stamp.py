"""Stamping: render the layer with copier, then apply it without clobbering.

Flow (spec: Composition — the CLI orchestrates, copier stamps):
  render layer into a temp dir -> copy clean paths (skip unmanaged existing)
  -> merge shared files -> apply fragments for files the template does not
  carry (mise.toml, prek.toml, .gitignore, AGENTS.md section).
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

import copier
import yaml

from .merge import (
    append_gitignore_lines,
    deep_merge,
    load_toml,
    load_yaml,
    merge_json_file,
    merge_prek_config,
    merge_toml_file,
    upsert_marked_section,
)

# every stamped file carries this managed comment; a file that merely
# mentions the tool must not be treated as layer-managed
MANAGED_COMMENT = "managed by agentic-project-template"

RENDERED_SHARED = {
    ".opencode/opencode.json": "json",
    "agents.toml": "toml",
    ".alint.yml": "yaml",
}


def repo_root() -> Path:
    env = os.environ.get("AGENTIC_TEMPLATE_SRC")
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve().parent
    dev_checkout = here.parents[1]
    if (dev_checkout / "copier.yml").exists():
        return dev_checkout
    if (here / "copier.yml").exists():
        return here
    raise RuntimeError(
        "cannot locate agentic-project-template sources; "
        "set AGENTIC_TEMPLATE_SRC"
    )


def default_data(destination: Path) -> dict[str, Any]:
    return {"project_name": destination.resolve().name, "description": ""}


def render_layer(destination: Path, data: dict[str, Any], defaults: bool) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="agentic-layer-"))
    try:
        copier.run_copy(
            str(repo_root()),
            str(tmp),
            data=data,
            defaults=defaults,
            quiet=True,
        )
    except BaseException:
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    return tmp


def _stamp_file(src: Path, target: Path, rel: str, warnings: list[str]) -> None:
    if target.exists():
        text = target.read_text(encoding="utf-8", errors="replace")
        if MANAGED_COMMENT in text:
            target.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            warnings.append(f"skipped existing {rel} (not layer-managed)")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, target)


def _merge_rendered(kind: str, src: Path, target: Path) -> list[str]:
    if kind == "json":
        return merge_json_file(target, json.loads(src.read_text(encoding="utf-8")))
    if kind == "toml":
        return merge_toml_file(target, load_toml(src))
    if kind == "yaml":
        base = load_yaml(target) or {}
        overlay = load_yaml(src) or {}
        merged, warnings = deep_merge(base, overlay)
        target.write_text(yaml.safe_dump(merged, sort_keys=False), encoding="utf-8")
        return warnings
    raise ValueError(f"unknown merge kind: {kind}")


def apply_fragments(destination: Path) -> list[str]:
    """Apply fragment merges for shared files the template does not carry.

    Called after a fresh render (apply_layer) and after `copier update` —
    never together with a defaults re-render, which would reset the user's
    layer choices (spec: two answers files).
    """
    warnings: list[str] = []
    destination.mkdir(parents=True, exist_ok=True)
    root = repo_root()
    fragments = root / "fragments"

    mise_fragment = fragments / "mise-layer.toml"
    mise_target = destination / "mise.toml"
    if mise_target.exists():
        warnings.extend(
            merge_toml_file(mise_target, load_toml(mise_fragment))
        )
    else:
        shutil.copy2(mise_fragment, mise_target)

    prek_entries = load_toml(fragments / "prek-layer.toml")["repos"]
    _, prek_warnings = merge_prek_config(destination, prek_entries)
    warnings.extend(prek_warnings)

    append_gitignore_lines(
        destination / ".gitignore",
        (fragments / "gitignore-layer.txt")
        .read_text(encoding="utf-8")
        .splitlines(),
    )

    wt_fragment = fragments / "wt-layer.toml"
    wt_target = destination / ".config" / "wt.toml"
    if wt_target.exists():
        warnings.extend(merge_toml_file(wt_target, load_toml(wt_fragment)))
    else:
        wt_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(wt_fragment, wt_target)

    section = (fragments / "agents-md-section.md").read_text(encoding="utf-8")
    upsert_marked_section(destination / "AGENTS.md", section)
    return warnings


def apply_layer(tmp: Path, destination: Path) -> list[str]:
    warnings: list[str] = []
    destination.mkdir(parents=True, exist_ok=True)

    for src in sorted(p for p in tmp.rglob("*") if p.is_file()):
        rel = src.relative_to(tmp).as_posix()
        target = destination / rel
        if rel == ".agentic-answers.yml":
            # always refresh: it records the latest layer choices
            shutil.copy2(src, target)
            continue
        kind = RENDERED_SHARED.get(rel)
        if kind and target.exists():
            warnings.extend(_merge_rendered(kind, src, target))
        elif kind:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
        else:
            _stamp_file(src, target, rel, warnings)

    warnings.extend(apply_fragments(destination))

    shutil.rmtree(tmp, ignore_errors=True)
    return warnings
