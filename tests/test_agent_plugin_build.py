"""Generated Agent Plugin packages: byte-identity, containment, determinism, provenance."""
from __future__ import annotations

import json
from pathlib import Path
import zipfile

import pytest
from jsonschema import Draft202012Validator

from tools import build_agent_plugins as b
from tools._common import ROOT, load_json, package_version


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("plugins")
    return out, b.build_all(out, include_preview=True, make_zip=True, commit="a" * 40)


def test_four_stable_packages_and_preview(built):
    _, results = built
    names = {r["name"]: r["channel"] for r in results}
    assert names == {"agile-v-core": "stable", "agile-v-verified-build": "stable", "agile-v-regulated": "stable",
                     "agile-v-embedded": "stable", "agile-v-regulated-preview": "preview"}


def test_default_build_excludes_preview(tmp_path):
    results = b.build_all(tmp_path, commit="a" * 40)
    assert {r["channel"] for r in results} == {"stable"}


def test_plugin_json_validates_against_agent_plugins_1_0(built):
    validator = Draft202012Validator(load_json(b.PLUGIN_SCHEMA))
    for result in built[1]:
        manifest = load_json(result["path"] / "plugin.json")
        assert not list(validator.iter_errors(manifest))
        assert manifest["$schema"] == b.PLUGIN_SCHEMA_ID
        assert manifest["version"] == package_version()
        assert set(manifest) <= {"$schema", "name", "version", "description", "author", "homepage",
                                 "repository", "license", "keywords", "extensions"}


def test_layout_and_no_mcp_json(built):
    for result in built[1]:
        root = result["path"]
        assert {p.name for p in root.iterdir()} == {"plugin.json", "skills", "LICENSE", "CHANGELOG.md",
                                                    "AGILE_V_PACKAGE_MANIFEST.json"}


def test_skill_md_is_byte_identical_and_contained(built):
    skills = b.catalog_skills()
    for result in built[1]:
        root = result["path"].resolve()
        names = [p.name for p in (root / "skills").iterdir()]
        assert len(names) == len(set(names))
        for skill_dir in (root / "skills").iterdir():
            source = ROOT / skills[skill_dir.name]["path"]
            assert (skill_dir / "SKILL.md").read_bytes() == source.read_bytes()
            for path in skill_dir.rglob("*"):
                assert path.resolve().is_relative_to(root)


def test_stable_packages_contain_no_draft_skill(built):
    skills = b.catalog_skills()
    for result in built[1]:
        if result["channel"] == "stable":
            for skill_dir in (result["path"] / "skills").iterdir():
                assert skills[skill_dir.name]["status"] == "released"


def test_package_manifest_records_provenance(built):
    skills = b.catalog_skills()
    for result in built[1]:
        manifest = load_json(result["path"] / "AGILE_V_PACKAGE_MANIFEST.json")
        assert manifest["source_commit"] == "a" * 40
        assert manifest["source_repository"] == "Agile-V/agile_v_skills"
        assert "do not establish that the skills are correct" in manifest["provenance_note"]
        for record in manifest["skills"]:
            assert record["source_path"] == str(Path(skills[record["skill"]]["path"]).parent) + "/"
            assert record["skill_version"] == skills[record["skill"]]["version"]
            assert record["content_digest"].startswith("sha256:")


def test_build_is_deterministic(built, tmp_path):
    out, results = built
    again = b.build_all(tmp_path, include_preview=True, make_zip=True, commit="a" * 40)
    assert {r["name"]: r["sha256"] for r in results} == {r["name"]: r["sha256"] for r in again}
    assert (out / "SHA256SUMS").read_text() == (tmp_path / "SHA256SUMS").read_text()


def test_zip_contents_match_package(built):
    for result in built[1]:
        with zipfile.ZipFile(result["zip"]) as archive:
            names = set(archive.namelist())
        expected = {f"{result['path'].name}/{p.relative_to(result['path']).as_posix()}"
                    for p in result["path"].rglob("*") if p.is_file()}
        assert names == expected


def test_draft_profile_cannot_be_built_as_stable(tmp_path):
    profile = {"name": "bad", "channel": "stable", "description": "bad profile here",
               "include": ["agile-v-core", "agile-v-aibom"]}
    with pytest.raises(b.CompositionError):
        b.build_package(profile, tmp_path, skills=b.catalog_skills(), version="0.0.0", commit="x", tree_clean=True)
