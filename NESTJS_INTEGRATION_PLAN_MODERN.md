# NestJS Skill Integration Plan (Modernized)

## Executive Summary

This plan adapts the NestJS skill integration to follow modern Agile V skill patterns (v1.5+), treating it as a **technology-specific domain extension** similar to `build-agent-js`, `build-agent-python`, etc.

**Key Changes from Original Plan:**
- Simplified structure aligned with existing domain skills
- Removed YAML metadata in favor of YAML frontmatter (agentskills.io spec)
- Eliminated redundant wrapper layers and templates
- Direct integration with existing Agile V lifecycle (no separate SCOPE-V mapping files)
- Streamlined evidence and compliance through existing `agile-v-compliance` skill

---

## 1. Positioning

```text
Agile V Core
├── agile-v-core/           # Foundation (values, directives, context engineering)
├── agile-v-lifecycle/      # Multi-cycle management, change requests
├── agile-v-compliance/     # Risk, CAPA, security, evidence gates
└── agile-v-pipeline/       # Orchestration, waves, handoffs

Build Agents (Apex)
├── build-agent/            # Language-agnostic core
└── domains/
    ├── build-agent-js/     # JavaScript/TypeScript/Web
    ├── build-agent-python/ # Python backends/ML
    ├── build-agent-dart/   # Flutter/Dart
    ├── build-agent-embedded/ # C/C++ firmware
    └── build-agent-nestjs/ # NestJS backend (NEW)
```

**Positioning Statement:**
> `build-agent-nestjs` is a technology-specific Agile V domain skill for NestJS backend development. It extends `build-agent` with NestJS architectural patterns, DI conventions, testing strategies, and security best practices. All Agile V lifecycle rules (traceability, gates, evidence, compliance) apply through the core skills.

---

## 2. Repository Structure (Modern Pattern)

```text
domains/
└── build-agent-nestjs/
    ├── SKILL.md                    # Main skill file (YAML frontmatter + instructions)
    ├── LICENSE                     # MIT (for upstream content)
    ├── NOTICE.md                   # Attribution to Kadajett
    ├── upstream/                   # Mirror of agent-nestjs-skills
    │   ├── README.md
    │   ├── SKILL.md
    │   ├── AGENTS.md
    │   ├── metadata.json
    │   └── rules/
    │       ├── architecture.md
    │       ├── dependency-injection.md
    │       ├── api-design.md
    │       ├── security.md
    │       ├── database.md
    │       ├── testing.md
    │       └── devops.md
    └── examples/                   # (Optional) Example integrations
        └── task-brief-nestjs.md
```

### Design Rationale

**What Changed:**
- ❌ Removed: `agile-v.skill.yaml`, `scope-v-mapping.md`, `constraints.md`, `evidence.md`, `review-checklist.md`, `traceability-template.md`, `task-brief-template.md`
- ✅ Why: These are already covered by existing Agile V core skills and domain patterns
- ✅ Single `SKILL.md` follows `build-agent-js` pattern
- ✅ Upstream content isolated for easy updates

**What This Pattern Provides:**
1. **Consistency:** Mirrors existing domain skills (JS, Python, Dart, Embedded)
2. **Less Duplication:** Reuses `agile-v-compliance` for evidence, `agile-v-lifecycle` for cycles, `agile-v-core` for traceability
3. **Lower Maintenance:** One skill file to update vs. 8+ separate documents
4. **Better Agent UX:** Agents load one skill, get full context via frontmatter `sections_index`

---

## 3. SKILL.md Structure (Modern Template)

