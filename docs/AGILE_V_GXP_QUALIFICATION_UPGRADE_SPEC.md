# Agile V GxP Qualification Upgrade Specification

**Status:** Proposed implementation specification  
**Target repository:** `Agile-V/agile_v_skills`  
**Primary outcome:** Make Agile V a substantially stronger, more precise, and more defensible framework for risk-based computerized-system assurance, including DQ, IQ, OQ, PQ, intended-use validation, requalification, supplier evidence, and controlled release.  
**Repository boundary:** Markdown Agent Skills, schemas, templates, behavioral contracts, fixtures, and documentation. No executable runtime enforcement is added to this repository.

---

## 1. Executive decision

Agile V should not map individual agents directly to qualification stages.

Remove or supersede this mapping wherever it appears:

```text
Logic Gatekeeper = DQ
Build Agent = IQ
Test Designer = OQ
Red Team Verifier = PQ
```

It is technically misleading.

Use this evidence-based model instead:

```text
Approved intended use and URS
        |
        v
Design Qualification (DQ)
Independent evidence that the proposed design satisfies the approved URS,
applicable quality/data-integrity controls, and controlled design constraints.
        |
        v
Installation Qualification (IQ)
Evidence that the approved software, infrastructure, configuration, interfaces,
security settings, and supporting components are installed as specified.
        |
        v
Operational Qualification (OQ)
Requirement-derived evidence that the installed system operates as designed,
including negative, boundary, error, security, data-integrity, and worst-case tests.
        |
        v
Performance Qualification (PQ)
Evidence that the qualified system supports its approved intended use under
representative operating conditions, users, workflows, data, volume, and controls.
        |
        v
Qualification Summary and authorized release
```

Agents contribute evidence to these stages. They are not themselves the stages.

The preferred architecture is:

```text
agile-v-gxp-qualification
    -> plans and coordinates qualification
    -> defines stage contracts and stop conditions
    -> records tailoring and stage release

requirement-architect
    -> creates approved intended use and URS-like requirements

logic-gatekeeper
    -> independently challenges requirement ambiguity and testability
    -> does not claim DQ completion

independent DQ review mode
    -> evaluates design against approved requirements and regulated constraints

build-agent
    -> produces controlled artifacts and installation inputs
    -> does not claim IQ completion

test-designer
    -> independently designs OQ-oriented tests from the approved baseline

red-team-verifier
    -> reviews IQ evidence and executes/challenges OQ evidence
    -> does not claim PQ completion

validation-agent
    -> plans and assesses PQ/intended-use validation in representative conditions

compliance-auditor
    -> audits the qualification chain and creates the summary package

release-manager
    -> releases only after required stage decisions are complete
```

---

## 2. Why this change is needed

Agile V already has strong foundations:

- persisted, approved, and frozen requirements;
- independent requirement findings;
- implementation only from a controlled baseline;
- independent test design;
- separation between builder and verifier;
- intended-use validation separated from verification;
- typed traceability;
- deviations, CAPA, change control, and periodic revalidation;
- durable Human Gates;
- risk-scaled evidence;
- AI-run provenance.

The main gaps are not the basic lifecycle. They are qualification semantics, installation/configuration evidence, regulated packaging, supplier evidence, role qualification, stage release, and technical enforcement boundaries.

The upgrade must solve these problems:

1. **DQ is not currently a distinct independent design review.** Requirement quality review is not design qualification.
2. **IQ is not currently represented as a coherent installation/configuration baseline and protocol.** Building software is not installation qualification.
3. **OQ is strong in substance but lacks explicit qualification metadata and execution controls.**
4. **PQ is conceptually supported by `validation-agent`, but the qualification relationship is not explicit or packaged consistently.**
5. **Existing GxP documentation is partly stale.** It still describes validation as missing or conflated even though a dedicated `validation-agent` now exists.
6. **Skill instructions and schemas are sometimes described too confidently.** A Markdown contract is not operational compliance, technical enforcement, or certification.
7. **Qualification of the target system and qualification of the Agile V toolchain are conflated.** These must be separate scopes.
8. **Requalification triggers are too focused on AI runtime changes and do not yet cover the full system/configuration lifecycle.**
9. **Protocol integrity is not explicit enough.** Approved test criteria must not be silently edited after execution starts.
10. **Part 11, Annex 11, identity, signatures, audit-trail integrity, and retention require external runtime and organizational controls.** Skills cannot provide these controls by themselves.

---

## 3. Normative terminology

Add the following terminology contract to the new profile and relevant documentation.

| Term | Agile V meaning |
|---|---|
| **User Requirements Specification (URS)** | Controlled, approved, and baselined requirements describing intended use, essential quality, data-integrity, security, interface, operational, and regulatory needs. |
| **Qualification** | Documented evidence that a defined subject, baseline, installation, configuration, or operating stage satisfies predefined criteria. |
| **Verification** | Evidence that specified outputs were built correctly against approved requirements. |
| **Validation** | Evidence that the right system supports its approved intended use in representative conditions. |
| **DQ** | Independent review that the proposed design satisfies the approved URS and applicable design constraints. |
| **IQ** | Evidence that the system and supporting components are installed and configured as specified. |
| **OQ** | Evidence that the installed system operates as designed throughout the required functional and risk-relevant operating range. |
| **PQ** | Evidence that the qualified system performs acceptably for intended use under representative operational conditions. |
| **IOQ** | A justified combined IQ/OQ execution in which installation and operational criteria remain separately identifiable. |
| **Process validation** | Validation of a manufacturing or business process. It is not automatically established by software PQ. |
| **Computerized-system validation** | The broader lifecycle assurance that the system is fit for intended use and remains in a controlled state. |
| **Qualification subject** | The exact item being qualified: target system, deployment environment, assurance toolchain, interface, migration, infrastructure component, or supplier service. |

Rules:

1. Never use verification and validation as synonyms.
2. Never claim that a Red Team verification report is PQ evidence by itself.
3. Never claim that the Build Agent performed IQ merely because it produced deployable software.
4. Never claim that a valid schema establishes regulatory compliance.
5. Never claim that a passing qualification package certifies an organization, product, or quality system.
6. PQ terminology may be mapped to intended-use validation only when the organization's approved procedure defines that mapping.
7. A software PQ does not establish pharmaceutical process validation unless the process-specific evidence also exists.

---

## 4. Regulatory and guidance baseline

The implementation should be designed against the following public baseline without reproducing copyrighted standards text:

- EudraLex Volume 4, Annex 15, Qualification and Validation, in operation since 1 October 2015.
- Current applicable EudraLex Annex 11 requirements and the official revised Annex 11 consultation draft as a future-readiness input only; the draft is not final law or final GMP guidance.
- FDA Computer Software Assurance for Production and Quality Management System Software, final guidance, February 2026, within its stated scope.
- 21 CFR Part 11 where applicable to electronic records and signatures.
- GAMP 5 Second Edition principles as locally licensed and interpreted by the regulated organization.
- Applicable organizational SOPs, quality agreements, validation master plans, policies, and sector rules.

Source anchors for implementation review:

| Source | Relevant anchors | Use in this specification |
|---|---|---|
| EudraLex Volume 4, Annex 15 | Sections 1-4; especially 2.4-2.10 and 3.2-3.14 | Lifecycle planning, approved protocols, deviations, stage release, URS, DQ, IQ, OQ, PQ, and requalification |
| Revised Annex 11 consultation draft | Sections 6 and 9; installation/configuration, evidence, traceability, negative/boundary testing, backup restore, security, and periodic review | Future-readiness and computerized-system detail; not treated as final requirements until adopted |
| FDA CSA final guidance, February 2026 | Risk-based assurance and testing rigor within stated production/QMS software scope | Lean, risk-proportionate assurance profile and evidence selection |
| 21 CFR Part 11 | Applicable electronic-record and electronic-signature controls | External identity, signature, record-integrity, and closed-system requirements |
| GAMP 5 Second Edition | Locally licensed lifecycle and risk-based assurance guidance | Organizational tailoring and terminology; do not reproduce licensed text |

