"""Deterministic behavioral contract tests for the Markdown skill library."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "behavioral_contracts.yaml"
SOURCE_CASES = ROOT / "skills" / "system-understanding-agent" / "tests"


@pytest.fixture(scope="module")
def contracts() -> dict:
    return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))


def _text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def _semantic_words(value: str) -> set[str]:
    stop_words = {"a", "an", "for", "the", "this", "to"}
    return set(_normalized(value).split()) - stop_words


def _table_rows(markdown: str) -> list[list[str]]:
    rows = []
    for line in markdown.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and not all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            rows.append(cells)
    return rows


def _understanding_decision(facts: dict) -> str:
    blockers = (
        facts.get("ambiguous_change")
        or facts.get("graph_invalid")
        or not facts.get("context_available", False)
        or (
            facts.get("confidence") == "Low"
            and not facts.get("human_acknowledged", False)
        )
    )
    return "halt" if blockers else "proceed"


def _understanding_activation(case: dict) -> str:
    signal = _normalized(case.get("signal", ""))
    facts = case.get("facts", {})
    signal_triggers = (
        "understand anything knowledge graph json",
        "what does this system do",
        "what will this change affect",
        "onboarding guide",
        "traceability matrix",
    )
    activates = (
        any(trigger in signal for trigger in signal_triggers)
        or facts.get("existing_repository", False)
        or facts.get("changed_files", 0) > 3
        or facts.get("risk_level") in {"L3", "L4"}
    )
    return "activate" if activates else "skip"


def _route(phrase: str) -> str | None:
    words = _semantic_words(phrase)
    routes = (
        ({"system", "does", "do"}, "system-understanding-agent"),
        ({"could", "break"}, "impact-analysis-agent"),
        ({"ambiguity"}, "logic-gatekeeper"),
        ({"implement", "features"}, "build-agent"),
        ({"design", "verification", "suite"}, "test-designer"),
        ({"challenge", "code"}, "red-team-verifier"),
    )
    return next((skill for trigger, skill in routes if trigger <= words), None)


def _approval_decision(facts: dict) -> str:
    if facts.get("external_effect") == "none":
        return "proceed"
    if facts.get("approval") != "approved":
        return "halt"
    if facts.get("resume_token_matches") is False:
        return "halt"
    return "proceed"


def _trace_decision(record: dict) -> str:
    required = {"artifact_id", "requirement_id", "revision", "baseline"}
    valid_ids = bool(
        re.fullmatch(r"ART-[A-Z0-9-]+", record.get("artifact_id", ""))
        and re.fullmatch(r"REQ-[A-Z0-9-]+", record.get("requirement_id", ""))
    )
    complete = required <= record.keys() and record.get("relation") == "implements" and valid_ids
    return "complete" if complete else "incomplete"


def test_markdown_system_understanding_cases_are_executable(contracts: dict):
    """Every existing AC/NC Markdown case must have a structured expectation."""
    markdown_ids = set()
    for name in ("activation_cases.md", "negative_cases.md"):
        markdown_ids.update(re.findall(r"\b(?:AC|NC)-\d{3}\b", _text(str((SOURCE_CASES / name).relative_to(ROOT)))))

    fixture_ids = {
        case["id"]
        for group in contracts["system_understanding_cases"].values()
        for case in group
    }
    assert markdown_ids <= fixture_ids, f"Markdown cases missing structured fixtures: {sorted(markdown_ids - fixture_ids)}"


@pytest.mark.parametrize("case_id", [f"AC-{number:03}" for number in range(1, 9)])
def test_system_understanding_activation_cases(contracts: dict, case_id: str):
    cases = {case["id"]: case for case in contracts["system_understanding_cases"]["activation"]}
    case = cases[case_id]
    assert _understanding_activation(case) == case["expected"]


@pytest.mark.parametrize("case_id", [f"NC-{number:03}" for number in range(1, 5)] + ["PC-001", "PC-002"])
def test_halt_vs_proceed_contract(contracts: dict, case_id: str):
    cases = {case["id"]: case for case in contracts["system_understanding_cases"]["decisions"]}
    case = cases[case_id]
    assert _understanding_decision(case["facts"]) == case["expected"]


def test_system_understanding_static_contract_supports_cases(contracts: dict):
    skill = _normalized(_text("skills/system-understanding-agent/SKILL.md"))
    required_clauses = (
        "continue with available context",
        "confidence is low and no human has explicitly accepted it",
        "no system context can be found",
        "ambiguous change request",
        "do not begin implementation",
    )
    for clause in required_clauses:
        assert _normalized(clause) in skill

    explicit_trigger_cases = {"AC-001", "AC-002", "AC-003", "AC-005"}
    for case in contracts["system_understanding_cases"]["activation"]:
        if case["id"] not in explicit_trigger_cases:
            continue
        if signal := case.get("signal"):
            assert _normalized(signal) in skill, f"{case['id']} signal is absent from skill triggers"


def test_system_understanding_artifact_contract(contracts: dict):
    expected = contracts["artifact_contract"]
    skill = _text("skills/system-understanding-agent/SKILL.md")
    source = _text("skills/system-understanding-agent/tests/expected_artifacts.md")
    for artifact in expected["always"] + expected["with_graph"]:
        assert artifact in skill and artifact in source
    for section in expected["overview_sections"]:
        assert re.search(rf"^## {re.escape(section)}\s*$", skill, re.MULTILINE)


def test_representative_routing_contracts(contracts: dict):
    catalog = json.loads(_text("catalog/skills.json"))
    by_name = {entry["name"]: entry for entry in catalog["skills"]}
    for case in contracts["routing_cases"]:
        skill = case["expected_skill"]
        assert _route(case["phrase"]) == skill
        assert by_name[skill]["routing"]["intent"].strip()
        assert by_name[skill]["status"] == "released"


@pytest.mark.parametrize("case_id", [f"APPROVAL-{number:03}" for number in range(1, 6)])
def test_unsafe_actions_require_durable_approval(contracts: dict, case_id: str):
    cases = {case["id"]: case for case in contracts["approval_cases"]}
    case = cases[case_id]
    assert _approval_decision(case["facts"]) == case["expected"]


def test_approval_rules_are_present_in_static_skills():
    core = _normalized(_text("agile-v-core/SKILL.md"))
    compliance = _normalized(_text("agile-v-compliance/SKILL.md"))
    assert "no deployments without approval" in core
    assert "resume only from file state matching token" in core
    assert "rejected pipeline halts" in compliance
    assert "matching agile v checkpoints md" in compliance


def test_build_test_and_verification_independence():
    build = _normalized(_text("build-agent/SKILL.md"))
    designer = _normalized(_text("test-designer/SKILL.md"))
    verifier = _normalized(_text("red-team-verifier/SKILL.md"))
    routing = _normalized(_text("SKILL_ROUTING_GUIDE.md"))
    assert "do not verify your own work" in build
    assert "design verification from requirements alone never from implementation" in designer
    assert "do not read build agent code schematics or implementation artifacts" in designer
    assert "you do not verify your own work" in verifier
    assert "preserve independence with separate fresh contexts" in routing
    assert "build agent test designer independent" in routing


def test_draft_skills_do_not_leak_as_released(contracts: dict):
    catalog = json.loads(_text("catalog/skills.json"))
    catalog_status = {entry["name"]: entry["status"] for entry in catalog["skills"]}
    routing_rows = _table_rows(_text("SKILL_ROUTING_GUIDE.md"))
    draft_skills = set()
    for path in ROOT.rglob("SKILL.md"):
        frontmatter = yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])
        if frontmatter.get("metadata", {}).get("status") == "draft":
            draft_skills.add(frontmatter["name"])

    assert set(contracts["draft_skills"]) <= draft_skills
    for skill in draft_skills:
        assert catalog_status[skill] == "draft"
        for source, rows in (("routing guide", routing_rows),):
            catalog_rows = [row for row in rows if skill in " ".join(row)]
            assert catalog_rows, f"{skill} missing from {source}"
            marked_rows = [
                row for row in catalog_rows
                if {"draft", "preview"} & _semantic_words(" ".join(row))
            ]
            assert marked_rows, f"{skill} has no Preview/Draft catalog entry in {source}"
            assert all(
                not ({"official", "released"} & _semantic_words(" ".join(row)))
                for row in marked_rows
            ), f"{skill} is presented as released in {source}"


@pytest.mark.parametrize("case_id", [f"TRACE-{number:03}" for number in range(1, 6)])
def test_trace_completeness_contract(contracts: dict, case_id: str):
    cases = {case["id"]: case for case in contracts["trace_cases"]}
    case = cases[case_id]
    assert _trace_decision(case["record"]) == case["expected"]


def test_static_trace_contract_requires_typed_complete_lineage():
    core = _normalized(_text("agile-v-core/SKILL.md"))
    designer = _normalized(_text("test-designer/SKILL.md"))
    graph = _normalized(_text("skills/graph-traceability-agent/SKILL.md"))
    assert "artifact implements baselined requirement" in core
    assert "req id revision baseline reference" in core
    assert "test case verifies baselined requirement" in designer
    assert "req xxxx revision and baseline reference" in designer
    assert "do not invent traceability links" in graph
    assert "orphan requirement" in graph and "orphan change" in graph