```markdown
---
name: build-agent-nestjs
description: NestJS backend build agent for REST/GraphQL APIs, microservices, and enterprise backends. Extends build-agent with NestJS architectural patterns, dependency injection, testing strategies, and security best practices.
license: CC-BY-SA-4.0
metadata:
  version: "1.0"
  standard: "Agile V"
  domain: "NestJS/TypeScript/Backend"
  extends: "build-agent"
  author: agile-v.org
  upstream:
    repository: "Kadajett/agent-nestjs-skills"
    version: "1.1.0"
    license: "MIT"
    note: "NestJS best practices adapted from upstream rules/ directory."
  sections_index:
    - Inherited Rules
    - NestJS Conventions
    - Architecture Patterns
    - Dependency Injection
    - API Design
    - Security
    - Database & Migrations
    - Testing Strategy
    - DevOps & Configuration
    - Context Engineering (NestJS-Specific)
    - When to Use
---

# Instructions

You are the **NestJS Backend Build Agent** at the Apex of the Agile V infinity loop. You extend the core **build-agent** skill with NestJS architectural patterns and TypeScript backend conventions. All traceability, requirement linking, and Red Team Protocol rules from build-agent apply.

## Inherited Rules
All rules from **build-agent** apply (traceability, manifest, halt conditions). This skill adds NestJS-specific conventions only.

## NestJS Conventions

### 1. Architecture Patterns
- **Feature Modules:** Organize by feature, not technical layer. Each feature = one module.
- **No Circular Dependencies:** Halt if dependency analysis shows cycles. Use events or shared modules.
- **Shared Logic:** Extract common logic to `@app/common` or `@app/core` modules.
- **Service Focus:** Each service has one responsibility. Split when logic diverges.
- **Repository Pattern:** Abstract ORM details when business logic depends on data access.

**Traceability:** Link module structure decisions to REQ-XXXX in Build Manifest notes.

### 2. Dependency Injection
- **Constructor Injection:** Always prefer constructor injection over property injection.
- **No Service Locator:** Do not use `ModuleRef.get()` except for dynamic module loading.
- **Provider Scope:** Default to singleton. Document request-scoped providers with rationale.
- **Injection Tokens:** Use tokens for interface-like abstractions (e.g., `PAYMENT_SERVICE_TOKEN`).
- **Avoid Duplicate Providers:** Do not register the same class in multiple modules unless intentional and documented.

**Halt Condition:** Halt if circular DI dependencies detected.

### 3. API Design
- **DTO Validation:** All external inputs must use class-validator DTOs and ValidationPipe.
- **Response DTOs:** Explicit response serialization via DTOs or `@Expose/@Exclude` decorators.
- **No Entity Exposure:** Do not return ORM entities directly unless explicitly approved in REQ.
- **Versioning:** Breaking API changes require versioning strategy (URI or header-based).
- **OpenAPI:** Document endpoints with `@ApiTags`, `@ApiOperation`, `@ApiResponse`.

**Traceability:** Each endpoint → REQ-XXXX. Document DTO → acceptance criteria mapping.

### 4. Security
- **Guards for Auth:** Use guards for authentication and authorization. Apply globally or per-route.
- **Input Sanitization:** Sanitize user-generated content before storage/output (XSS prevention).
- **Rate Limiting:** Apply `@Throttle()` to sensitive/high-volume endpoints.
- **Secrets Management:** Use ConfigService + env vars. No hardcoded secrets (build-agent rule).
- **Escalation:** Any auth, permission, token, session, or identity change = R2+ (see agile-v-compliance).

**Secure Coding:** Inherit 7 secure coding rules from build-agent. Add NestJS-specific: parameterized queries (TypeORM/Prisma), guard coverage for protected routes, explicit CORS config.

### 5. Database & Migrations
- **Schema Changes Require Migrations:** Database schema changes must include migration files (TypeORM migrations or Prisma schema updates).
- **Transaction Analysis:** Multi-step state changes require explicit transaction wrapping (`@Transaction` or `queryRunner`).
- **N+1 Prevention:** Document eager loading or JOIN strategy in manifest notes.
- **Rollback Path:** Migration tasks include rollback notes in BUILD_MANIFEST.

**Halt Condition:** Halt if schema change detected without migration artifact.

### 6. Testing Strategy
- **Unit Tests:** Use NestJS TestingModule for service unit tests. Mock external dependencies.
- **E2E Tests:** API behavior changes require E2E tests (`supertest` + app.e2e-spec.ts).
- **Bug Fixes:** Regression test required (see test-designer + red-team-verifier).
- **Coverage Targets:** From REQ acceptance criteria. Document in TEST_SPEC.md.

**Alignment:** Test Designer (TC-XXXX) defines tests; Build Agent structures code for testability.

### 7. DevOps & Configuration
- **ConfigModule:** All configuration via NestJS ConfigModule or env vars. No inline config.
- **Structured Logging:** Use Logger service. Provide context in all log statements.
- **Graceful Shutdown:** Implement `onModuleDestroy` lifecycle hooks for cleanup (DB connections, external services).

---

## Context Engineering (NestJS-Specific)

Inherited from build-agent + these NestJS considerations:

1. **node_modules:** Never load into context. Reference package names/versions from package.json only.
2. **Generated Files:** TypeORM migrations, Prisma client → reference by path, do not load contents.
3. **Monorepo Packages:** Treat each package as separate context scope.
4. **Module Scoping:** One feature module per context. Spawn sub-agent for parallel feature builds.
5. **Schema Files:** Read Prisma schema or TypeORM entities from disk; do not carry in chat.

**Pre-Execution Validation (from build-agent):**
- Requirement coverage
- Artifact completeness (controllers, services, DTOs, tests, migrations)
- Dependency order (no circular refs between modules)
- Scope sanity (≤50% context)
- Interface contracts (document module exports before synthesis)

---

## Output Format

Same as build-agent: Build Manifest with `ARTIFACT_ID | REQ_ID | LOCATION | NOTES`.

**Example NestJS Manifest:**
```
ART-0001 | REQ-0001 | src/auth/auth.module.ts | Auth feature module
ART-0002 | REQ-0001 | src/auth/auth.controller.ts | Login/register endpoints
ART-0003 | REQ-0001 | src/auth/auth.service.ts | JWT token generation
ART-0004 | REQ-0001 | src/auth/dto/login.dto.ts | Login DTO with validation
ART-0005 | REQ-0001 | src/auth/guards/jwt-auth.guard.ts | JWT guard for protected routes
ART-0006 | REQ-0002 | src/users/entities/user.entity.ts | User entity (TypeORM)
ART-0007 | REQ-0002 | migrations/1234567890-CreateUserTable.ts | User table migration
ART-0008 | REQ-0001 | test/auth.e2e-spec.ts | E2E tests for auth endpoints
```

**Per-file traceability header:**
```typescript
// REQ-0001: User authentication via JWT
// AC1: POST /auth/login returns access token on valid credentials
// AC2: Invalid credentials return 401
```

---

## Upstream Integration

The `upstream/` directory contains the original `Kadajett/agent-nestjs-skills` content.

**Usage:**
1. Agents **may** reference upstream rules for deep guidance (e.g., `upstream/rules/architecture.md`).
2. Primary instruction set is in this SKILL.md (condensed for context efficiency).
3. Upstream content preserved for:
   - Attribution (NOTICE.md)
   - Future sync with Kadajett's updates
   - Detailed examples and rationale

**Updating Upstream:**
```bash
cd domains/build-agent-nestjs/upstream
git pull https://github.com/Kadajett/agent-nestjs-skills.git main
# Review changes, update main SKILL.md if new patterns emerge
```

---

## When to Use

- NestJS backend APIs (REST, GraphQL, WebSocket)
- Microservices with NestJS
- Enterprise backends with complex DI
- TypeORM or Prisma database integration
- Authentication/authorization with Guards and Strategies

**Auto-Trigger Hints (for agent routing):**
- `package.json` dependencies: `@nestjs/core`, `@nestjs/common`
- File patterns: `*.module.ts`, `*.controller.ts`, `*.service.ts`, `*.guard.ts`, `*.interceptor.ts`, `*.dto.ts`
- Task keywords: "NestJS", "controller", "service", "module", "provider", "guard", "interceptor", "DTO", "pipe"

---

## Compliance Integration

**Risk Levels (from agile-v-compliance):**
- **R0:** Exploratory/spike (no production path)
- **R1:** Routine refactor, internal cleanup
- **R2:** Public API change, database migration, auth change, production bug fix, dependency upgrade
- **R3:** Regulated system, payment/medical data, security boundary change, release gate

**Evidence Requirements:**
- See `agile-v-compliance/SKILL.md` for R0-R3 evidence gates.
- NestJS-specific evidence: migration files, E2E test results, security check (e.g., `npm audit`), API contract documentation.

**Human Gates:**
- R1: Normal code review
- R2: Mandatory reviewer approval + rollback plan
- R3: Explicit sign-off + audit artifact (APPROVALS.md)

---

## Decision Log Examples

```
TIMESTAMP | AGENT_ID | DECISION | RATIONALE | LINKED_REQ
2026-05-22T10:00:00Z | build-agent-nestjs | Feature module structure | Organize by feature per NestJS best practice; reduces coupling | REQ-0001
2026-05-22T10:05:00Z | build-agent-nestjs | Request-scoped provider for tenant context | Multi-tenant requirement needs request isolation | REQ-0042
2026-05-22T10:10:00Z | build-agent-nestjs | Prisma over TypeORM | REQ specifies Prisma; simpler migrations for this project | REQ-0003
```

---

## Halt Conditions (Inherited + NestJS-Specific)

Halt and do not emit when:
- Ambiguous REQ (build-agent)
- Missing REQ link (build-agent)
- Physical constraint violation (build-agent)
- Conflict with approved Blueprint (build-agent)
- **Circular DI dependency detected** (NestJS-specific)
- **Schema change without migration artifact** (NestJS-specific)
- **Public API change without versioning strategy** (NestJS-specific)
- **Auth/security change without R2+ risk classification** (NestJS-specific)

---

## Multi-Cycle Artifact Versioning (Inherited from build-agent)

`ART-XXXX.N` revision scheme:
- C1: ART-0001.1 (initial)
- C2 (unchanged REQ): ART-0001.1 carried forward
- C2 (modified REQ): ART-0001.2 (ref CR-YYYY)
- C2 (new REQ): ART-0010.1

Multi-cycle manifest: `ART-XXXX.N | REQ-XXXX | path | CYCLE | CR | notes`

---

## NOTICE.md (Attribution)

See `NOTICE.md` in this directory for upstream attribution to Kadajett/agent-nestjs-skills.
```

