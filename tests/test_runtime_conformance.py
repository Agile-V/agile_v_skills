"""Opt-in subprocess comparison against the runtime's own evaluator.

Set AGILEV_RUNTIME_CHECKOUT to a checkout containing agilev.assurance.
Missing implementation is skipped in routine CI, never labeled conformant.
"""
from copy import deepcopy
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from admission_support import load, context
from contracts import semantics as s

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = os.environ.get("AGILEV_RUNTIME_CHECKOUT")
RUNTIME_PYTHON = os.environ.get("AGILEV_RUNTIME_PYTHON")
pytestmark = pytest.mark.skipif(not (RUNTIME or RUNTIME_PYTHON), reason="external runtime not configured")


def runtime_env():
    env = dict(os.environ)
    if RUNTIME_PYTHON:
        env.pop("PYTHONPATH", None)
    else:
        env["PYTHONPATH"] = str(Path(RUNTIME) / "src")
    return env


def baseline():
    approval = load("approval_v2.positive.json")
    return ({"gate": load("gate_receipt.positive.json"),
             "bundle": load("evidence_bundle_v2.positive.json")},
            {"decision_context": context(), "now": "2026-09-14T00:00:00+00:00",
             "adapters": {"EAD-pytest-junit-v1": load("evidence_source_profile.positive.json")},
             "property_profiles": {"requirement_satisfaction:L2": load("evidence_property_profile.positive.json")},
             "approvals": {"APR-1": approval}, "authenticated_approvals": [deepcopy(approval)],
             "exceptions": {}, "authenticated_exceptions": []})


def reference(request, trusted):
    if request.get("operation") == "reuse":
        eligible = s.revalidation_reuse_eligible(request["evaluation"], request.get("assessment_coverage", "unknown"))
        return {"status": "admitted" if eligible else "rejected", "findings": [], "eligible": eligible}
    return s.authorize_gate_transition(
        request["gate"], request["bundle"],
        resolve_adapter=trusted["adapters"].get if trusted.get("adapters") is not None else None,
        resolve_property_profile=(lambda kind, risk: trusted["property_profiles"].get(kind + ":" + risk))
        if trusted.get("property_profiles") is not None else None,
        resolve_approval=trusted["approvals"].get,
        resolve_exception=trusted["exceptions"].get,
        verify_authority=lambda kind, record, ctx: record in trusted["authenticated_" + kind + "s"],
        decision_context=trusted["decision_context"], now=datetime.fromisoformat(trusted["now"]))


def run_runtime(request, trusted, tmp_path):
    trusted_path = tmp_path / "trusted.json"
    trusted_path.write_text(json.dumps(trusted))
    env = runtime_env()
    completed = subprocess.run(
        [RUNTIME_PYTHON or sys.executable, "-m", "agilev.assurance", "--schemas", str(ROOT / "schemas"),
         "--trusted-context", str(trusted_path)], input=json.dumps(request),
        text=True, capture_output=True, cwd=tmp_path, env=env, timeout=15)
    assert completed.returncode in {0, 1}, completed.stderr
    result = json.loads(completed.stdout)
    assert completed.returncode == (0 if result["status"] == "admitted" else 1)
    return result


CASES = ["positive", "state", "policy", "adapter_drift", "overclaim", "property_floor",
         "approval_digest", "approval_scope", "forged_human", "expired", "consumed",
         "critical_risk", "independence", "bundle_task", "waiver_complete", "waiver_incomplete",
         "no_source_resolver", "no_property_resolver", "reuse_complete", "reuse_partial",
         "reuse_unknown", "reuse_missing", "reuse_stale"]


@pytest.mark.parametrize("case", CASES)
def test_runtime_matches_reference(case, tmp_path):
    request, trusted = baseline()
    bundle = request["bundle"]["bundle"]
    gate = request["gate"]["gate_receipt"]
    item = bundle["evidence"][0]
    if case == "state":
        item["state_binding"]["subject_digest"] = "sha256:" + "0" * 64
    elif case == "policy":
        item["policy_binding"]["policy_digest"] = "sha256:" + "0" * 64
    elif case == "adapter_drift":
        trusted["adapters"]["EAD-pytest-junit-v1"]["adapter"]["may_establish"].append("drift")
    elif case == "overclaim":
        item["establishes_properties"].append("human_authority")
    elif case == "property_floor":
        trusted["property_profiles"]["requirement_satisfaction:L2"]["profile"]["required_properties"].append("physical_measurement")
    elif case == "approval_digest":
        # Valid authenticated historical approval, bound to the wrong subject.
        trusted["approvals"]["APR-1"]["approval"]["binding"]["artifact_digest"] = "sha256:" + "0" * 64
        trusted["authenticated_approvals"] = [deepcopy(trusted["approvals"]["APR-1"])]
    elif case == "approval_scope":
        trusted["decision_context"]["resources"].append("OUTSIDE-SCOPE")
    elif case == "forged_human":
        trusted["approvals"]["APR-1"]["approval"]["authorship"] = "human"
    elif case == "expired":
        trusted["now"] = "2028-01-01T00:00:00+00:00"
    elif case == "consumed":
        trusted["approvals"]["APR-1"]["approval"]["usage"]["consumed_at"] = "2026-09-13T00:00:00Z"
        trusted["authenticated_approvals"] = [deepcopy(trusted["approvals"]["APR-1"])]
    elif case == "critical_risk":
        trusted["decision_context"]["critical_risks"] = ["RISK-CRITICAL"]
    elif case == "independence":
        gate["verifier"]["independence_class"] = "I1"
    elif case == "bundle_task":
        bundle["task_id"] = "OTHER-TASK"
    elif case.startswith("waiver_"):
        gate["decision"]["status"] = "WAIVED"
        gate["claims"]["rejected"] = ["CLM-0007"]
        if case == "waiver_incomplete":
            gate["claims"]["rejected"].append("CLM-UNCOVERED")
        gate["exception_refs"] = ["EXC-0001"]
        exception = load("exception_decision.positive.json")
        trusted["exceptions"] = {"EXC-0001": exception}
        trusted["authenticated_exceptions"] = [deepcopy(exception)]
    elif case == "no_source_resolver":
        trusted["adapters"] = None
    elif case == "no_property_resolver":
        trusted["property_profiles"] = None
    elif case.startswith("reuse_"):
        request = {"operation": "reuse", "evaluation": {"result": "UNCHANGED"}}
        coverage = case.removeprefix("reuse_")
        if coverage != "missing":
            request["evaluation"]["dependency_coverage"] = coverage if coverage != "stale" else "complete"
        if coverage == "stale":
            request["evaluation"]["result"] = "STALE"
    expected = reference(request, trusted)
    actual = run_runtime(request, trusted, tmp_path)
    assert actual["status"] == expected["status"]
    assert {f["code"] for f in actual["findings"]} == {f["code"] for f in expected["findings"]}
    if case in {"positive", "waiver_complete", "reuse_complete"}:
        assert actual["status"] == "admitted"
    else:
        assert actual["status"] == "rejected"


def test_runtime_publishes_manifest(tmp_path):
    env = runtime_env()
    completed = subprocess.run([RUNTIME_PYTHON or sys.executable, "-m", "agilev.assurance", "--manifest"],
                               capture_output=True, text=True, env=env, cwd=tmp_path, check=True)
    manifest = json.loads(completed.stdout)
    assert manifest["deployment_mode"] == "local-conformance"
    assert manifest["contracts"]["aggregate_semantics"] == "2.0"
    assert manifest["implementation"] == "agilev.assurance"
