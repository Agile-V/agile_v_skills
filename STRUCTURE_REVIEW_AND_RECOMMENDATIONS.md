# Agile V Skills: Structure Review & Modernization Recommendations

**Review Date:** 2026-05-22  
**Current Version:** v1.5.0  
**Reviewer:** Structure analysis for NestJS integration planning

---

## Executive Summary

The Agile V skills repository has evolved significantly through v1.5, achieving impressive context optimization (60% reduction in v1.3) and comprehensive compliance coverage. This review identifies opportunities to further modernize the structure, improve consistency, and prepare for technology-specific skill expansions like NestJS.

**Key Findings:**
- ✅ **Strong Foundation:** Core skills (agile-v-core, agile-v-lifecycle, agile-v-compliance) are well-structured
- ✅ **Domain Pattern Works:** `domains/build-agent-*` structure is extensible and consistent
- ⚠️ **Mixed Patterns:** Some skills use different organizational approaches
- ⚠️ **Routing Complexity:** Manual skill selection requires SKILL_ROUTING_GUIDE.md
- 💡 **Opportunity:** Auto-activation metadata could improve agent UX

---

## 1. Current Structure Analysis

### 1.1 Directory Organization

```text
agile_v_skills/
├── Core Lifecycle Skills (root level)
│   ├── agile-v-core/
│   ├── agile-v-lifecycle/
│   ├── agile-v-compliance/
│   └── agile-v-pipeline/
│
├── Left Side Skills (root level)
│   ├── requirement-architect/
│   ├── logic-gatekeeper/
│   ├── discovery-analyst/
│   ├── threat-modeler/
│   └── ux-spec-author/
│
├── Apex Skills (root level)
│   ├── build-agent/
│   ├── test-designer/
│   └── schematic-generator/
│
├── Domain-Specific Build Agents (domains/)
│   ├── domains/build-agent-dart/
│   ├── domains/build-agent-embedded/
│   ├── domains/build-agent-js/
│   └── domains/build-agent-python/
│
├── Right Side Skills (root level)
│   └── red-team-verifier/
│
├── Compliance & Documentation (root level)
│   ├── compliance-auditor/
│   └── documentation-agent/
│
└── Agile Delivery & Operations (root level)
    ├── agile-v-product-owner/
    ├── release-manager/
    └── observability-planner/
```

**Observations:**
- ✅ Clear V-model positioning (Left → Apex → Right)
- ✅ Domain skills isolated under `domains/`
- ⚠️ Most skills at root level → flat structure as skill count grows
- ⚠️ No clear grouping by phase (Discovery, Requirements, Synthesis, Verification, Release, Compliance)

---

### 1.2 Skill File Consistency

| Skill | SKILL.md | sections_index | metadata.version | metadata.extends | License |
|---|---|---|---|---|---|
| agile-v-core | ✅ | ✅ | ✅ (1.3) | N/A | ✅ CC-BY-SA-4.0 |
| build-agent | ✅ | ✅ | ✅ (1.3) | N/A | ✅ CC-BY-SA-4.0 |
| build-agent-js | ✅ | ❌ | ✅ (1.3) | ✅ (build-agent) | ✅ CC-BY-SA-4.0 |
| build-agent-python | ✅ | ❌ | ✅ (1.3) | ✅ (build-agent) | ✅ CC-BY-SA-4.0 |
| build-agent-dart | ✅ | ❌ | ✅ (1.3) | ✅ (build-agent) | ✅ CC-BY-SA-4.0 |
| build-agent-embedded | ✅ | ❌ | ✅ (1.3) | ✅ (build-agent) | ✅ CC-BY-SA-4.0 |
| requirement-architect | ✅ | ❌ | ✅ (1.3) | N/A | ✅ CC-BY-SA-4.0 |
| red-team-verifier | ✅ | ❌ | ✅ (1.3) | N/A | ✅ CC-BY-SA-4.0 |

**Observations:**
- ✅ All skills have YAML frontmatter (agentskills.io compliant)
- ✅ Licensing consistent (CC-BY-SA-4.0)
- ⚠️ Only `agile-v-core` and `build-agent` use `sections_index` (v1.3 optimization)
- ⚠️ Domain skills missing `sections_index` (small enough not to need?)
- ✅ `metadata.extends` used correctly in domain skills

---

### 1.3 Context Optimization Status

