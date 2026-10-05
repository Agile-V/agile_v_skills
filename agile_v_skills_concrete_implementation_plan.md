# Agile-V Skills: Concrete Implementation Plan for Competitive Hardening

**Target repository:** `Agile-V/agile_v_skills`  
**Baseline reviewed:** `main` at commit `982c1f6435219f0fe83dcef485503f45a7e9717e`  
**Repository version at review:** `3.9.0`  
**Plan date:** 2026-10-05  
**Primary objective:** Evolve `agile_v_skills` from a strong assurance skill/specification library into the portable, machine-verifiable assurance contract layer for heterogeneous agentic engineering systems.

---

## 1. Executive Direction

Do **not** turn `agile_v_skills` into another coding-agent framework.

The repository's strongest defensible position is:

> Coding agents produce work. Engineering tools produce evidence. Agile-V defines whether that evidence is trustworthy, sufficient, admissible, current, independent enough, and authorized to support the next engineering transition.

The repository already has unusually strong foundations:

- 49 catalogued skills.
- 36 evidence/assurance schemas.
- `L0-L4` risk classification.
- requirements, artifact, test, verification, validation, approval and traceability records.
- Evidence Bundle v2.
- Gate Receipt.
- Evidence Source Profile.
- Evidence Property Profile.
- I0-I4 independence classes.
- Exception and Waiver Contract.
- Change-Aware Revalidation.
- Trusted Admission Context.
- Agent Tool and Delegation Contract.
- AI Influence Traceability / AI-BOM draft capability.
- cross-repository runtime conformance scenarios.
- AgentSkills.io-compatible skills.
- Claude plugin packaging.
- platform guides for Claude Code, Cursor, VS Code and GitHub Copilot.

The next development cycle should therefore focus on **interoperability, machine-enforced semantics, distribution, evidence adapters, benchmarkability and trust boundaries**, not on adding many more generic skills.

### Target state

```text
                    AGILE-V SKILLS
             normative assurance contract layer
                              |
        +---------------------+----------------------+
        |                     |                      |
        v                     v                      v
 Agent Plugins          Evidence Adapters      Conformance Corpus
 portable bundles       trusted capabilities   adversarial cases
        |                     |                      |
        +---------------------+----------------------+
                              |
                              v
                   AGILE-V RUNTIME CONTRACT
                              |
                              v
        OpenHands / Codex / Claude / Cursor / Devin /
        GitHub / GitLab / CI / Sonar / Semgrep /
        Sigstore / KiCad / Zephyr / Renode / HIL
```

---

# 2. Scope

This plan changes **`agile_v_skills` only**.

It may define interfaces that `agentic_agile_v` or other runtimes must implement, but it must not move runtime-specific execution code into this repository.

### `agile_v_skills` should own

- normative lifecycle contracts;
- normative evidence semantics;
- risk and independence semantics;
- authority and delegation record contracts;
- evidence-source and evidence-property profiles;
- schemas;
- reference semantic evaluators;
- conformance fixtures;
- benchmark cases;
- distribution profiles;
- Agent Plugin packaging definitions;
- telemetry semantic contract;
- documentation and examples.

### `agile_v_skills` should not own

- actual GitHub/GitLab merge execution;
- Kubernetes deployment execution;
- credential stores;
- production OIDC authentication;
- actual firmware flashing;
- actual PCB fabrication submission;
- a proprietary IDE;
- a proprietary tracing backend;
- vulnerability scanning engines;
- a general coding agent.

Those belong in `agentic_agile_v`, external adapters, or existing tools.

---

# 3. External Drivers Behind This Plan

## 3.1 Agent Plugins 1.0

Agent Plugins 1.0 is now a published vendor-neutral packaging specification for Agent Skills plus MCP servers.

References:

- https://agent-plugins.org/specification
- https://agent-plugins.org/

Standard layout:

```text
my-plugin/
├── plugin.json
├── skills/
│   └── some-skill/
│       └── SKILL.md
└── mcp.json
```

Agile-V currently ships Agent Skills and a Claude-specific plugin definition, but does not yet publish portable Agent Plugin packages.

**Recommendation:** Make portable Agent Plugin release artifacts a P0 deliverable.

## 3.2 OpenTelemetry GenAI conventions

OpenTelemetry now has active semantic conventions for GenAI calls, agent invocation and tool execution.

References:

- https://opentelemetry.io/blog/2026/genai-observability/
- https://opentelemetry.io/docs/specs/semconv/

**Recommendation:** Agile-V should define how lifecycle, evidence and gate events map into OpenTelemetry rather than creating a proprietary observability format.

## 3.3 Runtime AI inventory

`k8s-aibom` and CycloneDX ML-BOM show the direction of AI runtime inventory and provenance.

References:

- https://github.com/GoogleCloudPlatform/k8s-aibom
- https://cyclonedx.org/capabilities/mlbom/

Agile-V already has AI Influence Traceability and `agile-v-aibom` in draft.

**Recommendation:** Harden and graduate this capability through the normal Skill Graduation Policy rather than creating another provenance mechanism.

## 3.4 Governance features are becoming commodity

Modern coding-agent and DevSecOps products increasingly provide:

- hooks;
- sandboxes;
- tool restrictions;
- audit logs;
- approval prompts;
- policy rules;
- code-quality gates;
- security gates;
- enterprise control planes.

Agile-V must therefore differentiate on **portable evidence admission and authorized engineering transitions**, not merely on the existence of gates.

---

# 4. Priority Summary

| Priority | Workstream | Outcome |
|---|---|---|
| P0 | Agent Plugins 1.0 packaging | Portable distribution across compatible agent clients |
| P0 | Evidence Adapter Registry | Trusted semantics for evidence from real engineering tools |
| P0 | Runtime compatibility hardening | Machine-verifiable skills/runtime compatibility |
| P0 | AgileV-Bench v0.1 | Reproducible adversarial benchmark corpus |
| P1 | Delegation Contract v2 | Explicit authority attenuation across agent/subagent chains |
| P1 | Context Trust Profile | Machine-readable prompt-injection / authority boundaries |
| P1 | Agile-V OpenTelemetry Contract | Vendor-neutral lifecycle and assurance telemetry |
| P1 | Capability composition metadata | Detect missing prerequisites, conflicts and supersession |
| P1 | AI-BOM graduation | Move AI influence traceability toward candidate/stable status |
| P2 | Signed release manifests | Integrity/provenance for distributed skills and profiles |
| P2 | External adapter contribution model | Scalable ecosystem for third-party evidence adapters |

---

