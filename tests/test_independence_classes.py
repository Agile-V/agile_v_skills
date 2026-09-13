"""Contract tests for the Independence Classes taxonomy (PR-S02).

Ensures I0-I4 are normatively defined, risk levels declare a minimum class,
and that "independent" claims in verification-adjacent skills are qualified
rather than left as an unqualified absolute.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAXONOMY = ROOT / "docs" / "agile-v-runtime" / "08_INDEPENDENCE_CLASSES.md"


def _text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def test_independence_taxonomy_exists() -> None:
    assert TAXONOMY.exists()


def test_all_five_classes_defined() -> None:
    text = TAXONOMY.read_text(encoding="utf-8")
    for code in ("I0", "I1", "I2", "I3", "I4"):
        assert re.search(rf"`{code}`", text), f"{code} not defined"


def test_fresh_context_is_not_organizational_assurance() -> None:
    text = _normalized(TAXONOMY.read_text(encoding="utf-8"))
    assert "fresh context" in text
    assert "does not constitute" in text or "never satisfies" in text or "at most" in text


def test_risk_classification_declares_minimum_independence_class() -> None:
    risk = _text("docs/agile-v-runtime/04_RISK_CLASSIFICATION.md")
    assert "Minimum independence class" in risk
    assert "08_INDEPENDENCE_CLASSES.md" in risk
    for code in ("I0", "I1", "I2", "I3", "I4"):
        assert f"`{code}`" in risk


def test_core_skill_references_independence_classes() -> None:
    core = _text("agile-v-core/SKILL.md")
    assert "08_INDEPENDENCE_CLASSES.md" in core


def test_red_team_and_test_designer_qualify_independence_claims() -> None:
    verifier = _text("red-team-verifier/SKILL.md")
    designer = _text("test-designer/SKILL.md")
    assert "08_INDEPENDENCE_CLASSES.md" in verifier
    assert "08_INDEPENDENCE_CLASSES.md" in designer
    # The Red Team Protocol sentence itself must remain intact (existing contract).
    assert "you do not verify your own work" in _normalized(verifier)


def test_human_oversight_profile_maps_to_independence_classes() -> None:
    hoc = _text("agile-v-human-oversight/SKILL.md")
    assert "08_INDEPENDENCE_CLASSES.md" in hoc


def test_gxp_dq_independence_is_class_qualified() -> None:
    gxp = _text("agile-v-gxp-qualification/SKILL.md")
    assert "08_INDEPENDENCE_CLASSES.md" in gxp


def test_no_skill_asserts_second_agent_alone_is_organizational_assurance() -> None:
    """No skill may claim that a second AI agent, by itself, constitutes I3/I4
    organizational assurance."""
    forbidden = re.compile(
        r"(second agent|another agent|different agent)[^.]{0,60}"
        r"(is|constitutes|satisfies)[^.]{0,40}(independent assurance|organizational(ly)? independent)"
    )
    for path in ROOT.rglob("SKILL.md"):
        if any(part.startswith(".") or part == "node_modules" for part in path.parts):
            continue
        text = _normalized(path.read_text(encoding="utf-8"))
        assert not forbidden.search(text), f"{path.relative_to(ROOT)} over-claims agent-only independence"
