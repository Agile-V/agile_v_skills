# Beyond Human-in-the-Loop: Bainbridge-Aware Assurance Contracts for AI-Assisted Software Engineering

**IEEE-style manuscript draft — Markdown working copy**  
**Paper status:** Conceptual framework and evaluation protocol; no empirical effectiveness claims  
**Authors:** Anonymous for review / to be completed before submission  
**Target artifact:** `Agile-V/agile_v_skills`  
**Companion design challenge:** `docs/research/BAINBRIDGE_HUMAN_OVERSIGHT_RED_TEAM.md`

---

## Abstract

AI coding agents increasingly participate in repository analysis, design, implementation, test generation, verification, and release preparation. This broad function allocation creates a familiar human-factors problem in a new engineering setting: the more routine work automation performs, the more difficult the remaining human supervisory task can become. A nominal “human-in-the-loop” control may therefore preserve formal authority while degrading the human's situation awareness, independent judgment, fault-detection ability, and recovery readiness. This paper translates Bainbridge's ironies of automation into a runtime-neutral assurance contract for AI-assisted software and cyber-physical engineering. The proposal extends the Agile V Agent Skills architecture with six linked controls: an Oversight Demand Profile, a blind human expectation record, a claim-based Human Oversight Case, claim-specific evidence-independence profiles, a predicted-versus-actual surprise gate, and a recovery-evidence ladder. The design distinguishes authority evidence from oversight-effectiveness evidence, prohibits agents from fabricating human-origin judgment, and treats agreement between generative agents as insufficient independent assurance for critical claims. Formal gate predicates specify the minimum conditions for acceptance without reducing oversight to a misleading composite score. We map the proposal to existing Agile V skills, schemas, templates, Human Gates, risk levels, and traceability records, while separating normative skill instructions from consuming-runtime enforcement. Finally, we present a controlled evaluation protocol comparing ordinary AI-assisted review, current Agile V controls, and the proposed Bainbridge-aware controls using seeded implementation, requirement, correlation, scope, provenance, and recovery failures. The central claim is deliberately bounded: effective human oversight should be represented as a testable property of the joint human-agent system rather than inferred from the presence of a human approval step.

**Index Terms—** AI-assisted software engineering, agentic coding, automation bias, human oversight, human–AI teaming, software assurance, verification, recovery, Agile V, agent skills.

---

# I. Introduction

Generative AI systems are moving from code completion toward agentic engineering workflows that inspect repositories, interpret requirements, propose architectures, modify multiple artifacts, generate tests, run tools, summarize evidence, and prepare release decisions. This shift is often described as an increase in model capability. From a human-factors perspective, however, it is also a redistribution of work across information acquisition, analysis, decision selection, and action implementation—the four broad automation functions described by Parasuraman, Sheridan, and Wickens [4].

Redistributing work changes the human role. When an agent performs most normal engineering activity, a human reviewer may no longer develop or continuously update a sufficiently rich mental model of the system. The reviewer can still be asked to approve the result, but approval may rest primarily on the agent's own summary, tests, confidence, and explanation. The nominal control is then circular:

```text
agent produces artifact
    -> agent produces acceptance evidence
    -> agent explains why the evidence is sufficient
    -> human approves the agent's framing
```

Bainbridge's 1983 analysis of the “ironies of automation” anticipated the structural form of this problem [1]. Automation can remove routine opportunities through which operators maintain skill and system knowledge while leaving them responsible for rare, difficult, and time-critical failures. Later research described out-of-the-loop performance degradation [2], automation misuse and disuse [3], automation surprises [6], imperfectly calibrated trust [5], and automation bias under flawed decision support [8], [9]. These findings do not prove that AI coding agents will reproduce every effect observed in aviation, process control, or laboratory decision tasks. They do establish a strong reason not to equate formal human involvement with effective supervision.

Software engineering adds several complications. AI-generated code can be plausible while containing security defects [11], [12]. Test generation can encode the same assumptions as implementation. Different agents may share models, providers, retrieval sources, tools, requirements, and incentives, creating correlated failures. A rollback document can exist without any person being able to execute it under operational pressure. A machine-valid evidence bundle can contain semantically false provenance claims. Finally, mandatory review rituals can overload humans, increasing superficial compliance rather than meaningful challenge.

The Agile V Agent Skills library provides a useful foundation for addressing these problems. Its current architecture separates requirements, independent findings, a frozen baseline, implementation, baseline-derived test design, independent verification, intended-use validation, durable Human Gates, risk classification, typed traceability, control-matrix governance, and AI-run provenance [20]. These controls already oppose self-verification and chat-only authority. Yet they do not, by themselves, demonstrate that the human at a gate retained independent understanding, attended to material surprises, performed a falsifiable challenge, or remained capable of intervention and recovery.

This paper proposes a **Bainbridge-Aware Assurance Contract (BAAC)** for Agile V. BAAC is not a new lifecycle and not a numeric “human oversight score.” It is a set of cross-cutting claims and evidence obligations integrated into the existing Agile V lifecycle. Its contributions are:

1. **A software-engineering interpretation of Bainbridge's automation problem.** We identify four coupled failure classes: cognitive displacement, circular self-certification, correlated assurance, and recovery cliffs.
2. **An Oversight Demand Profile.** The profile records automation allocation, independent verifiability, reversibility, novelty, takeover difficulty, and time pressure without collapsing them into a false-precision score.
3. **A Human Oversight Case.** The case represents oversight as explicit claims, evidence, assumptions, defeaters, human-reserved decisions, and authority references.
4. **Claim-specific independence and surprise controls.** Evidence independence is evaluated across role, context, model, method, source, organization, and time. Predicted and actual impact are compared, with material surprises shown before reassuring aggregate results.
5. **Active falsification and recovery evidence.** Risk-scaled challenge and recovery obligations replace passive review with observable activities that could fail.
6. **A repository implementation map and empirical evaluation protocol.** We specify how the contract fits the Markdown skills, schemas, templates, tests, and consuming-runtime boundaries of `agile_v_skills`, and how its effectiveness could be tested.