# 5. Phase 0 - Freeze the Current Assurance Baseline

## Goal

Before adding new contracts, make the current normative surface explicitly reproducible.

## Add

```text
release/
  ASSURANCE_RELEASE_MANIFEST.schema.json
```

Generated release artifact:

```text
ASSURANCE_RELEASE_MANIFEST.json
```

### Required fields

```json
{
  "repository": "Agile-V/agile_v_skills",
  "repository_version": "3.9.0",
  "commit": "<git-sha>",
  "contract_versions_ref": "contracts/versions.yaml",
  "catalog_ref": "catalog/skills.json",
  "catalog_digest": "sha256:...",
  "schemas_digest": "sha256:...",
  "conformance_corpus_digest": "sha256:...",
  "plugin_artifacts": [],
  "generated_at": "...",
  "generator_version": "..."
}
```

## Add tooling

```text
tools/build_release_manifest.py
```

## Tests

Add:

```text
tests/test_release_manifest.py
```

Test that:

1. `package.json` version is recorded.
2. every entry in `contracts/versions.yaml` resolves.
3. all normative schemas are included in the schema-set digest.
4. catalog digest is deterministic.
5. conformance corpus digest is deterministic.
6. the manifest references the exact Git commit.
7. generation produces byte-identical output for identical inputs except explicitly excluded timestamps.

## Acceptance criteria

- [ ] One command generates the release manifest.
- [ ] CI fails if the generated manifest does not match repository state.
- [ ] A release can always be traced to exact contracts, schemas, skill catalog and conformance corpus.
- [ ] No runtime-conformance claim is inferred from this manifest.

---

# 6. Phase 1 - Publish Portable Agent Plugin Packages

## Problem

`docs/INSTALL_PROFILES.md` currently defines installation profiles as documentation and asks users to copy skill directories manually.

The repository also contains a Claude-specific plugin manifest.

This causes distribution friction and creates a growing risk of manually maintained packaging drift.

## Design rule

**Do not reorganize the source repository just to satisfy Agent Plugins.**

Keep each skill in its current canonical location and generate Agent Plugin packages as release artifacts.

## Add directory

```text
packaging/
  agent-plugins/
    README.md
    profiles.yaml
    profile.schema.json
    schemas/
      1.0.0/
        plugin.schema.json
        mcp.schema.json
```

The vendored Agent Plugins schemas must include:

```text
source URL
upstream version
upstream digest
license/provenance note
```

Do not silently modify the vendored schemas.

## Define four stable plugin profiles

### 6.1 `agile-v-core`

```yaml
name: agile-v-core
include:
  - agile-v-core
  - requirement-architect
  - logic-gatekeeper
```

### 6.2 `agile-v-verified-build`

```yaml
name: agile-v-verified-build
include:
  - agile-v-core
  - requirement-architect
  - logic-gatekeeper
  - build-agent
  - test-designer
  - red-team-verifier
  - agile-v-quality-gates
```

Domain build skill is selected separately or built as variants.

### 6.3 `agile-v-regulated`

Include only **released** skills by default.

Draft skills such as `agile-v-aibom`, `agile-v-human-oversight`, and `agile-v-gxp-qualification` must not silently appear in a stable package.

Create explicit preview package only if desired:

```text
agile-v-regulated-preview
```

### 6.4 `agile-v-embedded`

Include:

```text
agile-v-core
requirement-architect
logic-gatekeeper
build-agent
domains/build-agent-embedded
test-designer
red-team-verifier
safety-engineer
schematic-generator
agile-v-quality-gates
```

Do not claim full PCB/firmware assurance merely because the package contains embedded skills.

## Add build tool

```text
tools/build_agent_plugins.py
```

Input:

```text
catalog/skills.json
packaging/agent-plugins/profiles.yaml
package.json
```

Output:

```text
dist/agent-plugins/
  agile-v-core-3.9.0/
  agile-v-verified-build-3.9.0/
  agile-v-regulated-3.9.0/
  agile-v-embedded-3.9.0/
```

Each output:

```text
plugin.json
skills/
LICENSE
CHANGELOG.md
AGILE_V_PACKAGE_MANIFEST.json
```

`mcp.json` is OPTIONAL.

Do not include an MCP server until a stable runtime MCP contract exists.

## Generated `plugin.json`

Example:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "agile-v-verified-build",
  "version": "3.9.0",
  "description": "Agile-V verified engineering lifecycle skills"
}
```

Use only fields allowed by Agent Plugins 1.0.

Client-specific metadata belongs under the specification's extension mechanism, not as invented top-level fields.

## Add tests

```text
tests/test_agent_plugin_profiles.py
tests/test_agent_plugin_build.py
```

Validate:

- profile contains no unknown skill;
- every skill prerequisite is satisfied;
- stable package does not contain a draft skill;
- copied `SKILL.md` is byte-identical to canonical source;
- every copied asset stays within plugin root;
- `plugin.json` validates against Agent Plugins 1.0;
- package has no duplicate skill names;
- package is deterministic;
- package manifest records canonical source path and source commit.

## CI

Add:

```text
.github/workflows/build-agent-plugins.yml
```

Triggers:

```text
pull_request
push to main
release
workflow_dispatch
```

On release:

1. generate all stable plugin packages;
2. validate;
3. zip each package;
4. generate SHA-256;
5. attach to GitHub release.

## Documentation changes

Update:

```text
README.md
docs/INSTALL_PROFILES.md
SKILL_ROUTING_GUIDE.md
```

New preferred installation flow:

```text
1. Install a published Agent Plugin if client supports Agent Plugins 1.0.
2. Otherwise install the corresponding Agent Skills profile manually.
```

## Acceptance criteria

- [ ] Four deterministic portable package profiles build.
- [ ] Agent Plugins 1.0 schema validation passes.
- [ ] Stable bundles contain no draft skills.
- [ ] No skill has a second manually maintained source copy.
- [ ] Release artifacts contain source commit and package digest.
- [ ] Existing Claude/Cursor/manual paths remain supported.

---

# 7. Phase 2 - Create the Agile-V Evidence Adapter Registry

## Why this matters

This should become one of Agile-V's central differentiators.

The current Evidence Admission Contract already distinguishes:

```text
evidence exists
!= evidence is sufficient
!= evidence is admissible
```

The repository also already has:

```text
EVIDENCE_SOURCE_PROFILE.schema.json
EVIDENCE_PROPERTY_PROFILE.schema.json
```

The missing piece is an official, reviewed registry of profiles for evidence produced by real engineering tools.

## New structure

```text
profiles/
  evidence-sources/
    pytest-junit-v1.yaml
    github-actions-v1.yaml
    sonarqube-quality-gate-v1.yaml
    semgrep-findings-v1.yaml
    sigstore-attestation-v1.yaml
    k8s-aibom-v1.yaml
    kicad-erc-v1.yaml
    kicad-drc-v1.yaml
    zephyr-twister-v1.yaml
    renode-simulation-v1.yaml

  evidence-properties/
    requirement-satisfaction-L0.yaml
    requirement-satisfaction-L1.yaml
    requirement-satisfaction-L2.yaml
    requirement-satisfaction-L3.yaml
    requirement-satisfaction-L4.yaml
    static-security-analysis-L2.yaml
    hardware-electrical-rule-check-L3.yaml
    firmware-hil-L4.yaml

