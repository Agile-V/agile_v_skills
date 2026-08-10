# AGENTS.md — Agile V Skills Library

> Guidelines for AI coding agents operating in this repository.

## Repository Context

The current repository line is **v3.8.x on `main`** (`package.json` is the repository-version source). Do not infer release status from old branch names or release-note filenames.

A skill is **preview/draft** only when its current YAML frontmatter contains `metadata.status: draft`. At v3.8.x this applies to `agile-v-aibom`, the four functional Business Track skills, `c-suite-foundation`, five `chief-*` orchestrators, and `c-suite-update`. These files are present on `main`, but their contracts remain preview and require local review before operational use. All other existing skills are current unless their own frontmatter says otherwise.

## Project Overview

This is the **Agile V Agent Skills Library** — a collection of Markdown-based
agent skill definitions (not executable code). Each skill is a `SKILL.md` file
with YAML frontmatter following the [AgentSkills.io specification](https://agentskills.io/specification).
Skills are organized in directories at the repo root, with language-specific
build agents under `domains/`.

**License:** CC-BY-SA-4.0 (all skills and contributions).

## Repository Structure

```
├── agile-v-core/           # Foundation skill (load first in any session)
├── agile-v-aibom/          # AI Influence Traceability: AI/ML-BOM and agent run provenance
├── agile-v-pipeline/       # Orchestration, waves, handoffs
├── agile-v-lifecycle/      # Multi-cycle management, change requests
├── agile-v-compliance/     # Risk, CAPA, gates, security, revalidation
├── agile-v-control-matrix/ # Agentic operating controls
├── agile-v-quality-gates/  # Interface, test, data type, and time checks
├── agile-v-behavioral/     # Implementation anti-pattern prevention
├── agile-v-product-owner/  # Sprint-based delivery, backlog management
├── requirement-architect/  # Intent → formal requirements
├── logic-gatekeeper/       # Ambiguity/constraint validation
├── build-agent/            # Apex: code generation (language-agnostic)
├── test-designer/          # Verification suite from requirements only
├── red-team-verifier/      # Independent verification/red teaming
├── validation-agent/       # Intended-use validation
├── safety-engineer/        # Hazard analysis and safety assurance
├── schematic-generator/    # Hardware schematics, netlists, HDL
├── compliance-auditor/     # Decision logging, traceability, audit
├── documentation-agent/    # Standards-based repo docs
├── discovery-analyst/      # User research → candidate requirements
├── threat-modeler/         # STRIDE analysis, privacy impact
├── ux-spec-author/         # UX specs, accessibility, design constraints
├── release-manager/        # Rollout plans, rollback, deployment
├── observability-planner/  # Metrics, dashboards, alerts, SLOs
├── venture-strategist/     # [Draft] Business: vision, product portfolio
├── rd-innovator/           # [Draft] Business: R&D pipeline, tech radar
├── gtm-executor/           # [Draft] Business: go-to-market, growth
├── business-operations/    # [Draft] Business: finance, OKRs, vendors
├── chief-exec/             # [Draft] C-Suite: CEO orchestrator, strategic alignment
├── chief-tech/             # [Draft] C-Suite: CTO orchestrator, architecture governance
├── chief-finance/          # [Draft] C-Suite: CFO orchestrator, financial governance
├── chief-people/           # [Draft] C-Suite: CHRO orchestrator, people operations
├── chief-ops/              # [Draft] C-Suite: COO orchestrator, operational excellence
├── c-suite-foundation/     # [Draft] Shared C-Suite governance primitives
├── c-suite-update/         # [Draft] Periodic executive briefings
├── skills/                 # Existing-repository understanding and evidence agents
├── domains/
│   ├── build-agent-dart/       # Dart/Flutter
│   ├── build-agent-embedded/   # C/C++ embedded/firmware
│   ├── build-agent-js/         # JavaScript/TypeScript/Web
│   ├── build-agent-nestjs/     # NestJS
│   └── build-agent-python/     # Python
├── docs/compliance/        # ISO/GxP compliance matrices
├── package.json            # Metadata + version only (no deps, no scripts)
├── CHANGELOG.md            # Maintained by Release Please
├── PERFORMANCE.md          # Reproducible performance measurement method
├── SKILL_ROUTING_GUIDE.md  # Maps user intents → skills
└── V2.0_RELEASE_NOTES.md   # Historical Business Track introduction; current status annotated
```

## Build / Lint / Test Commands

There is no application build or dependency installation. This repository contains Markdown skills plus JSON schemas and Python schema-validation tests; it has no application source code.

- **No `npm install` needed** — `package.json` holds metadata only (no deps).
- **Schema validation:** run `python -m pytest tests/test_schemas.py` when Python and `pytest`/`jsonschema` are available; otherwise review frontmatter, JSON schemas, fixtures, and content manually.
- **No linter configured** — no `.eslintrc`, `.prettierrc`, or `.editorconfig`.

### Versioning (CI/CD)

Versioning is automated via GitHub Actions on push to `main`:

- **Repo version:** Release Please reads Conventional Commits, opens a release PR,
  and updates `package.json`, distribution manifests, and `CHANGELOG.md`. Do NOT
  edit release versions by hand.
- **Skill versions:** Each skill has independent `metadata.version` in its
  YAML frontmatter. Bump only when that skill's content/contract changes.
- **Current line:** v3.8.x. Read the checked-out `package.json`; do not hard-code a branch-specific version here.

## Commit Message Convention

This repo uses **[Conventional Commits](https://www.conventionalcommits.org/)**:

```
feat: add new discovery-analyst skill        → minor bump
fix: correct frontmatter in build-agent      → patch bump
feat!: redesign pipeline orchestration       → major bump (breaking)
chore(release): 1.5.0 [skip ci]             → release commit (automated)
docs: update README with new workflow        → patch bump
```

Use scopes when appropriate: `feat(skills):`, `fix(compliance):`, `docs:`.

## Content Style Guidelines

### SKILL.md File Structure

Every skill file MUST follow this exact structure:

1. **YAML frontmatter** (between `---` fences) with required fields:
   - `name:` — kebab-case skill identifier (e.g., `build-agent-python`)
   - `description:` — single-line purpose statement
   - `license: CC-BY-SA-4.0` — mandatory
   - `metadata.version:` — quoted string (e.g., `"1.3"`)
   - `metadata.standard: "Agile V"`
   - `metadata.author:` — typically `agile-v.org`
   - `metadata.status:` — `draft` for preview/non-stable skills (omit for current skills)
   - `metadata.adapted_from:` — list if applicable (name, url, license, copyright)
   - `metadata.sections_index:` — optional list for context-optimized navigation

2. **`# Instructions`** — the top-level heading (always this exact text)

3. **Body** — structured Markdown with tables, compact notation, templates

### Formatting Rules

| Rule | Convention |
|------|------------|
| Skill names | `kebab-case` (e.g., `agile-v-core`, `build-agent-js`) |
| Requirement IDs | `REQ-XXXX` format, always referenced with prefix |
| Artifact IDs | `ART-XXXX` format |
| Test case IDs | `TC-XXXX` format |
| Business IDs | `VIS-XXXX`, `BM-XXXX`, `PORT-XXXX`, `TECH-XXXX`, etc. |
| C-Suite IDs | `EXEC-XXXX`, `ADR-XXXX`, `FM-XXXX`, `ORG-XXXX`, `PLAY-XXXX`, etc. |
| Directory names | `kebab-case`, matching the skill `name:` field |
| YAML strings | Quote version numbers: `"1.3"` not `1.3` |
| Tables over prose | Use Markdown tables for directives, rules, mappings |
| Compact notation | Use `;` and numbered items on single lines vs verbose bullets |
| Cross-references | `"see agile-v-core"` instead of duplicating shared concepts |
| Section headers | `##` for major sections, `###` for subsections |
| Code blocks | Use fenced blocks with language identifier for templates |
| Draft markers | Use `[Draft]` or `[Preview]` in docs for content whose frontmatter status is `draft` |

### Context Optimization

Skills should remain concise and stage-focused. Use `sections_index`, structure-only templates, directive tables, and cross-references where they improve navigation. Do not claim token, latency, quality, or efficiency gains without the reproducible inputs and method defined in `PERFORMANCE.md`.

### Key Principles for Skill Content

1. **Traceability** — synthesis artifacts use `artifact -> implements -> baselined requirement` with REQ ID, revision, and baseline reference; other records use applicable typed lineage. Halt rather than invent a REQ parent.
2. **Verification** — include a sub-process for checking output against requirements
3. **Halt-and-Ask** — instruct agents to halt on ambiguous requirements, never guess
4. **Red Team Protocol** — Build Agent never verifies its own work
5. **Human Gates** — always stop at critical decision points for human approval
6. **Decision Logging** — log the "Why" behind every output (Principle #9)
7. **AI Influence Traceability** — when AI materially influences any artifact, create or update `AI_RUN_MANIFEST.yaml` and link it to the evidence bundle (see `agile-v-aibom`)

**Terminology:** `red-team-verifier` independently verifies specified outputs and hands off `.agile-v/VERIFICATION_SUMMARY.md`. `validation-agent` separately assesses intended use in representative conditions and produces `VALIDATION_REPORT.md`. Never call verification evidence intended-use validation.

## AI Influence Traceability Rule

When an AI agent materially influences requirements, architecture, code, tests, PCB artifacts, firmware, documentation, verification, or release evidence, create or update an `AI_RUN_MANIFEST.yaml` and link it to the evidence bundle.

Do not store hidden chain-of-thought, secrets, API keys, or unredacted proprietary prompts. Store auditable metadata: model identity, runtime identity, tool access, skill versions, context sources, artifact hashes, test evidence, and confidence/evidence locators.

**Templates:** `templates/AI_RUN_MANIFEST.yaml` (source of truth), `templates/AI_BOM_POLICY.yaml` (risk-level rules), `templates/AI_BOM_EVIDENCE_FRAGMENT.json` (evidence bundle attachment).

### Attribution

When adapting content from external sources, include `adapted_from` in YAML
frontmatter with `name`, `url`, `license`, `copyright`, and `sections` fields.
The GSD framework (MIT, Lex Christopherson 2025) is the primary adapted source
for context engineering patterns.

## File Organization

- **One `SKILL.md` per directory** — each skill lives in its own folder
- **Domain-specific skills** go under `domains/` (e.g., `domains/build-agent-dart/`)
- **Compliance docs** live in `docs/compliance/` (numbered: `01_`, `02_`, etc.)
- **Do not create** `node_modules/`, lock files, or build artifacts
- **Do not add** executable code, scripts, or binaries to this repo

## What NOT to Do

- Do NOT edit `package.json` version — it is managed by CI/CD
- Do NOT create skills without all required YAML frontmatter fields
- Do NOT duplicate content across skills — use cross-references
- Do NOT write prose where a table would be clearer
- Do NOT add dependencies to `package.json`
- Do NOT create files outside the established directory structure
- Do NOT remove or rename the `# Instructions` heading in any SKILL.md
- Do NOT present any skill with `metadata.status: draft` as a stable operational contract
- Do NOT confuse C-Suite orchestrator skills with functional skills -- C-Suite skills govern and coordinate; functional skills execute
