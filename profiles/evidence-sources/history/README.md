# Historical evidence-source profile snapshots

When a reviewed source profile changes, the previous file is moved here
unchanged (renamed `<slug>@<sha256-hex-prefix>.yaml`) and its `superseded_by`
field is **not** edited -- the historical bytes, and therefore the digest that
existing evidence is bound to, must stay identical. The new active profile
records `supersedes: sha256:<old digest>`.

Snapshots here are resolvable **only by exact digest** for historical
evaluation (`EvidenceAdapterRegistry.historical_resolver`). They are never
returned by the current resolver. See
`docs/agile-v-runtime/15_EVIDENCE_ADAPTER_REGISTRY.md` section 6.
