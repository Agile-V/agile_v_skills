# Verified Authentication Change

Use this guide for an authentication, authorization, identity, secret, token, or session change. These changes are at least `L2`; raise the level to `L3` or `L4` when impact, regulated context, sensitive data, trust boundaries, or safety consequences warrant it.

## Example Scope

Suppose a team adds session revocation after a password reset. Record the affected services, identity provider, session store, clients, data classes, deployment configuration, owner, rollback path, and residual-risk authority in `.agile-v/RISK_REGISTER.md`.

## Workflow

1. **Model threats first.** Use `threat-modeler` to identify spoofing, disclosure, privilege escalation, replay, lockout, logging, and privacy risks. Preserve lineage from each applicable threat or stakeholder directive into candidate requirements.
2. **Persist requirements.** Use `requirement-architect` to write atomic `REQ-XXXX` entries in `.agile-v/REQUIREMENTS.md` as `draft_persisted`. Include measurable acceptance and verification criteria.
3. **Obtain independent findings.** `logic-gatekeeper` records findings without rewriting the draft. The architect resolves or rejects each finding with rationale.
4. **Approve and baseline.** At Human Gate 1, an authorized human reviews the revision and findings. Freeze the approved revision; only `baselined` requirements may drive synthesis.
5. **Build and design tests independently.** The artifact records `ART-XXXX -> implements -> REQ-XXXX@revision` with the baseline reference. Test cases record `TC-XXXX -> verifies -> REQ-XXXX@revision` and are derived without reading implementation.
6. **Collect `L2+` evidence.** Include security checks, affected configuration, test-to-acceptance mapping, rollback evidence, reviewer decision, and residual-risk notes. Never place production credentials in agent context or evidence.
7. **Verify independently.** `red-team-verifier` executes tests and adversarial checks, records `VER-XXXX`, and produces `.agile-v/VERIFICATION_SUMMARY.md`. Failures return to synthesis and require re-verification.
8. **Run the Eval Gate and human decision.** `.agile-v/EVAL_RESULTS.md` must be `PASS` or have an authorized `WAIVED` decision. The matching `EvalGate` block ends `VERIFICATION_SUMMARY.md`; unresolved critical or major findings block Gate 2.
9. **Validate intended use only when applicable.** Representative-user and operational evidence belongs in `VALIDATION_REPORT.md`, produced through `validation-agent`. A verification pass is not intended-use validation, and validation cannot close failed verification.
10. **Record AI influence.** If AI materially influenced an artifact, follow [AI run manifest](ai-run-manifest.md) and link the evidence fragment to the evidence bundle.

## Exit Check

| Check | Evidence |
|---|---|
| Risk is at least `L2` and justified | `.agile-v/RISK_REGISTER.md` |
| Synthesis uses a frozen baseline | Requirement revision and baseline locator |
| Security behavior and rollback are tested | `TC-XXXX`, logs, rollback evidence |
| Verification is independent | `VER-XXXX` and `.agile-v/VERIFICATION_SUMMARY.md` |
| Intended-use conclusion is correctly named | `VALIDATION_REPORT.md`, only when performed |
| AI influence is traceable | Manifest and evidence fragment, when applicable |

Next: [Independent agent verification](independent-agent-verification.md) or [Regulated software adoption](regulated-software-adoption.md).
