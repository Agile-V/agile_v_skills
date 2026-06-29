"""Tests for the Agile-V control matrix template and schema."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "templates" / "agile-v" / "CONTROL_MATRIX.example.yaml"
SCHEMA = ROOT / "templates" / "agile-v" / "CONTROL_MATRIX.schema.json"
FIXTURES = ROOT / "tests" / "fixtures"
INVALID_TOOL_OVERLAP = FIXTURES / "CONTROL_MATRIX.invalid_tool_overlap.yaml"
INVALID_TBD_OWNERS = FIXTURES / "CONTROL_MATRIX.invalid_tbd_owners.yaml"
VALID_FIXTURE = FIXTURES / "CONTROL_MATRIX.valid.yaml"


def _load_example() -> dict:
    return yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))


def _load_schema() -> dict:
    return json.loads(SCHEMA.read_text(encoding="utf-8"))


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------


def test_example_file_exists():
    assert EXAMPLE.exists(), f"Template not found: {EXAMPLE}"


def test_schema_file_exists():
    assert SCHEMA.exists(), f"Schema not found: {SCHEMA}"


# ---------------------------------------------------------------------------
# Parse checks
# ---------------------------------------------------------------------------


def test_example_parses_as_yaml():
    data = _load_example()
    assert isinstance(data, dict)


def test_schema_parses_as_json():
    schema = _load_schema()
    assert isinstance(schema, dict)


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------


def test_example_validates_against_schema():
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        pytest.skip("jsonschema not installed")
    schema = _load_schema()
    data = _load_example()
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(data))
    assert not errors, f"Schema validation errors: {[str(e) for e in errors]}"


# ---------------------------------------------------------------------------
# Required top-level sections
# ---------------------------------------------------------------------------


def test_required_top_level_keys():
    data = _load_example()
    for key in ("version", "default_fail_mode", "controls"):
        assert key in data, f"Missing top-level key: {key}"


def test_controls_is_non_empty_list():
    data = _load_example()
    assert isinstance(data["controls"], list)
    assert len(data["controls"]) > 0


# ---------------------------------------------------------------------------
# Per-control checks
# ---------------------------------------------------------------------------


REQUIRED_CONTROL_KEYS = [
    "id",
    "status",
    "scope",
    "applies_to",
    "minimum_risk_level",
    "data_class",
    "tools",
    "model",
    "logs",
    "max_permissions",
    "human_gates",
    "tests",
    "cost_limit",
    "rollback",
    "owner",
    "review",
]

REQUIRED_OWNER_KEYS = [
    "business_owner",
    "technical_owner",
    "security_owner",
    "reviewer",
]


def test_controls_have_required_keys():
    data = _load_example()
    for control in data["controls"]:
        cid = control.get("id", "<unknown>")
        for key in REQUIRED_CONTROL_KEYS:
            assert key in control, f"Control {cid} missing key: {key}"


def test_controls_have_owner_fields():
    data = _load_example()
    for control in data["controls"]:
        cid = control.get("id", "<unknown>")
        owner = control.get("owner", {})
        for key in REQUIRED_OWNER_KEYS:
            assert key in owner, f"Control {cid} missing owner field: {key}"


def test_draft_controls_may_have_tbd_owners():
    """Draft controls may contain TBD placeholders; active controls must not."""
    data = _load_example()
    for control in data["controls"]:
        if control.get("status") == "active":
            cid = control.get("id", "<unknown>")
            owner = control.get("owner", {})
            for key in REQUIRED_OWNER_KEYS:
                val = owner.get(key, "")
                assert val not in ("TBD", "", None), (
                    f"Active control {cid} has unresolved owner: {key}={val!r}"
                )


# ---------------------------------------------------------------------------
# Tool overlap check
# ---------------------------------------------------------------------------


def test_no_allowed_forbidden_overlap():
    data = _load_example()
    for control in data["controls"]:
        cid = control.get("id", "<unknown>")
        tools = control.get("tools", {})
        allowed = set(tools.get("allowed", []))
        forbidden = set(tools.get("forbidden", []))
        overlap = allowed & forbidden
        assert not overlap, (
            f"Control {cid} has tools in both allowed and forbidden: {sorted(overlap)}"
        )


# ---------------------------------------------------------------------------
# Human gate shape
# ---------------------------------------------------------------------------


def test_human_gates_required_before_shape():
    data = _load_example()
    for control in data["controls"]:
        cid = control.get("id", "<unknown>")
        gates = control.get("human_gates", {}).get("required_before", [])
        for gate in gates:
            assert "action" in gate, f"Control {cid} gate missing 'action'"
            assert "gate" in gate, f"Control {cid} gate missing 'gate'"
            assert "approver_role" in gate, (
                f"Control {cid} gate missing 'approver_role'"
            )


# ---------------------------------------------------------------------------
# Risk level enum
# ---------------------------------------------------------------------------


VALID_RISK_LEVELS = {"L0", "L1", "L2", "L3", "L4"}


def test_minimum_risk_level_valid():
    data = _load_example()
    for control in data["controls"]:
        cid = control.get("id", "<unknown>")
        level = control.get("minimum_risk_level")
        assert level in VALID_RISK_LEVELS, (
            f"Control {cid} has invalid minimum_risk_level: {level!r}"
        )


# ---------------------------------------------------------------------------
# Fail mode
# ---------------------------------------------------------------------------


def test_default_fail_mode_valid():
    data = _load_example()
    assert data.get("default_fail_mode") in ("closed", "open")


# ---------------------------------------------------------------------------
# Fixture existence
# ---------------------------------------------------------------------------


def test_invalid_tool_overlap_fixture_exists():
    assert INVALID_TOOL_OVERLAP.exists(), f"Fixture not found: {INVALID_TOOL_OVERLAP}"


def test_invalid_tbd_owners_fixture_exists():
    assert INVALID_TBD_OWNERS.exists(), f"Fixture not found: {INVALID_TBD_OWNERS}"


def test_valid_fixture_exists():
    assert VALID_FIXTURE.exists(), f"Fixture not found: {VALID_FIXTURE}"


# ---------------------------------------------------------------------------
# Valid fixture passes positive checks
# ---------------------------------------------------------------------------


def test_valid_fixture_parses():
    data = _load_yaml(VALID_FIXTURE)
    assert isinstance(data, dict)
    assert "controls" in data


def test_valid_fixture_no_tool_overlap():
    data = _load_yaml(VALID_FIXTURE)
    for control in data.get("controls", []):
        cid = control.get("id", "<unknown>")
        tools = control.get("tools", {})
        allowed = set(tools.get("allowed", []))
        forbidden = set(tools.get("forbidden", []))
        overlap = allowed & forbidden
        assert not overlap, (
            f"Valid fixture control {cid} has tool overlap: {sorted(overlap)}"
        )


def test_valid_fixture_no_tbd_owners_on_active():
    data = _load_yaml(VALID_FIXTURE)
    for control in data.get("controls", []):
        if control.get("status") == "active":
            cid = control.get("id", "<unknown>")
            owner = control.get("owner", {})
            for key in (
                "business_owner",
                "technical_owner",
                "security_owner",
                "reviewer",
            ):
                val = owner.get(key, "")
                assert val not in ("TBD", "", None), (
                    f"Valid fixture active control {cid} has unresolved owner: {key}={val!r}"
                )


# ---------------------------------------------------------------------------
# Negative tests: invalid fixtures must fail their respective checks
# ---------------------------------------------------------------------------


def test_invalid_tool_overlap_fixture_detected():
    """The tool-overlap fixture must trigger an overlap failure."""
    data = _load_yaml(INVALID_TOOL_OVERLAP)
    found_overlap = False
    for control in data.get("controls", []):
        tools = control.get("tools", {})
        allowed = set(tools.get("allowed", []))
        forbidden = set(tools.get("forbidden", []))
        if allowed & forbidden:
            found_overlap = True
            break
    assert found_overlap, (
        "Expected CONTROL_MATRIX.invalid_tool_overlap.yaml to contain a tool overlap "
        "but none was detected — fix the fixture."
    )


def test_invalid_tbd_owners_fixture_detected():
    """The TBD-owners fixture must have an active control with TBD owner fields."""
    data = _load_yaml(INVALID_TBD_OWNERS)
    found_tbd = False
    for control in data.get("controls", []):
        if control.get("status") == "active":
            owner = control.get("owner", {})
            for key in (
                "business_owner",
                "technical_owner",
                "security_owner",
                "reviewer",
            ):
                if owner.get(key) in ("TBD", "", None):
                    found_tbd = True
                    break
        if found_tbd:
            break
    assert found_tbd, (
        "Expected CONTROL_MATRIX.invalid_tbd_owners.yaml to contain an active control "
        "with TBD owner fields but none was detected — fix the fixture."
    )


def test_invalid_tool_overlap_would_fail_positive_check():
    """Confirm the overlap fixture would be caught by the positive test logic."""
    data = _load_yaml(INVALID_TOOL_OVERLAP)
    violations = []
    for control in data.get("controls", []):
        cid = control.get("id", "<unknown>")
        tools = control.get("tools", {})
        allowed = set(tools.get("allowed", []))
        forbidden = set(tools.get("forbidden", []))
        overlap = allowed & forbidden
        if overlap:
            violations.append((cid, sorted(overlap)))
    assert violations, (
        "CONTROL_MATRIX.invalid_tool_overlap.yaml did not produce any violations — "
        "the fixture is not actually invalid."
    )


def test_invalid_tbd_owners_would_fail_positive_check():
    """Confirm the TBD-owners fixture would be caught by the positive test logic."""
    data = _load_yaml(INVALID_TBD_OWNERS)
    violations = []
    for control in data.get("controls", []):
        if control.get("status") == "active":
            cid = control.get("id", "<unknown>")
            owner = control.get("owner", {})
            for key in (
                "business_owner",
                "technical_owner",
                "security_owner",
                "reviewer",
            ):
                val = owner.get(key, "")
                if val in ("TBD", "", None):
                    violations.append((cid, key, val))
    assert violations, (
        "CONTROL_MATRIX.invalid_tbd_owners.yaml did not produce any violations — "
        "the fixture is not actually invalid."
    )
