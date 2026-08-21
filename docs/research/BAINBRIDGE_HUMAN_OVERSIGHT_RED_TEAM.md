# Red-Team Review: Bainbridge-Aware Human Oversight for Agile V

> **Status:** Research and design challenge; non-normative
>
> **Target:** `Agile-V/agile_v_skills`
>
> **Purpose:** Attack the proposed human-oversight design before it becomes a stable Agile V contract.
>
> **Conclusion:** The direction is strong, but the original proposal still risks turning human oversight into another compliance-shaped ritual. The design should move from “add a human step” to a testable assurance case for the complete human-agent system.

## 1. Executive Verdict

The proposal correctly identifies a gap in ordinary “human-in-the-loop” approaches: a person can remain formally responsible while losing the knowledge, attention, practice, and independent evidence needed to exercise that responsibility effectively.

Agile V already has unusually strong foundations for addressing this gap:

- approved and frozen requirements;
- independent requirement findings;
- test design from requirements rather than implementation;
- separation of Build Agent and Red Team Verifier;
- durable Human Gates;
- typed traceability;
- risk-scaled evidence;
- pre-change impact analysis and post-change diff evidence;
- AI-run provenance.

Those controls are necessary, but they do not prove effective human oversight. The proposed `HUMAN_OVERSIGHT` record, human precommit, active challenge, and recovery evidence improve the design, but they remain vulnerable to correlated AI errors, performative review, alert fatigue, unverifiable authorship, and untested assumptions about human competence.

The strengthened design should be built around six claims:

1. **The human formed an independent expectation before exposure to the agent's recommendation.**
2. **Critical acceptance evidence is independent across relevant dimensions, not merely produced by a second agent.**
3. **Differences between expected, predicted, and actual change are visible and resolved.**
4. **The human performed an observable falsification activity before accepting high-risk work.**
5. **A capable person can intervene or recover within the required operational window.**
6. **The oversight process is proportionate enough to avoid routine bypass, rubber-stamping, and review exhaustion.**

A human approval without support for these claims is authority evidence, not oversight-effectiveness evidence.

## 2. Strongest Challenges to the Current Proposal

### 2.1 Skills are normative instructions, not enforcement

`agile_v_skills` defines behavior using Markdown contracts, schemas, templates, and tests. A host agent or runtime can ignore, misunderstand, or incompletely implement those contracts.

Therefore:

- a skill instruction is not a technical control;
- a YAML record is not proof that the described activity occurred;
- schema validity is not semantic truth;
- a second agent saying “PASS” is not independent assurance;
- a Human Gate in prose is not a blocking gate unless the consuming runtime enforces it.

**Required correction:** Describe the approach as a four-layer architecture:

| Layer | Responsibility | Typical Agile V artifact |
|---|---|---|
| Normative skill layer | Defines roles, stop conditions, required behavior, and handoffs | `SKILL.md` |
| Evidence-contract layer | Defines durable, machine-checkable records | schemas and templates |
| Enforcement layer | Blocks prohibited transitions and side effects | consuming runtime, CI, hooks, policy engine |
| Assurance-evaluation layer | Measures whether the controls improve real human-agent performance | experiments, audits, field metrics |

The skills repository owns the first two layers and contract tests for them. It must state explicitly that it does not, by itself, provide the third or fourth.

### 2.2 A human precommit can become ceremonial

A reviewer may write vague statements such as:

```text
Expected outcome: it should work.
Failure concern: bugs.
Recovery: roll back.
```

This technically fills the record while demonstrating almost no independent understanding.

A precommit can also be contaminated by prior AI interaction. Asking the human first inside one workflow does not prove that the human has not already seen an agent-generated plan, impact assessment, or preferred answer.

**Required correction:** The precommit should be a **blind-before-recommendation** record with:

- contamination status: `none-known | prior-ai-exposure | unknown`;
- specific expected observable behavior;
- at least one falsifiable failure hypothesis for applicable levels;
- explicit “unable to assess independently” as a valid answer that triggers escalation;
- no AI-generated suggested wording before the human response is captured;
- a quality check for specificity, not correctness.

The agent may flag vagueness, but it must not turn its own concern into alleged human judgment.

### 2.3 Human authorship metadata is an assertion, not proof

A field such as:

```yaml
authorship:
  type: human
```

