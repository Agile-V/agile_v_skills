"""Contract tests for Gate Receipt and Approval v2 (PR-S04).

A Gate Receipt records why a transition was permitted or denied; an
Approval v2 record is scoped, expiring, bound to an exact artifact/policy,
and distinguishes reusable from single-use authority. Neither substitutes
for the other: approval records authority, Gate Receipt records decision
basis (docs/agile-v-runtime/07_EVIDENCE_ADMISSION_CONTRACT.md, section 2).

Semantic (non-schema) checks are implemented once in contracts/semantics.py
and imported here rather than redefined locally.
"""
from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from contracts import semantics

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "tests" / "fixtures" / "schemas"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validator(name: str):
    jsonschema = pytest.importorskip("jsonschema")
    schema = _load(SCHEMAS / f"{name}.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


# ---------------------------------------------------------------------------
# Gate Receipt
# ---------------------------------------------------------------------------

def test_gate_receipt_schema_is_valid() -> None:
    _validator("GATE_RECEIPT")


def test_gate_receipt_positive_fixture_is_valid() -> None:
    instance = _load(FIXTURES / "gate_receipt.positive.json")
    errors = list(_validator("GATE_RECEIPT").iter_errors(instance))
    assert not errors, [e.message for e in errors]


@pytest.mark.parametrize(
    "case_id",
    [
        "invalid_decision_status", "invalid_independence_class", "missing_claims_block",
        "gate_1_missing_requirement_revision_ref", "waived_without_exception_refs",
    ],
)
def test_gate_receipt_structural_negative_cases(case_id: str) -> None:
    cases = _load(FIXTURES / "gate_receipt.negative.json")
    errors = list(_validator("GATE_RECEIPT").iter_errors(cases[case_id]))
    assert errors, f"{case_id} should have been schema-rejected"


def test_gate_receipt_authority_and_evidence_decision_are_distinct_objects() -> None:
    """approvals[] records authority; claims{required,admitted,rejected,stale}
    records the evidence-based decision basis. Neither field may substitute
    for the other."""
    instance = _load(FIXTURES / "gate_receipt.positive.json")
    receipt = instance["gate_receipt"]
    assert "approvals" in receipt and "claims" in receipt
    assert receipt["approvals"] != receipt["claims"]


def test_gate_receipt_pass_with_rejected_claim_is_semantically_inconsistent() -> None:
    """Schema validation alone cannot catch a PASS decision that coexists with
    a rejected mandatory claim; this must be caught by a semantic consistency
    check, not treated as valid."""
    cases = _load(FIXTURES / "gate_receipt.negative.json")
    instance = cases["pass_with_rejected_claim"]
    errors = list(_validator("GATE_RECEIPT").iter_errors(instance))
    assert not errors, "fixture must be structurally valid to exercise the semantic check"
    assert not semantics.gate_receipt_decision_consistent(instance)


def test_gate_receipt_positive_fixture_decision_is_consistent() -> None:
    instance = _load(FIXTURES / "gate_receipt.positive.json")
    assert semantics.gate_receipt_decision_consistent(instance)


def test_gate_receipt_subject_binding_matches_gate_2() -> None:
    instance = _load(FIXTURES / "gate_receipt.positive.json")
    assert instance["gate_receipt"]["gate"] == "gate_2"
    assert semantics.gate_receipt_subject_binding_matches_gate(instance)


def test_gate_receipt_gate_1_cannot_bind_to_a_baseline_that_does_not_exist_yet() -> None:
    """Gate 1 occurs before requirement baselining; a Gate 1 receipt must
    bind to the requirement revision under review, not a baseline id."""
    cases = _load(FIXTURES / "gate_receipt.negative.json")
    instance = cases["gate_1_missing_requirement_revision_ref"]
    errors = list(_validator("GATE_RECEIPT").iter_errors(instance))
    assert errors, "a gate_1 receipt missing requirement_revision_ref must be schema-rejected"


def test_gate_receipt_valid_gate_1_binds_to_requirement_revision_not_baseline() -> None:
    base = _load(FIXTURES / "gate_receipt.positive.json")
    instance = copy.deepcopy(base)
    receipt = instance["gate_receipt"]
    receipt["gate"] = "gate_1"
    receipt["lifecycle"] = {"from_state": "architect_revisions", "to_state": "gate_1"}
    receipt["subject_state"] = {"requirement_revision_ref": "REQ-0001@2", "subject_digest": "sha256:" + "d" * 64}
    errors = list(_validator("GATE_RECEIPT").iter_errors(instance))
    assert not errors, [e.message for e in errors]
    assert semantics.gate_receipt_subject_binding_matches_gate(instance)


def test_gate_receipt_waived_without_exception_refs_is_schema_rejected() -> None:
    cases = _load(FIXTURES / "gate_receipt.negative.json")
    instance = cases["waived_without_exception_refs"]
    errors = list(_validator("GATE_RECEIPT").iter_errors(instance))
    assert errors, "a WAIVED decision without exception_refs must be schema-rejected"


def test_gate_receipt_valid_waived_decision_lists_exception_refs() -> None:
    base = _load(FIXTURES / "gate_receipt.positive.json")
    instance = copy.deepcopy(base)
    instance["gate_receipt"]["decision"]["status"] = "WAIVED"
    instance["gate_receipt"]["exception_refs"] = ["EXC-0001"]
    errors = list(_validator("GATE_RECEIPT").iter_errors(instance))
    assert not errors, [e.message for e in errors]
    assert semantics.gate_receipt_decision_consistent(instance)


def test_gate_receipt_pass_requires_admitted_covers_required_no_stale_no_open_obligations() -> None:
    """A PASS decision must fail if a required claim is not admitted, if any
    claim is stale, or if a mandatory obligation is still open -- not just
    when claims.rejected is non-empty."""
    base = _load(FIXTURES / "gate_receipt.positive.json")

    unadmitted = copy.deepcopy(base)
    unadmitted["gate_receipt"]["claims"]["required"].append("CLM-9999")
    assert not semantics.gate_receipt_decision_consistent(unadmitted)

    stale = copy.deepcopy(base)
    stale["gate_receipt"]["claims"]["stale"] = ["CLM-1"]
    assert not semantics.gate_receipt_decision_consistent(stale)

    open_obligation = copy.deepcopy(base)
    open_obligation["gate_receipt"]["obligations"]["open"] = ["OBL-9999"]
    assert not semantics.gate_receipt_decision_consistent(open_obligation)

    assert semantics.gate_receipt_decision_consistent(base)


def test_gate_receipt_waived_resolves_to_a_real_scoped_valid_exception() -> None:
    """WAIVED must not be justified by a bare non-empty exception_refs list
    (item 5): each ref must resolve to a real, currently-valid exception
    bound to the same task and targeting one of the receipt's applicable
    claims."""
    base = _load(FIXTURES / "gate_receipt.positive.json")
    instance = copy.deepcopy(base)
    receipt = instance["gate_receipt"]
    receipt["decision"]["status"] = "WAIVED"
    receipt["claims"]["rejected"] = ["CLM-0007"]
    receipt["exception_refs"] = ["EXC-0001"]
    errors = list(_validator("GATE_RECEIPT").iter_errors(instance))
    assert not errors, [e.message for e in errors]

    exception_corpus = {"EXC-0001": _load(FIXTURES / "exception_decision.positive.json")}
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    assert semantics.gate_receipt_waiver_is_justified(instance, resolve_exception=exception_corpus.get, now=now)


def test_gate_receipt_waived_with_unresolvable_exception_ref_is_not_justified() -> None:
    base = _load(FIXTURES / "gate_receipt.positive.json")
    instance = copy.deepcopy(base)
    receipt = instance["gate_receipt"]
    receipt["decision"]["status"] = "WAIVED"
    receipt["claims"]["rejected"] = ["CLM-0007"]
    receipt["exception_refs"] = ["EXC-9999-DOES-NOT-EXIST"]
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    assert not semantics.gate_receipt_waiver_is_justified(instance, resolve_exception=lambda ref: None, now=now)


def test_gate_receipt_waived_exception_targeting_unrelated_claim_is_not_justified() -> None:
    """EXC-0001 targets CLM-0007. A receipt that rejects a different claim
    and cites EXC-0001 must not be justified merely because EXC-0001 itself
    is real and valid."""
    base = _load(FIXTURES / "gate_receipt.positive.json")
    instance = copy.deepcopy(base)
    receipt = instance["gate_receipt"]
    receipt["decision"]["status"] = "WAIVED"
    receipt["claims"]["rejected"] = ["CLM-DIFFERENT"]
    receipt["exception_refs"] = ["EXC-0001"]
    exception_corpus = {"EXC-0001": _load(FIXTURES / "exception_decision.positive.json")}
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    assert not semantics.gate_receipt_waiver_is_justified(instance, resolve_exception=exception_corpus.get, now=now)


def test_gate_receipt_pass_at_gate_2_requires_a_resolvable_valid_human_approval() -> None:
    """gate_1/gate_2 PASS requires a resolvable, currently-valid approval
    bound to the same task/gate -- an empty or unresolvable approvals list
    must not be treated as sufficient (item 7)."""
    instance = _load(FIXTURES / "gate_receipt.positive.json")
    approval_corpus = {"APR-1": _load(FIXTURES / "approval_v2.positive.json")}
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    assert semantics.gate_receipt_has_valid_human_approval(instance, resolve_approval=approval_corpus.get, now=now)


def test_gate_receipt_pass_at_gate_2_with_unresolvable_approval_is_not_justified() -> None:
    instance = copy.deepcopy(_load(FIXTURES / "gate_receipt.positive.json"))
    instance["gate_receipt"]["approvals"] = [{"approval_ref": "APR-9999-DOES-NOT-EXIST"}]
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    assert not semantics.gate_receipt_has_valid_human_approval(instance, resolve_approval=lambda ref: None, now=now)


def test_gate_receipt_stale_approval_bound_to_old_artifact_does_not_authorize_current_receipt() -> None:
    """An approval that is resolvable, currently valid, and for the same
    task/gate must still be rejected if it was bound to a DIFFERENT
    artifact/policy digest than the receipt's current subject_state/policy
    -- the classic stale-approval path (item 2): approve A under P1, then
    the artifact/policy changes to A2/P2, and the old approval must not
    silently authorize the new state."""
    receipt_instance = _load(FIXTURES / "gate_receipt.positive.json")
    stale_approval = copy.deepcopy(_load(FIXTURES / "approval_v2.positive.json"))
    stale_approval["approval"]["binding"]["artifact_digest"] = "sha256:" + "5" * 64  # different from receipt's subject_digest
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    resolver = {"APR-1": stale_approval}.get
    assert not semantics.gate_receipt_has_valid_human_approval(receipt_instance, resolve_approval=resolver, now=now)


def test_gate_receipt_approval_matching_exact_current_state_authorizes() -> None:
    """Sanity check: the same approval, bound correctly to the receipt's
    actual subject_digest/policy_digest/baseline, does authorize."""
    receipt_instance = _load(FIXTURES / "gate_receipt.positive.json")
    approval_instance = _load(FIXTURES / "approval_v2.positive.json")
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    resolver = {"APR-1": approval_instance}.get
    assert semantics.gate_receipt_has_valid_human_approval(receipt_instance, resolve_approval=resolver, now=now)


def test_gate_receipt_waived_coverage_must_include_every_unresolved_claim() -> None:
    """WAIVED must not be justified merely because every CITED exception is
    valid -- every unresolved mandatory item (required-not-admitted,
    rejected, stale, open obligations) must be covered by some cited
    exception. A receipt rejecting CLM-A and CLM-B but citing only an
    exception for CLM-A leaves CLM-B unresolved and must not be WAIVED."""
    base = _load(FIXTURES / "gate_receipt.positive.json")
    instance = copy.deepcopy(base)
    receipt = instance["gate_receipt"]
    receipt["decision"]["status"] = "WAIVED"
    receipt["claims"]["rejected"] = ["CLM-0007", "CLM-UNCOVERED"]
    receipt["exception_refs"] = ["EXC-0001"]  # only covers CLM-0007
    exception_corpus = {"EXC-0001": _load(FIXTURES / "exception_decision.positive.json")}
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    assert not semantics.gate_receipt_waiver_is_justified(instance, resolve_exception=exception_corpus.get, now=now)


def test_gate_receipt_waived_defer_exception_never_authorizes_advancement() -> None:
    """'defer' means 'nothing is currently satisfied, waived, or accepted'
    per 09_EXCEPTION_AND_WAIVER_CONTRACT.md; it must never satisfy the
    waiver resolver even if it is otherwise valid, current, and correctly
    scoped."""
    base = _load(FIXTURES / "gate_receipt.positive.json")
    instance = copy.deepcopy(base)
    receipt = instance["gate_receipt"]
    receipt["decision"]["status"] = "WAIVED"
    receipt["claims"]["rejected"] = ["CLM-0007"]
    receipt["exception_refs"] = ["EXC-DEFER"]

    defer_exception = copy.deepcopy(_load(FIXTURES / "exception_decision.positive.json"))
    defer_exception["exception"]["id"] = "EXC-DEFER"
    defer_exception["exception"]["type"] = "defer"
    defer_exception["exception"]["control_or_claim_ref"] = "CLM-0007"
    resolver = {"EXC-DEFER": defer_exception}.get
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    assert not semantics.gate_receipt_waiver_is_justified(instance, resolve_exception=resolver, now=now)


def test_gate_receipt_waiver_uses_policy_specific_non_waivable_controls() -> None:
    """A policy/control-matrix-specific non-waivable control must be
    enforceable by passing a broader non_waivable_controls set into the
    resolver, not only the hard-coded default."""
    base = _load(FIXTURES / "gate_receipt.positive.json")
    instance = copy.deepcopy(base)
    receipt = instance["gate_receipt"]
    receipt["decision"]["status"] = "WAIVED"
    receipt["claims"]["rejected"] = ["SAFETY-CRITICAL-CHECK"]
    receipt["exception_refs"] = ["EXC-SAFETY"]

    safety_exception = copy.deepcopy(_load(FIXTURES / "exception_decision.positive.json"))
    safety_exception["exception"]["id"] = "EXC-SAFETY"
    safety_exception["exception"]["control_or_claim_ref"] = "SAFETY-CRITICAL-CHECK"
    resolver = {"EXC-SAFETY": safety_exception}.get
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)

    # Not non-waivable under the hardcoded default set:
    assert semantics.gate_receipt_waiver_is_justified(instance, resolve_exception=resolver, now=now)
    # But IS non-waivable once the domain/policy-specific control is supplied:
    assert not semantics.gate_receipt_waiver_is_justified(
        instance, resolve_exception=resolver, now=now,
        non_waivable_controls=semantics.NON_WAIVABLE_CONTROLS | {"SAFETY-CRITICAL-CHECK"},
    )


