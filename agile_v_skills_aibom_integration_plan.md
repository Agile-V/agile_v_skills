# Integration Plan: AI/ML-BOM and Agent Run Provenance for `agile_v_skills`

**Target repository:** `Agile-V/agile_v_skills`  
**Capability name:** AI Influence Traceability  
**New primary skill:** `agile-v-aibom`  
**Primary output:** Agent Run BOM + AI/ML-BOM evidence fragments linked into Agile-V task evidence  
**Recommended release:** minor release, because this adds a new skill and new quality gates  
**Status:** implementation-agent-ready  
**Date:** 2026-07-14

---

## 1. Executive summary

Add a fundamental Agile-V capability that inventories the AI system that influenced an engineering result.

Today Agile-V mainly proves:

```text
REQ -> ART -> TEST -> EVIDENCE
```

After this integration it should also prove:

```text
REQ -> ART -> TEST -> EVIDENCE
        -> AI model / runtime / agent / tool / skill / RAG / sandbox / policy context
```

The goal is not only to know **what artifact changed**, but also **which AI system context influenced the change**.

This matters because AI-assisted engineering is becoming a regulated, auditable engineering activity. A release package should be able to answer:

- Which model or model endpoint was used?
- Which inference runtime, coding agent, or AI execution engine was used?
- Which agent skills, prompts, tools, plugins, MCP servers, and RAG sources were available?
- Which versions and hashes were used?
- Which facts were declared, inferred, verified, or unresolved?
- Did any AI component change between verification cycles?
- Did that change trigger revalidation?

The integration should make AI provenance part of the normal Agile-V evidence model.

---

## 2. Research foundation

### 2.1 k8s-aibom

`k8s-aibom` is a Kubernetes controller from GoogleCloudPlatform that generates CycloneDX 1.6 ML-BOM documents for AI workloads at runtime. Its README describes runtime inventory for inference services, agent stacks, RAG infrastructure, training jobs, and evaluation harnesses. It detects serving runtimes such as vLLM, Hugging Face TGI, NVIDIA Triton, Ollama, Ray Serve, SGLang, and LMDeploy; agent frameworks such as LangChain, LangGraph, AutoGen, CrewAI, Langflow, Flowise, and Chainlit; vector/RAG infrastructure such as Milvus, Qdrant, Weaviate, Chroma, and pgvector; and training/evaluation workloads.

Important lessons for Agile-V:

1. **Runtime matters.** Build-time inventories describe intent. Runtime BOMs describe what actually served inference or executed an agent stack.
2. **AI systems are more than models.** Inventory must cover model identity, inference runtime, agent framework, toolchain, external LLM APIs, vector stores, embeddings, evaluation harnesses, and relevant infrastructure.
3. **Confidence needs to be explicit.** k8s-aibom uses confidence classes such as `declared`, `inferred`, and `unresolved`, with evidence locators for attributes.
4. **Evidence locators are essential.** Every BOM claim should say where it came from: environment variable, annotation, container args, model card, API config, workload spec, artifact hash, commit, or session metadata.
5. **AI/ML-BOM complements SBOM.** AI provenance should be handled together with software dependencies, containers, runtimes, infrastructure, tools, and release evidence.

Reference:

- https://github.com/GoogleCloudPlatform/k8s-aibom

### 2.2 CycloneDX ML-BOM

CycloneDX supports Machine Learning Bill of Materials use cases for transparency around AI/ML systems, including models, datasets, configurations, frameworks, and risk-relevant metadata.

Agile-V should use CycloneDX as the first external standard format because:

- it already supports multiple BOM families, including SBOM and ML-BOM;
- it allows AI/ML inventory to be linked with broader supply-chain inventory;
- it is useful for security, compliance, transparency, and audit workflows.

Reference:

- https://cyclonedx.org/capabilities/mlbom/
- https://github.com/CycloneDX/specification

### 2.3 SPDX AI profile

SPDX 3.0.1 includes an AI profile for documenting AI systems and model artifacts.

Agile-V should not lock itself permanently to one external format.

Recommendation:

```text
Phase 1: Agile-V internal Agent Run Manifest + CycloneDX export.
Phase 2: SPDX 3.0 AI export adapter.
Phase 3: BOM diffing and round-trip validation across formats.
```

Reference:

- https://spdx.github.io/spdx-spec/v3.0.1/model/AI/AI/

---

## 3. Design decision

Make AI/ML-BOM support a **core skill capability**, not a separate optional document.

The new capability should be called:

```text
AI Influence Traceability
```

It should be implemented through:

