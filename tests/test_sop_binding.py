"""The SOP binding validator and example template must be self-consistent."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "agile-v-sop-adapter" / "validate.py"
EXAMPLE = ROOT / "templates" / "agile-v" / "SOP_BINDING.example.yaml"
SCHEMA = ROOT / "templates" / "agile-v" / "SOP_BINDING.schema.json"


def _load_validator():
    spec = importlib.util.spec_from_file_location("sop_binding_validate", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_validator_and_example_exist() -> None:
    assert VALIDATOR.is_file()
    assert EXAMPLE.is_file()
    assert SCHEMA.is_file()


def test_example_is_valid_non_strict() -> None:
    mod = _load_validator()
    binding = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    assert mod.validate(binding, mod.DEFAULT_DENY) == []


def test_example_gap_fails_strict() -> None:
    mod = _load_validator()
    binding = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    # The example intentionally includes one status:"gap" entry.
    assert mod.conformance_gaps(binding), "example should carry a demonstrative gap"


def test_validator_rejects_wrong_source_of_truth() -> None:
    mod = _load_validator()
    binding = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    binding["source_of_truth"] = "binding"
    errors = mod.validate(binding, mod.DEFAULT_DENY)
    assert any("source_of_truth" in e for e in errors)


def test_validator_flags_mapped_without_realization() -> None:
    mod = _load_validator()
    binding = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    for entry in binding["bindings"]:
        if entry["status"] == "mapped":
            entry.pop("agile_v", None)
            break
    errors = mod.validate(binding, mod.DEFAULT_DENY)
    assert any("agile_v.control or agile_v.artifact" in e for e in errors)


def test_validator_leak_guard_catches_embedded_prose() -> None:
    mod = _load_validator()
    binding = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    binding["bindings"][0]["title"] = "The system shall X and the system shall Y"
    errors = mod.validate(binding, mod.DEFAULT_DENY)
    assert any("embedded SOP body text" in e for e in errors)