can be fabricated by an agent, copied from a template, or added after the fact. A schema cannot verify who formed the judgment.

**Required correction:** Use the term **human-origin attestation**, not verified human authorship. Bind the attestation to existing durable approval evidence and record:

- identity or role reference;
- timestamp;
- gate or approval reference;
- content hash where the runtime supports it;
- whether an agent scaffolded the surrounding record;
- whether the human text was entered before agent recommendations were exposed.

The contract must state that these records improve auditability but cannot cryptographically prove independent cognition.

### 2.4 “Different agent” is not sufficient independence

A builder and verifier can be different sessions while sharing:

- the same model family;
- the same provider;
- the same training biases;
- the same retrieved documentation;
- the same flawed requirement;
- the same tools;
- the same generated tests;
- the same organizational incentives.

Fresh context reduces direct contamination but does not remove correlated failure.

**Required correction:** Define an **Independence Profile** with dimensions:

| Dimension | Example evidence |
|---|---|
| Role | builder and verifier have different responsibilities |
| Context | verifier does not inherit builder conversation or rationale |
| Model | different model family or independently configured model where justified |
| Provider/runtime | different execution path where concentration risk matters |
| Method | static analysis, property testing, simulation, HIL, formal analysis, manual test |
| Data/source | independent oracle or pre-existing baseline-derived test |
| Organization | separate reviewer, assurance role, or authority where required |
| Time | verification performed after a frozen artifact is available |

No universal rule should require all dimensions to differ. The risk profile should select relevant dimensions. For L4 critical claims, at least one evidence source should be non-generative and independently observable.

### 2.5 Requirements can be wrong

Independent test design from baselined requirements prevents implementation-led success bias, but it can still verify a flawed requirement perfectly.

This is not a reason to weaken requirement baselining. It is a reason to preserve the distinction between:

- requirements verification;
- implementation verification;
- intended-use validation;
- operational recovery.

**Required correction:** The Human Oversight Case must not claim that verification proves the right system was built. Intended-use validation remains separate. Human concerns that expose a requirement problem must return through a change request rather than being silently converted into test expectations.

### 2.6 An active challenge can be pseudo-independent

If the builder proposes the challenge, writes the test, predicts the outcome, runs it, and summarizes the result, the human may merely confirm the builder's own framing.

**Required correction:** For L3/L4, the final challenge should originate from one of:

- a human precommit concern;
- the independent Test Designer;
- the Logic Gatekeeper or Threat Modeler;
- a predefined organizational challenge catalog;
- randomized mutation or fault injection;
- an independent domain reviewer.

The Build Agent may provide execution support but must not be the sole source of the challenge hypothesis and oracle.

A valid challenge must be:

- falsifiable;
- linked to a requirement, risk, threat, or recovery claim;
- observable;
- capable of failing;
- supported by evidence;
- performed against the frozen candidate artifact.

### 2.7 More gates can produce less oversight

Requiring the same challenge for every task can create review fatigue, superficial completion, delay, and bypass pressure. Cognitive forcing interventions can reduce overreliance, but they impose effort and may be disliked or unevenly effective across users.

**Required correction:** Oversight must be proportionate and measurable. Track:

- review duration;
- false rejection rate;
- challenge yield;
- repeated low-value warnings;
- number of unresolved surprises;
- reviewer workload;
- gate bypass or waiver frequency.

Introduce a **challenge budget** and risk-based sampling for repetitive lower-consequence work. Do not weaken L3/L4 obligations merely to save time; instead improve automation, decomposition, and evidence quality so human attention is focused on genuine uncertainty.

### 2.8 “Surprises first” can become alert fatigue

Putting unexpected changes first is directionally correct, but an unranked list of harmless generated files, formatting changes, and dependency noise can obscure the important surprise.

**Required correction:** Classify surprises by:

```text
critical | material | explainable | administrative
```

For each surprise report:

- why it was not predicted;
- affected requirement, interface, control, or risk;
- evidence supporting the explanation;
- whether human acknowledgement is required;
- whether a change request or re-baseline is required.

Do not let the same agent that caused an unexpected change finally classify it as harmless without independent review at the levels where acknowledgement is required.

### 2.9 A rollback document is not recovery capability

A recovery plan may be obsolete, inaccessible, incomplete, or executable only by a person who is unavailable. The existence of instructions does not show that takeover will succeed under time pressure.

