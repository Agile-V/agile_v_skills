# Agile V Skills: Routing Guide

This guide maps common user phrases and intents to the appropriate Agile V skill(s). Use this to quickly identify which skill(s) to load for a given task.

## Quick Reference Table

| User Intent | Skill(s) to Load | Typical Phrases |
|---|---|---|
| Convert user research/feedback into requirements | `discovery-analyst` | "Analyze user interviews", "Convert feedback to requirements", "I have customer insights" |
| Write formal requirements from product intent | `requirement-architect` | "Write PRD", "Create requirements", "Define features", "I need a blueprint" |
| Check requirements for ambiguity/conflicts | `logic-gatekeeper` | "Validate requirements", "Check for ambiguity", "Review constraints", "Are requirements testable?" |
| Generate code from requirements | `build-agent` + domain-specific (e.g., `build-agent-python`) | "Implement features", "Generate code", "Build from requirements" |
| Design test cases | `test-designer` | "Create tests", "Design verification suite", "How do we verify this?" |
| Verify/test implementation | `red-team-verifier` | "Run verification", "Test the build", "Challenge the code", "Find defects" |
| Security threat modeling | `threat-modeler` | "Identify security threats", "STRIDE analysis", "Privacy assessment", "What are the security risks?" |
| UX/design specifications | `ux-spec-author` | "Define user flows", "Design spec", "Accessibility requirements", "What should the UX be?" |
| Sprint planning & backlog management | `agile-v-product-owner` | "Plan sprint", "Prioritize backlog", "Create user stories", "Track velocity" |
| Release planning & deployment | `release-manager` | "Plan release", "Create rollout plan", "Deployment checklist", "How do we deploy?" |
| Production monitoring & metrics | `observability-planner` | "Define metrics", "Create dashboards", "Set up alerts", "Monitor production" |
| Generate compliance documentation | `compliance-auditor` | "Audit trail", "Traceability matrix", "VSR", "ISO compliance", "Decision log" |
| Generate repository documentation | `documentation-agent` | "Generate docs", "Create README", "Document architecture", "ISO 9001 docs" |
| Orchestrate full pipeline | `agile-v-pipeline` + others | "Run full workflow", "Execute pipeline", "End-to-end process" |
| Multi-cycle management | `agile-v-lifecycle` | "Start Cycle 2", "Manage iterations", "Change requests", "Version requirements" |
| Business strategy & vision | `venture-strategist` | "Define vision", "Business model", "Product portfolio", "Competitive analysis", "Fundraising" |
| R&D & innovation pipeline | `rd-innovator` | "Evaluate technology", "Prototype", "R&D pipeline", "Technology radar", "Patent tracking" |
| Go-to-market & marketing | `gtm-executor` | "Launch plan", "Marketing strategy", "Growth experiments", "Sales enablement", "Channel strategy" |
| Financial & operational planning | `business-operations` | "Budget", "OKRs", "Vendor management", "Resource planning", "Runway" |

## Detailed Skill Triggers

### Discovery Phase (Pre-Requirements)

**`discovery-analyst`**
- "I have user interview transcripts"
- "Convert customer feedback to requirements"
- "Analyze support tickets for patterns"
- "We did user research, now what?"
- "Create discovery log"
- "Identify assumptions and hypotheses"
- "Plan experiments to validate ideas"

**`threat-modeler`**
- "What are the security risks?"
- "Perform threat modeling"
- "STRIDE analysis"
- "Privacy impact assessment"
- "Identify security requirements"
- "We need to assess data privacy"
- "What threats should we consider?"

**`ux-spec-author`**
- "Define user flows"
- "Create design specification"
- "What are the accessibility requirements?"
- "Design the interaction patterns"
- "Error states and edge cases"
- "Performance budgets for UX"
- "Convert wireframes to requirements"

### Requirements Phase (Left Side of V)

**`requirement-architect`**
- "Write PRD"
- "Create requirements document"
- "Convert product intent to requirements"
- "Define features formally"
- "Generate requirement IDs"
- "Blueprint approval"
- "Formalize candidate requirements"

