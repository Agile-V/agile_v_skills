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
    """Every evidence item's state_binding must match the bundle's own
    baseline.subject_state on ALL THREE of subject_type, subject_ref, and
    subject_digest -- not subject_ref alone. Matching only the ref would
    allow evidence bound to the same logical revision but a different
    actual digest (e.g. an amended commit with the same message/branch
    position) to pass undetected. Structural schema validity never implies
    this; it must be checked explicitly
    (docs/agile-v-runtime/07_EVIDENCE_ADMISSION_CONTRACT.md). subject_ref is
    domain-agnostic (a source-control commit, a document revision, a
    hardware revision, a dataset version, ...); this check does not assume
    a Git-specific identifier."""
    bundle = instance["bundle"]
    baseline_subject = bundle["baseline"]["subject_state"]
    expected = (
        baseline_subject["subject_type"],
        baseline_subject["subject_ref"],
        baseline_subject["subject_digest"],
    )
    for item in bundle["evidence"]:
        sb = item["state_binding"]
        actual = (sb.get("subject_type"), sb.get("subject_ref"), sb.get("subject_digest"))
        if actual != expected:
            return False
    return True


def evidence_policy_binding_matches_frozen_policy(instance: dict) -> bool:
    """Every evidence item that declares a policy_binding must match the
    bundle's own frozen policy_binding.policy_digest exactly. Presence of a
    policy_binding key is not sufficient (item 3): the digest itself must
    agree with the policy the bundle claims to be frozen under."""
    bundle = instance["bundle"]
    frozen_digest = bundle["policy_binding"]["policy_digest"]
    for item in bundle["evidence"]:
        policy_binding = item.get("policy_binding")
        if policy_binding is None:
            continue  # presence is enforced structurally for L2+ by the schema
        if policy_binding.get("policy_digest") != frozen_digest:
            return False
    return True


def evidence_bundle_admission_is_consistent(instance: dict) -> bool:
    """If admission.status is 'admitted', every mandatory claim must be
    satisfied WITHOUT the any-pass anti-pattern:

    1. Any contradictory mandatory evidence (result.status in
       {fail, error}) supporting a claim blocks that claim outright --
       an unrelated passing item never masks it.
    2. The claim's required_evidence_properties must be a subset of the
       UNION of establishes_properties declared by that claim's PASSING
       supporting evidence -- not merely "some evidence for this claim
       passed." A passing test_result item does not, by itself, establish
       'independence' or 'provenance' unless it actually declares those
       properties.
    3. A claim with no supporting evidence at all is never satisfied.
    """
    bundle = instance["bundle"]
    if bundle["admission"]["status"] != "admitted":
        return True

    evidence_by_claim: dict[str, list[dict]] = {}
    for item in bundle["evidence"]:
        for claim_id in item["supports"]:
            evidence_by_claim.setdefault(claim_id, []).append(item)

    for claim in bundle["claims"]:
        items = evidence_by_claim.get(claim["claim_id"], [])
        if not items:
            return False
        if any(item["result"]["status"] in {"fail", "error"} for item in items):
            return False
        established: set[str] = set()
        for item in items:
            if item["result"]["status"] == "pass":
                established |= set(item.get("establishes_properties", []))
        if not set(claim["required_evidence_properties"]) <= established:
            return False
    return True


# ---------------------------------------------------------------------------
# Gate Receipt (schemas/GATE_RECEIPT.schema.json)
# ---------------------------------------------------------------------------

def gate_receipt_decision_consistent(instance: dict) -> bool:
    """A PASS decision requires: every required claim admitted, no rejected
    or stale claims, and no open mandatory obligations. A WAIVED decision
    must be accompanied by exception_refs. This is a structural consistency
    check independent of any external resolver; see
    ``gate_receipt_waiver_is_justified`` and
    ``gate_receipt_has_valid_human_approval`` for checks that require
    resolving referenced exception/approval records."""
    receipt = instance["gate_receipt"]
    claims = receipt["claims"]
    status = receipt["decision"]["status"]
    if status == "PASS":
        if claims["rejected"] or claims["stale"]:
            return False
        if not set(claims["required"]) <= set(claims["admitted"]):
            return False
        if receipt.get("obligations", {}).get("open"):
            return False
    if status == "WAIVED" and not receipt.get("exception_refs"):
        return False
    return True


def gate_receipt_waiver_is_justified(instance: dict, resolve_exception, now: datetime) -> bool:
    """A WAIVED decision must reference exception(s) that actually resolve:
    each exception_ref must resolve to a real EXCEPTION_DECISION record
    that is currently valid (not expired, not a non-waivable meta-control),
    bound to the same task, and targeting one of this receipt's applicable
    claims -- a bare non-empty exception_refs list is not sufficient.

    ``resolve_exception``: Callable[[str], dict | None] returning the
    loaded EXCEPTION_DECISION instance for a given ref, or None if unknown.
    """
    receipt = instance["gate_receipt"]
    if receipt["decision"]["status"] != "WAIVED":
        return True
    refs = receipt.get("exception_refs") or []
    if not refs:
        return False
    applicable_claims = set(receipt["claims"]["rejected"]) | set(receipt["claims"]["stale"]) | set(receipt["claims"]["required"])
    for ref in refs:
        exc_instance = resolve_exception(ref)
        if exc_instance is None:
            return False
        if not exception_currently_valid(exc_instance, now):
            return False
        exc = exc_instance["exception"]
        if exc.get("task_id") != receipt.get("task_id"):
            return False
        if exc["control_or_claim_ref"] not in applicable_claims:
            return False
    return True


