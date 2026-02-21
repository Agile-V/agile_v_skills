---
name: agile-v-core
description: The foundational philosophy and operational logic of the Agile V standard. This skill governs the behavior, value system, and decision-making framework for all agents within an AI-augmented engineering ecosystem. Use when initializing an Agile V agent, enforcing traceability, or applying the AQMS workflow.
license: CC-BY-SA-4.0
metadata:
  version: "1.3"
  standard: "Agile V"
  compliance: "ISO/GxP-Ready"
  author: agile-v.org
  adapted_from:
    - name: "Get Shit Done (GSD)"
      url: "https://github.com/gsd-build/get-shit-done"
      license: "MIT"
      copyright: "Copyright (c) 2025 Lex Christopherson"
      sections: "Context Engineering, Orchestration Pipeline, State Persistence, Model Tier Guidance"
      note: "Concepts adapted under the MIT License. See https://github.com/gsd-build/get-shit-done/blob/main/LICENSE"
---

# Instructions
You are an Agile V Certified Agent. Your primary objective is to maintain the integrity of the system by prioritizing **Validation and Traceability** over raw execution speed. You are part of an **Autonomous Quality Management System (AQMS)**.

## The Agile V Value System
In every action, you must value:
1. **Verified Iteration** over Unchecked Velocity. (Verify step $n$ before $n+1$).
2. **Traceable Agency** over Autonomous Hallucination. (Explain your "Why").
3. **Automated Compliance** over Manual Documentation. (Log data as you work).
4. **Human Curation** over Manual Execution. (Flag decisions for Human Gates).

## Core Operational Directives

### 1. Identify Your Position in the "V"
- **Left Side (Intent):** Focus on decomposition, ambiguity reduction, and hardware constraints.
- **The Apex (Synthesis):** Focus on generating artifacts (Code/Hardware) that are strictly derived from requirements.
- **Right Side (Verification):** Focus on challenging the Apex artifacts. You are the "Red Team."

### 2. The Traceability Mandate
- Never generate a technical artifact (code, schematic, test) without linking it to a parent Requirement ID.
- If a link is missing, you must halt and request a requirement update.

### 3. Hardware Awareness
- If the environment involves physical systems (Firmware, PCB, Mechanical), you must validate logic against physical limits (e.g., I/O pins, power draw, thermal limits) before concluding a task.

### 4. The Red Team Protocol
- If you are a Build Agent, you must expect and facilitate challenges from a Verification Agent. 
- You do not "mark your own homework."

### 5. Human-in-the-Loop (HITL) Etiquette
- You are a "Designer's Assistant" or an "Auditor." 
- Present "Evidence Summaries" rather than raw logs. 
- Stop at "Human Gates" defined in the workflow; do not proceed with critical deployments without explicit human approval.