The proposal is intentionally conservative in its claims. It does not claim to eliminate automation bias, certify human competence, guarantee safe AI-generated code, or establish regulatory compliance. It makes the assumptions behind human oversight explicit, traceable, challengeable, and empirically testable.

# II. Background and Related Work

## A. Ironies of Automation and Out-of-the-Loop Performance

Bainbridge argued that automation design often leaves humans with the tasks that are difficult to automate while depriving them of practice in the routine control activities needed to understand and recover the system [1]. The human may be expected to monitor a highly capable automated system continuously, detect rare failures, diagnose unfamiliar states, and take over at precisely the point where automation has reduced recent involvement.

Endsley and Kiris experimentally examined the out-of-the-loop performance problem and linked high automation to reduced situation awareness and impaired manual takeover [2]. Sarter and Woods documented automation surprises arising from mismatches between operator expectations and automation behavior [6]. Klein et al. later framed powerful automation as a joint-activity problem: effective machine teammates must support observability, predictability, directability, and common ground rather than merely perform isolated functions well [7]. These concepts transfer naturally to agentic software work. Repository changes are not only outputs; they are state transitions in a joint cognitive system involving humans, models, tools, documentation, tests, and operational environments.

## B. Trust, Bias, Accountability, and Cognitive Forcing

Parasuraman and Riley distinguished appropriate use from misuse, disuse, and abuse of automation [3]. Lee and See argued that trust should be calibrated to the automation's capabilities and the context rather than maximized [5]. Automation bias can produce errors of omission, where a person fails to act because automation did not flag a problem, and commission, where a person follows incorrect automated advice despite contradictory evidence [8]. Parasuraman and Manzey reviewed complacency and automation bias as related attentional phenomena that can affect novices and experts [9].

Accountability can increase verification behavior and reduce some automation-bias effects, but it does not provide a universal solution [8]. Poorly designed accountability can also encourage defensive decision making, excessive conservatism, or documentation inflation. Cognitive forcing functions—such as requiring a person to reason before seeing AI advice—have reduced overreliance in controlled AI-assisted decision tasks, but they impose interaction costs, are not uniformly preferred, and may benefit users differently [10]. These tradeoffs motivate a proportionate design: the objective is appropriate reliance and discriminative review, not maximal friction or blanket distrust.

## C. Human–AI Complementarity

A 2024 meta-analysis of 106 experiments found that human–AI combinations did not, on average, outperform the better of the human or AI alone, although outcomes varied by task and creation tasks showed more favorable patterns than decision tasks [13]. This result cautions against assuming that adding a human and an AI automatically creates synergy. Complementarity is an engineered property that depends on task allocation, information structure, coordination, error correlation, and decision authority.

For AI-assisted software engineering, “human plus agent” should therefore be evaluated as a system configuration. A workflow that gives a human only an AI-written summary may produce less effective oversight than either careful human engineering or well-validated automation. Conversely, a workflow that exposes independent requirements, deterministic evidence, material surprises, and recovery options may create useful complementarity.

## D. AI-Assisted Code and Security

Empirical studies of AI code generation have found context-dependent security risks. Pearce et al. reported vulnerable outputs across a substantial fraction of evaluated GitHub Copilot scenarios [11]. Perry et al. found that, in their study, participants with AI assistance produced less secure code in several tasks and were more likely to believe their code was secure [12]. These studies do not characterize every model, developer, task, or current system. They illustrate two relevant hazards: generated code can fail silently, and perceived correctness can diverge from measured correctness.

The same model can influence requirements interpretation, implementation, tests, review, and explanation. This creates a special form of common-mode failure. A second generative agent may provide useful challenge, but agreement between agents is not equivalent to an independent measurement, pre-existing oracle, formal property, hardware observation, or accountable human judgment.

## E. Governance Context

NIST's AI Risk Management Framework emphasizes governance, defined roles, human–AI configurations, monitoring, and risk management across the lifecycle [14]. The EU AI Act requires high-risk AI systems to support effective human oversight proportionate to risk, autonomy, and context [15]. IEEE 7000 and ISO/IEC/IEEE 24748-7000 provide lifecycle-oriented approaches for addressing values and ethical concerns in system design [16]. BAAC is compatible with the direction of these sources but does not claim compliance with them. Legal and standards obligations require context-specific interpretation, controlled editions, and qualified review.

# III. Problem Formulation

## A. Authority Is Not Capability

A human gate can provide evidence that a person had formal authority and made a recorded decision. It does not automatically demonstrate that the person:

- formed an independent expectation;
- understood the relevant system state;
- could distinguish correct from incorrect agent output;
- saw material deviations from the expected scope;
- performed a meaningful challenge;
- could intervene or recover after failure.

We therefore separate two predicates:

- `Authority(t)`: an authorized person made a durable, properly scoped decision for task `t`;
- `OversightCapability(t)`: the joint process provides adequate evidence that the human could understand, challenge, intervene, and recover as required by the task context.

A valid high-risk acceptance requires both. Authority without capability risks rubber-stamping; capability without authority cannot authorize release or residual-risk acceptance.

## B. Four Failure Classes

### 1) Cognitive displacement

As agents absorb repository exploration, design, coding, test construction, and diagnosis, humans may lose the task exposure that supports mental models and skill retention. The remaining review task becomes more abstract and less informative.

### 2) Circular self-certification

The builder can generate the artifact, tests, evidence selection, and summary. Even when each item is well formed, the evidence can reproduce the builder's assumptions and omissions.

### 3) Correlated assurance

A nominally separate verifier can share the same requirement defect, model family, provider, retrieval corpus, toolchain, or organizational objective. Session separation reduces direct context contamination but not all common-mode failure.

### 4) Recovery cliffs

Automation may work well under normal conditions and then fail at a point requiring expert intervention. A documented rollback path does not prove that a capable person, required credential, prior artifact, physical interface, or operational window will be available.

## C. Design Requirements

A Bainbridge-aware engineering control should satisfy the following requirements:

