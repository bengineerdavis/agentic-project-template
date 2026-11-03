"""Stamping: render the layer with copier, then apply it without clobbering.

Flow (spec: Composition — the CLI orchestrates, copier stamps):
  render layer into a temp dir -> copy clean paths (skip unmanaged existing)
  -> merge shared files -> apply fragments for files the template does not
  carry (mise.toml, prek.toml, .gitignore, AGENTS.md section).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import tomllib
from pathlib import Path
from typing import Any

import copier
import yaml

from .merge import (
    append_gitignore_lines,
    deep_merge,
    dump_toml,
    load_toml,
    load_yaml,
    merge_json_file,
    merge_mise_fragment,
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

# rendered paths stamped only when their flag is true (prefix-matched).
# The answers come from the render's own .agentic-answers.yml, so a
# template file excludes itself by living under a gated prefix. Copier
# cannot do this per file: it renders path segments independently, so a
# conditional spanning `docs/agents/x.md` is not expressible as a path.
CONDITIONAL_PATHS: dict[str, tuple[str, ...]] = {
    "include_backlog": ("docs/agents/", ".agents/skills/backlog-workflow/"),
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


def _include_backlog(destination: Path) -> bool:
    """Backlog stays stamped unless the project's answers opt out.

    A missing key (stamps that predate the question) means True: the update
    path must not strip wiring the project never chose to remove.
    """
    answers_file = destination / ".agentic-answers.yml"
    if not answers_file.exists():
        return True
    answers = load_yaml(answers_file)
    if not isinstance(answers, dict):
        return True
    return bool(answers.get("include_backlog", True))


def _strip_backlog_wiring(mise_text: str) -> str:
    """Remove the layer's backlog wiring from mise fragment text.

    include_backlog=false stamps a mise.toml with no backlog trace: the
    backlog-init task table goes, and with it the install chain's call —
    a stale call would fail the install (set -euo pipefail) once the task
    is gone. Text-level because deep_merge never removes keys, and the
    fragment's comments must survive.
    """
    mise_text = mise_text.replace("mise run backlog-init\n", "")
    return re.sub(r"\[tasks\.backlog-init\]\n(?:(?!\[)[^\n]*\n)*", "", mise_text)


def _strip_backlog_wiring_doc(doc: dict[str, Any]) -> None:
    """Same removal, TOML-level, for a destination mise.toml on the merge
    path (the update path rewrites it without comments either way).
    """
    tasks = doc.get("tasks")
    if not isinstance(tasks, dict):
        return
    tasks.pop("backlog-init", None)
    install = tasks.get("install")
    if isinstance(install, dict) and isinstance(install.get("run"), str):
        install["run"] = install["run"].replace("mise run backlog-init\n", "")


def _remove_gated_files(
    destination: Path, prefixes: tuple[str, ...]
) -> list[str]:
    """Remove layer-managed files under gated prefixes (flag turned off).

    Only files carrying the managed comment go: a project's own file in
    the same location stays, with a warning.
    """
    warnings: list[str] = []
    for prefix in prefixes:
        root = destination / prefix
        if not root.exists():
            continue
        for p in sorted(root.rglob("*"), reverse=True):
            if not p.is_file():
                continue
            rel = p.relative_to(destination).as_posix()
            text = p.read_text(encoding="utf-8", errors="replace")
            if MANAGED_COMMENT in text:
                p.unlink()
                warnings.append(f"removed {rel} (include_backlog off)")
            else:
                warnings.append(
                    f"kept existing {rel} (not layer-managed)"
                )
        for d in sorted(root.rglob("*"), reverse=True):
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()
        if root.is_dir() and not any(root.iterdir()):
            root.rmdir()
    return warnings


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

    backlog_on = _include_backlog(destination)

    mise_fragment = fragments / "mise-layer.toml"
    mise_target = destination / "mise.toml"
    mise_text = mise_fragment.read_text(encoding="utf-8")
    if not backlog_on:
        mise_text = _strip_backlog_wiring(mise_text)
    if mise_target.exists():
        if not backlog_on:
            base = load_toml(mise_target)
            _strip_backlog_wiring_doc(base)
            dump_toml(base, mise_target)
        warnings.extend(merge_mise_fragment(mise_target, tomllib.loads(mise_text)))
    else:
        mise_target.write_text(mise_text, encoding="utf-8")

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
    if backlog_on:
        backlog_section = (
            fragments / "agents-md-backlog-section.md"
        ).read_text(encoding="utf-8")
        section = section.rstrip("\n") + "\n\n" + backlog_section.strip() + "\n"
    upsert_marked_section(destination / "AGENTS.md", section)
    if not backlog_on:
        warnings.extend(
            _remove_gated_files(
                destination, CONDITIONAL_PATHS["include_backlog"]
            )
        )
    return warnings


def apply_layer(tmp: Path, destination: Path) -> list[str]:
    warnings: list[str] = []
    destination.mkdir(parents=True, exist_ok=True)

    answers_file = tmp / ".agentic-answers.yml"
    answers = load_yaml(answers_file) if answers_file.exists() else {}
    if not isinstance(answers, dict):
        answers = {}
    skipped_prefixes = tuple(
        prefix
        for flag, prefixes in CONDITIONAL_PATHS.items()
        if not answers.get(flag, True)
        for prefix in prefixes
    )

    for src in sorted(p for p in tmp.rglob("*") if p.is_file()):
        rel = src.relative_to(tmp).as_posix()
        if skipped_prefixes and rel.startswith(skipped_prefixes):
            continue
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