**v1.3 Achievements:**
- agile-v-core: 610 → 227 lines (63% reduction)
- build-agent: 151 → 74 lines (51% reduction)
- red-team-verifier: 212 → 89 lines (58% reduction)

**Current Sizes (as of v1.5):**
- agile-v-core: 83 lines
- build-agent: 74 lines
- build-agent-js: 58 lines
- build-agent-python: ~60 lines (estimated)
- requirement-architect: 50 lines
- test-designer: 53 lines

**Observations:**
- ✅ All core skills highly optimized (<100 lines)
- ✅ Domain skills concise (50-60 lines)
- 💡 Opportunity: Standardize structure across domain skills for predictability

---

## 2. NestJS Integration: Modern Pattern

### 2.1 Why Modern Pattern Differs from Original Plan

**Original Plan Issues:**
1. **Over-Engineering:** 13 files for one skill (SKILL.md, agile-v.skill.yaml, scope-v-mapping.md, constraints.md, evidence.md, review-checklist.md, task-brief-template.md, traceability-template.md, tests/, upstream/, NOTICE.md, LICENSE)
2. **Duplication:** Evidence, traceability, review checklists already exist in `agile-v-compliance`, `build-agent`, `red-team-verifier`
3. **Inconsistency:** No other domain skill uses this pattern
4. **Context Bloat:** Loading 8+ files vs. 1 optimized SKILL.md
5. **Maintenance Burden:** Updating 8 files when upstream changes vs. 1 file

**Modern Pattern Advantages:**
1. **Consistency:** Matches `build-agent-js`, `build-agent-python`, etc.
2. **Low Context:** Single SKILL.md (~250-300 lines) with `sections_index`
3. **Inheritance:** Reuses `build-agent`, `agile-v-compliance`, `agile-v-lifecycle`
4. **Maintainability:** Update 1 file when upstream changes
5. **Extensibility:** Easy to add more domain skills (Go, Rust, Elixir, etc.)

---

### 2.2 Recommended Structure

```text
domains/build-agent-nestjs/
├── SKILL.md                 # 250-300 lines, YAML frontmatter, sections_index
├── LICENSE                  # MIT (for upstream Kadajett content)
├── NOTICE.md                # Attribution
└── upstream/                # Mirror of agent-nestjs-skills
    ├── README.md
    ├── SKILL.md
    ├── AGENTS.md
    ├── metadata.json
    └── rules/
        ├── architecture.md
        ├── dependency-injection.md
        ├── api-design.md
        ├── security.md
        ├── database.md
        ├── testing.md
        └── devops.md
```

**Key Design Decisions:**
- ✅ `SKILL.md` is single source of truth (agent loads this only)
- ✅ `upstream/` preserved for attribution and future sync
- ✅ `sections_index` in frontmatter for fast navigation
- ✅ `metadata.extends: "build-agent"` declares inheritance
- ✅ `metadata.upstream` documents source and license
- ❌ No separate YAML file (frontmatter suffices)
- ❌ No separate constraints/evidence files (inherited from core)
- ❌ No separate templates (examples inline or in examples/ if needed)

---

## 3. Structure Improvement Recommendations

### 3.1 Short-Term (v1.6 / Quick Wins)

#### 3.1.1 Add `sections_index` to Domain Skills
**Why:** Improves agent navigation, reduces context scanning overhead  
**Effort:** Low (5 min per skill)  
**Impact:** Medium (consistency + minor performance gain)

**Example for build-agent-js:**
```yaml
---
name: build-agent-js
description: ...
license: CC-BY-SA-4.0
metadata:
  version: "1.3"
  standard: "Agile V"
  domain: "JavaScript/TypeScript/Web"
  extends: "build-agent"
  author: agile-v.org
  sections_index:
    - Inherited Rules
    - JavaScript/TypeScript Conventions
    - Type Safety
    - Web Platform Constraints
    - Framework Conventions
    - Build Tooling
    - Testing Alignment
    - Context Engineering (JS/TS-Specific)
    - When to Use
---
```

**Apply to:** build-agent-js, build-agent-python, build-agent-dart, build-agent-embedded

---

#### 3.1.2 Integrate NestJS Skill (Modern Pattern)
**Why:** Validates domain pattern, fills gap for NestJS projects  
**Effort:** Medium (2-4 hours)  
**Impact:** High (enables NestJS support, tests extensibility)