**`logic-gatekeeper`**
- "Validate requirements"
- "Check for ambiguity"
- "Are the requirements testable?"
- "Review physical constraints"
- "Check for conflicts"
- "Verify requirement completeness"
- "Validate priority assignments"

### Synthesis Phase (Apex of V)

**`build-agent`** (core, language-agnostic)
- "Implement the features"
- "Generate artifacts"
- "Build from requirements"
- "Create build manifest"

**`build-agent-python`**
- "Build Python backend"
- "Implement in Python"
- "Create Python package"
- "FastAPI/Flask/Django application"

**`build-agent-js`**
- "Build React app"
- "Implement in TypeScript"
- "Create Node.js backend"
- "Next.js/Express application"

**`build-agent-dart`**
- "Build Flutter app"
- "Implement in Dart"
- "Create mobile application"

**`build-agent-embedded`**
- "Build firmware"
- "Implement for microcontroller"
- "C/C++ embedded code"
- "Hardware integration"

**`test-designer`**
- "Design test cases"
- "Create verification suite"
- "How do we test this?"
- "Generate test specification"
- "Define acceptance tests"

**`schematic-generator`**
- "Generate schematic"
- "Create PCB design"
- "Hardware design from requirements"
- "Netlist generation"

### Verification Phase (Right Side of V)

**`red-team-verifier`**
- "Run verification"
- "Test the implementation"
- "Verify against requirements"
- "Find defects"
- "Challenge the build"
- "Execute test suite"
- "Validation summary"

### Compliance & Documentation

**`compliance-auditor`**
- "Generate traceability matrix"
- "Create decision log"
- "Audit trail"
- "VSR (Validation Summary Report)"
- "ISO 9001 compliance"
- "Quality metrics"
- "Track defects and CAPAs"

**`documentation-agent`**
- "Generate repository docs"
- "Create README and architecture docs"
- "ISO 9001 documentation"
- "V-Model documentation"
- "Standards compliance docs"

### Agile Delivery

**`agile-v-product-owner`**
- "Plan sprint"
- "Create backlog"
- "Prioritize user stories"
- "Sprint planning"
- "Retrospective"
- "Track velocity"
- "Convert REQs to stories"
- "Generate change requests from retro"

### Release & Operations

**`release-manager`**
- "Plan release"
- "Create rollout plan"
- "Deployment strategy"
- "Release notes"
- "Rollback procedure"
- "Pre-release checklist"
- "Post-release validation"

**`observability-planner`**
- "Define production metrics"
- "Create monitoring dashboards"
- "Set up alerts"
- "SLO definition"
- "Monitor production"
- "Incident detection"
- "Error budget tracking"

### Business Track (Strategy, R&D, GTM, Operations)

**`venture-strategist`**
- "Define the product vision"
- "Create business model"
- "Build product portfolio"
- "Competitive analysis"
- "Market positioning"
- "Fundraising strategy"
- "Investor pitch materials"
- "Strategic OKRs"

**`rd-innovator`**
- "Evaluate this technology"
- "Create technology radar"
- "Start R&D initiative"
- "Build a prototype"
- "Track patents and IP"
- "Transfer prototype to engineering"
- "Technology scouting"
- "Innovation pipeline"

**`gtm-executor`**
- "Plan product launch"
- "Marketing strategy"
- "Define ideal customer profile"
- "Channel strategy"
- "Growth experiments"
- "Sales battle cards"
- "Pricing strategy"
- "Customer acquisition plan"

**`business-operations`**
- "Create budget"
- "Financial planning"
- "Set up OKRs"
- "Vendor evaluation"
- "Resource planning"
- "Team capacity"
- "Operational risk assessment"
- "Track burn rate and runway"

### Orchestration & Lifecycle

**`agile-v-core`**
- Load first in any Agile V session (foundational)
- "What are Agile V principles?"
- "Explain directives"
- "Context engineering rules"
- "Cost governance"

**`agile-v-pipeline`**
- "Orchestrate the workflow"
- "Run the full pipeline"
- "Stage handoffs"
- "Priority-ordered execution"
- "Checkpoint types"