The documentation MUST state:

```text
This Agile V profile supports structured qualification and validation evidence.
It does not determine legal applicability, replace controlled procedures,
provide technical Part 11 controls, or establish regulatory compliance.
```

---

## 5. Architecture: a qualification profile, not four new build agents

Create one new draft skill:

```text
agile-v-gxp-qualification/
└── SKILL.md
```

Suggested frontmatter:

```yaml
---
name: agile-v-gxp-qualification
description: Plans, coordinates, and audits risk-based DQ, IQ, OQ, PQ, intended-use validation, stage release, and requalification for regulated or high-assurance computerized systems. Use with Agile V lifecycle skills; it does not provide certification or runtime enforcement.
license: CC-BY-SA-4.0
metadata:
  version: "0.1"
  status: draft
  standard: "Agile V"
  author: agile-v.org
  sections_index:
    - Purpose and Boundaries
    - Qualification Applicability
    - Qualification Subjects
    - Planning and Tailoring
    - DQ
    - IQ and IOQ
    - OQ
    - PQ and Intended-Use Validation
    - Deviations and Stage Release
    - Requalification
    - Toolchain Qualification
    - Halt Conditions
---
```

The skill is a profile and coordinator. It MUST NOT:

- generate production code;
- approve its own evidence;
- replace `requirement-architect`;
- replace `test-designer`;
- replace `red-team-verifier`;
- replace `validation-agent`;
- issue a compliance or certification claim;
- assume every regulated system requires identical document volume;
- force DQ/IQ/OQ/PQ terminology where an approved local procedure uses a different but equivalent lifecycle.

---

## 6. Four-layer assurance model

All GxP documentation should distinguish these layers:

| Layer | What Agile V provides | What it does not prove |
|---|---|---|
| **Normative skill layer** | Role boundaries, procedures, stop conditions, handoffs | That an agent obeyed the instructions |
| **Evidence-contract layer** | Schemas, templates, typed records, required metadata | That the recorded facts are true |
| **Enforcement layer** | Contract expectations for CI, hooks, identity, signing, and gates | Enforcement unless a consuming runtime implements it |
| **Operational assurance layer** | Pilot protocols, audits, reference challenges, metrics | Effectiveness unless operated and evaluated in context |

Replace simplistic labels such as `COMPLIANT` in public matrices where they are based only on skill wording.

Recommended coverage labels:

```text
NOT ADDRESSED
NORMATIVE CONTRACT
SCHEMA-BACKED
RUNTIME-ENFORCED
OPERATIONALLY EVIDENCED
EXTERNALLY ASSESSED
```

A requirement should only be described at the highest level supported by actual evidence.

---

## 7. Qualification subjects

Every qualification plan and protocol MUST identify the subject.

Allowed `subject_type` values:

```text
target_system
assurance_toolchain
deployment_environment
infrastructure_component
interface
data_migration
supplier_service
operational_process
other
```

Examples:

```text
Target system:
Laboratory result review application release 4.7.1

Assurance toolchain:
Agile V skills 3.9.x + host runtime + selected model + connectors + policy

Deployment environment:
GMP-PROD-01 Kubernetes cluster and controlled configuration

Data migration:
LIMS schema v5 to v6 production migration process
```

Do not combine different qualification subjects into one conclusion unless the scope and evidence for each subject remain explicit.

---

## 8. Installation profiles

Add qualification-oriented profiles to `docs/INSTALL_PROFILES.md` without replacing existing profiles.

### 8.1 `gxp-lean-csa`

Use for lower-risk, configurable, or well-understood software where approved local procedures permit a lean risk-based approach.

Minimum components:

```text
agile-v-core
agile-v-gxp-qualification
agile-v-control-matrix
agile-v-compliance
requirement-architect
logic-gatekeeper
test-designer
red-team-verifier
validation-agent
compliance-auditor
release-manager
```

Expected evidence:

- intended use and approved requirements;
- documented risk assessment;
- controlled system/configuration baseline;
- targeted installation/configuration checks;
- requirement-derived testing;
- representative intended-use evidence where applicable;
- deviations and authorized release.

### 8.2 `gxp-standard`

Use for regulated computerized systems requiring explicit DQ/IQ/OQ/PQ packaging.

Adds:

- system description;
- qualification plan;
- DQ report;
- IQ or IOQ protocol and report;
- OQ protocol and report;
- PQ/intended-use validation plan, protocol, and report;
- qualification summary report;
- supplier suitability assessment;
- requalification strategy.

### 8.3 `gxp-high-assurance`

Use for L4, safety-relevant, high data-integrity risk, externally assured, or critical operational systems.

Adds:

- independent quality approval;
- stronger role separation;
- signed and integrity-protected records in the consuming environment;
- independently anchored evidence;
- recovery demonstration;
- witnessed or independently reviewed critical executions;
- supplier and service-continuity evidence;
- periodic review and requalification evidence;
- reference fault-injection or seeded-defect challenge where feasible.

---

## 9. Core qualification artifacts

Create these reusable templates under `templates/agile-v/` and matching schemas under `schemas/`.

### 9.1 Required core artifacts

```text
QUALIFICATION_PLAN.example.yaml
SYSTEM_DESCRIPTION.example.yaml
SYSTEM_BASELINE.example.yaml
QUALIFICATION_PROTOCOL.example.yaml
QUALIFICATION_EXECUTION.example.yaml
QUALIFICATION_DEVIATION.example.yaml
QUALIFICATION_SUMMARY.example.yaml
REQUALIFICATION_ASSESSMENT.example.yaml
```

Matching schemas:

```text
QUALIFICATION_PLAN.schema.json
SYSTEM_DESCRIPTION.schema.json
SYSTEM_BASELINE.schema.json
QUALIFICATION_PROTOCOL.schema.json
QUALIFICATION_EXECUTION.schema.json
QUALIFICATION_DEVIATION.schema.json
QUALIFICATION_SUMMARY.schema.json
REQUALIFICATION_ASSESSMENT.schema.json
```

### 9.2 Optional supporting artifacts

```text
SUPPLIER_SUITABILITY.example.yaml
TRAINING_QUALIFICATION.example.yaml
PERIODIC_REVIEW.example.yaml
```

Matching schemas may be added when the artifacts become normative.

### 9.3 Human-readable rendering

Machine-readable YAML records SHOULD be rendered into human-readable Markdown reports where useful:

```text
DQ_REPORT.md
IQ_REPORT.md
OQ_REPORT.md
PQ_REPORT.md
QUALIFICATION_SUMMARY_REPORT.md
```

The YAML record remains the machine-checkable source. The Markdown report is the reviewable narrative view.

---

## 10. Qualification plan contract

Suggested minimum structure:

```yaml
schema_version: "1.0"
plan_id: "QPLAN-0001"
subject:
  subject_type: "target_system"
  name: "Laboratory Result Review System"
  system_id: "SYS-0007"
  version_scope: "4.7.x"
regulatory_context:
  gxp_applicable: true
  part_11_applicable: "to-be-determined"
  annex_11_applicable: true
  local_procedure_refs: []
intended_use_ref: ".agile-v/REQUIREMENTS.md#REQ-0001"
system_description_ref: ".agile-v/qualification/SYSTEM_DESCRIPTION.yaml"
risk_refs:
  - "RISK-0012"
strategy:
  approach: "gxp-standard"
  stages_required:
    - "DQ"
    - "IQ"
    - "OQ"
    - "PQ"
  combined_stages: []
  supplier_evidence_reuse: "controlled"
  qualification_of_toolchain_required: true
roles:
  system_owner: "role-ref"
  quality_owner: "role-ref"
  protocol_author: "role-ref"
  executor: "role-ref"
  reviewer: "role-ref"
  approver: "role-ref"
independence:
  builder_may_approve: false
  protocol_author_may_execute: true
  independent_review_required_from: "L3"
evidence_controls:
  authoritative_repository: "controlled-system-ref"
  retention_ref: "policy-ref"
  signature_ref: "signature-policy-ref"
  hash_required: true
stage_release:
  conditional_release_allowed: true
  conditional_release_authority: "quality-owner"
requalification:
  periodic_review_interval_months: 12
  trigger_policy_ref: ".agile-v/qualification/REQUALIFICATION_POLICY.yaml"
status: "draft"
approval_ref: null
```

