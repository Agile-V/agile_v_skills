"""Graduation evidence for agile-v-aibom (draft -> candidate, AVS-09).

Negative tests and two end-to-end scenarios. These are reference-semantics
results; they do not graduate the skill. Graduation requires the reviewer
decision recorded under .agile-v/graduation/agile-v-aibom/.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from contracts.semantics import (EvidenceAdapterRegistry, ai_bom_diff, evaluate_ai_run_manifest,
                                 evaluate_revalidation_reuse, reconcile_ai_inventory)
from tools.aibom_to_cyclonedx import to_cyclonedx

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = EvidenceAdapterRegistry.from_repository()


def manifest():
    return yaml.safe_load((ROOT / "tests/aibom/valid_ai_run_manifest_v02.yaml").read_text())


def codes(result):
    return {f["code"] for f in result["findings"]}


def all_snapshots(ref):
    entry = next(e for e in REGISTRY.catalog["adapters"] if e["adapter_id"] == ref)
    return REGISTRY.resolve_snapshot(ref, entry["profile_digest"])


def test_valid_manifest_admitted():
    assert evaluate_ai_run_manifest(manifest()) == {"status": "admitted", "findings": []}


# --- negative tests -----------------------------------------------------------

def test_declared_model_presented_as_verified():
    m = manifest()
    m["models"][0]["confidence"] = "verified"
    assert "AIBOM_VERIFIED_WITHOUT_TRUSTED_SOURCE" in codes(evaluate_ai_run_manifest(m))


def test_verified_with_observed_but_unverifying_source_still_rejected():
    m = manifest()
    m["models"][0].update(confidence="verified", evidence_locator="EAD-otel-genai-trace-v1#trace/4bf9")
    result = evaluate_ai_run_manifest(m, resolve_source=all_snapshots)
    assert "AIBOM_VERIFIED_WITHOUT_TRUSTED_SOURCE" in codes(result)


def test_unknown_runtime_not_silently_accepted_at_l3():
    m = yaml.safe_load((ROOT / "tests/aibom/invalid_unresolved_l3_runtime.yaml").read_text())
    result = evaluate_ai_run_manifest(m)
    assert result["status"] == "rejected"
    assert "AIBOM_UNRESOLVED_MATERIAL_IDENTITY" in codes(result) or "SCHEMA_INVALID" in codes(result)


def test_unresolved_runtime_at_l3_rejected_semantically():
    m = manifest()
    m["risk"]["agile_v_risk_level"] = "L3"
    m["agent_runtime"] = {"agent_name": "a", "agent_framework": "f", "execution_environment": "unknown",
                          "confidence": "unresolved"}
    assert "AIBOM_UNRESOLVED_MATERIAL_IDENTITY" in codes(evaluate_ai_run_manifest(m))


def test_model_change_triggers_revalidation_of_dependent_evidence():
    before, after = manifest(), manifest()
    after["models"][0]["model_version"] = "2025-10-01"
    changes = ai_bom_diff(before, after)
    assert changes == [{"kind": "model", "ref": "model:test-model", "change": "modified", "ai_component": "model"}]


def test_skill_or_plugin_version_change_produces_influence_diff():
    before, after = manifest(), manifest()
    before["agile_v_skills"] = [{"skill": "build-agent", "version": "2.1", "source": "plugin", "confidence": "declared"}]
    after["agile_v_skills"] = [{"skill": "build-agent", "version": "2.2", "source": "plugin", "confidence": "declared"}]
    assert ai_bom_diff(before, after)[0]["ref"] == "skill:build-agent"


def test_confidence_flip_is_never_silent():
    before, after = manifest(), manifest()
    after["models"][0]["confidence"] = "verified"
    assert ai_bom_diff(before, after)[0]["change"] == "confidence_changed"


@pytest.mark.parametrize("text", ["<thinking>first I will</thinking>", "Chain-of-thought: step 1"])
def test_hidden_cot_captured(text):
    m = manifest()
    m["summary"]["verifier_notes"] = text
    assert "AIBOM_HIDDEN_REASONING_CAPTURED" in codes(evaluate_ai_run_manifest(m))
    m = manifest()
    m["security_and_privacy"]["hidden_chain_of_thought_excluded"] = False
    assert "AIBOM_HIDDEN_REASONING_CAPTURED" in codes(evaluate_ai_run_manifest(m))


@pytest.mark.parametrize("secret", ["ghp_" + "a" * 36, "AKIA" + "B" * 16, "sk-" + "c" * 32,
                                    "-----BEGIN RSA PRIVATE KEY-----"])
def test_secret_captured_in_manifest(secret):
    m = manifest()
    m["summary"]["verifier_notes"] = f"token={secret}"
    assert "AIBOM_SECRET_CAPTURED" in codes(evaluate_ai_run_manifest(m))


def test_cyclonedx_translation_preserves_confidence_and_is_a_view():
    m = manifest()
    m["models"][0]["confidence"] = "inferred"
    bom = to_cyclonedx(m)
    props = {p["name"]: p["value"] for p in bom["components"][0]["properties"]}
    assert props["agile-v:confidence"] == "inferred"
    assert {"name": "agile-v:export_kind", "value": "view-not-normative"} in bom["metadata"]["properties"]
    assert "verified" not in str(bom)


# --- E2E scenario 1: model A -> model B, exact affected evidence ----------------

def _assessment(changes, evaluations):
    return {"schema_version": "1.2", "compatibility": "additive", "migration": "none", "fixture_owner": "tests",
            "assessment": {"id": "REVAL-AIBOM-1", "task_id": "AAV-0001", "risk_level": "L2",
                           "evaluated_at": "2026-10-01T00:00:00Z",
                           "changed_refs": [{"kind": c["kind"], "ref": c["ref"]} for c in changes],
                           "evaluations": evaluations, "coverage": "complete",
                           "conservative_fallback_applied": False}}


def test_e2e_scenario_1_model_change_revalidates_only_dependent_evidence():
    run_a, run_b = manifest(), manifest()
    run_b["models"][0].update(model_id="test-model-2", model_version="B")
    changes = ai_bom_diff(run_a, run_b)
    assert {c["kind"] for c in changes} == {"model"}
    code_review = {"evidence_id": "EVI-AI-REVIEW", "invalidation_dependencies": [{"kind": "model", "ref": "model"},
                                                                                {"kind": "source", "ref": "s"}]}
    unit_tests = {"evidence_id": "EVI-UNIT", "invalidation_dependencies": [{"kind": "source", "ref": "s"}]}
    assessment = _assessment(changes, [
        {"evidence_ref": "EVI-AI-REVIEW", "claim_refs": ["CLM-1"], "result": "REVALIDATION_REQUIRED"},
        {"evidence_ref": "EVI-UNIT", "claim_refs": ["CLM-2"], "result": "UNCHANGED"}])
    assert evaluate_revalidation_reuse(assessment, code_review)["status"] == "rejected"
    assert evaluate_revalidation_reuse(assessment, unit_tests)["status"] == "admitted"
    # An UNCHANGED verdict for model-dependent evidence is not trusted.
    lying = deepcopy(assessment)
    lying["assessment"]["evaluations"][0]["result"] = "UNCHANGED"
    assert "REVALIDATION_DEPENDENCY_CONFLICT" in codes(evaluate_revalidation_reuse(lying, code_review))


# --- E2E scenario 2: declared manifest vs observed k8s-aibom ----------------------

def test_e2e_scenario_2_declared_vs_observed_inventory_keeps_confidence():
    declared = manifest()["models"]
    observed = [{"name": "test-model", "model_id": "test-model-1", "confidence": "inferred"},
                {"name": "shadow-embedder", "model_id": "embed-x", "confidence": "unresolved"}]
    findings = reconcile_ai_inventory(declared, observed)
    by_model = {f["model_id"]: f for f in findings}
    assert by_model["test-model-1"] == {"code": "AIBOM_OBSERVED", "model_id": "test-model-1",
                                        "declared_confidence": "declared", "observed_confidence": "inferred"}
    assert by_model["embed-x"]["code"] == "AIBOM_OBSERVED_NOT_DECLARED"
    assert by_model["embed-x"]["observed_confidence"] == "unresolved"
    assert all(f.get("observed_confidence") != "verified" for f in findings)
    # The observed source is experimental: it cannot currently admit evidence.
    assert REGISTRY.resolve_adapter("EAD-k8s-aibom-v1") is None
