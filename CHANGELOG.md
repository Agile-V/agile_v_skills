# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [2.0.0](https://github.com/Agile-V/agile_v_skills/compare/v1.5.0...v2.0.0) (2026-05-22)


### ⚠ BREAKING CHANGES

* agile-v-core version 1.3 → 1.4 (SCOPE-V addition)

### Features

* add runtime schemas and templates ([e942f36](https://github.com/Agile-V/agile_v_skills/commit/e942f36ae028814b2ac77c9b6d0f3e20f137dfef))
* add SCOPE-V framework and build-agent-nestjs skill ([9eeb8f3](https://github.com/Agile-V/agile_v_skills/commit/9eeb8f3ce56884c335d64e65391682c4328ed6ea))
* Comprehensive domain skill enrichment and modernization ([f467a6e](https://github.com/Agile-V/agile_v_skills/commit/f467a6e5355850588a67dbddd097c5ea941cf526))

## 1.6.0 (2026-05-22)


### Features

* **agile-v-core:** Add SCOPE-V Task Execution Framework (Specify → Constrain → Orchestrate → Prove → Evolve → Verify)
* **skills:** Add build-agent-nestjs domain skill for NestJS backend development
  - Extends build-agent with NestJS architectural patterns
  - Dependency injection, API design, security, database, testing conventions
  - R0-R3 evidence requirements with NestJS-specific additions
  - SCOPE-V participation mapping
  - Upstream integration with Kadajett/agent-nestjs-skills
  - MIT license attribution preserved
* **skills:** Comprehensive enrichment of all domain build agents
  - build-agent-python: FastAPI/Flask/Django patterns, SQLAlchemy, security, testing (695 lines)
  - build-agent-js: React/Next.js/Node.js patterns, TypeScript, security, testing (900 lines)
  - build-agent-dart: Flutter/BLoC patterns, platform channels, testing (787 lines)
  - build-agent-embedded: MISRA-C, RTOS, safety standards (ISO 26262, IEC 61508), HIL/SIL testing (787 lines)
  - All include comprehensive Evidence Requirements (R0-R3) and domain-specific Halt Conditions
  - All include SCOPE-V participation and sections_index


### Changed

* **agile-v-core:** Version bumped to 1.4 (added SCOPE-V + sections_index)
* **SKILL_ROUTING_GUIDE.md:** Updated with all domain skill auto-trigger patterns
* **README.md:** Updated skills table with comprehensive domain skill descriptions
* **agile-v-compliance:** Added sections_index
* **agile-v-lifecycle:** Added sections_index
* **agile-v-pipeline:** Added sections_index


### Performance

* **skills:** Context optimization for domain skills (24.4% → 19.1% max usage)
  - Reduced code examples while maintaining quality
  - Consolidated framework coverage (primary detailed, others brief)
  - Streamlined explanations to concise bullet points
  - 100% preservation of Evidence Requirements, Halt Conditions, and security patterns
  - Result: 160KB+ remaining for user code and requirements


### Documentation

* Added NESTJS_INTEGRATION_PLAN_FINAL.md (implementation guide)
* Added STRUCTURE_REVIEW_AND_RECOMMENDATIONS.md (architecture analysis)
* Added docs/DOMAIN_SKILL_TEMPLATE.md (community contribution guide with optimization guidelines)
* Added test validation framework (9/9 tests passing)
* Added SKILLS_EFFECTIVENESS_REVIEW.md (comprehensive analysis)
* NOTICE.md in build-agent-nestjs for upstream attribution

## 1.5.0 (2026-02-27)


### Features

* add documentation skill ([31102ea](https://github.com/Agile-V/agile_v_skills/commit/31102ea9c0a582ef1dcce6a35f9901ddcbd1bf94))
* Add v1.5 Product Development Extensions ([43b3867](https://github.com/Agile-V/agile_v_skills/commit/43b3867897148faa6f4d8b638b74a38a40207c55))
* enhance skills ([5edae4e](https://github.com/Agile-V/agile_v_skills/commit/5edae4e7f7ffb0ca5ed75852562940e9a0b01bae))
* reduce context-window load, enable parallel runs ([cb5b943](https://github.com/Agile-V/agile_v_skills/commit/cb5b9436115a2fd7975e1598a066c1937f61df89))
* restructure repository for easier reference of each skill, update README.md ([fd1b32c](https://github.com/Agile-V/agile_v_skills/commit/fd1b32cd8ed1c445e3ce3b8f060bf88a22621a53))
* **skills:** add iteration lifecycle and document versioning (v1.3) ([f5d14aa](https://github.com/Agile-V/agile_v_skills/commit/f5d14aa45ee51029eda9e1f34b2cab6496a9ae54))
* **skills:** compliance hardening after ISO/GxP audit (v1.3) ([7b9d83f](https://github.com/Agile-V/agile_v_skills/commit/7b9d83f1253734c15abbc4187ccb1eec663b4b47))
* **skills:** integrate context engineering and orchestration patterns from GSD ([3e671e3](https://github.com/Agile-V/agile_v_skills/commit/3e671e3c107c4dc0aa4fa13b0e25fa806ed40f4e))
* **skills:** schematic-generator C2+ versioning; unify skill metadata version ([f3a1c0c](https://github.com/Agile-V/agile_v_skills/commit/f3a1c0ca7ae0a757326c7c5b38c1f39278a8c9b9))
