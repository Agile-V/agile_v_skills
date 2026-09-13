# Evidence Admission Contract

> **Normative.** This contract defines claim, evidence, and admissibility vocabulary used by every Agile V gate decision, and the frozen-baseline rule that governs `Evolve` relative to `Verify`. It applies wherever `docs/agile-v-runtime/03_CANONICAL_LIFECYCLE_CONTRACT.md`, `04_RISK_CLASSIFICATION.md`, or a gate skill (Red Team Verifier, Compliance Auditor, GxP Qualification) requires evidence to authorize a transition.

## 1. Why this contract exists

Agile V already requires typed traceability, human-governed gates, and independent verification. Those contracts describe *what* must be produced. This contract describes *when evidence is allowed to count* toward a gate decision. A test log, an approval string, or a signed report is not automatically sufficient; it must be admissible for the specific claim, state, and policy in force.

## 2. Terms

| Term | Definition |
|---|---|
| **Claim** | An assertion relevant to a lifecycle decision, e.g. "`REQ-0042@r3` is satisfied by `ART-0011@sha256:...`", "`TC-0091` passed against build digest `...`". An agent stating a claim does not make it true. |
| **Evidence candidate** | An artifact that may support a claim: test result, static-analysis result, HIL trace, signed approval, CI attestation, verification record, log, simulator output, qualification protocol result. |
| **Evidence presence** | The evidence exists and is retrievable. |
| **Structural completeness** | The evidence satisfies the schema required for its type. |
| **Evidential sufficiency** | The evidence reconstructs all properties the claim/gate requires (not merely "a test ran"). |
| **Evidence admissibility** | Evidence is admissible only when it is sufficiently relevant, attributable, authorized, integrity-protected, bound to the correct artifact state, bound to the applicable policy/control version, bound to the relevant execution environment where material, fresh/non-stale, and independent where the gate requires independence (see `08_INDEPENDENCE_CLASSES.md`). |
| **Stale** | Evidence is stale when a dependency relevant to its claim changed after the evidence was produced. |
| **Gate Receipt** | A record of why a lifecycle transition was permitted or denied; see `schemas/GATE_RECEIPT.schema.json`. |

### 2.1 Implication hierarchy

```text
admissible -> sufficient -> structurally complete -> present
```

The reverse implications do not hold. Presence of a file never implies sufficiency; sufficiency never implies admissibility. `unknown` completeness or sufficiency must never be treated as a passing result for a mandatory claim.

### 2.2 Historical validity vs. current eligibility

Keep these two questions distinct:

1. **Historically valid** — was the evidence/decision justified under the state and policy in effect when it was produced?
2. **Currently eligible** — may it still be reused for a new/current lifecycle decision?

A later policy or requirement change does not rewrite history (do not edit or delete the original record), but it may make previously valid evidence ineligible for reuse. Record supersession as a new event; never overwrite the original.

## 3. Frozen verification baseline

For an active task/cycle, define:

```text
verification_baseline =
  requirements baseline (baselined REQ revisions in scope)
  + acceptance criteria
  + risk classification (L0-L4)
  + applicable policies (POLICY.yaml, CONTROL_MATRIX.yaml when present)
  + required evidence profile for the claim types involved
```

**Rule:** once synthesis (Orchestrate/Prove) begins, `verification_baseline` is frozen for the current decision. `Verify` evaluates the artifact against the frozen baseline that was in force when Prove started, not against a baseline an agent adjusted afterward.

## 4. Evolve is proposal-only relative to the active baseline

`Evolve` (SCOPE-V) may, during the active cycle:

- append observations and metrics;
- create CAPA candidates (see `agile-v-compliance`);
- create governance-conversion candidates (see `agile-v-control-matrix`);
- propose control, policy, or skill/process changes.

`Evolve` may **not**, during the active cycle:

- weaken, relax, or replace the acceptance criteria, risk classification, or policy that `Verify` is about to check;
- retroactively mark previously failed evidence as sufficient;
- alter the frozen `verification_baseline` for the task currently awaiting `Verify`.

A proposed change becomes active only through: `proposal -> review -> approved change request -> new baseline/version -> future cycle or explicit rebaseline`. This is the same rule stated operationally in `agile-v-core` (SCOPE-V table) and `agile-v-lifecycle` (Change Requests); this document is its normative source.

