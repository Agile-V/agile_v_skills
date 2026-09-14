"""Contract tests for Change-Aware Revalidation (PR-S06).

Semantic (non-schema) checks are implemented once in contracts/semantics.py
and imported here rather than redefined locally.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from contracts import semantics

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "tests" / "fixtures" / "schemas"
CONTRACT = ROOT / "docs" / "agile-v-runtime" / "10_CHANGE_AWARE_REVALIDATION.md"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validator():
    jsonschema = pytest.importorskip("jsonschema")
    schema = _load(SCHEMAS / "REVALIDATION_ASSESSMENT.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


def _evidence_bundle_validator():
    jsonschema = pytest.importorskip("jsonschema")
    schema = _load(SCHEMAS / "EVIDENCE_BUNDLE.v2.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


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
    assert not semantics.revalidation_reuse_eligible(unknown_eval)


def test_positive_fixture_revalidation_required_evidence_is_not_reuse_eligible() -> None:
    instance = _load(FIXTURES / "revalidation_assessment.positive.json")
    evaluations = instance["assessment"]["evaluations"]
    unchanged = next(e for e in evaluations if e["evidence_ref"] == "EVI-1")
    required = next(e for e in evaluations if e["evidence_ref"] == "EVI-2")
    assert semantics.revalidation_reuse_eligible(unchanged)
    assert not semantics.revalidation_reuse_eligible(required)


def test_partial_coverage_requires_conservative_fallback_structurally() -> None:
    """'partial' coverage (like 'unknown') structurally requires
    conservative_fallback_applied: true."""
    instance = copy.deepcopy(_load(FIXTURES / "revalidation_assessment.positive.json"))
    instance["assessment"]["coverage"] = "partial"
    instance["assessment"]["conservative_fallback_applied"] = False
    errors = list(_validator().iter_errors(instance))
    assert errors, "partial coverage without conservative_fallback_applied must be schema-rejected"


def test_global_conservative_fallback_flag_does_not_make_an_unchanged_item_safe() -> None:
    """A global conservative_fallback_applied: true does NOT, by itself,
    justify treating a specific UNCHANGED item as covered: item-level
    coverage governs that item unless the item explicitly overrides it.
    Missing dependency knowledge for one item is never proof that item is
    unchanged, even when the assessment as a whole applied some fallback
    elsewhere."""
    instance = copy.deepcopy(_load(FIXTURES / "revalidation_assessment.positive.json"))
    instance["assessment"]["coverage"] = "partial"
    instance["assessment"]["conservative_fallback_applied"] = True
    errors = list(_validator().iter_errors(instance))
    assert not errors

    # EVI-1 is UNCHANGED but inherits the assessment-level 'partial' coverage
    # (no item-level override) -- this must NOT be considered conservative.
    assert not semantics.revalidation_coverage_is_conservative(instance)
    unchanged_eval = next(e for e in instance["assessment"]["evaluations"] if e["evidence_ref"] == "EVI-1")
    assert not semantics.revalidation_reuse_eligible(unchanged_eval, assessment_coverage="partial")


def test_item_level_complete_coverage_override_makes_that_item_reuse_eligible() -> None:
    """An item MAY override the assessment-level coverage with its own
    dependency_coverage: complete, proving that item specifically was fully
    resolved even while the overall assessment remains 'partial' for other
    items (Option B from the review: per-evidence coverage model)."""
    instance = copy.deepcopy(_load(FIXTURES / "revalidation_assessment.positive.json"))
    instance["assessment"]["coverage"] = "partial"
    instance["assessment"]["conservative_fallback_applied"] = True
    for evaluation in instance["assessment"]["evaluations"]:
        if evaluation["evidence_ref"] == "EVI-1":
            evaluation["dependency_coverage"] = "complete"
    errors = list(_validator().iter_errors(instance))
    assert not errors, [e.message for e in errors]
    assert semantics.revalidation_coverage_is_conservative(instance)
    unchanged_eval = next(e for e in instance["assessment"]["evaluations"] if e["evidence_ref"] == "EVI-1")
    assert semantics.revalidation_reuse_eligible(unchanged_eval, assessment_coverage="partial")


def test_evidence_bundle_v2_invalidation_dependencies_declare_typed_kind() -> None:
    positive = _load(FIXTURES / "evidence_bundle_v2.positive.json")
    deps = positive["bundle"]["evidence"][0]["invalidation_dependencies"]
    assert deps, "Evidence Bundle v2 fixture should declare invalidation_dependencies"
    for dep in deps:
        assert dep["kind"] in {"source", "requirement", "policy", "environment", "tool", "model", "hardware"}


def test_evidence_bundle_v2_invalidation_dependency_missing_kind_is_rejected() -> None:
    cases = _load(FIXTURES / "evidence_bundle_v2.negative.json")
    instance = cases["invalidation_dependency_missing_kind"]
    errors = list(_evidence_bundle_validator().iter_errors(instance))
    assert errors, "invalidation_dependencies without a typed 'kind' must be schema-rejected"