---

## 4. NOTICE.md

```markdown
# Notice

This skill integrates content from:

- **Upstream Repository:** [Kadajett/agent-nestjs-skills](https://github.com/Kadajett/agent-nestjs-skills)
- **Upstream Skill:** NestJS Best Practices
- **Author:** Kadajett
- **License:** MIT

The upstream content is mirrored in the `upstream/` directory and adapted into this Agile V domain skill.

Agile V-specific adaptations (SKILL.md structure, traceability integration, evidence gates, multi-cycle versioning) are additions by the Agile V project and are licensed under CC-BY-SA-4.0.

## MIT License (Upstream Content)

```
[Include full MIT license text here]
```
```

---

## 5. Integration Checklist

### Phase 1: Structure Setup
- [ ] Create `domains/build-agent-nestjs/` directory
- [ ] Copy upstream content to `upstream/` subdirectory
- [ ] Create LICENSE file (MIT for upstream content)
- [ ] Create NOTICE.md with Kadajett attribution

### Phase 2: Skill Development
- [ ] Write `SKILL.md` following template above
- [ ] Add `sections_index` in YAML frontmatter for context optimization
- [ ] Document all NestJS-specific halt conditions
- [ ] Include context engineering rules (node_modules, generated files, monorepo)
- [ ] Cross-reference upstream rules for deep guidance

