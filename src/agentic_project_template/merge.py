"""Deterministic merges for shared files.

Every merge here is pure, idempotent, and base-wins: the layer fills gaps,
it does not overwrite choices the project already made. The spec calls this
out as the only sanctioned path for touching shared files.
"""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path
from typing import Any

import tomli_w
import yaml

MARKER_BEGIN = "<!-- BEGIN managed: agentic-project-template -->"
MARKER_END = "<!-- END managed: agentic-project-template -->"
MARKED_SECTION_RE = re.compile(
    re.escape(MARKER_BEGIN) + r".*?" + re.escape(MARKER_END), re.DOTALL
)


def load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def dump_toml(doc: dict[str, Any], path: Path) -> None:
    path.write_text(tomli_w.dumps(doc), encoding="utf-8")


def load_yaml(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text)


def deep_merge(base: dict, overlay: dict) -> tuple[dict, list[str]]:
    """Merge overlay into base; base wins on conflicts, gaps are filled.

    Lists of dicts that carry a `name` key merge by name (dotagents
    [[skills]]/[[mcp]], prek repos). Other lists: base's entries are kept and
    overlay's unseen entries are appended. Returns (merged, warnings).
    """
    warnings: list[str] = []
    merged = dict(base)

    for key, incoming in overlay.items():
        if key not in merged:
            merged[key] = incoming
            continue
        existing = merged[key]
        if isinstance(existing, dict) and isinstance(incoming, dict):
            merged[key], sub = deep_merge(existing, incoming)
            warnings.extend(sub)
        elif _is_named_list(existing) and _is_named_list(incoming):
            merged[key] = _merge_named_lists(existing, incoming)
        elif isinstance(existing, list) and isinstance(incoming, list):
            merged[key] = existing + [item for item in incoming if item not in existing]
        elif existing != incoming:
            warnings.append(f"kept existing value for {key!r}: {existing!r}")
    return merged, warnings


def _is_named_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, dict) and "name" in item for item in value)
    )


def _merge_named_lists(base: list, overlay: list) -> list:
    by_name = {item["name"]: dict(item) for item in base}
    for item in overlay:
        if item["name"] in by_name:
            continue
        by_name[item["name"]] = dict(item)
    return list(by_name.values())


def merge_toml_file(destination: Path, overlay_doc: dict) -> list[str]:
    """Deep-merge an overlay TOML document into a destination TOML file."""
    base = load_toml(destination) if destination.exists() else {}
    merged, warnings = deep_merge(base, overlay_doc)
    dump_toml(merged, destination)
    return warnings


def merge_mise_fragment(destination: Path, overlay_doc: dict) -> list[str]:
    """Merge the layer's mise fragment into the project's mise.toml.

    Two migrations beyond the plain deep-merge, both for layer-owned state
    a pre-bump stamp carries and deep_merge (base wins, never removes)
    would otherwise keep forever:

    1. When the layer's pin for a tool moves to a backend-prefixed key, the
       project still carries the layer's old bare key. mise treats them as
       separate backend instances of the same tool and shim dispatch
       resolves the first provider, so the stale pin keeps winning
       (opencode 1.18.32 beside http:opencode 2.0.32 resolves 1.18.32;
       verified 2026-10-20). The bare key was written by an earlier layer
       stamp, not chosen by the project, so removing it migrates
       layer-owned state rather than overwriting a project choice.

    2. When the layer rewrites a task's script (tasks.install.run), the
       project keeps the earlier layer-authored script verbatim. Scripts
       the layer itself wrote across its history are recognized by exact
       match (hash) and replaced with the current one; anything else is
       hand-tuned project content and wins, as deep_merge dictates.
    """
    base = load_toml(destination) if destination.exists() else {}
    warnings: list[str] = []
    tools = base.get("tools")
    overlay_tools = overlay_doc.get("tools")
    if (
        isinstance(tools, dict)
        and isinstance(overlay_tools, dict)
        and isinstance(tools.get("opencode"), str)
        and isinstance(overlay_tools.get("http:opencode"), dict)
    ):
        del tools["opencode"]
        warnings.append(
            "removed legacy registry pin tools.opencode: the layer now pins "
            "opencode as http:opencode; coexisting keys make mise resolve "
            "the stale registry binary first"
        )
    tasks = base.get("tasks")
    overlay_tasks = overlay_doc.get("tasks")
    if isinstance(tasks, dict) and isinstance(overlay_tasks, dict):
        for task_name, incoming in overlay_tasks.items():
            if not isinstance(incoming, dict):
                continue
            incoming_run = incoming.get("run")
            if not isinstance(incoming_run, str):
                continue
            existing = tasks.get(task_name)
            if not isinstance(existing, dict):
                continue
            existing_run = existing.get("run")
            if not isinstance(existing_run, str) or existing_run == incoming_run:
                continue
            if existing_run not in _LAYER_AUTHORED_SCRIPTS:
                continue
            existing["run"] = incoming_run
            warnings.append(
                f"replaced layer-authored {task_name}.run with the current "
                "layer version (exact match against an earlier layer stamp); "
                "a hand-tuned script would have been kept"
            )
    merged, merge_warnings = deep_merge(base, overlay_doc)
    dump_toml(merged, destination)
    return warnings + merge_warnings


