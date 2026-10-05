"""Agile-V OpenTelemetry Contract (AVS-07): privacy-safe, correlatable, not evidence."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from admission_support import load
from tools.telemetry_to_otlp import to_otlp

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/AGILE_V_TELEMETRY_EVENT.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
EVENTS = json.loads((ROOT / "examples/telemetry/gate-flow.default.json").read_text())["events"]


def errors(event):
    return list(VALIDATOR.iter_errors(event))


@pytest.mark.parametrize("event", EVENTS, ids=lambda e: e["name"])
def test_examples_validate(event):
    assert not errors(event)
    assert event["privacy_profile"] == "default"


def gate_event():
    return deepcopy(next(e for e in EVENTS if e["name"] == "agilev.gate.evaluate"))


def test_required_event_identity():
    event = gate_event()
    del event["attributes"]["agilev.task.id"]
    assert errors(event)
    event = gate_event()
    event["name"] = "agilev.made.up"
    assert errors(event)


def test_reason_codes_serialization():
    event = gate_event()
    event["attributes"]["agilev.reason_codes"] = "APPROVAL_NOT_JUSTIFIED"
    assert errors(event)
    event["attributes"]["agilev.reason_codes"] = ["approval not justified"]
    assert errors(event)
    event["attributes"]["agilev.reason_codes"] = ["APPROVAL_NOT_JUSTIFIED"]
    assert not errors(event)


def test_reject_event_requires_reason():
    event = deepcopy(next(e for e in EVENTS if e["name"] == "agilev.evidence.reject"))
    event["attributes"]["agilev.reason_codes"] = []
    assert errors(event)


@pytest.mark.parametrize("key", ["gen_ai.input.messages", "gen_ai.output.messages", "gen_ai.system_instructions",
                                 "gen_ai.tool.call.arguments"])
def test_default_profile_forbids_content(key):
    event = gate_event()
    event["attributes"][key] = "user said ..."
    assert errors(event)


@pytest.mark.parametrize("key", ["agilev.reasoning", "gen_ai.chain_of_thought", "agilev.thinking.text",
                                 "service.api_key", "agilev.secret", "error.credential"])
def test_hidden_cot_and_secrets_forbidden_in_every_profile(key):
    for profile in ("default", "extended"):
        event = gate_event()
        event["privacy_profile"] = profile
        event["attributes"][key] = "x"
        assert errors(event), (key, profile)


def test_unknown_namespace_rejected():
    event = gate_event()
    event["attributes"]["myvendor.score"] = 1
    assert errors(event)


def test_digests_must_be_valid():
    event = gate_event()
    event["attributes"]["agilev.subject.digest"] = "sha256:abc"
    assert errors(event)


def test_events_correlate_to_gate_receipt_and_ai_run():
    receipt = load("gate_receipt.positive.json")["gate_receipt"]
    event = gate_event()["attributes"]
    assert event["agilev.gate.receipt_id"] == receipt["id"]
    assert event["agilev.task.id"] == receipt["task_id"]
    assert event["agilev.subject.digest"] == receipt["subject_state"]["subject_digest"]
    assert event["agilev.policy.digest"] == receipt["policy"]["policy_digest"]
    run_ids = {e["attributes"].get("agilev.agent_run.id") for e in EVENTS} - {None}
    assert run_ids == {"RUN-0042"}


def test_otlp_conversion_is_generic():
    otlp = to_otlp(EVENTS)
    spans = otlp["resourceSpans"][0]["scopeSpans"][0]["spans"]
    assert len(spans) == len(EVENTS)
    assert all(len(s["traceId"]) == 32 and len(s["spanId"]) == 16 for s in spans)
    keys = {a["key"] for s in spans for a in s["attributes"]}
    assert "agilev.reason_codes" in keys and "service.name" not in keys
