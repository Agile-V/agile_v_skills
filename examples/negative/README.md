# Negative Golden Journeys

All ten scenarios in [manifest.yaml](manifest.yaml) execute
`contracts.semantics.authorize_gate_transition` in
[`test_issue42_trust_closure.py`](../../tests/test_issue42_trust_closure.py).
The positive control uses the same fixture set and trusted-provider inputs.

| Scenario | Required rejection code |
|---|---|
| stale-evidence | `EVIDENCE_STATE_MISMATCH` |
| self-approval | `HUMAN_AUTHORITY_UNVERIFIED` |
| missing-baseline | `SCHEMA_INVALID` |
| forged-human-authorship | `HUMAN_AUTHORITY_UNVERIFIED` |
| out-of-scope-change | `APPROVAL_SCOPE_MISMATCH` |
| policy-drift | `EVIDENCE_POLICY_MISMATCH` |
| expired-approval | `APPROVAL_NOT_JUSTIFIED` |
| unresolved-critical-risk | `UNRESOLVED_CRITICAL_RISK` |
| verifier-contamination | `INDEPENDENCE_BELOW_MINIMUM` |
| evolve-goalpost-change | `DECISION_CONTEXT_MISMATCH` |

These are deterministic contract tests using synthetic provider records.
They do not demonstrate live human authentication, automatic detection of
verifier contamination, sandbox prevention of file writes, or execution by
an external runtime. The scope test rejects authorization of an expanded
resource set; the contamination test supplies a degraded independence class.
Production integrations must establish these inputs independently of the
candidate and enforce the returned decision at the actual action boundary.