catalog/
  evidence-adapters.json
  evidence-adapter-catalog.schema.json
```

## Initial adapters

Start with 10 high-value sources.

### 7.1 pytest / JUnit

May establish:

```text
test_execution
observed_test_outcome
test_case_identity
execution_timestamp
subject_under_test
```

May NOT establish:

```text
human_authority
organizational_independence
intended_use_validation
regulatory_compliance
complete_security
```

### 7.2 GitHub Actions

May establish:

```text
workflow_execution
job_result
workflow_identity
commit_identity
artifact_reference
```

May NOT establish:

```text
semantic_correctness
human_authority
requirement_satisfaction_by_itself
```

### 7.3 SonarQube quality gate

May establish:

```text
static_analysis_executed
configured_quality_gate_result
reported_issue_counts
coverage_measurement_if_supplied
hotspot_review_state_if_supplied
```

May NOT establish:

```text
intended_use_validation
runtime_correctness
security_complete
human_release_authority
```

### 7.4 Semgrep

May establish:

```text
ruleset_executed
finding_presence
finding_absence_within_ruleset_scope
ruleset_identity
subject_digest
```

May NOT establish:

```text
absence_of_all_vulnerabilities
regulatory_compliance
system_safety
human_authority
```

### 7.5 Sigstore / DSSE attestation

May establish:

```text
attestation_integrity
signer_identity_if_verified
subject_digest_binding
provenance_statement_integrity
```

May NOT establish:

```text
semantic_correctness
quality
safety
test_sufficiency
```

### 7.6 k8s-aibom

May establish only what the actual BOM and confidence/evidence locator support.

Do not translate:

```text
declared -> verified
inferred -> verified
unresolved -> known
```

### 7.7 KiCad ERC

May establish:

```text
erc_executed
erc_result
erc_rule_set
schematic_subject
```

May NOT establish:

```text
board_is_safe
manufacturable
functional_in_real_hardware
human_EE_approval
```

### 7.8 KiCad DRC

Equivalent scope for layout/design-rule evidence.

### 7.9 Zephyr Twister

May establish:

```text
test_suite_execution
target_configuration
test_outcome
build_outcome_if_captured
```

### 7.10 Renode

May establish:

```text
simulation_execution
simulation_target
observed_simulated_behavior
trace_reference
```

May NOT establish:

```text
physical_hardware_behavior
EMC
electrical_safety
real_HIL_success
```

## Important governance rule

Evidence producers must **not** be able to edit the trusted profile that defines what their evidence may establish during the same task.

Treat profiles as policy-side artifacts.

## Add normative contract

```text
docs/agile-v-runtime/15_EVIDENCE_ADAPTER_REGISTRY.md
```

Define:

- profile identity;
- immutable digest;
- profile owner;
- source version scope;
- evidence type;
- `may_establish`;
- `may_not_establish`;
- minimum evidence locators;
- freshness policy;
- known limitations;
- deprecation;
- supersession;
- historical resolution rules.

## Add tooling

```text
tools/build_evidence_adapter_catalog.py
```

Generated catalog entry:

```json
{
  "adapter_id": "EAD-sonarqube-quality-gate-v1",
  "profile_path": "profiles/evidence-sources/sonarqube-quality-gate-v1.yaml",
  "profile_digest": "sha256:...",
  "status": "stable",
  "owner": "Agile-V",
  "evidence_type": "static_analysis"
}
```

## Extend `contracts/versions.yaml`

Add:

```yaml
evidence_adapter_registry: "1.0"
```

Do not bump unrelated schema versions.

## Tests

```text
tests/test_evidence_adapter_registry.py
tests/test_evidence_source_capabilities.py
```

Required adversarial tests:

- source overclaims `human_authority`;
- source profile digest changed;
- profile ID same but content changed;
- evidence type does not match source profile;
- source profile missing;
- superseded profile used without historical resolution;
- evidence locator absent when profile requires it;
- adapter claims property in `may_not_establish`;
- tool version outside supported range;
- untrusted producer supplies its own profile.

## Acceptance criteria

- [ ] At least 10 reviewed source profiles.
- [ ] At least 5 property profiles.
- [ ] Registry is deterministic and machine-readable.
- [ ] Aggregate semantics can resolve profiles exclusively from trusted registry input.
- [ ] No evidence source can expand its own authority.
- [ ] Historical profile resolution works by exact digest.
- [ ] Documentation clearly states that adapters describe evidence capability, not tool quality.

---

# 8. Phase 3 - Runtime Compatibility Must Become Release-Verifiable

## Current problem

`contracts/AGILE_V_RUNTIME_COMPATIBILITY.yaml` currently marks `agentic_agile_v` as:

```yaml
minimum_version: null
verification_status: unverified
```

The repository's runtime status document records successful cross-repository checks against an unreleased runtime branch/PR, but correctly does not treat that as released conformance.

This is the right safety posture.

The next step is to automate the release verification path.

## Add schema

```text
schemas/RUNTIME_COMPATIBILITY.schema.json
```

Apply to:

```text
contracts/AGILE_V_RUNTIME_COMPATIBILITY.yaml
```

## Runtime compatibility record

Require:

```yaml
runtime:
  id: agentic_agile_v
  repository: Agile-V/agentic_agile_v
  release: "<release-tag>"
  artifact_digest: "sha256:..."
  compatibility_manifest_digest: "sha256:..."

verified_against:
  contracts_commit: "<skills-commit>"
  contract_versions_digest: "sha256:..."
  conformance_corpus_digest: "sha256:..."

results:
  positive: ...
  rejected_as_expected: ...
  mismatches: ...
  skipped: ...

