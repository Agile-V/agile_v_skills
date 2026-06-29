"""Tests for Agile-V skill SKILL.md frontmatter validity."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

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

# Regex to extract ## headings from markdown body
_H2_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)


def _parse_frontmatter(path: Path) -> dict:
    """Extract and parse YAML frontmatter from a SKILL.md.

    Raises ``pytest.fail`` (rather than silently returning ``{}``) when the
    frontmatter block exists but contains invalid YAML, so failures are
    immediately actionable.
    """
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    raw_yaml = parts[1]
    try:
        result = yaml.safe_load(raw_yaml)
        return result or {}
    except yaml.YAMLError as exc:
        pytest.fail(
            f"{path.relative_to(ROOT)} contains invalid YAML frontmatter:\n{exc}"
        )


def _extract_body(path: Path) -> str:
    """Return the markdown body (everything after the closing ``---``)."""
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return content
    parts = content.split("---", 2)
    return parts[2] if len(parts) >= 3 else ""


def _body_h2_headings(path: Path) -> list[str]:
    """Return a list of all ``##`` heading titles found in the body."""
    body = _extract_body(path)
    return [m.group(1).strip() for m in _H2_RE.finditer(body)]


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


# ---------------------------------------------------------------------------
# Control-matrix skill specific tests
# ---------------------------------------------------------------------------


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


def test_control_matrix_sections_index_matches_headings():
    """Every entry in sections_index must correspond to a ## heading in the body."""
    skill_path = ROOT / "agile-v-control-matrix" / "SKILL.md"
    fm = _parse_frontmatter(skill_path)
    meta = fm.get("metadata", {})
    sections_index: list[str] = meta.get("sections_index", [])
    if not sections_index:
        pytest.skip("sections_index is empty — covered by other test")

    actual_headings = _body_h2_headings(skill_path)
    missing = [s for s in sections_index if s not in actual_headings]
    assert not missing, (
        "sections_index entries not found as ## headings in agile-v-control-matrix/SKILL.md:\n"
        + "\n".join(f"  - {s!r}" for s in missing)
        + f"\nActual ## headings: {actual_headings}"
    )