def gate_receipt_has_valid_human_approval(instance: dict, resolve_approval, now: datetime) -> bool:
    """For gate_1/gate_2, a PASS or WAIVED decision requires at least one
    resolvable, currently-valid, approved approval bound to this receipt's
    task and gate. A receipt with an empty/unresolvable approvals list is
    not entitled to PASS/WAIVED at these gates -- NEEDS_HUMAN is the correct
    state before that authority exists.

    ``resolve_approval``: Callable[[str], dict | None] returning the loaded
    APPROVAL/APPROVAL.v2 instance for a given approval_ref, or None.
    """
    receipt = instance["gate_receipt"]
    if receipt["gate"] not in {"gate_1", "gate_2"}:
        return True
    if receipt["decision"]["status"] not in {"PASS", "WAIVED"}:
        return True
    for entry in receipt.get("approvals") or []:
        approval_instance = resolve_approval(entry["approval_ref"])
        if approval_instance is None:
            continue
        if not approval_currently_valid(approval_instance, now):
            continue
        approval = approval_instance["approval"]
        if approval.get("task_id") not in (None, receipt.get("task_id")):
            continue
        if approval.get("gate_id") not in (None, receipt.get("gate")):
            continue
        return True
    return False


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
    """An approval is currently valid only if decision == approved, 'now'
    is before expires_at, AND -- if usage.reusable is false -- it has not
    already been consumed (usage.consumed_at is set). A non-reusable,
    already-consumed approval is not valid merely because it has not yet
    expired."""
    approval = instance["approval"]
    if approval["decision"] != "approved":
        return False
    if now >= _parse_datetime(approval["expires_at"]):
        return False
    usage = approval.get("usage", {})
    if usage.get("reusable") is False and usage.get("consumed_at"):
        return False
    return True


def approval_authorizes(
    instance: dict,
    now: datetime,
    *,
    task_id: str | None = None,
    gate_id: str | None = None,
    artifact_digest: str | None = None,
    policy_digest: str | None = None,
    requirement_baseline_id: str | None = None,
    resource: str | None = None,
) -> bool:
    """An approval authorizes a specific action only when it is currently
    valid AND every supplied binding/scope parameter matches exactly.
    Checking artifact_digest alone is not sufficient (item 8): task, gate,
    policy, baseline, and resource scope must also agree with what the
    approval actually authorizes."""
    if not approval_currently_valid(instance, now):
        return False
    approval = instance["approval"]
    if task_id is not None and approval.get("task_id") != task_id:
        return False
    if gate_id is not None and approval.get("gate_id") != gate_id:
        return False
    binding = approval.get("binding", {})
    if artifact_digest is not None and binding.get("artifact_digest") != artifact_digest:
        return False
    if policy_digest is not None and binding.get("policy_digest") != policy_digest:
        return False
    if requirement_baseline_id is not None and binding.get("requirement_baseline_id") != requirement_baseline_id:
        return False
    if resource is not None and resource not in (approval.get("scope", {}).get("resources") or []):
        return False
    return True


def approval_authorizes_artifact(instance: dict, artifact_digest: str, now: datetime | None = None) -> bool:
    """Backward-compatible narrow check: an approval bound to artifact
    digest A cannot authorize a release of artifact digest B. Prefer
    ``approval_authorizes`` for new checks that need to validate additional
    scope (task/gate/policy/baseline/resource)."""
    if now is None:
        # Legacy call sites that only checked decision == approved without
        # an explicit 'now': still require decision == approved, but this
        # path is deprecated -- always pass now going forward.
        approval = instance["approval"]
        if approval["decision"] != "approved":
            return False
        return approval["binding"]["artifact_digest"] == artifact_digest
    return approval_authorizes(instance, now, artifact_digest=artifact_digest)


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

def risk_floor_respected(instance: dict, resolve_exception=None, now: datetime | None = None) -> bool:
    """A dimension-based score may raise the selected level above the
    highest applicable floor; it must not select a level below the highest
    floor without an authorized, currently-valid, correctly-scoped
    exception.

    Fail-closed by default: without both ``resolve_exception`` and ``now``,
    a below-floor selection is NEVER considered respected, regardless of
    whether ``exception_ref`` is populated -- a bare non-empty string is
    not authorization. When both are supplied, the referenced exception
    must resolve to a real record that is currently valid, bound to the
    same task, and whose ``control_or_claim_ref`` actually targets one of
    this assessment's floor ``reason`` values (or the assessment's own id)
    with a type appropriate for overriding a risk floor
    (``residual_risk_acceptance`` or ``waiver``) -- an unrelated exception
    (e.g. a cosmetic concession for a different claim) must not satisfy
    this check merely because its ``exception_ref`` string was copied in.

    ``resolve_exception``: Callable[[str], dict | None] returning the
    loaded EXCEPTION_DECISION instance for a given ref, or None.
    """
    ra = instance["risk_assessment"]
    if not ra["floors"]:
        return True
    highest_floor = max(RISK_LEVEL_ORDER.index(f["minimum_level"]) for f in ra["floors"])
    selected = RISK_LEVEL_ORDER.index(ra["selected_level"])
    if selected >= highest_floor:
        return True
    exception_ref = ra.get("exception_ref")
    if not exception_ref or resolve_exception is None or now is None:
        return False
    exc_instance = resolve_exception(exception_ref)
    if exc_instance is None:
        return False
    if not exception_currently_valid(exc_instance, now):
        return False
    exc = exc_instance["exception"]
    if exc.get("task_id") != ra.get("task_id"):
        return False
    floor_reasons = {f["reason"] for f in ra["floors"]}
    if exc["control_or_claim_ref"] not in floor_reasons and exc["control_or_claim_ref"] != ra.get("id"):
        return False
    if exc.get("type") not in {"residual_risk_acceptance", "waiver"}:
        return False
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