Rules:

1. The plan MUST be approved before executing controlled qualification protocols.
2. The plan MUST identify which stages are required and why.
3. Omitted stages require a documented, risk-based rationale.
4. Combined IOQ is permitted only when IQ and OQ criteria remain separately traceable.
5. Supplier evidence reuse must identify exact version, scope, provenance, local configuration delta, and suitability review.
6. The qualification plan does not replace an organizational Validation Master Plan where one is required.

---

## 11. System description contract

`SYSTEM_DESCRIPTION` should capture the stable context required for qualification.

Minimum content:

```text
system identity and version scope
approved intended use
GxP/business process supported
system boundary
components and deployment topology
configured and customized functionality
user types and roles
records and data handled
data classifications
data flows and interfaces
calculation or decision functions
audit-trail scope
electronic-signature scope
backup, restore, archive, and retention design
availability and recovery expectations
security boundaries
supplier and service dependencies
operating environments
known exclusions
```

The system description MUST distinguish:

```text
standard functionality
configured functionality
custom functionality
external service functionality
manual procedural controls
```

This distinction is needed to select proportionate evidence and understand supplier evidence reuse.

---

## 12. System baseline contract

Create a controlled `SYSTEM_BASELINE` record for every IQ/OQ/PQ execution.

Minimum fields:

```yaml
baseline_id: "BASELINE-QUAL-0001"
subject_id: "SYS-0007"
application:
  release: "4.7.1"
  source_commit: "commit-sha"
  artifact_digest: "sha256:..."
  build_manifest_ref: ".agile-v/BUILD_MANIFEST.md"
environment:
  environment_id: "GMP-VAL-01"
  infrastructure_ref: "iac-or-controlled-record"
  infrastructure_digest: "sha256:..."
platform:
  operating_system: "value"
  runtime: "value"
  database: "value"
  container_images: []
configuration:
  configuration_ref: "controlled-config-ref"
  configuration_digest: "sha256:..."
  secret_values_recorded: false
interfaces: []
dependencies:
  sbom_ref: "sbom-ref"
  approved_versions: true
security:
  supported_platforms: true
  patch_status_ref: "patch-evidence-ref"
  identity_configuration_ref: "iam-evidence-ref"
  time_sync_ref: "time-source-ref"
backup_restore:
  configuration_ref: "backup-config-ref"
  last_restore_test_ref: "restore-test-ref"
calibration:
  applicable: false
  evidence_refs: []
captured_at: "ISO-8601"
captured_by: "identity-ref"
review_status: "pending"
```

Rules:

- Never record secret values in qualification evidence.
- Record hashes, identifiers, and controlled references instead.
- The same baseline reference must be used across protocol execution and reports.
- Any baseline drift during execution MUST halt or create an approved deviation and impact assessment.

---

## 13. Protocol integrity and lifecycle

Qualification protocols MUST have a controlled lifecycle:

```text
draft
  -> reviewed
  -> approved
  -> executing
  -> completed
  -> stage_released

or

executing
  -> blocked
  -> deviation_open
  -> resumed
  -> completed

or

any controlled state
  -> rejected
  -> superseded through a new revision
```

Rules:

1. Test steps, prerequisites, expected results, and acceptance criteria MUST be approved before execution.
2. An approved protocol MUST NOT be silently edited in place.
3. A change to acceptance criteria or a material test method requires a new revision and approval.
4. Execution failure MUST remain visible even if a later rerun passes.
5. Repeated execution until PASS without preserving the original failure is prohibited.
6. Every rerun must reference the original execution, deviation, corrective action, and approved rationale.
7. `INCONCLUSIVE`, `BLOCKED`, and `NOT RUN` are valid outcomes and MUST NOT be converted to PASS.
8. A test-level waiver requires authorized evidence and cannot be self-issued by an agent.
9. Stage-level conditional release requires an explicit impact assessment and authorized decision.
10. Protocol and execution records SHOULD include cryptographic digests in the consuming runtime.

Allowed test outcomes:

```text
NOT_RUN
PASS
FAIL
BLOCKED
INCONCLUSIVE
DEVIATION
WAIVED
```

Allowed stage outcomes:

```text
NOT_STARTED
IN_PROGRESS
PASS
FAIL
CONDITIONALLY_ACCEPTED
REJECTED
SUPERSEDED
```

---

## 14. Qualification protocol structure

Suggested minimum structure:

```yaml
schema_version: "1.0"
protocol_id: "OQ-0007"
revision: "1"
stage: "OQ"
subject_ref: "SYS-0007"
plan_ref: "QPLAN-0001"
baseline_ref: "BASELINE-QUAL-0001"
requirements:
  - requirement_id: "REQ-0012"
    revision: "rev-3"
    baseline_id: "BASELINE-REQ-0004"
risk_refs:
  - "RISK-0012"
preconditions:
  - id: "PRE-001"
    statement: "IQ stage released"
    evidence_ref: "IQ-RPT-0003"
roles:
  author: "identity-ref"
  executor: "identity-ref"
  reviewer: "identity-ref"
  approver: "identity-ref"
test_cases:
  - test_id: "TC-0042"
    title: "Reject unauthorized result release"
    type: "negative"
    qualification_stage: "OQ"
    gxp_critical: true
    requirement_refs:
      - "REQ-0012@rev-3"
    risk_refs:
      - "RISK-0012"
    prerequisites: []
    input_data_refs:
      - "TESTDATA-0003"
    steps:
      - step: 1
        action: "Authenticate as a role without release authority"
        expected: "Authentication succeeds with restricted role"
      - step: 2
        action: "Attempt to release a result"
        expected: "Release is denied and the attempt is audit-trailed"
    acceptance_criteria:
      - "No result status changes"
      - "Audit event records actor, time, action, and outcome"
    evidence_required:
      - "execution log"
      - "audit-trail extract"
approval:
  status: "pending"
  approval_ref: null
```

---

## 15. Qualification execution structure

Every executed step should record observable results rather than a bare PASS.

Minimum fields:

```yaml
execution_id: "EXEC-OQ-0007-01"
protocol_id: "OQ-0007"
protocol_revision: "1"
baseline_ref: "BASELINE-QUAL-0001"
started_at: "ISO-8601"
ended_at: "ISO-8601"
executor:
  identity_ref: "identity-ref"
  role: "qualification-executor"
witness:
  required: false
  identity_ref: null
environment_ref: "GMP-VAL-01"
test_case_results:
  - test_id: "TC-0042"
    result: "PASS"
    step_results:
      - step: 1
        actual: "Authenticated as QC_VIEWER"
        result: "PASS"
        evidence_refs:
          - "evidence/auth-log-0042.txt"
      - step: 2
        actual: "HTTP 403; result remained REVIEWED; audit event AT-8891 created"
        result: "PASS"
        evidence_refs:
          - "evidence/request-response-0042.txt"
          - "evidence/audit-event-AT-8891.json"
    deviation_refs: []
evidence_integrity:
  digest_algorithm: "sha256"
  evidence_digests: []
review:
  status: "pending"
  reviewer_ref: null
```

Rules:

