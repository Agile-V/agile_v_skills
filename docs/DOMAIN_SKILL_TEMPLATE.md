# Domain Skill Template

This template guides the creation of new domain-specific build agent skills for the Agile V framework.

**Purpose:** Domain skills extend **build-agent** with language/framework-specific patterns while maintaining full Agile V traceability and compliance.

---

## Template Structure

### 1. Frontmatter (YAML)

```yaml
---
name: build-agent-{domain}
description: {Brief description of domain}. Extends build-agent with {domain} conventions. Use when building {use cases}.
license: CC-BY-SA-4.0
metadata:
  version: "1.0"
  standard: "Agile V"
  domain: "{Domain Name}"
  extends: "build-agent"
  author: agile-v.org
  sections_index: [
    "Inherited Rules",
    "SCOPE-V Participation",
    "{Domain} Architecture & Patterns",
    "Evidence Requirements",
    "Halt Conditions",
    "Context Engineering",
    "When to Use"
  ]
---
```

**Fields:**
- `name`: Must be `build-agent-{domain}` (lowercase, hyphenated)
- `description`: 1-2 sentences explaining domain and use cases
- `domain`: Human-readable domain name (e.g., "Python", "Go", "Rust")
- `extends`: Always "build-agent"
- `sections_index`: List all major sections for navigation

---

### 2. Instructions Header

```markdown
# Instructions
You are the **{Domain} Build Agent** at the Apex of the Agile V infinity loop. You extend the core **build-agent** skill with {domain} domain knowledge. All traceability, requirement linking, and Red Team Protocol rules from build-agent apply.

## Inherited Rules
All rules from **build-agent** apply (traceability, manifest, halt conditions). This skill adds {domain}-specific conventions only.
```

**Purpose:** Establishes context and inheritance relationship with base build-agent.

---

### 3. SCOPE-V Participation (~20 lines)

```markdown
## SCOPE-V Participation

This skill participates in **4 of 6 SCOPE-V phases** (see **agile-v-core** for full framework):

- **Constrain:** Apply {domain} architectural constraints (structure, patterns, security)
- **Orchestrate:** Synthesize {domain} artifacts with full traceability (primary role)
- **Prove:** Generate evidence per risk level ({domain-specific tools})
- **Evolve:** Log decisions with rationale; update knowledge from failures

**Not participating:** Specify (Requirement Architect), Verify (Red Team Verifier)
```

**Purpose:** Maps skill to SCOPE-V framework phases. Standard pattern: Build agents participate in Constrain, Orchestrate, Prove, Evolve.

**Customization:**
- List domain-specific tools in Prove (e.g., "pytest, mypy, ruff" for Python)
- Keep structure identical to maintain consistency

---

### 4. {Domain} Architecture & Patterns (300-400 lines)

This is the **core section**. Organize into 8-12 subsections covering:

#### Template Subsections

**A. Project Structure**
- Recommended directory layouts for different project types
- Package/library structure
- Application structure
- Monorepo considerations (if applicable)

**Example:**
````markdown
### 1. Project Structure

**Package/Library:**
```
my-package/
├── {config file}
├── src/
│   └── {package structure}
├── tests/
└── README.md
```

**Application:**
```
app/
├── {config file}
├── src/
│   ├── {main entry point}
│   ├── {feature modules}
│   └── {config}
├── tests/
└── {deployment files}
```

**Principles:**
- {Guideline 1}
- {Guideline 2}
````

**B. Language Best Practices**
- Type system usage
- Naming conventions
- Style guides
- Modern language features

**C. Dependency Management**
- Package manager(s)
- Version pinning strategies
- Lock files
- Dependency security

**D. Framework Patterns**
- Popular frameworks in the ecosystem
- Code examples with traceability comments
- Best practices per framework

**Example:**
```{lang}
// Parent: REQ-0042
{framework import statements}

{code example demonstrating pattern}
```

**E. Architecture Patterns**
- Recommended architectural styles
- Layer separation
- Modularization
- Testability

**F. Security Patterns**
- Authentication/authorization
- Secrets management
- Input validation
- Common vulnerabilities and prevention

**G. Testing Strategy**
- Unit testing framework(s)
- Integration testing
- E2E testing
- Mocking and fixtures
- Coverage requirements

**H. Build and Deployment**
- Build tools
- Configuration management
- Environment handling
- Platform-specific considerations

**Additional subsections as needed:**
- Database/ORM patterns
- State management
- API patterns
- Async/concurrency patterns
- CLI patterns
- Performance optimization

