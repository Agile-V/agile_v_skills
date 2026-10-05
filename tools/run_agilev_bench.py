"""Run AgileV-Bench cases against the reference evaluator (or validate results).

Usage:
    python tools/run_agilev_bench.py                      # reference run, prints metrics
    python tools/run_agilev_bench.py --results out.jsonl  # also write per-case results
    python tools/run_agilev_bench.py --score external.jsonl  # score another runtime's results

The reference adapter below only translates case data into calls on
contracts.semantics aggregate evaluators. A result produced here is a
REFERENCE SEMANTIC result; it is not evidence that any live agent platform or
runtime behaves this way.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys
import time

try:
    from tools._common import ROOT, load_json
except ImportError:  # executed as a script
    from _common import ROOT, load_json  # noqa: E402

from contracts import semantics as s  # noqa: E402

BENCH = ROOT / "benchmarks" / "agilev-bench"


def load_cases(version: str | None = None) -> list[dict]:
    version = version or (BENCH / "VERSION").read_text().strip()
    manifest = load_json(BENCH / "manifests" / f"v{version}.json")
    return [load_json(BENCH / entry["path"]) for entry in manifest["cases"]]


def _gate(case):
    request, trusted = case["input"], case["trusted"]
    adapters, profiles = trusted.get("adapters"), trusted.get("property_profiles")
    return s.authorize_gate_transition(
        request["gate"], request["bundle"],
        resolve_adapter=adapters.get if adapters is not None else None,
        resolve_property_profile=(lambda kind, risk: profiles.get(f"{kind}:{risk}")) if profiles is not None else None,
        resolve_approval=trusted["approvals"].get, resolve_exception=trusted["exceptions"].get,
        verify_authority=lambda kind, record, ctx: record in trusted["authenticated_" + kind + "s"],
        decision_context=trusted["decision_context"], now=datetime.fromisoformat(trusted["now"]))


def _registry(case):
    registry = s.EvidenceAdapterRegistry(case["trusted"]["registry"]["catalog"], case["trusted"]["registry"]["records"])
    return s.evaluate_evidence_bundle_against_registry(case["input"]["bundle"], registry,
                                                       historical=case["trusted"].get("historical", False))


def _delegation(case):
    trusted = case["trusted"]
    consumed = set(trusted.get("consumed_nonces", []))
    return s.evaluate_delegation(case["input"]["record"], resolve_delegation=trusted["delegations"].get,
                                 resolve_authority=trusted["authorities"].get,
                                 now=datetime.fromisoformat(trusted["now"]),
                                 is_nonce_consumed=lambda nonce: nonce in consumed,
                                 request=case["input"].get("request"))


def _context(case):
    return s.evaluate_context_influence(case["input"]["influence"],
                                        resolve_context_profile=case["trusted"]["context_profiles"].get)


def _reuse(case):
    return s.evaluate_revalidation_reuse(case["input"]["assessment"], case["input"]["evidence_item"])


def _ai_manifest(case):
    sources = case["trusted"].get("sources") or {}
    return s.evaluate_ai_run_manifest(case["input"]["manifest"], resolve_source=sources.get)


OPERATIONS = {"ai_run_manifest": _ai_manifest, "gate_transition": _gate, "evidence_registry": _registry, "delegation": _delegation,
              "context_influence": _context, "revalidation_reuse": _reuse}


def run_reference(cases: list[dict]) -> list[dict]:
    results = []
    for case in cases:
        start = time.perf_counter()
        outcome = OPERATIONS[case["operation"]](case)
        results.append({"benchmark_version": case["benchmark_version"],
                        "runtime": {"id": "agile-v-reference-semantics", "kind": "reference"},
                        "case_id": case["id"], "expected_status": case["expected"]["status"],
                        "actual_status": outcome["status"],
                        "expected_reason_codes": case["expected"]["reason_codes"],
                        "actual_reason_codes": sorted({f["code"] for f in outcome["findings"]}),
                        "latency_ms": round((time.perf_counter() - start) * 1000, 3), "notes": ""})
    return results


def score(cases: list[dict], results: list[dict]) -> dict:
    """Metrics. A case missing from results counts as not executed (never as a pass)."""
    by_id = {r["case_id"]: r for r in results}
    expected_reject = [c for c in cases if c["expected"]["status"] == "rejected"]
    expected_allow = [c for c in cases if c["expected"]["status"] != "rejected"]

    def actual(c):
        return by_id.get(c["id"], {}).get("actual_status")

    def codes_agree(c):
        r = by_id.get(c["id"])
        if r is None:
            return False
        if c["expected"]["status"] != "rejected":
            return r["actual_reason_codes"] == [] and r["actual_status"] == c["expected"]["status"]
        return set(c["expected"]["reason_codes"]) <= set(r["actual_reason_codes"])

    tamper = [c for c in cases if "tamper" in c["tags"]]
    reval = [c for c in cases if c["category"] == "revalidation"]
    executed = [c for c in cases if c["id"] in by_id]
    ratio = lambda n, d: round(n / d, 4) if d else None  # noqa: E731
    return {
        "case_count": len(cases), "executed": len(executed),
        "false_authorize_rate": ratio(sum(actual(c) in {"admitted", "proposed"} for c in expected_reject), len(expected_reject)),
        "false_reject_rate": ratio(sum(actual(c) == "rejected" for c in expected_allow), len(expected_allow)),
        "status_agreement": ratio(sum(actual(c) == c["expected"]["status"] for c in cases), len(cases)),
        "reason_code_agreement": ratio(sum(codes_agree(c) for c in cases), len(cases)),
        "tamper_detection_rate": ratio(sum(actual(c) == "rejected" for c in tamper), len(tamper)),
        "revalidation_precision": ratio(sum(actual(c) == c["expected"]["status"] for c in reval), len(reval)),
        "case_coverage": ratio(len(executed), len(cases)),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--results", type=Path, help="write reference results (JSON lines)")
    parser.add_argument("--score", type=Path, help="score an external runtime's JSON-lines results")
    args = parser.parse_args(argv)
    cases = load_cases()
    if args.score:
        results = [json.loads(line) for line in args.score.read_text().splitlines() if line.strip()]
        label = "external"
    else:
        results = run_reference(cases)
        label = "reference-semantics"
        if args.results:
            args.results.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in results))
    metrics = score(cases, results)
    print(json.dumps({"result_kind": label, **metrics}, indent=2))
    return 0 if metrics["status_agreement"] == 1 and metrics["reason_code_agreement"] == 1 else 1


if __name__ == "__main__":
    sys.exit(main())
