# AI Run Manifest

Use an AI run manifest whenever AI materially influences requirements, architecture, code, tests, hardware artifacts, documentation, verification, or release evidence, including `L0` work.

> **Preview:** `agile-v-aibom` has `metadata.status: draft`. Review and approve its contract locally before operational use. The repository template and schema remain the source materials for a trial implementation.

## Create the Record

1. Classify the task `L0`-`L4` using [Risk Classification](../agile-v-runtime/04_RISK_CLASSIFICATION.md).
2. Copy the structure from `templates/AI_RUN_MANIFEST.yaml` into `.agile-v/aibom/<task_id>/AI_RUN_MANIFEST.yaml`.
3. Record declared model, provider, runtime, tools, loaded Agile V skills, repository revision, context sources, and influenced artifacts. Keep observed runtime evidence separate from declarations.
4. Assign `declared`, `inferred`, `verified`, or `unresolved` confidence and an evidence locator to each material field. Record a hash only when it was computed.
5. Exclude hidden chain-of-thought, API keys, secrets, personal data, and unredacted proprietary prompts. Prefer metadata, versions, configuration snapshots, logs, artifact hashes, and test locators.
6. For `L1+`, produce `AI_BOM_EVIDENCE_FRAGMENT.json` from the repository template and link it into the task evidence bundle.
7. Compare the run with the accepted baseline when required by `templates/AI_BOM_POLICY.yaml`. Record affected artifacts and the revalidation scope rather than assuming every artifact is affected.

## Risk Expectations

| Level | Minimum manifest treatment |
|---|---|
| `L0` | Task/run identity, model or tool name, and hidden-chain-of-thought exclusion; incomplete metadata is flagged |
| `L1` | Add provider/runtime, skills, repository commit, tools, and artifact influence; attach the evidence fragment |
| `L2` | Resolve model/runtime/tool identity; add versions, declared versus observed context, material hashes, evidence links, completeness, and required baseline diff/revalidation evidence |
| `L3` | Add deterministic affected scope, applicable evaluation evidence, independent review, human approval, and CycloneDX export; no unresolved material identity fields |
| `L4` | Add verified or explicitly approved runtime identity, signed/archived manifest, and authorized human approval |

At `L2+`, halt when required manifest fields are absent. A signature attests only to identified manifest bytes and the signer statement; it does not establish safety, security, compliance, verification, or validation.

## Revalidation Trigger Check

Assess changes to model provider/ID/version, inference runtime, agent framework, Agile V skill, tool access, RAG/vector/embedding sources, sandbox image, and system prompt or policy. Apply the approved policy and document whether revalidation is required, pending, complete, or risk-accepted by an authorized role.

The independent verifier checks manifest completeness and revalidation evidence in `.agile-v/VERIFICATION_SUMMARY.md`. Intended-use results, if required, remain in `VALIDATION_REPORT.md`.

Next: [Independent agent verification](independent-agent-verification.md), [Verified authentication](verified-authentication.md), or [Regulated software adoption](regulated-software-adoption.md).
