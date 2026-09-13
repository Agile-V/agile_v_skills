"""Reference semantic validators for Agile-V evidence/gate contracts.

These functions are the single, reusable implementation of consistency
rules that a JSON Schema alone cannot express (time-relative expiry,
cross-field consistency, floor-ordering comparisons, dependency-kind
semantics). Tests import from here rather than redefining the same logic
as test-local helpers, so the normative behavior has exactly one
implementation. Any future runtime (e.g. `agentic_agile_v`) implementing
these contracts should treat this module as the reference semantics to
reproduce, not merely the JSON Schemas' structural constraints.

Every function is pure and takes already-loaded JSON/YAML instances (dicts)
plus, where relevant, an explicit ``now`` timestamp — no filesystem or
network access, no hidden global state.
"""
from __future__ import annotations

from datetime import datetime

# Meta-controls that no exception may waive, per
# docs/agile-v-runtime/09_EXCEPTION_AND_WAIVER_CONTRACT.md rule 1.
NON_WAIVABLE_CONTROLS = {"GATE_INTEGRITY", "SUBJECT_BINDING", "UNKNOWN_IDENTITY", "RECEIPT_INTEGRITY"}

# Ordinal risk levels, low to high, per docs/agile-v-runtime/04_RISK_CLASSIFICATION.md.
RISK_LEVEL_ORDER = ["L0", "L1", "L2", "L3", "L4"]

# Only UNCHANGED is reuse-eligible; UNKNOWN/STALE/REVALIDATION_REQUIRED never are,
# per docs/agile-v-runtime/10_CHANGE_AWARE_REVALIDATION.md.
REUSE_ELIGIBLE_RESULTS = {"UNCHANGED"}


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


# ---------------------------------------------------------------------------
# Evidence Bundle v2 (schemas/EVIDENCE_BUNDLE.v2.schema.json)
# ---------------------------------------------------------------------------

def evidence_state_binding_matches_baseline(instance: dict) -> bool:
    """Every evidence item's state_binding.subject_ref must equal the
    bundle's own baseline.subject_state.subject_ref. Structural schema
    validity never implies this; it must be checked explicitly
    (docs/agile-v-runtime/07_EVIDENCE_ADMISSION_CONTRACT.md). subject_ref is
    domain-agnostic (a source-control commit, a document revision, a
    hardware revision, a dataset version, ...); this check does not assume
    a Git-specific identifier."""
    bundle = instance["bundle"]
    expected_ref = bundle["baseline"]["subject_state"]["subject_ref"]
    for item in bundle["evidence"]:
        if item["state_binding"]["subject_ref"] != expected_ref:
            return False
    return True


def evidence_bundle_admission_is_consistent(instance: dict) -> bool:
    """If admission.status is 'admitted', every mandatory claim must have at
    least one passing supporting evidence item."""
    bundle = instance["bundle"]
    if bundle["admission"]["status"] != "admitted":
        return True
    supported = {
        claim_id
        for item in bundle["evidence"]
        if item["result"]["status"] == "pass"
        for claim_id in item["supports"]
    }
    required = {claim["claim_id"] for claim in bundle["claims"]}
    return required <= supported


# ---------------------------------------------------------------------------
# Gate Receipt (schemas/GATE_RECEIPT.schema.json)
# ---------------------------------------------------------------------------

def gate_receipt_decision_consistent(instance: dict) -> bool:
    """A PASS decision must not coexist with any rejected required claim.
    A WAIVED decision must be accompanied by exception_refs (also enforced
    structurally by the schema; this restates it as a semantic invariant
    reusable independent of schema validation)."""
    receipt = instance["gate_receipt"]
    if receipt["decision"]["status"] == "PASS" and receipt["claims"]["rejected"]:
        return False
    if receipt["decision"]["status"] == "WAIVED" and not receipt.get("exception_refs"):
        return False
    return True


def gate_receipt_subject_binding_matches_gate(instance: dict) -> bool:
    """Gate 1 (pre-baseline) must bind to a requirement revision, never a
    baseline id (it does not exist yet). Later gates must bind to the
    frozen baseline. This mirrors the schema's conditional requirement as
    an explicit semantic check."""
    receipt = instance["gate_receipt"]
    subject = receipt.get("subject_state", {})
    if receipt["gate"] == "gate_1":
        return bool(subject.get("requirement_revision_ref")) and not subject.get("requirement_baseline_id")
    return bool(subject.get("requirement_baseline_id"))


# ---------------------------------------------------------------------------
# Approval v2 (schemas/APPROVAL.v2.schema.json)
# ---------------------------------------------------------------------------

def approval_currently_valid(instance: dict, now: datetime) -> bool:
    """An approval is currently valid only if decision == approved and
    'now' is before expires_at. Structural validity of the ISO date-time
    string never implies current validity."""
    approval = instance["approval"]
    if approval["decision"] != "approved":
        return False
    return now < _parse_datetime(approval["expires_at"])