# Scripts the layer shipped in fragments across its history (hashes over the
# exact `run` strings; provenance in git history of fragments/mise-layer.toml
# and fragments/tools/*/mise.toml). An exact match identifies layer-authored
# content — the same provenance argument as the legacy registry-pin removal.
_LAYER_AUTHORED_SCRIPTS: frozenset[str] = frozenset(
    {
        # 4aa50b3 (Merge apt-24 backlog workflow into apt-22 per-tool fragments)
        '#!/usr/bin/env bash\nset -euo pipefail\n: "${TMPDIR:=/tmp}"\nif [ -d "$TMPDIR/fslock" ] && [ ! -w "$TMPDIR/fslock" ]; then\n  echo "ERROR: $TMPDIR/fslock is not writable by $(whoami) — aube (mise npm backend) will fail to lock." >&2\n  echo "  fix: sudo chown -R \\"$(id -un):$(id -gn)\\" \\"$TMPDIR/fslock\\"   # or: export TMPDIR=<user-owned dir>" >&2\n  exit 1\nfi\nmise install prek tombi "http:opencode" "github:asamarts/alint"\nmise install "npm:@sentry/dotagents"\ndotagents --project install\nprek install --force\nif ! mise install "github:kenn-io/roborev"; then\n  echo "warn: roborev install failed (github:kenn-io/roborev — continuing without it)" >&2\nfi\nif ! roborev init; then\n  echo "warn: roborev init failed (no git repo yet, or daemon unavailable)" >&2\nfi\nmise run backlog-init\n',

        # 93bdec6 (fix: install alint in the stamped bootstrap)
        '#!/usr/bin/env bash\nset -euo pipefail\n: "${TMPDIR:=/tmp}"\nif [ -d "$TMPDIR/fslock" ] && [ ! -w "$TMPDIR/fslock" ]; then\n  echo "ERROR: $TMPDIR/fslock is not writable by $(whoami) — aube (mise npm backend) will fail to lock." >&2\n  echo "  fix: sudo chown -R \\"$(id -un):$(id -gn)\\" \\"$TMPDIR/fslock\\"   # or: export TMPDIR=<user-owned dir>" >&2\n  exit 1\nfi\nmise install prek tombi opencode "github:asamarts/alint"\nmise install "npm:@sentry/dotagents"\ndotagents --project install\nprek install --force\nif ! mise install "github:kenn-io/roborev"; then\n  echo "warn: roborev install failed (github:kenn-io/roborev — continuing without it)" >&2\nfi\nif ! roborev init; then\n  echo "warn: roborev init failed (no git repo yet, or daemon unavailable)" >&2\nfi\nmise run backlog-init\n',

        # ffcb4d5 (fix: ignore dotagents artifacts in stamped projects)
        '#!/usr/bin/env bash\nset -euo pipefail\n: "${TMPDIR:=/tmp}"\nif [ -d "$TMPDIR/fslock" ] && [ ! -w "$TMPDIR/fslock" ]; then\n  echo "ERROR: $TMPDIR/fslock is not writable by $(whoami) — aube (mise npm backend) will fail to lock." >&2\n  echo "  fix: sudo chown -R \\"$(id -un):$(id -gn)\\" \\"$TMPDIR/fslock\\"   # or: export TMPDIR=<user-owned dir>" >&2\n  exit 1\nfi\nmise install prek tombi opencode\nmise install "npm:@sentry/dotagents"\ndotagents --project install\nprek install --force\nif ! mise install "github:kenn-io/roborev"; then\n  echo "warn: roborev install failed (backend unverified)" >&2\nfi\nif ! roborev init; then\n  echo "warn: roborev init failed (no git repo yet, or daemon unavailable)" >&2\nfi\nmise run backlog-init\n',

        # 93f10df (fix: make the stamped task-id prefix a template question)
        '#!/usr/bin/env bash\nset -euo pipefail\n: "${TMPDIR:=/tmp}"\nif [ -d "$TMPDIR/fslock" ] && [ ! -w "$TMPDIR/fslock" ]; then\n  echo "ERROR: $TMPDIR/fslock is not writable by $(whoami) — aube (mise npm backend) will fail to lock." >&2\n  echo "  fix: sudo chown -R \\"$(id -un):$(id -gn)\\" \\"$TMPDIR/fslock\\"   # or: export TMPDIR=<user-owned dir>" >&2\n  exit 1\nfi\nmise install prek tombi opencode alint dotagents\ndotagents --project install\nprek install --force\nif ! mise install roborev; then\n  echo "warn: roborev install failed (backend unverified)" >&2\nfi\nif ! roborev init; then\n  echo "warn: roborev init failed (no git repo yet, or daemon unavailable)" >&2\nfi\nmise run backlog-init\n',

        # a454d02 (Preflight the aube lock dir in install tasks (detection layer))
        '#!/usr/bin/env bash\nset -euo pipefail\n: "${TMPDIR:=/tmp}"\nif [ -d "$TMPDIR/fslock" ] && [ ! -w "$TMPDIR/fslock" ]; then\n  echo "ERROR: $TMPDIR/fslock is not writable by $(whoami) — aube (mise npm backend) will fail to lock." >&2\n  echo "  fix: sudo chown -R \\"$(id -un):$(id -gn)\\" \\"$TMPDIR/fslock\\"   # or: export TMPDIR=<user-owned dir>" >&2\n  exit 1\nfi\nmise install prek tombi opencode alint dotagents\ndotagents --project install\nprek install --force\nif ! mise install roborev; then\n  echo "warn: roborev install failed (backend unverified — backlog task apt-3)" >&2\nfi\nif ! roborev init; then\n  echo "warn: roborev init failed (no git repo yet, or daemon unavailable)" >&2\nfi\nmise run backlog-init\n',

        # 23f8862 (Stamp worktrunk wiring into projects (apt-13))
        '#!/usr/bin/env bash\nset -euo pipefail\nmise install prek tombi opencode alint dotagents\ndotagents --project install\nprek install --force\nif ! mise install roborev; then\n  echo "warn: roborev install failed (backend unverified — backlog task apt-3)" >&2\nfi\nif ! roborev init; then\n  echo "warn: roborev init failed (no git repo yet, or daemon unavailable)" >&2\nfi\nmise run backlog-init\n',

    }
)