**`agile-v-lifecycle`**
- "Start Cycle 2"
- "Manage iterations"
- "Create change request"
- "Multi-cycle management"
- "Versioned requirements"
- "Archive previous cycle"

**`agile-v-compliance`**
- "Risk management"
- "CAPA protocol"
- "Canary tests"
- "Revalidation triggers"
- "Security controls"

## Common Workflows

### Workflow 1: New Project from Scratch

1. **`discovery-analyst`** — Convert user research → candidate REQs
2. **`threat-modeler`** — Identify security/privacy REQs
3. **`ux-spec-author`** — Define design constraints → candidate REQs
4. **`requirement-architect`** — Formalize all candidate REQs → REQUIREMENTS.md
5. **`logic-gatekeeper`** — Validate requirements
6. **Human Gate 1** — Approve blueprint
7. **`build-agent-*`** + **`test-designer`** — Parallel synthesis
8. **`red-team-verifier`** — Execute tests
9. **Human Gate 2** — Approve validation
10. **`release-manager`** — Plan deployment
11. **`observability-planner`** — Set up monitoring
12. **`compliance-auditor`** — Generate audit trail

### Workflow 2: Add New Feature (Cycle 2)

1. **`agile-v-lifecycle`** — Start Cycle 2
2. **`discovery-analyst`** — (if new research) Convert insights
3. **`requirement-architect`** — Create CR-XXXX, add new REQs
4. **`logic-gatekeeper`** — Validate new/modified REQs only
5. **Human Gate 1** — Approve changes
6. Continue with build → verify → release

### Workflow 3: Sprint-Based Delivery

1. **`requirement-architect`** + **`logic-gatekeeper`** — Full REQ set for cycle
2. **Human Gate 1** — Approve
3. **`agile-v-product-owner`** — Decompose into backlog, plan Sprint 1
4. For each sprint:
   - **`build-agent-*`** — Build sprint scope
   - **`test-designer`** — Design tests for sprint scope
   - **`red-team-verifier`** — Verify sprint artifacts
   - **`agile-v-product-owner`** — Sprint review + retro
5. After all sprints → **Human Gate 2** → Release

### Workflow 4: Security-First Development

1. **`threat-modeler`** — STRIDE analysis → security REQs
2. **`requirement-architect`** — Formalize security REQs (CRITICAL priority)
3. **`logic-gatekeeper`** — Validate
4. **Human Gate 1** — Approve
5. **`build-agent-*`** — Implement security controls
6. **`test-designer`** — Create security test cases (SQLMap, XSS, etc.)
7. **`red-team-verifier`** — Execute security tests + penetration testing
8. **Human Gate 2** — Security sign-off required

### Workflow 5: Production Incident Response

1. **Incident occurs** → `observability-planner` detects via alert
2. **`release-manager`** — Execute rollback plan
3. **`observability-planner`** — Log incident (INC-XXXX)
4. Root cause analysis → identify REQ gap
5. **`agile-v-lifecycle`** — Create CR-XXXX
6. **`requirement-architect`** — Update REQ-XXXX
7. **`logic-gatekeeper`** — Re-validate
8. Re-enter pipeline for fix

### Workflow 6: Business Track — New Venture

1. **`venture-strategist`** — Vision, business model, product portfolio
2. **Business Gate 0** — Approve strategy
3. **`rd-innovator`** — Technology assessment, R&D initiatives, prototyping
4. **`gtm-executor`** — Go-to-market strategy, channel planning
5. **Business Gate 1** — Approve R&D portfolio + GTM strategy
6. **`business-operations`** — Financial plan, OKRs, resource allocation
7. **Business Gate 2** — Approve budget + operational plan
8. **Enter Engineering Pipeline** — `discovery-analyst` (portfolio → product intent)
9. Continue: Requirements → Build → Verify → Release → Monitor
10. **Feedback** — Production metrics + growth data → inform next business cycle

### Workflow 7: Business Track — Product Launch