```text
1. New skill: agile-v-aibom
2. New templates: AI run manifest, AI BOM policy, AI evidence fragment, AI BOM diff report
3. Updates to existing skills: core, build, test, verifier, auditor, release, quality gates, control matrix
4. New routing rules in SKILL_ROUTING_GUIDE.md
5. New examples and tests
6. Evidence bundle integration
7. Revalidation triggers when AI components change
```

The repository should support both:

```text
Declared AI-BOM:
  What the agent/tool says it used.

Observed AI-BOM:
  What runtime inventory tools, logs, hooks, CI, Kubernetes controllers, or session metadata observed.
```

The verified evidence package should prefer observed facts. Declared facts are allowed but must be marked as such.

---

## 4. Non-goals

Do not implement these in the first release:

- Do not store hidden chain-of-thought.
- Do not require all users to run Kubernetes.
- Do not require k8s-aibom for local or IDE-based agent runs.
- Do not claim semantic AI review is formal verification.
- Do not block low-risk adoption with overly heavy compliance requirements.
- Do not make CycloneDX the internal source of truth. The internal Agile-V manifest should be easier for agents and humans to use, with CycloneDX as export format.

---

## 5. Target repository integration

The current `agile_v_skills` repository already contains core engineering skills such as `agile-v-core`, `agile-v-control-matrix`, `agile-v-quality-gates`, `build-agent`, `compliance-auditor`, `red-team-verifier`, `release-manager`, `requirement-architect`, and others.

Add this capability as a native extension of that ecosystem.

### 5.1 New directories

Create:

```text
agile-v-aibom/
  SKILL.md
  README.md
  examples/
    ai_run_manifest.minimal.yaml
    ai_run_manifest.agentic.yaml
    ai_run_manifest.k8s_runtime.yaml
    evidence_fragment.example.json
    cyclone_dx_ml_bom.example.cdx.json
    aibom_diff_report.example.md

templates/
  AI_RUN_MANIFEST.yaml
  AI_BOM_POLICY.yaml
  AI_BOM_EVIDENCE_FRAGMENT.json
  AI_BOM_DIFF_REPORT.md
  AI_COMPONENT_CHANGE_REQUEST.md
  AI_INFLUENCE_SUMMARY.md
  CYCLONEDX_AGENT_RUN_BOM.cdx.json

docs/
  ai-influence-traceability.md
  ai-ml-bom-evidence-model.md
  k8s-aibom-integration.md
  cyclonedx-ml-bom-export.md
  ai-bom-revalidation-triggers.md

tests/
  aibom/
    valid_ai_run_manifest.yaml
    invalid_missing_model.yaml
    invalid_unresolved_l3_runtime.yaml
    valid_evidence_fragment.json
    valid_cyclonedx_export.cdx.json
```

### 5.2 Files to update

Update:

```text
README.md
SKILL_ROUTING_GUIDE.md
EXAMPLES.md
AGENTS.md
CLAUDE.md
CURSOR.md
CHANGELOG.md
agile-v-core/SKILL.md
agile-v-control-matrix/SKILL.md
agile-v-quality-gates/SKILL.md
build-agent/SKILL.md
requirement-architect/SKILL.md
test-designer/SKILL.md
red-team-verifier/SKILL.md
compliance-auditor/SKILL.md
release-manager/SKILL.md
documentation-agent/SKILL.md
threat-modeler/SKILL.md
```

---

## 6. New skill: `agile-v-aibom`

### 6.1 Purpose

`agile-v-aibom` captures, validates, compares, and summarizes the AI system context that influenced an Agile-V task.

The skill should produce:

```text
AI_RUN_MANIFEST.yaml
AI_BOM_EVIDENCE_FRAGMENT.json
AI_INFLUENCE_SUMMARY.md
AI_BOM_DIFF_REPORT.md, when comparing runs
CycloneDX ML-BOM export, when requested
```

### 6.2 Skill trigger conditions

The skill should activate when the user asks for:

- AI/ML-BOM
- AI BOM
- AIBOM
- model inventory
- agent run provenance
- model/runtime/tool traceability
- AI evidence bundle
- CycloneDX ML-BOM
- k8s-aibom integration
- runtime AI inventory
- regulated AI-assisted engineering evidence
- revalidation after model/runtime/tool/skill changes

### 6.3 Required behavior

The skill must:

1. Capture model/provider/runtime/tool/skill/RAG/sandbox/policy context.
2. Mark each field with a confidence level.
3. Attach evidence locators for every material field.
4. Link AI inventory to task ID, requirement IDs, artifact IDs, tests, evidence bundle, and release package.
5. Detect changes between AI manifests.
6. Recommend revalidation when risk-relevant AI components changed.
7. Never store hidden chain-of-thought.
8. Prefer hashes, IDs, versions, config snapshots, logs, and output artifacts over internal reasoning traces.