**Tasks:**
1. Create `domains/build-agent-nestjs/`
2. Write SKILL.md (use template in NESTJS_INTEGRATION_PLAN_MODERN.md)
3. Clone upstream Kadajett content to `upstream/`
4. Write NOTICE.md and LICENSE
5. Update SKILL_ROUTING_GUIDE.md
6. Update README.md skill table
7. Test with sample NestJS project

**Deliverable:** `build-agent-nestjs` skill following modern pattern

---

#### 3.1.3 Document Domain Skill Template
**Why:** Enables community contributions, ensures consistency  
**Effort:** Low (1 hour)  
**Impact:** High (scalability for new tech stacks)

**Create:** `docs/DOMAIN_SKILL_TEMPLATE.md`

**Contents:**
```markdown
# Domain Skill Template

Use this template when creating a new domain-specific build agent (e.g., build-agent-go, build-agent-rust).

## File Structure
domains/build-agent-{LANGUAGE}/
├── SKILL.md
├── LICENSE (if upstream content)
├── NOTICE.md (if upstream content)
└── upstream/ (if upstream content)

## SKILL.md Template
---
name: build-agent-{LANGUAGE}
description: {LANGUAGE} build agent for... Extends build-agent with {LANGUAGE}-specific patterns.
license: CC-BY-SA-4.0
metadata:
  version: "1.0"
  standard: "Agile V"
  domain: "{LANGUAGE}/{PLATFORM}"
  extends: "build-agent"
  author: agile-v.org
  sections_index:
    - Inherited Rules
    - {LANGUAGE} Conventions
    - [Domain-Specific Sections]
    - Context Engineering ({LANGUAGE}-Specific)
    - When to Use
---

# Instructions
You are the **{LANGUAGE} Build Agent**...
[Inherit from build-agent, add language-specific rules]

## Inherited Rules
All rules from **build-agent** apply. This skill adds {LANGUAGE}-specific conventions only.

## {LANGUAGE} Conventions
[Language-specific architecture, idioms, tooling, testing]

## Context Engineering ({LANGUAGE}-Specific)
[Package managers, generated files, monorepo handling, etc.]

## When to Use
- {LANGUAGE} projects
- {Frameworks}
- {Typical use cases}
```

---

### 3.2 Medium-Term (v1.7-v1.8 / Structure Refinement)

#### 3.2.1 Introduce Phase-Based Grouping (Optional)
**Why:** Clearer organization as skill count grows  
**Effort:** Medium (restructure + update docs)  
**Impact:** Medium (developer experience, discoverability)

**Proposed Structure:**
```text
agile_v_skills/
├── core/
│   ├── agile-v-core/
│   ├── agile-v-lifecycle/
│   ├── agile-v-compliance/
│   └── agile-v-pipeline/
├── discovery/
│   ├── discovery-analyst/
│   ├── threat-modeler/
│   └── ux-spec-author/
├── requirements/
│   ├── requirement-architect/
│   └── logic-gatekeeper/
├── synthesis/
│   ├── build-agent/
│   ├── test-designer/
│   ├── schematic-generator/
│   └── domains/
│       ├── build-agent-js/
│       ├── build-agent-python/
│       ├── build-agent-dart/
│       ├── build-agent-embedded/
│       └── build-agent-nestjs/
├── verification/
│   └── red-team-verifier/
├── compliance/
│   ├── compliance-auditor/
│   └── documentation-agent/
└── delivery/
    ├── agile-v-product-owner/
    ├── release-manager/
    └── observability-planner/
```

**Trade-offs:**
- ✅ Clearer organization
- ✅ Easier to find skills by phase
- ⚠️ Breaking change for existing users (update `.cursor/skills/` paths)
- ⚠️ Requires documentation updates

**Recommendation:** Defer to v2.0 (major version bump allows breaking changes)

---

#### 3.2.2 Add Auto-Activation Metadata
**Why:** Reduce manual skill selection, improve agent UX  
**Effort:** Medium (define spec + update skills)  
**Impact:** High (less friction for users)

**Proposal:** Add `applies_when` to frontmatter (inspired by original NestJS plan):

```yaml
---
name: build-agent-nestjs
description: ...
metadata:
  version: "1.0"
  extends: "build-agent"
  applies_when:
    package_json_dependencies:
      - "@nestjs/core"
      - "@nestjs/common"
    file_patterns:
      - "**/*.module.ts"
      - "**/*.controller.ts"
      - "**/*.service.ts"
    task_keywords:
      - "NestJS"
      - "controller"
      - "service"
      - "module"
---
```