status: verified | failed | partial | unverified
```

## Add workflow

```text
.github/workflows/runtime-conformance.yml
```

Modes:

### Pull request mode

Run only against explicitly configured test runtime.

Result:

```text
informational
```

Never write `verified`.

### Release verification mode

Input:

```text
runtime repository
runtime release tag
runtime artifact digest
runtime compatibility manifest
```

Process:

1. download immutable runtime release artifact;
2. verify artifact digest;
3. install in clean environment;
4. run `tests/test_runtime_conformance.py`;
5. compare normalized decisions and reason codes;
6. generate compatibility record;
7. optionally open PR updating compatibility status.

## Critical rule

A mutable branch or PR SHA is not enough to claim a supported runtime release.

## Acceptance criteria

- [ ] Runtime compatibility file is schema validated.
- [ ] `verified` can only reference immutable released artifact identity.
- [ ] CI reproduces the compatibility result from scratch.
- [ ] conformance corpus digest is recorded.
- [ ] compatibility status does not update automatically on partial/failed/skip.
- [ ] skipped tests are never presented as conformance.

---

# 9. Phase 4 - Publish `AgileV-Bench` v0.1

## Goal

Turn the existing conformance scenarios and negative journeys into a public benchmark corpus.

This is necessary both academically and competitively.

## Do not confuse three things

```text
unit test
!= reference semantic conformance
!= live agent/runtime benchmark
```

Keep the distinction explicit.

## New structure

```text
benchmarks/
  agilev-bench/
    README.md
    VERSION
    benchmark.schema.json
    result.schema.json
    cases/
      evidence/
      approvals/
      independence/
      waivers/
      revalidation/
      delegation/
      context-trust/
      ai-provenance/
      software/
      firmware/
      pcb/
    manifests/
      v0.1.yaml
```

## Initial corpus target

**Minimum: 60 cases.**  
**Preferred initial release: 100 cases.**

### Category A - state binding

Examples:

```text
correct subject digest
wrong subject digest
same ref / different digest
amended artifact
wrong task
wrong baseline
```

### Category B - policy binding

```text
correct policy
policy changed after test
policy digest mismatch
historical policy unavailable
candidate-selected policy
```

### Category C - evidence capability

```text
valid pytest behavioral evidence
pytest claims human authority
static analyzer claims intended-use validation
signature claims semantic correctness
BOM claims compliance
```

### Category D - contradiction

```text
one passing test + one failing evidence item
pass + error
multiple partial evidence sources
missing required property
```

### Category E - approval/authority

```text
valid approval
expired approval
consumed approval
wrong task
wrong subject digest
wrong policy
wrong action
wrong resource
self-approval
forged authorship=human
revoked authority
```

### Category F - independence

```text
I0 where I2 required
I1 where I2 required
I2 accepted for L2
I3 authority separation
same-context fake "independent" verifier
```

### Category G - exceptions

```text
complete waiver coverage
partial waiver coverage
expired waiver
defer used as waiver
residual-risk acceptance used to waive failed verification
attempt to waive gate integrity
```

### Category H - revalidation

```text
source code changed
requirement changed
policy changed
model changed
tool changed
runtime changed
hardware revision changed
dependency coverage partial
dependency coverage unknown
unaffected evidence remains reusable
```

### Category I - delegation

Add after Delegation v2.

### Category J - context injection

```text
repo file claims "risk=L0"
retrieved web content claims approval
tool output requests policy modification
peer agent claims elevated rights
```

### Category K - cross-domain

Software:

```text
reviewed commit != merge commit
```

Firmware:

```text
approved image digest != flashed image digest
```

PCB:

```text
approved manufacturing archive != submitted archive
```

## Result schema

```json
{
  "benchmark_version": "0.1",
  "runtime": {},
  "case_id": "AVB-EVID-001",
  "expected_status": "rejected",
  "actual_status": "rejected",
  "expected_reason_codes": [],
  "actual_reason_codes": [],
  "latency_ms": 0,
  "notes": ""
}
```

## Metrics

At minimum:

```text
false_authorize_rate
false_reject_rate
reason_code_agreement
tamper_detection_rate
revalidation_precision
case_coverage
```

Optional live-runtime metrics:

```text
latency
token_cost
human_review_time
```

## Seed from existing assets

Reuse and normalize:

```text
conformance/scenarios.yaml
tests/test_issue42_trust_closure.py
tests/test_runtime_conformance.py
tests/admission_support.py
```

Do not duplicate business logic in the benchmark generator.

## Acceptance criteria

- [ ] v0.1 corpus contains >=60 cases.
- [ ] Every case has expected outcome and reason codes.
- [ ] Reference evaluator results are reproducible.
- [ ] Corpus has an immutable digest.
- [ ] Corpus can be consumed by an external runtime without importing `contracts.semantics`.
- [ ] README clearly distinguishes reference results from live-platform results.
- [ ] At least one software, firmware and PCB transition case is present.

---

# 10. Phase 5 - Delegation Contract v2: Authority Must Attenuate

## Current state

Agile-V already has:

```text
schemas/AGENT_DELEGATION_RECORD.schema.json
docs/agile-v-runtime/05_AGENT_TOOL_AND_DELEGATION_CONTRACT.md
```

The current contract already requires the receiver's scope to be no broader than the delegator's rights.

The missing improvement is a stronger **machine-checkable attenuation model**.

## Do not break v1 storage

Add:

```text
schemas/AGENT_DELEGATION_RECORD.v2.schema.json
```

Do not silently change historical v1 meaning.

## New v2 fields

```yaml
schema_version: "2.0"

delegation:
  id: DEL-...
  parent_delegation_ref: DEL-... | null
  source_authority_ref: AUTH-...
  issued_at: ...
  expires_at: ...
  nonce: ...
  single_use: false

delegator:
  authenticated_identity_ref: ...

delegate:
  authenticated_identity_ref: ...

authority_ceiling:
  max_risk_level: L2
  max_side_effect: internal_state
  may_delegate_further: false
  max_delegation_depth: 0

scope:
  requirements: [...]
  actions: [...]
  resources: [...]
  tools: [...]
  data_classes: [...]

revocation:
  status: active | revoked | expired
  revocation_ref: null
