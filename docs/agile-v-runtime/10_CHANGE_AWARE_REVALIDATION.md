# Change-Aware Revalidation

> **Normative.** This contract generalizes evidence invalidation beyond AI-BOM context changes (`docs/ai-bom-revalidation-triggers.md`) to any dependency a claim relies on: source, policy, environment, model/runtime, or hardware. It is implemented by `schemas/REVALIDATION_ASSESSMENT.schema.json` and consumed by Evidence Bundle v2's `invalidation_dependencies` (`schemas/EVIDENCE_BUNDLE.v2.schema.json`).

## 1. Principle

Evidence depends on more than the artifact it was produced against. A change to a dependency invalidates only the evidence that actually depends on it — but when dependency knowledge is incomplete, treat coverage as insufficient and widen revalidation rather than assume safety.

## 2. Dependency kinds

```yaml
invalidation_dependencies:
  - kind: source
    ref: sha256:...
  - kind: requirement
    ref: REQ-42@r3
  - kind: policy
    ref: POL-2.3
  - kind: environment
    ref: ENV-11
  - kind: tool
    ref: TOOLCHAIN-7
  - kind: model
    ref: MODEL-...
  - kind: hardware
    ref: PCB-REV-C
```

## 3. Invalidation results

| Result | Meaning |
|---|---|
| `UNCHANGED` | The dependency did not change; evidence remains eligible for reuse. |
| `REVALIDATION_REQUIRED` | The dependency changed in a way that affects the claim; evidence must be re-produced before reuse. |
| `STALE` | The dependency changed and no revalidation has occurred yet; do not treat as passing. |
| `UNKNOWN` | Dependency coverage is incomplete or the change's effect cannot be determined. |

**Rule:** `UNKNOWN` is conservative — for `L3`/`L4` claims, `UNKNOWN` widens to full revalidation of the affected claim; it must never be treated as `UNCHANGED`.

### 3.1 Coverage is per-evidence-item, not only assessment-wide

An assessment-level `coverage` (`complete`/`partial`/`unknown`) is a default, not a blanket permission. Each evaluation MAY declare its own `dependency_coverage`, which overrides the assessment-level default for that item specifically. **`UNCHANGED` is reuse-eligible only when the coverage relevant to that specific item is `complete`** — a global `conservative_fallback_applied: true` flag does not, by itself, make an individual `UNCHANGED` item safe; it only satisfies the requirement that *overall* assessment-level coverage be acknowledged as non-complete. Missing dependency knowledge for one item is never proof that specific item is unchanged, even inside an assessment where other items are fully covered. `contracts/semantics.py::revalidation_reuse_eligible(evaluation, assessment_coverage)` and `revalidation_coverage_is_conservative(instance)` implement this rule.

## 4. Assessment procedure

1. Identify actual changed inputs (source, policy, environment, model/runtime, hardware) by trusted identity/digest comparison — not by an agent's self-reported change summary.
2. For each admitted evidence item, evaluate each of its `invalidation_dependencies` against the current state.
3. If any dependency is `REVALIDATION_REQUIRED` or `STALE`, the evidence (and every claim it supports) is no longer eligible for reuse.
4. If dependency coverage is incomplete for a claim (a dependency exists that was not declared, or declared dependencies cannot be resolved), the result is `UNKNOWN` for that claim.
5. Record the assessment (`schemas/REVALIDATION_ASSESSMENT.schema.json`); do not silently drop prior evidence records — supersede them with a new assessment referencing the old evidence ID.
6. Re-run only the affected claims/evidence; unaffected evidence remains valid and does not need to be reproduced.

## 5. Relationship to AI-BOM revalidation triggers

`docs/ai-bom-revalidation-triggers.md` is the `model`/`tool`/`environment`-kind special case of this general mechanism, scoped to AI run context (model, runtime, agent framework, RAG source, skill version). Use the AI-BOM trigger list to populate `model`/`tool` dependency kinds; use this contract's `UNKNOWN -> conservative` rule for any AI-BOM diff that cannot be fully resolved, in addition to the AI-BOM severity table.

## 6. Non-normative example

A firmware change affecting a timing path invalidates timing/HIL evidence (`kind: hardware` or `kind: source` dependency) and any claim that depends on that timing evidence. A separately verified enclosure dimension remains reusable only if its own declared dependencies (geometry, manufacturing configuration) are unchanged — a graph miss or an untracked dependency does not make it eligible; it makes the result `UNKNOWN`, and `UNKNOWN` at `L3`/`L4` triggers revalidation. A simulator result never becomes a physical measurement through dependency reuse alone (see `agile-v-gxp-qualification` and `07_EVIDENCE_ADMISSION_CONTRACT.md`).
