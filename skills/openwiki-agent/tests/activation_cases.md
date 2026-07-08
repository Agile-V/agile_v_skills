# Activation Cases: openwiki-agent

## When should this skill activate?

| Case | Input signal | Expected behavior |
|---|---|---|
| AC-001 | `openwiki/` exists in the repository | Skill activates; runs `agilev wiki status --json` before relying on repo docs. |
| AC-002 | `.agile-v/wiki/manifest.json` exists | Skill activates even if `openwiki/` was moved/renamed unexpectedly (flags as inconsistency). |
| AC-003 | User asks "is the wiki up to date?" | Skill activates; runs `agilev wiki validate --json` and reports result. |
| AC-004 | User asks for an onboarding guide on an existing repo | Skill activates; reads `openwiki/ONBOARDING.md` and `openwiki/ARCHITECTURE.md` after validating. |
| AC-005 | Task touches `src/agilev/pcb/**` (or equivalent domain path) | Skill activates; reads `openwiki/domains/pcb.md` specifically, not the whole wiki. |
| AC-006 | Task touches both a PCB path and a firmware path | Skill activates; also reads `openwiki/co-verification.md`. |
| AC-007 | Task has a task ID and is closing out (evidence collection stage) | Skill activates; runs `agilev wiki snapshot --task <id>`. |
| AC-008 | Repository has no `openwiki/` and no `.agile-v/wiki/` | Skill activates in "absent" mode: notes absence, recommends `agilev wiki init`, proceeds without blocking. |

## Chaining behavior

- Typically runs before or alongside `system-understanding-agent` when both
  OpenWiki and Understand Anything are present in a repository — they are
  complementary (OpenWiki: curated narrative docs; Understand Anything:
  structural knowledge graph), not redundant.
- After this skill runs: proceed to the requirements/build/verification
  skills relevant to the task; this skill never gates progression on its
  own.
