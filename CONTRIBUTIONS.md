# Contributions & Attribution

This document provides a comprehensive list of all academic papers, open-source repositories, documentation, standards, and other resources that have contributed to the **Agile V Skills Library**.

---

## 📚 Academic Research

### ArXiv Papers

1. **pcbGPT: Automatic PCB Schematic Synthesis from Natural Language Requirements**
   - **Authors**: Research paper on PCB synthesis using LLMs
   - **URL**: https://arxiv.org/pdf/2606.01188
   - **Contribution**: Inspired the EDA domain skills and schematic generation approaches
   - **Referenced in**: PCB/EDA skill documentation and examples

---

## 🐙 GitHub Repositories

### Core Agile-V Ecosystem

1. **Agile-V/agile_v_skills** (This Repository)
   - **URL**: https://github.com/Agile-V/agile_v_skills
   - **License**: CC-BY-SA-4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
   - **Purpose**: Skills library for AI agents following AgentSkills.io specification
   - **Version**: 3.3.2

2. **Agile-V/agentic_agile_v**
   - **URL**: https://github.com/Agile-V/agentic_agile_v
   - **License**: Proprietary / Agile-V™
   - **Purpose**: Main implementation repository that uses this skills library
   - **Integration**: Consumes skills for agent orchestration and execution

3. **Agile-V/agile_v_cursor_plugin**
   - **URL**: https://github.com/Agile-V/agile_v_cursor_plugin
   - **Purpose**: Cursor editor plugin for Agile-V skills
   - **Referenced in**: `.github/workflows/sync-to-plugin-repo.yml:33`
   - **Integration**: Automated sync workflow for plugin distribution

### Major Framework Integrations

4. **Lum1104/Understand-Anything**
   - **URL**: https://github.com/Lum1104/Understand-Anything
   - **License**: MIT License
   - **Purpose**: Codebase comprehension tool for knowledge graph generation
   - **Integration Status**: Phase 1 complete (docs, skills, templates)
   - **Contribution**: Provides system context understanding, impact analysis, graph-based traceability, and regression-test selection
   - **Referenced in**:
     - `README.md:978`
     - `integrations/understand-anything/README.md:5`
     - 185+ matches across integration documentation and skills
   - **Integration Features**:
     - Knowledge graph generation from codebase
     - Impact analysis for changes
     - Graph-based traceability
     - Test selection based on change impact

### Upstream Pattern Sources

5. **gsd-build/get-shit-done** (GSD)
   - **URL**: https://github.com/gsd-build/get-shit-done
   - **Author**: Lex Christopherson
   - **License**: MIT License
   - **Copyright**: © 2025 Lex Christopherson
   - **Version**: v1.2 patterns integrated
   - **Contribution**: Source of context engineering, orchestration pipeline, and state persistence patterns
   - **Adapted Patterns**:
     - Context Engineering (token optimization, context windowing)
     - Orchestration Pipeline (multi-agent coordination)
     - State Persistence (checkpoint/resume)
     - Post-Verification Feedback (quality loops)
   - **Referenced in**:
     - `README.md:390`
     - `build-agent/SKILL.md:11`
     - `agile-v-pipeline/SKILL.md:12`
     - `red-team-verifier/SKILL.md:11`
     - `agile-v-core/SKILL.md:12`
   - **Attribution**: Full copyright notice maintained in all adapted skills

6. **forrestchang/andrej-karpathy-skills** (Karpathy Skills)
   - **URL**: https://github.com/forrestchang/andrej-karpathy-skills
   - **License**: MIT License
   - **Version**: v1.3 behavioral principles
   - **Contribution**: Behavioral guidelines for AI agents, accessibility practices, and distribution best practices
   - **Integrated Principles**:
     - Four core behavioral principles for agent interaction
     - Accessibility and discoverability patterns
     - Distribution and packaging best practices
   - **Referenced in**:
     - `agile-v-behavioral/SKILL.md:11,236`
     - `package.json:30`
     - `CHANGELOG.md:38`
   - **Integration**: Combined with Agile-V traceability framework for enhanced behavioral guidelines

