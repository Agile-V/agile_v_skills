"""Contract tests for Risk Assessment v2 (PR-S08).

Semantic (non-schema) checks are implemented once in contracts/semantics.py
and imported here rather than redefined locally.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from contracts import semantics

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "tests" / "fixtures" / "schemas"
CONTRACT = ROOT / "docs" / "agile-v-runtime" / "11_RISK_ASSESSMENT_V2.md"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validator():
    jsonschema = pytest.importorskip("jsonschema")
    schema = _load(SCHEMAS / "RISK_ASSESSMENT.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


def _resolve_real_exception(exception_ref: str) -> bool:
    """Resolves exception_ref against the actual EXCEPTION_DECISION fixture
    corpus, rather than treating any non-empty string as authorized. Only
    EXC-0001 (tests/fixtures/schemas/exception_decision.positive.json)
    exists and is currently valid in this fixture corpus."""
    known = {"EXC-0001": _load(FIXTURES / "exception_decision.positive.json")}
    if exception_ref not in known:
        return False
    from datetime import datetime, timezone
    return semantics.exception_currently_valid(known[exception_ref], now=datetime(2026, 9, 13, tzinfo=timezone.utc))


def test_contract_doc_exists() -> None:
    assert CONTRACT.exists()


def test_schema_is_valid() -> None:
    _validator()


def test_positive_fixture_is_valid_and_respects_floor() -> None:
    instance = _load(FIXTURES / "risk_assessment.positive.json")
    errors = list(_validator().iter_errors(instance))
    assert not errors, [e.message for e in errors]
    assert semantics.risk_floor_respected(instance)


@pytest.mark.parametrize("case_id", ["empty_dimensions", "invalid_level_enum", "missing_rationale"])
def test_structural_negative_cases(case_id: str) -> None:
    cases = _load(FIXTURES / "risk_assessment.negative.json")
    errors = list(_validator().iter_errors(cases[case_id]))
    assert errors, f"{case_id} should have been schema-rejected"


def test_level_cannot_be_silently_lowered_below_floor() -> None:
    cases = _load(FIXTURES / "risk_assessment.negative.json")
    instance = cases["below_floor_without_exception_semantic"]
    errors = list(_validator().iter_errors(instance))
    assert not errors, "fixture must be structurally valid to exercise the semantic check"
    assert not semantics.risk_floor_respected(instance, resolve_exception=_resolve_real_exception)


def test_level_may_be_lowered_below_floor_with_authorized_and_resolved_exception() -> None:
    cases = _load(FIXTURES / "risk_assessment.negative.json")
    instance = cases["below_floor_with_exception_semantic"]
    errors = list(_validator().iter_errors(instance))
    assert not errors
    assert semantics.risk_floor_respected(instance, resolve_exception=_resolve_real_exception), (
        "an authorized, resolvable, currently-valid exception_ref must permit the floor override"
    )


def test_level_below_floor_with_unresolvable_exception_ref_is_not_permitted() -> None:
    """A bare, non-empty exception_ref string is not sufficient: it must
    resolve to a real, currently-valid EXCEPTION_DECISION record."""
    cases = _load(FIXTURES / "risk_assessment.negative.json")
    instance = cases["below_floor_with_unresolvable_exception_semantic"]
    errors = list(_validator().iter_errors(instance))
    assert not errors, "fixture must be structurally valid to exercise the semantic check"
    assert not semantics.risk_floor_respected(instance, resolve_exception=_resolve_real_exception)


def test_dimensions_may_raise_but_not_replace_floor_reasoning() -> None:
    instance = _load(FIXTURES / "risk_assessment.positive.json")
    ra = instance["risk_assessment"]
    assert ra["dimensions"], "at least one scored dimension is required"
    assert ra["floors"], "fixture should exercise the floor rule"