def test_gate_receipt_independence_below_minimum_for_risk_level_is_insufficient() -> None:
    """An L2 decision requires at least I2 verification independence
    (docs/agile-v-runtime/04_RISK_CLASSIFICATION.md). A receipt recording
    I1 for an L2 risk level must fail even though every other predicate
    passes."""
    instance = copy.deepcopy(_load(FIXTURES / "gate_receipt.positive.json"))
    instance["gate_receipt"]["risk_level"] = "L2"
    instance["gate_receipt"]["verifier"]["independence_class"] = "I1"
    assert not semantics.gate_receipt_independence_is_sufficient(instance)


def test_gate_receipt_independence_meeting_minimum_for_risk_level_is_sufficient() -> None:
    instance = copy.deepcopy(_load(FIXTURES / "gate_receipt.positive.json"))
    instance["gate_receipt"]["risk_level"] = "L2"
    instance["gate_receipt"]["verifier"]["independence_class"] = "I2"
    assert semantics.gate_receipt_independence_is_sufficient(instance)


def test_gate_receipt_explicit_required_independence_override_takes_the_stricter_value() -> None:
    """A regulated profile may require more than the generic risk-level
    table (e.g. I4 for a GxP claim at L2); the explicit override must be
    honored, and the stricter of the two requirements applies."""
    instance = copy.deepcopy(_load(FIXTURES / "gate_receipt.positive.json"))
    instance["gate_receipt"]["risk_level"] = "L2"  # generic minimum: I2
    instance["gate_receipt"]["verifier"]["required_independence_class"] = "I4"  # profile override: stricter
    instance["gate_receipt"]["verifier"]["independence_class"] = "I2"
    assert not semantics.gate_receipt_independence_is_sufficient(instance)
    instance["gate_receipt"]["verifier"]["independence_class"] = "I4"
    assert semantics.gate_receipt_independence_is_sufficient(instance)


