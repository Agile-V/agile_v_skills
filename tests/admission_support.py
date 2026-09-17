"""Synthetic trusted-provider boundary for contract tests, not live authority."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "tests/fixtures/schemas" / name).read_text())


def property_profile(claim_type, risk_level):
    record = load("evidence_property_profile.positive.json")
    profile = record["profile"]
    return record if (profile["claim_type"], profile["risk_level"]) == (claim_type, risk_level) else None


def adapter(ref):
    record = load("evidence_source_profile.positive.json")
    return record if ref == record["adapter"]["adapter_id"] else None


def context():
    receipt = load("gate_receipt.positive.json")["gate_receipt"]
    return dict(task_id=receipt["task_id"], gate=receipt["gate"],
                subject_state=receipt["subject_state"],
                policy_digest=receipt["policy"]["policy_digest"],
                risk_level="L2", action="release", resources=["ART-1"], critical_risks=[])


def authority(kind, record, decision_context):
    # Exact out-of-band fixture equality: adding "authorship: human" to a
    # candidate is insufficient. Production providers must authenticate.
    if kind == "approval":
        return record == load("approval_v2.positive.json")
    return False


def trusted():
    return dict(resolve_adapter=adapter, resolve_property_profile=property_profile,
                verify_authority=authority, decision_context=context())
