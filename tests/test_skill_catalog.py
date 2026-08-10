"""Structural contracts for the authoritative machine-readable skill catalog."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "skills.json"
CATALOG_SCHEMA = ROOT / "catalog" / "skill-catalog.schema.json"
NESTED_SCHEMA = ROOT / "catalog" / "nested-skill-metadata.schema.json"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _frontmatter(path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    assert content.startswith("---\n"), f"{path.relative_to(ROOT)} lacks YAML frontmatter"
    parts = content.split("---", 2)
    assert len(parts) == 3, f"{path.relative_to(ROOT)} has unterminated frontmatter"
    data = yaml.safe_load(parts[1])
    assert isinstance(data, dict), f"{path.relative_to(ROOT)} frontmatter must be a mapping"
    return data


def _validator(schema_path: Path):
    jsonschema = pytest.importorskip("jsonschema")
    schema = _json(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema)


def _version_tuple(value: str) -> tuple[int, int, int, str]:
    match = re.fullmatch(r"(\d+)\.(\d+)(?:\.(\d+))?(?:-([0-9A-Za-z.-]+))?", value)
    assert match, f"invalid semantic version: {value}"
    return int(match[1]), int(match[2]), int(match[3] or 0), match[4] or ""


@pytest.fixture(scope="module")
def catalog() -> dict:
    data = _json(CATALOG_PATH)
    errors = sorted(_validator(CATALOG_SCHEMA).iter_errors(data), key=lambda error: list(error.path))
    assert not errors, [f"{list(error.path)}: {error.message}" for error in errors]
    return data


def test_catalog_completely_and_uniquely_covers_skills(catalog: dict) -> None:
    entries = catalog["skills"]
    names = [entry["name"] for entry in entries]
    paths = [entry["path"] for entry in entries]
    discovered = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("SKILL.md")
        if not any(part.startswith(".") or part == "node_modules" for part in path.parts)
    }
    assert len(names) == len(set(names)), "catalog skill names must be unique"
    assert len(paths) == len(set(paths)), "catalog skill paths must be unique"
    assert set(paths) == discovered


def test_catalog_agrees_with_skill_frontmatter(catalog: dict) -> None:
    for entry in catalog["skills"]:
        path = ROOT / entry["path"]
        frontmatter = _frontmatter(path)
        metadata = frontmatter.get("metadata")
        assert path.parent.name == entry["name"] == frontmatter.get("name")
        assert frontmatter.get("description")
        assert frontmatter.get("license") == "CC-BY-SA-4.0"
        assert isinstance(metadata, dict)
        assert metadata.get("standard") == "Agile V"
        assert metadata.get("author") == "agile-v.org"
        assert isinstance(metadata.get("version"), str)
        assert _version_tuple(entry["version"]) == _version_tuple(metadata["version"])
        expected_status = metadata.get("status", "released")
        assert expected_status in {"released", "draft"}
        assert entry["status"] == expected_status


def test_routing_markers_and_references_are_current(catalog: dict) -> None:
    names = {entry["name"] for entry in catalog["skills"]}
    for entry in catalog["skills"]:
        routing = entry["routing"]
        assert routing["intent"].strip()
        assert set(routing["prerequisites"]) <= names, f"stale prerequisite in {entry['name']}"
        assert entry["name"] not in routing["prerequisites"]
        frontmatter_requires = _frontmatter(ROOT / entry["path"]).get("metadata", {}).get("requires", [])
        assert set(frontmatter_requires) <= set(routing["prerequisites"])


def test_nested_companion_metadata_is_valid_and_agrees(catalog: dict) -> None:
    by_path = {entry["path"]: entry for entry in catalog["skills"]}
    validator = _validator(NESTED_SCHEMA)
    companions = sorted((ROOT / "skills").glob("*/metadata.json"))
    assert companions, "nested companion metadata unexpectedly absent"
    for path in companions:
        metadata = _json(path)
        errors = list(validator.iter_errors(metadata))
        assert not errors, f"{path.relative_to(ROOT)}: {[error.message for error in errors]}"
        skill_path = f"{path.parent.relative_to(ROOT).as_posix()}/SKILL.md"
        entry = by_path[skill_path]
        assert metadata["name"] == entry["name"]
        assert _version_tuple(metadata["version"]) == _version_tuple(entry["version"])
        assert metadata["category"] == entry["category"]
        internal_dependencies = {item for item in metadata["dependencies"] if not item.startswith("optional:")}
        assert internal_dependencies <= set(entry["routing"]["prerequisites"])
        for field in ("previous_skill", "next_skill"):
            if field in metadata:
                assert metadata[field] in {item["name"] for item in catalog["skills"]}, f"stale {field}"


def test_claude_plugin_cataloged_subset_and_version_agree(catalog: dict) -> None:
    integration = catalog["integrations"]["claude_plugin"]
    plugin = _json(ROOT / integration["manifest"])
    assert plugin["version"] == integration["version"]
    by_path = {entry["path"].removesuffix("/SKILL.md"): entry for entry in catalog["skills"]}
    plugin_paths = [path.removeprefix("./") for path in plugin["skills"]]
    assert len(plugin_paths) == len(set(plugin_paths))
    assert integration["skills"] == [by_path[path]["name"] for path in plugin_paths]
    for path in plugin_paths:
        assert path in by_path, f"plugin references uncataloged skill: {path}"
        assert by_path[path]["status"] == "released", f"plugin publishes draft skill: {path}"