def test_gate_receipt_independence_without_any_required_source_does_not_block() -> None:
    instance = _load(FIXTURES / "gate_receipt.positive.json")
    assert "risk_level" not in instance["gate_receipt"]
    assert "required_independence_class" not in instance["gate_receipt"].get("verifier", {})
    assert semantics.gate_receipt_independence_is_sufficient(instance)


# ---------------------------------------------------------------------------
# Canonical aggregate evaluators (item 6)
# ---------------------------------------------------------------------------

def _real_resolvers():
    exception_corpus = {"EXC-0001": _load(FIXTURES / "exception_decision.positive.json")}
    approval_corpus = {"APR-1": _load(FIXTURES / "approval_v2.positive.json")}
    return exception_corpus.get, approval_corpus.get


def test_evaluate_gate_receipt_admits_the_positive_fixture() -> None:
    instance = _load(FIXTURES / "gate_receipt.positive.json")
    resolve_exception, resolve_approval = _real_resolvers()
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    result = semantics.evaluate_gate_receipt(
        instance, resolve_exception=resolve_exception, resolve_approval=resolve_approval, now=now,
    )
    assert result["status"] == "admitted"
    assert result["findings"] == []


def test_evaluate_gate_receipt_rejects_independence_below_minimum_with_reason_code() -> None:
    instance = copy.deepcopy(_load(FIXTURES / "gate_receipt.positive.json"))
    instance["gate_receipt"]["verifier"]["independence_class"] = "I1"
    resolve_exception, resolve_approval = _real_resolvers()
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    result = semantics.evaluate_gate_receipt(
        instance, resolve_exception=resolve_exception, resolve_approval=resolve_approval, now=now, risk_level="L2",
    )
    assert result["status"] == "rejected"
    assert {"code": "INDEPENDENCE_BELOW_MINIMUM"} in result["findings"]


