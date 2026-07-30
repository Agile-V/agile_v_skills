# Risk Classification

> **Normative.** Risk classification and evidence obligations use `L0`–`L4`. The machine-readable register is [RISK_REGISTER.schema.json](../../schemas/RISK_REGISTER.schema.json); risk, control, claim, and evidence links use [TRACE_GRAPH.schema.json](../../schemas/TRACE_GRAPH.schema.json).

## Levels

| Level | Classification | Minimum decision/evidence |
|---|---|---|
| `L0` | Isolated exploration; no production or regulated path | scope/result record; no production credentials |
| `L1` | Routine, reversible internal change | affected files, targeted verification, residual-risk note |
| `L2` | Production-impacting or security-relevant change | approved baseline, test/acceptance mapping, security check, rollback, reviewer decision |
| `L3` | High-impact, regulated, sensitive-data, or trust-boundary change | L2 evidence, independent verification, trace matrix, explicit human sign-off |
| `L4` | Safety-critical or externally assured release decision | L3 evidence, independent assurance appropriate to the governing profile, residual-risk acceptance authority, release decision |

## Classification rules

1. Classify before synthesis; record level, rationale, controls, residual decision, owner, and affected configuration in `RISK_REGISTER`.
2. Auth, authorization, identity, secrets, payment, privacy-sensitive data, security boundary, irreversible migration, or production release is at least `L2`; raise level when impact or uncertainty warrants it.
3. A Critical residual risk, unresolved control, or unknown acceptance authority blocks the applicable gate/release.
4. `L3`/`L4` require independent findings and a human decision; AI output is never independent assurance.

## Legacy mapping

`R0 -> L0`; `R1 -> L1`; `R2 -> L2`; `R3 -> L3`. There is no legacy equivalent for `L4`; reassess prior `R3` work against `L4` criteria. Use the mapping only for migration; new records must use `L0`–`L4`.
