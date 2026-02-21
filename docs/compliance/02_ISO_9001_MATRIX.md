# ISO 9001:2015 Compliance Matrix

> **Document ID**: COMP-002
> **Version**: 1.3
> **Date**: 2026-02-21
> **Classification**: Public
> **Status**: Approved

[← Back to Documentation Hub](../README.md) | [← Previous: Compliance Posture](01_COMPLIANCE_POSTURE.md) | [Next: ISO 13485 Matrix →](03_ISO_13485_MATRIX.md)

---

## Scope

This matrix assesses Agile V Skills v1.3 against ISO 9001:2015 clauses relevant to design and development. Clauses related to general organizational context (4.1-4.3), leadership policy (5.2-5.3), and support infrastructure (7.2-7.4) are excluded as they require organizational implementation beyond what a skill set can provide.

## Compliance Matrix

### 4.4 -- QMS and Its Processes

| Aspect | Status | Evidence | Gap |
|--------|--------|----------|-----|
| Process definition | **COMPLIANT** | 5-stage orchestration pipeline with handoff rules (`agile-v-core`) | -- |
| Process interactions | **COMPLIANT** | Pipeline diagram shows agent interactions; Compliance Auditor observes all stages | -- |
| Process performance indicators | **NOT COVERED** | -- | No KPIs defined at QMS level. The compliance-auditor defines 7 project-level metrics but these are per-project, not QMS-wide. **User must:** Define organizational QMS KPIs. |
| Risk to processes | **NOT COVERED** | -- | Risk Register covers project risks, not process risks. **User must:** Assess risks to the Agile V workflow itself. |

### 5.1 -- Leadership and Commitment

| Aspect | Status | Evidence | Gap |
|--------|--------|----------|-----|
| Management review points | **COMPLIANT** | Human Gate 1 (Blueprint), Human Gate 2 (Validation), Evidence Summary format | -- |
| Quality policy | **NOT COVERED** | -- | No mechanism to import organizational quality policy. **User must:** Define quality policy; reference it in `.agile-v/config.json`. |
| Customer focus | **NOT COVERED** | -- | No customer satisfaction input loop. **User must:** Feed customer feedback into requirements via Requirement Architect. |

### 6.1 -- Actions to Address Risks and Opportunities

| Aspect | Status | Evidence | Gap |
|--------|--------|----------|-----|
| Technical risk identification | **COMPLIANT** | Logic Gatekeeper constraint checks; Risk Register in `.agile-v/RISK_REGISTER.md` with severity matrix | -- |
| Process risk assessment | **PARTIAL** | Halt conditions prevent execution risk | No systematic process-level risk assessment. **User must:** Conduct organizational risk assessment for the AI-augmented development process. |
| Opportunity identification | **NOT COVERED** | -- | System is defensive only. **User must:** Include opportunity identification in management reviews. |

### 7.5 -- Documented Information

| Aspect | Status | Evidence | Gap |
|--------|--------|----------|-----|
| Creation and updating | **COMPLIANT** | `.agile-v/` directory with 12+ controlled files; revision headers; write-through persistence | -- |
| Approval status | **COMPLIANT** | `APPROVALS.md` records Gate approvals with identity, authority, timestamp | -- |
| Version control | **COMPLIANT** | Cycle-tagged documents; ART-XXXX.N revision scheme; per-REQ status tags | -- |
| Retention and archival | **COMPLIANT** | Cycle archival to `.agile-v/cycles/CN/` (frozen, read-only); append-only logs | -- |
| Access control | **PARTIAL** | Agent access is protocol-based (honor system) | No technical enforcement of document access control. **User must:** Implement file system permissions or repository access controls. |

### 8.1 -- Operational Planning and Control

| Aspect | Status | Evidence | Gap |
|--------|--------|----------|-----|
| Planning | **COMPLIANT** | Orchestration pipeline; wave-based parallel execution; pre-execution validation (5 dimensions) | -- |
| Control | **COMPLIANT** | Checkpoint types (auto, human-verify, human-decision, human-action); halt conditions | -- |

### 8.2 -- Requirements for Products and Services

| Aspect | Status | Evidence | Gap |
|--------|--------|----------|-----|
| Requirements determination | **COMPLIANT** | Requirement Architect decomposes intent into REQ-XXXX with constraints, verification criteria, done criteria | -- |
| Requirements review | **COMPLIANT** | Logic Gatekeeper validates; Human Gate 1 approves | -- |
| Requirements changes | **COMPLIANT** | CR-XXXX protocol with impact analysis, Human approval, re-validation | -- |

### 8.3 -- Design and Development