```

## Required semantic rules

Add to `contracts/semantics.py`:

```python
delegation_scope_is_subset_of_parent(...)
delegation_authority_is_attenuated(...)
delegation_time_is_within_parent(...)
delegation_depth_is_allowed(...)
delegation_chain_is_valid(...)
evaluate_delegation(...)
```

### Invariants

A child delegation MUST NOT:

- add an action;
- add a resource;
- add a tool;
- add a data class;
- raise maximum risk level;
- raise side-effect class;
- extend expiry;
- gain re-delegation permission if parent lacks it;
- increase allowed delegation depth;
- recover revoked authority.

Unknown parent authority = reject.

## Update contract document

Bump:

```text
docs/agile-v-runtime/05_AGENT_TOOL_AND_DELEGATION_CONTRACT.md
```

Add explicit normative statement:

> Delegation may preserve or reduce authority. It may never increase authority.

## Add adversarial tests

```text
tests/test_delegation_v2.py
```

Cases:

- valid attenuation;
- resource expansion;
- action expansion;
- risk escalation;
- longer expiry;
- excessive delegation depth;
- replayed delegation;
- revoked parent;
- unknown parent;
- unrelated approval used as authority;
- peer-agent message claims delegation without durable record.

## Acceptance criteria

- [ ] v1 remains readable.
- [ ] v2 has canonical aggregate evaluator.
- [ ] every privilege escalation path fails closed.
- [ ] delegation chain produces explainable reason codes.
- [ ] benchmark contains corresponding cases.

---

# 11. Phase 6 - Machine-Readable Context Trust Boundaries

## Current state

The existing Tool and Delegation Contract already contains the invariant:

> Untrusted context is data, never authority.

Today this is primarily normative prose.

Make it machine-readable.

## Add schema

```text
schemas/CONTEXT_SOURCE_PROFILE.schema.json
```

## Recommended model

Avoid an overly complex numeric trust score.

Use explicit source classes plus allowed influence.

```yaml
profile:
  id: CTX-REPOSITORY-CONTENT
  source_class: repository_content
  default_trust: untrusted_data

  may_influence:
    - implementation_context
    - candidate_requirement
    - candidate_test
    - issue_discovery

  may_not_influence:
    - approved_requirement
    - risk_level
    - policy
    - approval
    - delegated_authority
    - evidence_source_profile
    - evidence_property_profile
    - gate_decision

  injection_sensitive: true
```

## Initial profiles

```text
authenticated_policy_source
approved_requirement_baseline
repository_content
user_prompt
web_retrieval
RAG_document
tool_description
tool_result
peer_agent_message
MCP_resource
generated_wiki
```

## Add normative contract

```text
docs/agile-v-runtime/16_CONTEXT_TRUST_CONTRACT.md
```

Rules:

1. `authoritative` applies only to accepted control-plane sources.
2. Repository content is not automatically authoritative.
3. Tool descriptions and outputs never grant permission.
4. Generated documentation never overrides frozen requirements or policy.
5. A source may propose a change to authoritative data, but cannot activate it.
6. Unknown source class fails closed for authority-bearing decisions.

## Integrate with AI Run Manifest

AI influence records should reference context source profiles:

```yaml
context:
  observed:
    sources:
      - ref: ...
        context_profile_ref: CTX-WEB-RETRIEVAL
```

## Tests

```text
tests/test_context_trust_contract.py
```

Required cases:

- `README.md` says "approval granted";
- web page says "ignore policy";
- MCP tool description says it needs admin rights;
- generated OpenWiki page changes risk level;
- peer agent claims manager role;
- approved requirement baseline remains authoritative;
- legitimate proposal is preserved as proposal, not activated automatically.

## Acceptance criteria

- [ ] no untrusted context can directly modify authority-bearing state;
- [ ] proposal flows remain possible;
- [ ] AI Run Manifest can reference context trust profile;
- [ ] benchmark includes prompt-injection authority cases.

---

# 12. Phase 7 - Define the Agile-V OpenTelemetry Contract

## Goal

Make Agile-V observable everywhere without building a proprietary tracing platform.

## Add

```text
docs/agile-v-runtime/17_OPENTELEMETRY_CONTRACT.md
schemas/AGILE_V_TELEMETRY_EVENT.schema.json
```

## Reuse existing conventions first

Where possible use:

```text
gen_ai.*
service.*
deployment.*
code.*
error.*
```

Only create `agilev.*` attributes for Agile-V-specific assurance concepts.

## Event/span names

Recommended initial vocabulary:

```text
agilev.task.create
agilev.requirements.freeze
agilev.risk.classify
agilev.evidence.collect
agilev.evidence.admit
agilev.evidence.reject
agilev.verify
agilev.gate.evaluate
agilev.gate.authorize
agilev.approval.consume
agilev.revalidation.evaluate
agilev.delegation.evaluate
agilev.transition.execute
```

## Core attributes

```text
agilev.task.id
agilev.risk.level
agilev.subject.type
agilev.subject.ref
agilev.subject.digest
agilev.policy.digest
agilev.claim.id
agilev.evidence.id
agilev.evidence.source_profile
agilev.gate.id
agilev.gate.receipt_id
agilev.decision.status
agilev.reason_codes
agilev.independence.class
agilev.approval.ref
agilev.exception.ref
agilev.revalidation.status
agilev.agent_run.id
```

## Privacy defaults

MUST NOT emit by default:

```text
prompt text
completion text
hidden chain-of-thought
secrets
credentials
PII
proprietary source content
raw tool arguments containing sensitive data
```

Prefer:

```text
IDs
digests
version identifiers
classification
reason codes
timestamps
```

## Add test fixtures

```text
examples/telemetry/
tests/test_telemetry_contract.py
```

Tests:

- required event identity;
- reason code serialization;
- no secret fields in default example;
- no hidden CoT field;
- subject/policy digests valid;
- event can correlate to AI Run Manifest and Gate Receipt.

## Acceptance criteria

- [ ] one documented mapping to OpenTelemetry.
- [ ] no proprietary collector required.
- [ ] privacy-safe default profile.
- [ ] examples can be visualized in a generic OTEL backend.
- [ ] telemetry is explicitly **observability**, not evidence admission by itself.

---

# 13. Phase 8 - Add Capability Composition Metadata

## Problem

Agent Plugins solves packaging, not the full semantics of combining assurance capabilities.

Agile-V already has skill prerequisites in `catalog/skills.json`.

Extend this model rather than inventing a parallel one.

## Update catalog schema

Add optional fields:

```json
{
  "capabilities": {
    "provides": [
      "org.agile-v.verification.independent"
    ],
    "requires": [
      "org.agile-v.requirements.baseline"
    ],
    "conflicts": [],
    "supersedes": []
  }
}
```

## Capability naming

Use stable reverse-domain names:

```text
org.agile-v.requirements.baseline
org.agile-v.verification.independent
org.agile-v.validation.intended-use
org.agile-v.risk.classification
org.agile-v.evidence.admission
org.agile-v.ai-influence.inventory
org.agile-v.hardware.schematic
```

## Build-time checks

Plugin profile builder must reject:

- missing required capability;
- duplicate exclusive capability;
- direct conflict;
- released profile depending on draft-only capability;
- superseded capability when current version required.

## Important distinction

Capability metadata helps package composition.

It does **not** prove that a runtime actually implements the behavior correctly.

Keep runtime conformance separate.

## Acceptance criteria

- [ ] every released skill has at least one `provides`.
- [ ] every prerequisite is representable through capability metadata.
- [ ] plugin builder validates composition.
- [ ] manual skill installation remains possible.

---

# 14. Phase 9 - Graduate AI Influence Traceability Deliberately

## Current state

`agile-v-aibom` is correctly marked `draft`.

Do not simply mark it released because AI-BOM is strategically important.

Use the repository's own Skill Graduation Policy.

## Target

First target:

```text
draft -> candidate
```

Only target `stable` after independent external feedback and required scenarios are complete.

## Required work

### 14.1 Evidence-source integrations

Create source profiles for:

```text
agent session metadata
OpenTelemetry GenAI trace
k8s-aibom
container image digest
Git commit
Agent Plugin package digest
```

### 14.2 E2E scenario 1

Software agent task:

```text
model A / runtime A
-> code change
-> verification
-> model changes to B
-> determine exact affected evidence
-> revalidation triggered only where required
```

### 14.3 E2E scenario 2

Kubernetes agent/inference workload:

```text
declared AI manifest
+
observed k8s-aibom
-> discrepancy
-> unresolved/inferred fields retained
-> release decision sees confidence difference
```

### 14.4 Negative tests

- declared model presented as verified;
- unknown runtime silently accepted;
- model change does not trigger configured revalidation;
- plugin/skill version changed without influence diff;
- hidden CoT accidentally captured;
- secret captured in manifest;
- incompatible CycloneDX translation.

## Candidate graduation evidence

Persist under:

```text
.agile-v/graduation/agile-v-aibom/
```

Include:

```text
review record
negative-test result
E2E scenario evidence
known limitations
compatibility statement
changelog
```

## Acceptance criteria

- [ ] graduation criteria are met by evidence, not assertion.
- [ ] no unresolved material identity is flattened into verified.
- [ ] AI-BOM diff maps to Change-Aware Revalidation.
- [ ] CycloneDX export is explicitly an export/view, not the normative internal contract.
- [ ] hidden CoT remains excluded.

---

# 15. Phase 10 - Strengthen Release Integrity

## Goal

Consumers should be able to prove exactly which Agile-V skill and profile set they installed.

## Release outputs

For each GitHub release publish:

```text
agile-v-core-<version>.zip
agile-v-verified-build-<version>.zip
agile-v-regulated-<version>.zip
agile-v-embedded-<version>.zip

