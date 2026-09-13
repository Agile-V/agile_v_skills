# Independence Classes (I0–I4)

> **Normative.** This taxonomy qualifies every use of "independent" across Agile V skills and compliance docs. "Independent verification," "independent findings," and "independent assurance" are related but distinct claims; they must not be conflated. Use the minimum class required by the applicable risk level or governing profile; do not claim a higher class than the actual separation achieved.

## 1. Classes

| Class | Name | Definition |
|---|---|---|
| `I0` | Self-check | Same agent/context reviews its own output. Not independence; a sanity check only. |
| `I1` | Context-separated | Same model/runtime permitted, but a fresh context with no builder memory, chat history, or reasoning carried over. |
| `I2` | Role-separated | A separate agent role (e.g. Test Designer, Red Team Verifier) with protected requirement/test inputs; the verifying role does not read builder implementation to design its checks. |
| `I3` | Authority-separated | A different authenticated actor/principal performs or approves the check and cannot modify the evaluated artifact, its policy, or its acceptance criteria. |
| `I4` | Organizationally independent assurance | An independent qualified human, team, or entity, as required by the governing regulatory/quality profile (e.g. GxP, safety case, external audit). |

Classes are cumulative in practice (I3 implies role separation; I4 implies authority separation) but are declared explicitly per claim rather than assumed from a single "is this independent?" judgment.

## 2. Rules

1. **Declare the required minimum, not the achieved maximum.** A verification requirement states `independence_minimum: I2` (or similar); the actual verification records which class was achieved for that specific claim.
2. **A fresh LLM context is I1 at most.** It reduces confirmation bias relative to I0 but does **not** constitute I3 authority separation, I4 organizational independence, or human approval. Do not describe I1 as "independent assurance."
3. **Role separation (I2) is not automatically authority separation (I3).** Red Team Verifier and Test Designer achieve I2 by design (Red Team Protocol, Directive #4/#7 in `agile-v-core`); this does not by itself satisfy an I3/I4 requirement for regulated or safety-critical claims.
4. **"Independent verification" (Red Team Protocol) and "independent assurance" (regulatory/organizational) are different claims.** `docs/agile-v-runtime/04_RISK_CLASSIFICATION.md` requires `I2` role-separated verification from `L2` upward (matching its own table: `L0`/`L1` require only `I1`) and reserves `I3`/`I4` for `L3`/`L4` as stated there; AI-only separation (same or different agent, without role separation and protected inputs) never satisfies an `I3`/`I4` requirement.
5. **Claim-specific, not global.** Independence is evaluated per claim/critical-evidence item, not once for the whole task. `agile-v-human-oversight`'s Independence Profile (`role_independent`, `context_independent`, `model_independent`, `method_independent`, `source_independent`, `organization_independent`) is the claim-specific mechanism that determines which I-class a specific piece of evidence actually achieved; this taxonomy is the normative vocabulary for stating the required minimum and the achieved result.

## 3. Minimum independence by risk level (summary)

| Risk level | Minimum independence for verification | Additional requirement |
|---|---|---|
| `L0`/`L1` | `I1` acceptable (fresh-context self-review permitted) | None beyond role hygiene |
| `L2` | `I2` required | Role-separated Test Designer + Red Team Verifier; protected requirement inputs |
| `L3` | `I2` required for verification; `I3` required for the human sign-off/approval | Trace matrix; explicit human sign-off with authority the builder cannot hold |
| `L4` | `I3` required; `I4` required where the governing profile (GxP, safety case, external audit) mandates organizational assurance | Residual-risk acceptance authority separate from build/verify roles |

This mirrors `docs/agile-v-runtime/04_RISK_CLASSIFICATION.md`; that document remains the normative source for risk-level requirements. This table restates them using the I-class vocabulary.

## 4. Non-normative examples

- Red Team Verifier re-checking its own verification output in the same session: `I0`. Not valid independent verification.
- Red Team Verifier invoked in a fresh context after Build Agent finishes, with its own read of requirements only: `I2`.
- A human reviewer with release authority who did not write the code or the tests, approving Gate 2: `I3` (and `I4` if that reviewer's authority derives from an organizationally separate quality function, e.g. a GxP Quality Unit).
- Two different LLM calls, same model, same conversation thread, one asked to "check the other's work": still `I0`/`I1` — this is not organizational independence and must not be reported as such.
