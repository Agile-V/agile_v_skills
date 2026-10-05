"""Builders for evidence bundles bound to the real Evidence Adapter Registry."""
from copy import deepcopy

from admission_support import load
from contracts.semantics import EvidenceAdapterRegistry

REGISTRY = EvidenceAdapterRegistry.from_repository()


def digest(ref):
    return next(e["profile_digest"] for e in REGISTRY.catalog["adapters"]
                if e["adapter_id"] == ref and not e["historical"])


def evidence_item(base, evidence_id, ref, properties, *, tool_version, locators):
    item = deepcopy(base)
    item["evidence_id"] = evidence_id
    item["evidence_type"] = REGISTRY.resolve_adapter(ref)["adapter"]["evidence_type"]
    item["establishes_properties"] = properties
    item["evidence_source"] = {"adapter_ref": ref, "adapter_digest": digest(ref), "locators": locators}
    if tool_version is not None:
        item["evidence_source"]["tool_version"] = tool_version
    return item


def registry_bundle(risk_level="L2"):
    """An L2 requirement-satisfaction bundle: pytest result + CI provenance."""
    record = load("evidence_bundle_v2.positive.json")
    bundle = record["bundle"]
    bundle["risk_level"] = risk_level
    base = bundle["evidence"][0]
    bundle["evidence"] = [
        evidence_item(base, "EVI-1", "EAD-pytest-junit-v1", ["test_result", "state_binding"],
                      tool_version="8.3.5",
                      locators={"report_uri": "artifact://junit.xml",
                                "report_digest": "sha256:" + "3" * 64}),
        evidence_item(base, "EVI-2", "EAD-github-actions-v1", ["provenance"], tool_version=None,
                      locators={"run_url": "https://github.com/o/r/actions/runs/1", "run_id": "1",
                                "head_sha": "c" * 40}),
    ]
    bundle["obligations"] = []
    return record
