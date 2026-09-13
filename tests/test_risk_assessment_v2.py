"""Contract tests for Risk Assessment v2 (PR-S08)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "tests" / "fixtures" / "schemas"
CONTRACT = ROOT / "docs" / "agile-v-runtime" / "11_RISK_ASSESSMENT_V2.md"

LEVEL_ORDER = ["L0", "L1", "L2", "L3", "L4"]


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validator():
    jsonschema = pytest.importorskip("jsonschema")
    schema = _load(SCHEMAS / "RISK_ASSESSMENT.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


def _floor_respected(instance: dict) -> bool:
    ra = instance["risk_assessment"]
    if not ra["floors"]:
        return True
    highest_floor = max(LEVEL_ORDER.index(f["minimum_level"]) for f in ra["floors"])
    selected = LEVEL_ORDER.index(ra["selected_level"])
    if selected >= highest_floor:
        return True
    # Below floor is only permitted with an authorized exception reference.
    return bool(ra.get("exception_ref"))


def test_contract_doc_exists() -> None:
    assert CONTRACT.exists()


def test_schema_is_valid() -> None:
    _validator()


def test_positive_fixture_is_valid_and_respects_floor() -> None:
    instance = _load(FIXTURES / "risk_assessment.positive.json")
    errors = list(_validator().iter_errors(instance))
    assert not errors, [e.message for e in errors]
    assert _floor_respected(instance)


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
    assert not _floor_respected(instance)


def test_level_may_be_lowered_below_floor_with_authorized_exception() -> None:
    cases = _load(FIXTURES / "risk_assessment.negative.json")
    instance = cases["below_floor_with_exception_semantic"]
    errors = list(_validator().iter_errors(instance))
    assert not errors
    assert _floor_respected(instance), "an authorized exception_ref must permit the floor override"


def test_dimensions_may_raise_but_not_replace_floor_reasoning() -> None:
    instance = _load(FIXTURES / "risk_assessment.positive.json")
    ra = instance["risk_assessment"]
    assert ra["dimensions"], "at least one scored dimension is required"
    assert ra["floors"], "fixture should exercise the floor rule"
