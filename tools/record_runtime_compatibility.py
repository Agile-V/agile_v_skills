"""Turn a runtime-conformance JUnit report into a compatibility record.

Usage (release verification mode, normally from .github/workflows/runtime-conformance.yml):
    python tools/record_runtime_compatibility.py --junit report.xml \
        --runtime-id agentic_agile_v --runtime-repository Agile-V/agentic_agile_v \
        --release v1.2.3 --artifact-digest sha256:... --compatibility-manifest-digest sha256:... \
        --contracts-commit <40-hex> --out record.json

The status is computed conservatively:
  * any mismatch (failure/error)                       -> failed
  * nothing executed (all skipped / no tests)          -> unverified
  * some skipped                                       -> partial
  * immutable release identity incomplete or not a tag -> unverified
  * otherwise                                          -> verified
Skipped tests are never reported as conformance.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

from jsonschema import Draft202012Validator

try:
    from tools._common import ROOT, dump_json, load_json, sha256_file, tree_digest
    from tools.build_release_manifest import conformance_corpus_files
except ImportError:  # executed as a script
    from _common import ROOT, dump_json, load_json, sha256_file, tree_digest  # noqa: E402
    from build_release_manifest import conformance_corpus_files  # noqa: E402

POSITIVE_CASES = {"positive", "waiver_complete", "reuse_complete"}
RELEASE_TAG = re.compile(r"^v?[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$")
DIGEST = re.compile(r"^sha256:[a-f0-9]{64}$")


def parse_junit(path: Path) -> dict:
    counts = {"positive": 0, "rejected_as_expected": 0, "mismatches": 0, "skipped": 0}
    for case in ET.parse(path).getroot().iter("testcase"):
        name = case.get("name", "")
        if case.find("skipped") is not None:
            counts["skipped"] += 1
        elif case.find("failure") is not None or case.find("error") is not None:
            counts["mismatches"] += 1
        else:
            param = name[name.find("[") + 1:-1] if "[" in name else ""
            if param in POSITIVE_CASES or not param:
                counts["positive"] += 1
            else:
                counts["rejected_as_expected"] += 1
    return counts


def status_for(results: dict, identity: dict) -> str:
    executed = results["positive"] + results["rejected_as_expected"] + results["mismatches"]
    if results["mismatches"]:
        return "failed"
    if executed == 0:
        return "unverified"
    if results["skipped"]:
        return "partial"
    immutable = (RELEASE_TAG.match(identity.get("release") or "")
                 and DIGEST.match(identity.get("artifact_digest") or "")
                 and DIGEST.match(identity.get("compatibility_manifest_digest") or ""))
    return "verified" if immutable and results["positive"] >= 1 else "unverified"


def build_record(*, junit: Path, runtime: dict, contracts_commit: str, workflow_run: str = "") -> dict:
    results = parse_junit(junit)
    record = {
        "runtime": runtime,
        "verified_against": {
            "contracts_commit": contracts_commit,
            "contract_versions_digest": sha256_file(ROOT / "contracts" / "versions.yaml"),
            "conformance_corpus_digest": tree_digest(conformance_corpus_files()),
        },
        "results": results,
        "status": status_for(results, runtime),
        "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    if workflow_run:
        record["workflow_run"] = workflow_run
    return record


def validate_record(record: dict) -> list[str]:
    schema = load_json(ROOT / "schemas" / "RUNTIME_COMPATIBILITY.schema.json")
    validator = Draft202012Validator({**schema["$defs"]["release_verification"], "$defs": schema["$defs"]})
    return [e.message for e in validator.iter_errors(record)]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--junit", type=Path, required=True)
    parser.add_argument("--runtime-id", required=True)
    parser.add_argument("--runtime-repository", required=True)
    parser.add_argument("--release", required=True)
    parser.add_argument("--artifact-digest", required=True)
    parser.add_argument("--compatibility-manifest-digest", required=True)
    parser.add_argument("--contracts-commit", required=True)
    parser.add_argument("--workflow-run", default="")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    runtime = {"id": args.runtime_id, "repository": args.runtime_repository, "release": args.release,
               "artifact_digest": args.artifact_digest,
               "compatibility_manifest_digest": args.compatibility_manifest_digest}
    record = build_record(junit=args.junit, runtime=runtime, contracts_commit=args.contracts_commit,
                          workflow_run=args.workflow_run)
    problems = validate_record(record)
    args.out.write_text(dump_json(record), encoding="utf-8")
    print(f"external runtime conformance: {record['status'].upper()} {record['results']}")
    if problems:
        print(f"record does not satisfy the immutable-identity schema: {problems}", file=sys.stderr)
    return 0 if record["status"] == "verified" and not problems else 1


if __name__ == "__main__":
    sys.exit(main())
