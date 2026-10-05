"""Reference semantic validators for Agile-V evidence/gate contracts.

These functions are the single, reusable implementation of consistency
rules that a JSON Schema alone cannot express (time-relative expiry,
cross-field consistency, floor-ordering comparisons, dependency-kind
semantics). Tests import from here rather than redefining the same logic
as test-local helpers, so the normative behavior has exactly one
implementation. Any future runtime (e.g. `agentic_agile_v`) implementing
these contracts should treat this module as the reference semantics to
reproduce, not merely the JSON Schemas' structural constraints.

IMPORTANT -- use the aggregate evaluators for admission decisions:
``evaluate_evidence_bundle``, ``evaluate_gate_receipt``, and
``authorize_gate_transition`` (bottom of this file) are the only functions
that should be documented as answering "may this evidence/gate actually
advance?". The individual predicates above them (state binding, policy
binding, decision consistency, waiver justification, approval validity,
independence sufficiency, ...) are reusable building blocks; calling only
one or two of them and treating the result as "admissible" reintroduces
exactly the gaps the aggregate evaluators exist to close.

Aggregate functions validate against repository-owned schemas before using
the lower-level predicates. Resolver callbacks are the trusted-provider
boundary; schema validation and a typed identity do not authenticate a person.
Evaluation never performs an external action or consumes an approval. The
runtime must atomically recheck and enforce the decision at the action boundary.
"""
from __future__ import annotations

from datetime import datetime
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

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