| Aspect | Status | Evidence | Gap |
|--------|--------|----------|-----|
| Planning (8.3.1) | **COMPLIANT** | Pipeline stages; phase directories; pre-execution validation | -- |
| Inputs (8.3.2) | **COMPLIANT** | REQUIREMENTS.md with constraints and verification criteria | -- |
| Controls (8.3.3) | **COMPLIANT** | Logic Gatekeeper review; Human Gate 1; Red Team Protocol; Human Gate 2 | -- |
| Outputs (8.3.4) | **COMPLIANT** | Build Manifest with traceability; per-artifact REQ headers | -- |
| Changes (8.3.5) | **COMPLIANT** | CR-XXXX protocol; impact analysis; re-validation; artifact versioning | -- |
| Design review records | **PARTIAL** | Decision Log captures decisions but Logic Gatekeeper results are applied in-place. | **User must:** Ensure Logic Gatekeeper findings are captured before changes are applied (Decision Log entry per finding). |

### 8.5 -- Production and Service Provision

| Aspect | Status | Evidence | Gap |
|--------|--------|----------|-----|
| Identification and traceability (8.5.2) | **COMPLIANT** | REQ → ART → TC → VER full chain; ATM with gap detection; dangling artifact alerts | -- |
| Controlled conditions (8.5.1) | **COMPLIANT** | Pipeline enforces: only approved inputs enter synthesis; outputs manifested; verification independent | -- |

### 8.7 -- Control of Nonconforming Outputs

| Aspect | Status | Evidence | Gap |
|--------|--------|----------|-----|
| Detection | **COMPLIANT** | Red Team Verifier: PASS/FAIL/FLAG; stub detection; anti-pattern scan | -- |
| Severity classification | **COMPLIANT** | CRITICAL (blocks release), MAJOR (fix required), MINOR (deferrable) | -- |
| Disposition | **COMPLIANT** | Rework, Accept-as-is (concession), Reject, Defer -- with approver records | -- |
| NC register | **PARTIAL** | NCs logged in Validation Summary and Decision Log | No consolidated NC register for trending. **User must:** Aggregate NC data across projects for organizational analysis. |

### 9.1 -- Monitoring, Measurement, Analysis, Evaluation

| Aspect | Status | Evidence | Gap |
|--------|--------|----------|-----|
| Measurement | **COMPLIANT** | 7 defined KPIs in compliance-auditor; VER records; coverage tracking | -- |
| Trend analysis | **COMPLIANT** | Cycle-over-cycle trend comparison built into KPI reporting | -- |
| Analysis procedures | **PARTIAL** | Metrics computed per project | No organizational analysis or customer satisfaction measurement. **User must:** Aggregate metrics across projects; implement customer feedback. |

### 9.2 -- Internal Audit

| Aspect | Status | Evidence | Gap |
|--------|--------|----------|-----|
| Continuous audit function | **COMPLIANT** | Compliance Auditor observes all stages; ATM; HITL alerts | -- |
| Audit program | **NOT COVERED** | -- | No scheduled audit intervals, scope rotations, or criteria. **User must:** Define an audit program with frequency, scope, and auditor assignment. |
| Corrective action tracking | **COMPLIANT** | CAPA protocol with effectiveness verification | -- |

### 10.1 -- Nonconformity and Corrective Action

| Aspect | Status | Evidence | Gap |
|--------|--------|----------|-----|
| Correction | **COMPLIANT** | Post-verification feedback loop; 3-attempt limit with escalation | -- |
| Root cause analysis | **COMPLIANT** | CAPA protocol with 5-Whys methodology | -- |
| Preventive action | **COMPLIANT** | CAPA preventive action field with effectiveness verification | -- |
| Corrective action records | **COMPLIANT** | CAPA_LOG.md (append-only) | -- |

### 10.2 -- Continual Improvement

| Aspect | Status | Evidence | Gap |
|--------|--------|----------|-----|
| Iteration framework | **COMPLIANT** | Multi-cycle V-loop with cycle history | -- |
| Metrics trending | **COMPLIANT** | KPIs with cycle-over-cycle trend analysis | -- |
| Lessons learned | **PARTIAL** | Decision Log captures rationale | No formal lessons-learned mechanism. **User must:** Conduct retrospectives at cycle boundaries; record in Decision Log. |

## Summary

| Status | Count |
|--------|-------|
| COMPLIANT | 10 |
| PARTIAL | 4 |
| NOT COVERED (user responsibility) | 5 |

The "NOT COVERED" items require organizational action and cannot be addressed by the skill set alone. See [COMP-007: Gap Roadmap](07_GAP_ROADMAP.md) for a prioritized action plan.

---

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.3 | 2026-02-21 | agile-v.org | Initial release |

[← Back to Documentation Hub](../README.md) | [← Previous: Compliance Posture](01_COMPLIANCE_POSTURE.md) | [Next: ISO 13485 Matrix →](03_ISO_13485_MATRIX.md)
