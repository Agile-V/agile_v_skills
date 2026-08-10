# Independent Agent Verification

Independent verification asks whether specified outputs were built correctly against the approved baseline. It does not establish intended-use acceptance.

## Set Up Independence

1. Freeze the approved requirements baseline before synthesis.
2. Give the Build Agent only the baselined requirement IDs and paths needed for synthesis.
3. Have `test-designer` derive `TC-XXXX` from the same baseline without reading implementation. Use a fresh context, separate agent/runtime, or design tests first when one context is unavoidable.
4. Assign `red-team-verifier` to execute tests and challenge artifacts. The builder must not verify its own work, and AI output is never independent assurance for `L3` or `L4`.

Independence must be real enough for the applicable risk and governing profile. Record agent or reviewer identity, context boundary, inputs, tools, timestamps, and conflicts of interest rather than merely labeling a run "independent."

## Execute and Record

For each result, record:

```text
VER-XXXX | TC-XXXX | REQ-XXXX | PASS/FAIL/FLAG | FT-CODE | description
```

Attach the expected and actual result, command or procedure, artifact path, evidence locator, requirement revision/baseline, reviewer decision, timestamp, and residual assumptions. The verifier reports observed differences and expected behavior from the requirement; it does not prescribe implementation fixes.

On a failure, return the finding to the builder, re-run failed or flagged tests after the change, and run regression tests for affected artifacts. Requirement changes require a change request, renewed review, Gate 1 approval, and a new baseline.

## Gate 2 Handoff

Produce `.agile-v/VERIFICATION_SUMMARY.md` with scope, result counts, findings, requirement coverage, audit trail, and the final `EvalGate` block linked to `.agile-v/EVAL_RESULTS.md`. `FAIL`, an unauthorized waiver, or unresolved critical/major findings blocks Gate 2.

Do not rename this output `VALIDATION_REPORT.md`. That report is reserved for representative intended-use assessment by `validation-agent`; validation does not repair a failed verification result.

## Risk Tailoring

| Level | Practical verification posture |
|---|---|
| `L0` | Scope/result record; keep exploration away from production credentials |
| `L1` | Targeted verification and a residual-risk note |
| `L2` | Approved baseline, mapped tests, security check, rollback, reviewer decision |
| `L3` | `L2` evidence plus independent verification, trace matrix, human sign-off |
| `L4` | `L3` evidence plus profile-appropriate independent assurance and authorized release/residual-risk decisions |

For materially AI-assisted work, add the checks in [AI run manifest](ai-run-manifest.md). For a concrete security example, see [Verified authentication](verified-authentication.md).