7. **Kadajett/agent-nestjs-skills**
   - **URL**: https://github.com/Kadajett/agent-nestjs-skills
   - **Author**: Kadajett
   - **License**: MIT License
   - **Copyright**: © 2024 Kadajett
   - **Version**: 1.1.0
   - **Contribution**: NestJS-specific development patterns and best practices
   - **Referenced in**:
     - `domains/build-agent-nestjs/NOTICE.md:5`
   - **Integration**: Adapted for SCOPE-V framework and Agile-V traceability requirements
   - **Attribution**: Full NOTICE.md file maintains original copyright

---

## 📖 External Documentation & Resources

### Specifications & Standards

1. **AgentSkills.io Specification**
   - **URL**: https://agentskills.io/specification
   - **Purpose**: Agent skill format specification and standard
   - **Contribution**: Primary specification for skill format, metadata, and structure
   - **Referenced in**:
     - `README.md:6,505,1023,1032`
     - All skill SKILL.md files follow this specification
   - **Compliance**: All skills in this repository follow AgentSkills.io v1.0 specification

2. **Agile-V.org**
   - **URL**: https://agile-v.org
   - **Purpose**: Official Agile V framework homepage and documentation
   - **Referenced in**: `package.json:33` and throughout documentation
   - **Contribution**: Foundation framework for all skills

3. **JSON Schema**
   - **URLs**:
     - http://json-schema.org/draft-07/schema
     - https://json-schema.org/draft/2020-12/schema
   - **Purpose**: Schema definitions for skill validation and runtime schemas
   - **Referenced in**: All schema files (`schemas/` directory)

4. **Semantic Versioning (SemVer)**
   - **URL**: https://semver.org/
   - **Purpose**: Versioning strategy for skills library
   - **Referenced in**: `README.md:1022`, release process
   - **Usage**: All releases follow semantic versioning (MAJOR.MINOR.PATCH)

5. **Conventional Commits**
   - **URL**: https://www.conventionalcommits.org/
   - **Purpose**: Commit message format for automated versioning and changelog
   - **Referenced in**: `README.md:1022`, CI/CD workflow
   - **Usage**: All commits follow conventional commit format for automated releases

6. **Creative Commons BY-SA 4.0 License**
   - **URL**: https://creativecommons.org/licenses/by-sa/4.0/
   - **Legal Text**: https://creativecommons.org/licenses/by-sa/4.0/legalcode.en
   - **Purpose**: License for Agile V Skills Library
   - **Referenced in**: LICENSE file, all skill metadata
   - **Requirements**:
     - Attribution required
     - ShareAlike - derivative works must use same license
     - Commercial use permitted

### Platform-Specific Documentation

7. **Cursor Skills Documentation**
   - **URL**: https://cursor.com/docs/context/skills
   - **Purpose**: Cursor IDE skill integration and usage
   - **Referenced in**: `README.md:486`
   - **Integration**: Skills are compatible with Cursor's skill format

8. **Claude Code Skills Documentation**
   - **URL**: https://code.claude.com/docs/en/skills
   - **Purpose**: Claude Code skill development and usage
   - **Referenced in**: `README.md:490`
   - **Integration**: Skills are compatible with Claude Code's format

9. **VS Code Copilot Skills Documentation**
   - **URL**: https://code.visualstudio.com/docs/copilot/customization/agent-skills
   - **Purpose**: VS Code agent skill customization
   - **Referenced in**: `README.md:495`
   - **Integration**: Skills follow VS Code Copilot skill guidelines

10. **GitHub Copilot Skills Documentation**
    - **URL**: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
    - **Purpose**: GitHub Copilot skill development
    - **Referenced in**: `README.md:500`
    - **Integration**: Skills are compatible with GitHub Copilot agents

