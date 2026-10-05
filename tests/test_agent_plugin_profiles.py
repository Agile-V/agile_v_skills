"""Agent Plugins 1.0 distribution profiles (AVS-01) and capability composition (AVS-08)."""
from __future__ import annotations

from copy import deepcopy
import hashlib

import pytest
import yaml

from tools import build_agent_plugins as b
from tools._common import ROOT, load_json

PROFILES = b.load_profiles()
SKILLS = b.catalog_skills()
STABLE = {"agile-v-core", "agile-v-verified-build", "agile-v-regulated", "agile-v-embedded"}


def test_vendored_agent_plugins_schemas_are_unmodified():
    provenance = yaml.safe_load((b.PACKAGING / "schemas/1.0.0/PROVENANCE.yaml").read_text())
    assert provenance["upstream_version"] == "1.0.0"
    for name, meta in provenance["files"].items():
        data = (b.PACKAGING / "schemas/1.0.0" / name).read_bytes()
        assert hashlib.sha256(data).hexdigest() == meta["sha256"], f"{name} was modified"
        assert meta["source_url"].startswith("https://agent-plugins.org/schemas/1.0.0/")


def test_four_stable_profiles_defined():
    assert {n for n, p in PROFILES.items() if p["channel"] == "stable"} == STABLE


@pytest.mark.parametrize("name", sorted(PROFILES))
def test_profile_composes(name):
    assert b.check_composition(PROFILES[name], SKILLS) == []


@pytest.mark.parametrize("name", sorted(STABLE))
def test_stable_profile_contains_no_draft_skill(name):
    assert all(SKILLS[s]["status"] == "released" for s in PROFILES[name]["include"])


def test_preview_profile_is_explicitly_preview():
    preview = PROFILES["agile-v-regulated-preview"]
    assert preview["channel"] == "preview"
    assert set(PROFILES["agile-v-regulated"]["include"]) < set(preview["include"])
    assert "PREVIEW" in preview["description"]


def _profile(include, channel="stable"):
    return {"name": "test-profile", "channel": channel, "description": "synthetic profile", "include": include}


def test_unknown_skill_rejected():
    assert b.check_composition(_profile(["agile-v-core", "no-such-skill"]), SKILLS)


def test_missing_prerequisite_rejected():
    errors = b.check_composition(_profile(["build-agent", "agile-v-core"]), SKILLS)
    assert any("prerequisite" in e for e in errors)


def test_draft_skill_in_stable_profile_rejected():
    errors = b.check_composition(_profile(["agile-v-core", "agile-v-aibom"]), SKILLS)
    assert any("draft skill" in e for e in errors)


def test_draft_only_capability_dependency_rejected():
    skills = deepcopy(SKILLS)
    skills["test-designer"]["capabilities"]["requires"].append("org.agile-v.ai-influence.inventory")
    errors = b.check_composition(_profile(["agile-v-core", "agile-v-aibom", "requirement-architect",
                                           "logic-gatekeeper", "test-designer"], "preview"), skills)
    assert errors == []
    errors = b.check_composition(_profile(["agile-v-core", "agile-v-aibom", "requirement-architect",
                                           "logic-gatekeeper", "test-designer"]), skills)
    assert any("draft-only capability" in e for e in errors)


def test_missing_required_capability_rejected():
    skills = deepcopy(SKILLS)
    skills["agile-v-core"]["capabilities"]["requires"] = ["org.agile-v.requirements.baseline"]
    assert any("missing capability" in e for e in b.check_composition(_profile(["agile-v-core"]), skills))


def test_conflict_rejected():
    skills = deepcopy(SKILLS)
    skills["requirement-architect"]["capabilities"]["conflicts"] = ["org.agile-v.core.lifecycle"]
    errors = b.check_composition(_profile(["agile-v-core", "requirement-architect"]), skills)
    assert any("conflicts" in e for e in errors)


def test_duplicate_exclusive_capability_rejected():
    skills = deepcopy(SKILLS)
    for name in ("agile-v-core", "requirement-architect"):
        skills[name]["capabilities"]["provides"].append("org.agile-v.test.exclusive")
        skills[name]["capabilities"]["exclusive"] = ["org.agile-v.test.exclusive"]
    errors = b.check_composition(_profile(["agile-v-core", "requirement-architect"]), skills)
    assert any("exclusive" in e for e in errors)


def test_superseded_capability_rejected():
    skills = deepcopy(SKILLS)
    skills["requirement-architect"]["capabilities"]["supersedes"] = ["org.agile-v.core.lifecycle"]
    errors = b.check_composition(_profile(["agile-v-core", "requirement-architect"]), skills)
    assert any("supersedes" in e for e in errors)


def test_every_released_skill_provides_a_capability_and_prereqs_are_representable():
    for entry in SKILLS.values():
        caps = entry["capabilities"]
        if entry["status"] == "released":
            assert caps["provides"], entry["name"]
        for prereq in entry["routing"]["prerequisites"]:
            assert set(caps["requires"]) & set(SKILLS[prereq]["capabilities"]["provides"]), (entry["name"], prereq)


def test_capability_names_are_globally_unique_per_provider():
    seen = {}
    for entry in SKILLS.values():
        for capability in entry["capabilities"]["provides"]:
            assert capability not in seen, f"{capability}: {seen.get(capability)} and {entry['name']}"
            seen[capability] = entry["name"]


def test_check_mode_passes():
    assert b.check_all() == []


def test_claude_plugin_manifest_still_present():
    assert load_json(ROOT / ".claude-plugin/plugin.json")["skills"]
