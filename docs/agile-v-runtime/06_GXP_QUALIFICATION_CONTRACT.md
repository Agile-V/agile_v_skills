# 06 — GxP Qualification Contract

> **Status:** Draft companion contract for the `agile-v-gxp-qualification` skill.
> This Agile V profile supports structured qualification and validation evidence. It does not determine legal applicability, replace controlled procedures, provide technical Part 11 controls, or establish regulatory compliance.

This document defines the machine-checkable evidence contracts a consuming runtime relies on when qualification is enabled. The skill (`agile-v-gxp-qualification/SKILL.md`) is the normative narrative; the schemas are the evidence contract.

## Evidence stages, not agents

`DQ`, `IQ`, `OQ`, `PQ` are **evidence stages**. Agents contribute evidence to them:

| Stage | Primary evidence contributors | Never |
|---|---|---|
| DQ | independent design review (not the builder) | `logic-gatekeeper` requirement review is not DQ |
| IQ / IOQ | `build-agent` installation inputs; qualification executor against a named `SYSTEM_BASELINE` | producing deployable software is not IQ |
| OQ | `test-designer` (design), `red-team-verifier` (execute/challenge) | OQ is not PQ or intended-use acceptance |
| PQ | `validation-agent` intended-use validation | a verification report is not PQ by itself |
| Summary | `compliance-auditor` | passing tests are not regulatory release |

## Schemas

| Record | Schema | Template |
|---|---|---|
| Qualification plan | `schemas/QUALIFICATION_PLAN.schema.json` | `templates/agile-v/QUALIFICATION_PLAN.example.yaml` |
| System description | `schemas/SYSTEM_DESCRIPTION.schema.json` | `templates/agile-v/SYSTEM_DESCRIPTION.example.yaml` |
| System baseline | `schemas/SYSTEM_BASELINE.schema.json` | `templates/agile-v/SYSTEM_BASELINE.example.yaml` |
| Protocol | `schemas/QUALIFICATION_PROTOCOL.schema.json` | `templates/agile-v/QUALIFICATION_PROTOCOL.example.yaml` |
| Execution | `schemas/QUALIFICATION_EXECUTION.schema.json` | `templates/agile-v/QUALIFICATION_EXECUTION.example.yaml` |
| Deviation | `schemas/QUALIFICATION_DEVIATION.schema.json` | `templates/agile-v/QUALIFICATION_DEVIATION.example.yaml` |
| Summary | `schemas/QUALIFICATION_SUMMARY.schema.json` | `templates/agile-v/QUALIFICATION_SUMMARY.example.yaml` |
| Requalification | `schemas/REQUALIFICATION_ASSESSMENT.schema.json` | `templates/agile-v/REQUALIFICATION_ASSESSMENT.example.yaml` |

Qualification also integrates optionally into `EVIDENCE_BUNDLE` (`bundle.qualification`), `CONTROL_MATRIX` (top-level `qualification` policy), and `TRACE_GRAPH` (qualification node/relation types). Non-qualification projects remain backward-compatible: the section is optional everywhere.

## Conditional schema rules

- `DQ` protocol requires `design_refs` and `urs_refs`.
- `IQ`/`IOQ` protocol requires `baseline_ref`.
- `OQ` protocol requires `requirements` (requirement-derived links with revision + baseline).
- `PQ` protocol requires `representative_conditions`.
- Execution steps require both an approved `expected` (in protocol) and an observed `actual`; a bare `PASS` step with no `actual` is rejected.
- `WAIVED` requires an authorized `waiver` (approval_ref + rationale).
- `CONDITIONALLY_ACCEPTED` stages require `conditions` (with owner + due date), an `impact_assessment`, and an `approval_ref`.
- `SYSTEM_BASELINE` rejects `configuration.secret_values_recorded: true` — never record secret values in evidence.

## Runtime enforcement contract

The skills repository defines the contract. A consuming runtime SHOULD implement: schema validation in CI; approved-protocol locking or digest verification; baseline drift detection; identity-bound approvals; electronic signatures where required; append-only execution records; controlled evidence storage; required-stage transition blocking; forbidden self-approval checks; conditional-release expiry tracking; and requalification trigger detection.

> A skill instruction is not runtime enforcement. A schema-valid record is not proof of truth. A Git commit is not automatically a compliant electronic signature.

## Part 11 / Annex 11 boundary

Skills can define required identity fields, approval intent/scope, signature references, record/evidence structure, traceability, review requirements, audit checks, and negative test cases. Skills **cannot by themselves** provide authenticated individual identity, non-repudiable electronic signatures, signature-to-record binding, secure audit-trail infrastructure, RBAC enforcement, retention infrastructure, time-source integrity, write protection, validated backup/restore, or closed-system controls. The revised Annex 11 consultation draft is a **future-readiness input**, not final law or final GMP guidance.

## References

Regulatory and guidance anchors (public source URLs, editions, and status) are recorded in [`docs/standards/SOURCE_REGISTER.md`](../standards/SOURCE_REGISTER.md) under IDs `SRC-GXP-01` (Annex 15), `SRC-GXP-02` (Annex 11), `SRC-GXP-03` (21 CFR Part 11), `SRC-GXP-04` (FDA CSA), `SRC-GXP-05` (GAMP 5 2nd Ed.), `SRC-GXP-06` (ICH Q9(R1)/Q10), and `SRC-GXP-07` (ALCOA+). Verify the current edition and adoption before relying on any mapping; a register entry is not a requirement.