---

## 📋 Compliance Standards & Regulations

### ISO Standards

1. **ISO 9001:2015** - Quality Management Systems
   - **Status**: Aligned (Design Phase)
   - **Coverage**: Quality management principles integrated into skills
   - **Referenced in**: Compliance documentation, quality gates skill
   - **Documentation**: `docs/compliance/02_ISO_9001_MATRIX.md`

2. **ISO 13485:2016** - Medical Device Quality Management
   - **Status**: Partial (Design Controls)
   - **Coverage**: Design control principles in development skills
   - **Referenced in**: Medical device development skills
   - **Documentation**: `docs/compliance/03_ISO_13485_MATRIX.md`

3. **ISO 27001:2022** - Information Security Management
   - **Status**: Aligned (Development Controls)
   - **Coverage**: Security controls in development lifecycle
   - **Referenced in**: Security-focused skills and templates
   - **Documentation**: `docs/compliance/05_ISO_27001_MATRIX.md`

4. **ISO 26262** - Automotive Functional Safety
   - **Referenced in**: `domains/build-agent-embedded/SKILL.md` (19 matches)
   - **Context**: Safety-critical automotive software development
   - **Coverage**: ASIL levels and automotive safety requirements

### Aerospace & Industry Standards

5. **AS9100D** - Aerospace Quality Management
   - **Status**: Aligned
   - **Referenced in**: Aerospace domain skills and compliance matrices
   - **Documentation**: `docs/compliance/04_AS9100D_MATRIX.md`

6. **IEC 61508** - Functional Safety
   - **Referenced in**: `domains/build-agent-embedded/SKILL.md`
   - **Context**: Safety integrity levels (SIL) for safety-critical systems
   - **Coverage**: SIL 1-4 development requirements

7. **DO-178C** - Software Considerations in Airborne Systems
   - **Referenced in**: `domains/build-agent-embedded/SKILL.md`
   - **Context**: Avionics software certification
   - **Coverage**: DO-178C Design Assurance Levels (DAL A-E)

### Pharmaceutical & Regulatory

8. **GxP / GAMP 5** - Good Automated Manufacturing Practice
   - **Status**: Aware
   - **Coverage**: GAMP 5 categories and validation requirements
   - **Referenced in**: Pharmaceutical development skills
   - **Documentation**: `docs/compliance/06_GXP_GAMP5_MATRIX.md`

9. **21 CFR Part 11** - FDA Electronic Records and Electronic Signatures
   - **Status**: Partial
   - **Gap**: Electronic signature infrastructure
   - **Referenced in**: Compliance gap roadmap
   - **Coverage**: Audit trail and record retention requirements

10. **EU Annex 11** - Computerized Systems
    - **Referenced in**: Pharmaceutical compliance documentation
    - **Context**: Electronic signature requirements for EU pharmaceutical systems

### Software Development Standards

11. **MISRA-C:2012** - Motor Industry Software Reliability Association C Coding Standard
    - **Referenced in**: `domains/build-agent-embedded/SKILL.md` (19 matches)
    - **Context**: Safety-critical C programming guidelines
    - **Coverage**: MISRA-C rules for embedded systems development

12. **AUTOSAR** - Automotive Open System Architecture
    - **Referenced in**: Embedded systems domain skills
    - **Context**: Automotive software architecture standards
    - **Coverage**: AUTOSAR Classic and Adaptive Platform

13. **V-Model** - Software Development Lifecycle
    - **Referenced extensively**: Throughout development skills and templates
    - **Context**: Development lifecycle methodology
    - **Coverage**: Requirements → Design → Implementation → Testing → Verification

---

## 📦 Dependencies

### JavaScript/Node Dependencies (package.json)

**Runtime Requirements:**
- Node.js >= 14.0.0

**No runtime dependencies** - Skills are pure markdown/YAML definitions