**Guidelines:**
1. Include code examples for each pattern (5-15 lines)
2. Add traceability comments (// Parent: REQ-XXXX or # Parent: REQ-XXXX)
3. Reference real-world tools and libraries
4. Provide "CORRECT" vs "WRONG" examples for security-critical patterns

---

### 5. Evidence Requirements (80-120 lines)

```markdown
## Evidence Requirements

Inherits R0-R3 framework from **agile-v-compliance**. {Domain}-specific additions below.

### R0: Exploratory
Base evidence applies (short result summary, no production credentials, no production code path changed).

**{Domain}-Specific Additions:** None (or minimal exploratory additions)

### R1: Routine
Base evidence applies (affected files, diff summary, targeted tests or explanation, lint/typecheck, residual-risk note).

**{Domain}-Specific Additions:**
- {Tool 1} passes: `{command}` output
- {Tool 2} passes: `{command}` output
- {Test framework}: `{command}` results (if applicable)
- No new {language-specific} warnings without justification

### R2: Production
Base evidence applies (task brief with REQ IDs, implementation plan, affected files, executed commands, test results, regression coverage, acceptance criteria → test mapping, security/static check, rollback path, reviewer decision).

**{Domain}-Specific Additions:**
- **{Critical artifact type 1}:** {Description and requirements}
- **{Critical artifact type 2}:** {Description and requirements}
- **Security scan:** `{tool}` output (0 high/critical vulnerabilities)
- **Coverage:** `{command}` output (>80% for critical modules)
- **{Domain-specific requirement}:** {Evidence needed}
- **Dependencies:** If new dependencies added, rationale in manifest + license check

### R3: High Assurance
Base evidence applies (all R2 evidence + independent verification agent review, traceability matrix, explicit human sign-off, audit artifact, release decision rationale).

**{Domain}-Specific Additions:**
- **{Safety-critical requirement 1}:** {Evidence needed}
- **{Safety-critical requirement 2}:** {Evidence needed}
- **Security audit:** {Static analysis tools} + {dependency scan} + code review for {vulnerabilities}
- **{Performance/compliance requirement}:** {Evidence needed}
```

**Purpose:** Defines what evidence is required at each risk level.

**Customization:**
- R0: Usually inherits from base only
- R1: Add linting, type checking, unit tests specific to domain
- R2: Add integration tests, security scans, domain-specific artifacts (migrations, API docs, etc.)
- R3: Add compliance artifacts, advanced testing, independent verification

---

### 6. Halt Conditions (40-60 lines)

```markdown
## Halt Conditions

In addition to base **build-agent** halt conditions, {Domain} Build Agent must HALT immediately if:

1. **{Critical issue 1}**
   - {Description of issue}
   - **Action:** {Remediation steps}

2. **{Critical issue 2}**
   - {Description of issue}
   - **Action:** {Remediation steps}

3. **{Critical issue 3}**
   - {Description of issue}
   - **Action:** {Remediation steps}

4. **Auth/security change without R2+ risk classification**
   - Password hashing, auth logic, permission checks changed but classified as R1
   - **Action:** Escalate to R2, add security evidence

5. **{Domain-specific security issue}**
   - {Description}
   - **Action:** {Remediation}

6. **{Domain-specific compliance issue}**
   - {Description}
   - **Action:** {Remediation}

7. **{Domain-specific performance/resource issue}**
   - {Description}
   - **Action:** {Remediation}

8. **{Domain-specific build/deployment issue}**
   - {Description}
   - **Action:** {Remediation}
```

**Purpose:** Pre-execution validation to prevent common errors and security vulnerabilities.

**Standard halt conditions to include:**
- Security vulnerabilities (SQL injection, XSS, secrets in code, etc.)
- Auth/permission changes without proper risk level
- Missing critical artifacts (tests, migrations, docs)
- Compliance violations (static analysis errors, security audit failures)
- Resource issues (memory leaks, performance degradation)
- Build/deployment blockers

---

### 7. Context Engineering (~30 lines)

```markdown
## Context Engineering ({Domain}-Specific)

Inherited from build-agent; additional {domain} considerations:

- **{Large artifact type 1}** must never be loaded into context. Reference by file path and metadata only.
- **{Framework-specific files}** should be decomposed by {module type}. Build one module per sub-agent context.
- **{High-context artifacts}** are high-context artifacts. {Strategy for handling them}.
- **{Dependency files}** (`{file names}`): read from disk, do not duplicate {content} in conversation.

**Additional constraints:**
- {Constraint 1}
- {Constraint 2}
```

**Purpose:** Optimize context window usage by defining what should/shouldn't be loaded.

---

### 8. When to Use (~10 lines)

```markdown
## When to Use
- {Use case 1}
- {Use case 2}
- {Use case 3}
- {Use case 4}
- {Use case 5}

**Auto-trigger hints:** {Framework name} projects detected by {file indicator}.
```

**Purpose:** Help orchestrators know when to activate this skill.

---

## Examples

See reference implementations:
- **build-agent-nestjs** (479 lines) - Backend framework with TypeScript
- **build-agent-python** (1007 lines) - General-purpose language with multiple frameworks
- **build-agent-js** (1213 lines) - Frontend + backend JavaScript/TypeScript
- **build-agent-dart** (1454 lines) - Flutter/mobile development
- **build-agent-embedded** (1040 lines) - Safety-critical embedded C/C++

---

## Quality Checklist

Before submitting a new domain skill:

### Frontmatter
- [ ] `name` follows `build-agent-{domain}` pattern
- [ ] `extends: "build-agent"` is set
- [ ] `sections_index` lists all sections
- [ ] Version starts at "1.0"

### Content
- [ ] "Inherited Rules" section present
- [ ] SCOPE-V Participation section present (4 of 6 phases)
- [ ] Architecture & Patterns section is comprehensive (300-400 lines minimum)
- [ ] Code examples include traceability comments
- [ ] Evidence Requirements section with R0-R3
- [ ] Halt Conditions section with 6-10 domain-specific conditions
- [ ] Context Engineering section present
- [ ] "When to Use" section with auto-trigger hints

### Code Examples
- [ ] All examples include `// Parent: REQ-XXXX` or `# Parent: REQ-XXXX`
- [ ] Examples are practical and realistic
- [ ] Security examples show CORRECT vs WRONG patterns
- [ ] Examples cover common use cases in the domain

### Quality
- [ ] Target length: 400-500 lines (can go higher for comprehensive coverage)
- [ ] No duplication of base build-agent content
- [ ] References to real tools and frameworks
- [ ] Clear, actionable guidance
- [ ] Consistent with other domain skills

### Testing
- [ ] Skill validates with YAML parser
- [ ] All sections present and properly formatted
- [ ] No broken internal references
- [ ] Follows Agile V philosophy (traceability, evidence, gates)

---

## Target Metrics

| Category | Target | Rationale |
|----------|--------|-----------|
| **Total lines** | 600-800 lines | Optimal balance of quality and context efficiency |
| **Architecture & Patterns** | 250-400 lines | Core content, streamlined examples |
| **Evidence Requirements** | 80-120 lines | Complete R0-R3 coverage |
| **Halt Conditions** | 40-60 lines | Critical pre-execution validation |
| **Code examples** | 8-15 examples | Key patterns with traceability |
| **Traceability comments** | All code examples | Mandatory for Agile V |
| **Context usage** | <20% of 200K window | Leaves 160KB+ for user work |

### Optimization Guidelines

**When skills exceed 800 lines:**
1. Reduce code examples from 3-4 per pattern to 1-2 key examples
2. Convert verbose explanations to concise bullet points
3. Consolidate similar frameworks (keep primary detailed, others brief)
4. Remove duplicate patterns showing same concept
5. **Never compromise:** Evidence Requirements, Halt Conditions, Security examples

**Example: Framework consolidation**
- ✅ Python: FastAPI (primary detail) + Flask/Django (brief mention)
- ✅ JavaScript: React/Next.js (primary) + Express (brief)
- ✅ Dart: BLoC (primary) + Provider/Riverpod (brief)
- ✅ Embedded: FreeRTOS (primary) + Zephyr (brief)

---

## Upstream Integration

If integrating content from an existing upstream repository:

1. Create `upstream/` directory in skill folder
2. Clone/copy upstream content
3. Create `NOTICE.md` with attribution:
   ```markdown
   # Attribution Notice
   
   This skill integrates patterns and guidance from:
   
   ## {Upstream Project Name}
   - **Repository:** {URL}
   - **License:** {License}
   - **Copyright:** {Copyright notice}
   - **Integration Date:** {Date}
   
   The upstream content has been adapted to fit the Agile V framework...
   ```
4. Include `LICENSE` file if different from CC-BY-SA-4.0
5. Update frontmatter with `adapted_from` field

---

## Contributing

When contributing a new domain skill:

1. Follow this template exactly
2. Use reference implementations as style guide
3. Include comprehensive code examples
4. Test with real projects in the domain
5. Submit PR with:
   - Skill file
   - NOTICE.md (if upstream integration)
   - LICENSE (if different from base)
   - Example project or test suite

For questions, see:
- **SKILL_ROUTING_GUIDE.md** - How skills are activated
- **agile-v-core/SKILL.md** - SCOPE-V framework
- **build-agent/SKILL.md** - Base build agent patterns

---

**Version:** 1.0  
**Last Updated:** 2026-05-22  
**Maintainer:** agile-v.org
