# Trusted Admission Context

**Contract version: 1.0.** Issue [#42](https://github.com/Agile-V/agile_v_skills/issues/42).
This refines the aggregate APIs in the [Evidence Admission Contract](07_EVIDENCE_ADMISSION_CONTRACT.md).

## Aggregate evidence requirements

| Input | Trusted aggregate rule |
|---|---|
| Schema | Validate the current repository schema before semantic checks. Invalid/unknown versions are rejected. |
| Source resolver | `resolve_adapter(adapter_ref)` is mandatory at every risk level. Missing, unavailable, or malformed profiles reject admission. |
| Source identity | Resolved `adapter_id` and `evidence_type` must match the evidence source and item. |
| Immutable source | `evidence_source.adapter_digest` must equal `profile_digest(resolved_profile)`; omission is rejected even if the storage schema permits it. |
| Property resolver | `resolve_property_profile(claim_type, risk_level)` must deterministically select the governing profile outside candidate write authority. |
| Property requirements | Use the union of profile-required properties and claim-local additions. Local lists cannot weaken the profile. |
| Property capability | Reject any claimed property outside `may_establish - may_not_establish`; do not silently discard an overclaim. |
| History | Resolve the historical profile snapshot matching the bound digest, or reject reuse. Never reinterpret old evidence using a changed profile with the same ID. |

`profile_digest` hashes the **whole profile envelope**, serialized as UTF-8
JSON with sorted keys, compact separators, ASCII escaping, and non-finite
numbers forbidden. It is the Python reference serialization, not an RFC 8785
claim. A profile has no embedded self-digest. Resolver-returned snapshots are
copied and checked once per invocation; evidence records are not modified.

The existing storage schema versions remain readable; aggregate semantics
are stricter than storage validity. Legacy resolver-less predicate calls are
advisory only and cannot authorize a transition.

## Trusted gate context

`evaluate_gate_receipt` and `authorize_gate_transition` require a
`decision_context` supplied by the transition authority:

```yaml
task_id: AAV-0042
gate: gate_2
subject_state: {} # exact accepted subject object, including its digest/baseline
policy_digest: sha256:...
risk_level: L2
action: release
resources: [ART-1]
critical_risks: [] # unresolved critical-risk references from trusted risk records
non_waivable_controls: [] # optional domain additions; core prohibitions remain
```

The context is **not** a candidate assertion or a resolver for arbitrary
candidate-selected policy. Its source must be authenticated/accepted by the
runtime. Absent/malformed context rejects admission; a non-empty critical-risk
set blocks advancement until a new accepted risk context records disposition.
A generic approval or unrelated exception cannot discharge it.

`verify_authority(kind, resolved_record, decision_context)` must return exactly
`True` only after authenticating the human principal, role, current delegated
authority, exact subject/policy/action scope, and applicable separation of duties.
It is mandatory for human gate approvals and exception decisions. Merely
resolving a JSON file or seeing `authorship: human` is not authentication.
Production providers must check revocation and single-use state externally.
The repository tests use explicitly synthetic authority providers.

The gate additionally checks the approval's exact task/gate/digest/policy/baseline,
action and resource set. The combined path checks the bundle's task, digest,
baseline, policy, claim inventory, and risk against the gate/context. Gate 2
requires an evidence bundle. Missing risk is not permission to skip independence.

## Boundaries and migration

| Concern | Rule |
|---|---|
| Low-level predicates | Diagnostic checks, not admission capabilities; success of one is insufficient. |
| `authorize_gate_transition` | Returns eligibility findings only. It performs no deployment, state write, signing, or atomic approval consumption. |
| Runtime enforcement | Recheck trusted context and approval state at the effect boundary; atomically consume single-use authority. |
| Resolver failures | Return structured rejection; do not expose provider error payloads. |
| Residual-risk acceptance | May disposition risk under the risk contract; cannot waive failed verification claims. |
| Reuse | Missing item and assessment coverage defaults to unknown, never complete. |
| Existing integrations | Supply both profile resolvers, trusted decision context and authority verification before using aggregate results. |

All negative journeys exercise these aggregate checks. This does not establish
live runtime conformance; see [runtime status](../../conformance/RUNTIME_STATUS.md).