1. **`venture-strategist`** — Confirm PORT-XXXX launch decision
2. **`gtm-executor`** — Launch plan (MKT-XXXX), marketing materials, campaigns
3. **`business-operations`** — Budget allocation (FIN-XXXX)
4. **`release-manager`** — Engineering deployment coordination
5. **`gtm-executor`** — Execute launch phases (pre-launch → launch → post-launch)
6. **`observability-planner`** — Monitor production metrics
7. **`gtm-executor`** — Growth experiments (GROW-XXXX), iterate
8. **Feedback** — Results → `venture-strategist` (portfolio updates), `discovery-analyst` (next cycle)

### Workflow 8: Business Track — R&D to Product

1. **`venture-strategist`** — Strategic direction (VIS-XXXX, PORT-XXXX)
2. **`rd-innovator`** — Technology scouting (TECH-XXXX), R&D initiative (RDI-XXXX)
3. **`rd-innovator`** — Prototype (PROTO-XXXX), validate against success criteria
4. **Business Gate 1 (R&D)** — Approve transfer to engineering
5. **`rd-innovator`** — Create Transfer Package
6. **`discovery-analyst`** — Convert transfer package → OBS/INS/HYP entries
7. Continue: Requirements → Build → Verify → Release
8. **`rd-innovator`** — Production feedback updates TECH_RADAR.md

## Skill Loading Recommendations

### Essential Core (Load First)
- `agile-v-core` — Always load first (foundational values & directives)

### By Phase
- **Discovery:** `discovery-analyst`, `threat-modeler`, `ux-spec-author`
- **Requirements:** `requirement-architect`, `logic-gatekeeper`
- **Synthesis:** `build-agent-*` (domain-specific), `test-designer`
- **Verification:** `red-team-verifier`
- **Release:** `release-manager`, `observability-planner`
- **Compliance:** `compliance-auditor`, `documentation-agent`
- **Agile Delivery:** `agile-v-product-owner`

### By Business Phase
- **Strategy:** `venture-strategist`
- **Innovation:** `rd-innovator`
- **Market Execution:** `gtm-executor`
- **Operations:** `business-operations`

### On Demand
- `agile-v-pipeline` — When orchestrating multi-agent workflows
- `agile-v-lifecycle` — When managing multi-cycle iterations
- `agile-v-compliance` — When risk/CAPA/revalidation needed

## Skill Compatibility Matrix

| Skill | Run Alone? | Run in Parallel? | Dependencies |
|---|---|---|---|
| `agile-v-core` | Yes (always load first) | N/A | None |
| `discovery-analyst` | Yes | No (sequential before requirement-architect) | None |
| `threat-modeler` | Yes | Yes (parallel with ux-spec-author) | None |
| `ux-spec-author` | Yes | Yes (parallel with threat-modeler) | None |
| `requirement-architect` | Yes | No (wait for discovery/threat/ux inputs) | `agile-v-core` |
| `logic-gatekeeper` | No (requires REQUIREMENTS.md) | No | `requirement-architect` |
| `build-agent-*` | No (requires approved REQs) | Yes (parallel with test-designer) | `logic-gatekeeper` |
| `test-designer` | No (requires approved REQs) | Yes (parallel with build-agent) | `logic-gatekeeper` |
| `red-team-verifier` | No (requires artifacts + tests) | No | `build-agent-*`, `test-designer` |
| `release-manager` | No (requires Gate 2 approval) | Yes (parallel with observability-planner) | `red-team-verifier` |
| `observability-planner` | No (requires REQs) | Yes (parallel with release-manager) | `requirement-architect` |
| `compliance-auditor` | Yes (observes all stages) | Yes (runs continuously) | None |
| `documentation-agent` | Yes (on demand) | Yes | None |
| `agile-v-product-owner` | No (requires REQs) | No (orchestrates sprints) | `requirement-architect` |
| `agile-v-pipeline` | No (orchestrates others) | N/A | `agile-v-core` |
| `agile-v-lifecycle` | No (manages cycles) | N/A | `agile-v-core` |
| `venture-strategist` | Yes | No (upstream of all business skills) | `agile-v-core` |
| `rd-innovator` | Yes | Yes (parallel with gtm-executor) | `venture-strategist` |
| `gtm-executor` | No (requires PORTFOLIO.md) | Yes (parallel with rd-innovator) | `venture-strategist` |
| `business-operations` | No (requires strategic OKRs) | Yes (parallel with rd-innovator, gtm-executor) | `venture-strategist` |

