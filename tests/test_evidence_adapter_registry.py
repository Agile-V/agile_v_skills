"""Evidence Adapter Registry contract tests (AVS-02).

docs/agile-v-runtime/15_EVIDENCE_ADAPTER_REGISTRY.md. Positive path plus the
adversarial cases the plan requires: overclaims, digest/content drift,
type mismatch, missing/superseded profiles, missing locators, unsupported
tool versions and producer-supplied profiles.
"""
from __future__ import annotations

from copy import deepcopy

import pytest
import yaml

from contracts.semantics import (EvidenceAdapterRegistry, RegistryIntegrityError,
                                 evaluate_evidence_bundle_against_registry, profile_digest,
                                 version_in_scope)
from registry_support import REGISTRY, registry_bundle
from tools import build_evidence_adapter_catalog as builder
from tools._common import ROOT, dump_json


def codes(result):
    return {f["code"] for f in result["findings"]}


def evaluate(record, **kwargs):
    return evaluate_evidence_bundle_against_registry(record, REGISTRY, **kwargs)


# --- registry shape ---------------------------------------------------------

def test_catalog_is_current_and_deterministic():
    catalog, errors = builder.build()
    assert not errors
    assert dump_json(catalog) == (ROOT / "catalog/evidence-adapters.json").read_text()
    assert dump_json(builder.build()[0]) == dump_json(catalog)


def test_registry_meets_minimum_coverage():
    catalog = REGISTRY.catalog
    active = [a for a in catalog["adapters"] if not a["historical"]]
    assert len(active) >= 10
    assert len(catalog["property_profiles"]) >= 5
    required = {"EAD-pytest-junit-v1", "EAD-github-actions-v1", "EAD-sonarqube-quality-gate-v1",
                "EAD-semgrep-findings-v1", "EAD-sigstore-attestation-v1", "EAD-k8s-aibom-v1",
                "EAD-kicad-erc-v1", "EAD-kicad-drc-v1", "EAD-zephyr-twister-v1", "EAD-renode-simulation-v1"}
    assert required <= {a["adapter_id"] for a in active}


@pytest.mark.parametrize("entry", REGISTRY.catalog["adapters"], ids=lambda e: e["adapter_id"])
def test_no_source_profile_may_establish_authority_or_validation(entry):
    adapter = REGISTRY.resolve_snapshot(entry["adapter_id"], entry["profile_digest"])["adapter"]
    forbidden = {"human_authority", "organizational_independence", "intended_use_validation",
                 "regulatory_compliance", "independent_verification"}
    assert not forbidden & set(adapter["may_establish"])
    assert forbidden <= set(adapter["may_not_establish"])


def test_registry_rejects_file_drift_against_catalog():
    catalog = REGISTRY.catalog
    records = {e["profile_path"]: yaml.safe_load((ROOT / e["profile_path"]).read_text())
               for e in catalog["adapters"] + catalog["property_profiles"]}
    path = "profiles/evidence-sources/pytest-junit-v1.yaml"
    records[path]["adapter"]["may_establish"].append("human_authority")
    with pytest.raises(RegistryIntegrityError):
        EvidenceAdapterRegistry(catalog, records)


def test_missing_registry_file_fails_closed(tmp_path):
    (tmp_path / "catalog").mkdir()
    (tmp_path / "catalog/evidence-adapters.json").write_text(dump_json(REGISTRY.catalog))
    with pytest.raises(RegistryIntegrityError):
        EvidenceAdapterRegistry.from_repository(tmp_path)


# --- positive path ----------------------------------------------------------

def test_registry_bound_bundle_is_admitted():
    result = evaluate(registry_bundle())
    assert result == {"status": "admitted", "findings": []}


def test_pytest_alone_does_not_satisfy_l2_provenance():
    record = registry_bundle()
    record["bundle"]["evidence"].pop()
    assert "EVIDENCE_ADMISSION_INCONSISTENT" in codes(evaluate(record))


# --- adversarial cases ------------------------------------------------------

def test_source_overclaims_human_authority():
    record = registry_bundle()
    record["bundle"]["evidence"][0]["establishes_properties"].append("human_authority")
    assert "EVIDENCE_PROPERTY_OVERCLAIM" in codes(evaluate(record))


def test_adapter_claims_property_listed_in_may_not_establish():
    record = registry_bundle()
    record["bundle"]["evidence"][0]["establishes_properties"].append("provenance")  # pytest may_not
    assert "EVIDENCE_PROPERTY_OVERCLAIM" in codes(evaluate(record))


def test_profile_digest_changed():
    record = registry_bundle()
    record["bundle"]["evidence"][0]["evidence_source"]["adapter_digest"] = "sha256:" + "0" * 64
    assert "EVIDENCE_SOURCE_DIGEST_MISMATCH" in codes(evaluate(record))


def test_same_profile_id_with_changed_content_is_not_the_registered_profile():
    record = registry_bundle()
    forged = REGISTRY.resolve_adapter("EAD-pytest-junit-v1")
    forged["adapter"]["may_establish"].append("provenance")
    forged["adapter"]["may_not_establish"].remove("provenance")
    record["bundle"]["evidence"][0]["evidence_source"]["adapter_digest"] = profile_digest(forged)
    record["bundle"]["evidence"][0]["establishes_properties"].append("provenance")
    assert evaluate(record)["status"] == "rejected"
    assert "EVIDENCE_SOURCE_DIGEST_MISMATCH" in codes(evaluate(record))


def test_evidence_type_does_not_match_source_profile():
    record = registry_bundle()
    record["bundle"]["evidence"][0]["evidence_type"] = "static_analysis"
    assert "EVIDENCE_SOURCE_IDENTITY_MISMATCH" in codes(evaluate(record))