**Anti-pattern this rule blocks:**

```text
implementation -> prove -> adjust rules/context -> verify against adjusted rules
```

If `Verify` needs criteria to change, that is a new change request and a new baseline revision — not a same-cycle edit.

## 5. Evidence sufficiency by risk level

Required evidence properties scale with the resolved risk level (`docs/agile-v-runtime/04_RISK_CLASSIFICATION.md`). Do not accept "there is a test log" as proof of "requirement satisfied" without checking which properties that log actually establishes for the applicable level. `schemas/EVIDENCE_BUNDLE.v2.schema.json` is the structured form of this rule: each claim declares `required_evidence_properties`; each evidence item declares which claim(s) it `supports`, the properties it actually `establishes_properties`, its `producer`, `evidence_source` (for `L2`+), `state_binding`, `integrity` digest, and — for `L2`+ — a `policy_binding` whose digest matches the bundle's own frozen policy. Schema validity is necessary but not sufficient: (1) matching `state_binding` (subject type, ref, *and* digest) against the actual current baseline, (2) requiring `required_evidence_properties` to be a subset of the union of *trusted* `establishes_properties` from *passing* supporting evidence, and (3) blocking a claim outright when any contradictory (`fail`/`error`) evidence supports it — regardless of other passing evidence — are all semantic admissibility checks (see `contracts/semantics.py`), not structural ones. The last point matters most: a single passing item must never mask a failing item for the same claim (the any-pass anti-pattern).

### 5.1 An evidence source cannot self-authorize what it establishes

`establishes_properties` is a producer *assertion*, not a fact. A unit-test adapter declaring `establishes_properties: [human_authority]` is structurally valid but must never be trusted: nothing about a unit test run can establish human authority. Two additional profiles constrain this:

- **`schemas/EVIDENCE_PROPERTY_PROFILE.schema.json`** answers "for this claim type / risk level, what properties are mandatory?" — removing arbitrary producer choice from `required_evidence_properties`.
- **`schemas/EVIDENCE_SOURCE_PROFILE.schema.json`** answers "what may this evidence source (adapter) actually establish?" via `may_establish`/`may_not_establish`. Each `L2`+ evidence item references one via `evidence_source.adapter_ref`.

Admission caps a claimed `establishes_properties` set by the resolved adapter's `may_establish` capability (`contracts/semantics.py::evidence_bundle_admission_is_consistent(instance, resolve_adapter=...)`): only the intersection is trusted. Without a resolver, the bare self-declared set is trusted (legacy/advisory mode) — the trusted path is always the aggregate evaluator in section 7, which requires a resolver.

## 6. Non-normative summary for agents

- A claim is not a fact because an agent wrote it down.
- Presence is not completeness; completeness is not sufficiency; sufficiency is not admissibility.
- `unknown` never authorizes a gate.
- An evidence source cannot self-authorize what it establishes; only a trusted adapter capability profile can.
- Once Prove starts, the criteria Verify will check are frozen; Evolve may only propose changes for a future cycle.
- Reusing old evidence for a new decision is a separate, explicit judgment from whether that evidence was originally valid.

## 7. Canonical aggregate evaluators

Every semantic predicate in `contracts/semantics.py` is a reusable building block, not individually sufficient to answer "may this evidence/gate actually advance?". Calling only one or two predicates and treating the result as "admissible" reintroduces exactly the gaps those predicates exist to close. Use the aggregate entrypoints instead:

| Function | Answers |
|---|---|
| `evaluate_evidence_bundle(instance, resolve_adapter=...)` | May this Evidence Bundle v2's admission be trusted? |
| `evaluate_gate_receipt(instance, resolve_exception=..., resolve_approval=..., now=..., risk_level=...)` | Is this Gate Receipt's decision actually justified? |
| `authorize_gate_transition(gate_receipt, evidence_bundle=None, ...)` | May this transition actually proceed? |

Each returns `{"status": "admitted"|"rejected", "findings": [{"code": ...}, ...]}` — structured, explainable reason codes, not a bare boolean. A runtime implementing this contract should reproduce these aggregate functions as its admission decision surface.