**Required correction:** Define a recovery-evidence ladder:

| Level | Evidence |
|---|---|
| R0 | written concept only |
| R1 | reviewed procedure with prerequisites and owner |
| R2 | table-top walkthrough |
| R3 | simulation or staging execution |
| R4 | representative HIL, operational exercise, or controlled real-system proof |

The control matrix should select the minimum evidence level. Record recency, responsible role, prerequisites, expected recovery time, actual recovery time, and limitations.

### 2.10 One task-level challenge does not prevent skill decay

Bainbridge's concern is longitudinal. A reviewer may complete a challenge without retaining broad diagnostic and recovery competence over months of automation use.

**Required correction:** Separate task-level oversight from organizational capability maintenance. The new skill should define optional policy hooks for:

- periodic manual diagnostic drills;
- recovery exercises;
- reviewer rotation;
- incident-based learning;
- expiry or recency of recovery evidence;
- team-level competence assumptions.

The repository must avoid employee-surveillance or certification claims. Capability evidence should be proportionate, privacy-preserving, and normally assessed at team or role level.

### 2.11 L0-L4 risk alone does not determine oversight demand

Two L2 tasks can differ radically:

- one has deterministic tests and instant rollback;
- the other changes a poorly understood distributed workflow with weak observability.

Creating a second numeric risk scale would add confusion.

**Required correction:** Add a non-scored **Oversight Demand Profile** alongside L0-L4:

```yaml
oversight_demand:
  automation_allocation: acquisition|analysis|decision|action
  independent_verifiability: high|medium|low|unknown
  reversibility: easy|bounded|difficult|irreversible
  novelty: routine|changed-pattern|novel|unknown
  takeover_difficulty: low|medium|high|unknown
  time_pressure: low|medium|high
```

Use decision rules rather than a misleading arithmetic score. Examples:

- `independent_verifiability: unknown` blocks L3/L4 release until resolved or explicitly accepted by authorized assurance roles;
- `takeover_difficulty: high` requires recovery evidence;
- high decision/action automation plus difficult reversibility requires stronger human reservation and external evidence;
- novel work with correlated AI roles requires additional independence dimensions.

### 2.12 Metrics can be gamed

Counting completed challenges, approvals, or linked evidence rewards activity, not effectiveness.

**Required correction:** Distinguish process conformance from outcome effectiveness.

Primary candidate outcomes:

- false acceptance rate for defective artifacts;
- correct acceptance rate for sound artifacts;
- seeded-defect detection rate;
- time to detect and localize a fault;
- recovery success and recovery time;
- calibration between reviewer confidence and correctness;
- retention of system understanding after repeated agent use.

Secondary outcomes:

- review cost;
- cognitive load;
- false alarm rate;
- waiver rate;
- coverage of critical claims;
- number and severity of unexpected changes.

A control should not be called effective until it improves relevant outcome measures in a suitable evaluation.

### 2.13 Accountability can cause defensive behavior

Accountability can encourage verification, but badly designed accountability can also produce excessive conservatism, documentation inflation, blame avoidance, or systematic rejection of unfamiliar work.

**Required correction:** Measure both unsafe acceptance and unnecessary rejection. Frame accountability around the quality of the decision process, not punishment for disagreeing with automation or for discovering late uncertainty.

### 2.14 The design can create accessibility and equity problems

Cognitive forcing and manual challenge tasks may disproportionately burden people with different cognitive styles, disabilities, language backgrounds, or time constraints.

**Required correction:** Permit equivalent accessible interaction modes while preserving the control objective. Evaluate whether controls create intervention-generated inequalities. Do not equate speed, prose fluency, or a preferred response format with competence.

### 2.15 The approach is vulnerable to adversarial manipulation

An agent, tool result, retrieved document, or peer handoff may attempt to:

- mark human fields complete;
- provide fake approval references;
- hide unexpected changes;
- relabel builder tests as independent;
- downgrade risk or verification difficulty;
- declare recovery evidence passed;
- prompt the reviewer toward a preferred answer.

**Required correction:** Treat all agent-produced content as untrusted evidence. Bind Human Oversight records to existing approval, tool, delegation, trace, and AI-run provenance contracts. Red Team verification should include negative tests for forged authorship, self-approval, scope expansion, and evidence relabeling.