def evidence_bundle_admission_is_consistent(instance: dict, resolve_adapter=None) -> bool:
    """If admission.status is 'admitted', every mandatory claim must be
    satisfied WITHOUT the any-pass anti-pattern AND without trusting a
    producer's self-declared establishes_properties beyond what its
    evidence source is actually capable of establishing:

    1. Any contradictory mandatory evidence (result.status in
       {fail, error}) supporting a claim blocks that claim outright --
       an unrelated passing item never masks it.
    2. The claim's required_evidence_properties must be a subset of the
       UNION of TRUSTED establishes_properties declared by that claim's
       PASSING supporting evidence -- not merely "some evidence for this
       claim passed." "Trusted" means capped by the resolved
       EVIDENCE_SOURCE_PROFILE's may_establish capability
       (``resolve_adapter``); a unit-test adapter cannot self-authorize
       'human_authority' merely because the evidence item's own
       establishes_properties field claims it. When ``resolve_adapter`` is
       not supplied, this falls back to trusting the bare self-declared
       set (legacy/advisory mode) -- prefer ``evaluate_evidence_bundle``,
       which always requires a resolver, as the trusted aggregate
       entrypoint.
    3. A claim with no supporting evidence at all is never satisfied.

    ``resolve_adapter``: Callable[[str], dict | None] returning the loaded
    EVIDENCE_SOURCE_PROFILE instance for a given adapter_ref, or None.
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
                established |= _evidence_trusted_established_properties(item, resolve_adapter)
        if not set(claim["required_evidence_properties"]) <= established:
            return False
    return True


def _evidence_trusted_established_properties(item: dict, resolve_adapter) -> set[str]:
    """The properties an evidence item may actually be TRUSTED to have
    established: its self-declared establishes_properties, capped by its
    resolved adapter's may_establish capability (minus may_not_establish).
    Without a resolver, falls back to the bare self-declared set (legacy/
    advisory; the trusted path is via ``evaluate_evidence_bundle``, which
    always supplies a resolver)."""
    claimed = set(item.get("establishes_properties", []))
    if resolve_adapter is None:
        return claimed
    source = item.get("evidence_source")
    if source is None:
        return set()  # no declared adapter: trust nothing when a resolver is in use
    adapter_instance = resolve_adapter(source["adapter_ref"])
    if adapter_instance is None:
        return set()  # unresolvable adapter: trust nothing
    adapter = adapter_instance["adapter"]
    capability = set(adapter.get("may_establish", [])) - set(adapter.get("may_not_establish", []))
    return claimed & capability


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


# Exception types that may actually justify a WAIVED gate decision.
# 'dispensation' affects obligation deadlines, not claim satisfaction, and
# 'defer' is explicitly "nothing is currently satisfied, waived, or
# accepted" per 09_EXCEPTION_AND_WAIVER_CONTRACT.md -- neither may
# authorize advancement on its own.
WAIVER_PERMITTED_EXCEPTION_TYPES = {"waiver", "concession"}


def gate_receipt_waiver_is_justified(
    instance: dict,
    resolve_exception,
    now: datetime,
    non_waivable_controls: set[str] = NON_WAIVABLE_CONTROLS,
) -> bool:
    """A WAIVED decision is justified only when EVERY unresolved mandatory
    item is covered by an applicable, valid exception -- not merely when
    every CITED exception happens to be valid. Compute the unresolved set
    (required-but-not-admitted, rejected, stale, plus open obligations) and
    require each item to be covered by at least one exception whose
    ``control_or_claim_ref`` matches it, whose ``type`` is one that may
    actually justify advancement (waiver/concession/residual_risk_
    acceptance -- not dispensation/defer), and which is otherwise currently
    valid (not expired, not a non-waivable meta-control -- using the
    caller-supplied ``non_waivable_controls`` set, so policy/control-matrix
    -specific non-waivable controls reach this check rather than only the
    hardcoded default).

    ``resolve_exception``: Callable[[str], dict | None] returning the
    loaded EXCEPTION_DECISION instance for a given ref, or None if unknown.
    """
    receipt = instance["gate_receipt"]
    if receipt["decision"]["status"] != "WAIVED":
        return True
    claims = receipt["claims"]
    unresolved = (set(claims["required"]) - set(claims["admitted"])) | set(claims["rejected"]) | set(claims["stale"])
    unresolved |= set(receipt.get("obligations", {}).get("open") or [])
    refs = receipt.get("exception_refs") or []
    if not refs:
        return False
    covered: set[str] = set()
    for ref in refs:
        exc_instance = resolve_exception(ref)
        if exc_instance is None:
            return False
        if not exception_currently_valid(exc_instance, now, non_waivable_controls):
            return False
        exc = exc_instance["exception"]
        if exc.get("task_id") != receipt.get("task_id"):
            return False
        if exc.get("type") not in WAIVER_PERMITTED_EXCEPTION_TYPES:
            return False
        covered.add(exc["control_or_claim_ref"])
    return unresolved <= covered


def gate_receipt_has_valid_human_approval(instance: dict, resolve_approval, now: datetime) -> bool:
    """For gate_1/gate_2, a PASS or WAIVED decision requires at least one
    resolvable, currently-valid approval that authorizes the EXACT receipt
    state -- not merely the same task/gate. An approval issued for an
    earlier artifact/policy/baseline must not silently authorize a receipt
    whose subject_state or policy has since changed (the classic
    stale-approval path). This delegates to ``approval_authorizes`` with
    every binding value the receipt actually carries, rather than
    duplicating a weaker subset of the checks.

    ``resolve_approval``: Callable[[str], dict | None] returning the loaded
    APPROVAL/APPROVAL.v2 instance for a given approval_ref, or None.
    """
    receipt = instance["gate_receipt"]
    if receipt["gate"] not in {"gate_1", "gate_2"}:
        return True
    if receipt["decision"]["status"] not in {"PASS", "WAIVED"}:
        return True
    subject = receipt.get("subject_state", {})
    policy = receipt.get("policy", {})
    for entry in receipt.get("approvals") or []:
        approval_instance = resolve_approval(entry["approval_ref"])
        if approval_instance is None:
            continue
        if approval_authorizes(
            approval_instance,
            now,
            task_id=receipt.get("task_id"),
            gate_id=receipt.get("gate"),
            artifact_digest=subject.get("subject_digest"),
            policy_digest=policy.get("policy_digest"),
            requirement_baseline_id=subject.get("requirement_baseline_id"),
        ):
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


# Ordinal independence classes, per docs/agile-v-runtime/08_INDEPENDENCE_CLASSES.md.
INDEPENDENCE_ORDER = ["I0", "I1", "I2", "I3", "I4"]

# Minimum independence class for VERIFICATION at each risk level, per
# docs/agile-v-runtime/04_RISK_CLASSIFICATION.md. L3/L4 additionally require
# I3 authority-separated human sign-off; that is an approval-level concern
# (see gate_receipt_has_valid_human_approval), not the verifier's
# independence_class checked here.
MINIMUM_VERIFICATION_INDEPENDENCE_BY_RISK_LEVEL = {
    "L0": "I0", "L1": "I1", "L2": "I2", "L3": "I2", "L4": "I3",
}


def minimum_independence_for_risk_level(risk_level: str) -> str:
    return MINIMUM_VERIFICATION_INDEPENDENCE_BY_RISK_LEVEL[risk_level]


def gate_receipt_independence_is_sufficient(instance: dict, risk_level: str | None = None) -> bool:
    """The verifier's achieved independence_class must be >= the minimum
    required. The requirement is resolved from (a) the receipt's own
    optional risk_level field or an explicit ``risk_level`` argument via
    ``minimum_independence_for_risk_level``, and/or (b) an explicit
    ``verifier.required_independence_class`` override (e.g. a regulated
    profile requiring more than the generic risk-level table) -- the
    stricter of the two applies. Previously this was documented in prose
    but never machine-checked: a Gate Receipt could record I0/I1
    verification for an L2+ decision and still pass every other predicate.
    If neither source supplies a requirement, this check does not itself
    block (the caller must supply a requirement from somewhere)."""
    receipt = instance["gate_receipt"]
    effective_risk_level = risk_level if risk_level is not None else receipt.get("risk_level")
    verifier = receipt.get("verifier") or {}
    required_candidates = []
    if effective_risk_level is not None:
        required_candidates.append(minimum_independence_for_risk_level(effective_risk_level))
    if verifier.get("required_independence_class") is not None:
        required_candidates.append(verifier["required_independence_class"])
    if not required_candidates:
        return True
    required = max(required_candidates, key=INDEPENDENCE_ORDER.index)
    achieved = verifier.get("independence_class")
    if achieved is None:
        return False
    return INDEPENDENCE_ORDER.index(achieved) >= INDEPENDENCE_ORDER.index(required)


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
    if not _parse_datetime(approval["issued_at"]) <= now < _parse_datetime(approval["expires_at"]):
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
    if exc["control_or_claim_ref"] in (NON_WAIVABLE_CONTROLS | non_waivable_controls):
        return False
    return _parse_datetime(exc["issued_at"]) <= now < _parse_datetime(exc["expires_at"])


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

def revalidation_reuse_eligible(evaluation: dict, assessment_coverage: str = "unknown") -> bool:
    """UNKNOWN, STALE, and REVALIDATION_REQUIRED are never reuse-eligible;
    only UNCHANGED is -- AND only when the coverage relevant to THIS item
    is complete. An evaluation's own ``dependency_coverage`` (if present)
    overrides the assessment-level ``coverage`` default. Missing dependency
    knowledge for one item is never proof that specific item is unchanged,
    even inside an assessment where other items are fully covered."""
    if evaluation["result"] not in REUSE_ELIGIBLE_RESULTS:
        return False
    item_coverage = evaluation.get("dependency_coverage", assessment_coverage)
    return item_coverage == "complete"


def revalidation_coverage_is_conservative(instance: dict) -> bool:
    """No evaluation may report UNCHANGED unless the coverage relevant to
    THAT evaluation (its own dependency_coverage, or the assessment-level
    coverage if the item does not override it) is complete -- partial/
    unknown assessment-level coverage does not become "safe" for an
    UNCHANGED item merely because a global conservative_fallback_applied
    flag is set elsewhere; the flag only relaxes the requirement that
    overall assessment coverage itself be complete, not the per-item
    UNCHANGED-requires-complete-coverage rule."""
    assessment = instance["assessment"]
    overall = assessment["coverage"]
    for evaluation in assessment["evaluations"]:
        item_coverage = evaluation.get("dependency_coverage", overall)
        if evaluation["result"] == "UNCHANGED" and item_coverage != "complete":
            return False
    if overall != "complete":
        return bool(assessment.get("conservative_fallback_applied"))
    return True


# ---------------------------------------------------------------------------
# Canonical aggregate evaluators
# ---------------------------------------------------------------------------
#
# Every predicate above is a reusable building block, NOT individually
# sufficient to answer "may this evidence/gate actually advance?". A caller
# that invokes only one or two predicates and labels the result "admissible"
# reintroduces exactly the gaps those predicates were written to close. The
# functions below are the only ones that should be documented as answering
# that question; they run every applicable check and return structured
# findings (a reason-code list) rather than a bare boolean, so a rejection
# is always explainable. Any runtime (e.g. `agentic_agile_v`) implementing
# this contract should reproduce these aggregate functions as its admission
# decision surface, not reimplement a subset of the underlying predicates.

def profile_digest(instance: dict) -> str:
    """SHA-256 of UTF-8 JSON: sorted keys, compact separators, ASCII escapes.

    This is the Python reference serialization, not an RFC 8785 claim.
    Hash the entire resolved profile envelope; never include a self-hash.
    """
    encoded = json.dumps(instance, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=True, allow_nan=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _schema_findings(instance, schema_name: str) -> list[dict]:
    """Validate before predicates run; missing resources never mean success."""
    try:
        schema = json.loads((Path(__file__).resolve().parents[1] / "schemas" /
                             f"{schema_name}.schema.json").read_text(encoding="utf-8"))
        # JSON permits no non-finite numbers. Python callers must not bypass
        # that input boundary by directly supplying float('nan').
        json.dumps(instance, allow_nan=False)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(instance), key=lambda e: str(list(e.path)))
        return [{"code": "SCHEMA_INVALID", "schema": schema_name,
                 "path": list(e.path)} for e in errors]
    except (TypeError, ValueError):
        return [{"code": "SCHEMA_INVALID", "schema": schema_name}]
    except OSError:
        return [{"code": "SCHEMA_UNAVAILABLE", "schema": schema_name}]


def _resolve(resolver, args, code: str, findings: list[dict], **locator):
    """Resolvers return authoritative snapshots, not candidate-provided profiles.

    Authentication, access control and historical retrieval belong to the
    caller's trusted resolver. Unknown records and provider errors deny.
    """
    if resolver is None:
        findings.append({"code": code, **locator})
        return None
    try:
        result = resolver(*args)
        if not isinstance(result, dict):
            findings.append({"code": code, **locator})
            return None
        return deepcopy(result)
    except Exception:
        # Do not leak provider errors, credentials or payloads into findings.
        findings.append({"code": "RESOLVER_ERROR", **locator})
        return None


def evaluate_evidence_bundle(instance: dict, *, resolve_adapter=None,
                             resolve_property_profile=None) -> dict:
    """Trusted aggregate; all risk levels require source/property resolution.

    resolve_property_profile(claim_type, risk_level) selects the authoritative
    profile independently of claim-local property lists. Local additions may
    strengthen it. No resolver-less fallback exists at this entrypoint.
    """
    findings = _schema_findings(instance, "EVIDENCE_BUNDLE.v2")
    if findings:
        return {"status": "rejected", "findings": findings}
    normalized = deepcopy(instance)
    bundle = normalized["bundle"]
    if resolve_adapter is None:
        findings.append({"code": "EVIDENCE_SOURCE_RESOLVER_REQUIRED"})
    if resolve_property_profile is None:
        findings.append({"code": "EVIDENCE_PROPERTY_RESOLVER_REQUIRED"})
    adapters = {}
    evidence_ids = set()
    claim_ids = {claim["claim_id"] for claim in bundle["claims"]}
    if len(claim_ids) != len(bundle["claims"]):
        findings.append({"code": "DUPLICATE_CLAIM_ID"})
    for item in bundle["evidence"]:
        locator = {"evidence_ref": item["evidence_id"]}
        if item["evidence_id"] in evidence_ids:
            findings.append({"code": "DUPLICATE_EVIDENCE_ID", **locator})
        evidence_ids.add(item["evidence_id"])
        if not set(item["supports"]) <= claim_ids:
            findings.append({"code": "UNKNOWN_SUPPORTED_CLAIM", **locator})
        frozen_control = bundle["policy_binding"].get("control_matrix_digest")
        # A separately supplied control binding must not contradict policy.
        bound_control = item.get("policy_binding", {}).get("control_matrix_digest")
        if bound_control is not None and bound_control != frozen_control:
            findings.append({"code": "EVIDENCE_POLICY_MISMATCH", **locator})
        source = item.get("evidence_source", {})
        ref = source.get("adapter_ref")
        adapter_record = _resolve(resolve_adapter, (ref,), "EVIDENCE_SOURCE_UNRESOLVED",
                                  findings, adapter_ref=ref, **locator)
        if adapter_record is None:
            continue
        errors = _schema_findings(adapter_record, "EVIDENCE_SOURCE_PROFILE")
        if errors:
            findings.extend(errors)
            continue
        adapter = adapter_record["adapter"]
        if adapter["adapter_id"] != ref or adapter["evidence_type"] != item["evidence_type"]:
            findings.append({"code": "EVIDENCE_SOURCE_IDENTITY_MISMATCH", **locator})
            continue
        if source.get("adapter_digest") != profile_digest(adapter_record):
            findings.append({"code": "EVIDENCE_SOURCE_DIGEST_MISMATCH", **locator})
            continue
        capabilities = set(adapter["may_establish"]) - set(adapter["may_not_establish"])
        if not set(item["establishes_properties"]) <= capabilities:
            findings.append({"code": "EVIDENCE_PROPERTY_OVERCLAIM", **locator})
        adapters[ref] = adapter_record
    profiles = {}
    for claim in bundle["claims"]:
        key = (claim["claim_type"], bundle["risk_level"])
        if key not in profiles:
            profiles[key] = _resolve(resolve_property_profile, key,
                                     "EVIDENCE_PROPERTY_PROFILE_UNRESOLVED", findings,
                                     claim_ref=claim["claim_id"])
        record = profiles[key]
        if record is None:
            continue
        errors = _schema_findings(record, "EVIDENCE_PROPERTY_PROFILE")
        if errors:
            findings.extend(errors)
            continue
        profile = record["profile"]
        if (profile["claim_type"], profile["risk_level"]) != key:
            findings.append({"code": "EVIDENCE_PROPERTY_PROFILE_MISMATCH", "claim_ref": claim["claim_id"]})
            continue
        claim["required_evidence_properties"] = sorted(
            set(claim["required_evidence_properties"]) | set(profile["required_properties"]))
    if not evidence_state_binding_matches_baseline(normalized):
        findings.append({"code": "EVIDENCE_STATE_MISMATCH"})
    if not evidence_policy_binding_matches_frozen_policy(normalized):
        findings.append({"code": "EVIDENCE_POLICY_MISMATCH"})
    if not evidence_bundle_admission_is_consistent(normalized, resolve_adapter=adapters.get):
        findings.append({"code": "EVIDENCE_ADMISSION_INCONSISTENT"})
    if any(o["state"] != "discharged" for o in bundle.get("obligations", [])):
        findings.append({"code": "EVIDENCE_OBLIGATION_UNRESOLVED"})
    if bundle["admission"]["status"] != "admitted":
        findings.append({"code": "EVIDENCE_NOT_ADMITTED"})
    return {"status": "rejected" if findings else "admitted", "findings": findings}


def evaluate_gate_receipt(
    instance: dict,
    *,
    resolve_exception,
    resolve_approval,
    now: datetime,
    non_waivable_controls: set[str] = NON_WAIVABLE_CONTROLS,
    risk_level: str | None = None,
    verify_authority=None,
    decision_context: dict | None = None,
) -> dict:
    """Canonical aggregate entrypoint for a Gate Receipt instance. Runs
    subject-binding, decision-consistency, independence, waiver, and
    approval checks together and returns structured findings."""
    findings = _schema_findings(instance, "GATE_RECEIPT")
    if findings:
        return {"status": "rejected", "findings": findings, "decision_status": None}
    receipt = instance["gate_receipt"]
    # Context is supplied by the transition authority, never by candidate
    # evidence. It identifies the actual proposed action and accepted state.
    context_fields = {"task_id", "gate", "subject_state", "policy_digest",
                      "risk_level", "action", "resources", "critical_risks"}
    if not isinstance(decision_context, dict) or not context_fields <= decision_context.keys():
        findings.append({"code": "DECISION_CONTEXT_REQUIRED"})
        decision_context = {}
    context = decision_context
    if context and (not isinstance(context["subject_state"], dict)
                    or not isinstance(context["critical_risks"], list)
                    or not isinstance(context["resources"], list)
                    or not all(isinstance(r, str) and r for r in context["resources"])
                    or not isinstance(context.get("non_waivable_controls", []), (list, set))):
        return {"status": "rejected", "findings": [{"code": "DECISION_CONTEXT_INVALID"}],
                "decision_status": receipt["decision"]["status"]}
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        return {"status": "rejected", "findings": [{"code": "EVALUATION_TIME_INVALID"}],
                "decision_status": receipt["decision"]["status"]}
    if context:
        if (receipt["task_id"] != context["task_id"] or receipt["gate"] != context["gate"]
                or receipt["subject_state"] != context["subject_state"]
                or receipt["policy"]["policy_digest"] != context["policy_digest"]):
            findings.append({"code": "DECISION_CONTEXT_MISMATCH"})
        if context["risk_level"] not in RISK_LEVEL_ORDER:
            findings.append({"code": "RISK_LEVEL_INVALID"})
        else:
            # A caller may raise but cannot lower the trusted risk floor.
            levels = [context["risk_level"]]
            if risk_level in RISK_LEVEL_ORDER:
                levels.append(risk_level)
            risk_level = max(levels, key=RISK_LEVEL_ORDER.index)
        if context["critical_risks"]:
            # Closed/dispositioned records must be supplied in a new accepted
            # context; a generic gate approval cannot close critical risks.
            findings.append({"code": "UNRESOLVED_CRITICAL_RISK"})
        if not context["action"] or not isinstance(context["resources"], list) or not context["resources"]:
            findings.append({"code": "AUTHORIZATION_SCOPE_REQUIRED"})
    if risk_level not in RISK_LEVEL_ORDER:
        findings.append({"code": "RISK_LEVEL_REQUIRED"})
        risk_level = "L4"  # conservative diagnostic fallback, never success
    authority_failures = []

    def authenticated(resolver, ref, kind, schema):
        record = _resolve(resolver, (ref,), f"{kind.upper()}_UNRESOLVED", authority_failures)
        if record is None:
            return None
        errors = _schema_findings(record, schema)
        if errors:
            authority_failures.extend(errors)
            return None
        if record[kind]["id"] != ref:
            authority_failures.append({"code": "AUTHORITY_RECORD_MISMATCH"})
            return None
        try:
            valid = verify_authority is not None and verify_authority(kind, record, context) is True
        except Exception:
            valid = False
        if not valid:
            authority_failures.append({"code": "HUMAN_AUTHORITY_UNVERIFIED"})
            return None
        if kind == "approval":
            approval = record["approval"]
            scope = approval["scope"]
            if (scope["action"] != context.get("action") or
                    not set(context.get("resources", [])) <= set(scope["resources"])):
                authority_failures.append({"code": "APPROVAL_SCOPE_MISMATCH"})
                return None
        else:
            # Free-text scope is not interpreted as authorization. The
            # authority provider must verify exact subject/policy/action
            # scope and exception-granting rights using the passed context.
            if record["exception"]["type"] not in {"waiver", "concession"}:
                authority_failures.append({"code": "EXCEPTION_TYPE_NOT_PERMITTED"})
                return None
            target = record["exception"]["control_or_claim_ref"]
            if target in receipt.get("obligations", {}).get("open", []):
                # A technical claim waiver cannot silently discharge a due
                # obligation. Require an updated, authority-resolved context.
                authority_failures.append({"code": "OBLIGATION_UNRESOLVED"})
                return None
        return record

    approval_resolver = lambda ref: authenticated(resolve_approval, ref, "approval", "APPROVAL.v2")
    exception_resolver = lambda ref: authenticated(resolve_exception, ref, "exception", "EXCEPTION_DECISION")
    if not gate_receipt_subject_binding_matches_gate(instance):
        findings.append({"code": "SUBJECT_BINDING_INVALID"})
    if not gate_receipt_decision_consistent(instance):
        findings.append({"code": "DECISION_INCONSISTENT"})
    if not gate_receipt_independence_is_sufficient(instance, risk_level=risk_level):
        findings.append({"code": "INDEPENDENCE_BELOW_MINIMUM"})
    status = receipt["decision"]["status"]
    if status == "WAIVED" and not gate_receipt_waiver_is_justified(
        instance, resolve_exception=exception_resolver, now=now,
        non_waivable_controls=NON_WAIVABLE_CONTROLS | non_waivable_controls | set(context.get("non_waivable_controls", [])),
    ):
        findings.append({"code": "WAIVER_NOT_JUSTIFIED"})
        findings.extend(authority_failures)
    if status in {"PASS", "WAIVED"} and not gate_receipt_has_valid_human_approval(
        instance, resolve_approval=approval_resolver, now=now,
    ):
        findings.append({"code": "APPROVAL_NOT_JUSTIFIED"})
        findings.extend(authority_failures)
    eligible = status in {"PASS", "WAIVED"} and not findings
    return {"status": "admitted" if eligible else "rejected", "findings": findings, "decision_status": status}


def authorize_gate_transition(
    gate_receipt_instance: dict,
    evidence_bundle_instance: dict | None = None,
    *,
    resolve_exception,
    resolve_approval,
    now: datetime,
    resolve_adapter=None,
    non_waivable_controls: set[str] = NON_WAIVABLE_CONTROLS,
    risk_level: str | None = None,
    resolve_property_profile=None,
    verify_authority=None,
    decision_context: dict | None = None,
) -> dict:
    """Top-level authorization combining a Gate Receipt evaluation with an
    optional associated Evidence Bundle evaluation. This is the function a
    runtime should call to answer "may this transition actually proceed?"
    -- never a bare individual predicate, and never only one of the two
    aggregate evaluators when both records apply to the same decision."""
    gate_result = evaluate_gate_receipt(
        gate_receipt_instance,
        resolve_exception=resolve_exception,
        resolve_approval=resolve_approval,
        now=now,
        non_waivable_controls=non_waivable_controls,
        risk_level=risk_level,
        verify_authority=verify_authority,
        decision_context=decision_context,
    )
    findings = list(gate_result["findings"])
    eligible = gate_result["status"] == "admitted"
    if evidence_bundle_instance is not None:
        bundle_result = evaluate_evidence_bundle(evidence_bundle_instance, resolve_adapter=resolve_adapter,
                                                resolve_property_profile=resolve_property_profile)
        findings.extend(bundle_result["findings"])
        eligible = eligible and bundle_result["status"] == "admitted"
        if not _schema_findings(gate_receipt_instance, "GATE_RECEIPT") and not _schema_findings(evidence_bundle_instance, "EVIDENCE_BUNDLE.v2"):
            receipt = gate_receipt_instance["gate_receipt"]
            bundle = evidence_bundle_instance["bundle"]
            if (receipt["task_id"] != bundle["task_id"] or
                    receipt["subject_state"].get("subject_digest") != bundle["baseline"]["subject_state"]["subject_digest"] or
                    receipt["subject_state"].get("requirement_baseline_id") != bundle["baseline"]["requirement_baseline_id"] or
                    receipt["policy"] != bundle["policy_binding"] or
                    set(receipt["claims"]["required"]) != {c["claim_id"] for c in bundle["claims"]}):
                findings.append({"code": "GATE_EVIDENCE_BINDING_MISMATCH"})
            if decision_context and bundle["risk_level"] != decision_context.get("risk_level"):
                findings.append({"code": "RISK_LEVEL_MISMATCH"})
    elif gate_receipt_instance.get("gate_receipt", {}).get("gate") != "gate_1":
        findings.append({"code": "EVIDENCE_BUNDLE_REQUIRED"})
    eligible = eligible and not findings
    return {"status": "admitted" if eligible else "rejected", "findings": findings}


# ---------------------------------------------------------------------------
# Evidence Adapter Registry (docs/agile-v-runtime/15_EVIDENCE_ADAPTER_REGISTRY.md)
# ---------------------------------------------------------------------------
#
# The registry is the trusted, policy-side source of evidence-source and
# evidence-property profiles. It is loaded from repository-owned files whose
# digests are pinned in catalog/evidence-adapters.json. Evidence producers
# never supply profiles: a profile embedded in an evidence item is rejected.

REGISTRY_ADMISSIBLE_STATUSES = frozenset({"candidate", "stable"})


class RegistryIntegrityError(ValueError):
    """The registry files do not match their catalog digests (fail closed)."""


def _version_key(version: str) -> tuple[int, ...]:
    parts = version.strip().split(".")
    if not parts or not all(p.isdigit() for p in parts):
        raise ValueError(version)
    key = [int(p) for p in parts]
    while len(key) > 1 and key[-1] == 0:
        key.pop()
    return tuple(key)


def version_in_scope(version, spec: str) -> bool:
    """True only when ``version`` satisfies every clause of ``spec``.

    ``spec`` is ``*`` or comma-separated clauses of ``>=,<=,==,<,>`` with
    dotted numeric versions. Unparseable versions never satisfy a non-``*``
    scope (fail closed).
    """
    if spec == "*":
        return True
    if not isinstance(version, str):
        return False
    try:
        actual = _version_key(version)
    except ValueError:
        return False
    import operator
    ops = {">=": operator.ge, "<=": operator.le, "==": operator.eq, "<": operator.lt, ">": operator.gt}
    for clause in spec.split(","):
        clause = clause.strip()
        op = next(o for o in (">=", "<=", "==", "<", ">") if clause.startswith(o))
        if not ops[op](actual, _version_key(clause[len(op):])):
            return False
    return True


class EvidenceAdapterRegistry:
    """Trusted, digest-pinned view of the evidence adapter registry.

    ``resolve_adapter``/``resolve_property_profile`` return only current,
    non-historical entries whose status is admissible. ``resolve_snapshot``
    returns any registered snapshot -- including historical/deprecated ones --
    by exact (id, digest) match only.
    """

    def __init__(self, catalog: dict, records: dict[str, dict]):
        self._catalog = deepcopy(catalog)
        self._sources: list[tuple[dict, dict]] = []
        self._properties: list[tuple[dict, dict]] = []
        for entry in catalog.get("adapters", []):
            record = records.get(entry["profile_path"])
            if record is None or profile_digest(record) != entry["profile_digest"]:
                raise RegistryIntegrityError(entry["profile_path"])
            if record["adapter"]["adapter_id"] != entry["adapter_id"]:
                raise RegistryIntegrityError(entry["profile_path"])
            self._sources.append((entry, deepcopy(record)))
        for entry in catalog.get("property_profiles", []):
            record = records.get(entry["profile_path"])
            if record is None or profile_digest(record) != entry["profile_digest"]:
                raise RegistryIntegrityError(entry["profile_path"])
            self._properties.append((entry, deepcopy(record)))

    @classmethod
    def from_repository(cls, root: Path | None = None) -> "EvidenceAdapterRegistry":
        import yaml
        root = root or Path(__file__).resolve().parents[1]
        catalog = json.loads((root / "catalog" / "evidence-adapters.json").read_text(encoding="utf-8"))
        records = {}
        for entry in catalog.get("adapters", []) + catalog.get("property_profiles", []):
            path = root / entry["profile_path"]
            try:
                records[entry["profile_path"]] = yaml.safe_load(path.read_text(encoding="utf-8"))
            except OSError as exc:
                raise RegistryIntegrityError(entry["profile_path"]) from exc
        return cls(catalog, records)

    @property
    def catalog(self) -> dict:
        return deepcopy(self._catalog)

    def resolve_adapter(self, ref):
        for entry, record in self._sources:
            if (entry["adapter_id"] == ref and not entry["historical"]
                    and entry["status"] in REGISTRY_ADMISSIBLE_STATUSES):
                return deepcopy(record)
        return None

    def resolve_snapshot(self, ref, digest):
        for entry, record in self._sources:
            if entry["adapter_id"] == ref and entry["profile_digest"] == digest:
                return deepcopy(record)
        return None

    def is_superseded_snapshot(self, ref, digest) -> bool:
        return any(entry["adapter_id"] == ref and entry["profile_digest"] == digest
                   and (entry["historical"] or entry["status"] == "deprecated")
                   for entry, _ in self._sources)

    def resolve_property_profile(self, claim_type, risk_level):
        for entry, record in self._properties:
            if ((entry["claim_type"], entry["risk_level"]) == (claim_type, risk_level)
                    and entry["status"] in REGISTRY_ADMISSIBLE_STATUSES):
                return deepcopy(record)
        return None

    def historical_adapter_resolver(self, bundle_instance: dict):
        """Resolver that returns, per adapter_ref, the exact snapshot the
        bundle's evidence is bound to. Conflicting digests for one ref, or a
        digest not in the registry, resolve to nothing (fail closed)."""
        bound: dict[str, set] = {}
        for item in bundle_instance.get("bundle", {}).get("evidence", []):
            source = item.get("evidence_source") or {}
            bound.setdefault(source.get("adapter_ref"), set()).add(source.get("adapter_digest"))

        def resolve(ref):
            digests = bound.get(ref, set())
            if len(digests) != 1:
                return None
            return self.resolve_snapshot(ref, next(iter(digests)))
        return resolve


SELF_SUPPLIED_PROFILE_KEYS = frozenset({"profile", "adapter_profile", "source_profile", "may_establish"})


def evaluate_evidence_bundle_against_registry(instance: dict, registry: EvidenceAdapterRegistry, *,
                                              historical: bool = False) -> dict:
    """Aggregate evidence evaluation using ONLY the trusted registry.

    ``historical=False`` answers "is this admissible under current profiles?".
    ``historical=True`` answers "was this valid under the exact profile
    snapshots it was bound to?" -- it never establishes current reuse
    eligibility (see 10_CHANGE_AWARE_REVALIDATION.md).
    """
    resolver = registry.historical_adapter_resolver(instance) if historical else registry.resolve_adapter
    result = evaluate_evidence_bundle(instance, resolve_adapter=resolver,
                                      resolve_property_profile=registry.resolve_property_profile)
    if any(f["code"] == "SCHEMA_INVALID" for f in result["findings"]):
        return result
    findings = list(result["findings"])
    for item in instance["bundle"]["evidence"]:
        locator = {"evidence_ref": item["evidence_id"]}
        source = item.get("evidence_source") or {}
        ref = source.get("adapter_ref")
        if SELF_SUPPLIED_PROFILE_KEYS & set(source):
            findings.append({"code": "EVIDENCE_SOURCE_SELF_SUPPLIED_PROFILE", **locator})
        if not historical and registry.is_superseded_snapshot(ref, source.get("adapter_digest")):
            findings.append({"code": "EVIDENCE_SOURCE_SUPERSEDED", **locator})
        record = resolver(ref)
        if record is None:
            continue
        adapter = record["adapter"]
        scope = adapter.get("source_version_scope", {}).get("supported_versions", "*")
        if scope != "*":
            if not source.get("tool_version"):
                findings.append({"code": "EVIDENCE_SOURCE_TOOL_VERSION_UNKNOWN", **locator})
            elif not version_in_scope(source["tool_version"], scope):
                findings.append({"code": "EVIDENCE_SOURCE_TOOL_VERSION_UNSUPPORTED", **locator})
        locators = source.get("locators")
        required = adapter.get("minimum_evidence_locators", [])
        if required and (not isinstance(locators, dict) or
                         not all(isinstance(locators.get(k), str) and locators.get(k) for k in required)):
            findings.append({"code": "EVIDENCE_LOCATOR_MISSING", **locator})
    return {"status": "rejected" if findings else "admitted", "findings": findings}


# ---------------------------------------------------------------------------
# Delegation v2 (schemas/AGENT_DELEGATION_RECORD.v2.schema.json,
# docs/agile-v-runtime/05_AGENT_TOOL_AND_DELEGATION_CONTRACT.md section 3.1)
# ---------------------------------------------------------------------------
#
# Delegation may preserve or reduce authority. It may never increase it.
# Scope sets are compared literally: no wildcard, prefix or pattern grants
# anything ("*" is an ordinary string). Unknown parent authority rejects.

SIDE_EFFECT_ORDER = ["none", "internal_state", "external_state", "irreversible"]
DELEGATION_SCOPE_FIELDS = ("requirements", "actions", "resources", "tools", "data_classes")
_AUTHORITY_REQUIRED = {"id", "holder_identity_ref", "task_id", "scope", "authority_ceiling", "expires_at", "status"}


def delegation_scope_is_subset_of_parent(child_scope: dict, parent_scope: dict) -> list[str]:
    """Return the scope fields in which the child adds anything."""
    return [field for field in DELEGATION_SCOPE_FIELDS
            if not set(child_scope.get(field, [])) <= set(parent_scope.get(field, []))]


def delegation_authority_is_attenuated(child_ceiling: dict, parent_ceiling: dict) -> list[str]:
    """Return reason codes for every ceiling dimension the child raises."""
    codes = []
    if RISK_LEVEL_ORDER.index(child_ceiling["max_risk_level"]) > RISK_LEVEL_ORDER.index(parent_ceiling["max_risk_level"]):
        codes.append("DELEGATION_RISK_ESCALATION")
    if SIDE_EFFECT_ORDER.index(child_ceiling["max_side_effect"]) > SIDE_EFFECT_ORDER.index(parent_ceiling["max_side_effect"]):
        codes.append("DELEGATION_SIDE_EFFECT_ESCALATION")
    return codes


def delegation_time_is_within_parent(child: dict, parent_expires_at: str) -> bool:
    return _parse_datetime(child["delegation"]["expires_at"]) <= _parse_datetime(parent_expires_at)


def delegation_depth_is_allowed(child_ceiling: dict, parent_ceiling: dict) -> list[str]:
    """A parent must permit re-delegation; the child's remaining depth must
    be strictly smaller and it cannot gain re-delegation the parent lacks."""
    codes = []
    if not parent_ceiling["may_delegate_further"] or parent_ceiling["max_delegation_depth"] < 1:
        codes.append("DELEGATION_REDELEGATION_NOT_PERMITTED")
    elif child_ceiling["max_delegation_depth"] > parent_ceiling["max_delegation_depth"] - 1:
        codes.append("DELEGATION_DEPTH_EXCEEDED")
    if child_ceiling["may_delegate_further"] and child_ceiling["max_delegation_depth"] < 1:
        codes.append("DELEGATION_DEPTH_EXCEEDED")
    return codes


def _authority_is_well_formed(record) -> bool:
    if not isinstance(record, dict) or not isinstance(record.get("authority"), dict):
        return False
    authority = record["authority"]
    if not _AUTHORITY_REQUIRED <= authority.keys():
        return False
    ceiling, scope = authority["authority_ceiling"], authority["scope"]
    try:
        _parse_datetime(authority["expires_at"])
        return (isinstance(scope, dict) and isinstance(ceiling, dict)
                and all(isinstance(scope.get(f), list) for f in DELEGATION_SCOPE_FIELDS)
                and ceiling.get("max_risk_level") in RISK_LEVEL_ORDER
                and ceiling.get("max_side_effect") in SIDE_EFFECT_ORDER
                and isinstance(ceiling.get("may_delegate_further"), bool)
                and isinstance(ceiling.get("max_delegation_depth"), int))
    except (TypeError, ValueError, AttributeError):
        return False


def _link_findings(child: dict, parent_scope: dict, parent_ceiling: dict, parent_expires: str,
                   *, root: bool) -> list[dict]:
    ref = child["delegation"]["id"]
    findings = [{"code": "DELEGATION_SCOPE_EXPANSION", "delegation_ref": ref, "field": field}
                for field in delegation_scope_is_subset_of_parent(child["scope"], parent_scope)]
    findings += [{"code": code, "delegation_ref": ref}
                 for code in delegation_authority_is_attenuated(child["authority_ceiling"], parent_ceiling)]
    if not delegation_time_is_within_parent(child, parent_expires):
        findings.append({"code": "DELEGATION_EXPIRY_EXTENDED", "delegation_ref": ref})
    child_ceiling = child["authority_ceiling"]
    if root:
        # A root grant is bounded by the authority itself: it may not
        # exceed the authority's own re-delegation depth.
        if child_ceiling["max_delegation_depth"] > parent_ceiling["max_delegation_depth"]:
            findings.append({"code": "DELEGATION_DEPTH_EXCEEDED", "delegation_ref": ref})
        if child_ceiling["may_delegate_further"] and not parent_ceiling["may_delegate_further"]:
            findings.append({"code": "DELEGATION_REDELEGATION_NOT_PERMITTED", "delegation_ref": ref})
    else:
        findings += [{"code": code, "delegation_ref": ref}
                     for code in delegation_depth_is_allowed(child_ceiling, parent_ceiling)]
    return findings


def delegation_chain_is_valid(record: dict, **kwargs) -> bool:
    """Boolean convenience over ``evaluate_delegation``; prefer the findings."""
    return evaluate_delegation(record, **kwargs)["status"] == "admitted"


def evaluate_delegation(record: dict, *, resolve_delegation, resolve_authority, now: datetime,
                        is_nonce_consumed=None, request: dict | None = None,
                        max_chain_length: int = 16) -> dict:
    """Canonical aggregate evaluator for a v2 delegation (and its chain).

    resolve_delegation(ref) -> durable v2 record or None (trusted store).
    resolve_authority(ref)  -> {"authority": {...}} grant from the trusted
        authority provider, already authenticated; None when unknown.
    is_nonce_consumed(nonce) -> True when a single-use delegation was used.
    request: optional {"action", "resource", "tool", "data_class",
        "requirement", "risk_level", "side_effect"} checked against the leaf.

    Evaluation never consumes a nonce; the runtime must do that atomically
    at the effect boundary.
    """
    findings = _schema_findings(record, "AGENT_DELEGATION_RECORD.v2")
    if findings:
        return {"status": "rejected", "findings": findings, "chain": []}
    if not isinstance(now, datetime) or now.tzinfo is None:
        return {"status": "rejected", "findings": [{"code": "EVALUATION_TIME_INVALID"}], "chain": []}
    chain = [deepcopy(record)]
    seen = {record["delegation"]["id"]}
    while chain[-1]["delegation"]["parent_delegation_ref"] is not None:
        parent_ref = chain[-1]["delegation"]["parent_delegation_ref"]
        if parent_ref in seen or len(chain) >= max_chain_length:
            findings.append({"code": "DELEGATION_CHAIN_CYCLE", "delegation_ref": parent_ref})
            return {"status": "rejected", "findings": findings, "chain": [c["delegation"]["id"] for c in chain]}
        parent = _resolve(resolve_delegation, (parent_ref,), "DELEGATION_PARENT_UNRESOLVED", findings,
                          delegation_ref=parent_ref)
        if parent is None:
            return {"status": "rejected", "findings": findings, "chain": [c["delegation"]["id"] for c in chain]}
        errors = _schema_findings(parent, "AGENT_DELEGATION_RECORD.v2")
        if errors or parent["delegation"]["id"] != parent_ref:
            findings.extend(errors or [{"code": "DELEGATION_PARENT_UNRESOLVED", "delegation_ref": parent_ref}])
            return {"status": "rejected", "findings": findings, "chain": [c["delegation"]["id"] for c in chain]}
        seen.add(parent_ref)
        chain.append(parent)
    ids = [c["delegation"]["id"] for c in chain]

    root = chain[-1]
    authority_ref = root["delegation"]["source_authority_ref"]
    authority_record = _resolve(resolve_authority, (authority_ref,), "DELEGATION_AUTHORITY_UNRESOLVED",
                                findings, authority_ref=authority_ref)
    if authority_record is not None and not _authority_is_well_formed(authority_record):
        findings.append({"code": "DELEGATION_AUTHORITY_INVALID", "authority_ref": authority_ref})
        authority_record = None
    if authority_record is not None:
        authority = authority_record["authority"]
        if authority["id"] != authority_ref:
            findings.append({"code": "DELEGATION_AUTHORITY_INVALID", "authority_ref": authority_ref})
        if authority["status"] != "active" or _parse_datetime(authority["expires_at"]) <= now:
            findings.append({"code": "DELEGATION_AUTHORITY_REVOKED", "authority_ref": authority_ref})
        if authority["holder_identity_ref"] != root["delegator"]["authenticated_identity_ref"]:
            findings.append({"code": "DELEGATION_CHAIN_BROKEN", "delegation_ref": root["delegation"]["id"]})
        if authority["task_id"] != root["delegation"]["task_id"]:
            findings.append({"code": "DELEGATION_TASK_MISMATCH", "delegation_ref": root["delegation"]["id"]})
        findings += _link_findings(root, authority["scope"], authority["authority_ceiling"],
                                   authority["expires_at"], root=True)

    nonces = set()
    for index, item in enumerate(chain):
        ref = item["delegation"]["id"]
        issued = _parse_datetime(item["delegation"]["issued_at"])
        expires = _parse_datetime(item["delegation"]["expires_at"])
        if item["revocation"]["status"] == "revoked":
            findings.append({"code": "DELEGATION_REVOKED", "delegation_ref": ref})
        if item["revocation"]["status"] == "expired" or expires <= now:
            findings.append({"code": "DELEGATION_EXPIRED", "delegation_ref": ref})
        if issued > now or expires <= issued:
            findings.append({"code": "DELEGATION_NOT_YET_VALID", "delegation_ref": ref})
        nonce = item["delegation"]["nonce"]
        if nonce in nonces:
            findings.append({"code": "DELEGATION_REPLAYED", "delegation_ref": ref})
        nonces.add(nonce)
        if index == 0 and item["delegation"]["single_use"]:
            try:
                consumed = is_nonce_consumed is None or is_nonce_consumed(nonce) is not False
            except Exception:
                consumed = True
            if consumed:
                findings.append({"code": "DELEGATION_REPLAYED", "delegation_ref": ref})
        if index + 1 < len(chain):
            parent = chain[index + 1]
            if (item["delegator"]["authenticated_identity_ref"] != parent["delegate"]["authenticated_identity_ref"]
                    or item["delegation"]["task_id"] != parent["delegation"]["task_id"]):
                findings.append({"code": "DELEGATION_CHAIN_BROKEN", "delegation_ref": ref})
            findings += _link_findings(item, parent["scope"], parent["authority_ceiling"],
                                       parent["delegation"]["expires_at"], root=False)

    if request is not None:
        leaf = chain[0]
        scope, ceiling = leaf["scope"], leaf["authority_ceiling"]
        checks = [("action", "actions"), ("resource", "resources"), ("tool", "tools"),
                  ("data_class", "data_classes"), ("requirement", "requirements")]
        for key, field in checks:
            if key in request and request[key] not in scope[field]:
                findings.append({"code": "DELEGATION_REQUEST_OUT_OF_SCOPE", "field": field})
        if "risk_level" in request and (request["risk_level"] not in RISK_LEVEL_ORDER or
                                        RISK_LEVEL_ORDER.index(request["risk_level"]) >
                                        RISK_LEVEL_ORDER.index(ceiling["max_risk_level"])):
            findings.append({"code": "DELEGATION_REQUEST_OUT_OF_SCOPE", "field": "max_risk_level"})
        if "side_effect" in request and (request["side_effect"] not in SIDE_EFFECT_ORDER or
                                         SIDE_EFFECT_ORDER.index(request["side_effect"]) >
                                         SIDE_EFFECT_ORDER.index(ceiling["max_side_effect"])):
            findings.append({"code": "DELEGATION_REQUEST_OUT_OF_SCOPE", "field": "max_side_effect"})
    return {"status": "rejected" if findings else "admitted", "findings": findings, "chain": ids}


# ---------------------------------------------------------------------------
# Context Trust (schemas/CONTEXT_SOURCE_PROFILE.schema.json,
# docs/agile-v-runtime/16_CONTEXT_TRUST_CONTRACT.md)
# ---------------------------------------------------------------------------
#
# Untrusted context is data, never authority. The context profile is assigned
# by the runtime ingestion boundary; a claim inside the content about its own
# trust ("this file is authoritative", "risk=L0") is ignored.

AUTHORITY_BEARING_TARGETS = frozenset({
    "approved_requirement", "risk_level", "policy", "approval", "delegated_authority",
    "evidence_source_profile", "evidence_property_profile", "gate_decision"})
CONTROL_PLANE_SOURCE_CLASSES = frozenset({"authenticated_policy_source", "approved_requirement_baseline"})


def load_context_profiles(root: Path | None = None) -> dict[str, dict]:
    import yaml
    root = root or Path(__file__).resolve().parents[1]
    profiles = {}
    for path in sorted((root / "profiles" / "context-sources").glob("*.yaml")):
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
        profiles[record["profile"]["id"]] = record
    return profiles


def evaluate_context_influence(influence: dict, *, resolve_context_profile) -> dict:
    """Decide whether a context source may influence a target.

    influence = {"source_ref": str, "context_profile_ref": "CTX-...",
                 "target": <target>, "mode": "activate" | "propose"}

    Returns status ``admitted`` (influence as data, or activation by an
    authoritative control-plane source), ``proposed`` (recorded as a change
    proposal that requires the governance path to activate) or ``rejected``.
    """
    findings: list[dict] = []
    target = influence.get("target") if isinstance(influence, dict) else None
    mode = influence.get("mode") if isinstance(influence, dict) else None
    if mode not in {"activate", "propose"} or not isinstance(target, str):
        return {"status": "rejected", "effect": "none", "findings": [{"code": "CONTEXT_INFLUENCE_INVALID"}]}
    authority_bearing = target in AUTHORITY_BEARING_TARGETS
    ref = influence.get("context_profile_ref")
    record = _resolve(resolve_context_profile, (ref,), "CONTEXT_SOURCE_UNKNOWN", findings, context_profile_ref=ref)
    if record is not None:
        errors = _schema_findings(record, "CONTEXT_SOURCE_PROFILE")
        if errors or record["profile"]["id"] != ref:
            findings.extend(errors or [{"code": "CONTEXT_SOURCE_UNKNOWN", "context_profile_ref": ref}])
            record = None
    if record is None:
        if authority_bearing:
            return {"status": "rejected", "effect": "none", "findings": findings}
        # Non-authority targets: unknown sources are still usable as untrusted data.
        return {"status": "admitted", "effect": "data", "findings": findings}
    profile = record["profile"]
    authoritative = (profile["default_trust"] == "authoritative"
                     and profile["source_class"] in CONTROL_PLANE_SOURCE_CLASSES)
    if target in profile["may_not_influence"]:
        if mode == "propose" and target in profile["may_propose"]:
            return {"status": "proposed", "effect": "proposal", "findings": []}
        code = "CONTEXT_AUTHORITY_ESCALATION" if authority_bearing else "CONTEXT_INFLUENCE_NOT_PERMITTED"
        return {"status": "rejected", "effect": "none", "findings": [{"code": code, "target": target}]}
    if mode == "propose":
        if target in profile["may_propose"] or (not authority_bearing and target in profile["may_influence"]):
            return {"status": "proposed", "effect": "proposal", "findings": []}
        return {"status": "rejected", "effect": "none",
                "findings": [{"code": "CONTEXT_PROPOSAL_NOT_PERMITTED", "target": target}]}
    if target not in profile["may_influence"]:
        code = "CONTEXT_AUTHORITY_ESCALATION" if authority_bearing else "CONTEXT_INFLUENCE_NOT_PERMITTED"
        return {"status": "rejected", "effect": "none", "findings": [{"code": code, "target": target}]}
    if authority_bearing and not authoritative:
        return {"status": "rejected", "effect": "none",
                "findings": [{"code": "CONTEXT_AUTHORITY_ESCALATION", "target": target}]}
    return {"status": "admitted", "effect": "activate" if authority_bearing else "data", "findings": []}


# ---------------------------------------------------------------------------
# Revalidation reuse aggregate (10_CHANGE_AWARE_REVALIDATION.md)
# ---------------------------------------------------------------------------

def evaluate_revalidation_reuse(assessment_instance: dict, evidence_item: dict) -> dict:
    """May this evidence item be reused for a current decision after change?

    Admitted only when the assessment is schema-valid and conservative, the
    item's own evaluation is UNCHANGED with complete coverage, the item
    declares its invalidation dependencies, and none of the changed
    dependency kinds is one the item declares (an UNCHANGED verdict that
    contradicts a declared dependency is rejected, not trusted).
    """
    findings = _schema_findings(assessment_instance, "REVALIDATION_ASSESSMENT")
    if findings:
        return {"status": "rejected", "findings": findings}
    assessment = assessment_instance["assessment"]
    ref = evidence_item.get("evidence_id") if isinstance(evidence_item, dict) else None
    evaluation = next((e for e in assessment["evaluations"] if e["evidence_ref"] == ref), None)
    if evaluation is None:
        return {"status": "rejected", "findings": [{"code": "REVALIDATION_EVALUATION_MISSING", "evidence_ref": ref}]}
    if not revalidation_coverage_is_conservative(assessment_instance):
        findings.append({"code": "REVALIDATION_COVERAGE_NOT_CONSERVATIVE"})
    if evaluation["result"] not in REUSE_ELIGIBLE_RESULTS:
        findings.append({"code": "REVALIDATION_RESULT_NOT_REUSABLE", "result": evaluation["result"]})
    if evaluation.get("dependency_coverage", assessment["coverage"]) != "complete":
        findings.append({"code": "REVALIDATION_COVERAGE_INCOMPLETE"})
    dependencies = evidence_item.get("invalidation_dependencies")
    if not dependencies:
        findings.append({"code": "REVALIDATION_DEPENDENCIES_UNKNOWN", "evidence_ref": ref})
    else:
        changed = {c["kind"] for c in assessment["changed_refs"]}
        overlap = changed & {d["kind"] for d in dependencies}
        if overlap and evaluation["result"] == "UNCHANGED":
            findings.append({"code": "REVALIDATION_DEPENDENCY_CONFLICT", "kinds": sorted(overlap)})
    return {"status": "rejected" if findings else "admitted", "findings": findings}


# ---------------------------------------------------------------------------
# AI Influence Traceability (schemas/AI_RUN_MANIFEST.schema.json; draft skill
# agile-v-aibom). Reference checks used by the graduation evidence package.
# ---------------------------------------------------------------------------

import re as _re

_REASONING_MARKERS = _re.compile(r"<\s*/?\s*(thinking|reasoning|scratchpad)\b|chain[-_ ]of[-_ ]thought\s*:", _re.I)
_SECRET_PATTERNS = _re.compile(
    r"(-----BEGIN [A-Z ]*PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\bgh[pousr]_[A-Za-z0-9]{30,}\b|"
    r"\bsk-[A-Za-z0-9_-]{20,}\b|\bxox[abpr]-[A-Za-z0-9-]{10,}\b|\bBearer\s+[A-Za-z0-9._-]{20,})")
AIBOM_COMPONENT_KINDS = {"models": "model", "tools": "tool", "agile_v_skills": "skill"}


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def _aibom_components(manifest: dict):
    for field, kind in AIBOM_COMPONENT_KINDS.items():
        for index, item in enumerate(manifest.get(field) or []):
            yield kind, f"{field}[{index}]", item
    if isinstance(manifest.get("agent_runtime"), dict):
        yield "runtime", "agent_runtime", manifest["agent_runtime"]


def evaluate_ai_run_manifest(manifest: dict, *, resolve_source=None) -> dict:
    """Reference admission checks for an AI Run Manifest.

    ``verified`` confidence is accepted only when the component's
    ``evidence_locator`` is ``<adapter_ref>#<locator>`` and the trusted
    ``resolve_source(adapter_ref)`` profile may establish
    ``verified_<kind>_identity``. No registry v1 profile can, so ``verified``
    fails closed today: a declaration is never promoted to verification.
    """
    findings = _schema_findings(manifest, "AI_RUN_MANIFEST")
    if findings:
        return {"status": "rejected", "findings": findings}
    privacy = manifest["security_and_privacy"]
    text = list(_strings(manifest))
    if privacy["hidden_chain_of_thought_excluded"] is not True or any(_REASONING_MARKERS.search(s) for s in text):
        findings.append({"code": "AIBOM_HIDDEN_REASONING_CAPTURED"})
    if privacy["secrets_redacted"] is not True or any(_SECRET_PATTERNS.search(s) for s in text):
        findings.append({"code": "AIBOM_SECRET_CAPTURED"})
    risk = manifest["risk"]["agile_v_risk_level"]
    for kind, path, item in _aibom_components(manifest):
        confidence = item.get("confidence")
        if confidence == "verified":
            locator = item.get("evidence_locator") or ""
            ref = locator.split("#", 1)[0] if "#" in locator else None
            profile = None
            if ref and resolve_source is not None:
                try:
                    profile = resolve_source(ref)
                except Exception:
                    profile = None
            capability = f"verified_{kind}_identity"
            if not (isinstance(profile, dict) and capability in profile.get("adapter", {}).get("may_establish", [])
                    and capability not in profile.get("adapter", {}).get("may_not_establish", [])):
                findings.append({"code": "AIBOM_VERIFIED_WITHOUT_TRUSTED_SOURCE", "path": path})
        if (confidence == "unresolved" and kind in {"model", "runtime"}
                and RISK_LEVEL_ORDER.index(risk) >= RISK_LEVEL_ORDER.index("L3")):
            findings.append({"code": "AIBOM_UNRESOLVED_MATERIAL_IDENTITY", "path": path})
    return {"status": "rejected" if findings else "admitted", "findings": findings}


def _identity(kind: str, item: dict) -> tuple[str, dict]:
    if kind == "model":
        return item["name"], {k: item.get(k) for k in ("provider", "model_id", "model_version", "endpoint_or_deployment")}
    if kind == "tool":
        return item["name"], {k: item.get(k) for k in ("type", "version", "allowed", "used")}
    if kind == "skill":
        return item["skill"], {k: item.get(k) for k in ("version", "source", "commit_sha")}
    return "agent_runtime", {k: item.get(k) for k in ("agent_name", "agent_framework", "framework_version",
                                                      "sandbox_image", "sandbox_image_digest", "execution_environment")}


# AI-BOM component kind -> Change-Aware Revalidation dependency kind.
AIBOM_REVALIDATION_KIND = {"model": "model", "tool": "tool", "skill": "tool", "runtime": "environment"}


def ai_bom_diff(baseline: dict, current: dict) -> list[dict]:
    """Material AI-context changes between two manifests, as revalidation
    ``changed_refs`` entries ({kind, ref, change, ai_component}). Confidence
    changes are reported too, so a declared->verified flip is never silent."""
    def index(manifest):
        result = {}
        for kind, _, item in _aibom_components(manifest):
            name, identity = _identity(kind, item)
            result[(kind, name)] = (identity, item.get("confidence"))
        return result
    before, after = index(baseline), index(current)
    changes = []
    for key in sorted(set(before) | set(after)):
        kind, name = key
        if key not in before:
            change = "added"
        elif key not in after:
            change = "removed"
        elif before[key][0] != after[key][0]:
            change = "modified"
        elif before[key][1] != after[key][1]:
            change = "confidence_changed"
        else:
            continue
        changes.append({"kind": AIBOM_REVALIDATION_KIND[kind], "ref": f"{kind}:{name}", "change": change,
                        "ai_component": kind})
    return changes


def reconcile_ai_inventory(declared_models: list[dict], observed_components: list[dict]) -> list[dict]:
    """Compare declared models with an observed runtime inventory (e.g. a
    k8s-aibom export normalized to {name, model_id, confidence}). Observed
    confidence is retained as reported; nothing is upgraded to verified."""
    observed = {c.get("model_id") or c.get("name"): c for c in observed_components}
    declared = {m["model_id"]: m for m in declared_models}
    findings = []
    for model_id, model in sorted(declared.items()):
        match = observed.get(model_id)
        if match is None:
            findings.append({"code": "AIBOM_DECLARED_NOT_OBSERVED", "model_id": model_id,
                             "declared_confidence": model.get("confidence")})
        else:
            findings.append({"code": "AIBOM_OBSERVED", "model_id": model_id,
                             "declared_confidence": model.get("confidence"),
                             "observed_confidence": match.get("confidence", "unresolved")})
    for model_id in sorted(set(observed) - set(declared)):
        findings.append({"code": "AIBOM_OBSERVED_NOT_DECLARED", "model_id": model_id,
                         "observed_confidence": observed[model_id].get("confidence", "unresolved")})
    return findings