def test_authorize_gate_transition_combines_gate_and_evidence_bundle_results() -> None:
    gate_instance = _load(FIXTURES / "gate_receipt.positive.json")
    bundle_instance = _load(FIXTURES / "evidence_bundle_v2.positive.json")
    resolve_exception, resolve_approval = _real_resolvers()
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    result = semantics.authorize_gate_transition(
        gate_instance, bundle_instance,
        resolve_exception=resolve_exception, resolve_approval=resolve_approval, now=now,
    )
    assert result["status"] == "admitted"

    broken_bundle = copy.deepcopy(bundle_instance)
    broken_bundle["bundle"]["evidence"][0]["state_binding"]["subject_ref"] = "9" * 40
    rejected = semantics.authorize_gate_transition(
        gate_instance, broken_bundle,
        resolve_exception=resolve_exception, resolve_approval=resolve_approval, now=now,
    )
    assert rejected["status"] == "rejected"
    assert {"code": "EVIDENCE_STATE_MISMATCH"} in rejected["findings"]


# ---------------------------------------------------------------------------
# Approval v2
# ---------------------------------------------------------------------------

def test_approval_v1_schema_is_unchanged() -> None:
    v1 = _load(SCHEMAS / "APPROVAL.schema.json")
    assert v1["properties"]["schema_version"]["const"] == "1.0"


