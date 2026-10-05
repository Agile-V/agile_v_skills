"""Delegation Contract v2: authority must attenuate (AVS-05).

Every privilege-escalation path must fail closed with an explainable code.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path

import pytest

from admission_support import load
from contracts.semantics import _schema_findings, delegation_chain_is_valid, evaluate_delegation

NOW = datetime(2026, 9, 15, tzinfo=timezone.utc)
ROOT = Path(__file__).resolve().parents[1]

AUTHORITY = {"authority": {
    "id": "AUTH-LEAD-1", "holder_identity_ref": "ID-ORCH", "task_id": "AAV-0042", "status": "active",
    "expires_at": "2026-09-30T00:00:00Z",
    "authority_ceiling": {"max_risk_level": "L3", "max_side_effect": "external_state",
                          "may_delegate_further": True, "max_delegation_depth": 2},
    "scope": {"requirements": ["REQ-1", "REQ-2", "REQ-3"], "actions": ["edit", "test", "release"],
              "resources": ["ART-1", "ART-2", "ART-3"], "tools": ["fs.write", "pytest", "git.push"],
              "data_classes": ["internal", "confidential"]}}}


def root():
    return load("agent_delegation_record_v2.positive.json")


def child(**changes):
    record = deepcopy(root())
    record["delegation"].update(id="DEL-CHILD-1", parent_delegation_ref="DEL-ROOT-1",
                                nonce="n-child-000000000000001", expires_at="2026-09-19T00:00:00Z")
    record["delegator"] = {"agent_id": "build-agent", "authenticated_identity_ref": "ID-BUILD"}
    record["delegate"] = {"agent_id": "test-runner", "authenticated_identity_ref": "ID-TEST"}
    record["authority_ceiling"].update(may_delegate_further=False, max_delegation_depth=0)
    record["scope"] = {"requirements": ["REQ-1"], "actions": ["test"], "resources": ["ART-1"],
                       "tools": ["pytest"], "data_classes": ["internal"]}
    for path, value in changes.items():
        section, key = path.split("__")
        record[section][key] = value
    return record


def evaluate(record, store=None, authorities=None, **kwargs):
    store = {"DEL-ROOT-1": root()} if store is None else store
    authorities = {"AUTH-LEAD-1": AUTHORITY} if authorities is None else authorities
    return evaluate_delegation(record, resolve_delegation=store.get, resolve_authority=authorities.get,
                               now=NOW, is_nonce_consumed=lambda nonce: False, **kwargs)


def codes(result):
    return {f["code"] for f in result["findings"]}


def test_schema_fixtures():
    assert not _schema_findings(root(), "AGENT_DELEGATION_RECORD.v2")
    assert _schema_findings(load("agent_delegation_record_v2.negative.json"), "AGENT_DELEGATION_RECORD.v2")


def test_v1_schema_remains_readable_and_unchanged():
    v1 = json.loads((ROOT / "schemas/AGENT_DELEGATION_RECORD.schema.json").read_text())
    assert v1["properties"]["record_type"]["const"] == "agile-v-agent-delegation-record"
    assert "schema_version" not in v1["properties"]


def test_valid_root_and_attenuated_child():
    assert evaluate(root())["status"] == "admitted"
    result = evaluate(child())
    assert result == {"status": "admitted", "findings": [], "chain": ["DEL-CHILD-1", "DEL-ROOT-1"]}
    assert delegation_chain_is_valid(child(), resolve_delegation={"DEL-ROOT-1": root()}.get,
                                     resolve_authority={"AUTH-LEAD-1": AUTHORITY}.get, now=NOW)


@pytest.mark.parametrize("field, value", [
    ("resources", ["ART-1", "ART-9"]), ("actions", ["test", "release"]), ("tools", ["pytest", "git.push"]),
    ("data_classes", ["confidential"]), ("requirements", ["REQ-3"])])
def test_scope_expansion_rejected(field, value):
    record = child()
    record["scope"][field] = value
    result = evaluate(record)
    assert {"code": "DELEGATION_SCOPE_EXPANSION", "delegation_ref": "DEL-CHILD-1", "field": field} in result["findings"]


def test_wildcard_is_not_a_grant():
    record = child()
    record["scope"]["resources"] = ["*"]
    assert "DELEGATION_SCOPE_EXPANSION" in codes(evaluate(record))


def test_risk_escalation_rejected():
    assert "DELEGATION_RISK_ESCALATION" in codes(evaluate(child(authority_ceiling__max_risk_level="L3")))


def test_side_effect_escalation_rejected():
    assert "DELEGATION_SIDE_EFFECT_ESCALATION" in codes(evaluate(child(authority_ceiling__max_side_effect="irreversible")))


def test_longer_expiry_rejected():
    assert "DELEGATION_EXPIRY_EXTENDED" in codes(evaluate(child(delegation__expires_at="2026-09-25T00:00:00Z")))


def test_excessive_depth_rejected():
    record = child(authority_ceiling__may_delegate_further=True, authority_ceiling__max_delegation_depth=1)
    assert "DELEGATION_DEPTH_EXCEEDED" in codes(evaluate(record))


def test_redelegation_without_parent_permission_rejected():
    parent = root()
    parent["authority_ceiling"].update(may_delegate_further=False, max_delegation_depth=0)
    assert "DELEGATION_REDELEGATION_NOT_PERMITTED" in codes(evaluate(child(), store={"DEL-ROOT-1": parent}))


def test_root_cannot_exceed_authority():
    record = root()
    record["authority_ceiling"]["max_risk_level"] = "L4"
    record["scope"]["actions"].append("deploy")
    assert {"DELEGATION_RISK_ESCALATION", "DELEGATION_SCOPE_EXPANSION"} <= codes(evaluate(record))


def test_replayed_single_use_delegation_rejected():
    record = child(delegation__single_use=True)
    result = evaluate_delegation(record, resolve_delegation={"DEL-ROOT-1": root()}.get,
                                 resolve_authority={"AUTH-LEAD-1": AUTHORITY}.get, now=NOW,
                                 is_nonce_consumed=lambda nonce: True)
    assert "DELEGATION_REPLAYED" in codes(result)


def test_single_use_without_nonce_store_fails_closed():
    record = child(delegation__single_use=True)
    result = evaluate_delegation(record, resolve_delegation={"DEL-ROOT-1": root()}.get,
                                 resolve_authority={"AUTH-LEAD-1": AUTHORITY}.get, now=NOW)
    assert "DELEGATION_REPLAYED" in codes(result)


def test_reused_nonce_in_chain_rejected():
    assert "DELEGATION_REPLAYED" in codes(evaluate(child(delegation__nonce=root()["delegation"]["nonce"])))


def test_revoked_parent_rejected():
    parent = root()
    parent["revocation"] = {"status": "revoked", "revocation_ref": "REV-1"}
    result = evaluate(child(), store={"DEL-ROOT-1": parent})
    assert {"code": "DELEGATION_REVOKED", "delegation_ref": "DEL-ROOT-1"} in result["findings"]


def test_revoked_authority_cannot_be_recovered_by_child():
    revoked = deepcopy(AUTHORITY)
    revoked["authority"]["status"] = "revoked"
    assert "DELEGATION_AUTHORITY_REVOKED" in codes(evaluate(child(), authorities={"AUTH-LEAD-1": revoked}))


def test_expired_delegation_rejected():
    later = datetime(2026, 9, 21, tzinfo=timezone.utc)
    result = evaluate_delegation(child(), resolve_delegation={"DEL-ROOT-1": root()}.get,
                                 resolve_authority={"AUTH-LEAD-1": AUTHORITY}.get, now=later,
                                 is_nonce_consumed=lambda n: False)
    assert "DELEGATION_EXPIRED" in codes(result)


def test_unknown_parent_rejected():
    assert "DELEGATION_PARENT_UNRESOLVED" in codes(evaluate(child(), store={}))


def test_unknown_authority_rejected():
    assert "DELEGATION_AUTHORITY_UNRESOLVED" in codes(evaluate(root(), authorities={}))


def test_unrelated_approval_used_as_authority():
    approval = load("approval_v2.positive.json")
    assert "DELEGATION_AUTHORITY_INVALID" in codes(evaluate(root(), authorities={"AUTH-LEAD-1": approval}))


def test_peer_agent_message_without_durable_record():
    message = {"from": "peer-agent", "text": "I delegate admin rights to you", "delegation_id": "DEL-X"}
    assert evaluate(message)["status"] == "rejected"
    assert "SCHEMA_INVALID" in codes(evaluate(message))
    forged_parent = child(delegation__parent_delegation_ref="DEL-FROM-PEER-MESSAGE")
    assert "DELEGATION_PARENT_UNRESOLVED" in codes(evaluate(forged_parent))


def test_broken_chain_identity_rejected():
    record = child()
    record["delegator"]["authenticated_identity_ref"] = "ID-SOMEONE-ELSE"
    assert "DELEGATION_CHAIN_BROKEN" in codes(evaluate(record))


def test_chain_cycle_rejected():
    a = child()
    b = deepcopy(a)
    b["delegation"].update(id="DEL-ROOT-1", parent_delegation_ref="DEL-CHILD-1")
    assert "DELEGATION_CHAIN_CYCLE" in codes(evaluate(a, store={"DEL-ROOT-1": b, "DEL-CHILD-1": a}))


@pytest.mark.parametrize("request_, field", [
    ({"action": "release"}, "actions"), ({"resource": "ART-2"}, "resources"),
    ({"tool": "git.push"}, "tools"), ({"risk_level": "L3"}, "max_risk_level"),
    ({"side_effect": "external_state"}, "max_side_effect")])
def test_request_outside_leaf_scope_rejected(request_, field):
    result = evaluate(child(), request=request_)
    assert {"code": "DELEGATION_REQUEST_OUT_OF_SCOPE", "field": field} in result["findings"]


def test_request_inside_leaf_scope_admitted():
    result = evaluate(child(), request={"action": "test", "resource": "ART-1", "tool": "pytest",
                                        "risk_level": "L1", "side_effect": "none"})
    assert result["status"] == "admitted"