def _repo_signature(entry: dict) -> tuple:
    hook_ids = frozenset(
        hook.get("id") for hook in entry.get("hooks", []) if isinstance(hook, dict)
    )
    return entry.get("repo"), hook_ids


def _merge_repo_lists(existing: list, incoming: list) -> tuple[list, list[str]]:
    """Merge prek repo entries; base wins, dedupe by repo + hook-id set.

    Exact-dict equality is not enough: the same repo pinned at a different
    rev must not duplicate the entry (the hooks would run twice).
    """
    warnings: list[str] = []
    merged = [e for e in existing if isinstance(e, dict)]
    seen = {_repo_signature(e): e for e in merged}
    for entry in incoming:
        if not isinstance(entry, dict):
            continue
        signature = _repo_signature(entry)
        if signature in seen:
            if seen[signature] != entry:
                warnings.append(
                    f"prek repo {entry.get('repo')!r} already present; kept existing"
                )
            continue
        merged.append(entry)
        seen[signature] = entry
    return merged, warnings


def merge_prek_config(
    destination_root: Path, repo_entries: list[dict]
) -> tuple[Path, list[str]]:
    """Append [[repos]] entries to the project's prek config.

    Native `prek.toml` is merged as TOML when present (or created when no
    config exists at all). A legacy `.pre-commit-config.yaml` is appended to
    in its own YAML format instead, because prek would otherwise read only
    one config and silently drop the legacy hooks. Returns (path, warnings).
    """
    native = destination_root / "prek.toml"
    legacy = destination_root / ".pre-commit-config.yaml"
    if native.exists() or not legacy.exists():
        doc = load_toml(native) if native.exists() else {}
        repos, warnings = _merge_repo_lists(doc.get("repos", []), repo_entries)
        doc["repos"] = repos
        dump_toml(doc, native)
        if native.exists() and legacy.exists():
            warnings.append(
                "both prek.toml and .pre-commit-config.yaml exist; "
                "prek reads prek.toml — migrate legacy hooks or drop one config"
            )
        return native, warnings
    doc = load_yaml(legacy) or {}
    if not isinstance(doc, dict):
        return legacy, [".pre-commit-config.yaml is not a mapping; left untouched"]
    original_count = len(doc.get("repos", []))
    repos, warnings = _merge_repo_lists(doc.get("repos", []), repo_entries)
    doc["repos"] = repos
    if len(repos) != original_count:
        legacy.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
        warnings.append(
            "appended to legacy .pre-commit-config.yaml; prek reads prek.toml "
            "when both exist — migrate these hooks before adding a prek.toml"
        )
    return legacy, warnings