### 6.4 Suggested `SKILL.md` outline

Create `agile-v-aibom/SKILL.md` with this structure:

```markdown
# Agile-V AIBOM Skill

## Purpose
Capture AI/ML-BOM and agent run provenance for Agile-V tasks.

## When to use
Use when an engineering task is influenced by AI models, agent runtimes, inference services, RAG systems, coding tools, generated code, generated tests, generated requirements, generated PCB/firmware/software artifacts, or AI-assisted verification.

## Outputs
- AI_RUN_MANIFEST.yaml
- AI_BOM_EVIDENCE_FRAGMENT.json
- AI_INFLUENCE_SUMMARY.md
- AI_BOM_DIFF_REPORT.md
- optional CycloneDX ML-BOM export

## Required fields
- task_id
- risk_level
- agent_run_id
- model identity
- model provider or inference runtime
- agent framework/tool
- loaded Agile-V skills
- tool access
- repository and sandbox context
- RAG/context sources
- evidence locators
- confidence levels
- privacy/safety exclusions

## Process
1. Identify task and risk level.
2. Capture declared AI context.
3. Capture observed AI context where available.
4. Normalize into AI_RUN_MANIFEST.yaml.
5. Validate required fields for risk level.
6. Export evidence fragment.
7. Compare against baseline if available.
8. Trigger revalidation when policy requires it.
9. Summarize AI influence for release evidence.

## Safety rules
- Do not record hidden chain-of-thought.
- Do not record secrets, API keys, personal data, or proprietary prompts unless explicitly approved and redacted.
- Do not mark inferred data as verified.
- Do not allow unresolved critical AI components for L3/L4 tasks.
```

---

## 7. Core artifact: `AI_RUN_MANIFEST.yaml`

Create `templates/AI_RUN_MANIFEST.yaml`.

### 7.1 Template

```yaml
aibom_schema_version: "0.1"
manifest_type: "agile-v-agent-run-bom"

identity:
  task_id: "AAV-0000"
  run_id: "RUN-0000"
  created_at: "YYYY-MM-DDTHH:MM:SSZ"
  created_by: "agent-or-human"
  repository: "owner/repo"
  commit_sha: ""
  branch: ""
  pull_request: ""

risk:
  agile_v_risk_level: "L0|L1|L2|L3|L4"
  ai_influence_level: "none|assistive|substantial|critical"
  regulated_context: false
  human_approval_required: false

models:
  - name: ""
    provider: ""
    model_id: ""
    model_version: ""
    endpoint_or_deployment: ""
    inference_runtime: ""
    runtime_version: ""
    context_window: null
    temperature: null
    top_p: null
    tool_calling_enabled: null
    confidence: "declared|inferred|verified|unresolved"
    evidence_locator: ""

agent_runtime:
  agent_name: ""
  agent_framework: ""
  framework_version: ""
  execution_environment: "local|ci|container|kubernetes|ide|saas|unknown"
  sandbox_image: ""
  sandbox_image_digest: ""
  orchestrator: ""
  confidence: "declared|inferred|verified|unresolved"
  evidence_locator: ""

agile_v_skills:
  - skill: "agile-v-core"
    version: ""
    source: "repository|plugin|local|unknown"
    commit_sha: ""
    confidence: "declared|inferred|verified|unresolved"
    evidence_locator: ""

tools:
  - name: ""
    type: "code_execution|shell|filesystem|browser|mcp|connector|git|ci|eda|firmware|test|other"
    version: ""
    allowed: true
    used: false
    confidence: "declared|inferred|verified|unresolved"
    evidence_locator: ""

rag_and_context:
  sources:
    - name: ""
      type: "repo|openwiki|vector_db|document|web|ticket|design_doc|datasheet|other"
      version_or_hash: ""
      retrieved_at: ""
      confidence: "declared|inferred|verified|unresolved"
      evidence_locator: ""
  embedding_model:
    name: ""
    version: ""
    confidence: "declared|inferred|verified|unresolved"
  vector_store:
    name: ""
    version: ""
    collection: ""
    confidence: "declared|inferred|verified|unresolved"

external_services:
  - name: ""
    type: "llm_api|telemetry|tracing|vector_db|artifact_store|other"
    version: ""
    endpoint_class: "public|private|internal|unknown"
    confidence: "declared|inferred|verified|unresolved"
    evidence_locator: ""

runtime_inventory:
  source: "manual|ci|k8s-aibom|agent-log|openhands-hook|other"
  imported_bom: ""
  imported_bom_hash: ""
  confidence: "declared|inferred|verified|unresolved"

security_and_privacy:
  secrets_redacted: true
  hidden_chain_of_thought_excluded: true
  pii_redacted: true
  prompt_capture_policy: "metadata_only|redacted|full_allowed|not_captured"

evidence_links:
  sbom: ""
  ml_bom: ""
  agent_log: ""
  test_results: ""
  evidence_bundle: ""
  verification_report: ""
  release_package: ""

change_control:
  baseline_manifest: ""
  bom_diff_required: false
  revalidation_required: false
  revalidation_reason: ""

summary:
  unresolved_items: []
  verifier_notes: ""
  human_approval: "not_required|required|approved|rejected|pending"
```

