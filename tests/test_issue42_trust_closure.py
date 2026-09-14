"""Issue #42 counterexamples exercised through aggregate entrypoints.

Providers here are controlled test doubles, not evidence of live human
authentication or runtime conformance. Every rejection has a valid control.
"""
from copy import deepcopy
from datetime import datetime, timezone

import pytest

from admission_support import adapter, authority, context, load, property_profile, trusted
from contracts import semantics as s

NOW = datetime(2026, 9, 14, tzinfo=timezone.utc)


def evidence(**overrides):
    args = dict(resolve_adapter=adapter, resolve_property_profile=property_profile)
    args.update(overrides)
    return args


def transition(gate=None, bundle=None, **overrides):
    args = dict(**trusted(), resolve_approval=lambda ref: load("approval_v2.positive.json")
                if ref == "APR-1" else None, resolve_exception=lambda ref: None, now=NOW)
    args.update(overrides)
    return s.authorize_gate_transition(
        gate or load("gate_receipt.positive.json"),
        bundle or load("evidence_bundle_v2.positive.json"), **args)


def rejects(result, code):
    assert result["status"] == "rejected", result
    assert code in {f["code"] for f in result["findings"]}, result


def test_positive_transition_has_no_findings():
    assert transition() == {"status": "admitted", "findings": []}


@pytest.mark.parametrize("level", ["L2", "L3", "L4"])
def test_source_resolver_is_mandatory(level):
    bundle = load("evidence_bundle_v2.positive.json")
    bundle["bundle"]["risk_level"] = level
    rejects(s.evaluate_evidence_bundle(bundle), "EVIDENCE_SOURCE_RESOLVER_REQUIRED")


def test_overclaim_never_uses_advisory_fallback_in_aggregate():
    bundle = load("evidence_bundle_v2.negative.json")[
        "overclaimed_property_not_in_adapter_capability_semantic"]
    rejects(s.evaluate_evidence_bundle(bundle), "EVIDENCE_SOURCE_RESOLVER_REQUIRED")
    rejects(transition(resolve_adapter=None), "EVIDENCE_SOURCE_RESOLVER_REQUIRED")


def test_unknown_adapter_identifies_offending_evidence():
    result = s.evaluate_evidence_bundle(load("evidence_bundle_v2.positive.json"),
                                       **evidence(resolve_adapter=lambda ref: None))
    rejects(result, "EVIDENCE_SOURCE_UNRESOLVED")
    finding = next(f for f in result["findings"] if f["code"] == "EVIDENCE_SOURCE_UNRESOLVED")
    assert finding["evidence_ref"] == "EVI-1"
    assert finding["adapter_ref"] == "EAD-pytest-junit-v1"


@pytest.mark.parametrize("change", ["digest", "identity", "type", "missing_digest", "drift"])
def test_immutable_adapter_binding(change):
    bundle = load("evidence_bundle_v2.positive.json")
    profile = load("evidence_source_profile.positive.json")
    code = "EVIDENCE_SOURCE_DIGEST_MISMATCH"
    if change == "digest":
        bundle["bundle"]["evidence"][0]["evidence_source"]["adapter_digest"] = "sha256:" + "0" * 64
    elif change == "missing_digest":
        del bundle["bundle"]["evidence"][0]["evidence_source"]["adapter_digest"]
    elif change == "identity":
        profile["adapter"]["adapter_id"] = "different-adapter"
        code = "EVIDENCE_SOURCE_IDENTITY_MISMATCH"
    elif change == "type":
        profile["adapter"]["evidence_type"] = "physical_measurement"
        code = "EVIDENCE_SOURCE_IDENTITY_MISMATCH"
    else:
        profile["adapter"]["may_establish"].append("new_capability")
    rejects(s.evaluate_evidence_bundle(bundle, **evidence(resolve_adapter=lambda ref: profile)), code)


def test_property_profile_missing_unresolved_or_wrong_scope():
    bundle = load("evidence_bundle_v2.positive.json")
    rejects(s.evaluate_evidence_bundle(bundle, **evidence(resolve_property_profile=None)),
            "EVIDENCE_PROPERTY_RESOLVER_REQUIRED")
    rejects(s.evaluate_evidence_bundle(bundle, **evidence(resolve_property_profile=lambda *args: None)),
            "EVIDENCE_PROPERTY_PROFILE_UNRESOLVED")
    profile = load("evidence_property_profile.positive.json")
    profile["profile"]["risk_level"] = "L4"
    rejects(s.evaluate_evidence_bundle(bundle, **evidence(resolve_property_profile=lambda *args: profile)),
            "EVIDENCE_PROPERTY_PROFILE_MISMATCH")


