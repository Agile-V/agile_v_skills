"""Contract tests for the skills<->runtime compatibility registry (PR-S09).

The version registry must not silently drift from the schemas it describes,
and the compatibility declaration must not overclaim runtime support that
has not actually been verified.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
VERSIONS = ROOT / "contracts" / "versions.yaml"
COMPAT = ROOT / "contracts" / "AGILE_V_RUNTIME_COMPATIBILITY.yaml"

# Registry key -> schema file name whose schema_version const must match.
SCHEMA_KEY_MAP = {
    "requirements": "REQUIREMENTS",
    "trace_graph": "TRACE_GRAPH",
    "approval": "APPROVAL",
    "approval_v2": "APPROVAL.v2",
    "evidence_bundle": "EVIDENCE_BUNDLE",
    "evidence_bundle_v2": "EVIDENCE_BUNDLE.v2",
    "gate_receipt": "GATE_RECEIPT",
    "exception_decision": "EXCEPTION_DECISION",
    "revalidation_assessment": "REVALIDATION_ASSESSMENT",
    "risk_assessment": "RISK_ASSESSMENT",
}


def _yaml(path: Path) -> dict:
    yaml = pytest.importorskip("yaml")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _schema_version_const(schema_name: str) -> str:
    schema = json.loads((SCHEMAS / f"{schema_name}.schema.json").read_text(encoding="utf-8"))
    return schema["properties"]["schema_version"]["const"]


def test_versions_registry_exists_and_parses() -> None:
    registry = _yaml(VERSIONS)
    assert "contracts" in registry


@pytest.mark.parametrize("registry_key, schema_name", list(SCHEMA_KEY_MAP.items()))
def test_registry_version_matches_schema_const(registry_key: str, schema_name: str) -> None:
    registry = _yaml(VERSIONS)
    assert registry["contracts"][registry_key] == _schema_version_const(schema_name), (
        f"contracts/versions.yaml '{registry_key}' has drifted from "
        f"schemas/{schema_name}.schema.json schema_version"
    )


def test_compatibility_file_exists_and_parses() -> None:
    compat = _yaml(COMPAT)
    assert "skills_contract" in compat
    assert "compatible_runtimes" in compat


def test_compatibility_declares_evidence_bundle_v2_and_gate_receipt() -> None:
    compat = _yaml(COMPAT)
    contract = compat["skills_contract"]
    assert contract["evidence_bundle"] == "2.0"
    assert contract["gate_receipt"] == "1.0"


def test_unverified_runtime_capability_is_not_reported_as_confirmed() -> None:
    """A runtime with verification_status != 'verified' must not claim a
    minimum_version, and every required_capability must be understood as
    unconfirmed rather than silently treated as supported."""
    compat = _yaml(COMPAT)
    for name, runtime in compat["compatible_runtimes"].items():
        if runtime.get("verification_status") != "verified":
            assert runtime.get("minimum_version") is None, (
                f"{name}: unverified runtime must not declare a minimum_version"
            )


def test_generated_copy_provenance_fields_declared() -> None:
    compat = _yaml(COMPAT)
    fields = compat["generated_copy_provenance_fields"]
    assert {"source_repository", "source_commit", "skill_contract_version"} <= set(fields)