### 7.2 Required fields by risk level

```text
L0:
  task_id, run_id, model name or tool name, hidden CoT excluded flag

L1:
  L0 + provider/runtime + loaded skills + repository commit + tool list

L2:
  L1 + model version/deployment + agent runtime + RAG/context sources + evidence links

L3:
  L2 + BOM diff + no unresolved model/runtime/tool fields + independent verifier review

L4:
  L3 + verified or explicitly approved AI runtime identity + signed/archived manifest + human approval
```

---

## 8. Evidence fragment: `AI_BOM_EVIDENCE_FRAGMENT.json`

Create `templates/AI_BOM_EVIDENCE_FRAGMENT.json`.

```json
{
  "evidence_type": "ai_bom",
  "schema_version": "0.1",
  "task_id": "AAV-0000",
  "run_id": "RUN-0000",
  "risk_level": "L0|L1|L2|L3|L4",
  "ai_influence_level": "none|assistive|substantial|critical",
  "manifest_path": ".agile-v/aibom/AAV-0000/AI_RUN_MANIFEST.yaml",
  "manifest_hash": "sha256:",
  "cyclonedx_export_path": ".agile-v/aibom/AAV-0000/agent_run.cdx.json",
  "cyclonedx_export_hash": "sha256:",
  "sbom_link": "",
  "observed_runtime_inventory": {
    "source": "manual|ci|k8s-aibom|agent-log|openhands-hook|other",
    "path": "",
    "hash": "sha256:"
  },
  "unresolved_items": [],
  "revalidation_required": false,
  "revalidation_reason": "",
  "verifier_status": "not_required|pending|passed|failed",
  "human_approval_required": false,
  "human_approval_status": "not_required|pending|approved|rejected"
}
```

---

## 9. AI BOM policy

Create `templates/AI_BOM_POLICY.yaml`.

```yaml
policy_version: "0.1"

risk_level_requirements:
  L0:
    allow_unresolved_model: true
    require_manifest: true
    require_bom_diff: false
    require_human_approval: false
  L1:
    allow_unresolved_model: true
    require_manifest: true
    require_bom_diff: false
    require_human_approval: false
  L2:
    allow_unresolved_model: false
    require_manifest: true
    require_bom_diff: true
    require_human_approval: false
  L3:
    allow_unresolved_model: false
    require_manifest: true
    require_bom_diff: true
    require_independent_verification: true
    require_human_approval: true
  L4:
    allow_unresolved_model: false
    require_manifest: true
    require_bom_diff: true
    require_independent_verification: true
    require_signed_manifest: true
    require_human_approval: true

revalidation_triggers:
  - model_provider_changed
  - model_id_changed
  - model_version_changed
  - inference_runtime_changed
  - agent_framework_changed
  - agile_v_skill_changed
  - tool_access_changed
  - rag_source_changed
  - vector_store_changed
  - embedding_model_changed
  - sandbox_image_changed
  - system_prompt_or_policy_changed
  - unresolved_runtime_attribute_in_l2_plus

privacy_rules:
  store_hidden_chain_of_thought: false
  store_api_keys: false
  store_unredacted_secrets: false
  prompt_capture_default: "metadata_only"
```

---

## 10. CycloneDX export strategy

Add `templates/CYCLONEDX_AGENT_RUN_BOM.cdx.json` as a minimal example.

Use this export as the external interoperability format. Keep the internal `AI_RUN_MANIFEST.yaml` as the source of truth for Agile-V skills.

### 10.1 Mapping

```text
Agile-V task_id             -> CycloneDX metadata.properties
Agile-V run_id              -> CycloneDX serialNumber or metadata.properties
Model identity              -> CycloneDX component with type/data classification where applicable
Inference runtime           -> CycloneDX component/service
Agent framework             -> CycloneDX component/service
RAG source/vector store     -> CycloneDX component/service/data reference where applicable
Tooling                     -> CycloneDX component/service
Evidence locator            -> CycloneDX externalReferences/properties
Confidence                  -> CycloneDX properties
SBOM link                   -> CycloneDX externalReferences or BOM-Link
```

### 10.2 Export guidance

The export does not need to be perfect in v1. It must be:

