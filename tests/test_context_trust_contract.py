"""Context Trust Contract (AVS-06): untrusted context is data, never authority."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from contracts.semantics import AUTHORITY_BEARING_TARGETS, evaluate_context_influence, load_context_profiles

ROOT = Path(__file__).resolve().parents[1]
PROFILES = load_context_profiles()
SCHEMA = json.loads((ROOT / "schemas/CONTEXT_SOURCE_PROFILE.schema.json").read_text())


def influence(profile, target, mode="activate"):
    return evaluate_context_influence({"source_ref": "x", "context_profile_ref": profile, "target": target,
                                       "mode": mode}, resolve_context_profile=PROFILES.get)


def test_all_initial_profiles_present_and_valid():
    classes = {p["profile"]["source_class"] for p in PROFILES.values()}
    assert classes == {"authenticated_policy_source", "approved_requirement_baseline", "repository_content",
                       "user_prompt", "web_retrieval", "rag_document", "tool_description", "tool_result",
                       "peer_agent_message", "mcp_resource", "generated_wiki"}
    validator = Draft202012Validator(SCHEMA)
    for record in PROFILES.values():
        assert not list(validator.iter_errors(record))


def test_only_control_plane_classes_may_be_authoritative():
    forged = deepcopy(PROFILES["CTX-REPOSITORY-CONTENT"])
    forged["profile"]["default_trust"] = "authoritative"
    assert list(Draft202012Validator(SCHEMA).iter_errors(forged))


def test_untrusted_profile_cannot_list_authority_targets_as_influence():
    forged = deepcopy(PROFILES["CTX-WEB-RETRIEVAL"])
    forged["profile"]["may_influence"].append("approval")
    assert list(Draft202012Validator(SCHEMA).iter_errors(forged))


@pytest.mark.parametrize("ref", [r for r, p in PROFILES.items() if p["profile"]["default_trust"] == "untrusted_data"])
@pytest.mark.parametrize("target", sorted(AUTHORITY_BEARING_TARGETS))
def test_no_untrusted_source_can_activate_authority(ref, target):
    result = influence(ref, target)
    assert result["status"] == "rejected"
    assert result["findings"][0]["code"] == "CONTEXT_AUTHORITY_ESCALATION"


def test_readme_saying_approval_granted():
    assert influence("CTX-REPOSITORY-CONTENT", "approval")["status"] == "rejected"
    assert influence("CTX-REPOSITORY-CONTENT", "approval", "propose")["status"] == "rejected"


def test_web_page_saying_ignore_policy():
    assert influence("CTX-WEB-RETRIEVAL", "policy")["status"] == "rejected"
    assert influence("CTX-WEB-RETRIEVAL", "policy", "propose")["status"] == "rejected"


def test_mcp_tool_description_claims_admin_rights():
    assert influence("CTX-TOOL-DESCRIPTION", "delegated_authority")["status"] == "rejected"


def test_generated_wiki_changes_risk_level():
    assert influence("CTX-GENERATED-WIKI", "risk_level")["status"] == "rejected"


def test_repository_file_claims_risk_l0():
    assert influence("CTX-REPOSITORY-CONTENT", "risk_level")["status"] == "rejected"


def test_peer_agent_claims_manager_role():
    assert influence("CTX-PEER-AGENT-MESSAGE", "delegated_authority")["status"] == "rejected"
    assert influence("CTX-PEER-AGENT-MESSAGE", "approval")["status"] == "rejected"


def test_approved_requirement_baseline_remains_authoritative():
    assert influence("CTX-APPROVED-REQUIREMENT-BASELINE", "approved_requirement") == {
        "status": "admitted", "effect": "activate", "findings": []}


def test_policy_source_cannot_approve_or_decide_gate():
    assert influence("CTX-AUTHENTICATED-POLICY-SOURCE", "approval")["status"] == "rejected"
    assert influence("CTX-AUTHENTICATED-POLICY-SOURCE", "gate_decision")["status"] == "rejected"
    assert influence("CTX-AUTHENTICATED-POLICY-SOURCE", "policy")["effect"] == "activate"


def test_legitimate_proposal_is_preserved_but_not_activated():
    result = influence("CTX-REPOSITORY-CONTENT", "approved_requirement", "propose")
    assert result == {"status": "proposed", "effect": "proposal", "findings": []}
    assert influence("CTX-USER-PROMPT", "policy", "propose")["effect"] == "proposal"


def test_untrusted_content_still_usable_as_data():
    assert influence("CTX-WEB-RETRIEVAL", "implementation_context")["effect"] == "data"


@pytest.mark.parametrize("target, status", [("policy", "rejected"), ("implementation_context", "admitted")])
def test_unknown_source_class_fails_closed_for_authority(target, status):
    result = influence("CTX-UNKNOWN", target)
    assert result["status"] == status
    assert result["findings"][0]["code"] == "CONTEXT_SOURCE_UNKNOWN"


def test_malformed_influence_rejected():
    result = evaluate_context_influence({"target": "policy", "mode": "force"}, resolve_context_profile=PROFILES.get)
    assert result["status"] == "rejected"


def test_ai_run_manifest_can_reference_context_profile():
    schema = json.loads((ROOT / "schemas/AI_RUN_MANIFEST.schema.json").read_text())
    item = schema["$defs"]["named_evidence"]["items"]
    assert item["properties"]["context_profile_ref"]["pattern"] == "^CTX-[A-Z0-9-]+$"
    Draft202012Validator(schema["$defs"]["named_evidence"]).validate(
        [{"name": "https://example.org/page", "context_profile_ref": "CTX-WEB-RETRIEVAL"}])
