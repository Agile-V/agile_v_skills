"""Repository discovery and contribution surfaces remain complete and current."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_community_health_files_exist() -> None:
    required = {
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CITATION.cff",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/ISSUE_TEMPLATE/config.yml",
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/feature_request.yml",
        ".github/ISSUE_TEMPLATE/skill_proposal.yml",
    }
    missing = {path for path in required if not (ROOT / path).is_file()}
    assert not missing


def test_community_yaml_is_valid() -> None:
    paths = [ROOT / "CITATION.cff", *sorted((ROOT / ".github/ISSUE_TEMPLATE").glob("*.yml"))]
    for path in paths:
        assert isinstance(yaml.safe_load(path.read_text(encoding="utf-8")), dict), path


def test_public_docs_link_to_growth_resources() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    docs = (ROOT / "docs/README.md").read_text(encoding="utf-8")
    for link in ("docs/tutorials/README.md", "docs/COMPARISONS.md", "docs/SHOWCASE.md"):
        assert link in readme
    for link in ("OUTREACH_KIT.md", "GROWTH_METRICS.md"):
        assert link in docs