## Tips for Effective Skill Use

1. **Always start with `agile-v-core`** — It sets foundational values and directives.

2. **Discovery before requirements** — Run `discovery-analyst`, `threat-modeler`, `ux-spec-author` *before* `requirement-architect` for complete requirements.

3. **Parallel synthesis** — Run `build-agent-*` and `test-designer` in parallel (fresh context each) for speed.

4. **Independent verification** — Never let `red-team-verifier` inherit context from `build-agent` (prevents bias).

5. **Continuous compliance** — `compliance-auditor` can observe all stages; doesn't block workflow.

6. **Sprint-based flexibility** — Use `agile-v-product-owner` to break large cycles into manageable sprints.

7. **Post-release rigor** — Don't skip `release-manager` and `observability-planner` — they close the feedback loop.

8. **Security shifts left** — Run `threat-modeler` early (before code) to catch threats before implementation.

9. **Multi-cycle evolution** — Use `agile-v-lifecycle` for Cycle 2+ to manage change requests and versioning.

10. **Context optimization** — Load only the skills you need for the current stage; use file paths in handoffs (not full file contents).

11. **Business before engineering** — Run `venture-strategist` before `discovery-analyst` when starting a new product. Strategy defines *what* to build; engineering defines *how*.

12. **Traceable marketing** — Always run `gtm-executor` with access to `VALIDATION_SUMMARY.md` — marketing claims must trace to verified capabilities.

13. **R&D is not engineering** — Prototypes from `rd-innovator` are *not* production code. Transfer to engineering means fresh build from requirements.

## Troubleshooting

**"I'm not sure which skill to use"**
- Start with `agile-v-core` for foundational guidance
- Check the Quick Reference Table above
- When in doubt, ask: "What phase am I in?" (Discovery → Requirements → Synthesis → Verification → Release)

**"Can I skip a skill?"**
- Discovery skills (discovery-analyst, threat-modeler, ux-spec-author): Optional if requirements are already clear
- `requirement-architect`: Required (no REQs = no traceability)
- `logic-gatekeeper`: Required (prevents ambiguous REQs)
- `build-agent-*`: Required for code generation
- `test-designer`: Required for independent verification
- `red-team-verifier`: Required (Gate 2 depends on it)
- `release-manager`, `observability-planner`: Recommended for production deployment
- `compliance-auditor`: Recommended for audit trail (required for regulated industries)

**"Skills seem to overlap"**
- `requirement-architect` vs `discovery-analyst`: Discovery analyzes messy inputs; Requirement Architect formalizes them
- `build-agent` (core) vs `build-agent-python`: Core is language-agnostic; domain-specific extends it
- `release-manager` vs `observability-planner`: Release handles deployment; Observability handles monitoring
- `agile-v-pipeline` vs `agile-v-lifecycle`: Pipeline orchestrates stages within a cycle; Lifecycle manages multiple cycles
- `venture-strategist` vs `discovery-analyst`: Venture Strategist defines *what product to build* (business); Discovery Analyst converts *user research into requirements* (engineering)
- `gtm-executor` vs `release-manager`: GTM handles market launch (marketing, campaigns); Release Manager handles technical deployment
- `rd-innovator` vs `build-agent`: R&D explores and prototypes (disposable); Build Agent creates production artifacts from requirements
- `business-operations` vs `compliance-auditor`: Business Operations manages financial/operational compliance; Compliance Auditor manages engineering/regulatory compliance

**"How do I know when to move to the next skill?"**
- Each skill produces a **handoff artifact** (REQUIREMENTS.md, BUILD_MANIFEST.md, VALIDATION_SUMMARY.md, etc.)
- Wait for **Human Gate approval** before proceeding past Gate 1 or Gate 2
- Check **Halt Conditions** in each skill — if any are true, stop and resolve before proceeding

---

For more information, see the [Agile V Skills README](README.md) or visit [agile-v.org](https://agile-v.org).
