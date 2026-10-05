"""Generate catalog/evidence-adapters.json from reviewed registry profiles.

Usage:
    python tools/build_evidence_adapter_catalog.py           # write
    python tools/build_evidence_adapter_catalog.py --check   # fail on drift

Inputs are policy-side profiles under profiles/evidence-sources/ (including
history/) and profiles/evidence-properties/. Every profile is validated against
its base schema (schemas/EVIDENCE_*_PROFILE.schema.json) and the registry
overlay schema. Composition errors (duplicate active ids, capability
contradictions, ambiguous property selection) fail the build.
"""
from __future__ import annotations

import argparse
import sys

from jsonschema import Draft202012Validator, FormatChecker

try:
    from tools._common import ROOT, dump_json, load_json, load_yaml, write_or_check
except ImportError:  # executed as a script: tools/ is sys.path[0]
    from _common import ROOT, dump_json, load_json, load_yaml, write_or_check  # noqa: E402

from contracts.semantics import profile_digest  # noqa: E402

OUTPUT = ROOT / "catalog" / "evidence-adapters.json"
SOURCES = ROOT / "profiles" / "evidence-sources"
PROPERTIES = ROOT / "profiles" / "evidence-properties"


def _validator(path):
    return Draft202012Validator(load_json(path), format_checker=FormatChecker())


def registry_contract_version() -> str:
    return load_yaml(ROOT / "contracts" / "versions.yaml")["contracts"]["evidence_adapter_registry"]


def build() -> tuple[dict, list[str]]:
    errors: list[str] = []
    base_source = _validator(ROOT / "schemas" / "EVIDENCE_SOURCE_PROFILE.schema.json")
    base_property = _validator(ROOT / "schemas" / "EVIDENCE_PROPERTY_PROFILE.schema.json")
    overlay_source = _validator(ROOT / "profiles" / "evidence-source-registry-entry.schema.json")
    overlay_property = _validator(ROOT / "profiles" / "evidence-property-registry-entry.schema.json")

    adapters = []
    paths = [(p, False) for p in sorted(SOURCES.glob("*.yaml"))]
    paths += [(p, True) for p in sorted((SOURCES / "history").glob("*.yaml"))]
    for path, historical in paths:
        rel = path.relative_to(ROOT).as_posix()
        record = load_yaml(path)
        problems = [e.message for v in (base_source, overlay_source) for e in v.iter_errors(record)]
        if problems:
            errors.append(f"{rel}: {problems}")
            continue
        adapter = record["adapter"]
        overlap = set(adapter["may_establish"]) & set(adapter["may_not_establish"])
        if overlap:
            errors.append(f"{rel}: may_establish contradicts may_not_establish: {sorted(overlap)}")
        if not historical and path.stem != adapter["adapter_id"].removeprefix("EAD-"):
            errors.append(f"{rel}: file name must equal adapter_id without 'EAD-'")
        adapters.append({
            "adapter_id": adapter["adapter_id"], "adapter_version": adapter["adapter_version"],
            "profile_path": rel, "profile_digest": profile_digest(record),
            "status": adapter["status"], "owner": adapter["owner"],
            "evidence_type": adapter["evidence_type"], "historical": historical,
        })
    active = [a["adapter_id"] for a in adapters if not a["historical"]]
    for dup in sorted({a for a in active if active.count(a) > 1}):
        errors.append(f"duplicate active adapter_id {dup}")
    digests = [a["profile_digest"] for a in adapters]
    for dup in sorted({d for d in digests if digests.count(d) > 1}):
        errors.append(f"duplicate profile digest {dup}")

    properties = []
    for path in sorted(PROPERTIES.glob("*.yaml")):
        rel = path.relative_to(ROOT).as_posix()
        record = load_yaml(path)
        problems = [e.message for v in (base_property, overlay_property) for e in v.iter_errors(record)]
        if problems:
            errors.append(f"{rel}: {problems}")
            continue
        profile = record["profile"]
        if path.stem != profile["profile_id"].removeprefix("EVP-"):
            errors.append(f"{rel}: file name must equal profile_id without 'EVP-'")
        properties.append({
            "profile_id": profile["profile_id"], "claim_type": profile["claim_type"],
            "risk_level": profile["risk_level"], "profile_path": rel,
            "profile_digest": profile_digest(record), "status": profile["status"], "owner": profile["owner"],
        })
    keys = [(p["claim_type"], p["risk_level"]) for p in properties if p["status"] != "deprecated"]
    for dup in sorted({k for k in keys if keys.count(k) > 1}):
        errors.append(f"ambiguous property profile selection for {dup}")

    catalog = {
        "$schema": "./evidence-adapter-catalog.schema.json",
        "schema_version": "1.0",
        "registry_contract_version": registry_contract_version(),
        "generator": "tools/build_evidence_adapter_catalog.py",
        "adapters": sorted(adapters, key=lambda a: (a["adapter_id"], a["historical"], a["profile_digest"])),
        "property_profiles": sorted(properties, key=lambda p: (p["claim_type"], p["risk_level"])),
    }
    errors += [e.message for e in _validator(ROOT / "catalog" / "evidence-adapter-catalog.schema.json").iter_errors(catalog)]
    return catalog, errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail if the committed catalog is stale")
    args = parser.parse_args(argv)
    catalog, errors = build()
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    return 0 if write_or_check(OUTPUT, dump_json(catalog), args.check) else 1


if __name__ == "__main__":
    sys.exit(main())
