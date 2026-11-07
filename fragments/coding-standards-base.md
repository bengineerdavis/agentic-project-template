## Testing

- **Every vacuity guard must be shown to fire.** A vacuity guard is an
  assertion whose purpose is to stop a test from passing vacuously (a walk
  that saw nothing, a collection that is empty by construction). Write it so
  the test cannot pass without real data, then prove it: demonstrate the
  failure (e.g. red-proof by removing a data source in process) at least once
  when the guard is introduced. A guard that cannot fire is itself a finding.
  Count thresholds are suspect when a single construction site (e.g. HEAD's
  tree alone) already satisfies them — prefer guards on the *substance* the
  test exists to check (e.g. "the walk saw at least one stale item") over
  counts.