def approval_authorizes_artifact(instance: dict, artifact_digest: str, now: datetime | None = None) -> bool:
    """An approval bound to artifact digest A cannot authorize a release of
    artifact digest B."""
    approval = instance["approval"]
    if now is not None and not approval_currently_valid(instance, now):
        return False
    elif now is None and approval["decision"] != "approved":
        return False
    return approval["binding"]["artifact_digest"] == artifact_digest


# ---------------------------------------------------------------------------
# Exception and Waiver (schemas/EXCEPTION_DECISION.schema.json)
# ---------------------------------------------------------------------------

def exception_currently_valid(
    instance: dict, now: datetime, non_waivable_controls: set[str] = NON_WAIVABLE_CONTROLS,
) -> bool:
    """A non-waivable meta-control can never be waived regardless of
    approver; an expired exception is invalid for any new decision."""
    exc = instance["exception"]
    if exc["control_or_claim_ref"] in non_waivable_controls:
        return False
    return now < _parse_datetime(exc["expires_at"])


# ---------------------------------------------------------------------------
# Risk Assessment v2 (schemas/RISK_ASSESSMENT.schema.json)
# ---------------------------------------------------------------------------

def risk_floor_respected(instance: dict, resolve_exception=None) -> bool:
    """A dimension-based score may raise the selected level above the
    highest applicable floor; it must not select a level below the highest
    floor without an authorized, currently-valid exception.

    ``resolve_exception``, if provided, is a callable
    ``exception_ref -> bool`` that resolves whether the referenced
    EXCEPTION_DECISION is currently authorized and valid (see
    ``exception_currently_valid``). Without it, presence of a non-empty
    ``exception_ref`` string is treated as sufficient (weaker check, kept
    for fixtures that do not carry a resolvable exception record)."""
    ra = instance["risk_assessment"]
    if not ra["floors"]:
        return True
    highest_floor = max(RISK_LEVEL_ORDER.index(f["minimum_level"]) for f in ra["floors"])
    selected = RISK_LEVEL_ORDER.index(ra["selected_level"])
    if selected >= highest_floor:
        return True
    exception_ref = ra.get("exception_ref")
    if not exception_ref:
        return False
    if resolve_exception is not None:
        return resolve_exception(exception_ref)
    return True


# ---------------------------------------------------------------------------
# Governance Conversion (schemas/GOVERNANCE_CONVERSION.schema.json)
# ---------------------------------------------------------------------------

def governance_conversion_proposer_is_not_approver(instance: dict) -> bool:
    """The proposer of a governance conversion must never be its approving
    authority for approved/deployed/validated decisions."""
    decision = instance["conversion"]["decision"]
    if decision["status"] not in {"approved", "deployed", "validated"}:
        return True
    proposer = decision.get("proposer_ref")
    authority = decision.get("authority_ref")
    if proposer is None or authority is None:
        return False  # both must be recorded to prove separation
    return proposer != authority


def governance_conversion_activation_is_justified(instance: dict) -> bool:
    """Deployed/validated conversions require proposer identity, an
    authority distinct from the proposer, a held-out validation reference,
    and an effective_from baseline -- activation is not justified by a mere
    'approved' status string."""
    conversion = instance["conversion"]
    decision = conversion["decision"]
    if decision["status"] not in {"deployed", "validated"}:
        return True
    if not governance_conversion_proposer_is_not_approver(instance):
        return False
    if not conversion.get("evidence", {}).get("held_out_validation_ref"):
        return False
    if not conversion.get("effective_from", {}).get("lifecycle_baseline"):
        return False
    return True


# ---------------------------------------------------------------------------
# Change-aware revalidation (schemas/REVALIDATION_ASSESSMENT.schema.json)
# ---------------------------------------------------------------------------

def revalidation_reuse_eligible(evaluation: dict) -> bool:
    """UNKNOWN, STALE, and REVALIDATION_REQUIRED are never reuse-eligible;
    only UNCHANGED is. This holds regardless of risk level."""
    return evaluation["result"] in REUSE_ELIGIBLE_RESULTS


def revalidation_coverage_is_conservative(instance: dict) -> bool:
    """Partial or unknown dependency coverage must not leave any evaluated
    evidence item silently reported as UNCHANGED without an explicit
    conservative decision: 'partial'/'unknown' coverage requires
    conservative_fallback_applied to be true whenever any evaluation for
    that assessment is not UNCHANGED."""
    assessment = instance["assessment"]
    if assessment["coverage"] == "complete":
        return True
    all_unchanged = all(e["result"] == "UNCHANGED" for e in assessment["evaluations"])
    if all_unchanged:
        return True
    return bool(assessment.get("conservative_fallback_applied"))