- valid JSON;
- clearly marked as generated from Agile-V;
- traceable to the internal manifest;
- stable enough for diffing;
- able to preserve confidence and evidence locator metadata.

---

## 11. k8s-aibom integration

Add `docs/k8s-aibom-integration.md` and examples for importing a runtime ML-BOM into an Agile-V evidence bundle.

### 11.1 Integration modes

```text
Mode A: Manual import
  User provides a CycloneDX ML-BOM generated by k8s-aibom.

Mode B: CI import
  CI fetches the latest runtime BOM artifact and attaches it to Agile-V evidence.

Mode C: Kubernetes runtime observation
  Runtime controller emits BOMs for AI workloads; Agile-V references those BOMs in release evidence.
```

### 11.2 Import fields

When a k8s-aibom document is available, import or link:

```text
container images and digests
inference runtime identity
model identity
agent framework identity
external LLM API dependencies
RAG/vector infrastructure
training/evaluation workload metadata
confidence values
evidence locators
source workload identity
BOM hash
BOM generation timestamp
```

### 11.3 Validation rule

For L2+ tasks, if the agent run or deployed system used a Kubernetes AI runtime and a k8s-aibom artifact is available, the Agile-V evidence bundle must either:

```text
1. link the k8s-aibom artifact, or
2. explain why runtime inventory was unavailable.
```

For L3/L4 tasks, missing runtime inventory should be a verifier finding unless explicitly risk-accepted by a human approver.

---

## 12. Updates to existing skills

### 12.1 `agile-v-core`

Add AI Influence Traceability to the core lifecycle.

Modify core skill guidance:

```text
When an AI agent materially influences an artifact, create or update AI_RUN_MANIFEST.yaml.
When model/runtime/tool/skill/context changes occur after verification, trigger revalidation according to risk level.
Do not treat AI-generated output as fully traceable unless the influencing AI system context is documented.
```

Add to SCOPE-V:

```text
Specify:
  Identify AI influence expectations.

Constrain:
  Define allowed models, tools, skills, runtimes, and data sources.

Orchestrate:
  Select agent/runtime and create AI_RUN_MANIFEST.

Prove:
  Link tests and evidence to AI run context.

Evolve:
  Diff AI run context when changes occur.

Verify:
  Confirm BOM completeness and revalidation status.
```

### 12.2 `requirement-architect`

Add questions:

```text
Will AI generate or materially modify artifacts?
Are there allowed or prohibited model providers?
Are there regulated data constraints?
Are RAG/document sources allowed?
What level of AI provenance is required for this task?
```

Add output field to requirements/task briefs:

```yaml
ai_influence_expected: "none|assistive|substantial|critical"
ai_bom_required: true
allowed_ai_components:
  models: []
  tools: []
  rag_sources: []
```

### 12.3 `build-agent`

Add requirement:

```text
Before implementation, confirm AI_RUN_MANIFEST exists for L1+ tasks.
After implementation, update tool usage, model/runtime identity, loaded skills, context sources, and evidence links.
Never hide AI-generated or AI-modified artifacts from evidence.
```

### 12.4 `test-designer`

Add requirement:

```text
Use AI_RUN_MANIFEST to decide whether test re-execution is needed.
If a model/runtime/tool/skill changed, flag affected tests for rerun according to AI_BOM_POLICY.
```

### 12.5 `red-team-verifier`

Add verification checklist:

```text
Does the task include an AI_RUN_MANIFEST?
Are all L2+ required fields present?
Are critical model/runtime/tool fields unresolved?
Did AI context change since the last accepted baseline?
Was required revalidation performed?
Are hidden chain-of-thought and secrets excluded?
Are RAG sources and repository knowledge snapshots documented?
Is the AI influence level consistent with the actual task?
```

Verifier decision rules:

```text
L0-L1: warn on incomplete AI metadata.
L2: fail if model/runtime/tool identity is unresolved.
L3-L4: fail if BOM diff is missing or human approval is pending.
```

### 12.6 `compliance-auditor`

Add audit outputs:

```text
AI influence inventory summary
AI BOM completeness score
AI component change history
Runtime inventory gap report
Revalidation trigger report
Release AI provenance statement
```

### 12.7 `agile-v-quality-gates`

Add gates:

```text
AIBOM-G0: AI influence declared
AIBOM-G1: AI run manifest exists
AIBOM-G2: Required fields complete for risk level
AIBOM-G3: Evidence locators present
AIBOM-G4: SBOM and AI/ML-BOM linked
AIBOM-G5: BOM diff reviewed when AI context changed
AIBOM-G6: Revalidation complete when triggered
AIBOM-G7: Human approval complete for L3/L4
```

### 12.8 `agile-v-control-matrix`

Add new control family:

