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
| PCB schematic from requirements | EDA domain skills (Groups A-F) | "Design a PCB", "Generate schematic", "KiCad schematic", "Hardware design" |
| Component selection for PCB | `power-path-selector`, `controller-selector`, `interface-selector`, etc. | "Select regulator", "Pick MCU", "Choose connector", "BOM risk check" |
| KiCad library creation | `symbol-builder`, `footprint-builder`, `symbol-footprint-mapper` | "Create KiCad symbol", "Build footprint", "Map symbol to footprint" |
| Schematic validation | `kicad-erc-gate`, `protocol-rule-checks`, `file-integrity-check` | "Run ERC", "Validate schematic", "Check USB-C CC resistors", "Protocol checks" |
| BOM & layout handoff | `bom-generator`, `documentation-packager`, `layout-handoff-exporter` | "Generate BOM", "Export for layout", "Create handoff package" |

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

### EDA Domain — PCB Schematic Generation

**Group A — Spec & Architecture**

**`requirements-normalizer`**
- "Normalize hardware requirements"
- "Convert spec to structured format"
- "Parse interface list and constraints"
- "Define power rails and budgets"

**`schematic-sheet-plan`**
- "Plan schematic sheets"
- "Define sheet hierarchy"
- "How many sheets for this design?"
- "Organize schematic structure"

**`power-tree-plan`**
- "Design power tree"
- "Plan power distribution"
- "Define rail sequencing"
- "Calculate power budget"

**Group B — Component Research & Selection**

**`power-path-selector`**
- "Select voltage regulator"
- "Choose buck/boost/LDO"
- "Design power path"
- "Derating analysis for regulator"

**`controller-selector`**
- "Select MCU"
- "Pick microcontroller"
- "Choose SoC for this design"
- "MCU pin strategy"

**`interface-selector`**
- "Select connector for USB-C"
- "Choose I2C level shifter"
- "Design CAN interface circuit"
- "SPI/UART/Ethernet interface"

**`protection-emc-selector`**
- "Add ESD protection"
- "Select TVS diodes"
- "Design EMC filtering"
- "Reverse polarity protection"

**`analog-frontend-selector`**
- "Design analog frontend"
- "Select op-amp"
- "ADC conditioning circuit"
- "Sensor interface topology"

**`bom-risk-check`**
- "Check BOM risk"
- "Single source parts?"
- "Component lifecycle status"
- "AVL recommendations"

**Group C — Library Build**

**`symbol-builder`**
- "Create KiCad symbol"
- "Build .kicad_sym"
- "Generate symbol from datasheet"
- "Pin mapping for new part"

**`footprint-builder`**
- "Create KiCad footprint"
- "Build .kicad_mod"
- "Generate footprint from datasheet"
- "Pad layout for QFN/BGA"

**`symbol-footprint-mapper`**
- "Map symbol to footprint"
- "Link library entries"
- "Set MPN and metadata"

**`library-qa`**
- "Validate library entries"
- "Check pin/pad consistency"
- "Library quality check"
- "Multi-unit symbol validation"

**Group D — Schematic Generation**

**`template-instantiator`**
- "Create new KiCad project"
- "Scaffold schematic from template"
- "Initialize hardware project"

**`placement-engine`**
- "Place components on schematic"
- "Run ELK layout"
- "Deterministic placement"
- "Grid-aligned component positions"

**`connectivity-synthesizer`**
- "Wire the schematic"
- "Connect components"
- "Add net labels and sheet pins"
- "Route schematic connections"

**`support-passives`**
- "Add decoupling caps"
- "Place pull-up resistors"
- "Bootstrap circuit passives"
- "RC filter components"

**`net-naming-hygiene`**
- "Normalize net names"
- "Clean up net labels"
- "Name differential pairs"
- "Bus naming convention"

**Group E — Validation**

**`file-integrity-check`**
- "Check .kicad_sch file integrity"
- "Validate S-expression structure"
- "UTF-8 and syntax check"

**`kicad-render-test`**
- "Render schematic to PDF"
- "Export SVG from KiCad"
- "KiCad CLI parse check"

