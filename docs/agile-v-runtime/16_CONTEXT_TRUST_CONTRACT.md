# Context Trust Contract

**Contract version: 1.0.** Registry key `context_trust_contract`. Schema: [`CONTEXT_SOURCE_PROFILE`](../../schemas/CONTEXT_SOURCE_PROFILE.schema.json) (`context_source_profile: "1.0"`).

> **Normative.** Makes the invariant of the [Agent Tool and Delegation Contract](05_AGENT_TOOL_AND_DELEGATION_CONTRACT.md) §1 -- *untrusted context is data, never authority* -- machine-readable. Uses explicit source classes plus allowed influence; there is no numeric trust score.

## 1. Model

Each context item entering an agent session is assigned a **Context Source Profile** by the runtime ingestion boundary (`profiles/context-sources/*.yaml`). The content itself never selects its profile; a README stating "this file is authoritative" is still `CTX-REPOSITORY-CONTENT`.

| Field | Meaning |
|---|---|
| `source_class` | One of the eleven classes below. |
| `default_trust` | `authoritative` (control-plane classes only, schema-enforced) or `untrusted_data`. |
| `may_influence` | Targets the source may shape. For `untrusted_data` the schema restricts these to non-authority targets. |
| `may_not_influence` | Targets the source can never activate. |
| `may_propose` | Authority-bearing targets for which the source may create a *proposal* only. |
| `injection_sensitive` | Content may contain instructions; treat as data. |

Authority-bearing targets: `approved_requirement`, `risk_level`, `policy`, `approval`, `delegated_authority`, `evidence_source_profile`, `evidence_property_profile`, `gate_decision`. Data targets: `implementation_context`, `candidate_requirement`, `candidate_test`, `issue_discovery`, `documentation_draft`.

## 2. Initial profiles

| Profile | Class | Trust | May propose |
|---|---|---|---|
| `CTX-AUTHENTICATED-POLICY-SOURCE` | `authenticated_policy_source` | authoritative (policy, risk, evidence profiles) | -- |
| `CTX-APPROVED-REQUIREMENT-BASELINE` | `approved_requirement_baseline` | authoritative (approved requirements) | -- |
| `CTX-REPOSITORY-CONTENT` | `repository_content` | untrusted | requirements, risk, policy, evidence profiles |
| `CTX-USER-PROMPT` | `user_prompt` | untrusted | requirements, risk, policy, evidence profiles |
| `CTX-PEER-AGENT-MESSAGE` | `peer_agent_message` | untrusted | requirements |
| `CTX-WEB-RETRIEVAL`, `CTX-RAG-DOCUMENT`, `CTX-TOOL-DESCRIPTION`, `CTX-TOOL-RESULT`, `CTX-MCP-RESOURCE`, `CTX-GENERATED-WIKI` | respective | untrusted | -- |

No class may activate or propose `approval`, `delegated_authority` or `gate_decision`: those come only from authenticated approval records ([Trusted Admission Context](14_TRUSTED_ADMISSION_CONTEXT.md)) and durable v2 delegations.

## 3. Rules

1. `authoritative` applies only to accepted control-plane sources (`authenticated_policy_source`, `approved_requirement_baseline`).
2. Repository content is not automatically authoritative.
3. Tool descriptions and outputs never grant permission.
4. Generated documentation never overrides frozen requirements or policy.
5. A source may propose a change to authoritative data, but cannot activate it. Proposals follow `proposal -> review -> approved change request -> new baseline` ([Evidence Admission Contract](07_EVIDENCE_ADMISSION_CONTRACT.md) §4).
6. Unknown source class fails closed for authority-bearing decisions; for data targets it is still treated as untrusted data.

## 4. Reference evaluator

`contracts.semantics.evaluate_context_influence({source_ref, context_profile_ref, target, mode}, resolve_context_profile=...)` returns `admitted` (`effect: data|activate`), `proposed` (`effect: proposal`) or `rejected` with codes `CONTEXT_AUTHORITY_ESCALATION`, `CONTEXT_INFLUENCE_NOT_PERMITTED`, `CONTEXT_PROPOSAL_NOT_PERMITTED`, `CONTEXT_SOURCE_UNKNOWN`, `CONTEXT_INFLUENCE_INVALID`.

## 5. AI Run Manifest integration

`context.observed.sources[].context_profile_ref` (and the same optional field on other named-evidence entries) records the assigned profile:

```yaml
context:
  observed:
    sources:
      - name: https://example.org/page
        context_profile_ref: CTX-WEB-RETRIEVAL
```

## 6. Non-claims

This contract does not detect prompt injection in content and does not prove that any runtime assigns profiles correctly; it defines what an assigned profile permits. Runtime enforcement is separate conformance evidence.