SHA256SUMS
ASSURANCE_RELEASE_MANIFEST.json
```

## Recommended provenance

Use GitHub artifact attestation or Sigstore/in-toto-compatible provenance if practical.

Do not claim that signed packaging proves that the skills are correct.

It proves integrity/provenance of the package.

## Skill provenance

Generated package manifest must record per skill:

```yaml
skill: red-team-verifier
source_repository: Agile-V/agile_v_skills
source_commit: ...
source_path: red-team-verifier/
skill_version: ...
content_digest: sha256:...
```

This extends the existing generated-copy provenance rule.

## Acceptance criteria

- [ ] package integrity can be independently verified.
- [ ] canonical source commit can be reconstructed.
- [ ] all installed skill content has digest.
- [ ] provenance language does not overclaim semantic correctness.

---

# 16. External Evidence Adapter Contribution Model

After the first official registry is stable, make it possible for vendors and users to contribute adapters.

## Add

```text
docs/CONTRIBUTING_EVIDENCE_ADAPTERS.md
templates/evidence-source-profile.yaml
templates/evidence-property-profile.yaml
```

## Required contribution evidence

A new adapter PR must include:

1. authoritative tool documentation;
2. exact evidence format/sample;
3. supported tool/version scope;
4. `may_establish`;
5. `may_not_establish`;
6. known limitations;
7. at least one positive fixture;
8. at least three negative/overclaim fixtures;
9. owner;
10. freshness/revalidation assumptions.

## Review rule

A vendor's own contribution is not automatically trusted merely because the vendor authored it.

Repository maintainers approve the Agile-V capability profile.

## Status model

```text
experimental
candidate
stable
deprecated
```

Use the same evidence-based graduation philosophy as skills.

---

# 17. Repository Tree After Implementation

Recommended additions:

```text
agile_v_skills/
├── packaging/
│   └── agent-plugins/
│       ├── README.md
│       ├── profiles.yaml
│       ├── profile.schema.json
│       └── schemas/
│
├── profiles/
│   ├── evidence-sources/
│   ├── evidence-properties/
│   └── context-sources/
│
├── benchmarks/
│   └── agilev-bench/
│       ├── README.md
│       ├── VERSION
│       ├── benchmark.schema.json
│       ├── result.schema.json
│       ├── cases/
│       └── manifests/
│
├── release/
│   └── ASSURANCE_RELEASE_MANIFEST.schema.json
│
├── tools/
│   ├── build_agent_plugins.py
│   ├── build_evidence_adapter_catalog.py
│   ├── build_release_manifest.py
│   └── validate_benchmark.py
│
├── schemas/
│   ├── AGENT_DELEGATION_RECORD.v2.schema.json
│   ├── CONTEXT_SOURCE_PROFILE.schema.json
│   ├── RUNTIME_COMPATIBILITY.schema.json
│   └── AGILE_V_TELEMETRY_EVENT.schema.json
│
├── docs/agile-v-runtime/
│   ├── 15_EVIDENCE_ADAPTER_REGISTRY.md
│   ├── 16_CONTEXT_TRUST_CONTRACT.md
│   └── 17_OPENTELEMETRY_CONTRACT.md
│
└── .github/workflows/
    ├── build-agent-plugins.yml
    ├── runtime-conformance.yml
    └── validate-control-matrix.yml
