"""Contract tests for Evidence Bundle v2 (PR-S03).

Evidence Bundle v2 upgrades the v1 container schema into typed claims and
evidence with explicit state/policy/environment binding, invalidation
dependencies, and an admission result. v1 remains unchanged and available.

Semantic (non-schema) checks are implemented once in contracts/semantics.py
and imported here rather than redefined locally.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from contracts import semantics

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "EVIDENCE_BUNDLE.v2.schema.json"
FIXTURES = ROOT / "tests" / "fixtures" / "schemas"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validator():
    jsonschema = pytest.importorskip("jsonschema")
    schema = _load(SCHEMA_PATH)
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


def test_v1_schema_is_unchanged_and_still_present() -> None:
    v1 = _load(ROOT / "schemas" / "EVIDENCE_BUNDLE.schema.json")
    assert v1["properties"]["schema_version"]["const"] == "1.0"


def test_v1_to_v2_transition_rule_is_documented() -> None:
    """v2 is mandatory for new L2+ decisions; v1 is valid only for
    historical/migration reads. This must be stated, not left implicit
    ('new bundles SHOULD use v2' is not a hard requirement)."""
    text = (ROOT / "docs" / "agile-v-runtime" / "01_SCHEMAS.md").read_text(encoding="utf-8")
    assert "MUST" in text and "v1/v2 transition" in text
    assert "historical records and migration reads" in text


def test_v2_schema_is_valid_draft_2020_12() -> None:
    _validator()


def test_v2_positive_fixture_is_admissible() -> None:
    instance = _load(FIXTURES / "evidence_bundle_v2.positive.json")
    errors = list(_validator().iter_errors(instance))
    assert not errors, [e.message for e in errors]


@pytest.mark.parametrize(
    "case_id",
    [
        "evidence_with_no_claim", "missing_policy_binding_for_l2", "missing_producer",
        "unknown_admission_status", "invalidation_dependency_missing_kind",
        "subject_state_missing_subject_type",
    ],
)
def test_v2_structural_negative_cases_are_rejected(case_id: str) -> None:
    cases = _load(FIXTURES / "evidence_bundle_v2.negative.json")
    instance = cases[case_id]
    errors = list(_validator().iter_errors(instance))
    assert errors, f"{case_id} should have been schema-rejected"


def test_v2_wrong_commit_passes_schema_but_fails_semantic_state_binding_check() -> None:
    """A structurally valid bundle can still bind evidence to the wrong source
    state. Schema validation alone cannot catch this — it is a semantic
    admissibility check the gate (or an equivalent test) must perform."""
    cases = _load(FIXTURES / "evidence_bundle_v2.negative.json")
    instance = cases["wrong_commit_semantic"]
    errors = list(_validator().iter_errors(instance))
    assert not errors, "fixture must be structurally valid to exercise the semantic check"
    assert not semantics.evidence_state_binding_matches_baseline(instance), (
        "evidence bound to a different commit than the baseline must be flagged as a state mismatch"
    )


def test_v2_positive_fixture_state_binding_matches_baseline() -> None:
    instance = _load(FIXTURES / "evidence_bundle_v2.positive.json")
    assert semantics.evidence_state_binding_matches_baseline(instance)


def test_v2_evidence_every_item_declares_supported_claims() -> None:
    instance = _load(FIXTURES / "evidence_bundle_v2.positive.json")
    claim_ids = {c["claim_id"] for c in instance["bundle"]["claims"]}
    for item in instance["bundle"]["evidence"]:
        assert item["supports"], "evidence item must declare at least one supported claim"
        assert set(item["supports"]) <= claim_ids, "evidence supports an undeclared claim"


def test_v2_every_mandatory_claim_has_admitting_evidence_when_admitted() -> None:
    instance = _load(FIXTURES / "evidence_bundle_v2.positive.json")
    assert semantics.evidence_bundle_admission_is_consistent(instance)
