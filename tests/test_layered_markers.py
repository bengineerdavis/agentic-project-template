"""Per-writer markers: several writers share one markdown file (T2).

The single-marker upsert cannot serve a layered file: the regex matches the
first block, so a second writer silently destroys the first. Ansible's
blockinfile documents the fix — "when more than one block should be handled in
one file you must change the marker per task" — and the same convention is
adopted here, with the writer's name in the marker.
"""

from agentic_project_template.merge import (
    WRITER_MARKERS,
    managed_block,
    remove_managed_section,
    upsert_marked_section,
)


def test_three_writers_coexist_without_destroying_each_other(tmp_path) -> None:
    target = tmp_path / "CODING_STANDARDS.md"
    target.write_text("# Coding standards\n\n## Testing\n\nProject text.\n")

    upsert_marked_section(target, "## Language\n\n- python rule", writer="base")
    upsert_marked_section(target, "## Agent\n\n- agentic rule", writer="overlay")
    upsert_marked_section(target, "## Defaults\n\n- meta rule", writer="meta")

    text = target.read_text()
    assert "python rule" in text
    assert "agentic rule" in text
    assert "meta rule" in text
    assert "Project text." in text
    assert text.count("BEGIN managed") == 3


def test_rewriting_one_writer_leaves_the_others_intact(tmp_path) -> None:
    target = tmp_path / "AGENTS.md"
    target.write_text("# Existing\n")
    upsert_marked_section(target, "base v1", writer="base")
    upsert_marked_section(target, "overlay v1", writer="overlay")

    upsert_marked_section(target, "base v2", writer="base")

    text = target.read_text()
    assert "base v2" in text and "base v1" not in text
    assert "overlay v1" in text
    assert text.count("BEGIN managed") == 2


def test_each_writer_upsert_is_idempotent(tmp_path) -> None:
    target = tmp_path / "CONTRIBUTING.md"
    target.write_text("# Contributing\n")
    for _ in range(3):
        upsert_marked_section(target, "base body", writer="base")
        upsert_marked_section(target, "overlay body", writer="overlay")
    text = target.read_text()
    assert text.count("BEGIN managed: base") == 1
    assert text.count("BEGIN managed: overlay") == 1
    assert text.count("END managed") == 2


def test_blocks_are_ordered_by_rank_not_by_write_order(tmp_path) -> None:
    """Meta renders first, then base, then overlay — whatever order we write."""
    target = tmp_path / "STD.md"
    target.write_text("# Std\n")
    upsert_marked_section(target, "OVERLAY", writer="overlay")
    upsert_marked_section(target, "META", writer="meta")
    upsert_marked_section(target, "BASE", writer="base")
    text = target.read_text()
    assert text.index("META") < text.index("BASE") < text.index("OVERLAY")


def test_removing_a_writer_drops_only_its_block(tmp_path) -> None:
    target = tmp_path / "STD.md"
    target.write_text("# Std\n\nProject prose.\n")
    upsert_marked_section(target, "meta body", writer="meta")
    upsert_marked_section(target, "overlay body", writer="overlay")

    remove_managed_section(target, writer="overlay")

    text = target.read_text()
    assert "meta body" in text
    assert "overlay body" not in text
    assert "Project prose." in text
    assert text.count("BEGIN managed") == 1


def test_removing_an_absent_writer_is_a_no_op(tmp_path) -> None:
    target = tmp_path / "STD.md"
    target.write_text("# Std\n")
    upsert_marked_section(target, "meta body", writer="meta")
    before = target.read_text()
    remove_managed_section(target, writer="overlay")
    assert target.read_text() == before


def test_removing_a_writer_deletes_the_file_only_when_nothing_remains(tmp_path) -> None:
    target = tmp_path / "EMPTY.md"
    target.write_text("# Std\n")
    upsert_marked_section(target, "meta body", writer="meta")
    remove_managed_section(target, writer="meta")
    assert target.exists()
    assert "meta body" not in target.read_text()

    lone = tmp_path / "LONE.md"
    upsert_marked_section(lone, "only body", writer="meta")
    remove_managed_section(lone, writer="meta")
    assert not lone.exists()


def test_unknown_writer_is_rejected(tmp_path) -> None:
    target = tmp_path / "STD.md"
    target.write_text("# Std\n")
    try:
        upsert_marked_section(target, "body", writer="bogus")
    except ValueError as exc:
        assert "bogus" in str(exc)
    else:
        raise AssertionError("unknown writer must raise")


def test_writer_markers_are_declared_and_distinct() -> None:
    assert set(WRITER_MARKERS) == {"meta", "base", "overlay"}
    rendered = {w: managed_block(w, "x") for w in WRITER_MARKERS}
    assert len(set(rendered.values())) == 3


def test_coding_standards_base_block_is_created_with_its_header(tmp_path) -> None:
    """T2 Q2/Q3: the base creates the file and owns the vacuity-guard rule."""
    from pathlib import Path as _Path

    from agentic_project_template.stamp import CODING_STANDARDS_HEADER

    fragment = (
        _Path(__file__).parents[1] / "fragments" / "coding-standards-base.md"
    ).read_text(encoding="utf-8")
    assert "vacuity guard" in fragment

    target = tmp_path / "CODING_STANDARDS.md"
    target.write_text(CODING_STANDARDS_HEADER, encoding="utf-8")
    upsert_marked_section(target, fragment, writer="base")

    text = target.read_text()
    assert text.startswith(CODING_STANDARDS_HEADER)
    assert "BEGIN managed: base" in text
    assert "vacuity guard" in text


def test_legacy_single_marker_is_adopted_as_the_overlay_block(tmp_path) -> None:
    """A project stamped before this change carries the old un-named marker."""
    legacy = (
        "# Std\n\n"
        "<!-- BEGIN managed: agentic-project-template -->\n"
        "old agentic rule\n"
        "<!-- END managed: agentic-project-template -->\n"
    )
    target = tmp_path / "CODING_STANDARDS.md"
    target.write_text(legacy)

    upsert_marked_section(target, "new agentic rule", writer="overlay")

    text = target.read_text()
    assert "new agentic rule" in text
    assert "old agentic rule" not in text
    assert "agentic-project-template" not in text
    assert text.count("BEGIN managed") == 1