@pytest.mark.parametrize("level", ["L2", "L3", "L4"])
def test_claim_cannot_understate_profile_requirements(level):
    bundle = load("evidence_bundle_v2.positive.json")
    bundle["bundle"]["risk_level"] = level
    bundle["bundle"]["claims"][0]["required_evidence_properties"] = ["test_result"]
    profile = load("evidence_property_profile.positive.json")
    profile["profile"]["risk_level"] = level
    profile["profile"]["required_properties"].append("physical_measurement")
    rejects(s.evaluate_evidence_bundle(bundle, **evidence(resolve_property_profile=lambda *args: profile)),
            "EVIDENCE_ADMISSION_INCONSISTENT")


def test_local_properties_can_strengthen_but_not_weaken_requirements():
    bundle = load("evidence_bundle_v2.positive.json")
    original = deepcopy(bundle)
    bundle["bundle"]["claims"][0]["required_evidence_properties"].append("extra_check")
    rejects(s.evaluate_evidence_bundle(bundle, **evidence()), "EVIDENCE_ADMISSION_INCONSISTENT")
    assert original == load("evidence_bundle_v2.positive.json")
    assert "extra_check" in bundle["bundle"]["claims"][0]["required_evidence_properties"]


def test_resolver_errors_are_rejected_without_disclosing_provider_data():
    def broken(*args):
        raise RuntimeError("sensitive provider message")
    result = s.evaluate_evidence_bundle(load("evidence_bundle_v2.positive.json"),
                                       **evidence(resolve_adapter=broken))
    rejects(result, "RESOLVER_ERROR")
    assert "sensitive" not in str(result)


def test_forged_human_authorship():
    approval = load("approval_v2.positive.json")
    approval["approval"]["authorship"] = "human"
    approval["approval"]["approver"]["identity"] = "builder-asserted-human"
    rejects(transition(resolve_approval=lambda ref: approval), "HUMAN_AUTHORITY_UNVERIFIED")
    rejects(transition(verify_authority=None), "HUMAN_AUTHORITY_UNVERIFIED")


def test_out_of_scope_change():
    current = context()
    current["resources"].append("ART-OUTSIDE-APPROVED-SCOPE")
    rejects(transition(decision_context=current), "APPROVAL_SCOPE_MISMATCH")
    current = context()
    current["action"] = "deploy"
    rejects(transition(decision_context=current), "APPROVAL_SCOPE_MISMATCH")


def test_unresolved_critical_risk():
    current = context()
    current["critical_risks"] = ["RISK-CRITICAL-1"]
    # The otherwise valid generic release approval cannot disposition it.
    rejects(transition(decision_context=current), "UNRESOLVED_CRITICAL_RISK")


def test_missing_baseline():
    bundle = load("evidence_bundle_v2.positive.json")
    del bundle["bundle"]["baseline"]
    rejects(transition(bundle=bundle), "SCHEMA_INVALID")


def test_stale_evidence():
    bundle = load("evidence_bundle_v2.positive.json")
    bundle["bundle"]["evidence"][0]["state_binding"]["subject_digest"] = "sha256:" + "0" * 64
    rejects(transition(bundle=bundle), "EVIDENCE_STATE_MISMATCH")


def test_policy_drift():
    bundle = load("evidence_bundle_v2.positive.json")
    bundle["bundle"]["evidence"][0]["policy_binding"]["policy_digest"] = "sha256:" + "0" * 64
    rejects(transition(bundle=bundle), "EVIDENCE_POLICY_MISMATCH")


def test_expired_approval():
    rejects(transition(now=datetime(2028, 1, 1, tzinfo=timezone.utc)), "APPROVAL_NOT_JUSTIFIED")


def test_self_approval():
    record = load("approval_v2.positive.json")
    record["approval"]["approver"]["identity"] = "builder"
    rejects(transition(resolve_approval=lambda ref: record), "HUMAN_AUTHORITY_UNVERIFIED")


def test_verifier_contamination():
    gate = load("gate_receipt.positive.json")
    gate["gate_receipt"]["verifier"]["independence_class"] = "I1"
    rejects(transition(gate=gate), "INDEPENDENCE_BELOW_MINIMUM")


def test_evolve_goalpost_change():
    gate = load("gate_receipt.positive.json")
    gate["gate_receipt"]["policy"]["policy_digest"] = "sha256:" + "0" * 64
    rejects(transition(gate=gate), "DECISION_CONTEXT_MISMATCH")


def test_unrelated_bundle_cannot_support_gate():
    bundle = load("evidence_bundle_v2.positive.json")
    bundle["bundle"]["task_id"] = "OTHER-TASK"
    rejects(transition(bundle=bundle), "GATE_EVIDENCE_BINDING_MISMATCH")


def test_missing_context_and_missing_reuse_coverage_fail_closed():
    rejects(transition(decision_context=None), "DECISION_CONTEXT_REQUIRED")
    assert not s.revalidation_reuse_eligible({"result": "UNCHANGED"})