**`kicad-erc-gate`**
- "Run ERC"
- "Electrical rules check"
- "ERC violations report"
- "Fatal vs warning classification"

**`protocol-rule-checks`**
- "Check USB-C CC resistors"
- "Verify I2C pull-ups"
- "CAN termination check"
- "Protocol compliance verification"

**`library-resolution-check`**
- "Missing symbols or footprints?"
- "Resolve library references"
- "Check all parts are linked"

**Group F — Release & Handoff**

**`bom-generator`**
- "Generate BOM"
- "Export bill of materials"
- "BOM with alternates"
- "DNP handling"

**`documentation-packager`**
- "Package schematic docs"
- "Create design notes"
- "Bring-up checklist"
- "Export schematic PDF"

**`layout-handoff-exporter`**
- "Export netlist for layout"
- "Critical placement notes"
- "Testpoint list"
- "Hand off to PCB layout"

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
- **EDA (PCB):** See EDA Domain skills (Groups A-F, 26 skills)

### On Demand
- `agile-v-pipeline` — When orchestrating multi-agent workflows
- `agile-v-lifecycle` — When managing multi-cycle iterations
- `agile-v-compliance` — When risk/CAPA/revalidation needed
- **EDA domain** — When designing PCB schematics (see EDA workflows below)

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
| EDA Group A (spec) | Yes | No (sequential) | None |
| EDA Group B (components) | No (requires spec) | Yes (skills 4-8 parallel) | Group A |
| EDA Group C (library) | No (requires components) | Partial (10-11 parallel) | Group B |
| EDA Group D (schematic) | No (requires library) | No (sequential) | Group C |
| EDA Group E (validation) | No (requires schematic) | Yes (19-23 parallel) | Group D |
| EDA Group F (handoff) | No (requires Gate 2) | Yes (24-26 parallel) | Group E |

### Workflow 6: PCB Schematic — Fast Path (13 Skills)

1. **`requirements-normalizer`** — Structured spec from free text
2. **`schematic-sheet-plan`** — Sheet hierarchy
3. **`power-path-selector`** — Regulator selection
4. **`interface-selector`** — Per-interface circuits
5. **`symbol-builder`** + **`footprint-builder`** — Library entries (parallel)
6. **`symbol-footprint-mapper`** — Link symbols to footprints
7. **`template-instantiator`** — Scaffold KiCad project
8. **`placement-engine`** — Place components
9. **`connectivity-synthesizer`** — Wire everything
10. **`kicad-render-test`** — PDF export (parse check)
11. **`kicad-erc-gate`** — ERC validation
12. **`bom-generator`** — Bill of materials

### Workflow 7: PCB Schematic — Full Path (26 Skills)

1. **Group A** — `requirements-normalizer` → `schematic-sheet-plan` → `power-tree-plan`
2. **Human Gate 1** — Approve architecture
3. **Group B** — Component research (skills 4-9, parallelizable)
4. **`bom-risk-check`** — Lifecycle/AVL check
5. **Group C** — Library build (`symbol-builder` + `footprint-builder` parallel, then `symbol-footprint-mapper` → `library-qa`)
6. **Group D** — Schematic generation (`template-instantiator` → `placement-engine` → `connectivity-synthesizer` → `support-passives` → `net-naming-hygiene`)
7. **Group E** — Full validation (skills 19-23)
8. **Human Gate 2** — Approve validated schematic
9. **Group F** — Release & handoff (`bom-generator` + `documentation-packager` + `layout-handoff-exporter`, parallel)

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

**"How do I know when to move to the next skill?"**
- Each skill produces a **handoff artifact** (REQUIREMENTS.md, BUILD_MANIFEST.md, VALIDATION_SUMMARY.md, etc.)
- Wait for **Human Gate approval** before proceeding past Gate 1 or Gate 2
- Check **Halt Conditions** in each skill — if any are true, stop and resolve before proceeding

---

For more information, see the [Agile V Skills README](README.md) or visit [agile-v.org](https://agile-v.org).
