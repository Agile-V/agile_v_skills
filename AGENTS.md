# AGENTS.md — Agile V Skills Library

> Guidelines for AI coding agents operating in this repository.

## Branch Context

**You are on the `feature-business` development branch** (version `2.0.0-dev.1`).
This is a development fork of the official Agile V augmented engineering framework,
whose stable release is **v1.5.0 on `main`**.

This branch adds 4 **draft** Business Track skills that have NOT been officially
released: `venture-strategist`, `rd-innovator`, `gtm-executor`, `business-operations`.
These skills carry `metadata.status: draft` in their YAML frontmatter. Content,
contracts, and artifact formats may change before merging to `main`.

**Official (released) skills:** All engineering track skills from v1.5.0 (`main`).
**Draft (unreleased) skills:** The 4 business track skills listed above.

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
├── agile-v-pipeline/       # Orchestration, waves, handoffs
├── agile-v-lifecycle/      # Multi-cycle management, change requests
├── agile-v-compliance/     # Risk, CAPA, gates, security, revalidation
├── agile-v-product-owner/  # Sprint-based delivery, backlog management
├── requirement-architect/  # Intent → formal requirements
├── logic-gatekeeper/       # Ambiguity/constraint validation
├── build-agent/            # Apex: code generation (language-agnostic)
├── test-designer/          # Verification suite from requirements only
├── red-team-verifier/      # Independent verification/red teaming
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
├── domains/
│   ├── build-agent-dart/       # Dart/Flutter
│   ├── build-agent-embedded/   # C/C++ embedded/firmware
│   ├── build-agent-js/         # JavaScript/TypeScript/Web
│   └── build-agent-python/     # Python
├── docs/compliance/        # ISO/GxP compliance matrices
├── package.json            # Metadata + version only (no deps, no scripts)
├── CHANGELOG.md            # Auto-generated via standard-version
├── PERFORMANCE.md          # Token usage analysis per skill
├── SKILL_ROUTING_GUIDE.md  # Maps user intents → skills
└── V2.0_RELEASE_NOTES.md   # Draft release notes for business track
```

## Build / Lint / Test Commands

There are **no build, lint, or test commands**. This repository contains only
Markdown files with YAML frontmatter — no executable source code exists.

- **No `npm install` needed** — `package.json` holds metadata only (no deps).
- **No test suite** — validation is manual (review YAML frontmatter + content).
- **No linter configured** — no `.eslintrc`, `.prettierrc`, or `.editorconfig`.

### Versioning (CI/CD)

Versioning is automated via GitHub Actions on push to `main`:

- **Repo version:** `npx standard-version` reads Conventional Commits and bumps
  `package.json` version. Do NOT edit `package.json` version by hand.
- **Skill versions:** Each skill has independent `metadata.version` in its
  YAML frontmatter. Bump only when that skill's content/contract changes.
- **This branch** uses `2.0.0-dev.1` (semver prerelease) to indicate unreleased.

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
   - `metadata.status:` — `draft` for unreleased skills (omit for released)
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
| Directory names | `kebab-case`, matching the skill `name:` field |
| YAML strings | Quote version numbers: `"1.3"` not `1.3` |
| Tables over prose | Use Markdown tables for directives, rules, mappings |
| Compact notation | Use `;` and numbered items on single lines vs verbose bullets |
| Cross-references | `"see agile-v-core"` instead of duplicating shared concepts |
| Section headers | `##` for major sections, `###` for subsections |
| Code blocks | Use fenced blocks with language identifier for templates |
| Draft markers | Use `[Draft]` label in docs for unreleased content |

### Context Optimization

Skills MUST be context-efficient. Target guidelines from PERFORMANCE.md:

- Average released skill: ~5.6 KB (~0.7% of 200K context window)
- Largest skill should stay under ~12 KB (~1.5% of context)
- Use `sections_index` in frontmatter so agents can jump to needed sections
- Format templates show structure only — one example is sufficient
- Directive tables replace prose paragraphs

### Key Principles for Skill Content

1. **Traceability** — every artifact must link to a parent `REQ-XXXX`; halt if missing
2. **Verification** — include a sub-process for checking output against requirements
3. **Halt-and-Ask** — instruct agents to halt on ambiguous requirements, never guess
4. **Red Team Protocol** — Build Agent never verifies its own work
5. **Human Gates** — always stop at critical decision points for human approval
6. **Decision Logging** — log the "Why" behind every output (Principle #9)

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
- Do NOT present draft Business Track skills as officially released