def test_approval_v2_schema_is_valid() -> None:
    _validator("APPROVAL.v2")


def test_approval_v2_positive_fixture_is_valid() -> None:
    instance = _load(FIXTURES / "approval_v2.positive.json")
    errors = list(_validator("APPROVAL.v2").iter_errors(instance))
    assert not errors, [e.message for e in errors]


@pytest.mark.parametrize("case_id", ["missing_authority_source", "invalid_decision_enum"])
def test_approval_v2_structural_negative_cases(case_id: str) -> None:
    cases = _load(FIXTURES / "approval_v2.negative.json")
    errors = list(_validator("APPROVAL.v2").iter_errors(cases[case_id]))
    assert errors, f"{case_id} should have been schema-rejected"


def test_approval_v2_expired_approval_cannot_authorize_now() -> None:
    """Expiry is a semantic (time-relative) check: schema validation of an
    ISO date-time string cannot know whether 'now' is past expires_at."""
    cases = _load(FIXTURES / "approval_v2.negative.json")
    instance = cases["expired_semantic"]
    errors = list(_validator("APPROVAL.v2").iter_errors(instance))
    assert not errors, "fixture must be structurally valid to exercise the semantic check"
    assert not semantics.approval_currently_valid(instance, now=datetime(2026, 9, 13, tzinfo=timezone.utc))


