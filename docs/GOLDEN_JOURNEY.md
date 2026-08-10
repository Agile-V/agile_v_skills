# Agile V Golden Journey

> **Repository version:** 3.8.x
> **Purpose:** Canonical evidence flow for a new feature or controlled change. Tailor rigor to `L0`-`L4`; do not skip required human or independent roles.

## Verification and Validation

| Activity | Question | Primary skill | Canonical result |
|---|---|---|---|
| Verification | Was the specified output built correctly against the approved baseline? | `red-team-verifier` | `.agile-v/VERIFICATION_SUMMARY.md`, `VER-XXXX`, test/eval evidence |
| Intended-use validation | Was the right system built for representative users, use, and operational conditions? | `validation-agent` | `VALIDATION_PLAN.md`, `VALIDATION_PROTOCOL.md`, `VALIDATION_REPORT.md` |

A verification pass does not establish intended-use validation. Validation is required only when the intended-use and risk context call for it, but it cannot replace failed verification.

## Canonical Flow

| Step | Activity | Evidence and stop condition |
|---|---|---|
| 1 | **Classify risk and scope.** Record delivery level `L0`-`L4`, affected configuration, uncertainty, controls, owner, and residual-risk authority. | `.agile-v/RISK_REGISTER.md`; unresolved scope, critical residual risk, or unknown authority blocks progress. |
| 2 | **Persist the draft.** Convert source intent into atomic requirements with acceptance criteria and typed source lineage. | `.agile-v/REQUIREMENTS.md` in `draft_persisted`; chat text is not synthesis input. |
| 3 | **Record independent findings.** `logic-gatekeeper` challenges ambiguity, conflicts, constraints, and testability without editing the draft. | Durable `FND-XXXX` findings; unresolved blocking findings return to the architect. |
| 4 | **Obtain Gate 1 approval.** The architect resolves or rejects each finding with rationale; an authorized human reviews the revision and findings. | Approval in `.agile-v/APPROVALS.md`; rejection returns to revision, not build. |
| 5 | **Freeze the baseline.** Capture the approved revision and register it. | Immutable baseline plus `.agile-v/ARTIFACT_INDEX.yaml`; only this baseline is synthesis input. |
| 6 | **Build and design tests independently.** Build artifacts implement the baseline; Test Designer derives tests from the baseline without reading implementation. Use separate fresh contexts, or run test design first if one context is unavoidable. | `ART-XXXX -> implements -> REQ-XXXX@revision`; `TC-XXXX -> verifies -> REQ-XXXX@revision`. |
| 7 | **Verify independently.** Red Team executes tests, challenges artifacts, records `VER-XXXX` findings, and requires re-verification after fixes. Requirement changes go through a change request and a new Gate 1 baseline. | `.agile-v/VERIFICATION_SUMMARY.md`; unresolved verification failures block Gate 2. |
| 8 | **Run the Eval Gate.** Execute required offline/online suites against policy thresholds. | `.agile-v/EVAL_RESULTS.md`; status must be `PASS` or an authorized `WAIVED`, and the `EvalGate` block belongs in `VERIFICATION_SUMMARY.md`. |
| 9 | **Perform intended-use validation when required.** Use representative users, environments, configurations, and data; reconcile anomalies and residual risk. | `VALIDATION_REPORT.md`; insufficiently representative evidence cannot support intended-use acceptance. |
| 10 | **Complete AI influence evidence.** For material AI influence, record model/runtime identity, loaded skills, tools, context sources, affected artifacts, hashes, tests, and evidence locators without secrets or hidden reasoning. | `.agile-v/aibom/<task-id>/AI_RUN_MANIFEST.yaml` linked to the evidence bundle; apply approved policy before using the preview `agile-v-aibom` skill. |
| 11 | **Obtain Gate 2 and release.** Present verification, applicable validation, Eval Gate, control conformance, trace coverage, open anomalies, rollback, and residual-risk evidence to the authorized human. | Gate 2 approval is durable; `release-manager` then executes the approved rollout/rollback plan. No autonomous production release. |

The normative state transitions and typed edges are defined in [Canonical Lifecycle Contract](agile-v-runtime/03_CANONICAL_LIFECYCLE_CONTRACT.md); minimum rigor by level is defined in [Risk Classification](agile-v-runtime/04_RISK_CLASSIFICATION.md).
