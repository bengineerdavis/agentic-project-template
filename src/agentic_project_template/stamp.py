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


# apt-22: per-tool fragments are applied in this declared order — the
# single source of ordering for every shared-file merge (prek [[repos]]
# hook order, AGENTS.md bullet order, mise [tools] appearance). Sorted-
# directory inference is forbidden: a new fragments/tools/<tool>/ dir
# fails test_per_tool_fragments_are_declared until it is declared here.
TOOL_FRAGMENT_ORDER = (
    "roborev",
    "opencode",
    "pyright",
    "dotagents",
    "worktrunk",
    "backlog-py",
    "tombi",
    "alint",
    "prek",
    "mise",
    "consult-llm",
)


def _include_backlog(destination: Path) -> bool:
    """Backlog stays stamped unless the project's answers opt out."""
    return _include_flag(destination, "include_backlog")


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

    Fragments are per tool (fragments/tools/<tool>/: mise pin + tasks,
    prek hooks, gitignore lines, AGENTS.md lines) plus the top-level
    layer-composition fragments (bootstrap install, check gate, section
    prose). Every merge runs in TOOL_FRAGMENT_ORDER.
    """
    warnings: list[str] = []
    destination.mkdir(parents=True, exist_ok=True)
    root = repo_root()
    fragments = root / "fragments"

    backlog_on = _include_backlog(destination)
    lore_on = _include_flag(destination, "include_lore")
    if not lore_on:
        _strip_lore_pointer(destination, warnings)
    _merge_mise(destination, fragments / "mise-layer.toml", warnings, backlog_on)

    for tool in TOOL_FRAGMENT_ORDER:
        if tool == "backlog-py" and not backlog_on:
            continue
        tool_dir = fragments / "tools" / tool
        if not tool_dir.is_dir():
            raise FileNotFoundError(
                f"declared fragment dir missing: {tool_dir}"
            )

        mise_fragment = tool_dir / "mise.toml"
        if mise_fragment.exists():
            _merge_mise(destination, mise_fragment, warnings, backlog_on)

        prek_fragment = tool_dir / "prek.toml"
        if prek_fragment.exists():
            _, prek_warnings = merge_prek_config(
                destination, load_toml(prek_fragment)["repos"]
            )
            warnings.extend(prek_warnings)

        gitignore_fragment = tool_dir / "gitignore.txt"
        if gitignore_fragment.exists():
            append_gitignore_lines(
                destination / ".gitignore",
                gitignore_fragment.read_text(encoding="utf-8").splitlines(),
            )

        wt_fragment = tool_dir / "wt.toml"
        if wt_fragment.exists():
            wt_target = destination / ".config" / "wt.toml"
            if wt_target.exists():
                warnings.extend(
                    merge_toml_file(wt_target, load_toml(wt_fragment))
                )
            else:
                wt_target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(wt_fragment, wt_target)

    upsert_marked_section(
        destination / "AGENTS.md",
        _compose_agents_md_section(fragments, backlog_on),
    )
    if not backlog_on:
        warnings.extend(
            _remove_gated_files(destination, CONDITIONAL_PATHS["include_backlog"])
        )
    return warnings


LORE_POINTER = "Long-term knowledge lives in `.lore.md`"


def _include_flag(destination: Path, flag: str, default: bool = True) -> bool:
    """Read one boolean layer answer; missing key means the default.

    Stamps that predate a question never opted out, so the update path
    must not strip wiring the project never chose to remove.
    """
    answers_file = destination / ".agentic-answers.yml"
    if not answers_file.exists():
        return default
    answers = load_yaml(answers_file)
    if not isinstance(answers, dict):
        return default
    return bool(answers.get(flag, default))


def _strip_lore_pointer(destination: Path, warnings: list[str]) -> None:
    """Remove the ai-rules lore pointer (include_lore turned off).

    .lore.md itself is project data and is never touched here. Text-level
    on the rendered file because the pointer rides a gated jinja block,
    not a mergeable section.
    """
    ai_rules = destination / ".context" / "ai-rules.md"
    if not ai_rules.exists():
        return
    text = ai_rules.read_text(encoding="utf-8")
    if LORE_POINTER not in text:
        return
    lines = text.splitlines(keepends=True)
    kept: list[str] = []
    skipping = False
    for line in lines:
        if LORE_POINTER in line:
            skipping = True
            warnings.append("removed lore pointer from .context/ai-rules.md")
            continue
        if skipping:
            # continuation lines: indented, until a bullet ("- ") or blank
            if line.startswith("  ") and line.strip():
                continue
            skipping = False
        kept.append(line)
    ai_rules.write_text("".join(kept), encoding="utf-8")


def _merge_mise(
    destination: Path, fragment: Path, warnings: list[str], backlog_on: bool
) -> None:
    """Merge one mise fragment into the project's mise.toml.

    include_backlog=false strips the backlog wiring from both sides: the
    fragment text (task table + install-chain call) and the destination's
    own doc (stale wiring from a previous stamp). Text-level for fragments
    because deep_merge never removes keys and comments must survive.
    """
    mise_target = destination / "mise.toml"
    mise_text = fragment.read_text(encoding="utf-8")
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


def _compose_agents_md_section(fragments: Path, backlog_on: bool) -> str:
    """The managed AGENTS.md section: layer prose first, then each tool's
    lines in TOOL_FRAGMENT_ORDER (apt-22: declared, not directory-sorted).
    include_backlog=false (apt-24) drops the backlog prose block too."""
    parts = [
        (fragments / "agents-md-section.md")
        .read_text(encoding="utf-8")
        .rstrip("\n")
    ]
    for tool in TOOL_FRAGMENT_ORDER:
        if tool == "backlog-py" and not backlog_on:
            continue
        agents_fragment = fragments / "tools" / tool / "agents.md"
        if agents_fragment.exists():
            parts.append(agents_fragment.read_text(encoding="utf-8").rstrip("\n"))
    if backlog_on:
        parts.append(
            (fragments / "agents-md-backlog-section.md")
            .read_text(encoding="utf-8")
            .strip()
        )
    return "\n\n".join(parts) + "\n"


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