def append_gitignore_lines(destination: Path, lines: list[str]) -> None:
    existing = set()
    if destination.exists():
        existing = {
            line.strip()
            for line in destination.read_text(encoding="utf-8").splitlines()
        }
    missing = [
        line
        for line in lines
        if line.strip() and line.strip() not in existing
    ]
    if not missing:
        return
    with destination.open("a", encoding="utf-8") as fh:
        if destination.exists() and destination.stat().st_size > 0:
            fh.write("\n")
        fh.write("\n".join(missing) + "\n")


def upsert_marked_section(destination: Path, section: str) -> None:
    """Insert or replace the managed section in a markdown file."""
    block = f"{MARKER_BEGIN}\n{section.strip()}\n{MARKER_END}\n"
    if destination.exists():
        text = destination.read_text(encoding="utf-8")
        if MARKED_SECTION_RE.search(text):
            text = MARKED_SECTION_RE.sub(
                lambda _match: block.rstrip("\n"), text
            )
        else:
            if not text.endswith("\n"):
                text += "\n"
            text += "\n" + block
        destination.write_text(text, encoding="utf-8")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(block, encoding="utf-8")


def merge_json_file(destination: Path, overlay: dict) -> list[str]:
    base = {}
    if destination.exists():
        base = json.loads(destination.read_text(encoding="utf-8"))
    merged, warnings = deep_merge(base, overlay)
    destination.write_text(
        json.dumps(merged, indent=2) + "\n", encoding="utf-8"
    )
    return warnings