- **R1—Independent expectation:** capture a human expectation before exposure to the builder's recommendation when required.
- **R2—Evidence diversity:** identify and enforce claim-specific independence requirements.
- **R3—Surprise visibility:** compare human expectation, technical prediction, and actual change.
- **R4—Falsifiability:** require a challenge that could expose an incorrect artifact.
- **R5—Recoverability:** provide risk-proportionate evidence that intervention or recovery is feasible.
- **R6—Proportionality:** focus human attention where uncertainty and consequence justify it.
- **R7—Non-fabrication:** prohibit agents from creating human-origin judgment or approval evidence.
- **R8—Runtime neutrality:** express normative behavior and evidence contracts independently of a specific agent platform.
- **R9—Claim discipline:** distinguish process conformance, evidence support, effectiveness, compliance, and certification.
- **R10—Evaluability:** define measurable outcomes that can disconfirm the proposed benefits.

# IV. Existing Agile V Foundation

Agile V separates the engineering lifecycle into durable, role-specific artifacts. Requirements are persisted, independently challenged, revised, approved at Human Gate 1, and captured in a frozen baseline. Build agents synthesize only from baselined requirements. Test design is derived from the baseline without reading implementation. A Red Team Verifier independently executes tests and challenges the produced artifacts. Intended-use validation remains a separate activity. Human Gate 2 authorizes acceptance or release based on evidence, residual risk, and accountable authority.

The current skills architecture already contains controls directly relevant to Bainbridge's concerns:

| Existing Agile V control | Human-factors contribution |
|---|---|
| Frozen requirement baseline | Prevents long chat history from silently redefining intent |
| Logic Gatekeeper | Preserves independent requirement findings |
| Independent Test Designer | Reduces implementation-led confirmation bias |
| Red Team Protocol | Prevents the builder from formally verifying its own work |
| Fresh context guidance | Reduces direct propagation of builder rationale |
| Impact Analysis Agent | Predicts affected components before implementation |
| Diff Evidence Agent | Compares predicted and actual change |
| Typed traceability | Exposes lineage among requirements, artifacts, tests, and evidence |
| Human Gates | Records authority and stop/resume decisions |
| Control Matrix | Selects tools, models, rights, tests, gates, rollback, and owners |
| AI Run Manifest | Records model, runtime, tool, skill, and context provenance |

The remaining gap is not the absence of humans. It is the lack of a normative assurance argument showing why the human gate should be considered effective for the particular allocation of automation. BAAC fills that gap without replacing the canonical lifecycle.

# V. Bainbridge-Aware Assurance Contract

## A. Four-Layer Architecture

BAAC separates four layers that are often conflated:

| Layer | Function | Ownership in `agile_v_skills` |
|---|---|---|
| Normative skill layer | Defines roles, invariants, stop conditions, and handoffs | Yes |
| Evidence-contract layer | Defines machine-checkable records and provenance fields | Yes |
| Enforcement layer | Blocks invalid transitions, writes, tools, or releases | Contract only; implemented by consuming runtime |
| Assurance-evaluation layer | Measures whether controls improve outcomes | Research protocol and external evaluation |

This separation prevents a schema-valid file from being misrepresented as proof that a cognitive activity occurred. The skills repository can require and validate attestations; it cannot observe a person's private reasoning or guarantee runtime enforcement.

## B. Oversight Demand Profile

The existing Agile V level `L0`–`L4` remains the primary delivery-risk classification. BAAC adds a descriptive **Oversight Demand Profile (ODP)** rather than a second score:

```yaml
oversight_demand:
  automation_allocation:
    - information_acquisition
    - analysis
    - decision_selection
    - action_implementation
  independent_verifiability: high | medium | low | unknown
  reversibility: easy | bounded | difficult | irreversible
  novelty: routine | changed_pattern | novel | unknown
  takeover_difficulty: low | medium | high | unknown
  time_pressure: low | medium | high
```

Automation allocation adapts the four-stage model of Parasuraman et al. [4] to software work:

| Function | Agentic software example |
|---|---|
| Information acquisition | repository search, dependency discovery, retrieval |
| Information analysis | impact analysis, diagnosis, risk assessment, planning |
| Decision selection | architecture choice, change strategy, acceptance recommendation |
| Action implementation | code modification, test execution, release action |

The ODP is intentionally not summed. A single high-consequence property can dominate the control decision. Suggested monotonic rules include:

- `independent_verifiability: unknown` blocks unresolved L3/L4 critical claims;
- `takeover_difficulty: high` requires recovery evidence;
- difficult or irreversible action automation requires explicit human-reserved decisions;
- novel work with shared model, context, and method requires additional independence dimensions;
- low verifiability plus high time pressure requires decomposition, reduced autonomy, stronger external evidence, or an authorized risk decision.

## C. Human Oversight Case

The central durable artifact is a **Human Oversight Case (HOC)**:

```text
.agile-v/HUMAN_OVERSIGHT_CASE.yaml
```

Unlike a checklist, the HOC records claims, support, assumptions, defeaters, and decisions. A minimum claim set is:

| Claim ID | Claim |
|---|---|
| HOC-001 | An accountable human formed an independent expected outcome before builder recommendation exposure where required |
| HOC-002 | Critical acceptance claims have evidence with adequate independence |
| HOC-003 | Material differences among expected, predicted, and actual change were surfaced and resolved |
| HOC-004 | Required active challenge was falsifiable, executed, and evidenced |
| HOC-005 | Required intervention or recovery capability is supported at the selected evidence level |
| HOC-006 | Residual uncertainty, defeaters, reserved decisions, and decision authority are explicit |

Illustrative structure:

```yaml
schema_version: "1.0"
task_id: "TASK-XXXX"
risk_level: "L3"
requirements_baseline_ref: ".agile-v/baselines/BL-XXXX"
ai_run_manifest_ref: ".agile-v/aibom/TASK-XXXX/AI_RUN_MANIFEST.yaml"

oversight_demand: {}

claims:
  - claim_id: HOC-001
    statement: "Independent expected behavior was recorded before builder advice."
    status: supported | unsupported | disputed | not_applicable
    evidence_refs: []
    assumptions: []
    defeaters: []
    owner_role: "technical reviewer"

independence_profiles: []
surprises: []
challenge_checks: []
recovery_readiness: {}
human_reserved_decisions: []
final_decision: {}
```