- Each critical test must preserve expected versus actual behavior.
- Evidence locators must resolve to controlled records.
- Screenshots may supplement but should not replace machine-readable evidence where such evidence exists.
- AI-generated summaries are not raw execution evidence.
- Hidden chain-of-thought must never be stored.

---

## 16. Design Qualification (DQ)

DQ MUST be a distinct independent review of the proposed design.

### 16.1 Inputs

Required inputs:

```text
approved intended use
approved and baselined URS/requirements
system description
controlled design/architecture records
interface specifications
data-flow and record-flow description
risk assessment
security and data-integrity requirements
supplier/configuration information
applicable local procedures
```

### 16.2 DQ questions

The independent DQ review should determine whether:

- every critical requirement is represented in the design;
- system boundaries and responsibilities are clear;
- configured versus customized behavior is identified;
- data flows and interfaces preserve data integrity;
- access-control and segregation-of-duty requirements are designed;
- audit trails and record retention are designed where required;
- calculations, decisions, and release controls are specified;
- backup, restore, archive, and disaster-recovery mechanisms are designed;
- failures, alarms, degraded modes, and recovery behavior are defined;
- security boundaries and supplier dependencies are addressed;
- testability and observability are sufficient for IQ/OQ/PQ;
- the design introduces undocumented GMP or operational risks;
- human procedures are being used to compensate for technical gaps and whether that is justified;
- the design remains consistent with the approved intended use.

### 16.3 Independence

The Build Agent MUST NOT approve DQ for its own proposed design.

For L3/L4 or locally regulated use:

```text
DQ reviewer context != builder implementation context
DQ approval authority != builder identity
```

A domain expert, system owner, quality reviewer, safety engineer, security reviewer, or independent agent may contribute, but accountable human approval remains required where policy says so.

### 16.4 DQ output

Create a stage report containing:

```text
design scope and revision
requirements reviewed
risk and control coverage
findings and severity
unresolved assumptions
required design changes
verification strategy impact
qualification feasibility
final DQ recommendation
human approval reference
```

A DQ PASS means only that the reviewed design is acceptable against the stated scope and evidence. It does not qualify the installation or operation.

---

## 17. Installation Qualification (IQ)

IQ MUST verify the installed and configured system before operational testing.

### 17.1 Minimum software IQ checks

Select risk-relevant checks from this catalog:

```text
application version and artifact digest
source/build/artifact identity linkage
deployment target identity
operating system and platform version
runtime and database version
container image identities
infrastructure-as-code version and drift status
configuration baseline and digest
feature flags and configured functionality
custom modules and plugins
supported-version status
security patch status
SBOM/dependency inventory
license or approval status where applicable
certificates and trust stores
identity provider integration
service accounts and technical users
time synchronization
locale and time-zone configuration
audit-trail configuration
logging and retention configuration
backup configuration
restore prerequisites
archive configuration
monitoring and alarm configuration
interface endpoints and versions
network and firewall configuration
data-storage locations
data migration baseline and checksums
operating instructions and maintenance references
calibration status for connected measuring equipment
```

### 17.2 IQ evidence rules

- IQ must execute against a named `SYSTEM_BASELINE`.
- The protocol must distinguish installation, configuration, and calibration checks.
- Supplier installation records may be reused only after suitability review.
- A clean deployment is not evidence of correct configuration unless criteria and results are recorded.
- Configuration defaults must not be assumed.
- Unsupported platforms or unresolved critical patch status must block stage release unless a documented, authorized risk decision exists.
- Environment drift between IQ and OQ must be detected or reassessed.

### 17.3 Combined IOQ

IOQ is allowed when justified.

The combined protocol MUST retain:

```text
IQ-specific prerequisites and results
OQ-specific functional results
separate stage conclusions
traceability to installation criteria and operational criteria
```

A combined file must not make installation evidence indistinguishable from functional evidence.

---

## 18. Operational Qualification (OQ)

Agile V already has a strong OQ foundation through `test-designer` and `red-team-verifier`.

The upgrade should make that relationship explicit.

### 18.1 Test design

`test-designer` MUST continue to design tests from approved, baselined requirements and referenced controlled constraints, not from implementation behavior.

Add optional qualification metadata:

```text
qualification_stage: OQ
gxp_critical: true|false
risk_refs
system_baseline_ref
required_precondition_stage: IQ|IOQ
```

### 18.2 OQ test catalog

Select according to risk and intended use:

```text
positive functional behavior
negative behavior
boundary values
upper and lower operating limits
worst-case conditions
error handling
alarms and warnings
retry and timeout behavior
concurrency and duplicate processing
calculations and rounding
data-input validation
data transfer and interfaces
data migration
access control
segregation of duties
least privilege
unique-account behavior
audit-trail generation and protection
electronic-signature behavior where applicable
record creation, modification, review, and release
report generation
search, sort, export, and retrieval
backup and restore
archive and retrieval
failover and recovery
performance and capacity
availability
security and abuse cases
prompt/tool/delegation security for agentic functionality
```

### 18.3 OQ execution

`red-team-verifier` should:

- verify IQ/IOQ preconditions and baseline identity;
- execute approved OQ tests;
- design additional independent challenge tests when allowed;
- preserve failures and deviations;
- map every result to requirements, risks, protocol revision, baseline, and evidence;
- block OQ release on unresolved critical failures;
- avoid performing intended-use acceptance.

The Red Team MUST state:

```text
OQ verifies operation against specification.
It does not establish PQ or intended-use acceptance.
```

---

## 19. Performance Qualification (PQ) and intended-use validation

Use `validation-agent` as the primary PQ/intended-use evidence role.

The profile MUST not claim that all intended-use validation is automatically called PQ. It should provide an approved mapping where the organization's procedure uses PQ terminology.

### 19.1 PQ prerequisites

Unless an approved strategy justifies a combined approach:

```text
DQ stage acceptable
IQ or IOQ stage acceptable
OQ stage acceptable
release candidate/system baseline identified
approved SOPs available
representative users or roles identified
representative environment/configuration/data defined
open critical anomalies resolved
residual-risk authority identified
```

### 19.2 Representative conditions

PQ should explicitly define:

```text
representative user roles and qualification
representative business/GxP workflow
representative environment
representative configuration
representative production-like data
qualified substitute or simulated data rationale
normal volume and workload
peak or worst-case volume where relevant
operating range
external interfaces
SOPs and procedural controls
support and escalation model
monitoring and alarms
backup/recovery expectations
foreseeable misuse
```

### 19.3 PQ test catalog

Use risk-relevant scenarios such as:

```text
end-to-end intended-use workflow
routine operation by representative users
role transitions and approvals
record review and release
production-like data volume
peak load and queue depth
repeatability across multiple runs
long-running process behavior
shift/day/time-zone changes
interface availability and delayed messages
failover and recovery
backup restoration in representative conditions
operational alarm response
contingency procedure use
SOP usability
known misuse or error scenarios
record retention and retrieval
support handoff and incident escalation
```

### 19.4 PQ execution record

Each PQ execution should capture:

```text
actual system baseline
actual environment
actual data set/version
participant role or operator qualification reference
scenario
expected outcome
observed outcome
operational timing
anomalies
deviations
limitations
residual risk
acceptance decision authority
```

### 19.5 PQ conclusion

Allowed conclusions:

```text
ACCEPTED FOR INTENDED USE
CONDITIONALLY ACCEPTED WITH RESTRICTIONS
NOT ACCEPTED FOR INTENDED USE
EVIDENCE INSUFFICIENT
```

An AI agent MUST NOT self-authorize residual-risk acceptance or intended-use release.

---

## 20. Qualification of the Agile V assurance toolchain

Separate the qualification of the target system from the qualification of the Agile V toolchain used to generate or assess evidence.

### 20.1 Toolchain subject

A toolchain qualification scope may include:

