# ISO 27001:2022 Compliance Matrix

> **Document ID**: COMP-005
> **Version**: 1.3
> **Date**: 2026-02-21
> **Classification**: Public
> **Status**: Approved

[← Back to Documentation Hub](../README.md) | [← Previous: AS9100D Matrix](04_AS9100D_MATRIX.md) | [Next: GxP / GAMP 5 Matrix →](06_GXP_GAMP5_MATRIX.md)

---

## Scope

This matrix assesses Agile V against ISO 27001:2022 Annex A controls relevant to secure software development. Controls related to physical security (A.7.1-A.7.6), HR screening (A.6.1), and network security (A.8.20-A.8.22) are excluded as they require organizational infrastructure.

## Compliance Matrix

| Control | Title | Status | Evidence (Skill) | Gap / User Action Required |
|---------|-------|--------|-------------------|---------------------------|
| A.5.1 | Information security policies | **PARTIAL** | AI Agent Security Controls in `agile-v-core` (LLM provider requirements, data classification, access controls). | No system-level security policy for the skill set itself. **User must:** Create an information security policy covering AI agent usage; reference it in `.agile-v/config.json`. |
| A.5.9 | Asset inventory | **PARTIAL** | `.agile-v/` directory defines controlled files. Build Manifest lists artifacts. | Skill files and Decision Log not formally classified as information assets. **User must:** Include `.agile-v/` contents in organizational asset register with classification. |
| A.5.23 | Cloud services security | **COMPLIANT** | LLM provider documentation in `config.json` with data residency, retention, training usage, confidentiality certification, and approval status. Data classification rules. | -- |
| A.8.1 | User endpoint devices | **PARTIAL** | Context engineering limits data in agent context. "Clear between phases" directive. | No agent sandboxing. Agents run with full user permissions. **User must:** Implement endpoint security policy; consider running agents in restricted environments. |
| A.8.3 | Access restriction | **PARTIAL** | Test Designer protocol: "do not read Build Agent code." Agent role separation in pipeline. | Enforcement is protocol-based (honor system), not technical. **User must:** Where possible, configure runtime to restrict agent file access per role. |
| A.8.5 | Secure authentication | **PARTIAL** | APPROVALS.md records approver identity. | No LLM API key management procedure defined. **User must:** Implement API key rotation, scoped tokens, and secure storage for LLM provider credentials. |
| A.8.8 | Vulnerability management | **PARTIAL** | Red-team-verifier detects hardcoded secrets, missing error handling, unbounded operations. | Skill files themselves not covered by vulnerability scanning. **User must:** Include skill file reviews in vulnerability management program. |
| A.8.9 | Configuration management | **COMPLIANT** | `.agile-v/` state directory. Skill version numbers in frontmatter. Build Manifest with artifact locations. Cycle archival. | -- |
| A.8.25 | Secure development lifecycle | **COMPLIANT** | V-Model pipeline: requirements → validation → synthesis → verification → acceptance. Red Team Protocol. Independent test design. Pre-execution validation. | -- |
| A.8.26 | Application security requirements | **COMPLIANT** | Requirement Architect mandates security constraints per REQ. Logic Gatekeeper validates. Hallucination hunting catches unauthorized additions. | -- |
| A.8.27 | Secure architecture | **COMPLIANT** | Logic Gatekeeper enforces constraint validation. Cross-domain synthesis (Principle #11). Hardware awareness for embedded. | -- |
| A.8.28 | Secure coding | **COMPLIANT** | 7 secure coding rules in build-agent: input validation, error handling, no hardcoded secrets, parameterized queries, bounded operations, least privilege, dependency awareness. | -- |
| A.8.29 | Security testing | **PARTIAL** | Stub detection includes hardcoded secrets, missing error handling, unbounded operations. Edge case injection. | No explicit "security" test type in Test Designer taxonomy. No SAST/DAST tooling referenced. **User must:** Add security-specific test cases to requirements; integrate SAST/DAST into CI pipeline. |
| A.8.31 | Environment separation | **PARTIAL** | Pipeline stages provide logical separation. | Skills do not enforce environment boundaries. **User must:** Implement dev/test/prod separation in deployment; ensure agents cannot access production data during development. |
| A.8.32 | Change management | **COMPLIANT** | CR-XXXX protocol. Human Gate approvals. Decision Log. Impact analysis. | -- |
| A.8.33 | Test information | **PARTIAL** | Test cases from requirements only. VER records append-only. | No data classification for test artifacts. **User must:** Classify test data; ensure test specifications don't contain production secrets. |
| A.7.7 | Clear desk/screen | **NOT COVERED** | "Clear between phases" is advisory only. | **User must:** Implement context sanitization procedures; ensure agent sessions are terminated after use. |

## Summary

| Status | Count |
|--------|-------|
| COMPLIANT | 7 |
| PARTIAL | 9 |
| NOT COVERED | 1 |

**Key message for security teams:** Agile V provides strong secure development lifecycle controls (A.8.25-A.8.28), change management (A.8.32), and LLM provider documentation (A.5.23). You must supplement it with: API key management, agent sandboxing, SAST/DAST integration, environment separation enforcement, and organizational security policy.

---

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.3 | 2026-02-21 | agile-v.org | Initial release |

[← Back to Documentation Hub](../README.md) | [← Previous: AS9100D Matrix](04_AS9100D_MATRIX.md) | [Next: GxP / GAMP 5 Matrix →](06_GXP_GAMP5_MATRIX.md)