**Implementation:**
1. Define `applies_when` schema in `docs/SKILL_SPEC.md`
2. Add to all domain skills
3. Create skill loader utility (optional, for tools that support it)
4. Document in README.md

**Benefit:** Agents can auto-load `build-agent-nestjs` when user says "implement auth controller" in a NestJS project

---

#### 3.2.3 Standardize Domain Skill Sections
**Why:** Predictable structure → easier for agents to parse  
**Effort:** Low (template + update existing)  
**Impact:** Medium (consistency)

**Standard Sections for Domain Skills:**
1. **Inherited Rules** (boilerplate: "All rules from build-agent apply")
2. **{LANGUAGE} Conventions** (architecture, idioms, frameworks)
3. **Context Engineering ({LANGUAGE}-Specific)** (package managers, generated files, monorepo)
4. **Output Format** (manifest examples)
5. **When to Use** (project types, frameworks, auto-trigger hints)
6. **Upstream Integration** (if applicable)

**Action:** Update DOMAIN_SKILL_TEMPLATE.md + retrofit existing skills

---

### 3.3 Long-Term (v2.0 / Major Refactor)

#### 3.3.1 Skill Registry & Discovery System
**Why:** Scale to 50+ skills without manual SKILL_ROUTING_GUIDE.md  
**Effort:** High (new tooling)  
**Impact:** High (scalability)

**Proposal:**
- Create `skills-registry.json` with all skill metadata
- Auto-generate SKILL_ROUTING_GUIDE.md from registry
- Provide CLI tool for skill search/discovery
- Support multi-skill workflows (agent chains)

**Example registry.json:**
```json
{
  "skills": [
    {
      "id": "build-agent-nestjs",
      "name": "NestJS Build Agent",
      "path": "domains/build-agent-nestjs",
      "phase": "synthesis",
      "extends": "build-agent",
      "applies_when": {
        "package_json_dependencies": ["@nestjs/core"],
        "file_patterns": ["**/*.module.ts"],
        "task_keywords": ["NestJS", "controller"]
      }
    }
  ]
}
```

**Tooling:**
```bash
# CLI for skill discovery
agile-v skills search "authentication"
# → Returns: build-agent, threat-modeler, test-designer

agile-v skills recommend --project ./my-nestjs-app
# → Returns: build-agent-nestjs, test-designer, red-team-verifier
```

---

#### 3.3.2 Multi-Language Support for Skills
**Why:** Global adoption  
**Effort:** High (translation + maintenance)  
**Impact:** High (accessibility)

**Proposal:**
```text
domains/build-agent-nestjs/
├── SKILL.md (English, default)
├── SKILL.es.md (Spanish)
├── SKILL.de.md (German)
└── ...
```

**Defer to:** Post v2.0 (requires translation process + governance)

---

#### 3.3.3 Skill Versioning & Compatibility Matrix
**Why:** Manage breaking changes across skill dependencies  
**Effort:** High (tooling + governance)  
**Impact:** Medium (stability for large teams)

**Proposal:**
- Each skill declares `requires: { "agile-v-core": ">=1.3", "build-agent": ">=1.3" }`
- Version compatibility checker
- Deprecation warnings

**Example:**
```yaml
metadata:
  version: "2.0"
  requires:
    agile-v-core: ">=1.5"
    build-agent: ">=1.5"
  deprecated: false
  breaking_changes: ["Removed support for pre-1.3 BUILD_MANIFEST format"]
```

---

## 4. Specific Recommendations Summary

### Priority 1 (v1.6 - Do Now)
1. ✅ **Integrate NestJS skill using modern pattern** (validates extensibility)
2. ✅ **Add sections_index to all domain skills** (consistency)
3. ✅ **Create DOMAIN_SKILL_TEMPLATE.md** (enables community contributions)
4. ✅ **Document upstream sync process** (for skills with external sources)

### Priority 2 (v1.7-v1.8 - Do Soon)
1. 🔶 **Add applies_when metadata to domain skills** (auto-activation)
2. 🔶 **Standardize domain skill sections** (predictability)
3. 🔶 **Create skill contribution guidelines** (README mentions in progress)
4. 🔶 **Add CI validation for skill metadata** (prevents regressions)

