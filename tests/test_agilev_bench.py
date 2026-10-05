"""AgileV-Bench v0.1 (AVS-04): corpus integrity and reference reproducibility."""
from __future__ import annotations

import json

import pytest
from jsonschema import Draft202012Validator

from tools import build_agilev_bench, validate_benchmark
from tools.run_agilev_bench import BENCH, load_cases, run_reference, score
from tools._common import load_json

CASES = load_cases()
RESULTS = {r["case_id"]: r for r in run_reference(CASES)}


def test_corpus_is_valid_and_matches_manifest():
    assert validate_benchmark.validate() == []


def test_committed_corpus_matches_generator():
    assert build_agilev_bench.write_corpus(check=True)


def test_minimum_size_and_coverage():
    assert len(CASES) >= 60
    categories = {c["category"] for c in CASES}
    assert {"state-binding", "policy-binding", "evidence-capability", "contradiction", "approvals", "independence",
            "exceptions", "revalidation", "delegation", "context-trust", "ai-provenance", "cross-domain"} == categories
    assert {"software", "firmware", "pcb"} <= {c["domain"] for c in CASES if c["category"] == "cross-domain"}


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_reference_reproduces_declared_expectation(case):
    result = RESULTS[case["id"]]
    assert result["actual_status"] == case["expected"]["status"]
    if case["expected"]["status"] == "rejected":
        assert set(case["expected"]["reason_codes"]) <= set(result["actual_reason_codes"])
    else:
        assert result["actual_reason_codes"] == []


def test_results_validate_against_result_schema():
    validator = Draft202012Validator(load_json(BENCH / "result.schema.json"))
    for result in RESULTS.values():
        assert not list(validator.iter_errors(result))


def test_reference_metrics():
    metrics = score(CASES, list(RESULTS.values()))
    assert metrics["false_authorize_rate"] == 0 and metrics["false_reject_rate"] == 0
    assert metrics["reason_code_agreement"] == 1 and metrics["tamper_detection_rate"] == 1
    assert metrics["case_coverage"] == 1


def test_missing_results_never_count_as_passes():
    partial = [r for cid, r in RESULTS.items() if cid != CASES[0]["id"]]
    metrics = score(CASES, partial)
    assert metrics["case_coverage"] < 1 and metrics["status_agreement"] < 1


def test_always_admit_runtime_is_caught():
    fake = [dict(r, actual_status="admitted", actual_reason_codes=[]) for r in RESULTS.values()]
    assert score(CASES, fake)["false_authorize_rate"] == 1


def test_cases_are_plain_json_without_code_references():
    for case in CASES:
        text = json.dumps(case)
        assert "contracts.semantics" not in text and "lambda" not in text