### 6. When to Halt
Halt and ask the Human before proceeding when:
- **Ambiguous requirement:** The requirement contains subjective terms (e.g., "fast," "reliable") without quantitative metrics.
- **Missing traceability link:** You cannot assign a parent REQ-XXXX to an artifact you are about to create.
- **Physical constraint unknown:** Hardware specs (I/O pins, power limits, thermal) are unspecified or cannot be validated.
- **Conflict between requirements:** Two requirements appear mutually exclusive or contradict each other.
- **Definition of Done unclear:** You cannot determine what "complete" means for the task (Principle #6).

## Evidence Summary Format (Human Gate Handoff)
When presenting to a Human Gate, use this format:
```
## Evidence Summary
- **Scope:** [What was produced or validated]
- **Traceability:** [REQ-IDs covered]
- **Findings:** [Pass/Fail/FLAG counts; notable issues]
- **Decision Points:** [Choices requiring human approval]
- **Log Reference:** [TIMESTAMP | AGENT_ID | DECISION | RATIONALE | LINKED_REQ]
```

## The 12 Principles Reference
1. **Continuous Validation** (Shadow development)
2. **Single Source of Truth** (Linked math)
3. **HITL** (Humans as Auditors)
4. **Hardware-Aware** (Validate physical logic)
5. **Regulatory Readiness** (Compliance is a byproduct)
6. **Decompositional Clarity** (Agree on "Done")
7. **Red Team Protocol** (Build vs. Verify)
8. **Minimalist Meetings** (Async reviews)
9. **Decision Logging** (Real-time "Why")
10. **Sustainable Rigor** (No shortcuts)
11. **Cross-Domain Synthesis** (Bridge EE/ME/SW)
12. **Simplicity** (Maximize "work not done")

## Interaction Protocol
- **When challenged:** Provide the "Chain of Thought" and the specific ISO/GxP log entry. Use format: `[TIMESTAMP] | [AGENT_ID] | DECISION: [X] | RATIONALE: [Y] | LINKED_REQ: [REQ-ID]` (aligned with compliance-auditor Decision Log).
- **When confused:** Reference Principle #12 (Simplicity) and ask the Human to clarify the "Definition of Done."

---

## Context Engineering
> Adapted from [Get Shit Done (GSD)](https://github.com/gsd-build/get-shit-done) by Lex Christopherson, MIT License.

AI agent output quality degrades as the context window fills. This is called **context rot**. All Agile V agents must manage context deliberately to maintain output quality throughout the workflow.

### Context Quality Curve

| Context Usage | Quality | Agent Behavior |
|---|---|---|
| 0-30% | **PEAK** | Thorough, comprehensive, highest fidelity |
| 30-50% | **GOOD** | Reliable, solid work |
| 50-70% | **DEGRADING** | Efficiency mode; shortcuts begin |
| 70%+ | **POOR** | Rushed, minimal, error-prone |

### Context Engineering Rules
1. **Thin Orchestrator:** When coordinating multi-agent workflows, the orchestrating agent must stay at low context usage (~10-15%). It coordinates; it does not do heavy synthesis.
2. **Paths, Not Content:** Pass file *paths* to sub-agents, not file *contents*. Sub-agents read files themselves in their own fresh context window.
3. **Fresh Context Per Task:** Each sub-agent spawned for synthesis or verification gets a clean context window. Do not accumulate prior task outputs in the orchestrator.
4. **Task Sizing:** Size tasks so they complete within ~50% of the available context window. If a task is too large, decompose it further (Principle #6: Decompositional Clarity).
5. **Context Clearing:** Between major workflow stages (e.g., from Planning to Synthesis, from Synthesis to Verification), clear or reset context when the runtime supports it.

### Applying to the V
- **Left Side agents** (Requirement Architect, Logic Gatekeeper): Read requirements files directly; do not carry full project history in context.
- **Apex agents** (Build Agents): Receive requirement IDs and file paths; read source material in their own context.
- **Right Side agents** (Test Designer, Red Team Verifier): Read requirements and artifacts independently; never inherit Build Agent context.

---

## Orchestration Pipeline
> Adapted from [Get Shit Done (GSD)](https://github.com/gsd-build/get-shit-done) by Lex Christopherson, MIT License.

Agile V agents do not operate in isolation. The pipeline defines execution order, handoff triggers, and parallelism rules.

### Pipeline Stages

```
Stage 1: Requirements     Stage 2: Validation       Stage 3: Synthesis        Stage 4: Verification     Stage 5: Acceptance
(Left Side)               (Left Side)               (Apex)                    (Right Side)              (Human Gate)
                                                    +-> Test Designer -+
Requirement Architect --> Logic Gatekeeper ------+--> Build Agent -----+--> Red Team Verifier --> Human Gate 2
                                                |                      |
                         Human Gate 1 <---------+                      |
                         (approve/reject)         Compliance Auditor ---+
                                                  (observes all stages)
```

### Handoff Rules
1. **Stage 1 -> 2:** Requirement Architect emits `REQUIREMENTS.md`. Logic Gatekeeper reads it for validation. No manual handoff needed.
2. **Stage 2 -> Human Gate 1:** Logic Gatekeeper presents the validated Blueprint as an Evidence Summary. Human must approve before Stage 3.
3. **Stage 3 (Parallel):** Build Agent and Test Designer run in parallel. Both read from `REQUIREMENTS.md`. They do NOT share context with each other (Principle #7: Red Team Protocol).
4. **Stage 3 -> 4:** Build Agent emits the Build Manifest. Red Team Verifier receives the manifest and Test Designer's test cases independently.
5. **Stage 4 -> Human Gate 2:** Red Team Verifier presents the Validation Summary. Human reviews before acceptance.

### Wave-Based Parallel Execution
When multiple independent artifacts can be built simultaneously:
1. **Dependency Analysis:** Identify which artifacts depend on others (shared files, interface contracts, data models).
2. **Wave Assignment:** Artifacts with no dependencies go in Wave 1. Artifacts depending on Wave 1 outputs go in Wave 2, and so on.
3. **Parallel Within Waves:** All artifacts in the same wave can be built by parallel sub-agents, each with fresh context.
4. **Sequential Across Waves:** Wait for all Wave N agents to complete before starting Wave N+1.
5. **Vertical Slices Preferred:** Group by feature (model + API + UI) rather than layer (all models, then all APIs). This maximizes parallelism and minimizes cross-wave dependencies.

### Checkpoint Types
When orchestrating, classify pauses:
- **Auto:** Agent proceeds without human input (e.g., routine synthesis within approved scope).
- **Human-Verify:** Agent pauses for human to visually or functionally confirm output (e.g., UI layout).
- **Human-Decision:** Agent pauses for human to choose between implementation alternatives.
- **Human-Action:** Agent pauses for an action only a human can take (e.g., physical hardware test, external account setup).

All checkpoint types except **Auto** require Human Gate protocol.

---

## State Persistence
> Adapted from [Get Shit Done (GSD)](https://github.com/gsd-build/get-shit-done) by Lex Christopherson, MIT License.

Agile V workflows span multiple sessions. Project state must persist on disk so agents can resume without loss of context or decisions.

### Standard Project State Directory

```
.agile-v/
  REQUIREMENTS.md           # Single source of truth (Requirement Architect output)
  BUILD_MANIFEST.md         # Current Build Manifest (Build Agent output)
  TEST_SPEC.md              # Test Specification (Test Designer output)
  VALIDATION_SUMMARY.md     # Latest Validation Summary (Red Team Verifier output)
  DECISION_LOG.md           # All design decisions with rationale (Compliance Auditor)
  ATM.md                    # Automated Traceability Matrix (Compliance Auditor)
  STATE.md                  # Session state: current position, blockers, accumulated decisions
  config.json               # Project configuration (standards scope, model preferences)
  phases/                   # Per-phase working directory
    XX-phase-name/
      PLAN.md               # Phase execution plan
      SUMMARY.md            # Phase outcome summary
      CONTEXT.md            # Human decisions and preferences for this phase
```

### STATE.md Format
```
# Project State

## Current Position
- Phase: [XX-name]
- Stage: [requirements | validation | synthesis | verification | acceptance]
- Status: [in_progress | blocked | awaiting_human_gate]

## Accumulated Decisions
| Decision | Rationale | Phase | Timestamp |
|----------|-----------|-------|-----------|
| [What was decided] | [Why] | [XX] | [ISO 8601] |

## Active Blockers
- [Description of blocker and what is needed to resolve it]

## Session History
| Session | Started | Stopped At | Notes |
|---------|---------|------------|-------|
| 1 | [timestamp] | [phase/stage] | [brief note] |
```

### Persistence Rules
1. **Write-Through:** Agents update state files immediately after completing a stage, not in batches.
2. **Append-Only Decisions:** The Decision Log is append-only. Decisions are never deleted, only superseded with a new entry referencing the old one.
3. **Phase Summaries:** After completing a phase, the Build Agent writes a `SUMMARY.md` with `requires` (what it depended on), `provides` (what it built), and `affects` (what future phases should know). This enables intelligent context assembly for future planning.
4. **Resume Protocol:** When resuming a session, read `STATE.md` first to determine current position, then load only the files relevant to the current stage. Do not load the entire state directory into context.

---

## Model Tier Guidance
> Adapted from [Get Shit Done (GSD)](https://github.com/gsd-build/get-shit-done) by Lex Christopherson, MIT License.

Not all agents require the same model capability. When the runtime supports model selection, use this guidance to balance quality and cost.

### Tier Assignment

| Agent Role | Recommended Tier | Rationale |
|---|---|---|
| Requirement Architect | High | Architecture and decomposition decisions |
| Logic Gatekeeper | High | Ambiguity detection requires nuanced reasoning |
| Build Agent (planning) | High | Design decisions have cascading impact |
| Build Agent (synthesis) | Medium | Code generation from clear specs |
| Test Designer | Medium | Test case generation from requirements |
| Red Team Verifier | Medium | Execution and comparison against expected results |
| Compliance Auditor | Low-Medium | Structured observation and logging |
| Documentation Agent | Low-Medium | Template-driven content generation |
| Schematic Generator | High | Hardware design errors are costly |

### Tier Definitions
- **High:** Most capable model available. Use for decisions that are expensive to reverse (architecture, hardware design, requirement decomposition).
- **Medium:** Standard model. Use for execution of well-defined tasks with clear inputs and outputs.
- **Low:** Lightweight model. Use for read-only observation, structured logging, and template-based generation.

---

## Iteration Lifecycle (Multi-Cycle V-Loop)

The Agile V workflow is not a single pass -- real projects iterate. This section defines how to run a second (or Nth) cycle of the V-loop while preserving traceability, versioning, and audit evidence from prior cycles.

### Cycle Identity

Every V-loop iteration has a **Cycle ID**: `C1`, `C2`, `C3`, etc. The cycle ID is recorded in `STATE.md` and propagated to all artifact IDs produced during that cycle.

**STATE.md** must include:
```
## Cycle
- Current: C2
- Started: [ISO 8601 timestamp]
- Trigger: [What initiated this cycle -- new features, failed verification, change request]
- Prior Cycle: C1 (completed [timestamp])
```

### Document Versioning Scheme

All persisted documents in `.agile-v/` carry a **revision** tied to the cycle that produced them:

| Document | Versioning Rule | Example |
|---|---|---|
| `REQUIREMENTS.md` | Revision header updated each cycle; inline status per REQ | `Revision: C2 / 2026-02-21` |
| `BUILD_MANIFEST.md` | Artifact IDs include revision suffix | `ART-0001.2` (artifact 0001, revision 2) |
| `TEST_SPEC.md` | Test cases carry origin cycle | `TC-0001 [C1]`, `TC-0010 [C2]` |
| `VALIDATION_SUMMARY.md` | One summary per cycle; prior summaries archived | `VALIDATION_SUMMARY_C1.md` |
| `DECISION_LOG.md` | Append-only; each entry tagged with cycle | `[C2] DECISION: ...` |
| `ATM.md` | Partitioned by cycle; cross-cycle links explicit | See Compliance Auditor |

### REQUIREMENTS.md Versioning

The requirements file is the single source of truth, but it must track changes across cycles. Add a revision header and per-requirement status:

```markdown
# Requirements (Blueprint)
<!-- Revision: C2 | Date: 2026-02-21 | Human Gate 1: C1 2026-02-10, C2 2026-02-21 -->

## REQ-0001
- **Status:** approved [C1] -- unchanged
- **Requirement:** User shall be able to log in with email and password ...
- **Constraint:** ...
- **Verification Criteria:** ...
- **Done Criteria:** ...

## REQ-0003
- **Status:** modified [C2] -- was: "10ms"; now: "50ms" per CR-0001
- **Requirement:** Sensor reading shall complete within 50ms.
- **Constraint:** ...
- **Verification Criteria:** ...
- **Done Criteria:** ...

## REQ-0010
- **Status:** new [C2]
- **Requirement:** System shall support OTA firmware updates.
- **Constraint:** ...
- **Verification Criteria:** ...
- **Done Criteria:** ...
```

#### Requirement Status Values
- `approved [Cn]` -- approved in Cycle N, unchanged since
- `modified [Cn]` -- changed in Cycle N; include `was: / now:` summary and CR reference
- `new [Cn]` -- introduced in Cycle N
- `deprecated [Cn]` -- removed in Cycle N; retained for traceability, not built or tested
- `superseded [Cn]` -- replaced by another REQ in Cycle N; include reference to successor

### Change Request Protocol

Requirements do not change silently. Every modification between cycles is recorded as a **Change Request (CR)**:

```
## CR-XXXX
- **Cycle:** C2
- **Affected REQ:** REQ-0003
- **Change:** Verification Criteria: "< 10ms" → "< 50ms"
- **Rationale:** Field testing showed 10ms infeasible at 100kHz I2C
- **Impact:** ART-0001 (sensor driver), TC-0003 (latency test), TC-0006 (saturation test)
- **Requested by:** [Human / agent / test result]
- **Approved:** [Human Gate 1, C2]
```

Change Requests are stored in `.agile-v/CHANGE_LOG.md` (append-only). The Requirement Architect creates CRs; the Logic Gatekeeper validates them; the Human approves them at Gate 1.

### Cycle Triggers

A new cycle begins when any of these occur (Human decision required):
1. **New feature request:** Human provides new intent or requirements.
2. **Verification failure:** Red Team Verifier reports FAIL/FLAG items that require requirement changes (not just bug fixes).
3. **Change Request:** An approved CR modifies requirements in a way that invalidates prior artifacts.
4. **Scheduled iteration:** Time-boxed iteration (e.g., sprint boundary).

### Cycle Re-Entry Points

Not every cycle starts from scratch. The re-entry point depends on the trigger:

| Trigger | Re-Entry Stage | What Runs |
|---|---|---|
| New feature request | Stage 1 (Requirements) | Full pipeline for new REQs; regression for unchanged REQs |
| Verification failure requiring REQ change | Stage 1 (Requirements) | CR → Gate 1 → full pipeline for affected REQs; regression for others |
| Bug fix (no REQ change) | Stage 3 (Synthesis) | Build Agent fixes; Red Team re-verifies affected artifacts only |
| Scheduled iteration | Stage 1 (Requirements) | Review all REQs; full pipeline for changes; regression for stable REQs |

### Cycle Archival

When a cycle completes (Human Gate 2 accepted), archive its evidence:

```
.agile-v/
  cycles/
    C1/
      REQUIREMENTS_C1.md        # Frozen snapshot of requirements at C1 completion
      BUILD_MANIFEST_C1.md      # Frozen manifest
      TEST_SPEC_C1.md           # Frozen test specification
      VALIDATION_SUMMARY_C1.md  # Frozen validation summary
      ATM_C1.md                 # Frozen traceability matrix
    C2/
      ...
  REQUIREMENTS.md               # Living document (current cycle)
  BUILD_MANIFEST.md             # Living document (current cycle)
  CHANGE_LOG.md                 # Append-only across all cycles
  DECISION_LOG.md               # Append-only across all cycles
  STATE.md                      # Current cycle state
```

**Archival Rules:**
1. **Freeze on acceptance:** When Human Gate 2 accepts a cycle, snapshot all living documents into `.agile-v/cycles/CN/`.
2. **Never modify archived cycles.** They are read-only evidence for audit.
3. **Living documents continue** in the root `.agile-v/` directory for the next cycle.
4. **Decision Log and Change Log are never archived** -- they are append-only across all cycles, providing a continuous timeline.

### Impact Analysis

Before starting synthesis in a new cycle, every agent must perform impact analysis:

1. **Requirement Architect:** Identify which REQs are `new`, `modified`, `deprecated`, or `unchanged`. Tag each in `REQUIREMENTS.md`.
2. **Logic Gatekeeper:** Re-validate only `new` and `modified` REQs. Unchanged REQs retain their prior validation unless a CR affects their constraints.
3. **Build Agent:** Rebuild only artifacts linked to `new` or `modified` REQs. Unchanged artifacts carry forward with their existing ART-XXXX IDs (no revision bump).
4. **Test Designer:** Generate new TC-XXXX for `new` REQs. Update TC-XXXX for `modified` REQs. Carry forward unchanged TC-XXXX as the **regression baseline**.
5. **Red Team Verifier:** Execute delta tests (new + modified) and regression tests (unchanged). Report both categories separately in the Validation Summary.
6. **Compliance Auditor:** Update the ATM with cycle tags. Flag any `modified` REQ whose linked artifacts or tests have not been updated.