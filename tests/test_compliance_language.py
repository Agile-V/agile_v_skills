"""Contract test for PR-S12: bounded compliance-language claims.

'Automated Compliance' can be misread as an assertion that Agile V itself
establishes compliance. Enforce the replacement wording repo-wide so it is
not silently reintroduced, and ensure the core skill still carries the
qualifying disclaimer next to the value.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def test_automated_compliance_value_label_is_not_used() -> None:
    pattern = re.compile(r"automated compliance\b", re.IGNORECASE)
    for path in ROOT.rglob("*.md"):
        if any(part.startswith(".") or part == "node_modules" for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert not pattern.search(text), f"{path.relative_to(ROOT)} still uses the unqualified 'Automated Compliance' label"


def test_core_skill_uses_bounded_replacement_and_disclaimer() -> None:
    core = _normalized((ROOT / "agile-v-core" / "SKILL.md").read_text(encoding="utf-8"))
    assert "automated assurance evidence" in core
    assert "does not itself establish conformity certification regulatory approval or legal compliance" in core