A claim cannot be marked supported while a material defeater remains unresolved. Examples of defeaters include prior exposure to a builder recommendation, disputed human-origin provenance, a verifier sharing the only flawed test oracle, unreviewed unexpected scope, or an unexecuted recovery plan.

## D. Blind Human Expectation

For selected L2+ work, the human records an expected observable outcome and at least one primary failure concern before the builder's proposed solution or acceptance recommendation is exposed. “Blind” does not mean uninformed. Allowed inputs include stakeholder intent, persisted requirements, independent findings, approved constraints, and relevant system evidence. Prohibited inputs before capture include the builder's plan, generated implementation, generated acceptance recommendation, and builder-authored suggested wording for the human answer.

The record includes:

```yaml
human_expectation:
  expected_observable_outcome: "..."
  primary_failure_concerns: []
  unacceptable_outcomes: []
  decisions_reserved_for_human: []
  recovery_expectation: "..."
  prior_ai_exposure: none_known | prior_exposure | unknown
  human_origin_attestation:
    identity_or_role_ref: "..."
    timestamp: "..."
    approval_ref: "..."
```

The system should permit the answer:

```text
Unable to assess independently from the available evidence.
```

This is a valuable stop signal, not a user failure. It should trigger additional evidence, decomposition, reduced autonomy, a domain expert, or an explicit authorized decision. The agent may detect that the text is vague or incomplete, but it must not replace the human's concern with its own.

The term **human-origin attestation** is used deliberately. Metadata cannot prove independent cognition. A consuming runtime may strengthen provenance using identity, timestamps, content hashes, signed approvals, and event ordering, but the skills contract must not overstate what those mechanisms establish.

## E. Claim-Specific Independence Profile

Independence is not a binary property of an agent. It is a property of evidence relative to a claim and threat model. BAAC records an independence vector for evidence supporting critical claims:

```yaml
independence_profile:
  claim_ref: "HOC-002"
  evidence_ref: "TC-0042"
  role_independent: true
  context_independent: true
  model_independent: false
  provider_or_runtime_independent: false
  method_independent: true
  source_or_oracle_independent: true
  organizationally_independent: false
  temporally_independent: true
  rationale: "Test was derived from the frozen requirement and executed by a deterministic harness."
```

Dimensions are interpreted as follows:

| Dimension | Question |
|---|---|
| Role | Did a different responsibility produce or assess the evidence? |
| Context | Was builder conversation/rationale excluded? |
| Model | Does evidence avoid the same generative model family where relevant? |
| Provider/runtime | Does it avoid a concentrated execution path where relevant? |
| Method | Does it use a different verification method? |
| Source/oracle | Is the expected result independent of implementation assumptions? |
| Organization | Is a separate accountable assurance authority involved where required? |
| Time | Was evidence generated against the frozen candidate rather than co-evolving unnoticed? |

Not every dimension must differ. The Control Matrix selects claim-specific requirements. For L4 critical claims, at least one supporting evidence source should be independently observable and non-generative, such as a pre-existing regression oracle, deterministic analyzer, formal property, simulation, HIL measurement, controlled manual observation, or external system result. A second AI agent can contribute evidence but cannot alone transform AI agreement into independent assurance.

## F. Surprise Delta Gate

BAAC uses existing pre-change impact analysis and post-change diff evidence to preserve situation awareness. Three perspectives are kept distinct:

1. human expected behavior and concerns;
2. graph/tool-derived technical impact prediction;
3. actual artifact, test, and operational change.

The Surprise Delta Gate classifies deviations:

```text
critical | material | explainable | administrative
```

Each surprise includes:

- the expected or predicted state;
- the actual state;
- why the difference occurred;
- affected requirement, interface, control, or risk;
- supporting evidence;
- whether a change request or re-baseline is required;
- whether human acknowledgement is required;
- who has authority to resolve it.

Gate summaries present critical and material surprises before aggregate pass results. Administrative noise may be grouped using transparent rules so that “surprises first” does not become alert fatigue. The same builder that caused a material unexpected change may explain it but must not be the sole authority declaring it harmless where independent acknowledgement is required.

## G. Active Falsification Challenge

For L3/L4 and other tasks selected by ODP rules, the human gate includes a falsifiable challenge. The challenge hypothesis should originate from a source independent of the builder's implementation framing:

- the blind human concern;
- the Logic Gatekeeper, Threat Modeler, or Safety Engineer;
- the independent Test Designer;
- a controlled challenge catalog;
- mutation testing or fault injection;
- an independent domain reviewer.

A valid challenge record includes:

```yaml
challenge_check:
  id: "HC-0001"
  origin: "human_precommit"
  linked_claim_or_risk: "RISK-0042"
  hypothesis: "Authorization may be bypassed for an unauthenticated request."
  action: "Execute the negative access test against the frozen candidate."
  oracle: "Request is rejected without data disclosure."
  observed: "HTTP 401; no response body data."
  result: pass | fail | inconclusive
  evidence_ref: ".agile-v/evidence/auth-negative.log"
  performed_by_role: "technical reviewer"
```

The Build Agent may assist with execution mechanics but cannot be the sole source of the hypothesis and oracle. An inconclusive result remains inconclusive; it must not be converted into a pass to complete the workflow.

## H. Recovery Evidence Ladder

Recovery readiness is graded by evidence, not prose volume:

| Level | Recovery evidence |
|---|---|
| R0 | Concept or rollback statement only |
| R1 | Reviewed procedure, prerequisites, owner, and expected recovery time |
| R2 | Table-top walkthrough with recorded gaps |
| R3 | Staging, simulation, or representative dry-run execution |
| R4 | Representative HIL, controlled operational exercise, or equivalent real-system proof |

The Control Matrix selects the required level based on L0–L4 and the ODP. The record includes:

