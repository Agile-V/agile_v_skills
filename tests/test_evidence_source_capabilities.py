"""Per-source capability boundaries from the implementation plan (AVS-02 section 7).

Each reviewed source profile must keep the plan's "may NOT establish" set,
so that a later edit widening a tool's authority fails review visibly.
"""
import pytest

from registry_support import REGISTRY

MUST_NOT = {
    "EAD-pytest-junit-v1": {"human_authority", "organizational_independence", "intended_use_validation",
                            "regulatory_compliance", "complete_security"},
    "EAD-github-actions-v1": {"semantic_correctness", "human_authority", "requirement_satisfaction_by_itself"},
    "EAD-sonarqube-quality-gate-v1": {"intended_use_validation", "runtime_correctness", "complete_security",
                                      "human_release_authority"},
    "EAD-semgrep-findings-v1": {"absence_of_all_vulnerabilities", "regulatory_compliance", "system_safety",
                                "human_authority"},
    "EAD-sigstore-attestation-v1": {"semantic_correctness", "quality", "safety", "test_sufficiency"},
    "EAD-k8s-aibom-v1": {"verified_model_identity", "regulatory_compliance"},
    "EAD-kicad-erc-v1": {"board_is_safe", "manufacturable", "functional_in_real_hardware", "human_ee_approval"},
    "EAD-kicad-drc-v1": {"board_is_safe", "manufacturable", "functional_in_real_hardware", "human_ee_approval"},
    "EAD-zephyr-twister-v1": {"physical_measurement", "real_hil_success"},
    "EAD-renode-simulation-v1": {"physical_hardware_behavior", "emc", "electrical_safety", "real_hil_success"},
}


def _adapter(ref):
    entry = next(e for e in REGISTRY.catalog["adapters"] if e["adapter_id"] == ref and not e["historical"])
    return REGISTRY.resolve_snapshot(ref, entry["profile_digest"])["adapter"]


@pytest.mark.parametrize("ref, forbidden", sorted(MUST_NOT.items()))
def test_source_keeps_plan_capability_boundary(ref, forbidden):
    adapter = _adapter(ref)
    assert forbidden <= set(adapter["may_not_establish"])
    assert not forbidden & set(adapter["may_establish"])


@pytest.mark.parametrize("ref", sorted(MUST_NOT))
def test_source_declares_limitations_locators_and_scope(ref):
    adapter = _adapter(ref)
    assert adapter["known_limitations"] and adapter["minimum_evidence_locators"]
    assert adapter["source_version_scope"]["supported_versions"]
    assert adapter["owner"] == "Agile-V"


def test_k8s_aibom_does_not_translate_declared_or_inferred_to_verified():
    adapter = _adapter("EAD-k8s-aibom-v1")
    assert "verified_model_identity" not in adapter["may_establish"]
    assert any("never promoted to verified" in item for item in adapter["known_limitations"])
