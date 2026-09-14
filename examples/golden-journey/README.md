# Golden Journey (executable fixture map)

> **Scope note.** This is a fixture *map*, not a new set of artifacts: every stage below points to an existing, schema-validated fixture already exercised by the test suite (`tests/test_schemas.py`, `tests/test_evidence_bundle_v2.py`, `tests/test_gate_receipt_and_approval_v2.py`, `tests/test_risk_assessment_v2.py`, `tests/test_exception_and_waiver.py`, `tests/test_governance_conversion.py`). `tests/test_golden_journey.py` re-validates each referenced file against its schema directly from this directory's manifest, so the map cannot silently go stale. Fixture IDs are illustrative per-record examples, not a single globally unified task; see the "ID consistency" note at the end.

## Stages

| Stage | Artifact | Fixture |
|---|---|---|
| Ambiguous prompt persisted as draft requirement | `REQUIREMENTS` (`REQ-1`, `status: approved`) | `tests/fixtures/schemas/positive.json` (`REQUIREMENTS`) |
| Typed trace graph (goal -> requirement -> artifact -> test -> verification) | `TRACE_GRAPH` | `tests/fixtures/schemas/positive.json` (`TRACE_GRAPH`) |
| Gate 1 human approval of the baselined requirement | `APPROVAL` (v1) | `tests/fixtures/schemas/positive.json` (`APPROVAL`) |
| Frozen baseline + risk classification with dimension-based rationale | `RISK_ASSESSMENT` | `tests/fixtures/schemas/risk_assessment.positive.json` |
| Build artifact + independent test design (see `TRACE_GRAPH` `ART-1`/`TC-1`) | — | `tests/fixtures/schemas/positive.json` (`TRACE_GRAPH`) |
| Typed claims/evidence with state+policy binding | `EVIDENCE_BUNDLE` v2 | `tests/fixtures/schemas/evidence_bundle_v2.positive.json` |
| Independent verification record | `VERIFICATION_RESULT` | `tests/fixtures/schemas/positive.json` (`VERIFICATION_RESULT`) |
| Human Gate 2 approval, scoped and expiring | `APPROVAL` v2 | `tests/fixtures/schemas/approval_v2.positive.json` |
| Gate decision basis (accepted) | `GATE_RECEIPT` | `tests/fixtures/schemas/gate_receipt.positive.json` |
| Release / accepted state | — | Gate Receipt `decision.status: PASS` above is the accepted outcome; see `docs/agile-v-runtime/13_...` N/A here — release itself is out of this repository's scope (no release-execution schema; `release-manager` skill documents the process). |
| Change request after release (a later change) | `GOVERNANCE_CONVERSION` (illustrates a control-level change; a REQ-level change request uses the `CHANGE_LOG.md` format in `agile-v-lifecycle`, which is a Markdown record, not a JSON schema) | `tests/fixtures/schemas/governance_conversion.positive.json` |
| Targeted revalidation after the change | `REVALIDATION_ASSESSMENT` | `tests/fixtures/schemas/revalidation_assessment.positive.json` |
| An exception used along the way (illustrative, not part of the PASS path above) | `EXCEPTION_DECISION` | `tests/fixtures/schemas/exception_decision.positive.json` |

## ID consistency

The legacy fixture set (`REQUIREMENTS`, `TRACE_GRAPH`, `APPROVAL`, `VERIFICATION_RESULT`) shares consistent IDs (`REQ-1`, `ART-1`, `TC-1`, `VER-1`, `BASELINE-1`) because they were authored together as one coherent scenario in `tests/fixtures/schemas/positive.json`. The v2/newer fixtures (`EVIDENCE_BUNDLE` v2, `GATE_RECEIPT`, `APPROVAL` v2, `RISK_ASSESSMENT`, `REVALIDATION_ASSESSMENT`, `GOVERNANCE_CONVERSION`, `EXCEPTION_DECISION`) were authored per-schema in PR-S03–S08 with their own illustrative IDs (`AAV-0042`, `EVD-AAV-0042`, `GATE-1`/`GATE-0001`, `RA-0001`, etc.) and are **not** currently cross-referenced to `REQ-1`/`ART-1`. Unifying every fixture under one literal task ID end-to-end is future work (tracked as a limitation here, not silently implied as already done).

## Aggregate authorization proof

`tests/test_golden_journey.py::test_golden_journey_gate_receipt_and_evidence_bundle_are_jointly_authorized` runs the canonical aggregate evaluator (`contracts/semantics.py::authorize_gate_transition`) against the Gate Receipt and Evidence Bundle v2 stage fixtures together, with real resolvers for the referenced exception, approval, and evidence-adapter records. This is stronger evidence than "each schema/helper behaves individually": it proves the complete decision path admits this journey's known-good state end to end.