def test_approval_v2_positive_fixture_is_currently_valid() -> None:
    instance = _load(FIXTURES / "approval_v2.positive.json")
    assert semantics.approval_currently_valid(instance, now=datetime(2026, 9, 13, tzinfo=timezone.utc))


def test_approval_v2_bound_artifact_cannot_authorize_a_different_artifact() -> None:
    """An approval bound to artifact digest A cannot authorize a release of
    artifact digest B (AV-style rule: approval bound to artifact A cannot
    authorize artifact B)."""
    cases = _load(FIXTURES / "approval_v2.negative.json")
    instance = cases["wrong_artifact_semantic"]
    bound_digest = instance["approval"]["binding"]["artifact_digest"]
    candidate_digest = "sha256:" + "9" * 64
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    assert bound_digest != candidate_digest
    assert not semantics.approval_authorizes_artifact(instance, candidate_digest, now=now)
    assert semantics.approval_authorizes_artifact(instance, bound_digest, now=now)


def test_approval_v2_consumed_single_use_approval_is_no_longer_valid() -> None:
    """usage.reusable: false + usage.consumed_at set means the approval has
    already been used; it must not remain 'valid' merely because it has
    not yet expired (item 8)."""
    base = _load(FIXTURES / "approval_v2.positive.json")
    instance = copy.deepcopy(base)
    instance["approval"]["usage"] = {"reusable": False, "consumed_at": "2026-09-05T00:00:00Z"}
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    assert not semantics.approval_currently_valid(instance, now=now)


def test_approval_v2_unconsumed_single_use_approval_remains_valid() -> None:
    instance = copy.deepcopy(_load(FIXTURES / "approval_v2.positive.json"))
    instance["approval"]["usage"] = {"reusable": False, "consumed_at": None}
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    assert semantics.approval_currently_valid(instance, now=now)


def test_approval_authorizes_checks_full_scope_not_artifact_digest_alone() -> None:
    """A valid, currently-usable approval for the right artifact must still
    fail authorization if the task, gate, policy, baseline, or resource
    scope does not match (item 8)."""
    instance = _load(FIXTURES / "approval_v2.positive.json")
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)
    approval = instance["approval"]

    assert semantics.approval_authorizes(
        instance, now,
        task_id=approval["task_id"], gate_id=approval["gate_id"],
        artifact_digest=approval["binding"]["artifact_digest"],
        policy_digest=approval["binding"]["policy_digest"],
        requirement_baseline_id=approval["binding"]["requirement_baseline_id"],
        resource=approval["scope"]["resources"][0],
    )

    assert not semantics.approval_authorizes(instance, now, task_id="WRONG-TASK")
    assert not semantics.approval_authorizes(instance, now, gate_id="wrong_gate")
    assert not semantics.approval_authorizes(instance, now, policy_digest="sha256:" + "0" * 64)
    assert not semantics.approval_authorizes(instance, now, requirement_baseline_id="WRONG-BASELINE")
    assert not semantics.approval_authorizes(instance, now, resource="ART-WRONG")
