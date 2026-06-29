"""Tests for Agile-V skill SKILL.md frontmatter validity."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]

# Directories that contain SKILL.md files at their root
SKILL_DIRS = [
    p
    for p in ROOT.iterdir()
    if p.is_dir()
    and (p / "SKILL.md").exists()
    and not p.name.startswith(".")
    and p.name not in ("node_modules", "tests", "docs", "templates")
]

# Skills under skills/ subdirectory
SKILLS_SUBDIR = ROOT / "skills"
if SKILLS_SUBDIR.exists():
    SKILL_DIRS += [
        p for p in SKILLS_SUBDIR.iterdir() if p.is_dir() and (p / "SKILL.md").exists()
    ]


def _parse_frontmatter(path: Path) -> dict:
    """Extract and parse YAML frontmatter from a SKILL.md."""
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda p: p.name)
def test_skill_has_skill_md(skill_dir: Path):
    assert (skill_dir / "SKILL.md").exists()


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda p: p.name)
def test_skill_has_yaml_frontmatter(skill_dir: Path):
    fm = _parse_frontmatter(skill_dir / "SKILL.md")
    assert fm, f"{skill_dir.name}/SKILL.md has no valid YAML frontmatter"


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda p: p.name)
def test_skill_has_name_field(skill_dir: Path):
    fm = _parse_frontmatter(skill_dir / "SKILL.md")
    assert "name" in fm, f"{skill_dir.name}/SKILL.md missing 'name' in frontmatter"


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda p: p.name)
def test_skill_has_description_field(skill_dir: Path):
    fm = _parse_frontmatter(skill_dir / "SKILL.md")
    assert "description" in fm, (
        f"{skill_dir.name}/SKILL.md missing 'description' in frontmatter"
    )


def test_control_matrix_skill_exists():
    skill_path = ROOT / "agile-v-control-matrix" / "SKILL.md"
    assert skill_path.exists(), "agile-v-control-matrix/SKILL.md not found"


def test_control_matrix_skill_name():
    skill_path = ROOT / "agile-v-control-matrix" / "SKILL.md"
    fm = _parse_frontmatter(skill_path)
    assert fm.get("name") == "agile-v-control-matrix"


def test_control_matrix_skill_has_version():
    skill_path = ROOT / "agile-v-control-matrix" / "SKILL.md"
    fm = _parse_frontmatter(skill_path)
    meta = fm.get("metadata", {})
    assert "version" in meta, "agile-v-control-matrix/SKILL.md missing metadata.version"


def test_control_matrix_skill_has_sections_index():
    skill_path = ROOT / "agile-v-control-matrix" / "SKILL.md"
    fm = _parse_frontmatter(skill_path)
    meta = fm.get("metadata", {})
    assert "sections_index" in meta, (
        "agile-v-control-matrix/SKILL.md missing metadata.sections_index"
    )
    assert isinstance(meta["sections_index"], list)
    assert len(meta["sections_index"]) > 0