```text
Agile V skill repository version and commit
installed skill profile
host agent/runtime
model/provider/model version
connector and tool inventory
policy and control matrix
schemas and validators
prompt/context sources
identity and approval integration
logging and evidence storage
CI/hooks/runtime enforcement
```

Do not claim that a generic model is globally validated.

Qualify the controlled human-agent configuration for defined uses and limits.

### 20.2 Toolchain IQ

Verify:

```text
correct skill directories installed
skill versions and commit hashes recorded
schemas/templates match the approved profile
runtime and model identity recorded
allowed tools and permissions configured
control matrix active
logging and evidence paths configured
identity and approval mechanisms connected
required hooks/CI checks installed where applicable
```

### 20.3 Toolchain OQ

Execute reference behavioral contracts:

```text
halts on missing baseline
rejects ambiguous requirements
prevents builder self-verification
requires independent test design
rejects malformed evidence
blocks unauthorized gates in the consuming runtime
records AI provenance
preserves failed test history
detects traceability gaps
detects out-of-scope changes
enforces forbidden tool policy where runtime support exists
```

### 20.4 Toolchain PQ

Run a production-representative pilot project using the controlled toolchain.

The pilot should include seeded conditions such as:

```text
ambiguous requirement
missing critical requirement
incorrect implementation
builder-written inadequate test
correlated verifier error
unexpected scope expansion
forged or incomplete provenance
failed rollback prerequisite
unrepresentative PQ data
unauthorized approval
```

Measure:

```text
unsafe acceptance rate
correct acceptance rate
defect detection rate
traceability completeness
evidence retrieval success
review time
false alarm rate
recovery success
recovery time
human confidence calibration
```

The qualification conclusion must stay bounded to the tested configuration, task classes, model/runtime versions, and evidence.

---

## 21. Supplier and external evidence reuse

Create an optional `SUPPLIER_SUITABILITY` record or integrate equivalent fields into the qualification plan.

Minimum review areas:

```text
supplier identity and service
criticality and intended use
version and configuration scope
quality/security evidence reviewed
service availability and support
change-notification process
incident and vulnerability process
data handling and residency
subprocessor dependencies
backup and continuity commitments
export and exit strategy
vendor test evidence and limitations
local configuration delta
local acceptance tests required
reviewer and approval
```

Rules:

1. Supplier certifications are evidence inputs, not proof that the configured local use is qualified.
2. Vendor protocols must be reviewed for suitability against the implemented version and local process.
3. Supplier evidence reuse must record what is reused, what is repeated, and what remains untested.
4. SaaS and model-provider changes must feed change control and requalification assessment.
5. Supplier evidence supplied by an AI agent must retain source and version provenance.

---

## 22. Deviations, anomalies, CAPA, and reruns

Use existing Agile V deviation and CAPA mechanisms, but add qualification-specific records.

`QUALIFICATION_DEVIATION` minimum fields:

```text
deviation ID
protocol and execution reference
stage
subject and baseline
what differed from the approved protocol
when detected
immediate containment
impact on product quality, patient safety, data integrity, and intended use
root-cause requirement
corrective action
retest requirement
scope of affected evidence
approver/disposition
closure evidence
```

Rules:

- A protocol deviation is not a convenient method for post-hoc acceptance-criteria changes.
- A failed result must remain in the record.
- Re-execution requires a controlled rationale.
- Critical or recurring deviations should trigger CAPA according to `agile-v-compliance`.
- A validation deviation does not close a failed verification result.
- Open deviations must be summarized in the qualification summary.

---

## 23. Stage release

Each stage requires an explicit release decision before the next stage when the approved strategy requires sequencing.

Minimum stage release evidence:

```text
stage and subject
protocol/report revisions
baseline
acceptance criteria status
deviations and anomalies
unresolved actions
risk assessment
conditions or restrictions
release decision
authorized approver
timestamp and signature reference
```

Conditional release is allowed only when:

- the responsible authority explicitly approves it;
- the impact on product quality, patient safety, data integrity, and the next stage is assessed;
- conditions and due dates are recorded;
- outstanding items remain visible;
- the consuming runtime can prevent silent final release while conditions remain open.

An agent may recommend but MUST NOT authorize conditional release.

---

## 24. Qualification summary report

The Compliance Auditor should generate a qualification summary package containing:

```text
1. System and qualification subject
2. Intended use and scope
3. Regulatory/local procedure context
4. Qualification strategy and tailoring
5. System baseline and configuration
6. Risk assessment summary
7. DQ status and findings
8. IQ/IOQ status and findings
9. OQ status and findings
10. PQ/intended-use validation status and findings
11. Traceability completeness
12. Deviations and anomalies
13. CAPAs
14. Supplier evidence and limitations
15. Data-integrity and security evidence
16. Training/role evidence where required
17. Open actions and restrictions
18. Residual risks and acceptance authority
19. Requalification triggers
20. Final conclusion and release decision
```

The report MUST distinguish:

```text
PASSING TESTS
STAGE ACCEPTANCE
INTENDED-USE ACCEPTANCE
REGULATORY/QUALITY RELEASE AUTHORITY
```

These are not interchangeable.

---

## 25. Traceability model

Extend `TRACE_GRAPH` only after inspecting existing node and relation conventions.

Recommended new node types:

```text
qualification_plan
system_description
system_baseline
qualification_protocol
qualification_execution
qualification_deviation
qualification_report
qualification_summary
requalification_assessment
```

Recommended relations:

```text
qualification_plan -> governs -> qualification_subject
system_baseline -> identifies -> qualification_subject
qualification_protocol -> executes_against -> system_baseline
qualification_protocol -> qualifies -> qualification_subject
qualification_execution -> executes -> qualification_protocol
qualification_execution -> produces -> evidence
qualification_deviation -> deviates_from -> qualification_protocol|execution
qualification_report -> reports_on -> qualification_execution
approval -> releases -> qualification_stage
requalification_assessment -> evaluates_change_to -> system_baseline
```

Continue existing lineage:

```text
test_case -> verifies -> baselined requirement
artifact -> implements -> baselined requirement
verification -> evaluates -> artifact|test_case
claim -> supported_by -> evidence|verification|validation
```

Do not force all qualification artifacts under a generic REQ link.

Every synthesis and test link must retain requirement revision and baseline identity.

---

## 26. Evidence bundle integration

Extend `EVIDENCE_BUNDLE.schema.json` with an optional `qualification` section.

Suggested structure:

```yaml
qualification:
  applicable: true
  plan_ref: ".agile-v/qualification/QUALIFICATION_PLAN.yaml"
  subject_ref: "SYS-0007"
  baseline_ref: "BASELINE-QUAL-0001"
  stages:
    DQ:
      required: true
      status: "PASS"
      report_ref: "DQ_REPORT.md"
      approval_ref: "GATE-DQ-0001"
    IQ:
      required: true
      status: "PASS"
      report_ref: "IQ_REPORT.md"
      approval_ref: "GATE-IQ-0001"
    OQ:
      required: true
      status: "PASS"
      report_ref: "OQ_REPORT.md"
      approval_ref: "GATE-OQ-0001"
    PQ:
      required: true
      status: "PASS"
      report_ref: "PQ_REPORT.md"
      approval_ref: "GATE-PQ-0001"
  deviations: []
  summary_ref: "QUALIFICATION_SUMMARY_REPORT.md"
  requalification_assessment_ref: null
```

The schema should remain backward-compatible when qualification is not applicable.

Semantic tests should require the section when the resolved control matrix says qualification is required.

---

## 27. Control matrix extension

Extend `agile-v-control-matrix/SKILL.md`, `schemas/CONTROL_MATRIX.schema.json`, and both control-matrix templates with an optional qualification policy.

Suggested structure:

```yaml
qualification:
  enabled: true
  profile: "gxp-standard"
  subject_types:
    - "target_system"
    - "assurance_toolchain"
  stages_required:
    L0: []
    L1: []
    L2:
      - "IQ"
      - "OQ"
    L3:
      - "DQ"
      - "IQ"
      - "OQ"
      - "PQ"
    L4:
      - "DQ"
      - "IQ"
      - "OQ"
      - "PQ"
  combined_ioq_allowed: true
  supplier_evidence_reuse: "review-required"
  approved_protocol_required: true
  protocol_integrity_required: true
  baseline_drift_action: "stop"
  independent_review_required_from: "L3"
  quality_approval_required_from: "L3"
  representative_data_required_for_pq: true
  recovery_demonstration_required_from: "L4"
  external_signature_control_required: false
  conditional_release:
    allowed: true
    minimum_approver_role: "quality_owner"
  requalification:
    periodic_review_months: 12
    change_assessment_required: true
```

Rules:

- Sector or regulatory applicability is not inferred solely from L0-L4.
- The local quality profile decides whether qualification applies.
- L0-L4 scale rigor after applicability is established.
- A control matrix cannot itself provide electronic signatures or runtime blocking.

---

## 28. Risk scaling

Use the existing L0-L4 levels without redefining them.

Recommended qualification scaling:

| Level | Default qualification behavior when the profile applies |
|---|---|
| **L0** | No formal qualification; retain exploration scope and no-production boundary. |
| **L1** | Controlled baseline and targeted verification; formal DQ/IQ/OQ/PQ optional according to local procedure. |
| **L2** | Approved baseline, targeted IQ/configuration checks, OQ evidence, rollback, reviewer decision; PQ where intended-use risk warrants it. |
| **L3** | Explicit qualification plan; DQ, IQ/IOQ, OQ, PQ or approved equivalent; independent review and human sign-off. |
| **L4** | L3 plus independent assurance, stronger evidence anchors, recovery demonstration, quality authority, supplier evidence, and explicit residual-risk acceptance. |

A regulated but low-complexity system may still require qualification stages even when technical complexity is modest.

A technically complex non-regulated prototype may be L3 for engineering risk without using GxP terminology.

Do not equate sector criticality and Agile V delivery level.

---

## 29. Requalification and periodic review

Expand current revalidation triggers.

Required change-assessment triggers should include:

```text
application release or patch
configuration change
feature-flag change
operating-system/platform update
database/runtime update
container image change
infrastructure change
security patch
identity/access-control change
interface change
supplier/service change
data migration
intended-use change
business-process or SOP change
critical incident
audit-trail or data-integrity issue
backup/restore process change
monitoring/alarm change
model/provider/runtime/tool/skill change
control-matrix change
accumulated change requests
periodic-review interval
```

Create a `REQUALIFICATION_ASSESSMENT` record that selects one outcome:

```text
NO ADDITIONAL QUALIFICATION
DOCUMENT REVIEW ONLY
TARGETED REGRESSION
IQ ONLY
OQ ONLY
PQ ONLY
IQ + OQ
OQ + PQ
FULL DQ/IQ/OQ/PQ
RETIRE OR REPLACE SYSTEM
```

The assessment MUST include:

```text
change description
old and new baselines
affected intended use
requirements and risks affected
configuration/environment impact
supplier impact
data-integrity impact
required stage evidence
approver and rationale
```

Periodic review should consider:

```text
open deviations and CAPAs
incidents
change history
access reviews
audit-trail reviews
backup/restore results
security and patch status
supplier performance
performance/capacity trends
validation limitations
requalification status
model/toolchain changes
```

---

## 30. Part 11, Annex 11, and data-integrity boundary

The skills library should clearly state which controls require an external system.

### 30.1 Skills can define

```text
required identity fields
approval intent and scope
signature references
record and evidence structure
traceability
review requirements
audit checks
runtime enforcement expectations
negative test cases
```

### 30.2 Skills cannot provide by themselves

```text
authenticated individual identity
non-repudiable electronic signatures
signature-to-record binding
secure audit-trail infrastructure
role-based access enforcement
record retention infrastructure
time-source integrity
write protection
validated backup and restore
closed-system controls
```

### 30.3 Data-integrity controls

For ALCOA+ support, require evidence for:

| Attribute | Evidence expectation |
|---|---|
| Attributable | Authenticated identity or controlled identity reference for author, executor, reviewer, and approver. |
| Legible | Human-readable rendering and machine-readable source. |
| Contemporaneous | Execution timestamps recorded during activity, not reconstructed later. |
| Original | Raw evidence retained or linked; transformations identified. |
| Accurate | Expected-versus-actual results, review, and integrity checks. |
| Complete | Failed, blocked, inconclusive, rerun, and deviation history retained. |
| Consistent | Ordered timestamps, controlled identifiers, and stable schemas. |
| Enduring | Controlled retention and backup in the consuming system. |
| Available | Retrieval tests and authoritative evidence locators. |

The public documentation should describe these as evidence contracts unless runtime/operational evidence exists.

---

## 31. Training and role qualification

Qualification execution may require suitably trained personnel under local procedures.

Add optional references for:

```text
role qualification
procedure training
system training
protocol-specific briefing
witness qualification
quality approval authority
```

Do not store sensitive personnel records in the project repository unless authorized.

Use controlled external references where appropriate.

For PQ, representative users should match the approved intended-use roles.

The framework MUST NOT claim to certify a person's competence.

---

## 32. Human oversight and Bainbridge-aware review

Qualification should actively preserve human understanding rather than create another PASS-heavy documentation ritual.

For L3/L4:

- the human reviewer should see unexpected changes, failed/inconclusive evidence, deviations, assumptions, and evidence gaps before aggregate PASS counts;
- critical stage decisions should include an active question or challenge, not only an approval checkbox;
- AI must not fabricate human rationale, risk acceptance, or approval;
- a reviewer may state `unable to assess independently`, which triggers escalation rather than forced approval;
- recovery procedures should be demonstrated where required, not merely documented;
- a second generative agent is not automatically independent assurance for a critical claim.

Qualification summaries should lead with:

```text
Unexpected changes
Failures and inconclusive results
Open deviations
Evidence gaps
Residual risks
Recovery limitations
Then passing coverage
```

---

## 33. Existing skill changes

### 33.1 `agile-v-core/SKILL.md`

Add a qualification directive:

```text
For locally applicable regulated or high-assurance work, load
agile-v-gxp-qualification. Treat DQ, IQ, OQ, and PQ as evidence stages,
not agent names. Do not proceed past required stage gates without durable evidence.
```

Add `agile-v-gxp-qualification` to companion skills.

### 33.2 `requirement-architect/SKILL.md`

Add qualification-applicability questions:

```text
What is the approved intended use?
Which users, processes, records, and environments are in scope?
Is GxP or another controlled quality context applicable?
Which data-integrity and electronic-record/signature requirements apply?
Which functions are critical to product quality, patient safety, or data integrity?
What representative conditions will later be required for PQ/validation?
```

The requirement artifact should support URS use but should not claim regulatory completeness without local review.

### 33.3 `logic-gatekeeper/SKILL.md`

Clarify:

```text
Logic Gatekeeper performs independent requirement-quality review.
It does not complete DQ because DQ evaluates a proposed design.
```

Add findings for missing qualification path, intended-use ambiguity, untestable critical functions, and missing representative conditions.

### 33.4 `build-agent/SKILL.md`

Add qualification evidence duties:

- produce exact artifact and dependency identity;
- provide installation/configuration inputs;
- identify configuration and customization;
- link SBOM and deployment artifacts;
- never mark its own installation as IQ PASS;
- never approve DQ, OQ, or PQ for its own work.

### 33.5 `test-designer/SKILL.md`

Add qualification-stage metadata and OQ-oriented categories.

Require tests for critical access, audit trail, calculation, error handling, interface, backup/restore, negative, and boundary behavior when selected by risk.

