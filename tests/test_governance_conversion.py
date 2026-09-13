"""Contract tests for Governance Conversion (PR-S07)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "tests" / "fixtures" / "schemas"
CONTRACT = ROOT / "docs" / "agile-v-runtime" / "12_GOVERNANCE_CONVERSION.md"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validator():
    jsonschema = pytest.importorskip("jsonschema")
    schema = _load(SCHEMAS / "GOVERNANCE_CONVERSION.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


def _proposer_is_not_approver(instance: dict) -> bool:
    decision = instance["conversion"]["decision"]
    if decision["status"] not in {"approved", "deployed", "validated"}:
        return True
    proposer = decision.get("proposer_ref")
    authority = decision.get("authority_ref")
    if proposer is None or authority is None:
        return True
    return proposer != authority


def test_contract_doc_exists() -> None:
    assert CONTRACT.exists()


def test_contract_states_agent_cannot_self_activate() -> None:
    text = CONTRACT.read_text(encoding="utf-8").casefold()
    assert "may not make a safety, security, or compliance control effective for its own current task" in text


def test_schema_is_valid() -> None:
    _validator()


def test_positive_fixture_is_valid_and_proposer_differs_from_approver() -> None:
    instance = _load(FIXTURES / "governance_conversion.positive.json")
    errors = list(_validator().iter_errors(instance))
    assert not errors, [e.message for e in errors]
    assert _proposer_is_not_approver(instance)


@pytest.mark.parametrize(
    "case_id", ["approved_without_authority_ref", "invalid_status_enum", "empty_source_findings"],
)
def test_structural_negative_cases(case_id: str) -> None:
    cases = _load(FIXTURES / "governance_conversion.negative.json")
    errors = list(_validator().iter_errors(cases[case_id]))
    assert errors, f"{case_id} should have been schema-rejected"


def test_proposer_cannot_approve_own_conversion() -> None:
    cases = _load(FIXTURES / "governance_conversion.negative.json")
    instance = cases["proposer_is_approver_semantic"]
    errors = list(_validator().iter_errors(instance))
    assert not errors, "fixture must be structurally valid to exercise the semantic check"
    assert not _proposer_is_not_approver(instance)


def test_control_matrix_skill_cross_references_governance_conversion() -> None:
    text = (ROOT / "agile-v-control-matrix" / "SKILL.md").read_text(encoding="utf-8")
    assert "12_GOVERNANCE_CONVERSION.md" in text