```text
AIBOM-001 AI Influence Declaration
AIBOM-002 Agent Run Manifest Required
AIBOM-003 Model and Runtime Identity
AIBOM-004 Tool and Skill Inventory
AIBOM-005 RAG and Context Source Inventory
AIBOM-006 Evidence Locator Completeness
AIBOM-007 SBOM / ML-BOM Linkage
AIBOM-008 AI Component Change Detection
AIBOM-009 AI-Triggered Revalidation
AIBOM-010 Runtime Inventory Import
AIBOM-011 Secret and CoT Exclusion
AIBOM-012 Human Approval for High-Risk AI Influence
```

### 12.9 `release-manager`

Add release checklist:

```text
AI_RUN_MANIFEST present for all AI-assisted release tasks.
AI_BOM_EVIDENCE_FRAGMENT linked in evidence bundle.
CycloneDX export attached where required.
AI component changes since baseline reviewed.
Revalidation complete or risk-accepted.
Human approval captured for L3/L4.
```

Release summary should include:

```text
AI models used
AI runtimes/tools used
BOM hashes
unresolved AI inventory items
revalidation status
risk acceptance decisions
```

### 12.10 `documentation-agent`

Add docs rules:

```text
Document AI-BOM policy in project documentation.
Keep public docs high-level; keep evidence manifests in controlled release evidence.
Do not publish sensitive model endpoints, secrets, prompts, or internal policy details without review.
```

### 12.11 `threat-modeler`

Add AI supply-chain threat prompts:

```text
Could a model/runtime/tool change alter generated output quality?
Could a compromised RAG source influence implementation?
Could an agent tool provide unauthorized access?
Could an untracked external LLM endpoint leak data?
Could a vector database or embedding model change invalidate traceability?
Could a malicious MCP/tool call change the artifact outside approved scope?
```

---

## 13. Evidence bundle integration

Extend Agile-V evidence bundles with:

```json
"ai_influence": {
  "manifest": ".agile-v/aibom/AAV-0000/AI_RUN_MANIFEST.yaml",
  "manifest_hash": "sha256:",
  "cyclonedx_export": ".agile-v/aibom/AAV-0000/agent_run.cdx.json",
  "cyclonedx_export_hash": "sha256:",
  "sbom_link": "",
  "runtime_inventory_source": "manual|ci|k8s-aibom|agent-log|openhands-hook|other",
  "unresolved_items": [],
  "revalidation_required": false,
  "revalidation_status": "not_required|pending|complete|risk_accepted",
  "verifier_status": "not_required|pending|passed|failed",
  "human_approval_status": "not_required|pending|approved|rejected"
}
```

This should be a required evidence section for all AI-assisted L1+ tasks.

---

## 14. Revalidation rules

A task must be marked for revalidation when any of the following changes after verification:

```text
model provider
model ID
model version or deployment
inference runtime
agent runtime/framework
agent skill version
system/developer instruction version
tool access policy
MCP/plugin/connector availability
RAG corpus version
OpenWiki/context snapshot
embedding model
vector store or collection
sandbox/container image
CI/runtime environment
AI BOM policy
```

### 14.1 Revalidation severity

```text
Documentation-only task:
  Review AI influence summary and refresh docs if needed.

L1 software task:
  Rerun tests affected by generated artifacts.

L2 task:
  Rerun full verification for changed artifacts.

L3 task:
  Rerun independent verifier and require human review.

L4 task:
  Treat as controlled change request with formal approval.
```

---

## 15. How this integrates with software, PCB, and firmware workflows

### 15.1 Software / OpenHands

For OpenHands or other coding-agent execution:

```text
OpenHands session metadata -> AI_RUN_MANIFEST
OpenHands hooks/tool logs -> evidence locators
repository commit/diff -> artifact traceability
CI results -> evidence bundle
independent verifier -> verification report
```

Required fields:

```text
agent runtime
model/provider
loaded skills
tools used
repository commit
sandbox image
CI/test links
```

### 15.2 PCB / KiCad backend

For AI-assisted PCB work:

```text
schematic-generation model -> AI_RUN_MANIFEST
component search/datasheet RAG -> RAG/context sources
KiCad/ERC/BOM outputs -> evidence bundle
component manifest -> SBOM/HBOM/ML-BOM linkage
```

Additional required fields:

```text
EDA tool version
component library source
datasheet source hashes or URLs
schematic DSL version
KiCad export artifact hashes
```

### 15.3 Firmware / Embedded backend

For AI-assisted firmware work:

```text
firmware generation agent -> AI_RUN_MANIFEST
hardware-firmware contract -> context source
compiler/toolchain -> tools/runtime
build/test/HIL outputs -> evidence bundle
```

Additional required fields:

