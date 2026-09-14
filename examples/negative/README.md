# Negative Golden Journeys

> Each scenario below must be blocked, and for a reason the repository can point to. As in `conformance/README.md`, `status: tested` means a deterministic test in this repository's own suite proves the rejection; `status: specified` means the rule exists in a skill/contract document but has no dedicated executable fixture yet — it is not fabricated as tested.

| Scenario | Expected | Status | Proof |
|---|---|---|---|
| `stale-evidence` | Evidence bound to a superseded commit is rejected/flagged, not silently reused. | tested | `tests/test_evidence_bundle_v2.py::test_v2_wrong_commit_passes_schema_but_fails_semantic_state_binding_check` |
| `self-approval` | An agent cannot approve its own gate/conversion. | tested | `tests/test_governance_conversion.py::test_proposer_cannot_approve_own_conversion` |
| `missing-baseline` | A bundle/approval missing its required baseline reference is schema-rejected. | tested | `tests/test_schemas.py::test_schema_fixtures[negative-False]` (`EVIDENCE_BUNDLE` case in `tests/fixtures/schemas/negative.json` omits `baseline_id` along with other required fields) |
| `forged-human-authorship` | An `authorship: human` field is an assertion, not proof, and must bind to durable approval evidence. | specified | `agile-v-human-oversight/SKILL.md` "Human-origin attestation" section; no dedicated schema/test yet |
| `out-of-scope-change` | An agent that discovers an adjacent issue logs it (`OBS-XXXX`) and does not modify out-of-scope files. | specified | `agile-v-core/SKILL.md` SCOPE-V rule 6 ("No Scope Creep"); no dedicated schema/test yet |
| `policy-drift` | Evidence produced under policy P1 is not automatically eligible for reuse once the active policy is P2. | tested | `tests/test_change_aware_revalidation.py::test_unknown_result_is_never_reuse_eligible_even_at_l3` (policy is one of the declared dependency `kind`s) |
| `expired-approval` | An expired approval cannot authorize a current transition. | tested | `tests/test_gate_receipt_and_approval_v2.py::test_approval_v2_expired_approval_cannot_authorize_now` |
| `unresolved-critical-risk` | A Critical residual risk with no documented, scoped, owned exception blocks the gate. | specified | `agile-v-compliance/SKILL.md` Risk Management section ("Critical risks require Human resolution or documented acceptance before Gate 2"); no dedicated schema/test yet |
| `verifier-contamination` | A verifier that received builder reasoning/chat has a degraded independence class, not `I2`+. | tested | `tests/test_independence_classes.py::test_fresh_context_is_not_organizational_assurance` |
| `evolve-goalpost-change` | `Evolve` cannot weaken the active cycle's acceptance criteria before `Verify` runs. | tested | `tests/test_evidence_admission.py::test_no_skill_instructs_evolve_to_edit_active_criteria` |

See `manifest.yaml` for the machine-readable form; `tests/test_golden_journey.py` validates that every `tested` row's proof reference actually resolves to a real, collectible test, and that every `specified` row has no fabricated test reference.