Keep implementation independence unchanged.

### 33.6 `red-team-verifier/SKILL.md`

Add:

```text
IQ evidence review
OQ execution and challenge
protocol revision/baseline verification
qualification deviation checks
stage recommendation
```

Explicitly prohibit calling Red Team verification PQ or intended-use acceptance.

### 33.7 `validation-agent/SKILL.md`

Add an optional PQ mapping mode:

- require IQ/OQ preconditions where applicable;
- identify representative users, data, environment, workflow, and range;
- record operational timing and repeatability;
- distinguish qualified substitutes/simulation from production data;
- issue intended-use conclusions only within tested conditions;
- preserve current verification-versus-validation boundary.

### 33.8 `agile-v-compliance/SKILL.md`

Add qualification deviations, stage release, requalification assessment, and periodic-review triggers.

### 33.9 `compliance-auditor/SKILL.md`

Expand the Validation Summary Report into a Qualification Summary Report view while retaining the existing evidence bundle and traceability model.

Audit:

```text
plan approval
baseline identity
stage completeness
protocol integrity
requirement and risk coverage
execution evidence
deviations and CAPA
supplier evidence
conditional release
requalification triggers
```

### 33.10 `release-manager/SKILL.md`

Block release when required qualification stages are incomplete or conditionally accepted without satisfied conditions.

Add pre-release checks for:

```text
qualified baseline identity
PQ/intended-use acceptance
open critical deviations
residual-risk authority
backup/recovery evidence
requalification status
```

### 33.11 `agile-v-control-matrix/SKILL.md`

Add the qualification control family described above.

### 33.12 `documentation-agent/SKILL.md`

Add duties to maintain qualification documentation, source status, and non-certification language.

---

## 34. Correct stale compliance documentation

Update at least:

```text
docs/compliance/06_GXP_GAMP5_MATRIX.md
docs/compliance/07_GAP_ROADMAP.md
docs/compliance/01_COMPLIANCE_POSTURE.md
docs/tutorials/regulated-software-adoption.md
docs/README.md
README.md
```

Required corrections:

1. Remove the direct agent-to-DQ/IQ/OQ/PQ mapping.
2. Acknowledge that `validation-agent` now provides validation planning, protocol, report, and deviation behavior.
3. Replace the claim that verification and validation are conflated.
4. Replace `COMPLIANT` where only skill or schema coverage exists.
5. Separate target-system qualification from assurance-toolchain qualification.
6. Add explicit IQ/configuration gaps and the proposed solution.
7. Add qualification plan, system description, protocol integrity, supplier suitability, training, and requalification coverage.
8. Preserve the Part 11/e-signature external-control gap.
9. State that the revised Annex 11 consultation draft is a future-readiness input, not a final requirement.

---

## 35. Schema requirements

All new schemas MUST:

```text
use the repository's established JSON Schema draft
set additionalProperties: false where compatible
use stable IDs and enumerations
validate state-dependent fields conditionally
support revision and baseline references
support explicit N/A with rationale where appropriate
reject ambiguous PASS-only execution records
remain backward-compatible with non-qualification projects
```

Important conditional rules:

- `PQ` requires representative-condition fields.
- `IQ` requires installation/configuration fields.
- `OQ` requires requirement-derived test references.
- `DQ` requires design and URS references.
- `CONDITIONALLY_ACCEPTED` requires conditions, impact assessment, owner, and due date.
- `WAIVED` requires approval reference and rationale.
- `executing` requires approved protocol revision and baseline.
- `completed` requires execution records and review.
- secret values must be rejected from evidence fields intended only for references.

---

## 36. Behavioral contract tests

Add or extend contract tests for at least the following.

### 36.1 Skill contracts

```text
test_gxp_qualification_skill_exists
test_gxp_qualification_skill_has_valid_frontmatter
test_gxp_qualification_skill_is_draft_initially
test_core_routes_regulated_work_to_gxp_qualification
test_logic_gatekeeper_does_not_claim_dq
test_build_agent_does_not_claim_iq
test_red_team_does_not_claim_pq
test_validation_agent_preserves_intended_use_boundary
```

### 36.2 Schema tests

```text
test_qualification_plan_schema_accepts_valid_plan
test_qualification_plan_requires_subject
test_protocol_rejects_unknown_stage
test_pq_protocol_requires_representative_conditions
test_iq_protocol_requires_baseline
test_oq_protocol_requires_requirement_links
test_dq_protocol_requires_design_ref
test_execution_requires_expected_and_actual
test_execution_preserves_fail_result
test_conditional_acceptance_requires_authority
test_waiver_requires_approval_ref
test_baseline_rejects_secret_values
test_requalification_assessment_requires_change_scope
test_existing_evidence_bundle_without_qualification_remains_valid
```

### 36.3 Behavioral scenarios

```text
missing approved protocol -> HALT
baseline drift during execution -> HALT or approved deviation
builder self-approves IQ -> FAIL
red-team result labeled PQ -> FAIL
PQ uses unrepresentative data with no rationale -> EVIDENCE INSUFFICIENT
supplier test reused without version/suitability review -> FAIL
failed test overwritten by rerun -> FAIL
conditional release with no impact assessment -> FAIL
critical deviation open at release -> BLOCK
unsupported platform in IQ -> BLOCK or authorized risk decision
no restore evidence for critical system -> BLOCK where policy requires
model/runtime change with no requalification assessment -> BLOCK
```

---

## 37. Reference fixtures

Create fixtures for:

```text
valid DQ package
valid IQ package
valid combined IOQ package
valid OQ package
valid PQ package
valid qualification summary
valid toolchain qualification pilot
invalid post-hoc protocol edit
invalid PASS-only execution
invalid unrepresentative PQ
invalid supplier evidence reuse
invalid unauthorized stage release
invalid hidden baseline drift
```

At least one reference fixture should model a regulated laboratory or manufacturing-support workflow without containing proprietary or personal data.

---

## 38. Runtime enforcement contract

The skills repository defines the contract. Consuming runtimes SHOULD implement:

```text
schema validation in CI
approved-protocol locking or digest verification
baseline drift detection
identity-bound approvals
electronic signatures where required
append-only execution records
controlled evidence storage
required-stage transition blocking
forbidden self-approval checks
conditional-release expiry tracking
requalification trigger detection
```

The skills MUST say:

```text
A skill instruction is not runtime enforcement.
A schema-valid record is not proof of truth.
A Git commit is not automatically a compliant electronic signature.
```

---

## 39. Metrics

Measure both assurance quality and process burden.

Recommended metrics:

```text
requirement coverage
critical-risk coverage
first-pass OQ rate
PQ scenario pass rate
unsafe acceptance rate
correct acceptance rate
deviation rate
deviation closure time
traceability completeness
baseline drift incidents
evidence retrieval success
evidence retrieval time
requalification cycle time
supplier evidence reuse percentage
open CAPA count
recovery success and recovery time
review time and reviewer workload
false alarm rate
```

Do not publish improvement claims without a defined method, baseline, sample, and uncertainty.

---

## 40. Rollout plan

### Phase 0: Correct claims and terminology

- remove the incorrect agent-to-stage mapping;
- update stale validation-gap statements;
- strengthen non-certification language;
- add the four-layer coverage model.

### Phase 1: Draft profile and schemas

- add `agile-v-gxp-qualification` as draft;
- add core schemas and templates;
- add qualification control-matrix fields;
- add documentation and routing.

No stable-use claim yet.

### Phase 2: Behavioral contracts

- add schema tests;
- add role-boundary tests;
- add valid and invalid fixtures;
- verify backward compatibility.

### Phase 3: Reference pilot

Run a controlled qualification pilot for:

```text
a representative target system
and
the Agile V assurance toolchain configuration
```

Record gaps, false alarms, burden, and evidence quality.

### Phase 4: Runtime reference implementation