**Skills are dependency-free** and can be used with any AI agent framework that supports AgentSkills.io specification.

---

## 🏆 Attribution & Licensing

### Copyright Holders

1. **Agile V™**
   - **Email**: info@agile-v.org, hello@agile-v.org
   - **Copyright**: Agile-V framework, skills, and templates
   - **License**: CC-BY-SA-4.0
   - **Repository**: Agile V Skills Library

2. **Lex Christopherson**
   - **Copyright**: © 2025 Lex Christopherson
   - **License**: MIT License
   - **Contribution**: GSD patterns (Get Shit Done)
   - **Original Work**: https://github.com/gsd-build/get-shit-done
   - **Adapted In**:
     - `build-agent/SKILL.md`
     - `agile-v-pipeline/SKILL.md`
     - `red-team-verifier/SKILL.md`
     - `agile-v-core/SKILL.md`
   - **Attribution**: Full copyright notice maintained with note: "Adapted for Agile V framework"

3. **Kadajett**
   - **Copyright**: © 2024 Kadajett
   - **License**: MIT License
   - **Contribution**: NestJS agent skills
   - **Original Work**: https://github.com/Kadajett/agent-nestjs-skills
   - **Adapted In**: `domains/build-agent-nestjs/`
   - **Attribution**: Full NOTICE.md file in skill directory

4. **Karpathy Skills Contributors**
   - **License**: MIT License
   - **Contribution**: Behavioral guidelines and distribution patterns
   - **Original Work**: https://github.com/forrestchang/andrej-karpathy-skills
   - **Adapted In**: `agile-v-behavioral/SKILL.md`
   - **Attribution**: Referenced in skill metadata and documentation

### License Information

**This Repository (agile_v_skills)**:
- **Primary License**: CC-BY-SA-4.0
- **License URL**: https://creativecommons.org/licenses/by-sa/4.0/
- **Legal Text**: https://creativecommons.org/licenses/by-sa/4.0/legalcode.en
- **Permissions**:
  - ✅ Commercial use
  - ✅ Modification
  - ✅ Distribution
  - ✅ Private use
- **Conditions**:
  - 📋 License and copyright notice
  - 📋 State changes
  - 📋 Disclose source
  - 📋 Same license (ShareAlike)

**Upstream Sources**:
- **GSD (Get Shit Done)**: MIT License
- **Karpathy Skills**: MIT License
- **Kadajett NestJS Skills**: MIT License
- **Understand Anything**: MIT License

**License Compatibility**:
- MIT-licensed patterns integrated into CC-BY-SA-4.0 work (compatible - attribution maintained)
- All derivative works must be released under CC-BY-SA-4.0 or compatible license

---

## 📊 Contribution Summary

- **Academic Papers**: 1 (pcbGPT - EDA inspiration)
- **GitHub Repositories**: 7 repositories
  - 3 Agile-V repositories
  - 3 upstream pattern sources (GSD, Karpathy, Kadajett)
  - 1 framework integration (Understand Anything)
- **External Documentation Sites**: 10+ (AgentSkills.io, platform docs, specifications)
- **Compliance Standards**: 13+ standards (ISO, aerospace, pharmaceutical, automotive)
- **Platform Integrations**: 4 platforms (Cursor, Claude Code, VS Code, GitHub Copilot)
- **Total Skill Count**: 40+ skills across 7 domains
- **Primary License**: CC-BY-SA-4.0 with MIT-licensed upstream attributions

---

## 🎯 Key Integration Points

1. **GSD (Get Shit Done)** - Context engineering and orchestration patterns
   - **Pattern Count**: 4 major patterns adapted
   - **Skills Affected**: build-agent, agile-v-pipeline, red-team-verifier, agile-v-core
   - **License**: MIT → CC-BY-SA-4.0 (compatible, attribution maintained)