## 3. Revised Core Design

### 3.1 Use a Human Oversight Case, not a checklist

The central artifact should be named and structured as an assurance case:

```text
.agile-v/HUMAN_OVERSIGHT_CASE.yaml
```

It should contain claims, evidence, assumptions, defeaters, ownership, and decisions.

Minimum top-level structure:

```yaml
schema_version: "1.0"
task_id: "TASK-XXXX"
risk_level: "L3"
requirements_baseline_ref: "..."
ai_run_manifest_ref: "..."

oversight_demand:
  automation_allocation: [analysis, decision, action]
  independent_verifiability: medium
  reversibility: bounded
  novelty: changed-pattern
  takeover_difficulty: medium
  time_pressure: low

claims:
  - claim_id: HOC-001
    statement: "The accountable human formed an independent expected outcome before builder recommendations were exposed."
    status: supported
    evidence_refs: []
    assumptions: []
    defeaters: []

independence_profile: {}
surprises: []
challenge_checks: []
recovery_readiness: {}
final_decision: {}
```

Suggested claim set:

| Claim | Meaning |
|---|---|
| HOC-001 | Independent human expectation existed before automation recommendation |
| HOC-002 | Critical acceptance evidence has adequate independence |
| HOC-003 | Expected/predicted/actual differences were surfaced and resolved |
| HOC-004 | Required active challenge was performed and could have failed |
| HOC-005 | Required intervention or recovery capability is supported |
| HOC-006 | Residual uncertainty and decision authority are explicit |

Each claim should permit explicit defeaters. A claim with an unresolved material defeater cannot be marked supported.

### 3.2 Preserve three independent perspectives

The approach should retain distinct channels:

```text
Human expectation
        |
        +---- independent requirement and threat findings
        |
Graph/tool-derived impact prediction
        |
        +---- Build Agent implementation
        |
Independent test and verification evidence
        |
        +---- actual diff and operational observations
```

Disagreement is valuable. The system should not force early consensus.

### 3.3 Treat independence as claim-specific

Do not ask whether “the verifier” is independent in the abstract. Ask whether the evidence supporting each critical claim is sufficiently independent.

Example:

```yaml
independence_profile:
  - claim_ref: HOC-002
    evidence_ref: "TC-0042"
    role_independent: true
    context_independent: true
    model_independent: false
    method_independent: true
    source_independent: true
    organization_independent: false
    rationale: "Test was derived from the frozen requirement and executed by a deterministic harness."
```

### 3.4 Reserve human decisions explicitly

The Human Oversight Case should identify decisions an agent may advise on but not make:

- acceptance of residual risk;
- concession or waiver;
- release authorization;
- classification of material unexpected scope as acceptable;
- approval of irreversible action;
- determination that a human-origin concern has been resolved;
- acceptance of unproven recovery capability.

### 3.5 Allow “unable to assess” without penalty

The safest answer may be:

```text
I cannot independently assess this claim from the available evidence.
```

The skill should treat that as a valid signal that triggers decomposition, additional evidence, a domain expert, or reduced autonomy. It must not pressure the human to manufacture confidence so a gate can proceed.

## 4. Revised Skill Architecture

Create the draft skill:

```text
agile-v-human-oversight/SKILL.md
```

The skill should be concise and cross-cutting. It should not duplicate the lifecycle, test, verification, validation, release, or control-matrix skills.

Required sections:

1. Purpose and boundaries
2. Trigger conditions
3. Oversight Demand Profile
4. Human Oversight Case
5. Blind human precommit
6. Independence Profile
7. Surprise review
8. Active challenge
9. Recovery readiness
10. Capability-maintenance hooks
11. Human-reserved decisions
12. Halt conditions
13. Evidence summary
14. Companion skills and runtime responsibilities

Update companion skills only where their role changes:

| Skill | Required change |
|---|---|
| `agile-v-core` | Add effective-oversight invariant and surprises-first evidence fields |
| `requirement-architect` | Capture blind human expectation before recommendation exposure where required |
| `logic-gatekeeper` | Preserve discrepancy; never rewrite human-origin evidence |
| `test-designer` | Cover approved human concerns where testable without reading implementation |
| `red-team-verifier` | Verify oversight claims, independence, surprise resolution, and challenge quality |
| `agile-v-control-matrix` | Select oversight obligations and recovery evidence level |
| `impact-analysis-agent` | Compare human expectation with graph-derived impact without forcing agreement |
| `diff-evidence-agent` | Surface prediction misses and require appropriate acknowledgement |
| `release-manager` | Block release when required oversight claims or recovery evidence are unresolved |
| `agile-v-aibom` | Provide model/runtime/context provenance needed for independence analysis |

