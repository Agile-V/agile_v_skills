"""Contract tests for the Exception and Waiver Contract (PR-S05).

Distinguishes waiver, concession, dispensation, residual-risk acceptance,
and defer; enforces expiry, non-waivable meta-controls, and the rule that
WAIVED must never mean "missing evidence, continue anyway."

Semantic (non-schema) checks are implemented once in contracts/semantics.py
and imported here rather than redefined locally.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pytest

from contracts import semantics

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "tests" / "fixtures" / "schemas"
CONTRACT = ROOT / "docs" / "agile-v-runtime" / "09_EXCEPTION_AND_WAIVER_CONTRACT.md"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def _validator():
    jsonschema = pytest.importorskip("jsonschema")
    schema = _load(SCHEMAS / "EXCEPTION_DECISION.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


def test_contract_doc_exists_and_defines_five_types() -> None:
    text = _normalized(CONTRACT.read_text(encoding="utf-8"))
    for exc_type in ("waiver", "concession", "dispensation", "residual risk acceptance", "defer"):
        assert exc_type in text


def test_contract_states_waived_is_not_missing_evidence_continue() -> None:
    text = _normalized(CONTRACT.read_text(encoding="utf-8"))
    assert "waived never means missing evidence continue anyway" in text


def test_schema_is_valid() -> None:
    _validator()


def test_positive_fixture_is_valid() -> None:
    instance = _load(FIXTURES / "exception_decision.positive.json")
    errors = list(_validator().iter_errors(instance))
    assert not errors, [e.message for e in errors]


@pytest.mark.parametrize(
    "case_id", ["missing_expiry", "dispensation_missing_monitoring", "invalid_type_enum"],
)
def test_structural_negative_cases(case_id: str) -> None:
    cases = _load(FIXTURES / "exception_decision.negative.json")
    errors = list(_validator().iter_errors(cases[case_id]))
    assert errors, f"{case_id} should have been schema-rejected"


def test_nonwaivable_control_cannot_be_waived_even_if_structurally_valid() -> None:
    cases = _load(FIXTURES / "exception_decision.negative.json")
    instance = cases["non_waivable_control_semantic"]
    errors = list(_validator().iter_errors(instance))
    assert not errors, "fixture must be structurally valid to exercise the semantic check"
    assert not semantics.exception_currently_valid(instance, now=datetime(2026, 9, 13, tzinfo=timezone.utc))


def test_expired_exception_is_invalid_despite_being_structurally_valid() -> None:
    cases = _load(FIXTURES / "exception_decision.negative.json")
    instance = cases["expired_semantic"]
    errors = list(_validator().iter_errors(instance))
    assert not errors
    assert not semantics.exception_currently_valid(instance, now=datetime(2026, 9, 13, tzinfo=timezone.utc))


def test_positive_fixture_is_currently_valid() -> None:
    instance = _load(FIXTURES / "exception_decision.positive.json")
    assert semantics.exception_currently_valid(instance, now=datetime(2026, 9, 13, tzinfo=timezone.utc))


def test_red_team_disposition_model_cross_references_exception_contract() -> None:
    verifier = _normalized((ROOT / "red-team-verifier" / "SKILL.md").read_text(encoding="utf-8"))
    assert "09 exception and waiver contract" in verifier or "09_exception_and_waiver_contract" in verifier


def test_compliance_risk_management_cross_references_exception_contract() -> None:
    compliance = (ROOT / "agile-v-compliance" / "SKILL.md").read_text(encoding="utf-8")
    assert "09_EXCEPTION_AND_WAIVER_CONTRACT.md" in compliance
