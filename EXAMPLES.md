# Agile V Examples

These compact scenarios illustrate the current lifecycle. The authoritative rules remain in each skill's `SKILL.md` and the [canonical lifecycle contract](docs/agile-v-runtime/03_CANONICAL_LIFECYCLE_CONTRACT.md).

## 1. Vague Authentication Request

**Request:** “Add login.”

1. Load the `verified-build` profile and classify authentication work at least `L2`.
2. Halt because method, users, sessions, threats, constraints, and acceptance criteria are unresolved.
3. `requirement-architect` persists atomic draft requirements; `logic-gatekeeper` independently records findings without silently editing them.
4. Resolve findings, obtain Human Gate 1 approval, and freeze the approved requirement revision as the baseline.
5. Build only from that baseline. Record typed lineage such as:

```text
ART-0001 -> implements -> REQ-0001@rev-2; baseline: BL-0001
TC-0001  -> verifies   -> REQ-0001@rev-2; baseline: BL-0001
```

6. `test-designer` derives tests from the baseline without reading the implementation. The Build Agent does not verify its own work.
7. `red-team-verifier` runs independent checks and writes `.agile-v/VERIFICATION_SUMMARY.md`. Failures return to synthesis and re-verification; requirement changes require a new approved baseline.
8. Gate 2 remains blocked until required verification and Eval Gate evidence passes or has an authorized waiver.

Follow the [Verified Authentication tutorial](docs/tutorials/verified-authentication.md) and [Independent Agent Verification tutorial](docs/tutorials/independent-agent-verification.md).

## 2. Change an Existing Repository

**Request:** “Change invoice rounding without breaking existing exports.”

1. Install the [`existing-repo` profile](docs/INSTALL_PROFILES.md). Do not infer architecture or impact from filenames alone.
2. `system-understanding-agent` captures evidence-backed components, interfaces, behavior, and uncertainty at Gate 0.
3. `impact-analysis-agent` maps the proposed change to affected code, data, interfaces, tests, risks, and downstream consumers. Unknown high-impact paths are halt conditions.
4. Formalize and baseline the change requirements. Existing behavior that must remain stable becomes explicit acceptance criteria.
5. Build from the approved revision. `regression-selection-agent` selects justified regression scope; `graph-traceability-agent` checks typed links; `diff-evidence-agent` compares the approved scope with the actual diff.
6. Independently verify changed and affected behavior. Record requirement coverage, findings, commands, evidence locators, and result counts in `.agile-v/VERIFICATION_SUMMARY.md`.
7. Present impact, regression, unresolved uncertainty, rollback, and verification evidence at the applicable Human Gate.

Use the [Golden Journey](docs/GOLDEN_JOURNEY.md) for lifecycle order and the [Independent Agent Verification tutorial](docs/tutorials/independent-agent-verification.md) for the right-side evidence flow.

## 3. Verification Versus Intended-Use Validation

**Scenario:** A medication reminder feature passes all specified tests, but release requires evidence that intended users can operate it safely in representative conditions.

| Activity | Question | Output |
|---|---|---|
| Independent verification | Was the specified output built correctly against the approved baseline? | `.agile-v/VERIFICATION_SUMMARY.md` from `red-team-verifier` |
| Intended-use validation | Was the right system built for representative users, environments, data, and operating conditions? | `VALIDATION_REPORT.md` from `validation-agent` or an authorized equivalent |

A verification pass does not establish intended-use acceptance. Validation cannot close failed verification, and it is required only when the intended-use and risk context call for it. Gate 2 reviews both records when both apply, including anomalies, representativeness limits, and residual risk.

See the distinction in the [Regulated Software Adoption tutorial](docs/tutorials/regulated-software-adoption.md) and the end-to-end authentication example in the [Verified Authentication tutorial](docs/tutorials/verified-authentication.md).

## Next Steps

Choose an [installation profile](docs/INSTALL_PROFILES.md), load `agile-v-core`, and follow the [tutorial index](docs/tutorials/README.md). Skills marked `metadata.status: draft` are preview contracts and require local review before operational use.

**License:** CC-BY-SA-4.0 | **Author:** Agile V™ | **Homepage:** https://github.com/Agile-V/agile_v_skills
