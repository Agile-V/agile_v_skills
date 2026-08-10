"""Distribution manifests must match the repository release and skill catalog."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _frontmatter(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])


def _discoverable_skills() -> dict[str, dict]:
    paths = [*ROOT.glob("*/SKILL.md"), *ROOT.glob("domains/*/SKILL.md"), *ROOT.glob("skills/*/SKILL.md")]
    return {f"./{path.parent.relative_to(ROOT).as_posix()}": _frontmatter(path) for path in paths}


def test_distribution_versions_match_package() -> None:
    version = _json(ROOT / "package.json")["version"]
    plugin = _json(ROOT / ".claude-plugin/plugin.json")
    marketplace = _json(ROOT / ".claude-plugin/marketplace.json")
    catalog = _json(ROOT / "catalog/skills.json")
    release_manifest = _json(ROOT / ".release-please-manifest.json")
    citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    assert plugin["version"] == version
    assert marketplace["metadata"]["version"] == version
    assert marketplace["plugins"] and all(item["version"] == version for item in marketplace["plugins"])
    assert catalog["integrations"]["claude_plugin"]["version"] == version
    assert release_manifest["."] == version
    assert citation["version"] == version


def test_release_please_updates_every_distribution_version() -> None:
    config = _json(ROOT / "release-please-config.json")
    extra_files = config["packages"]["."]["extra-files"]
    targets = {(item["path"], item.get("jsonpath", "")) for item in extra_files}
    assert targets == {
        (".claude-plugin/plugin.json", "$.version"),
        (".claude-plugin/marketplace.json", "$.metadata.version"),
        (".claude-plugin/marketplace.json", "$.plugins[0].version"),
        ("catalog/skills.json", "$.integrations.claude_plugin.version"),
        ("CITATION.cff", ""),
    }


def test_plugin_catalog_contains_exactly_released_discoverable_skills() -> None:
    discovered = _discoverable_skills()
    released = {path for path, data in discovered.items() if data.get("metadata", {}).get("status") != "draft"}
    drafts = set(discovered) - released
    catalog = _json(ROOT / ".claude-plugin/plugin.json")["skills"]
    assert len(catalog) == len(set(catalog)), "plugin skill paths must be unique"
    assert set(catalog) == released
    assert set(catalog).isdisjoint(drafts), "draft skills must not be distributed"
