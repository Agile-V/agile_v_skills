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