```text
compiler version
SDK/RTOS version
board support package version
flasher/debugger tool
simulation/HIL runner
hardware contract hash
```

---

## 16. Routing guide update

Add to `SKILL_ROUTING_GUIDE.md`:

```markdown
## AI/ML-BOM and Agent Run Provenance

Use `agile-v-aibom` when the user asks to:

- inventory AI models, agent runtimes, or AI tools;
- create an AI-BOM, ML-BOM, or Agent Run BOM;
- link model/runtime/tool provenance to evidence bundles;
- compare two AI-assisted runs;
- determine whether model/runtime/tool changes require revalidation;
- integrate k8s-aibom or CycloneDX ML-BOM artifacts;
- prepare regulated release evidence for AI-assisted engineering.

Common companion skills:

- `agile-v-core` for lifecycle integration;
- `agile-v-control-matrix` for controls;
- `agile-v-quality-gates` for acceptance gates;
- `red-team-verifier` for independent review;
- `compliance-auditor` for audit evidence;
- `release-manager` for release packaging.
```

---

## 17. README update

Add a section to `README.md`:

```markdown
## AI Influence Traceability

Agile-V now supports AI/ML-BOM and Agent Run BOM evidence. This allows teams to trace not only requirements, artifacts, tests, and verification evidence, but also the AI systems that influenced engineering outputs.

This includes:

- model and provider identity;
- inference runtime or agent framework;
- loaded Agile-V skills;
- tools, plugins, connectors, MCP servers, and execution sandbox;
- RAG/context sources;
- runtime inventory imports such as k8s-aibom;
- CycloneDX ML-BOM export;
- revalidation triggers when AI components change.

Use the `agile-v-aibom` skill for AI-assisted tasks that require provenance, compliance, or release evidence.
```

---

## 18. AGENTS / CLAUDE / CURSOR instructions

Add the same short rule to agent instruction files:

```markdown
## AI Influence Traceability Rule

When an AI agent materially influences requirements, architecture, code, tests, PCB artifacts, firmware, documentation, verification, or release evidence, create or update an AI_RUN_MANIFEST and link it to the evidence bundle.

Do not store hidden chain-of-thought, secrets, API keys, or unredacted proprietary prompts. Store auditable metadata: model identity, runtime identity, tool access, skill versions, context sources, artifact hashes, test evidence, and confidence/evidence locators.
```

---

## 19. Test plan

### 19.1 Static content checks

Add tests to ensure:

```text
agile-v-aibom/SKILL.md exists
all templates exist
SKILL_ROUTING_GUIDE.md references agile-v-aibom
README.md includes AI Influence Traceability
quality gates include AIBOM-G0..AIBOM-G7
control matrix includes AIBOM-001..AIBOM-012
```

### 19.2 Manifest validation examples

Validate sample manifests:

```text
valid_ai_run_manifest.minimal.yaml -> pass
valid_ai_run_manifest.agentic.yaml -> pass
invalid_missing_model.yaml -> fail for L2+
invalid_unresolved_l3_runtime.yaml -> fail for L3
valid_evidence_fragment.json -> pass
```

### 19.3 Policy tests

Test rules:

```text
L0 allows unresolved model identity.
L2 fails unresolved model/runtime/tool identity.
L3 requires BOM diff and independent verification.
L4 requires signed or explicitly approved manifest.
AI context change triggers revalidation.
Hidden chain-of-thought field is forbidden.
Secrets/API keys are forbidden.
```

---

## 20. Implementation backlog

### Issue 1: Add `agile-v-aibom` skill

**Scope**

```text
Create agile-v-aibom/SKILL.md, README.md, and examples.
```

**Acceptance criteria**

```text
Skill explains purpose, triggers, outputs, process, safety rules, and companion skills.
Examples cover minimal local run, agentic software run, and k8s runtime import.
```

### Issue 2: Add AI-BOM templates

**Scope**

```text
Add AI_RUN_MANIFEST.yaml, AI_BOM_POLICY.yaml, evidence fragment, diff report, component change request, influence summary, CycloneDX example.
```

**Acceptance criteria**

```text
Templates include risk-level fields, confidence levels, evidence locators, and no hidden CoT fields.
```

### Issue 3: Extend quality gates

**Scope**

```text
Add AIBOM-G0..AIBOM-G7 to agile-v-quality-gates.
```

**Acceptance criteria**

```text
Gate behavior is explicit for L0-L4.
L3/L4 cannot pass with missing AI manifest, missing diff, or pending human approval.
```

### Issue 4: Extend control matrix

**Scope**

```text
Add AIBOM-001..AIBOM-012 to agile-v-control-matrix.
```

**Acceptance criteria**