## 5. Required Halt Conditions

The strengthened skill should halt when any applicable condition holds:

- required blind human expectation is absent;
- the human reports inability to assess and no escalation resolves it;
- human-origin content is agent-authored or provenance is materially disputed;
- a critical claim relies only on builder-generated evidence;
- builder and verifier independence is insufficient for the selected control;
- an unexpected material change is unresolved;
- active challenge is required but not falsifiable or not executed;
- recovery evidence is below the control-matrix requirement;
- acceptance authority is unknown;
- review workload or alert volume makes the gate predictably ineffective and no tailoring decision exists;
- intended-use validation is required but is being replaced by implementation verification;
- an agent attempts to approve, waive, or accept residual risk for itself.

## 6. Evidence Summary Format

For applicable L2-L4 work, present Gate 2 information in this order:

```text
Decision requested:
Human-reserved decision owner:

Material surprises:
Unverified critical behavior:
Open defeaters:
Residual risks:
Recovery readiness:

Independent evidence profile:
Challenge results:
Coverage:
Pass results:

Recommendation:
Authority evidence:
```

This focuses attention on uncertainty without burying the reviewer in low-value noise.

## 7. Evaluation Required Before Stable Status

The new skill should remain `metadata.status: draft` until at least:

1. schema and behavioral contract tests pass;
2. seeded scenarios demonstrate that agents cannot validly self-author human evidence;
3. independent reviewers can distinguish valid from invalid oversight cases;
4. a controlled study evaluates defective-change acceptance and review cost;
5. at least one realistic recovery scenario is tested;
6. failure and waiver behavior is documented;
7. accessibility and privacy concerns are reviewed;
8. claims in README and papers are limited to demonstrated evidence.

## 8. Recommended Experimental Conditions

A useful initial experiment should compare:

| Condition | Process |
|---|---|
| C0 | AI builder plus ordinary human pull-request review |
| C1 | Current Agile V: frozen requirements, independent tests, Red Team verification, Human Gate |
| C2 | Bainbridge-aware Agile V: C1 plus blind human expectation, claim-specific independence, surprise review, active challenge, and recovery evidence |

Seed multiple defect classes:

- implementation defect detectable by a standard test;
- omission defect hidden by an incomplete generated test;
- requirement defect that implementation verification cannot resolve;
- correlated builder/verifier error;
- unexpected scope expansion;
- recovery or rollback failure;
- forged human-origin evidence;
- sound change with noisy warnings to measure false rejection.

Primary outcomes:

```text
unsafe acceptance rate
sound-change acceptance rate
fault localization accuracy
intervention success
recovery success and time
confidence calibration
```

Secondary outcomes:

```text
review time
cognitive load
false alarm rate
challenge yield
waiver rate
retained system understanding
```

## 9. Publication Claim Discipline

Until empirical evaluation exists, the project may claim that it:

- defines a Bainbridge-aware oversight contract;
- operationalizes independent expectation, evidence provenance, active challenge, and recovery readiness;
- makes human-oversight assumptions explicit and testable;
- provides runtime-neutral skill and schema contracts;
- proposes an evaluation protocol.

It must not claim that it:

- eliminates automation bias;
- proves human competence;
- guarantees safe AI-generated software;
- establishes regulatory compliance;
- makes a second AI agent independent assurance;
- has been empirically shown to prevent the out-of-the-loop problem;
- certifies effective human oversight.

## 10. Final Design Principle

The strongest form of the Agile V approach is not:

```text
AI works; human approves.
```

It is:

```text
Humans establish intent and reserved decisions.
Independent processes create competing expectations.
Agents synthesize within a frozen contract.
Evidence exposes both success and surprise.
Humans perform risk-proportionate falsification.
Recovery capability is demonstrated where consequences require it.
The effectiveness of the joint system is measured, not assumed.
```

The core invariant should be:

> **Do not merely keep a human in the workflow. Preserve and test the human's capacity to understand, challenge, intervene, and recover.**
