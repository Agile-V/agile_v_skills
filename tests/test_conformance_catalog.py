"""Contract tests for the cross-platform conformance catalog (PR-S10).

Validates conformance/scenarios.yaml structure and that every 'tested'
scenario's test_ref resolves to a real, collectible test function in this
repository's own suite. Does not execute against external agent platforms
(see conformance/README.md scope note).
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "conformance" / "scenarios.yaml"
README = ROOT / "conformance" / "README.md"

VALID_STATUSES = {"specified", "implemented", "tested"}


def _load_catalog() -> dict:
    yaml = pytest.importorskip("yaml")
    return yaml.safe_load(CATALOG.read_text(encoding="utf-8"))


def test_conformance_readme_and_catalog_exist() -> None:
    assert README.exists()
    assert CATALOG.exists()


def test_readme_states_scope_and_does_not_overclaim() -> None:
    text = README.read_text(encoding="utf-8").casefold()
    assert "does **not** currently execute live scenarios against" in text
    assert "do not claim multi-platform conformance until that harness exists" in text


def test_catalog_has_ten_scenarios_with_valid_status() -> None:
    catalog = _load_catalog()
    scenarios = catalog["scenarios"]
    assert len(scenarios) == 10
    ids = [s["id"] for s in scenarios]
    assert ids == [f"C-{n:03}" for n in range(1, 11)]
    for scenario in scenarios:
        assert scenario["status"] in VALID_STATUSES
        assert scenario["expected_behavior"].strip()


@pytest.mark.parametrize(
    "scenario_id",
    [f"C-{n:03}" for n in range(1, 11)],
)
def test_tested_scenarios_have_resolvable_test_ref(scenario_id: str) -> None:
    catalog = _load_catalog()
    scenario = next(s for s in catalog["scenarios"] if s["id"] == scenario_id)
    if scenario["status"] != "tested":
        pytest.skip(f"{scenario_id} is status={scenario['status']}, not tested")
    test_ref = scenario["test_ref"]
    assert test_ref, f"{scenario_id} is marked tested but has no test_ref"
    path_part, _, func_name = test_ref.partition("::")
    test_path = ROOT / path_part
    assert test_path.exists(), f"{scenario_id} test_ref path does not exist: {path_part}"
    content = test_path.read_text(encoding="utf-8")
    assert re.search(rf"def {re.escape(func_name)}\(", content), (
        f"{scenario_id} test_ref function '{func_name}' not found in {path_part}"
    )


def test_specified_only_scenarios_do_not_claim_a_test_ref() -> None:
    catalog = _load_catalog()
    for scenario in catalog["scenarios"]:
        if scenario["status"] == "specified":
            assert scenario["test_ref"] is None


def test_platforms_target_list_is_explicitly_not_yet_executed() -> None:
    catalog = _load_catalog()
    assert len(catalog["platforms_target_not_yet_executed"]) >= 4
