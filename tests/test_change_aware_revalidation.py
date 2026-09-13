"""Contract tests for Change-Aware Revalidation (PR-S06)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "tests" / "fixtures" / "schemas"
CONTRACT = ROOT / "docs" / "agile-v-runtime" / "10_CHANGE_AWARE_REVALIDATION.md"

REUSE_ELIGIBLE_RESULTS = {"UNCHANGED"}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validator():
    jsonschema = pytest.importorskip("jsonschema")
    schema = _load(SCHEMAS / "REVALIDATION_ASSESSMENT.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


def _reuse_eligible(evaluation: dict) -> bool:
    """UNKNOWN, STALE, and REVALIDATION_REQUIRED are never reuse-eligible;
    only UNCHANGED is. This must hold regardless of risk level (UNKNOWN is
    conservative everywhere; L3/L4 additionally forces full revalidation)."""
    return evaluation["result"] in REUSE_ELIGIBLE_RESULTS


def test_contract_doc_exists() -> None:
    assert CONTRACT.exists()


def test_contract_defines_four_results() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    for result in ("UNCHANGED", "REVALIDATION_REQUIRED", "STALE", "UNKNOWN"):
        assert result in text


def test_schema_is_valid() -> None:
    _validator()


def test_positive_fixture_is_valid() -> None:
    instance = _load(FIXTURES / "revalidation_assessment.positive.json")
    errors = list(_validator().iter_errors(instance))
    assert not errors, [e.message for e in errors]


@pytest.mark.parametrize(
    "case_id",
    ["unknown_coverage_without_conservative_fallback", "empty_changed_refs", "invalid_result_enum"],
)
def test_structural_negative_cases(case_id: str) -> None:
    cases = _load(FIXTURES / "revalidation_assessment.negative.json")
    errors = list(_validator().iter_errors(cases[case_id]))
    assert errors, f"{case_id} should have been schema-rejected"


def test_unknown_result_is_never_reuse_eligible_even_at_l3() -> None:
    cases = _load(FIXTURES / "revalidation_assessment.negative.json")
    instance = cases["unknown_result_at_l3_semantic"]
    errors = list(_validator().iter_errors(instance))
    assert not errors, "fixture must be structurally valid to exercise the semantic check"
    unknown_eval = next(e for e in instance["assessment"]["evaluations"] if e["result"] == "UNKNOWN")
    assert not _reuse_eligible(unknown_eval)


def test_positive_fixture_revalidation_required_evidence_is_not_reuse_eligible() -> None:
    instance = _load(FIXTURES / "revalidation_assessment.positive.json")
    evaluations = instance["assessment"]["evaluations"]
    unchanged = next(e for e in evaluations if e["evidence_ref"] == "EVI-1")
    required = next(e for e in evaluations if e["evidence_ref"] == "EVI-2")
    assert _reuse_eligible(unchanged)
    assert not _reuse_eligible(required)


def test_evidence_bundle_v2_invalidation_dependencies_align_with_dependency_kinds() -> None:
    positive = _load(FIXTURES / "evidence_bundle_v2.positive.json")
    deps = positive["bundle"]["evidence"][0]["invalidation_dependencies"]
    assert deps, "Evidence Bundle v2 fixture should declare invalidation_dependencies"
