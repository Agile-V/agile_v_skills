# Governance Conversion

> **Normative.** This contract governs how a recurrent failure becomes a new control, without letting an agent activate a control change for its own currently-active task. It is implemented by `schemas/GOVERNANCE_CONVERSION.schema.json` and consumed by `agile-v-control-matrix` and `agile-v-compliance` (CAPA).

## 1. Rule

An agent MAY propose a governance conversion (a new or changed control). An agent MAY NOT make a safety, security, or compliance control effective for its own current task without an authorized, versioned change. This is the same rule as the frozen verification baseline (`07_EVIDENCE_ADMISSION_CONTRACT.md`, section 4) applied to controls specifically: `Evolve` proposes; only an approved change request creates a new baseline that a *future* cycle is evaluated against.

## 2. Conversion lifecycle

```text
proposed -> approved -> deployed -> validated
                \-> rejected
```

- **proposed**: an agent or human identifies a recurrent failure class and proposes a control.
- **approved**: an authorized owner (not the proposing agent, and not the builder whose work motivated the control) approves activation.
- **deployed**: the control is active for new/future tasks from its `effective_from` baseline onward.
- **validated**: the control has been checked against both the motivating failure reproduction and a representative valid-work corpus (see rule 4).
- **rejected**: the proposal did not meet the bar; the finding remains recorded.

## 3. Required fields

```yaml
conversion:
  id: GOVCONV-XXXX
  source_findings: [VER-..., INC-...]
  failure_class:
  recurrence_count:
  classification:
    local: false
    structural: true
  proposed_change:
    type: control | architecture | test_invariant | tool_policy | skill_contract
    target_ref:
  evidence:
    recurrence_refs: [...]
    root_cause_ref:
  decision:
    status: proposed | approved | rejected | deployed | validated
    authority_ref:
  effective_from:
    lifecycle_baseline:
```

## 4. Rules

1. **Recurrence is a trigger, not a prerequisite.** A single severe incident can justify an immediate control proposal and, where authorized, an immediate stop — it does not need to recur three times first. Conversely, recurrence alone does not prove a structural cause; `classification.structural` must be justified, not assumed from a count.
2. **Held-out validation before activation.** A candidate control must pass (a) a reproduction of the motivating failure and (b) representative *valid* tasks it must not block. Use held-out failure variants, not only the exact observed failure, so the control generalizes rather than pattern-matching one incident.
3. **Owner approval required; proposer != approver.** The agent that proposed the conversion, and the builder whose work motivated it, are not the approving authority. This mirrors the Red Team Protocol and `I3` authority separation (`08_INDEPENDENCE_CLASSES.md`).
4. **Does not retroactively affect the active task.** `effective_from.lifecycle_baseline` marks where the control becomes binding. The task/cycle that motivated the conversion is evaluated under the baseline that was frozen when it started Prove (`07_EVIDENCE_ADMISSION_CONTRACT.md`), not the new control — unless a separate, explicit rebaseline decision applies it retroactively.
5. **Rollback is itself a governance change.** If a deployed control causes excessive false rejection, rolling it back requires the same authorized decision process as deploying it — an agent may not silently stop enforcing a control it finds inconvenient.
6. **Distinguish a mechanically enforced control from a prompt/instruction change.** Adding an instruction to a skill can be a useful compensating measure, but record it as `type: skill_contract` explicitly, not as if it were a `runtime`-enforced control (see the enforcement-class distinction the spec raises for behavioral vs. runtime-enforced controls).

## 5. Relationship to CAPA

`agile-v-compliance`'s CAPA protocol (`.agile-v/CAPA_LOG.md`) is the trigger-and-tracking mechanism; a `GOVERNANCE_CONVERSION` record is what CAPA produces when the corrective/preventive action is a new or changed control rather than a one-off fix. A CAPA may close without a governance conversion (the fix was local); a governance conversion always traces back to at least one CAPA or verification finding.