### Priority 3 (v2.0 - Do Later)
1. 🔷 **Introduce phase-based directory structure** (breaking change)
2. 🔷 **Build skill registry & discovery system** (scaling)
3. 🔷 **Implement skill versioning & compatibility checks** (stability)
4. 🔷 **Multi-language skill support** (global adoption)

---

## 5. Risk Analysis

### 5.1 Risks of Modern NestJS Pattern

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Context bloat** (if SKILL.md grows too large) | Low | Medium | Enforce 300-line limit; split to upstream/ if needed |
| **Upstream sync conflicts** | Medium | Low | Document clear sync process; use git submodules if needed |
| **Pattern divergence** (future skills don't follow) | Medium | High | Create DOMAIN_SKILL_TEMPLATE.md; enforce in PR reviews |
| **Loss of detail** (vs. 8-file approach) | Low | Low | Upstream/ preserves full detail; SKILL.md is curated summary |

### 5.2 Risks of Structure Changes (v2.0)

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Breaking changes for users** | High | High | Wait for v2.0; provide migration guide; auto-migration script |
| **Fragmentation** (some adopt, some don't) | Medium | Medium | Clear versioning; deprecation warnings; support both for 6 months |

---

## 6. Measurement & Success Criteria

### 6.1 For NestJS Integration

**Success = All True:**
- [ ] NestJS skill loads in Cursor/Claude Code/VS Code
- [ ] Context usage <50% for typical NestJS feature (auth module)
- [ ] Generated code includes traceability headers
- [ ] Build Manifest includes NestJS artifacts (modules, controllers, services, DTOs, tests, migrations)
- [ ] Halt conditions trigger correctly (circular deps, missing migrations)
- [ ] Upstream attribution preserved (NOTICE.md)
- [ ] SKILL_ROUTING_GUIDE.md updated

### 6.2 For Overall Structure (v1.6)

**Success = All True:**
- [ ] All domain skills have `sections_index`
- [ ] DOMAIN_SKILL_TEMPLATE.md exists and is referenced in README
- [ ] Contribution guidelines updated
- [ ] No context regression (total context for typical workflow <50KB)
- [ ] Community can add new domain skill in <2 hours using template

---

## 7. Action Plan

### Phase 1: NestJS Integration (Week 1)
- [ ] Day 1: Create `domains/build-agent-nestjs/` structure
- [ ] Day 2: Write SKILL.md (use NESTJS_INTEGRATION_PLAN_MODERN.md template)
- [ ] Day 3: Clone upstream, write NOTICE.md, LICENSE
- [ ] Day 4: Test with sample NestJS project (auth module from REQ)
- [ ] Day 5: Update SKILL_ROUTING_GUIDE.md, README.md, CHANGELOG.md

### Phase 2: Standardization (Week 2)
- [ ] Day 1: Add `sections_index` to build-agent-js, build-agent-python, build-agent-dart, build-agent-embedded
- [ ] Day 2: Create DOMAIN_SKILL_TEMPLATE.md
- [ ] Day 3: Document upstream sync process (CONTRIBUTING.md or docs/)
- [ ] Day 4: Review all domain skills for consistency
- [ ] Day 5: Update contribution guidelines

### Phase 3: Validation (Week 3)
- [ ] Test NestJS workflow end-to-end
- [ ] Verify context usage metrics
- [ ] Community review (GitHub issue for feedback)
- [ ] Address feedback
- [ ] Release v1.6

---

## 8. Conclusion

The Agile V skills repository is well-positioned for growth. The modern NestJS integration pattern:
- ✅ Maintains v1.3 context optimization gains
- ✅ Follows existing domain skill patterns
- ✅ Enables rapid addition of new tech stacks (Go, Rust, Ruby, etc.)
- ✅ Preserves upstream attribution and sync capability
- ✅ Avoids over-engineering and duplication

**Recommended Next Steps:**
1. Implement NestJS skill using modern pattern (validates approach)
2. Add `sections_index` to existing domain skills (quick win)
3. Create DOMAIN_SKILL_TEMPLATE.md (enables community)
4. Plan v2.0 structural improvements (phase-based grouping, skill registry)

**Long-Term Vision:**
- 50+ domain skills covering all major tech stacks
- Auto-activation based on project context
- Skill registry for discovery and composition
- Multi-language support for global adoption

---

**End of Structure Review & Recommendations**
