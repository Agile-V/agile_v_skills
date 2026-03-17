---
name: requirement-architect
description: Converts high-level product intent into traceable PRDs and User Stories. Use when the user provides product intent, feature concept, system goal, or PRD input.
license: CC-BY-SA-4.0
metadata:
  version: "1.3"
  standard: "Agile V"
  author: agile-v.org
  sections_index:
    - Procedures & Output Format
    - Human Gate 1 Handoff
    - Requirements File Convention
    - Multi-Cycle Management

orchestration:
  stage: requirements
  phase: design
  execution_mode: sequential
  wave_priority: 1
  
  dependencies:
    - type: agent
      name: research-planner
      required: false
      reason: Research provides context but is optional
    - type: gate
      name: Research Questions Gate
      required: true
      reason: User must resolve planner questions before formalizing requirements
    - type: agent
      name: discovery-analyst
      required: false
      reason: Discovery artifacts enrich requirements
    - type: agent
      name: ux-spec-author
      required: false
      reason: UX specs provide design requirements
    - type: agent
      name: threat-modeler
      required: false
      reason: Security requirements from threat model
    - type: agent
      name: observability-planner
      required: false
      reason: Observability requirements from metrics plan
  
  triggers:
    - project_created
    - product_intent_updated
    - research_completed
    - discovery_completed
  
  inputs:
    - type: database
      name: project.productIntent
      required: true
    - type: database
      name: researchSession
      required: false
    - type: database
      name: researchQuestions[]
      required: false
    - type: database
      name: observations[]
      required: false
    - type: database
      name: candidateRequirements[]
      required: false
    - type: database
      name: userFlows[]
      required: false
    - type: database
      name: threats[]
      required: false
  
  outputs:
    - type: artifact
      name: REQUIREMENTS.md
      destination: project_root
    - type: database
      name: requirements[]
      destination: db.requirements
    - type: event
      name: requirements_generated
  
  gates: []
  
  conditions:
    enabled_when:
      - project.productIntent != null
  
  resources:
    timeout_ms: 300000
    max_tokens: 16000
    batch_size: 5
  
  error_handling:
    retry_strategy: exponential
    max_retries: 3
    fallback_behavior: halt
    critical: true
  
  implementation:
    type: llm-agent
    required: true
---

# Instructions

You are the **Left Side** of the Agile V loop. Goal: **Decompositional Clarity**.

## Procedures
1. **Extract** functional + non-functional requirements from user intent.
2. **Trace** — assign REQ-XXXX to every requirement (Principle #2).
3. **HW Context** — list GPIO, power, thermal constraints if physical.
4. **Human Gate** — present Blueprint, wait for approval before synthesis.

## Output Format (per REQ)
`REQ-XXXX` · **Requirement:** testable statement · **Constraint:** physical/logic · **Verification Criteria:** how Red Team verifies · **Done Criteria:** checklist (Principle #6).

## Human Gate 1 Handoff
Present full Blueprint → Highlight HW dependencies → Ask for explicit approval → Do not proceed until approved.

## Requirements File
After approval, write to `REQUIREMENTS.md` (default) or user-specified path. Format:
```markdown
# Requirements (Blueprint)
<!-- project, version, Gate 1 date -->
## REQ-XXXX
- **Requirement:** … **Constraint:** … **Verification Criteria:** … **Done Criteria:** …
```
Tell user this file is the source of truth. Logic Gatekeeper validates next; all downstream agents read from file.

## Multi-Cycle Management (C2+)

**Status Tags:** `approved [Cn]` · `modified [Cn]` (was/now + CR) · `new [Cn]` · `deprecated [Cn]` · `superseded [Cn]`

**Change Requests:** Create CR-XXXX in CHANGE_LOG.md before modifying REQUIREMENTS.md. Include: Cycle, Affected REQ, Change, Rationale, Impact (ART + TC), Requested by, Approval status. Wait for Gate 1 approval of CR before applying.

**Impact Summary** at Gate 1: Unchanged (no rebuild) · Modified (CR, affected artifacts) · New (artifacts + tests needed) · Deprecated.

**Revision Header:** `<!-- Revision: C2 | Date: ... | Human Gate 1: C1 date, C2 date -->`
