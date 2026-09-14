"""Contract tests for the Golden Journey and Negative Golden Journeys (PR-S11).

Validates that every fixture referenced by the golden-journey manifest still
exists and still validates against its declared schema, and that every
negative-scenario proof reference in the negative manifest resolves to a
real, collectible test function.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pytest

from contracts import semantics
from admission_support import trusted

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "tests" / "fixtures" / "schemas"
GOLDEN_MANIFEST = ROOT / "examples" / "golden-journey" / "manifest.yaml"
NEGATIVE_MANIFEST = ROOT / "examples" / "negative" / "manifest.yaml"


def _yaml(path: Path) -> dict:
    yaml = pytest.importorskip("yaml")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _validator(schema_name: str):
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((SCHEMAS / f"{schema_name}.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


def _load_fixture(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def test_golden_journey_manifest_exists() -> None:
    manifest = _yaml(GOLDEN_MANIFEST)
    assert len(manifest["stages"]) == 11


def test_negative_manifest_exists() -> None:
    manifest = _yaml(NEGATIVE_MANIFEST)
    assert len(manifest["scenarios"]) == 10
    for scenario in manifest["scenarios"]:
        assert scenario["status"] == "tested"
        assert scenario["test_ref"].startswith("tests/test_issue42_trust_closure.py::")


@pytest.mark.parametrize("index", range(11))
def test_golden_journey_stage_fixture_validates(index: int) -> None:
    manifest = _yaml(GOLDEN_MANIFEST)
    stage = manifest["stages"][index]
    record = _load_fixture(stage["fixture"])
    instance = record[stage["key"]] if stage["key"] else record
    errors = list(_validator(stage["schema"]).iter_errors(instance))
    assert not errors, f"{stage['stage']}: {[e.message for e in errors]}"


def test_golden_journey_gate_receipt_and_evidence_bundle_are_jointly_authorized() -> None:
    """Beyond each stage validating individually against its own schema, the
    Gate Receipt and Evidence Bundle v2 stages must jointly pass the
    canonical aggregate evaluator (authorize_gate_transition) -- proving
    the complete decision path admits this journey's known-good state, not
    merely that each schema/helper behaves in isolation."""
    gate_receipt_instance = _load_fixture("tests/fixtures/schemas/gate_receipt.positive.json")
    evidence_bundle_instance = _load_fixture("tests/fixtures/schemas/evidence_bundle_v2.positive.json")
    exception_corpus = {"EXC-0001": _load_fixture("tests/fixtures/schemas/exception_decision.positive.json")}
    approval_corpus = {"APR-1": _load_fixture("tests/fixtures/schemas/approval_v2.positive.json")}
    adapter_corpus = {"EAD-pytest-junit-v1": _load_fixture("tests/fixtures/schemas/evidence_source_profile.positive.json")}
    now = datetime(2026, 9, 13, tzinfo=timezone.utc)

    result = semantics.authorize_gate_transition(
        gate_receipt_instance,
        evidence_bundle_instance,
        resolve_exception=exception_corpus.get,
        resolve_approval=approval_corpus.get,
        **trusted(),
        now=now,
    )
    assert result["status"] == "admitted"
    assert result["findings"] == []


@pytest.mark.parametrize(
    "scenario_id",
    [
        "stale-evidence", "self-approval", "missing-baseline", "forged-human-authorship",
        "out-of-scope-change", "policy-drift", "expired-approval", "unresolved-critical-risk",
        "verifier-contamination", "evolve-goalpost-change",
    ],
)
def test_negative_scenario_proof_resolves_or_is_honestly_unspecified(scenario_id: str) -> None:
    manifest = _yaml(NEGATIVE_MANIFEST)
    scenario = next(s for s in manifest["scenarios"] if s["id"] == scenario_id)
    if scenario["status"] == "specified":
        assert scenario["test_ref"] is None
        return
    assert scenario["status"] == "tested"
    test_ref = scenario["test_ref"]
    path_part, _, func_name = test_ref.partition("::")
    test_path = ROOT / path_part
    assert test_path.exists()
    content = test_path.read_text(encoding="utf-8")
    assert re.search(rf"def {re.escape(func_name)}\(", content), (
        f"{scenario_id}: function '{func_name}' not found in {path_part}"
    )
