"""Assurance Release Manifest (Phase 0 / AVS-10)."""
from __future__ import annotations

from tools import build_release_manifest as rm
from tools._common import ROOT, dump_json, load_json, package_version

COMMIT = "f" * 40


def manifest(**kw):
    return rm.release_manifest(commit=COMMIT, generated_at="2026-10-05T00:00:00Z", **kw)


def test_committed_digests_match_repository_state():
    assert dump_json(rm.digests()) == (ROOT / "release/assurance-digests.json").read_text(), \
        "run: python tools/build_release_manifest.py"


def test_every_contract_version_entry_resolves():
    assert rm.resolve_contract_versions() == []


def test_release_manifest_records_package_version_and_commit():
    m = manifest()
    assert m["repository_version"] == package_version()
    assert m["commit"] == COMMIT
    assert rm.validate_manifest(m) == []


def test_all_schemas_included_in_schema_digest():
    listed = set(manifest()["schemas"])
    assert listed == {p.relative_to(ROOT).as_posix() for p in (ROOT / "schemas").glob("*.schema.json")}


def test_digests_are_deterministic_except_timestamp():
    a = manifest()
    b = rm.release_manifest(commit=COMMIT, generated_at="2030-01-01T00:00:00Z")
    a.pop("generated_at"), b.pop("generated_at")
    assert dump_json(a) == dump_json(b)


def test_tree_digest_is_content_and_path_sensitive(tmp_path):
    from tools._common import tree_digest
    a, b = tmp_path / "a.json", tmp_path / "b.json"
    a.write_text("{}"), b.write_text("[]")
    first = tree_digest([a, b], root=tmp_path)
    assert first == tree_digest([b, a], root=tmp_path)
    b.write_text("[1]")
    assert first != tree_digest([a, b], root=tmp_path)


def test_conformance_corpus_includes_benchmark_and_fixtures():
    paths = {p.relative_to(ROOT).as_posix() for p in rm.conformance_corpus_files()}
    assert "conformance/scenarios.yaml" in paths
    assert "benchmarks/agilev-bench/manifests/v0.1.json" in paths
    assert any(p.startswith("benchmarks/agilev-bench/cases/") for p in paths)
    assert "tests/fixtures/schemas/gate_receipt.positive.json" in paths


def test_catalog_digest_ignores_release_managed_version():
    catalog = load_json(ROOT / "catalog/skills.json")
    before = rm.catalog_content_digest()
    catalog["integrations"]["claude_plugin"]["version"] = "99.0.0"
    assert before == rm.catalog_content_digest()


def test_no_runtime_conformance_claim():
    assert manifest()["runtime_conformance_claim"] == "none"
    schema = load_json(ROOT / "release/ASSURANCE_RELEASE_MANIFEST.schema.json")
    assert schema["properties"]["runtime_conformance_claim"] == {"const": "none"}


def test_plugin_artifacts_from_sha256sums(tmp_path):
    (tmp_path / "SHA256SUMS").write_text("a" * 64 + "  agile-v-core-3.9.0.zip\n")
    m = manifest(plugin_dir=tmp_path)
    assert m["plugin_artifacts"] == [{"file": "agile-v-core-3.9.0.zip", "sha256": "sha256:" + "a" * 64}]
    assert rm.validate_manifest(m) == []


def test_invalid_commit_rejected():
    m = manifest()
    m["commit"] = "main"
    assert rm.validate_manifest(m)
