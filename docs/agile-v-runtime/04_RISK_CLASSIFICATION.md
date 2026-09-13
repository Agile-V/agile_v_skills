# Risk Classification

> **Normative.** Risk classification and evidence obligations use `L0`–`L4`. The machine-readable register is [RISK_REGISTER.schema.json](../../schemas/RISK_REGISTER.schema.json); risk, control, claim, and evidence links use [TRACE_GRAPH.schema.json](../../schemas/TRACE_GRAPH.schema.json). "Independent verification" and "independent assurance" below are qualified by the independence classes (`I0`–`I4`) defined in [08_INDEPENDENCE_CLASSES.md](08_INDEPENDENCE_CLASSES.md); that document is the normative source for what each class requires.

## Levels

| Level | Classification | Minimum decision/evidence | Minimum independence class |
|---|---|---|---|
| `L0` | Isolated exploration; no production or regulated path | scope/result record; no production credentials | `I0` |
| `L1` | Routine, reversible internal change | affected files, targeted verification, residual-risk note | `I1` |
| `L2` | Production-impacting or security-relevant change | approved baseline, test/acceptance mapping, security check, rollback, reviewer decision | `I2` |
| `L3` | High-impact, regulated, sensitive-data, or trust-boundary change | L2 evidence, independent verification, trace matrix, explicit human sign-off | `I2` verification; `I3` human sign-off |
| `L4` | Safety-critical or externally assured release decision | L3 evidence, independent assurance appropriate to the governing profile, residual-risk acceptance authority, release decision | `I3`; `I4` where the governing profile requires organizational assurance |

## Classification rules

1. Classify before synthesis; record level, rationale, controls, residual decision, owner, and affected configuration in `RISK_REGISTER`.
2. Auth, authorization, identity, secrets, payment, privacy-sensitive data, security boundary, irreversible migration, or production release is at least `L2`; raise level when impact or uncertainty warrants it.
3. A Critical residual risk, unresolved control, or unknown acceptance authority blocks the applicable gate/release.
4. `L3`/`L4` require independent findings and a human decision; AI output is never independent assurance. A fresh context or a second AI agent is at most `I1` and never satisfies an `I3`/`I4` requirement on its own (see `08_INDEPENDENCE_CLASSES.md`).

## Legacy mapping

`R0 -> L0`; `R1 -> L1`; `R2 -> L2`; `R3 -> L3`. There is no legacy equivalent for `L4`; reassess prior `R3` work against `L4` criteria. Use the mapping only for migration; new records must use `L0`–`L4`.
