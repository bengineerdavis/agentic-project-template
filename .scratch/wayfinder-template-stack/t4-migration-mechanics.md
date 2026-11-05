# T4 — Migration mechanics for concern moves across repos

Type: grilling (HITL) · Blocked by: T1, T2, T3
Status: OPEN · Claimed: nobody

## Question

When a concern's owning repo changes (T2/T3 outcomes), the layer's
deterministic-merge machinery is affected in ways already paid for once:
(a) _LAYER_AUTHORED_SCRIPTS provenance — if install.run's content moves to
another repo's fragment, the migration table + tripwire (tests/
test_merge.py::test_layer_authored_script_table_covers_fragment_history)
must walk the new repo's history or be retired; (b) copier answers files —
stamped projects record _src_path + _commit per layer; what updates them;
(c) migration warnings — the legacy-pin and stale-script migrations assume
the layer writes those keys; a moved concern needs the same base-wins-safe
handover. Decide the mechanics ONCE so each concern move is a pattern
instance, not a new design.
