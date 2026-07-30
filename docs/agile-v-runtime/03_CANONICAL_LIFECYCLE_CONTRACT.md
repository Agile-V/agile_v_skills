# Canonical Lifecycle Contract

> **Normative.** This contract governs requirements, findings, baselines, claims, and their trace links. It is implemented by [REQUIREMENTS.schema.json](../../schemas/REQUIREMENTS.schema.json), [TRACE_GRAPH.schema.json](../../schemas/TRACE_GRAPH.schema.json), [APPROVAL.schema.json](../../schemas/APPROVAL.schema.json), and [EVIDENCE_BUNDLE.schema.json](../../schemas/EVIDENCE_BUNDLE.schema.json).

## Canonical requirement flow

`draft_persisted -> independent_findings -> architect_revisions -> gate_1 -> approved -> baselined`

| State | Owner/action | Required record | Permitted transition |
|---|---|---|---|
| `draft_persisted` | Requirement Architect persists a draft; it is not synthesis input | `REQUIREMENTS` requirement node | `independent_findings` |
| `independent_findings` | Logic Gatekeeper records findings only; it does not rewrite the draft | `TRACE_GRAPH` `finding` nodes/edges | `architect_revisions` |
| `architect_revisions` | Requirement Architect resolves or rejects each finding with rationale | revised requirement + decision link | `independent_findings` or `gate_1` |
| `gate_1` | Human reviews the revision and findings | `APPROVAL` record | `approved` or `architect_revisions` |
| `approved` | Gate 1 approved, immutable pending baseline capture | approval edge | `baselined` |
| `baselined` | Approved revision is frozen and becomes the only synthesis input | `baseline` node + inclusion edge | `changed` or `retired` through a change request |

**Rules:** Persist before independent review; a rejected Gate 1 returns only to `architect_revisions`; `baselined` content is never edited in place. A change creates a new draft revision linked by `change_request`; the former baseline remains immutable.

## Typed graph contract

| From → relation → to | Meaning |
|---|---|
| `requirement -> derived_from -> source|goal|observation|threat|law` | Requirement lineage |
| `finding -> challenges -> requirement` | Independent issue; never an edit instruction applied by the gatekeeper |
| `requirement -> resolved_by -> requirement` | Architect revision resolves a prior draft/finding set |
| `approval -> approves -> requirement` | Gate 1 decision for a revision |
| `baseline -> includes -> requirement` | Frozen approved revision |
| `artifact -> implements -> requirement` | A synthesis artifact implements a specific baselined REQ revision; record the baseline reference |
| `test_case -> verifies -> requirement` | An independently specified test verifies a specific baselined REQ revision |
| `verification -> evaluates -> artifact|test_case` | Verification evidence evaluates the artifact or test execution it concerns |
| `claim -> supported_by -> evidence|verification|validation` | Claim support; support is not proof of certification |
| `claim -> bounded_by -> risk|assumption` | Explicit scope, residual uncertainty, or rebuttal |

Nodes use `id`, `type`, `revision`, and `state`; edges use `source`, `target`, `relation`, and an evidence locator as defined by `TRACE_GRAPH.schema.json`. Claims are qualified engineering assertions, not certification statements.

**Lineage rule:** Do not use a universal `artifact -> REQ-XXXX` shorthand. Synthesis artifacts require the `implements` relation to a baselined requirement; tests require `verifies`; claims, findings, approvals, baselines, discovery, threats, and governance records use the applicable typed relation above. A REQ ID alone is insufficient without revision and baseline evidence where synthesis occurs.

## Compatibility

Legacy requirement values map as follows: `draft -> draft_persisted`; `validated -> independent_findings` (review complete only when findings are recorded); `approved -> approved`; `baselined -> baselined`; `changed -> architect_revisions`; `retired -> retired`. Legacy artifacts must declare their mapping in `migration` until migrated.
