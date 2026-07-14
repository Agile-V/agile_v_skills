# AI Influence Traceability

> Agile-V traces not only the engineered artifact, but also the AI system context that influenced the artifact.

## Overview

AI Influence Traceability is a core Agile-V capability that inventories the AI system that influenced an engineering result. It extends the standard evidence chain:

```
REQ -> ART -> TEST -> EVIDENCE
       -> AI model / runtime / agent / tool / skill / RAG / sandbox / policy context
```

## Why It Matters

AI-assisted engineering is an auditable activity in regulated and high-assurance environments. A release package must be able to answer:

- Which model or model endpoint was used?
- Which inference runtime, coding agent, or AI execution engine was used?
- Which agent skills, prompts, tools, plugins, MCP servers, and RAG sources were available?
- Which versions and hashes were used?
- Which facts were declared, inferred, verified, or unresolved?
- Did any AI component change between verification cycles?
- Did that change trigger revalidation?

## Key Concepts

### Declared vs Observed AI-BOM

| Type | Description |
|------|-------------|
| **Declared** | What the agent/tool says it used (from session config, tool logs, metadata) |
| **Observed** | What runtime inventory tools, logs, CI, Kubernetes controllers, or session hooks observed |

Verified evidence packages prefer observed facts. Declared facts are allowed but must be marked as such with `confidence: "declared"`.

### Confidence Levels

| Level | Meaning |
|-------|---------|
| `declared` | Reported by agent or tool; not independently verified |
| `inferred` | Derived from context (e.g., container image implies runtime version) |
| `verified` | Independently confirmed via log, hash, or runtime observation |
| `unresolved` | Cannot be determined; may block release for L2+ tasks |

### Risk Levels and Requirements

| Level | Context | AI-BOM Requirements |
|-------|---------|---------------------|
| L0 | Docs, trivial tasks | Minimal: model/tool name + CoT exclusion flag |
| L1 | Low-risk code/test | + provider, loaded skills, repo commit, tool list |
| L2 | Production code | + model version, agent runtime, RAG sources, evidence links, BOM diff |
| L3 | Regulated / security-critical | + no unresolved fields, independent verifier, human approval |
| L4 | Safety/release-critical | + signed/archived manifest, formal revalidation, release approval |

## Workflow Integration

1. **Requirement Architect** captures AI influence expectations in the task brief.
2. **agile-v-aibom** creates `AI_RUN_MANIFEST.yaml` at task start.
3. **Build Agent** updates tool usage, model/runtime identity, and context sources.
4. **Test Designer** checks manifest to determine if test re-execution is needed.
5. **Red-Team Verifier** reviews manifest completeness and BOM diff.
6. **Compliance Auditor** produces AI influence inventory summary.
7. **Release Manager** attaches `AI_BOM_EVIDENCE_FRAGMENT.json` to the release package.

## Templates

| Template | Purpose |
|----------|---------|
| `templates/AI_RUN_MANIFEST.yaml` | Core AI inventory document |
| `templates/AI_BOM_EVIDENCE_FRAGMENT.json` | Evidence bundle attachment |
| `templates/AI_BOM_POLICY.yaml` | Risk-level requirements and revalidation triggers |
| `templates/AI_BOM_DIFF_REPORT.md` | Change comparison between runs |
| `templates/AI_COMPONENT_CHANGE_REQUEST.md` | Formal change record for AI components |
| `templates/AI_INFLUENCE_SUMMARY.md` | Release-ready AI provenance summary |
| `templates/CYCLONEDX_AGENT_RUN_BOM.cdx.json` | CycloneDX ML-BOM export |

## Related Docs

- [AI/ML-BOM Evidence Model](ai-ml-bom-evidence-model.md)
- [k8s-aibom Integration](k8s-aibom-integration.md)
- [CycloneDX ML-BOM Export](cyclonedx-ml-bom-export.md)
- [AI-BOM Revalidation Triggers](ai-bom-revalidation-triggers.md)