2. **Karpathy Skills** - Behavioral guidelines
   - **Principles**: 4 behavioral principles
   - **Skills Affected**: agile-v-behavioral
   - **License**: MIT → CC-BY-SA-4.0 (compatible, attribution maintained)

3. **Kadajett NestJS Skills** - Domain-specific development patterns
   - **Skills Affected**: build-agent-nestjs
   - **License**: MIT → CC-BY-SA-4.0 (compatible, full NOTICE.md maintained)

4. **Understand Anything** - Knowledge graph integration
   - **Integration**: Phase 1 complete (docs, skills, templates)
   - **Skills**: System context, impact analysis, traceability
   - **License**: MIT

5. **AgentSkills.io Specification** - Skill format standard
   - **Compliance**: All 40+ skills follow v1.0 specification
   - **Validation**: JSON Schema validation for all skills

---

## 📝 Skill Development History

### Version 3.x Series (Current)

- **v3.3.2** (Latest) - P0 fixes: sync workflow, evidence language, validation
- **v3.3.1** - Documentation improvements
- **v3.3.0** - Karpathy Skills integration and discoverability enhancements
- **v3.2.0** - Understand Anything integration (Phase 1)
- **v3.1.0** - Karpathy Skills behavioral principles
- **v3.0.0** - Quality gates skill for enhanced QA

### Version 2.x Series

- **v2.0.1** - Documentation updates with final v1.6 metrics
- **v2.0.0** - Context efficiency optimization (~19% max usage)
- **v1.6.0** - NestJS skill comprehensive enrichment
- **v1.5.0** - Product development extensions (EDA domain with 26 PCB skills)

### Version 1.x Series

- **v1.4.0** - SCOPE-V framework and runtime schemas
- **v1.3.0** - Compliance hardening (ISO/GxP audit)
- **v1.2.0** - Context engineering integration from GSD
- **v1.1.0** - Composable skills architecture
- **v1.0.0** - Initial release

---

## 🔄 Upstream Sync & Maintenance

### Active Integrations

1. **agile_v_cursor_plugin** - Automated sync via GitHub Actions
   - **Workflow**: `.github/workflows/sync-to-plugin-repo.yml`
   - **Trigger**: On push to main branch
   - **Direction**: agile_v_skills → agile_v_cursor_plugin

2. **Understand Anything** - Manual integration with version tracking
   - **Status**: Phase 1 complete, Phase 2 planned
   - **Update Frequency**: Per integration plan milestones

3. **Upstream Pattern Sources** - Manual review and adaptation
   - **GSD**: Monitor for new patterns, evaluate for integration
   - **Karpathy Skills**: Track updates to behavioral guidelines
   - **Kadajett NestJS**: Monitor for NestJS best practice updates

---

## 📧 Contact & Attribution Questions

For questions about:
- **Licensing**: info@agile-v.org
- **Contributions**: hello@agile-v.org
- **Attribution Requirements**: Refer to LICENSE file and individual skill NOTICE.md files
- **Integration Support**: https://agile-v.org

---

## ✅ Attribution Checklist for Derivative Works

If you create derivative works based on this skills library, you must:

- [ ] Include a copy of the CC-BY-SA-4.0 license
- [ ] Provide attribution to "Agile V™" with link to https://agile-v.org
- [ ] State changes made to the original work
- [ ] Disclose source code (if distributed)
- [ ] Use CC-BY-SA-4.0 or compatible license for derivative work
- [ ] Maintain MIT license attributions for GSD, Karpathy, and Kadajett contributions
- [ ] Include original copyright notices from adapted skills (see NOTICE.md files)

---

**Last Updated**: June 2026  
**Repository Version**: v3.3.2 (commit `87f965a`)  
**License**: CC-BY-SA-4.0  
**Upstream Attributions**: 3 MIT-licensed sources (GSD, Karpathy Skills, Kadajett NestJS)

For the most current information, visit: https://github.com/Agile-V/agile_v_skills
