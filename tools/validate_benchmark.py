"""Validate the AgileV-Bench corpus without evaluating it.

Checks every case against benchmark.schema.json, every manifest digest, the
corpus digest, unique ids, and minimum coverage (>=60 cases; at least one
software, firmware and PCB transition). Exit 1 on any problem.
"""
from __future__ import annotations

import sys

from jsonschema import Draft202012Validator

try:
    from tools._common import ROOT, dump_json, load_json, sha256_bytes
except ImportError:  # executed as a script
    from _common import ROOT, dump_json, load_json, sha256_bytes  # noqa: E402

BENCH = ROOT / "benchmarks" / "agilev-bench"


def validate(version: str | None = None) -> list[str]:
    version = version or (BENCH / "VERSION").read_text().strip()
    manifest = load_json(BENCH / "manifests" / f"v{version}.json")
    validator = Draft202012Validator(load_json(BENCH / "benchmark.schema.json"))
    errors, ids, domains = [], set(), set()
    for entry in manifest["cases"]:
        path = BENCH / entry["path"]
        if not path.exists():
            errors.append(f"missing case file {entry['path']}")
            continue
        case = load_json(path)
        if sha256_bytes(dump_json(case).encode()) != entry["sha256"] or path.read_text() != dump_json(case):
            errors.append(f"{entry['id']}: digest or canonical form mismatch")
        errors += [f"{entry['id']}: {e.message}" for e in validator.iter_errors(case)]
        if case.get("id") != entry["id"] or entry["id"] in ids:
            errors.append(f"{entry['id']}: id mismatch or duplicate")
        ids.add(entry["id"])
        if case.get("category") == "cross-domain":
            domains.add(case.get("domain"))
    listed = {BENCH / e["path"] for e in manifest["cases"]}
    errors += [f"unlisted case file {p.relative_to(ROOT)}" for p in (BENCH / "cases").rglob("*.json") if p not in listed]
    corpus = sha256_bytes("".join(f"{e['path']}\0{e['sha256']}\n"
                                  for e in sorted(manifest["cases"], key=lambda e: e["path"])).encode())
    if corpus != manifest["corpus_digest"]:
        errors.append("corpus_digest does not match case digests")
    if manifest["case_count"] != len(manifest["cases"]) or len(ids) < 60:
        errors.append("case_count mismatch or fewer than 60 cases")
    if not {"software", "firmware", "pcb"} <= domains:
        errors.append("cross-domain cases must cover software, firmware and pcb")
    return errors


def main() -> int:
    errors = validate()
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