```

Do not commit generated `dist/` artifacts to source control unless there is a strong repository policy reason.

Publish them as CI/release artifacts.

---

# 18. Required `contracts/versions.yaml` Changes

Only bump/add versions when the corresponding normative contract actually changes.

Target after this plan:

```yaml
contracts:
  canonical_lifecycle_contract: "1.0"
  risk_classification: "1.0"
  evidence_admission_contract: "1.1"
  independence_classes: "1.0"
  exception_and_waiver_contract: "1.1"
  change_aware_revalidation: "1.0"
  risk_assessment_v2: "1.0"
  governance_conversion_contract: "1.0"
  skill_graduation_policy: "1.0"
  conformance_catalog: "1.0"
  trusted_admission_context: "1.0"
  aggregate_semantics: "2.0"

  evidence_adapter_registry: "1.0"
  context_trust_contract: "1.0"
  opentelemetry_contract: "1.0"
  delegation_contract: "2.0"

  agent_delegation_record_v2: "2.0"
  context_source_profile: "1.0"
  runtime_compatibility: "1.0"
  agile_v_telemetry_event: "1.0"
```

Do not renumber old historical schemas merely for aesthetic consistency.

---

# 19. CI Pipeline Changes

Target CI stages:

```text
1. validate skill metadata
2. validate catalog
3. validate all schemas
4. run contract semantics tests
5. validate source/property/context profiles
6. build evidence-adapter catalog
7. validate benchmark corpus
8. build Agent Plugin profiles
9. validate Agent Plugin schemas
10. run normal test suite
11. optionally run external runtime conformance
12. generate release manifest
```

## Pull requests

PR must fail on:

- schema drift;
- catalog drift;
- plugin profile drift;
- invalid stable/draft composition;
- evidence-profile overclaims;
- benchmark malformed case;
- generated release-manifest mismatch.

External runtime absence may skip external conformance, but the UI/text must say:

```text
external runtime conformance: NOT EXECUTED
```

Never:

```text
passed
```

when it was skipped.

---

# 20. Recommended GitHub Governance

The repository currently has no open issues, so create implementation issues from this plan rather than attempting one giant PR.

## Add CODEOWNERS

Recommended:

```text
/contracts/                  @Agile-V/<assurance-maintainers>
/schemas/                    @Agile-V/<assurance-maintainers>
/docs/agile-v-runtime/       @Agile-V/<assurance-maintainers>
/profiles/                   @Agile-V/<assurance-maintainers>
/packaging/agent-plugins/    @Agile-V/<distribution-maintainers>
/benchmarks/                 @Agile-V/<assurance-maintainers>
```

Replace placeholders with actual GitHub teams/users.

Where possible, branch protection should require CODEOWNER review for normative changes.

## Normative-change PR checklist

Every normative contract PR should answer:

```text
What behavior changes?
Is change backward compatible?
Which schema/contract version changes?
Which positive test proves intended behavior?
Which negative tests prove failure behavior?
Does conformance corpus change?
Does a runtime implementation need an update?
Does an evidence profile need revalidation?
```

---

# 21. Concrete Issue Backlog

Create these as separate GitHub issues.

## AVS-01 - Agent Plugins 1.0 portable package builder

**Priority:** P0

Deliver:

```text
packaging/agent-plugins/
tools/build_agent_plugins.py
tests/test_agent_plugin_build.py
.github/workflows/build-agent-plugins.yml
```

Acceptance:

- four profiles build;
- v1 schema valid;
- deterministic;
- no draft leakage;
- release ZIPs generated.

---

## AVS-02 - Evidence Adapter Registry v1

**Priority:** P0

Deliver:

```text
profiles/evidence-sources/
profiles/evidence-properties/
catalog/evidence-adapters.json
docs/agile-v-runtime/15_EVIDENCE_ADAPTER_REGISTRY.md
```

Acceptance:

- >=10 source adapters;
- >=5 property profiles;
- digest-bound registry;
- positive and negative tests.

---

## AVS-03 - Runtime compatibility release verification

**Priority:** P0

Deliver:

```text
schemas/RUNTIME_COMPATIBILITY.schema.json
.github/workflows/runtime-conformance.yml
```

Acceptance:

- immutable runtime release identity;
- clean environment installation;
- conformance corpus digest;
- no verified status on skipped/branch-only run.

---

## AVS-04 - AgileV-Bench v0.1

**Priority:** P0

Deliver:

```text
benchmarks/agilev-bench/
```

Acceptance:

- >=60 cases;
- expected reason codes;
- deterministic manifest;
- software + firmware + PCB cases.

---

## AVS-05 - Delegation Contract v2

**Priority:** P1

Deliver:

```text
schemas/AGENT_DELEGATION_RECORD.v2.schema.json
contracts/semantics.py changes
delegation contract update
tests/test_delegation_v2.py
```

Acceptance:

- machine-enforced attenuation;
- no authority escalation;
- explainable rejection codes.

---

## AVS-06 - Context Trust Contract

**Priority:** P1

Deliver:

```text
schemas/CONTEXT_SOURCE_PROFILE.schema.json
profiles/context-sources/
docs/agile-v-runtime/16_CONTEXT_TRUST_CONTRACT.md
```

Acceptance:

- repository/web/tool/agent content cannot grant authority;
- proposals remain possible;
- benchmark injection cases added.

---

## AVS-07 - OpenTelemetry assurance semantic contract

**Priority:** P1

Deliver:

```text
docs/agile-v-runtime/17_OPENTELEMETRY_CONTRACT.md
schemas/AGILE_V_TELEMETRY_EVENT.schema.json
examples/telemetry/
```

Acceptance:

- OTEL mapping documented;
- privacy-safe defaults;
- no prompt/CoT/secrets required.

---

## AVS-08 - Capability composition metadata

**Priority:** P1

Deliver:

```text
catalog schema update
catalog skill capability data
plugin builder composition validation
```

Acceptance:

- `provides/requires/conflicts/supersedes`;
- stable packages cannot depend on unresolved draft capability;
- plugin build fails on conflict.

---

## AVS-09 - AI-BOM draft -> candidate evidence package

**Priority:** P1

Deliver:

```text
negative tests
2 E2E scenarios
graduation evidence
source profiles
```

Acceptance:

- satisfies candidate requirements in Skill Graduation Policy;
- no premature `stable` claim.

---

## AVS-10 - Signed/integrity-bound release packaging

**Priority:** P2

Deliver:

```text
ASSURANCE_RELEASE_MANIFEST
SHA256SUMS
artifact attestations if supported
```

Acceptance:

- package-to-source provenance independently verifiable.

---

## AVS-11 - Third-party Evidence Adapter contribution process

**Priority:** P2

Deliver:

```text
docs/CONTRIBUTING_EVIDENCE_ADAPTERS.md
templates
review checklist
```

Acceptance:

- third-party adapter cannot self-authorize;
- capability overclaims tested.

---

# 22. Recommended Implementation Order

Use this order:

```text
AVS-01 Agent Plugins
       |
       +--> AVS-08 Capability composition