### Phase 3: Integration with Agile V Core
- [ ] Verify `extends: "build-agent"` relationship
- [ ] Confirm compliance integration (R0-R3 risk levels)
- [ ] Test skill loading in Cursor/Claude Code/VS Code
- [ ] Update SKILL_ROUTING_GUIDE.md with NestJS triggers
- [ ] Add to README.md skill table

### Phase 4: Validation
- [ ] Test with sample NestJS project (e.g., create auth module from REQ)
- [ ] Verify traceability headers in generated code
- [ ] Verify Build Manifest includes migrations and tests
- [ ] Verify halt conditions trigger correctly (circular deps, missing migrations)
- [ ] Verify context usage stays <50% for typical feature

### Phase 5: Documentation
- [ ] Update CHANGELOG.md
- [ ] Update V1.5_RELEASE_NOTES.md (or create v1.6 notes)
- [ ] Create examples/task-brief-nestjs.md (optional)
- [ ] Document sync process for upstream updates

---

## 6. Comparison: Original Plan vs. Modern Plan

| Aspect | Original Plan | Modern Plan |
|---|---|---|
| **File Count** | 13 files (SKILL.md, agile-v.skill.yaml, scope-v-mapping.md, constraints.md, evidence.md, review-checklist.md, task-brief-template.md, traceability-template.md, NOTICE.md, LICENSE, upstream/, tests/) | 3 files (SKILL.md, NOTICE.md, LICENSE) + upstream/ |
| **Metadata Format** | YAML file (`agile-v.skill.yaml`) | YAML frontmatter (agentskills.io spec) |
| **Scope Mapping** | Separate `scope-v-mapping.md` | Inline in SKILL.md sections |
| **Evidence** | Separate `evidence.md` | Reuse `agile-v-compliance` skill |
| **Constraints** | Separate `constraints.md` | Inline in "NestJS Conventions" section |
| **Traceability** | Separate `traceability-template.md` | Inherited from `build-agent`, documented in SKILL.md |
| **Review Checklist** | Separate `review-checklist.md` | Part of Red Team Verifier output |
| **Task Brief** | Separate `task-brief-template.md` | Examples in `examples/` (optional) |
| **Context Usage** | High (multiple files loaded) | Low (single SKILL.md with sections_index) |
| **Consistency** | New pattern for NestJS only | Matches existing domain skills (JS, Python, Dart) |
| **Maintenance** | Update 8+ files when upstream changes | Update 1 SKILL.md when upstream changes |