```text
Each control has objective, evidence artifact, verifier check, and failure mode.
```

### Issue 5: Update existing skills

**Scope**

```text
Patch agile-v-core, requirement-architect, build-agent, test-designer, red-team-verifier, compliance-auditor, release-manager, documentation-agent, threat-modeler.
```

**Acceptance criteria**

```text
Each skill references when and how AI_RUN_MANIFEST is created, checked, or used.
```

### Issue 6: Add docs

**Scope**

```text
Add docs/ai-influence-traceability.md, ai-ml-bom-evidence-model.md, k8s-aibom-integration.md, cyclonedx-ml-bom-export.md, ai-bom-revalidation-triggers.md.
```

**Acceptance criteria**

```text
Docs include workflow diagrams, risk-level tables, integration examples, and compliance notes.
```

### Issue 7: Add tests and examples

**Scope**

```text
Add manifest examples and repository tests for presence/format/routing.
```

**Acceptance criteria**

```text
CI validates that required files exist and sample manifests conform to policy expectations.
```

### Issue 8: Release update

**Scope**

```text
Update README, EXAMPLES, SKILL_ROUTING_GUIDE, CHANGELOG, and release notes.
```

**Acceptance criteria**

```text
Users can discover the new capability, understand when to use it, and see example outputs.
```

---

## 21. Example end-to-end workflow

```text
1. Requirement Architect creates task brief.
2. Task is classified as L2 with substantial AI influence.
3. agile-v-aibom creates AI_RUN_MANIFEST.yaml.
4. Build Agent implements code using approved model/tool/runtime.
5. Tool usage and context sources are added to AI_RUN_MANIFEST.
6. Test Designer runs required tests.
7. Evidence bundle links SBOM + AI_RUN_MANIFEST + CycloneDX export.
8. Red-Team Verifier checks manifest completeness and BOM diff.
9. Compliance Auditor creates AI influence summary.
10. Release Manager attaches AI_BOM_EVIDENCE_FRAGMENT to release evidence.
```

---

## 22. Example risk-level outcomes

### L0 example

```text
AI helped draft a README section.
Required: minimal manifest, model/tool name if known, CoT exclusion.
Gate result: pass with warning if details incomplete.
```

### L1 example

```text
AI generated a unit test.
Required: model/provider, repository commit, tool list, skill list.
Gate result: pass if tests pass and manifest exists.
```

### L2 example

```text
AI modified production code.
Required: full manifest, model/runtime identity, RAG/context sources, evidence links, BOM diff.
Gate result: fail if model/runtime identity unresolved.
```

### L3 example

```text
AI changed authentication, firmware update, medical logic, or regulated workflow logic.
Required: full manifest, no unresolved critical fields, independent verifier, human approval.
Gate result: fail if verifier or human approval missing.
```

### L4 example

```text
AI influenced safety/security/regulated release-critical artifact.
Required: signed or archived manifest, formal revalidation, release approval, controlled change record.
Gate result: block release until evidence complete.
```

---

## 23. Definition of done

This integration is complete when:

```text
agile-v-aibom skill exists and is routable.
All templates exist and include examples.
AI_RUN_MANIFEST is referenced by core, build, verify, audit, and release workflows.
Quality gates include AI-BOM rules by risk level.
Control matrix includes AIBOM controls.
Evidence bundle examples include AI influence evidence.
k8s-aibom import is documented.
CycloneDX ML-BOM export is documented.
Tests verify presence and minimum schema expectations.
README and EXAMPLES explain usage.
No template stores hidden chain-of-thought or secrets.
```

---

## 24. Implementation order

Use this order to minimize merge conflicts:

```text
1. Add templates and examples.
2. Add agile-v-aibom skill.
3. Add docs.
4. Update routing guide.
5. Update core/build/verifier/auditor/release skills.
6. Update quality gates and control matrix.
7. Update README/EXAMPLES/agent instructions.
8. Add tests.
9. Update changelog/release notes.
```

---

## 25. Key wording for project positioning

Use this phrase consistently:

> Agile-V traces not only the engineered artifact, but also the AI system context that influenced the artifact.

And:

> SBOM tells us what software components are in the system. AI/ML-BOM and Agent Run BOM tell us what AI components influenced the engineering process and runtime behavior.

---

## 26. Final recommendation

Make `agile-v-aibom` a default companion skill for any L2+ AI-assisted work.

For low-risk tasks, keep it lightweight. For regulated, security-critical, firmware, PCB, medical, GxP, or release-critical work, make AI Influence Traceability mandatory.

This turns Agile-V from:

```text
verified AI-assisted engineering
```

into:

```text
verified and AI-provenance-aware engineering
```

That is the right direction for agentic development in regulated and high-assurance environments.