AVS-02 Evidence Adapter Registry
       |
       +--> AVS-09 AI-BOM graduation
       |
       +--> AVS-11 External adapters

AVS-03 Runtime compatibility
       |
       +--> AVS-04 AgileV-Bench

AVS-05 Delegation v2
       |
       +--> AVS-04 additional benchmark cases

AVS-06 Context trust
       |
       +--> AVS-04 injection cases

AVS-07 OpenTelemetry

AVS-10 Release integrity
```

Suggested milestones:

### Milestone 1 - Portable Agile-V

```text
AVS-01
AVS-03
```

### Milestone 2 - Evidence Interoperability

```text
AVS-02
AVS-04
```

### Milestone 3 - Agentic Trust Boundaries

```text
AVS-05
AVS-06
```

### Milestone 4 - Ecosystem Integration

```text
AVS-07
AVS-08
AVS-09
```

### Milestone 5 - Supply Chain & Community

```text
AVS-10
AVS-11
```

---

# 23. What Not to Implement Yet

## Do not build an Agile-V IDE

Integrate with existing coding agents.

## Do not build a proprietary tracing UI

Emit OpenTelemetry.

## Do not create a vulnerability scanner

Create evidence-source profiles for Semgrep/Snyk/etc.

## Do not build another model gateway

Inventory and govern model/runtime use instead.

## Do not create more generic agent roles unless a real assurance gap exists

The repository already has 49 skills.

The priority is making the existing assurance model:

```text
portable
composable
machine-verifiable
benchmarkable
interoperable
```

## Do not mark preview capabilities stable to improve marketing

Use the existing graduation policy.

This restraint is itself a competitive advantage.

---

# 24. Definition of Done for This Program

The improvement program is complete when all of the following are true.

## Distribution

- [ ] Stable Agile-V profiles are available as Agent Plugins 1.0 artifacts.
- [ ] Manual Agent Skills installation remains supported.
- [ ] Generated packages contain exact canonical skill bytes.
- [ ] Package provenance is recorded.

## Evidence interoperability

- [ ] At least 10 production-relevant evidence-source profiles exist.
- [ ] Tool evidence capability is machine-readable.
- [ ] Evidence producers cannot self-expand what their output proves.
- [ ] historical source-profile digests are resolvable.

## Trust

- [ ] delegated authority is provably attenuating.
- [ ] untrusted context cannot alter policy, authority or approved baselines.
- [ ] unknown authority fails closed.

## Conformance

- [ ] AgileV-Bench v0.1 is public and reproducible.
- [ ] runtime conformance references immutable runtime release artifacts.
- [ ] skipped tests cannot become `verified` compatibility.

## Observability

- [ ] Agile-V lifecycle/gate events have an OTEL mapping.
- [ ] privacy-safe telemetry is the default.
- [ ] telemetry is not confused with evidence admission.

## AI provenance

- [ ] AI Run Manifest integrates trusted observed sources.
- [ ] AI-BOM changes connect to general revalidation.
- [ ] `agile-v-aibom` progresses only through evidence-backed graduation.

## Governance

- [ ] normative files have explicit ownership.
- [ ] contract changes state compatibility impact.
- [ ] contract/schema versions remain single-source-of-truth.

---

# 25. Expected Competitive Position After Implementation

Before:

```text
Agile-V Skills
= strong assurance method
+ unusually rich schemas/contracts
+ cross-domain thinking
- installation friction
- few concrete evidence adapters
- limited external benchmark evidence
- runtime compatibility not released/verified
```

After:

```text
Agile-V Skills
= portable assurance protocol
+ portable Agent Plugin distribution
+ trusted evidence adapter ecosystem
+ machine-checkable authority boundaries
+ public adversarial benchmark
+ runtime compatibility contract
+ cross-domain evidence semantics
+ AI provenance/revalidation
+ vendor-neutral telemetry contract
```

The resulting positioning should be:

> **Agile-V is the vendor-neutral assurance contract that defines what engineering evidence means, when it is admissible, and what it can authorize across AI-assisted software, firmware and hardware development.**

That is more durable than competing on agent generation quality, IDE features, generic orchestration or proprietary governance dashboards.

---

# 26. Source and Baseline References

## Agile-V repository baseline

- Repository: https://github.com/Agile-V/agile_v_skills
- Reviewed baseline commit: `982c1f6435219f0fe83dcef485503f45a7e9717e`
- Runtime compatibility declaration: `contracts/AGILE_V_RUNTIME_COMPATIBILITY.yaml`
- Runtime status: `conformance/RUNTIME_STATUS.md`
- Evidence Admission Contract: `docs/agile-v-runtime/07_EVIDENCE_ADMISSION_CONTRACT.md`
- Agent Tool and Delegation Contract: `docs/agile-v-runtime/05_AGENT_TOOL_AND_DELEGATION_CONTRACT.md`
- Trusted Admission Context: `docs/agile-v-runtime/14_TRUSTED_ADMISSION_CONTEXT.md`
- Skill Graduation Policy: `docs/agile-v-runtime/13_SKILL_GRADUATION_POLICY.md`

## External standards / ecosystem references

- Agent Plugins 1.0: https://agent-plugins.org/specification
- Agent Plugins home: https://agent-plugins.org/
- Agent Skills: https://agentskills.io/specification
- OpenTelemetry semantic conventions: https://opentelemetry.io/docs/specs/semconv/
- OpenTelemetry GenAI observability: https://opentelemetry.io/blog/2026/genai-observability/
- CycloneDX ML-BOM: https://cyclonedx.org/capabilities/mlbom/
- k8s-aibom: https://github.com/GoogleCloudPlatform/k8s-aibom

---

# 27. Instruction to the Implementation Agent

Implement this plan incrementally.

For every workstream:

1. inspect the current repository before editing;
2. reuse existing contracts and schemas;
3. never duplicate an existing capability under a new name;
4. preserve backward compatibility unless a versioned replacement is explicitly required;
5. add negative tests before declaring a new trust property implemented;
6. keep reference semantics in `contracts/semantics.py`;
7. keep runtime execution out of this repository;
8. update `contracts/versions.yaml` only for actual normative changes;
9. update the skill catalog and documentation in the same PR as relevant contract changes;
10. do not claim external runtime conformance unless an immutable released runtime artifact was actually tested;
11. do not graduate draft skills without evidence required by the Skill Graduation Policy;
12. produce small, reviewable PRs corresponding to the backlog above.

The order of optimization is:

```text
correctness
> trust-boundary integrity
> backward compatibility
> testability
> interoperability
> usability
> feature count
```