In a consuming runtime, implement:

```text
protocol digest checks
stage gates
identity approvals
baseline drift checks
execution append-only behavior
requalification triggers
```

This runtime work belongs outside `agile_v_skills` unless only interface contracts are added here.

### Phase 5: Stabilization

Remove `metadata.status: draft` only after:

- contract tests pass;
- reference pilot evidence exists;
- major usability issues are resolved;
- claims are reviewed by qualified GxP/CSV personnel;
- installation profiles and migration guidance are complete.

---

## 41. Migration and backward compatibility

- Existing Agile V projects remain valid when qualification is not enabled.
- Existing control matrices remain valid without the new optional section.
- Existing evidence bundles remain valid without qualification fields.
- Existing `validation-agent` records remain usable.
- Existing `VERIFICATION_SUMMARY.md` remains verification evidence, not PQ.
- Historical GxP documents should be marked superseded rather than silently rewritten when versioned releases are involved.
- Do not change package/repository version manually; follow the repository release process.

---

## 42. Files expected to change

New files:

```text
agile-v-gxp-qualification/SKILL.md

schemas/QUALIFICATION_PLAN.schema.json
schemas/SYSTEM_DESCRIPTION.schema.json
schemas/SYSTEM_BASELINE.schema.json
schemas/QUALIFICATION_PROTOCOL.schema.json
schemas/QUALIFICATION_EXECUTION.schema.json
schemas/QUALIFICATION_DEVIATION.schema.json
schemas/QUALIFICATION_SUMMARY.schema.json
schemas/REQUALIFICATION_ASSESSMENT.schema.json

templates/agile-v/QUALIFICATION_PLAN.example.yaml
templates/agile-v/SYSTEM_DESCRIPTION.example.yaml
templates/agile-v/SYSTEM_BASELINE.example.yaml
templates/agile-v/QUALIFICATION_PROTOCOL.example.yaml
templates/agile-v/QUALIFICATION_EXECUTION.example.yaml
templates/agile-v/QUALIFICATION_DEVIATION.example.yaml
templates/agile-v/QUALIFICATION_SUMMARY.example.yaml
templates/agile-v/REQUALIFICATION_ASSESSMENT.example.yaml

docs/agile-v-runtime/06_GXP_QUALIFICATION_CONTRACT.md
docs/tutorials/gxp-qualification-pilot.md
```

Likely modified files:

```text
agile-v-core/SKILL.md
requirement-architect/SKILL.md
logic-gatekeeper/SKILL.md
build-agent/SKILL.md
test-designer/SKILL.md
red-team-verifier/SKILL.md
validation-agent/SKILL.md
agile-v-compliance/SKILL.md
agile-v-control-matrix/SKILL.md
compliance-auditor/SKILL.md
release-manager/SKILL.md
documentation-agent/SKILL.md

schemas/CONTROL_MATRIX.schema.json
schemas/EVIDENCE_BUNDLE.schema.json
schemas/TRACE_GRAPH.schema.json

templates/agile-v/CONTROL_MATRIX.example.yaml
templates/agile-v/CONTROL_MATRIX.schema.json

catalog/skills.json
SKILL_ROUTING_GUIDE.md
docs/INSTALL_PROFILES.md
docs/compliance/01_COMPLIANCE_POSTURE.md
docs/compliance/06_GXP_GAMP5_MATRIX.md
docs/compliance/07_GAP_ROADMAP.md
docs/tutorials/regulated-software-adoption.md
docs/README.md
README.md
AGENTS.md

tests/
```

The implementing agent MUST inspect actual repository conventions before finalizing names or relations.

---

## 43. Implementation order for an agent

Implement in this order:

```text
1. Read AGENTS.md and current repository version rules.

2. Read current:
   agile-v-core
   requirement-architect
   logic-gatekeeper
   build-agent
   test-designer
   red-team-verifier
   validation-agent
   agile-v-compliance
   agile-v-control-matrix
   compliance-auditor
   release-manager
   documentation-agent.

3. Read current schemas, fixtures, catalog, routing, and compliance docs.

4. Correct stale claims and the incorrect DQ/IQ/OQ/PQ mapping.

5. Add the draft agile-v-gxp-qualification skill.

6. Add qualification terminology and role boundaries.

7. Add core schemas and templates.

8. Add control-matrix qualification policy.

9. Add evidence-bundle integration.

10. Add trace node/relation types only where existing types are insufficient.

11. Update existing skills with minimal, role-specific duties.

12. Add contract and schema tests.

13. Add valid and invalid fixtures.

14. Update routing, profiles, catalog, README, and documentation hub.

15. Run:
    python -m pytest tests -q

16. Measure and update repository counts from actual state.

17. Confirm no executable runtime code or dependencies were added.

18. Confirm package version was not manually edited.
```

Do not implement the entire change as one unreviewed commit.

Recommended commit sequence:

```text
docs(gxp): correct qualification terminology and stale gaps
feat(gxp): add draft qualification profile and contracts
feat(schemas): add qualification evidence schemas
feat(skills): integrate qualification role boundaries
feat(tests): add qualification contract fixtures
 docs(gxp): add pilot and migration guidance
```

---

## 44. Definition of Done

- [ ] Incorrect agent-to-DQ/IQ/OQ/PQ mapping is removed
- [ ] Verification, validation, qualification, and process validation are clearly distinguished
- [ ] `agile-v-gxp-qualification` exists and is marked draft
- [ ] Qualification subjects are explicit
- [ ] Target-system and assurance-toolchain qualification are separated
- [ ] Qualification plan schema and template exist
- [ ] System description schema and template exist
- [ ] System baseline schema and template exist
- [ ] Protocol and execution schemas preserve approved criteria and actual results
- [ ] DQ is a distinct independent design review
- [ ] IQ verifies installation and configuration before OQ
- [ ] OQ uses independent requirement-derived test design
- [ ] Red Team does not claim PQ
- [ ] PQ is mapped to representative intended-use validation only through approved policy
- [ ] PQ records representative users, environment, configuration, data, workflow, and operating range
- [ ] Failed, blocked, inconclusive, waived, and rerun results remain visible
- [ ] Conditional stage release requires authorized impact assessment
- [ ] Supplier evidence reuse is controlled and version-specific
- [ ] Requalification triggers cover system, environment, process, supplier, and AI-toolchain changes
- [ ] Part 11/Annex 11 external-control boundaries are explicit
- [ ] Training and role qualification references are supported
- [ ] Qualification summary report covers all required stages and limitations
- [ ] Evidence bundle and traceability support qualification records
- [ ] Existing non-qualification projects remain backward-compatible
- [ ] Behavioral contract tests cover positive and negative scenarios
- [ ] Reference fixtures exist
- [ ] Public compliance wording no longer overclaims skill-level coverage
- [ ] Repository tests pass
- [ ] README/catalog/schema/test counts are recalculated, not guessed
- [ ] No package version is manually modified

---

## 45. Final operating model

After this upgrade, Agile V should support this controlled flow:

```text
Intent and intended use
        |
        v
Approved URS / baselined requirements
        |
        v
Independent requirement findings
        |
        v
Controlled design
        |
        v
DQ: design acceptable against URS and constraints
        |
        v
Controlled build and deployment baseline
        |
        v
IQ: installed and configured as specified
        |
        v
Independent requirement-derived tests
        |
        v
OQ: operates as designed across risk-relevant range
        |
        v
Representative operational validation
        |
        v
PQ: acceptable for intended use in tested conditions
        |
        v
Qualification summary, residual-risk decision, and release
        |
        v
Periodic review, change control, and requalification
```

The core principle is:

> Agile V should not generate qualification paperwork around an uncontrolled process. It should create a controlled, traceable, risk-based chain from intended use and approved requirements to an identified installation, independently tested operation, representative performance evidence, and accountable release.