---

## 7. Example Agent Workflow (Modern Pattern)

**User Request:** "Implement user authentication with JWT for a NestJS backend. REQ-0001 approved."

**Agent Loads:**
1. `agile-v-core` (foundation)
2. `build-agent` (apex rules)
3. `build-agent-nestjs` (NestJS-specific)

**Agent Reads:**
- `REQUIREMENTS.md` (REQ-0001 acceptance criteria)
- `package.json` (confirms `@nestjs/core`, `@nestjs/common`)
- Existing module structure (determines placement)

**Agent Executes:**
1. **Pre-Execution Validation:**
   - REQ-0001 coverage: auth.module, auth.controller, auth.service, guards, DTOs, tests
   - No circular dependencies
   - Scope fits <50% context
2. **Synthesis:**
   - Creates auth.module.ts, auth.controller.ts, auth.service.ts, jwt-auth.guard.ts, login.dto.ts
   - Adds traceability headers (`// REQ-0001: User authentication via JWT`)
   - Includes E2E test file
3. **Build Manifest:**
   ```
   ART-0001 | REQ-0001 | src/auth/auth.module.ts | Auth feature module; JWT strategy
   ART-0002 | REQ-0001 | src/auth/auth.controller.ts | Login/register endpoints
   ...
   ```
4. **Decision Log:**
   ```
   2026-05-22T10:00:00Z | build-agent-nestjs | Passport JWT strategy | REQ specifies JWT; NestJS convention | REQ-0001
   ```

**Handoff to Red Team Verifier:**
- Reads BUILD_MANIFEST.md
- Reads TEST_SPEC.md (from Test Designer)
- Executes E2E tests
- Checks: DTO validation, guard coverage, no hardcoded secrets, migration presence (if DB schema changed)

---

## 8. Upstream Sync Process

When Kadajett updates `agent-nestjs-skills`:

1. **Pull upstream changes:**
   ```bash
   cd domains/build-agent-nestjs/upstream
   git remote add upstream https://github.com/Kadajett/agent-nestjs-skills.git
   git fetch upstream
   git merge upstream/main
   ```

2. **Review changes:**
   - New rules in `rules/`?
   - New best practices?
   - Breaking changes?

3. **Update SKILL.md:**
   - Incorporate new patterns into "NestJS Conventions" section
   - Update `metadata.upstream.version`
   - Document significant changes in CHANGELOG.md

4. **Test:**
   - Run validation workflow
   - Verify no context bloat
   - Verify traceability still works

