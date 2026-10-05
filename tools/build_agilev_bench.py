"""Generate the AgileV-Bench corpus (self-contained JSON cases + manifest).

Usage:
    python tools/build_agilev_bench.py          # write cases and manifest
    python tools/build_agilev_bench.py --check  # fail if committed corpus drifted

Cases are derived from repository fixtures by explicit, declared mutations.
Expected outcomes are DECLARED here (not computed by the reference
evaluator); tests/test_agilev_bench.py checks that the reference evaluator
reproduces them. Every case embeds all records and trusted-provider data it
needs, so an external runtime can consume it without importing
contracts.semantics. No evaluation logic lives in this generator.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import sys

try:
    from tools._common import ROOT, dump_json, load_json, load_yaml, sha256_bytes, write_or_check
except ImportError:  # executed as a script
    from _common import ROOT, dump_json, load_json, load_yaml, sha256_bytes, write_or_check  # noqa: E402

BENCH = ROOT / "benchmarks" / "agilev-bench"
FIXTURES = ROOT / "tests" / "fixtures" / "schemas"
VERSION = (BENCH / "VERSION").read_text().strip() if (BENCH / "VERSION").exists() else "0.1"
Z64 = "sha256:" + "0" * 64


def fx(name):
    return load_json(FIXTURES / name)


# --- base inputs ---------------------------------------------------------------

def gate_base():
    approval = fx("approval_v2.positive.json")
    receipt = fx("gate_receipt.positive.json")
    r = receipt["gate_receipt"]
    context = dict(task_id=r["task_id"], gate=r["gate"], subject_state=deepcopy(r["subject_state"]),
                   policy_digest=r["policy"]["policy_digest"], risk_level="L2", action="release",
                   resources=["ART-1"], critical_risks=[])
    case_input = {"gate": receipt, "bundle": fx("evidence_bundle_v2.positive.json")}
    trusted = {"decision_context": context, "now": "2026-09-14T00:00:00+00:00",
               "adapters": {"EAD-pytest-junit-v1": fx("evidence_source_profile.positive.json")},
               "property_profiles": {"requirement_satisfaction:L2": fx("evidence_property_profile.positive.json")},
               "approvals": {"APR-1": approval}, "authenticated_approvals": [deepcopy(approval)],
               "exceptions": {}, "authenticated_exceptions": []}
    return case_input, trusted


def registry_records():
    catalog = load_json(ROOT / "catalog" / "evidence-adapters.json")
    records = {e["profile_path"]: load_yaml(ROOT / e["profile_path"])
               for e in catalog["adapters"] + catalog["property_profiles"]}
    return catalog, records


def registry_base(risk="L2"):
    catalog, records = registry_records()
    record = fx("evidence_bundle_v2.positive.json")
    bundle = record["bundle"]
    bundle["risk_level"] = risk
    base = bundle["evidence"][0]

    def item(eid, ref, props, tool_version, locators):
        entry = next(e for e in catalog["adapters"] if e["adapter_id"] == ref and not e["historical"])
        new = deepcopy(base)
        new.update(evidence_id=eid, evidence_type=entry["evidence_type"], establishes_properties=props)
        new["evidence_source"] = {"adapter_ref": ref, "adapter_digest": entry["profile_digest"], "locators": locators}
        if tool_version:
            new["evidence_source"]["tool_version"] = tool_version
        return new

    bundle["evidence"] = [
        item("EVI-1", "EAD-pytest-junit-v1", ["test_result", "state_binding"], "8.3.5",
             {"report_uri": "artifact://junit.xml", "report_digest": "sha256:" + "3" * 64}),
        item("EVI-2", "EAD-github-actions-v1", ["provenance"], None,
             {"run_url": "https://github.com/o/r/actions/runs/1", "run_id": "1", "head_sha": "c" * 40}),
    ]
    bundle["obligations"] = []
    return {"bundle": record}, {"registry": {"catalog": catalog, "records": records}, "historical": False}, item


def trim_registry(case_input, trusted):
    """Keep only the registry entries a case can resolve (smaller cases)."""
    bundle = case_input["bundle"]["bundle"]
    refs = {e.get("evidence_source", {}).get("adapter_ref") for e in bundle["evidence"]}
    keys = {(c["claim_type"], bundle["risk_level"]) for c in bundle["claims"]}
    catalog = deepcopy(trusted["registry"]["catalog"])
    catalog["adapters"] = [e for e in catalog["adapters"] if e["adapter_id"] in refs]
    catalog["property_profiles"] = [p for p in catalog["property_profiles"] if (p["claim_type"], p["risk_level"]) in keys]
    paths = {e["profile_path"] for e in catalog["adapters"] + catalog["property_profiles"]}
    trusted["registry"] = {"catalog": catalog,
                           "records": {p: r for p, r in trusted["registry"]["records"].items() if p in paths}}
    return trusted


def delegation_base():
    root = fx("agent_delegation_record_v2.positive.json")
    child = deepcopy(root)
    child["delegation"].update(id="DEL-CHILD-1", parent_delegation_ref="DEL-ROOT-1",
                               nonce="n-child-000000000000001", expires_at="2026-09-19T00:00:00Z")
    child["delegator"] = {"agent_id": "build-agent", "authenticated_identity_ref": "ID-BUILD"}
    child["delegate"] = {"agent_id": "test-runner", "authenticated_identity_ref": "ID-TEST"}
    child["authority_ceiling"].update(may_delegate_further=False, max_delegation_depth=0)
    child["scope"] = {"requirements": ["REQ-1"], "actions": ["test"], "resources": ["ART-1"],
                      "tools": ["pytest"], "data_classes": ["internal"]}
    authority = {"authority": {
        "id": "AUTH-LEAD-1", "holder_identity_ref": "ID-ORCH", "task_id": "AAV-0042", "status": "active",
        "expires_at": "2026-09-30T00:00:00Z",
        "authority_ceiling": {"max_risk_level": "L3", "max_side_effect": "external_state",
                              "may_delegate_further": True, "max_delegation_depth": 2},
        "scope": {"requirements": ["REQ-1", "REQ-2", "REQ-3"], "actions": ["edit", "test", "release"],
                  "resources": ["ART-1", "ART-2", "ART-3"], "tools": ["fs.write", "pytest", "git.push"],
                  "data_classes": ["internal", "confidential"]}}}
    trusted = {"delegations": {"DEL-ROOT-1": root}, "authorities": {"AUTH-LEAD-1": authority},
               "now": "2026-09-15T00:00:00+00:00", "consumed_nonces": []}
    return {"record": child}, trusted


def context_profiles():
    profiles = {}
    for path in sorted((ROOT / "profiles" / "context-sources").glob("*.yaml")):
        record = load_yaml(path)
        profiles[record["profile"]["id"]] = record
    return profiles


def revalidation_base(changed_kind, result, dependencies=("source", "policy"), coverage="complete"):
    item = deepcopy(fx("evidence_bundle_v2.positive.json")["bundle"]["evidence"][0])
    item["invalidation_dependencies"] = [{"kind": k, "ref": f"{k}_ref"} for k in dependencies]
    assessment = {"schema_version": "1.2", "compatibility": "additive", "migration": "none",
                  "fixture_owner": "agilev-bench",
                  "assessment": {"id": "REVAL-BENCH", "task_id": "AAV-0042", "risk_level": "L2",
                                 "evaluated_at": "2026-09-13T12:00:00Z",
                                 "changed_refs": [{"kind": changed_kind, "ref": f"changed-{changed_kind}"}],
                                 "evaluations": [{"evidence_ref": item["evidence_id"], "claim_refs": ["CLM-1"],
                                                  "result": result}],
                                 "coverage": coverage, "conservative_fallback_applied": coverage != "complete"}}
    return {"assessment": assessment, "evidence_item": item}, {}


# --- case catalogue -------------------------------------------------------------

CASES: list[dict] = []


def case(cid, category, title, operation, case_input, trusted, status, codes=(), *, domain="generic",
         tags=(), source_ref=None):
    CASES.append({"benchmark_version": VERSION, "id": cid, "category": category, "title": title,
                  "domain": domain, "tags": sorted(tags), "operation": operation, "input": case_input,
                  "trusted": trusted, "expected": {"status": status, "reason_codes": sorted(set(codes))},
                  **({"source_ref": source_ref} if source_ref else {})})


def gate_case(cid, category, title, status, codes=(), mutate=None, **kw):
    case_input, trusted = gate_base()
    if mutate:
        mutate(case_input, trusted)
    case(cid, category, title, "gate_transition", case_input, trusted, status, codes, **kw)


def g(ci):
    return ci["gate"]["gate_receipt"]


def b(ci):
    return ci["bundle"]["bundle"]


def ev(ci):
    return b(ci)["evidence"][0]


def build_cases():
    CASES.clear()
    # A - state binding ------------------------------------------------------
    gate_case("AVB-STATE-001", "state-binding", "Evidence, gate, approval and context bound to the same subject digest",
              "admitted", domain="software")
    gate_case("AVB-STATE-002", "state-binding", "Evidence bound to a different subject digest", "rejected",
              ["EVIDENCE_STATE_MISMATCH"], lambda ci, t: ev(ci)["state_binding"].update(subject_digest=Z64),
              tags=["tamper"], source_ref="tests/test_issue42_trust_closure.py::test_stale_evidence")

    def same_ref_new_digest(ci, t):
        b(ci)["baseline"]["subject_state"]["subject_digest"] = "sha256:" + "4" * 64
    gate_case("AVB-STATE-003", "state-binding", "Same subject ref, different baseline digest", "rejected",
              ["EVIDENCE_STATE_MISMATCH", "GATE_EVIDENCE_BINDING_MISMATCH"], same_ref_new_digest, tags=["tamper"])

    def amended(ci, t):
        t["decision_context"]["subject_state"]["subject_digest"] = "sha256:" + "5" * 64
    gate_case("AVB-STATE-004", "state-binding", "Artifact amended after the gate was evaluated", "rejected",
              ["DECISION_CONTEXT_MISMATCH"], amended, tags=["tamper"])
    gate_case("AVB-STATE-005", "state-binding", "Evidence bundle from another task", "rejected",
              ["GATE_EVIDENCE_BINDING_MISMATCH"], lambda ci, t: b(ci).update(task_id="OTHER-TASK"),
              source_ref="tests/test_issue42_trust_closure.py::test_unrelated_bundle_cannot_support_gate")
    gate_case("AVB-STATE-006", "state-binding", "Evidence bundle against another requirement baseline", "rejected",
              ["GATE_EVIDENCE_BINDING_MISMATCH"],
              lambda ci, t: b(ci)["baseline"].update(requirement_baseline_id="BL-OTHER"))
    gate_case("AVB-STATE-007", "state-binding", "Gate receipt for a different task than the transition", "rejected",
              ["DECISION_CONTEXT_MISMATCH"], lambda ci, t: t["decision_context"].update(task_id="AAV-9999"))

    # B - policy binding -----------------------------------------------------
    gate_case("AVB-POLICY-001", "policy-binding", "Evidence bound to the frozen policy", "admitted")
    gate_case("AVB-POLICY-002", "policy-binding", "Evidence produced under a different policy digest", "rejected",
              ["EVIDENCE_POLICY_MISMATCH"], lambda ci, t: ev(ci)["policy_binding"].update(policy_digest=Z64),
              source_ref="tests/test_issue42_trust_closure.py::test_policy_drift")
    gate_case("AVB-POLICY-003", "policy-binding", "Policy changed after the test (context carries new policy)",
              "rejected", ["DECISION_CONTEXT_MISMATCH"],
              lambda ci, t: t["decision_context"].update(policy_digest="sha256:" + "6" * 64))

    def bundle_policy(ci, t):
        b(ci)["policy_binding"]["policy_digest"] = Z64
    gate_case("AVB-POLICY-004", "policy-binding", "Bundle policy digest disagrees with gate policy", "rejected",
              ["GATE_EVIDENCE_BINDING_MISMATCH", "EVIDENCE_POLICY_MISMATCH"], bundle_policy, tags=["tamper"])
    gate_case("AVB-POLICY-005", "policy-binding", "Historical policy context unavailable", "rejected",
              ["DECISION_CONTEXT_REQUIRED"], lambda ci, t: t["decision_context"].pop("policy_digest"))
    gate_case("AVB-POLICY-006", "policy-binding", "Candidate-selected control matrix differs from frozen policy",
              "rejected", ["EVIDENCE_POLICY_MISMATCH"],
              lambda ci, t: ev(ci)["policy_binding"].update(control_matrix_digest=Z64), tags=["tamper"])
    gate_case("AVB-POLICY-007", "policy-binding", "Gate receipt rewritten to an adjusted policy (Evolve goalpost)",
              "rejected", ["DECISION_CONTEXT_MISMATCH"],
              lambda ci, t: g(ci)["policy"].update(policy_digest=Z64),
              source_ref="tests/test_issue42_trust_closure.py::test_evolve_goalpost_change")

    # C - evidence capability --------------------------------------------------
    def reg_case(cid, title, status, codes=(), mutate=None, risk="L2", **kw):
        case_input, trusted, item = registry_base(risk)
        if mutate:
            mutate(case_input, trusted, item)
        case(cid, "evidence-capability", title, "evidence_registry", case_input, trim_registry(case_input, trusted),
             status, codes, **kw)

    reg_case("AVB-EVID-001", "Valid pytest behavioral evidence with CI provenance (registry)", "admitted",
             domain="software")
    reg_case("AVB-EVID-002", "pytest evidence claims human authority", "rejected", ["EVIDENCE_PROPERTY_OVERCLAIM"],
             lambda ci, t, item: b(ci)["evidence"][0]["establishes_properties"].append("human_authority"))

    def swap(ref, props, version, locators, claim_type=None, extra=None):
        def mutate(ci, t, item):
            b(ci)["evidence"][1] = item("EVI-2", ref, props, version, locators)
            if extra:
                extra(ci)
        return mutate
    reg_case("AVB-EVID-003", "Static analyzer claims intended-use validation", "rejected",
             ["EVIDENCE_PROPERTY_OVERCLAIM"],
             swap("EAD-sonarqube-quality-gate-v1", ["quality_gate_result", "intended_use_validation"], "10.6",
                  {"analysis_id": "A1", "project_key": "p", "revision": "c" * 40}))
    reg_case("AVB-EVID-004", "Signature claims semantic correctness", "rejected", ["EVIDENCE_PROPERTY_OVERCLAIM"],
             swap("EAD-sigstore-attestation-v1", ["provenance", "semantic_correctness"], "2.4.1",
                  {"bundle_uri": "oci://x", "subject_digest": "sha256:" + "d" * 64, "certificate_identity": "ci@x"}))

    def bom_claims_compliance(ci, t, item):
        catalog = t["registry"]["catalog"]
        entry = next(e for e in catalog["adapters"] if e["adapter_id"] == "EAD-k8s-aibom-v1")
        extra = deepcopy(b(ci)["evidence"][1])
        extra.update(evidence_id="EVI-3", evidence_type="ai_inventory",
                     establishes_properties=["observed_ai_component_inventory", "regulatory_compliance"])
        extra["evidence_source"] = {"adapter_ref": "EAD-k8s-aibom-v1", "adapter_digest": entry["profile_digest"],
                                    "locators": {"bom_digest": Z64, "cluster_ref": "c", "evidence_locator": "x"}}
        b(ci)["evidence"].append(extra)
    reg_case("AVB-EVID-005", "AI-BOM evidence claims regulatory compliance (experimental source)", "rejected",
             ["EVIDENCE_SOURCE_UNRESOLVED"], bom_claims_compliance)

    def self_profile(ci, t, item):
        source = b(ci)["evidence"][0]["evidence_source"]
        own = deepcopy(next(r for p, r in t["registry"]["records"].items() if p.endswith("pytest-junit-v1.yaml")))
        own["adapter"]["may_establish"].append("human_authority")
        source["profile"] = own
    reg_case("AVB-EVID-006", "Producer supplies its own capability profile", "rejected",
             ["EVIDENCE_SOURCE_SELF_SUPPLIED_PROFILE"], self_profile, tags=["tamper"])
    reg_case("AVB-EVID-007", "Tool version outside supported range", "rejected",
             ["EVIDENCE_SOURCE_TOOL_VERSION_UNSUPPORTED"],
             lambda ci, t, item: b(ci)["evidence"][0]["evidence_source"].update(tool_version="6.2.5"))
    reg_case("AVB-EVID-008", "Required evidence locator absent", "rejected", ["EVIDENCE_LOCATOR_MISSING"],
             lambda ci, t, item: b(ci)["evidence"][0]["evidence_source"]["locators"].pop("report_digest"))
    reg_case("AVB-EVID-009", "Source profile digest changed", "rejected", ["EVIDENCE_SOURCE_DIGEST_MISMATCH"],
             lambda ci, t, item: b(ci)["evidence"][0]["evidence_source"].update(adapter_digest=Z64), tags=["tamper"])
    reg_case("AVB-EVID-010", "Evidence type does not match source profile", "rejected",
             ["EVIDENCE_SOURCE_IDENTITY_MISMATCH"],
             lambda ci, t, item: b(ci)["evidence"][0].update(evidence_type="static_analysis"))
    reg_case("AVB-EVID-011", "pytest alone cannot establish L2 provenance", "rejected",
             ["EVIDENCE_ADMISSION_INCONSISTENT"], lambda ci, t, item: b(ci)["evidence"].pop())
    reg_case("AVB-EVID-012", "L4 requirement satisfaction needs independent verification no tool can establish",
             "rejected", ["EVIDENCE_ADMISSION_INCONSISTENT"], risk="L4")
    reg_case("AVB-EVID-013", "Unknown evidence source", "rejected", ["EVIDENCE_SOURCE_UNRESOLVED"],
             lambda ci, t, item: b(ci)["evidence"][0]["evidence_source"].update(adapter_ref="EAD-unknown-v1"))

    def superseded(historical):
        def mutate(ci, t, item):
            records, catalog = t["registry"]["records"], t["registry"]["catalog"]
            path = "profiles/evidence-sources/pytest-junit-v1.yaml"
            old = records[path]
            new = deepcopy(old)
            new["adapter"]["known_limitations"].append("Revised limitation text added in a later review.")
            from contracts.semantics import profile_digest  # digest helper only; no evaluation
            new["adapter"]["supersedes"] = profile_digest(old)
            hist = "profiles/evidence-sources/history/pytest-junit-v1@old.yaml"
            records[hist], records[path] = old, new
            entry = next(e for e in catalog["adapters"] if e["adapter_id"] == "EAD-pytest-junit-v1")
            catalog["adapters"].append(dict(entry, profile_path=hist, historical=True))
            entry["profile_digest"] = profile_digest(new)
            t["historical"] = historical
        return mutate
    reg_case("AVB-EVID-014", "Superseded source profile used for a current decision", "rejected",
             ["EVIDENCE_SOURCE_SUPERSEDED"], superseded(False))
    reg_case("AVB-EVID-015", "Superseded source profile resolved historically by exact digest", "admitted",
             (), superseded(True))

    gate_case("AVB-EVID-016", "evidence-capability", "Trusted adapter profile drifted after binding", "rejected",
              ["EVIDENCE_SOURCE_DIGEST_MISMATCH"],
              lambda ci, t: t["adapters"]["EAD-pytest-junit-v1"]["adapter"]["may_establish"].append("drift"),
              tags=["tamper"])
    gate_case("AVB-EVID-017", "evidence-capability", "No trusted source resolver supplied", "rejected",
              ["EVIDENCE_SOURCE_RESOLVER_REQUIRED"], lambda ci, t: t.update(adapters=None))
    gate_case("AVB-EVID-018", "evidence-capability", "No trusted property-profile resolver supplied", "rejected",
              ["EVIDENCE_PROPERTY_RESOLVER_REQUIRED"], lambda ci, t: t.update(property_profiles=None))
    gate_case("AVB-EVID-019", "evidence-capability", "Policy raises the property floor above what evidence shows",
              "rejected", ["EVIDENCE_ADMISSION_INCONSISTENT"],
              lambda ci, t: t["property_profiles"]["requirement_satisfaction:L2"]["profile"]["required_properties"]
              .append("physical_measurement"))
    gate_case("AVB-EVID-020", "evidence-capability", "Gate-level overclaim of human authority by test evidence",
              "rejected", ["EVIDENCE_PROPERTY_OVERCLAIM"],
              lambda ci, t: ev(ci)["establishes_properties"].append("human_authority"))

    # D - contradiction --------------------------------------------------------
    def add_item(status, props, eid="EVI-2"):
        def mutate(ci, t):
            extra = deepcopy(ev(ci))
            extra.update(evidence_id=eid, establishes_properties=props, result={"status": status})
            b(ci)["evidence"].append(extra)
        return mutate
    gate_case("AVB-CONTRA-001", "contradiction", "One passing and one failing item for the same claim", "rejected",
              ["EVIDENCE_ADMISSION_INCONSISTENT"], add_item("fail", ["test_result"]))
    gate_case("AVB-CONTRA-002", "contradiction", "Passing item plus an errored item", "rejected",
              ["EVIDENCE_ADMISSION_INCONSISTENT"], add_item("error", ["test_result"]))

    def partials(ci, t):
        ev(ci)["establishes_properties"] = ["provenance", "state_binding"]
        add_item("pass", ["test_result"])(ci, t)
    gate_case("AVB-CONTRA-003", "contradiction", "Multiple partial sources jointly satisfy the claim", "admitted",
              (), partials)
    gate_case("AVB-CONTRA-004", "contradiction", "Required property missing from all passing evidence", "rejected",
              ["EVIDENCE_ADMISSION_INCONSISTENT"], lambda ci, t: ev(ci).update(establishes_properties=["provenance"]))

    def unsupported_claim(ci, t):
        ev(ci)["supports"] = ["CLM-NOT-IN-BUNDLE"]
    gate_case("AVB-CONTRA-005", "contradiction", "Evidence supports an undeclared claim; real claim unsupported",
              "rejected", ["UNKNOWN_SUPPORTED_CLAIM", "EVIDENCE_ADMISSION_INCONSISTENT"], unsupported_claim)

    # E - approval / authority -------------------------------------------------
    def approval(mutator):
        def mutate(ci, t):
            record = t["approvals"]["APR-1"]
            mutator(record["approval"])
            t["authenticated_approvals"] = [deepcopy(record)]
        return mutate
    gate_case("AVB-APPR-001", "approvals", "Valid authenticated, scoped, unexpired approval", "admitted")
    gate_case("AVB-APPR-002", "approvals", "Expired approval", "rejected", ["APPROVAL_NOT_JUSTIFIED"],
              lambda ci, t: t.update(now="2028-01-01T00:00:00+00:00"),
              source_ref="tests/test_issue42_trust_closure.py::test_expired_approval")
    gate_case("AVB-APPR-003", "approvals", "Consumed single-use approval", "rejected", ["APPROVAL_NOT_JUSTIFIED"],
              approval(lambda a: a["usage"].update(consumed_at="2026-09-13T00:00:00Z")), tags=["replay"])
    gate_case("AVB-APPR-004", "approvals", "Approval issued for another task", "rejected", ["APPROVAL_NOT_JUSTIFIED"],
              approval(lambda a: a.update(task_id="AAV-9999")))
    gate_case("AVB-APPR-005", "approvals", "Approval bound to another subject digest", "rejected",
              ["APPROVAL_NOT_JUSTIFIED"], approval(lambda a: a["binding"].update(artifact_digest=Z64)), tags=["tamper"])
    gate_case("AVB-APPR-006", "approvals", "Approval bound to another policy", "rejected", ["APPROVAL_NOT_JUSTIFIED"],
              approval(lambda a: a["binding"].update(policy_digest=Z64)))
    gate_case("AVB-APPR-007", "approvals", "Approval for a different action", "rejected", ["APPROVAL_SCOPE_MISMATCH"],
              lambda ci, t: t["decision_context"].update(action="deploy"))
    gate_case("AVB-APPR-008", "approvals", "Approval does not cover an additional resource", "rejected",
              ["APPROVAL_SCOPE_MISMATCH"], lambda ci, t: t["decision_context"]["resources"].append("ART-OUTSIDE"))

    def self_approval(ci, t):
        t["approvals"]["APR-1"]["approval"]["approver"]["identity"] = "builder"
    gate_case("AVB-APPR-009", "approvals", "Builder approves its own work", "rejected", ["HUMAN_AUTHORITY_UNVERIFIED"],
              self_approval, source_ref="tests/test_issue42_trust_closure.py::test_self_approval")
    gate_case("AVB-APPR-010", "approvals", "Candidate asserts authorship=human", "rejected",
              ["HUMAN_AUTHORITY_UNVERIFIED"],
              lambda ci, t: t["approvals"]["APR-1"]["approval"].update(authorship="human"), tags=["tamper"])
    gate_case("AVB-APPR-011", "approvals", "Approver authority revoked (provider no longer authenticates it)",
              "rejected", ["HUMAN_AUTHORITY_UNVERIFIED"], lambda ci, t: t.update(authenticated_approvals=[]))
    gate_case("AVB-APPR-012", "approvals", "Unresolved critical risk cannot be closed by a generic approval",
              "rejected", ["UNRESOLVED_CRITICAL_RISK"],
              lambda ci, t: t["decision_context"].update(critical_risks=["RISK-CRITICAL-1"]))

    # F - independence ---------------------------------------------------------
    def independence(cls):
        return lambda ci, t: g(ci)["verifier"].update(independence_class=cls)
    gate_case("AVB-INDEP-001", "independence", "I0 verification where L2 requires I2", "rejected",
              ["INDEPENDENCE_BELOW_MINIMUM"], independence("I0"))
    gate_case("AVB-INDEP-002", "independence", "I1 verification where L2 requires I2", "rejected",
              ["INDEPENDENCE_BELOW_MINIMUM"], independence("I1"),
              source_ref="tests/test_issue42_trust_closure.py::test_verifier_contamination")
    gate_case("AVB-INDEP-003", "independence", "I2 verification accepted at L2", "admitted", (), independence("I2"))
    gate_case("AVB-INDEP-004", "independence", "I3 authority separation exceeds the L2 minimum", "admitted", (),
              independence("I3"))

    def raised_risk(ci, t):
        t["decision_context"]["risk_level"] = "L4"
        g(ci)["verifier"]["independence_class"] = "I2"
    gate_case("AVB-INDEP-005", "independence", "I2 verifier where the trusted L4 context requires I3",
              "rejected", ["INDEPENDENCE_BELOW_MINIMUM", "RISK_LEVEL_MISMATCH"], raised_risk)

    def same_context(ci, t):
        g(ci)["verifier"]["independence_class"] = "I0"
        g(ci)["verifier"]["verification_ref"] = "VER-SAME-CONTEXT"
    gate_case("AVB-INDEP-006", "independence", "Builder-context verifier labelled independent is recorded as I0",
              "rejected", ["INDEPENDENCE_BELOW_MINIMUM"], same_context, tags=["tamper"])

    # G - exceptions -----------------------------------------------------------
    def waiver(exc_mutator=None, uncovered=False, waive_ref="CLM-0007"):
        def mutate(ci, t):
            receipt = g(ci)
            receipt["decision"]["status"] = "WAIVED"
            receipt["claims"]["rejected"] = [waive_ref] + (["CLM-UNCOVERED"] if uncovered else [])
            receipt["exception_refs"] = ["EXC-0001"]
            exception = fx("exception_decision.positive.json")
            exception["exception"]["control_or_claim_ref"] = waive_ref
            if exc_mutator:
                exc_mutator(exception["exception"])
            t["exceptions"] = {"EXC-0001": exception}
            t["authenticated_exceptions"] = [deepcopy(exception)]
        return mutate
    gate_case("AVB-EXC-001", "exceptions", "Waiver covers every unresolved item", "admitted", (), waiver())
    gate_case("AVB-EXC-002", "exceptions", "Waiver covers only part of the unresolved items", "rejected",
              ["WAIVER_NOT_JUSTIFIED"], waiver(uncovered=True))
    gate_case("AVB-EXC-003", "exceptions", "Expired waiver", "rejected", ["WAIVER_NOT_JUSTIFIED"],
              waiver(lambda e: e.update(expires_at="2026-09-10T00:00:00Z")))
    gate_case("AVB-EXC-004", "exceptions", "Defer used as a waiver", "rejected", ["WAIVER_NOT_JUSTIFIED"],
              waiver(lambda e: e.update(type="defer")))
    gate_case("AVB-EXC-005", "exceptions", "Residual-risk acceptance used to waive failed verification", "rejected",
              ["WAIVER_NOT_JUSTIFIED"], waiver(lambda e: e.update(type="residual_risk_acceptance")))
    gate_case("AVB-EXC-006", "exceptions", "Attempt to waive gate integrity", "rejected", ["WAIVER_NOT_JUSTIFIED"],
              waiver(waive_ref="GATE_INTEGRITY"), tags=["tamper"])

    # H - revalidation ---------------------------------------------------------
    def reval(cid, title, kind, result, status, codes=(), deps=("source", "policy"), coverage="complete", **kw):
        case_input, trusted = revalidation_base(kind, result, deps, coverage)
        case(cid, "revalidation", title, "revalidation_reuse", case_input, trusted, status, codes, **kw)
    reval("AVB-REVAL-001", "Source code changed; evidence depends on source", "source", "STALE", "rejected",
          ["REVALIDATION_RESULT_NOT_REUSABLE"])
    reval("AVB-REVAL-002", "Requirement changed", "requirement", "REVALIDATION_REQUIRED", "rejected",
          ["REVALIDATION_RESULT_NOT_REUSABLE"], deps=("source", "requirement"))
    reval("AVB-REVAL-003", "Policy changed", "policy", "STALE", "rejected", ["REVALIDATION_RESULT_NOT_REUSABLE"])
    reval("AVB-REVAL-004", "Model changed", "model", "REVALIDATION_REQUIRED", "rejected",
          ["REVALIDATION_RESULT_NOT_REUSABLE"], deps=("source", "model"))
    reval("AVB-REVAL-005", "Tool changed", "tool", "REVALIDATION_REQUIRED", "rejected",
          ["REVALIDATION_RESULT_NOT_REUSABLE"], deps=("source", "tool"))
    reval("AVB-REVAL-006", "Runtime/environment changed", "environment", "REVALIDATION_REQUIRED", "rejected",
          ["REVALIDATION_RESULT_NOT_REUSABLE"], deps=("source", "environment"))
    reval("AVB-REVAL-007", "Hardware revision changed", "hardware", "REVALIDATION_REQUIRED", "rejected",
          ["REVALIDATION_RESULT_NOT_REUSABLE"], deps=("hardware",), domain="firmware")
    reval("AVB-REVAL-008", "Dependency coverage partial", "tool", "UNCHANGED", "rejected",
          ["REVALIDATION_COVERAGE_INCOMPLETE", "REVALIDATION_COVERAGE_NOT_CONSERVATIVE"], coverage="partial")
    reval("AVB-REVAL-009", "Dependency coverage unknown", "tool", "UNCHANGED", "rejected",
          ["REVALIDATION_COVERAGE_INCOMPLETE", "REVALIDATION_COVERAGE_NOT_CONSERVATIVE"], coverage="unknown")
    reval("AVB-REVAL-010", "Unaffected evidence remains reusable", "tool", "UNCHANGED", "admitted")
    reval("AVB-REVAL-011", "UNCHANGED verdict contradicts a declared model dependency", "model", "UNCHANGED",
          "rejected", ["REVALIDATION_DEPENDENCY_CONFLICT"], deps=("source", "model"), tags=["tamper"])
    reval("AVB-REVAL-012", "Evidence with undeclared dependencies cannot be reused", "tool", "UNCHANGED",
          "rejected", ["REVALIDATION_DEPENDENCIES_UNKNOWN"], deps=())

    # I - delegation -----------------------------------------------------------
    def dele(cid, title, status, codes=(), mutate=None, request=None, **kw):
        case_input, trusted = delegation_base()
        if mutate:
            mutate(case_input["record"], trusted)
        if request:
            case_input["request"] = request
        case(cid, "delegation", title, "delegation", case_input, trusted, status, codes, **kw)
    dele("AVB-DELEG-001", "Valid attenuated child delegation", "admitted")
    dele("AVB-DELEG-002", "Child adds a resource", "rejected", ["DELEGATION_SCOPE_EXPANSION"],
         lambda r, t: r["scope"]["resources"].append("ART-3"))
    dele("AVB-DELEG-003", "Child adds an action", "rejected", ["DELEGATION_SCOPE_EXPANSION"],
         lambda r, t: r["scope"]["actions"].append("release"))
    dele("AVB-DELEG-004", "Child raises risk ceiling", "rejected", ["DELEGATION_RISK_ESCALATION"],
         lambda r, t: r["authority_ceiling"].update(max_risk_level="L3"))
    dele("AVB-DELEG-005", "Child extends expiry", "rejected", ["DELEGATION_EXPIRY_EXTENDED"],
         lambda r, t: r["delegation"].update(expires_at="2026-09-25T00:00:00Z"))
    dele("AVB-DELEG-006", "Child exceeds delegation depth", "rejected", ["DELEGATION_DEPTH_EXCEEDED"],
         lambda r, t: r["authority_ceiling"].update(may_delegate_further=True, max_delegation_depth=1))

    def replay(r, t):
        r["delegation"]["single_use"] = True
        t["consumed_nonces"] = [r["delegation"]["nonce"]]
    dele("AVB-DELEG-007", "Replayed single-use delegation", "rejected", ["DELEGATION_REPLAYED"], replay,
         tags=["replay"])
    dele("AVB-DELEG-008", "Revoked parent delegation", "rejected", ["DELEGATION_REVOKED"],
         lambda r, t: t["delegations"]["DEL-ROOT-1"]["revocation"].update(status="revoked", revocation_ref="REV-1"))
    dele("AVB-DELEG-009", "Unknown parent delegation", "rejected", ["DELEGATION_PARENT_UNRESOLVED"],
         lambda r, t: t.update(delegations={}))

    def approval_as_authority(r, t):
        t["authorities"]["AUTH-LEAD-1"] = fx("approval_v2.positive.json")
    dele("AVB-DELEG-010", "Unrelated approval used as delegation authority", "rejected",
         ["DELEGATION_AUTHORITY_INVALID"], approval_as_authority)
    dele("AVB-DELEG-011", "Peer-agent message references a non-durable parent delegation", "rejected",
         ["DELEGATION_PARENT_UNRESOLVED"], lambda r, t: r["delegation"].update(parent_delegation_ref="DEL-PEER-MSG"))
    dele("AVB-DELEG-012", "Request outside leaf scope", "rejected", ["DELEGATION_REQUEST_OUT_OF_SCOPE"],
         request={"action": "release", "resource": "ART-1"})
    dele("AVB-DELEG-013", "Child raises side-effect class", "rejected", ["DELEGATION_SIDE_EFFECT_ESCALATION"],
         lambda r, t: r["authority_ceiling"].update(max_side_effect="irreversible"))

    # J - context injection ----------------------------------------------------
    profiles = context_profiles()

    def ctx(cid, title, profile, target, mode, status, codes=(), **kw):
        case(cid, "context-trust", title, "context_influence",
             {"influence": {"source_ref": f"src:{cid}", "context_profile_ref": profile, "target": target, "mode": mode}},
             {"context_profiles": {k: deepcopy(v) for k, v in profiles.items() if k == profile}}, status, codes, **kw)
    ctx("AVB-CTX-001", "Repository file claims risk=L0", "CTX-REPOSITORY-CONTENT", "risk_level", "activate",
        "rejected", ["CONTEXT_AUTHORITY_ESCALATION"], tags=["injection"])
    ctx("AVB-CTX-002", "Retrieved web content claims approval", "CTX-WEB-RETRIEVAL", "approval", "activate",
        "rejected", ["CONTEXT_AUTHORITY_ESCALATION"], tags=["injection"])
    ctx("AVB-CTX-003", "Tool output requests policy modification", "CTX-TOOL-RESULT", "policy", "activate",
        "rejected", ["CONTEXT_AUTHORITY_ESCALATION"], tags=["injection"])
    ctx("AVB-CTX-004", "Peer agent claims elevated rights", "CTX-PEER-AGENT-MESSAGE", "delegated_authority",
        "activate", "rejected", ["CONTEXT_AUTHORITY_ESCALATION"], tags=["injection"])
    ctx("AVB-CTX-005", "MCP tool description demands admin rights", "CTX-TOOL-DESCRIPTION", "delegated_authority",
        "activate", "rejected", ["CONTEXT_AUTHORITY_ESCALATION"], tags=["injection"])
    ctx("AVB-CTX-006", "Generated wiki page changes the risk level", "CTX-GENERATED-WIKI", "risk_level", "activate",
        "rejected", ["CONTEXT_AUTHORITY_ESCALATION"], tags=["injection"])
    ctx("AVB-CTX-007", "Repository content proposes a requirement change (preserved as proposal)",
        "CTX-REPOSITORY-CONTENT", "approved_requirement", "propose", "proposed")
    ctx("AVB-CTX-008", "Approved requirement baseline remains authoritative", "CTX-APPROVED-REQUIREMENT-BASELINE",
        "approved_requirement", "activate", "admitted")
    ctx("AVB-CTX-009", "Unknown source class tries to set policy", "CTX-UNREGISTERED", "policy", "activate",
        "rejected", ["CONTEXT_SOURCE_UNKNOWN"], tags=["injection"])
    ctx("AVB-CTX-010", "README proposes an approval (never proposable)", "CTX-REPOSITORY-CONTENT", "approval",
        "propose", "rejected", ["CONTEXT_AUTHORITY_ESCALATION"], tags=["injection"])

    # L - AI provenance -------------------------------------------------------
    base_manifest = load_yaml(ROOT / "tests" / "aibom" / "valid_ai_run_manifest_v02.yaml")

    def aiprov(cid, title, status, codes=(), mutate=None, **kw):
        m = deepcopy(base_manifest)
        if mutate:
            mutate(m)
        case(cid, "ai-provenance", title, "ai_run_manifest", {"manifest": m}, {"sources": {}}, status, codes, **kw)
    aiprov("AVB-AIPROV-001", "AI Run Manifest with declared identities", "admitted")
    aiprov("AVB-AIPROV-002", "Declared model presented as verified", "rejected",
           ["AIBOM_VERIFIED_WITHOUT_TRUSTED_SOURCE"], lambda m: m["models"][0].update(confidence="verified"),
           tags=["tamper"])
    aiprov("AVB-AIPROV-003", "Hidden reasoning captured in manifest", "rejected",
           ["AIBOM_HIDDEN_REASONING_CAPTURED"],
           lambda m: m["summary"].update(verifier_notes="<thinking>internal</thinking>"))
    aiprov("AVB-AIPROV-004", "Unresolved model identity at L3", "rejected", ["AIBOM_UNRESOLVED_MATERIAL_IDENTITY"],
           lambda m: (m["risk"].update(agile_v_risk_level="L3"), m["models"][0].update(confidence="unresolved")))

    # K - cross-domain transitions ---------------------------------------------
    def rebind(subject_type, ref, digest, specific):
        def mutate(ci, t):
            receipt = g(ci)
            receipt["subject_state"] = {"requirement_baseline_id": "BL-1", "subject_digest": digest, **specific}
            baseline = b(ci)["baseline"]["subject_state"]
            baseline.update(subject_type=subject_type, subject_ref=ref, subject_digest=digest,
                            profile_specific=dict(specific))
            for item in b(ci)["evidence"]:
                item["state_binding"] = {"subject_type": subject_type, "subject_ref": ref, "subject_digest": digest,
                                         "profile_specific": dict(specific)}
            t["approvals"]["APR-1"]["approval"]["binding"]["artifact_digest"] = digest
            t["authenticated_approvals"] = [deepcopy(t["approvals"]["APR-1"])]
            t["decision_context"]["subject_state"] = deepcopy(receipt["subject_state"])
        return mutate

    def then(first, second):
        def mutate(ci, t):
            first(ci, t)
            second(ci, t)
        return mutate
    sw_reviewed = "sha256:" + "a1" * 32
    gate_case("AVB-XDOM-001", "cross-domain", "Software: merge commit equals the reviewed commit", "admitted", (),
              rebind("source_control_commit", "1" * 40, sw_reviewed, {"source_commit": "1" * 40}), domain="software")
    gate_case("AVB-XDOM-002", "cross-domain", "Software: reviewed commit != merge commit", "rejected",
              ["DECISION_CONTEXT_MISMATCH"],
              then(rebind("source_control_commit", "1" * 40, sw_reviewed, {"source_commit": "1" * 40}),
                   lambda ci, t: t["decision_context"].update(subject_state={
                       "requirement_baseline_id": "BL-1", "subject_digest": "sha256:" + "a2" * 32,
                       "source_commit": "2" * 40})), domain="software", tags=["tamper"])
    fw = "sha256:" + "b1" * 32
    fw_spec = {"image_digest": fw, "target": "board-rev-c"}
    gate_case("AVB-XDOM-003", "cross-domain", "Firmware: flashed image equals the approved image", "admitted", (),
              rebind("configuration_baseline", "fw-1.4.0", fw, fw_spec), domain="firmware")
    gate_case("AVB-XDOM-004", "cross-domain", "Firmware: approved image digest != flashed image digest", "rejected",
              ["DECISION_CONTEXT_MISMATCH"],
              then(rebind("configuration_baseline", "fw-1.4.0", fw, fw_spec),
                   lambda ci, t: t["decision_context"]["subject_state"].update(
                       subject_digest="sha256:" + "b2" * 32, image_digest="sha256:" + "b2" * 32)),
              domain="firmware", tags=["tamper"])
    pcb = "sha256:" + "c1" * 32
    pcb_spec = {"manufacturing_archive_digest": pcb, "hardware_revision": "PCB-REV-B"}
    gate_case("AVB-XDOM-005", "cross-domain", "PCB: submitted archive equals the approved archive", "admitted", (),
              rebind("hardware_revision", "PCB-REV-B", pcb, pcb_spec), domain="pcb")
    gate_case("AVB-XDOM-006", "cross-domain", "PCB: approved manufacturing archive != submitted archive", "rejected",
              ["DECISION_CONTEXT_MISMATCH"],
              then(rebind("hardware_revision", "PCB-REV-B", pcb, pcb_spec),
                   lambda ci, t: t["decision_context"]["subject_state"].update(
                       subject_digest="sha256:" + "c2" * 32, manufacturing_archive_digest="sha256:" + "c2" * 32)),
              domain="pcb", tags=["tamper"])
    return CASES


def write_corpus(check: bool) -> bool:
    cases = build_cases()
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids)), "duplicate case id"
    ok = True
    expected_paths = set()
    for c in cases:
        path = BENCH / "cases" / c["category"] / f"{c['id']}.json"
        expected_paths.add(path)
        ok &= write_or_check(path, dump_json(c), check)
    for stale in set((BENCH / "cases").rglob("*.json")) - expected_paths:
        if check:
            print(f"DRIFT: stale case {stale.relative_to(ROOT)}", file=sys.stderr)
            ok = False
        else:
            stale.unlink()
    ok &= write_or_check(BENCH / "manifests" / f"v{VERSION}.json", dump_json(manifest(cases)), check)
    return ok


def manifest(cases) -> dict:
    entries = [{"id": c["id"], "category": c["category"], "domain": c["domain"], "operation": c["operation"],
                "path": f"cases/{c['category']}/{c['id']}.json",
                "sha256": sha256_bytes(dump_json(c).encode())} for c in cases]
    by_category = {}
    for c in cases:
        by_category[c["category"]] = by_category.get(c["category"], 0) + 1
    corpus = sha256_bytes("".join(f"{e['path']}\0{e['sha256']}\n" for e in sorted(entries, key=lambda e: e["path"]))
                          .encode())
    return {"benchmark": "AgileV-Bench", "benchmark_version": VERSION, "case_count": len(cases),
            "categories": by_category, "corpus_digest": corpus,
            "case_schema": "benchmark.schema.json", "result_schema": "result.schema.json",
            "cases": sorted(entries, key=lambda e: e["id"])}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    return 0 if write_corpus(args.check) else 1


if __name__ == "__main__":
    sys.exit(main())