```yaml
recovery_readiness:
  required_level: R3
  demonstrated_level: R3
  responsible_role: "embedded engineer"
  procedure_ref: ".agile-v/RECOVERY_PLAN.md"
  prerequisites: []
  expected_recovery_time_minutes: 20
  observed_recovery_time_minutes: 17
  demonstration_ref: ".agile-v/evidence/recovery-run.md"
  recency: "2026-08-21"
  limitations: []
  result: pass | fail | partial | not_run
```

A documented plan at R1 cannot satisfy an R3 requirement. Missing credentials, unavailable artifacts, undocumented physical access, or an expired procedure are material defeaters.

## I. Human-Reserved Decisions and Non-Coercive Uncertainty

BAAC explicitly reserves decisions that an agent may advise on but not make for itself:

- acceptance of residual risk;
- concessions and waivers;
- final release authorization;
- classification of material unexpected scope as acceptable;
- approval of irreversible action;
- resolution of disputed human-origin evidence;
- acceptance of recovery evidence below policy.

The workflow must not coerce confidence. “Unable to assess” and “evidence insufficient” are valid outcomes. This prevents the process from rewarding fabricated certainty.

## J. Longitudinal Capability Maintenance

Task-level challenge does not fully address skill decay. BAAC therefore permits organizational policy hooks for:

- periodic manual diagnostic exercises;
- recovery drills;
- reviewer rotation;
- incident-derived scenarios;
- expiry or recency requirements for recovery evidence;
- team-level competence assumptions and escalation paths.

These controls should be proportionate and privacy-preserving. BAAC does not certify individual competence and should not become an employee-surveillance system. Team- or role-level readiness is generally preferable to simplistic individual scoring.

# VI. Contract Semantics and Gate Rules

## A. Notation

For a task `t`:

- `R(t)` is its Agile V level `L0`–`L4`;
- `D(t)` is its Oversight Demand Profile;
- `C(t)` is the set of critical acceptance and oversight claims;
- `E(c)` is the evidence supporting claim `c`;
- `I(e)` is the independence vector of evidence `e`;
- `P(R,D,c)` is the policy-selected set of required independence and control conditions;
- `Defeaters(c)` is the set of unresolved rebuttals to claim `c`.

Evidence is adequate for a claim when:

```text
Adequate(c) =
  exists e in E(c):
    supports(e, c)
    and independence_satisfies(I(e), P(R(t), D(t), c))
    and evidence_is_reproducible_or_observable(e)
    and no_material_conflict(e)
```

For a critical L4 claim, policy additionally requires at least one independently observable, non-generative evidence anchor.

## B. Gate 2 Predicate

A Bainbridge-aware Gate 2 decision is valid only if:

```text
Gate2(t) =
  BaselinedRequirements(t)
  AND AuthorizedHumanDecision(t)
  AND RequiredHumanExpectation(t)
  AND all c in C(t): Adequate(c)
  AND MaterialSurprisesResolved(t)
  AND RequiredChallengeSatisfied(t)
  AND RequiredRecoverySatisfied(t)
  AND NoUnresolvedMaterialDefeater(t)
  AND IntendedUseValidationSatisfiedWhenRequired(t)
```

This predicate is a contract model, not a mathematical proof of safety. It prevents several invalid substitutions:

```text
SchemaValid(record)       != ClaimTrue(record)
HumanApprovalPresent      != HumanUnderstandingDemonstrated
DifferentAgent            != IndependentAssurance
AIConsensus               != ExternalEvidence
ExplanationAvailable      != VerificationComplete
RollbackDocumentExists    != RecoveryCapabilityDemonstrated
VerificationPassed        != IntendedUseValidated
```

## C. No Composite Oversight Score

BAAC deliberately avoids a weighted score. Scores can mask a critical missing control: excellent documentation should not compensate for an unverified safety property or unavailable recovery path. The decision model is conjunctive and policy-based. Unknown values fail closed where the risk profile requires resolution.

## D. Evidence Provenance

Recommended provenance categories are:

```text
human-origin-attestation
builder-agent
independent-test-agent
red-team-agent
pre-existing-baseline
formal-or-static-tool
deterministic-test-harness
simulation
HIL
external-system
controlled-manual-observation
organizational-assurance
```

Provenance supports reasoning about independence but does not establish truth by label alone. AI-run manifests, tool records, delegation records, artifact hashes, timestamps, and approvals should be linked where available.

## E. State and Mutability

A consuming runtime should protect relevant ordering:

```text
human_expectation_draft
  -> human_expectation_attested
  -> gate_1_approved
  -> requirements_baselined
  -> build_and_independent_test
  -> verification
  -> surprise_review
  -> active_challenge
  -> gate_2_decision
```

Changes to attested human expectation after builder recommendation exposure should create a new revision with explicit contamination and rationale rather than silently overwriting the original. Historical records remain immutable.

# VII. Mapping to the Agile V Skills Repository

## A. New Draft Skill and Artifacts

The skills repository should add:

```text
agile-v-human-oversight/SKILL.md
schemas/HUMAN_OVERSIGHT_CASE.schema.json
templates/agile-v/HUMAN_OVERSIGHT_CASE.example.yaml
docs/agile-v-runtime/06_HUMAN_OVERSIGHT_CONTRACT.md
```

The skill should begin with `metadata.status: draft`. It should remain concise and cross-cutting, delegating lifecycle, requirements, testing, verification, validation, release, provenance, and control-matrix details to existing companion skills.

## B. Changes to Existing Skills

| Skill | Bainbridge-aware responsibility |
|---|---|
| `agile-v-core` | Add the effective-oversight invariant; expose surprises, unverified behavior, residual risk, and recovery before pass totals |
| `requirement-architect` | Capture blind human expectation where policy requires it before builder recommendation exposure |
| `logic-gatekeeper` | Preserve disagreement; never rewrite human-origin evidence |
| `test-designer` | Cover approved human concerns where testable while remaining implementation-independent |
| `red-team-verifier` | Evaluate HOC claims, evidence independence, surprise resolution, challenge quality, and recovery evidence |
| `agile-v-control-matrix` | Select required HOC controls, independence dimensions, and recovery level |
| `impact-analysis-agent` | Produce pre-change technical prediction and highlight disagreement with human expectation |
| `diff-evidence-agent` | Compare actual change to prediction and require appropriate acknowledgement of material surprises |
| `release-manager` | Block release when required HOC claims, authority, challenge, or recovery evidence are unresolved |
| `agile-v-aibom` | Supply model, runtime, tool, skill, and context provenance needed for correlation analysis |
| `validation-agent` | Preserve intended-use validation as distinct from implementation verification and oversight evidence |

