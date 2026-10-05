"""Generate the Assurance Release Manifest.

Usage:
    python tools/build_release_manifest.py                 # refresh release/assurance-digests.json
    python tools/build_release_manifest.py --check         # CI: fail if digests drifted from repository state
    python tools/build_release_manifest.py --release-out dist/agent-plugins [--plugin-dir dist/agent-plugins]
        # write ASSURANCE_RELEASE_MANIFEST.json (adds commit, timestamp, plugin artifacts)

release/assurance-digests.json is the committed, timestamp-free part: it binds
a repository version to exact contract versions, schemas, skill catalog,
registry profiles and conformance corpus. The release manifest adds the Git
commit, generation time and plugin artifact digests. Neither file claims
runtime conformance.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

try:
    from tools._common import (ROOT, dump_json, load_json, load_yaml, package_version, sha256_bytes,
                               sha256_file, tree_digest, write_or_check)
    from tools.build_agent_plugins import git_commit, git_tree_clean
except ImportError:  # executed as a script
    from _common import (ROOT, dump_json, load_json, load_yaml, package_version, sha256_bytes,  # noqa: E402
                         sha256_file, tree_digest, write_or_check)
    from build_agent_plugins import git_commit, git_tree_clean  # noqa: E402

GENERATOR_VERSION = "1.0"
DIGESTS = ROOT / "release" / "assurance-digests.json"
SCHEMA = ROOT / "release" / "ASSURANCE_RELEASE_MANIFEST.schema.json"

# Where each contracts/versions.yaml key is defined. Schema keys must equal the
# schema's schema_version const; document keys must exist and, when the
# document states "Contract version: X", X must equal the registry value.
DOCS = ROOT / "docs" / "agile-v-runtime"
CONTRACT_SOURCES = {
    "canonical_lifecycle_contract": DOCS / "03_CANONICAL_LIFECYCLE_CONTRACT.md",
    "risk_classification": DOCS / "04_RISK_CLASSIFICATION.md",
    "evidence_admission_contract": DOCS / "07_EVIDENCE_ADMISSION_CONTRACT.md",
    "independence_classes": DOCS / "08_INDEPENDENCE_CLASSES.md",
    "exception_and_waiver_contract": DOCS / "09_EXCEPTION_AND_WAIVER_CONTRACT.md",
    "change_aware_revalidation": DOCS / "10_CHANGE_AWARE_REVALIDATION.md",
    "risk_assessment_v2": DOCS / "11_RISK_ASSESSMENT_V2.md",
    "governance_conversion_contract": DOCS / "12_GOVERNANCE_CONVERSION.md",
    "skill_graduation_policy": DOCS / "13_SKILL_GRADUATION_POLICY.md",
    "conformance_catalog": ROOT / "conformance" / "scenarios.yaml",
    "trusted_admission_context": DOCS / "14_TRUSTED_ADMISSION_CONTEXT.md",
    "aggregate_semantics": ROOT / "contracts" / "semantics.py",
    "evidence_adapter_registry": DOCS / "15_EVIDENCE_ADAPTER_REGISTRY.md",
    "context_trust_contract": DOCS / "16_CONTEXT_TRUST_CONTRACT.md",
    "opentelemetry_contract": DOCS / "17_OPENTELEMETRY_CONTRACT.md",
    "delegation_contract": DOCS / "05_AGENT_TOOL_AND_DELEGATION_CONTRACT.md",
    "capability_composition": DOCS / "18_CAPABILITY_COMPOSITION.md",
    "requirements": "REQUIREMENTS", "trace_graph": "TRACE_GRAPH", "approval": "APPROVAL",
    "approval_v2": "APPROVAL.v2", "evidence_bundle": "EVIDENCE_BUNDLE", "evidence_bundle_v2": "EVIDENCE_BUNDLE.v2",
    "gate_receipt": "GATE_RECEIPT", "exception_decision": "EXCEPTION_DECISION",
    "revalidation_assessment": "REVALIDATION_ASSESSMENT", "risk_assessment": "RISK_ASSESSMENT",
    "governance_conversion": "GOVERNANCE_CONVERSION", "evidence_source_profile": "EVIDENCE_SOURCE_PROFILE",
    "evidence_property_profile": "EVIDENCE_PROPERTY_PROFILE", "agent_delegation_record_v2": "AGENT_DELEGATION_RECORD.v2",
    "context_source_profile": "CONTEXT_SOURCE_PROFILE", "runtime_compatibility": "RUNTIME_COMPATIBILITY",
    "agile_v_telemetry_event": "AGILE_V_TELEMETRY_EVENT",
}


def resolve_contract_versions() -> list[str]:
    """Every registry entry must resolve to a source that agrees with it."""
    errors = []
    registry = load_yaml(ROOT / "contracts" / "versions.yaml")["contracts"]
    for key, version in registry.items():
        source = CONTRACT_SOURCES.get(key)
        if source is None:
            errors.append(f"{key}: no declared source")
        elif isinstance(source, str):
            path = ROOT / "schemas" / f"{source}.schema.json"
            if not path.exists() or load_json(path)["properties"]["schema_version"]["const"] != version:
                errors.append(f"{key}: schema {source} missing or schema_version != {version}")
        elif not source.exists():
            errors.append(f"{key}: {source.relative_to(ROOT)} missing")
        elif source.suffix == ".md":
            stated = re.search(r"\*\*Contract version: ([0-9.]+)", source.read_text(encoding="utf-8"))
            if stated and stated.group(1).rstrip(".") != version:
                errors.append(f"{key}: document states {stated.group(1)} but registry says {version}")
    return errors


def _files(*patterns: str) -> list[Path]:
    return sorted({p for pattern in patterns for p in ROOT.glob(pattern) if p.is_file()})


def schema_files() -> list[Path]:
    return _files("schemas/*.schema.json")


def conformance_corpus_files() -> list[Path]:
    return _files("conformance/*", "tests/fixtures/schemas/*.json", "tests/test_runtime_conformance.py",
                  "tests/admission_support.py", "benchmarks/agilev-bench/manifests/*.json",
                  "benchmarks/agilev-bench/cases/*/*.json", "benchmarks/agilev-bench/*.schema.json")


def profile_files() -> list[Path]:
    return _files("profiles/**/*.yaml", "profiles/*.schema.json")


def catalog_content_digest() -> str:
    """Catalog digest with the Release-Please-managed version field blanked,
    so automated release PRs do not invalidate the committed digests."""
    catalog = load_json(ROOT / "catalog" / "skills.json")
    catalog["integrations"]["claude_plugin"]["version"] = ""
    return sha256_bytes(dump_json(catalog).encode())


def digests() -> dict:
    """Timestamp- and release-version-free digests (committed and CI-checked)."""
    return {
        "repository": "Agile-V/agile_v_skills",
        "contract_versions_ref": "contracts/versions.yaml",
        "contract_versions_digest": sha256_file(ROOT / "contracts" / "versions.yaml"),
        "catalog_ref": "catalog/skills.json",
        "catalog_content_digest": catalog_content_digest(),
        "schemas_digest": tree_digest(schema_files()),
        "schemas": [p.relative_to(ROOT).as_posix() for p in schema_files()],
        "evidence_adapter_catalog_digest": sha256_file(ROOT / "catalog" / "evidence-adapters.json"),
        "profiles_digest": tree_digest(profile_files()),
        "reference_semantics_digest": sha256_file(ROOT / "contracts" / "semantics.py"),
        "conformance_corpus_digest": tree_digest(conformance_corpus_files()),
        "benchmark_corpus_digest": load_json(ROOT / "benchmarks" / "agilev-bench" / "manifests" / "v0.1.json")["corpus_digest"],
        "agent_plugin_profiles_digest": sha256_file(ROOT / "packaging" / "agent-plugins" / "profiles.yaml"),
        "runtime_conformance_claim": "none",
        "generator_version": GENERATOR_VERSION,
    }


def plugin_artifacts(plugin_dir: Path | None) -> list[dict]:
    if plugin_dir is None or not (plugin_dir / "SHA256SUMS").exists():
        return []
    artifacts = []
    for line in (plugin_dir / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split(None, 1)
        artifacts.append({"file": name.strip(), "sha256": "sha256:" + digest})
    return artifacts


def release_manifest(*, commit: str, generated_at: str, plugin_dir: Path | None = None) -> dict:
    manifest = digests()
    manifest.update(repository_version=package_version(),
                    catalog_digest=sha256_file(ROOT / "catalog" / "skills.json"), commit=commit, source_tree_clean=git_tree_clean(), generated_at=generated_at,
                    plugin_artifacts=plugin_artifacts(plugin_dir))
    return manifest


def validate_manifest(manifest: dict) -> list[str]:
    validator = Draft202012Validator(load_json(SCHEMA), format_checker=FormatChecker())
    return [e.message for e in validator.iter_errors(manifest)]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--release-out", type=Path, help="directory to write ASSURANCE_RELEASE_MANIFEST.json")
    parser.add_argument("--plugin-dir", type=Path, help="directory containing SHA256SUMS of plugin ZIPs")
    parser.add_argument("--commit", help="commit to record (default: git HEAD)")
    args = parser.parse_args(argv)
    errors = resolve_contract_versions()
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    if args.release_out:
        now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        manifest = release_manifest(commit=args.commit or git_commit(), generated_at=now, plugin_dir=args.plugin_dir)
        problems = validate_manifest(manifest)
        if problems:
            print(f"ERROR: {problems}", file=sys.stderr)
            return 1
        args.release_out.mkdir(parents=True, exist_ok=True)
        (args.release_out / "ASSURANCE_RELEASE_MANIFEST.json").write_text(dump_json(manifest), encoding="utf-8")
        return 0
    return 0 if write_or_check(DIGESTS, dump_json(digests()), args.check) else 1


if __name__ == "__main__":
    sys.exit(main())
