# Regulated Software Adoption

Agile V can organize lifecycle evidence inside an existing quality, safety, security, or regulatory system. It does not certify a product or organization, replace governing procedures, or determine legal applicability.

## Adopt in a Controlled Pilot

1. **Define authority.** Name the applicable quality system, governing profile, document-control rules, approval roles, retention, electronic-record/signature controls, and residual-risk acceptance authority.
2. **Choose one bounded change.** Avoid beginning with the highest-consequence release. Classify it `L0`-`L4`; regulated, sensitive-data, or high-impact work is generally `L3`, while safety-critical or externally assured release decisions are `L4`.
3. **Map records, do not duplicate blindly.** Map existing requirement, risk, change, test, trace, anomaly, CAPA, validation, and release records to Agile V artifacts. Document ownership and the authoritative system when names differ.
4. **Approve tailoring.** Specify which skills, schemas, tools, gates, independent roles, and retention controls apply. A local procedure takes precedence where it imposes stricter controls.
5. **Run the canonical lifecycle.** Persist draft requirements, record independent findings, resolve them, obtain Human Gate 1 approval, freeze the baseline, synthesize and design tests independently, verify, run the Eval Gate, perform applicable intended-use validation, and obtain the authorized release decision.
6. **Control AI influence.** If AI materially contributes, follow [AI run manifest](ai-run-manifest.md). Because `agile-v-aibom` is draft, approve its local use and required fields before relying on it operationally.
7. **Review the pilot.** Reconcile every claim with evidence, record gaps and deviations, test retrieval and audit readiness, and approve any expansion through change control.

## Evidence Boundary

| Question | Canonical evidence |
|---|---|
| Was the specified output built correctly? | `.agile-v/VERIFICATION_SUMMARY.md` from `red-team-verifier` |
| Was it acceptable for approved intended use in representative conditions? | `VALIDATION_REPORT.md` from `validation-agent` or an authorized equivalent |
| Who accepted residual risk or release? | Durable approval identifying authority, scope, date, and rationale |
| What AI context influenced the work? | `AI_RUN_MANIFEST.yaml` and linked evidence fragment |

Do not turn a passing test, signed manifest, trace matrix, or agent statement into a certification claim. Conclusions must stay bounded by the baseline, configuration, environment, data, users, deviations, anomalies, and evidence actually reviewed.

## Pilot Exit Criteria

Approve wider adoption only after accountable humans accept the tailoring, open gaps have owners and dispositions, required independent evidence exists, records can be retrieved under document control, and no critical residual risk or unknown acceptance authority remains.

Practice the mechanics with [Verified authentication](verified-authentication.md) and [Independent agent verification](independent-agent-verification.md). See [Showcase submissions](../SHOWCASE.md) before publishing pilot results.