## C. Behavioral Contract Tests

The repository should add deterministic contract scenarios for:

- missing human expectation where required;
- vague but syntactically valid precommit;
- prior AI exposure and contamination disclosure;
- agent-authored text falsely labeled as human;
- builder and verifier sharing all relevant independence dimensions;
- a deterministic independent oracle satisfying a claim despite using the same model elsewhere;
- material unexpected scope without human acknowledgement;
- non-falsifiable challenge;
- challenge designed entirely by the builder;
- recovery document below the required evidence level;
- L4 AI-only agreement without non-generative evidence;
- “unable to assess” causing valid escalation rather than forced completion;
- intended-use validation incorrectly substituted by verification;
- backward compatibility for projects without the preview control enabled.

Tests can validate structure and prescribed behavior. They cannot empirically prove that the controls improve human performance.

## D. Consuming-Runtime Responsibilities

The skills library must clearly assign runtime enforcement to consumers. Examples include:

- preventing implementation before required expectation and Gate 1 records exist;
- protecting human-origin records from agent modification;
- binding approvals to identity, scope, content hash, action, and time;
- preventing self-approval and forged provenance;
- verifying event order;
- blocking release on unresolved required claims;
- recording tool, model, context, and artifact identities;
- enforcing control-matrix requirements.

A host that cannot enforce a control should report the control as advisory and must not claim equivalent assurance.

# VIII. Evaluation Protocol

The paper proposes a testable design, not a completed evaluation. A preregistered controlled study should compare three conditions.

## A. Experimental Conditions

| Condition | Workflow |
|---|---|
| C0—Ordinary AI review | AI builder, generated tests/evidence, conventional human pull-request review |
| C1—Current Agile V | frozen requirements, independent findings, independent test design, Red Team verification, Human Gates |
| C2—BAAC Agile V | C1 plus ODP, blind human expectation, HOC, claim-specific independence, surprise gate, active challenge, and recovery evidence |

A secondary ablation study should remove one BAAC component at a time to identify which controls contribute value and which add cost without benefit.

## B. Research Questions

- **RQ1:** Does BAAC reduce false acceptance of defective AI-generated changes compared with C0 and C1?
- **RQ2:** Does BAAC improve appropriate reliance, defined as correct acceptance of sound changes and correct rejection of defective changes?
- **RQ3:** Does BAAC improve situation awareness and fault localization after agent implementation?
- **RQ4:** Does recovery evidence improve successful intervention and recovery time under injected failure?
- **RQ5:** What review time, cognitive workload, false-alarm, and usability costs does BAAC impose?
- **RQ6:** Which independence dimensions reduce correlated builder/verifier failures?
- **RQ7:** Do blind human expectations remain substantive over repeated tasks, or do they become ceremonial?
- **RQ8:** Do controls affect participants differently across expertise, accessibility needs, and prior AI reliance?

## C. Seeded Failure Classes

Tasks should include balanced sound and defective changes. Defects should be introduced independently of participants and hidden from reviewers:

1. implementation defect detectable by an ordinary test;
2. omission defect hidden by incomplete generated tests;
3. requirement defect that implementation verification cannot resolve;
4. correlated builder/verifier error;
5. unexpected scope expansion into a security or data boundary;
6. misleading but schema-valid provenance;
7. forged human-origin or approval evidence;
8. rollback procedure that fails due to a missing prerequisite;
9. sound change with noisy low-severity warnings to test false rejection and alert fatigue;
10. time-critical failure requiring human takeover.

## D. Participants and Tasks

Participants should include practicing engineers with relevant domain experience. Expertise, familiarity with the repository, AI-tool experience, and security or safety background should be recorded. Task domains should include ordinary application code and at least one high-consequence or cyber-physical scenario, but sector claims must remain bounded to the sampled tasks.

Sample size should be selected by prospective power analysis using the primary outcome and expected clustering by participant and task. The study should not choose a sample after inspecting significance.

## E. Primary Outcomes

```text
unsafe acceptance rate
sound-change acceptance rate
seeded-defect detection rate
fault localization accuracy
time to correct decision
recovery success
recovery time
confidence-to-correctness calibration
```

Appropriate reliance can be represented using a confusion matrix:

| Artifact state | Human accepts | Human rejects/escalates |
|---|---|---|
| Sound | correct acceptance | false rejection |
| Defective | unsafe acceptance | correct rejection/escalation |

The objective is not maximum rejection. A control that reduces unsafe acceptance by causing indiscriminate rejection may be operationally unacceptable.

## F. Secondary Outcomes

```text
review duration
NASA-TLX or suitable workload measure
number and severity of reviewed surprises
challenge yield
false alarm rate
waiver frequency
amount of evidence inspected
retained system understanding
participant trust calibration
perceived usefulness and usability
```

Retained understanding should be measured after a delay using explanation, prediction, diagnosis, and recovery tasks rather than self-report alone.

## G. Analysis Plan

Binary outcomes should be analyzed using mixed-effects logistic models with participant and task as random effects where appropriate. Time outcomes may require log transformation or survival analysis. Confidence calibration can be evaluated using calibration curves and proper scoring rules. Multiple primary comparisons should be preregistered and corrected. Effect sizes and uncertainty intervals should be reported regardless of statistical significance.

Qualitative interviews should examine:

- how participants formed expectations;
- which evidence changed their decision;
- when the process felt ceremonial;
- how surprises affected mental models;
- why participants bypassed or disliked controls;
- whether “unable to assess” was psychologically safe;
- accessibility and workload barriers.

## H. Manipulation and Integrity Checks

