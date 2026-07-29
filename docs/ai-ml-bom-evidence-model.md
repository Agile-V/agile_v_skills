# AI/ML-BOM Evidence Model

## Evidence Chain

Agile-V evidence normally proves:

```
REQ -> ART -> TEST -> EVIDENCE
```

With AI Influence Traceability enabled, evidence also proves:

```
REQ -> ART -> TEST -> EVIDENCE
       -> AI_RUN_MANIFEST
            -> model identity
            -> inference runtime
            -> agent framework
            -> loaded skills
            -> tools and connectors
            -> RAG/context sources
            -> sandbox/environment
            -> security/privacy posture
```

## Core Artifact: AI_RUN_MANIFEST.yaml

The `AI_RUN_MANIFEST.yaml` is the internal source of truth for Agile-V AI provenance. It is easier for agents and humans to read and write than CycloneDX. CycloneDX is the external export format.

### Field Groups

| Group | Fields | Required at |
|-------|--------|-------------|
| `identity` | task_id, run_id, commit_sha, repository | L0+ |
| `risk` | agile_v_risk_level, ai_influence_level | L0+ |
| `models` | name, provider, model_id, confidence | L0+ |
| `models` | model_version, inference_runtime | L1+ |
| `agent_runtime` | framework, execution_environment | L1+ |
| `agile_v_skills` | skill, version, source | L1+ |
| `tools` | name, type, used | L1+ |
| `rag_and_context` | sources, embedding_model, vector_store | L2+ |
| `evidence_links` | sbom, ml_bom, evidence_bundle | L2+ |
| `change_control` | baseline, bom_diff_required | L2+ |
| `security_and_privacy` | secrets_redacted, hidden_chain_of_thought_excluded | L0+ |

## Evidence Fragment

The `AI_BOM_EVIDENCE_FRAGMENT.json` is the lightweight attachment added to the Agile-V evidence bundle. It links:

- the manifest path and hash
- the CycloneDX export path and hash
- the SBOM link
- the observed runtime inventory source
- revalidation and approval status

## SBOM and AI/ML-BOM Linkage

SBOM tells us what software components are in the system.
AI/ML-BOM and Agent Run BOM tell us what AI components influenced the engineering process and runtime behavior.

They are complementary. Both should be linked in the evidence bundle for L2+ tasks:

```json
"evidence": {
  "sbom": "path/to/sbom.cdx.json",
  "ai_bom": "path/to/AI_BOM_EVIDENCE_FRAGMENT.json"
}
```

## Quality Gates (AIBOM-G0..AIBOM-G7)

| Gate | Check | Applies to |
|------|-------|------------|
| AIBOM-G0 | AI influence declared | All tasks |
| AIBOM-G1 | AI run manifest exists | L1+ |
| AIBOM-G2 | Required fields complete for risk level | L0+ (risk-scaled) |
| AIBOM-G3 | Evidence locators present | L2+ |
| AIBOM-G4 | SBOM and AI/ML-BOM linked | L2+ |
| AIBOM-G5 | BOM diff reviewed when AI context changed | L2+ |
| AIBOM-G6 | Revalidation complete when triggered | L2+ |
| AIBOM-G7 | Human approval complete | L3/L4 |

## Controls (AIBOM-001..AIBOM-012)

| Control | Name |
|---------|------|
| AIBOM-001 | AI Influence Declaration |
| AIBOM-002 | Agent Run Manifest Required |
| AIBOM-003 | Model and Runtime Identity |
| AIBOM-004 | Tool and Skill Inventory |
| AIBOM-005 | RAG and Context Source Inventory |
| AIBOM-006 | Evidence Locator Completeness |
| AIBOM-007 | SBOM / ML-BOM Linkage |
| AIBOM-008 | AI Component Change Detection |
| AIBOM-009 | AI-Triggered Revalidation |
| AIBOM-010 | Runtime Inventory Import |
| AIBOM-011 | Secret and CoT Exclusion |
| AIBOM-012 | Human Approval for High-Risk AI Influence |