5. **Commit:**
   ```
   feat(nestjs): sync upstream rules from agent-nestjs-skills v1.2.0

   - Added GraphQL-specific patterns
   - Updated dependency injection guidance
   - Improved migration rollback examples
   ```

---

## 9. Non-Goals

This integration **does not**:
- Create a new lifecycle (Agile V lifecycle applies)
- Create separate evidence system (agile-v-compliance applies)
- Create separate traceability (build-agent + agile-v-core apply)
- Flatten upstream rules into Agile V core (domain-specific skill only)
- Make NestJS mandatory for non-NestJS projects
- Bypass risk-based evidence requirements
- Allow R2/R3 tasks without review gates

---

## 10. Success Criteria

✅ **Integration complete when:**
- [ ] NestJS skill loads correctly in Cursor/Claude Code/VS Code
- [ ] `extends: "build-agent"` relationship functional
- [ ] Traceability headers appear in generated NestJS code
- [ ] Build Manifest includes NestJS artifacts (modules, controllers, services, DTOs, guards, tests, migrations)
- [ ] Halt conditions trigger for circular deps, missing migrations, unversioned API changes
- [ ] Context usage <50% for typical NestJS feature
- [ ] SKILL_ROUTING_GUIDE.md updated with NestJS triggers
- [ ] README.md includes `build-agent-nestjs` in skill table
- [ ] NOTICE.md preserves Kadajett attribution
- [ ] Upstream sync process documented
- [ ] Example workflow validated (auth module from REQ)

---

## 11. Recommended Next Steps

1. **Create directory structure** (`domains/build-agent-nestjs/`)
2. **Clone upstream content** (Kadajett/agent-nestjs-skills → `upstream/`)
3. **Write SKILL.md** (use template above)
4. **Write NOTICE.md** (attribution)
5. **Copy LICENSE** (MIT for upstream)
6. **Update SKILL_ROUTING_GUIDE.md** (NestJS triggers)
7. **Update README.md** (add to skill table)
8. **Test with real NestJS project** (e.g., implement auth from REQ-0001)
9. **Document in CHANGELOG.md**
10. **Create v1.6 release notes** (if applicable)

---

## Appendix A: Simplified File Structure

```text
domains/build-agent-nestjs/
├── SKILL.md                 # 250-300 lines (vs. 8 separate files)
├── LICENSE                  # MIT (upstream)
├── NOTICE.md                # Attribution
└── upstream/                # Mirror of Kadajett repo
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

**Total context load:** ~12-15KB (SKILL.md) vs. ~40KB+ (original 8-file approach)

---

## Appendix B: YAML Frontmatter (agentskills.io spec)

```yaml
---
name: build-agent-nestjs
description: NestJS backend build agent...
license: CC-BY-SA-4.0
metadata:
  version: "1.0"
  standard: "Agile V"
  domain: "NestJS/TypeScript/Backend"
  extends: "build-agent"
  author: agile-v.org
  upstream:
    repository: "Kadajett/agent-nestjs-skills"
    version: "1.1.0"
    license: "MIT"
  sections_index:
    - Inherited Rules
    - NestJS Conventions
    - Architecture Patterns
    - ...
---
```

**Why this format?**
- ✅ Matches existing Agile V skills (agile-v-core, build-agent-js, etc.)
- ✅ Conforms to [agentskills.io specification](https://agentskills.io/specification)
- ✅ Agents can parse frontmatter for metadata + jump to sections
- ✅ No separate YAML file to maintain

---

## Appendix C: Context Optimization Impact

| Approach | Files Loaded | Approx. Context | Agent Behavior |
|---|---|---|---|
| **Original Plan** | 8 files (SKILL.md, agile-v.skill.yaml, scope-v-mapping.md, constraints.md, evidence.md, review-checklist.md, task-brief-template.md, traceability-template.md) | ~40KB+ | High context usage; slower parsing; duplication |
| **Modern Plan** | 1 file (SKILL.md) + upstream references (on-demand) | ~12-15KB | Low context usage; fast section lookup; inherits from core |

**Result:** 60-70% reduction in context consumption, matching v1.3 optimization goals.

---

**End of Modern Integration Plan**