The evaluation should verify that:

- blind participants did not see builder advice before expectation capture;
- C1 and C2 verifiers were isolated from builder reasoning as specified;
- provenance and event-order records match the experimental condition;
- seeded defects were neither accidentally revealed nor removed;
- challenge cases could genuinely fail;
- recovery exercises used the intended artifact and environment;
- experimenters remained blinded to condition where practical during outcome coding.

## I. Open Science and Artifact Evaluation

The study should publish, subject to security and privacy constraints:

- preregistration;
- task and defect taxonomy;
- anonymized data dictionary;
- analysis code;
- skill versions and hashes;
- model, runtime, tool, and context manifests;
- schemas and fixtures;
- negative and positive examples;
- limitations and deviations from protocol.

Security-sensitive tasks should be redacted or replaced with representative synthetic artifacts. Hidden model chain-of-thought should not be collected or published.

# IX. Threats to Validity and Ethical Considerations

## A. Construct Validity

No single measure fully captures effective oversight. Defect detection, confidence, situation awareness, and recovery are related but distinct. A participant can detect a bug without understanding the system broadly, or understand the system while lacking authority to act. The evaluation therefore requires multiple outcomes.

Human-origin attestation is not proof of independent cognition. Prior AI exposure can contaminate a supposedly blind expectation. The protocol records exposure and treats disputed origin as a defeater rather than asserting certainty.

## B. Internal Validity

Participants may behave more carefully because they know they are studied. Repeated tasks may create learning or fatigue effects. Defect difficulty may differ across conditions. Counterbalancing, randomization, preregistered coding, and mixed-effects analysis are needed.

## C. External Validity

Laboratory repositories and seeded defects cannot reproduce all organizational, regulatory, and operational conditions. Results may not generalize across languages, models, companies, safety domains, or team structures. Field studies and longitudinal replications are necessary before broad effectiveness claims.

## D. Common-Mode Failure

Even “independent” evidence can share flawed requirements, libraries, infrastructure, or data. The Independence Profile makes these dependencies visible but cannot eliminate unknown correlations. Critical decisions should use domain-appropriate assurance methods rather than relying on a universal agent pattern.

## E. Review Fatigue and Process Gaming

Additional records can cause alert fatigue, boilerplate, or bypass behavior. BAAC therefore requires surprise triage, challenge yield measurement, and proportional control selection. Metrics can themselves be gamed; outcome measures should dominate counts of completed forms.

## F. Accessibility, Fairness, and Privacy

Cognitive forcing may impose unequal burdens across users. Equivalent accessible modes should preserve the control objective without treating speed, writing fluency, or a preferred interaction style as competence. Identity and capability records should minimize personal data. Team- or role-level readiness is preferable where individual tracking is unnecessary.

## G. Accountability and Psychological Safety

Accountability can improve verification but can also produce blame avoidance and excessive conservatism. “Unable to assess” must be an accepted escalation outcome. Organizations should evaluate decision-process quality rather than punish uncertainty disclosure or disagreement with automation.

## H. Regulatory and Standards Claims

BAAC may support documentation relevant to AI governance, quality, safety, or compliance programs, but it does not establish legal compliance, certification, conformity, or product safety. Applicable standards and laws require qualified interpretation and controlled source texts.

# X. Discussion

## A. Why Skills Rather Than a Monolithic Agent Framework?

A skill-based architecture separates normative roles from execution engines. The same assurance contract can be used with different coding agents and runtimes while retaining stable artifacts and handoffs. This reduces dependence on a particular vendor and makes role contamination easier to reason about. The limitation is equally important: Markdown instructions cannot enforce themselves. Strong deployments require runtime and organizational controls that implement the contract faithfully.

## B. From Human-in-the-Loop to Joint-System Assurance

The phrase “human-in-the-loop” describes topology, not effectiveness. BAAC changes the unit of analysis from the AI artifact to the joint human-agent system. It asks whether the workflow preserved independent expectations, exposed disagreements, provided adequate evidence, reserved authority, and maintained intervention capability.

This framing also avoids a false choice between automation and manual work. The goal is not to force humans to duplicate everything an agent does. Humans should spend attention on values, ambiguity, material surprise, failure hypotheses, evidence adequacy, residual risk, and recovery—while deterministic automation performs repeatable checks and agents accelerate synthesis.

## C. Independence as a Portfolio

The proposed Independence Profile treats assurance as a portfolio of partially independent methods. A verifier using the same model may still add value if it starts from a fresh baseline and executes a deterministic property test. A different model may add little if it receives the same flawed builder-written test and summary. Independence should therefore be justified per claim rather than inferred from agent count.

## D. Recovery as a First-Class Engineering Output

Software processes often document rollback but under-test recovery. Bainbridge's analysis makes recovery central: the human role becomes most demanding when automation fails. Recording actual recovery evidence, prerequisites, recency, and observed time converts a vague fallback into a reviewable engineering claim.

## E. Strong Claims Require Empirical Restraint

The proposed design is promising because it is falsifiable. It could fail if humans produce boilerplate expectations, if challenge costs outweigh detection gains, if independence metadata is unreliable, or if recovery exercises do not transfer to incidents. These possibilities should be treated as research questions, not hidden behind confident governance language.

# XI. Conclusion

AI-assisted engineering can retain a human approval step while progressively removing the knowledge, practice, and independent evidence needed for that approval to be meaningful. Bainbridge's ironies of automation therefore apply not merely to deployment-time operation but to the engineering workflow itself.

This paper proposed a Bainbridge-Aware Assurance Contract for Agile V Agent Skills. The contract adds an Oversight Demand Profile, blind human expectation, claim-based Human Oversight Case, claim-specific independence, surprise-delta review, falsifiable challenge, recovery evidence, and longitudinal capability hooks. It preserves existing Agile V risk levels, lifecycle states, role separation, Human Gates, traceability, and runtime-neutral skill structure. It also defines strict boundaries: schema validity is not truth, agent agreement is not independent assurance, approval is not demonstrated understanding, and a rollback document is not recovery capability.

