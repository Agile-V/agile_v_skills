# Exception and Waiver Contract

> **Normative.** This contract defines waiver, concession, dispensation, residual-risk acceptance, and defer as distinct exception types, and states the rules that apply to all of them. It is implemented by `schemas/EXCEPTION_DECISION.schema.json` and referenced by Gate Receipts (`schemas/GATE_RECEIPT.schema.json`), the Red Team Verifier disposition model, and `agile-v-compliance`.

## 1. Why these must not be conflated

`WAIVED`, "accept as is," "defer," and "residual risk accepted" are used loosely in practice to mean "continue anyway." They are different decisions with different authority, scope, and expiry requirements. Collapsing them into one informal "it's fine" loses the information a later reviewer, auditor, or incident investigation needs.

## 2. Exception types

| Type | Definition |
|---|---|
| **Waiver** | A required criterion is intentionally not applied, for a defined scope and time. The underlying criterion still exists and still failed/was not met; the waiver permits proceeding without it. |
| **Concession** | A known nonconformity is accepted for a defined case (e.g. this specific artifact/batch), without changing the general requirement. |
| **Dispensation** | An obligation is temporarily released under authority (e.g. a due-obligation deadline is extended), distinct from waiving the obligation's substance. |
| **Residual-risk acceptance** | Remaining risk is explicitly accepted by an accountable owner; the underlying condition is not disputed, only its consequence is accepted. |
| **Defer** | Work remains open for future resolution; nothing is currently satisfied, waived, or accepted — it is scheduled. |

## 3. Required fields (all types)

```yaml
exception:
  id:                    # EXC-XXXX
  type:                  # waiver | concession | dispensation | residual_risk_acceptance | defer
  task_id:
  control_or_claim_ref:  # what is being excepted (CONTROL-ID, CLM-ID, REQ-ID, RISK-ID)
  rationale:
  scope:                 # exact bounded subject/subject-class, not "everything"
  approver:
  authority_source:
  issued_at:
  expires_at:
  monitoring:            # required for dispensation/residual-risk acceptance
  remediation_owner:
  target_resolution:
  evidence_refs:
```

See `schemas/EXCEPTION_DECISION.schema.json` for the structured form.

## 4. Rules

1. **Non-waivable meta-controls.** A valid exception cannot waive unknown identity, broken receipt/evidence integrity, absent subject binding, or the integrity of the gate itself. Domain policies (safety, security, regulatory) may additionally mark specific controls non-waivable; those controls MUST reject any exception referencing them regardless of approver.
2. **`WAIVED` never means "missing evidence, continue anyway."** `WAIVED` means: the criterion was not met (or not applicable in a way requiring a formal exception), and an authorized, scoped, time-bounded exception record exists. Missing evidence with no exception record is `BLOCKED`, not `WAIVED`.
3. **Visible in the Gate Receipt.** A gate decision that relies on an exception is not a clean `PASS`. It is `WAIVED` (or an equivalent explicit status), and the Gate Receipt lists the exception ID(s) alongside the underlying finding that was excepted. Display and exports must not flatten a waived decision into an unqualified PASS.
4. **Expiry is enforced.** An expired exception is invalid for any new decision; using an expired exception is equivalent to having no exception at all (`BLOCKED`, not `WAIVED`). Expiry does not delete the historical record.
5. **No propagation to later cycles.** An exception is scoped to the task/subject/time stated. A new cycle, new baseline, or new subject requires either a new exception decision or genuine resolution — it does not inherit the prior cycle's waiver.
6. **A waiver cannot grant authority to create further waivers.** Exception-granting authority is a property of the approver's role, not something an exception record can delegate onward.
7. **Distinguish accepted non-applicability from a retrospective waiver.** If a control is genuinely not applicable (e.g. a documentation-only change has no executable tests), that is an **applicability determination** made before/at gate time under the accepted contract — not a waiver of a failed test. Do not record a legitimately-inapplicable check as a waived failure, and do not use "not applicable" to retroactively excuse an actual failure.

## 5. Relationship to other contracts

- **Red Team Verifier disposition model** (`red-team-verifier/SKILL.md`, Severity & Disposition): `Accept-as-is/Concession` and `Defer` map directly to the `concession` and `defer` exception types here; both require a Decision Log rationale and, for anything beyond MINOR severity, a durable exception record per this contract.
- **Eval Gate `WAIVED` status** (`red-team-verifier/SKILL.md`): requires an `APPROVALS.md`/exception reference in `eval_gate_rationale`; this contract defines what that reference must contain.
- **Risk Management** (`agile-v-compliance`): a residual-risk decision in `RISK_REGISTER.md` is a `residual_risk_acceptance` exception; Critical risks still require Human resolution or a documented, scoped, owned acceptance — not a bare "accepted" note.
- **Gate Receipt** (`schemas/GATE_RECEIPT.schema.json`): `decision.status` reflects whether any exception was used; the receipt does not itself carry full exception content — it references `exception` IDs recorded per this contract.
