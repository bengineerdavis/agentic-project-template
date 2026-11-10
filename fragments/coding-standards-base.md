## Testing

- **Test the contract you own, not the dependency.** Upstream tests establish
  a dependency's behavior at a particular release under its supported
  interfaces. Do not duplicate its rule-engine, parsing, packaging, or
  protocol tests. Test the behavior your project adds: configuration and
  defaults, composition, recorded choices, preservation of customizations,
  and the smallest real integration path that exercises them. Use observable
  behavior at public seams rather than snapshots of incidental configuration
  or implementation details. Version compatibility between independently
  selected dependencies is your integration responsibility, not upstream's.
  An integration failure is a failure, never a passing test. Provenance:
  copier-template-copier-template decision-1, "Test the contract we own,
  not the dependency".

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