The approach should be judged by outcomes: whether it reduces unsafe acceptance while preserving correct acceptance, improves fault localization and recovery, calibrates confidence, and does so at an acceptable human cost. Until such evidence exists, BAAC is a design and evaluation framework—not a proven solution. Its central invariant is nevertheless clear:

> Do not merely keep a human in the workflow. Preserve and test the human's capacity to understand, challenge, intervene, and recover.

---

# References

[1] L. Bainbridge, “Ironies of automation,” *Automatica*, vol. 19, no. 6, pp. 775–779, 1983, doi: 10.1016/0005-1098(83)90046-8.

[2] M. R. Endsley and E. O. Kiris, “The out-of-the-loop performance problem and level of control in automation,” *Human Factors*, vol. 37, no. 2, pp. 381–394, 1995, doi: 10.1518/001872095779064555.

[3] R. Parasuraman and V. Riley, “Humans and automation: Use, misuse, disuse, abuse,” *Human Factors*, vol. 39, no. 2, pp. 230–253, 1997, doi: 10.1518/001872097778543886.

[4] R. Parasuraman, T. B. Sheridan, and C. D. Wickens, “A model for types and levels of human interaction with automation,” *IEEE Trans. Syst., Man, Cybern. A, Syst. Humans*, vol. 30, no. 3, pp. 286–297, 2000, doi: 10.1109/3468.844354.

[5] J. D. Lee and K. A. See, “Trust in automation: Designing for appropriate reliance,” *Human Factors*, vol. 46, no. 1, pp. 50–80, 2004, doi: 10.1518/hfes.46.1.50_30392.

[6] N. B. Sarter and D. D. Woods, “Team play with a powerful and independent agent: Operational experiences and automation surprises on the Airbus A-320,” *Human Factors*, vol. 39, no. 4, pp. 553–569, 1997, doi: 10.1518/001872097778667997.

[7] G. Klein, D. D. Woods, J. M. Bradshaw, R. R. Hoffman, and P. J. Feltovich, “Ten challenges for making automation a ‘team player’ in joint human-agent activity,” *IEEE Intell. Syst.*, vol. 19, no. 6, pp. 91–95, 2004, doi: 10.1109/MIS.2004.74.

[8] L. J. Skitka, K. L. Mosier, and M. D. Burdick, “Accountability and automation bias,” *Int. J. Human-Computer Studies*, vol. 52, no. 4, pp. 701–717, 2000, doi: 10.1006/ijhc.1999.0349.

[9] R. Parasuraman and D. H. Manzey, “Complacency and bias in human use of automation: An attentional integration,” *Human Factors*, vol. 52, no. 3, pp. 381–410, 2010, doi: 10.1177/0018720810376055.

[10] Z. Buçinca, M. B. Malaya, and K. Z. Gajos, “To trust or to think: Cognitive forcing functions can reduce overreliance on AI in AI-assisted decision-making,” *Proc. ACM Human-Computer Interaction*, vol. 5, no. CSCW1, Art. no. 188, 2021, doi: 10.1145/3449287.

[11] H. Pearce, B. Ahmad, B. Tan, B. Dolan-Gavitt, and R. Karri, “Asleep at the keyboard? Assessing the security of GitHub Copilot's code contributions,” in *Proc. 2022 IEEE Symp. Security and Privacy*, 2022, pp. 754–768, doi: 10.1109/SP46214.2022.9833571.

[12] N. Perry, M. Srivastava, D. Kumar, and D. Boneh, “Do users write more insecure code with AI assistants?” in *Proc. 2023 ACM SIGSAC Conf. Computer and Communications Security*, 2023, pp. 2785–2799, doi: 10.1145/3576915.3623157.

[13] M. Vaccaro, A. Almaatouq, and T. W. Malone, “When combinations of humans and AI are useful: A systematic review and meta-analysis,” *Nature Human Behaviour*, vol. 8, pp. 2293–2303, 2024, doi: 10.1038/s41562-024-02024-1.

[14] E. Tabassi, “Artificial Intelligence Risk Management Framework (AI RMF 1.0),” National Institute of Standards and Technology, NIST AI 100-1, 2023, doi: 10.6028/NIST.AI.100-1.

[15] European Parliament and Council of the European Union, “Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence,” *Official Journal of the European Union*, 2024, Art. 14.

[16] *IEEE Standard Model Process for Addressing Ethical Concerns during System Design*, IEEE Std 7000-2021, 2021; also published as ISO/IEC/IEEE 24748-7000:2022.

[17] D. D. Woods and N. B. Sarter, “Learning from automation surprises and ‘going sour’ accidents,” NASA Ames Research Center, NASA/CR-1998-207061, 1998.

[18] S. W. A. Dekker and D. D. Woods, “MABA-MABA or abracadabra? Progress on human-automation co-ordination,” *Cognition, Technology & Work*, vol. 4, no. 4, pp. 240–244, 2002, doi: 10.1007/s101110200022.

[19] C. D. Wickens, B. A. Clegg, A. Z. Vieane, and A. L. Sebok, “Complacency and automation bias in the use of imperfect automation,” *Human Factors*, vol. 57, no. 5, pp. 728–739, 2015, doi: 10.1177/0018720815581940.

[20] Agile V Project, “Agile V Agent Skills Library,” GitHub repository. Artifact version, commit hash, and access date to be fixed at submission.

---

## Draft-to-Submission Checklist

- [ ] Confirm target IEEE venue and page limit
- [ ] Replace anonymous author placeholders after internal approval
- [ ] Freeze the cited Agile V repository commit and archive an artifact release
- [ ] Verify every bibliographic record against publisher metadata
- [ ] Add a figure suitable for IEEE two-column layout
- [ ] Decide whether the first submission is a design paper, experience report, or registered evaluation protocol
- [ ] Preregister the empirical protocol before collecting effectiveness data
- [ ] Obtain ethics/privacy review where human participants or organizational data are involved
- [ ] Add empirical results only after analysis; do not convert hypotheses into claims
- [ ] Ensure standards and regulatory wording remains bounded and non-certifying