def test_source_profile_missing_from_registry():
    record = registry_bundle()
    record["bundle"]["evidence"][0]["evidence_source"]["adapter_ref"] = "EAD-unknown-tool-v1"
    assert "EVIDENCE_SOURCE_UNRESOLVED" in codes(evaluate(record))


def test_experimental_profile_is_not_admissible_for_current_decisions():
    assert REGISTRY.resolve_adapter("EAD-k8s-aibom-v1") is None


def test_required_evidence_locator_absent():
    record = registry_bundle()
    del record["bundle"]["evidence"][0]["evidence_source"]["locators"]["report_digest"]
    assert "EVIDENCE_LOCATOR_MISSING" in codes(evaluate(record))


@pytest.mark.parametrize("version, code", [("6.2.5", "EVIDENCE_SOURCE_TOOL_VERSION_UNSUPPORTED"),
                                           ("10.0", "EVIDENCE_SOURCE_TOOL_VERSION_UNSUPPORTED"),
                                           ("banana", "EVIDENCE_SOURCE_TOOL_VERSION_UNSUPPORTED"),
                                           (None, "EVIDENCE_SOURCE_TOOL_VERSION_UNKNOWN")])
def test_tool_version_outside_supported_range(version, code):
    record = registry_bundle()
    source = record["bundle"]["evidence"][0]["evidence_source"]
    source.pop("tool_version")
    if version is not None:
        source["tool_version"] = version
    assert code in codes(evaluate(record))


def test_untrusted_producer_supplies_its_own_profile():
    record = registry_bundle()
    own = REGISTRY.resolve_adapter("EAD-pytest-junit-v1")
    own["adapter"]["may_establish"].append("human_authority")
    record["bundle"]["evidence"][0]["evidence_source"]["profile"] = own
    record["bundle"]["evidence"][0]["establishes_properties"].append("human_authority")
    result = evaluate(record)
    assert {"EVIDENCE_SOURCE_SELF_SUPPLIED_PROFILE", "EVIDENCE_PROPERTY_OVERCLAIM"} <= codes(result)


def test_renode_simulation_cannot_satisfy_firmware_hil():
    record = registry_bundle("L4")
    bundle = record["bundle"]
    bundle["claims"][0]["claim_type"] = "firmware_hil"
    bundle["claims"][0]["required_evidence_properties"] = ["state_binding"]
    item = bundle["evidence"][0]
    item["evidence_type"] = "simulation_result"
    item["establishes_properties"] = ["simulation_execution", "state_binding"]
    item["evidence_source"] = {"adapter_ref": "EAD-renode-simulation-v1",
                               "adapter_digest": REGISTRY.catalog and next(
                                   e["profile_digest"] for e in REGISTRY.catalog["adapters"]
                                   if e["adapter_id"] == "EAD-renode-simulation-v1"),
                               "tool_version": "1.15", "locators": {
                                   "results_digest": "sha256:" + "4" * 64,
                                   "platform_description_digest": "sha256:" + "5" * 64,
                                   "trace_uri": "artifact://trace"}}
    assert "EVIDENCE_ADMISSION_INCONSISTENT" in codes(evaluate(record))


# --- historical resolution --------------------------------------------------

def _registry_with_superseded_pytest():
    """Registry where the pytest profile was revised; the old one is history."""
    catalog = REGISTRY.catalog
    records = {e["profile_path"]: yaml.safe_load((ROOT / e["profile_path"]).read_text())
               for e in catalog["adapters"] + catalog["property_profiles"]}
    old_path = "profiles/evidence-sources/pytest-junit-v1.yaml"
    old = records[old_path]
    new = deepcopy(old)
    new["adapter"]["known_limitations"].append("Revised limitation text added in a later review.")
    new["adapter"]["supersedes"] = profile_digest(old)
    hist_path = "profiles/evidence-sources/history/pytest-junit-v1@old.yaml"
    records[hist_path] = old
    records[old_path] = new
    entry = next(e for e in catalog["adapters"] if e["adapter_id"] == "EAD-pytest-junit-v1")
    hist_entry = dict(entry, profile_path=hist_path, historical=True)
    entry["profile_digest"] = profile_digest(new)
    catalog["adapters"].append(hist_entry)
    return EvidenceAdapterRegistry(catalog, records)


def test_superseded_profile_used_without_historical_resolution_is_rejected():
    registry = _registry_with_superseded_pytest()
    result = evaluate_evidence_bundle_against_registry(registry_bundle(), registry)
    assert {"EVIDENCE_SOURCE_SUPERSEDED", "EVIDENCE_SOURCE_DIGEST_MISMATCH"} <= codes(result)


def test_historical_resolution_by_exact_digest():
    registry = _registry_with_superseded_pytest()
    result = evaluate_evidence_bundle_against_registry(registry_bundle(), registry, historical=True)
    assert result["status"] == "admitted"


def test_historical_resolution_rejects_unknown_digest():
    registry = _registry_with_superseded_pytest()
    record = registry_bundle()
    record["bundle"]["evidence"][0]["evidence_source"]["adapter_digest"] = "sha256:" + "9" * 64
    result = evaluate_evidence_bundle_against_registry(record, registry, historical=True)
    assert "EVIDENCE_SOURCE_UNRESOLVED" in codes(result)


@pytest.mark.parametrize("version, spec, expected", [
    ("8.3.5", ">=7.0,<10.0", True), ("7", ">=7.0,<10.0", True), ("10.0.0", ">=7.0,<10.0", False),
    ("x", "*", True), (None, ">=1.0", False), ("1.0.0", "==1", True), ("2", ">1.9", True)])
def test_version_in_scope(version, spec, expected):
    assert version_in_scope(version, spec) is expected
