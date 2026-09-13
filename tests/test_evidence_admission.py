"""Contract tests for the Evidence Admission Contract (PR-S01).

Verifies that the claim/evidence/admissibility vocabulary exists, that the
frozen-verification-baseline rule is stated normatively, and that no skill
permits Evolve to weaken the active cycle's acceptance criteria before Verify.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "agile-v-runtime" / "07_EVIDENCE_ADMISSION_CONTRACT.md"


def _text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def test_evidence_admission_contract_exists() -> None:
    assert CONTRACT.exists(), "docs/agile-v-runtime/07_EVIDENCE_ADMISSION_CONTRACT.md must exist"


def test_evidence_admission_contract_defines_core_vocabulary() -> None:
    text = _normalized(CONTRACT.read_text(encoding="utf-8"))
    for term in (
        "claim",
        "evidence candidate",
        "evidence presence",
        "structural completeness",
        "evidential sufficiency",
        "evidence admissibility",
        "stale",
        "gate receipt",
        "historically valid",
        "currently eligible",
    ):
        assert _normalized(term) in text, f"missing term: {term}"


def test_implication_hierarchy_is_stated() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "admissible -> sufficient -> structurally complete -> present" in text


def test_frozen_baseline_rule_is_normative() -> None:
    text = _normalized(CONTRACT.read_text(encoding="utf-8"))
    assert "verification baseline" in text
    assert "frozen" in text
    assert _normalized("Evolve may propose control, policy, or skill/process changes") in text or (
        "evolve" in text and "propose" in text
    )


def test_core_skill_states_frozen_baseline_and_evolve_proposal_only_rule() -> None:
    core = _normalized(_text("agile-v-core/SKILL.md"))
    assert "frozen baseline" in core
    assert "evidence admission contract" in core
    assert (
        "never by editing the current cycle s criteria before verify runs" in core
        or "never alter the active task s frozen verification baseline" in core
    )


def test_lifecycle_contract_cross_references_admission_contract() -> None:
    lifecycle = _text("docs/agile-v-runtime/03_CANONICAL_LIFECYCLE_CONTRACT.md")
    assert "07_EVIDENCE_ADMISSION_CONTRACT.md" in lifecycle


def test_agile_v_lifecycle_change_requests_are_sole_baseline_change_mechanism() -> None:
    lifecycle_skill = _normalized(_text("agile-v-lifecycle/SKILL.md"))
    assert "only mechanism that may change the frozen verification baseline" in lifecycle_skill


def test_no_skill_instructs_evolve_to_edit_active_criteria() -> None:
    """No skill may instruct editing/weakening/relaxing active-cycle acceptance
    criteria, thresholds, or policy directly from Evolve (must go through a CR)."""
    forbidden_patterns = [
        re.compile(r"evolve[^.]{0,80}(weaken|relax|lower)[^.]{0,80}(criteria|threshold|policy)"),
        re.compile(r"(weaken|relax|lower)[^.]{0,80}(criteria|threshold|policy)[^.]{0,80}before verify"),
    ]
    for path in ROOT.rglob("SKILL.md"):
        if any(part.startswith(".") or part == "node_modules" for part in path.parts):
            continue
        text = _normalized(path.read_text(encoding="utf-8"))
        for pattern in forbidden_patterns:
            assert not pattern.search(text), f"{path.relative_to(ROOT)} appears to permit Evolve to weaken active criteria"
