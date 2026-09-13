"""Contract tests for the Skill Preview/Draft Graduation Policy (PR-S13).

Every skill with metadata.status == draft must declare a preview block
(owner, graduation_target, graduation_criteria_ref, compatibility_declaration,
known_limitations) validated against schemas/SKILL_STATUS.schema.json.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "SKILL_STATUS.schema.json"
POLICY = ROOT / "docs" / "agile-v-runtime" / "13_SKILL_GRADUATION_POLICY.md"

SKILL_DIRS = sorted(
    path.parent for path in ROOT.rglob("SKILL.md")
    if not any(part.startswith(".") or part == "node_modules" for part in path.parts)
)


def _frontmatter(path: Path) -> dict:
    content = (path / "SKILL.md").read_text(encoding="utf-8")
    return yaml.safe_load(content.split("---", 2)[1]) or {}


def _draft_skill_dirs() -> list[Path]:
    return [d for d in SKILL_DIRS if _frontmatter(d).get("metadata", {}).get("status") == "draft"]


def _validator():
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema)


def test_policy_doc_exists() -> None:
    assert POLICY.exists()


def test_policy_defines_six_states() -> None:
    text = POLICY.read_text(encoding="utf-8")
    for state in ("experimental", "draft", "candidate", "stable", "deprecated", "retired"):
        assert state in text


def test_schema_is_valid() -> None:
    _validator()


def test_at_least_one_draft_skill_exists_to_exercise_this_policy() -> None:
    assert len(_draft_skill_dirs()) >= 1


@pytest.mark.parametrize("skill_dir", _draft_skill_dirs(), ids=lambda p: p.name)
def test_every_draft_skill_declares_a_valid_preview_block(skill_dir: Path) -> None:
    metadata = _frontmatter(skill_dir).get("metadata", {})
    errors = list(_validator().iter_errors(metadata))
    assert not errors, f"{skill_dir.name}: {[e.message for e in errors]}"


@pytest.mark.parametrize("skill_dir", _draft_skill_dirs(), ids=lambda p: p.name)
def test_known_limitations_are_non_boilerplate_statements(skill_dir: Path) -> None:
    """known_limitations must not be an empty/placeholder statement like 'none'."""
    preview = _frontmatter(skill_dir)["metadata"]["preview"]
    for item in preview["known_limitations"]:
        assert item.strip().casefold() not in {"none", "n/a", "tbd"}
        assert len(item.strip()) >= 10
