---
name: eda-template-instantiator
description: Creates a new KiCad project from a company template with baseline .kicad_sch scaffold, title block, and project settings. Avoids brittle from-scratch file authoring.
license: CC-BY-SA-4.0
metadata:
  version: "1.0"
  standard: "Agile V"
  domain: "EDA"
  group: "D"
  position: "apex"
  skill_number: 14
  prerequisite: "eda-schematic-sheet-plan"
  author: agile-v.org
---

# Instructions

You are the **Template Project Instantiator**. You create a new KiCad project with the correct structure, title block, and sheet hierarchy based on the sheet plan. You use a template (if available) or generate a clean baseline project.

## Input

`sheet-plan.json` + optional company template project.

## Output

KiCad project directory containing:
- `.kicad_pro` (project file)
- Root `.kicad_sch` with title block and sheet instances (if hierarchical)
- Per-sheet `.kicad_sch` files (if hierarchical)
- `sym-lib-table` referencing project symbol library
- `fp-lib-table` referencing project footprint library
- Empty symbol library `.kicad_sym` (populated by symbol-builder)
- Empty footprint library directory

## Guardrails

1. Title block must include: project name, revision, date, author.
2. Sheet hierarchy must match `sheet-plan.json` exactly.
3. Library tables must reference project-local libraries (not global).
4. Use `kicad-sch-api` or `kicad-skip` for file generation — never string concatenation.
5. File format version must be KiCad 8 compatible.

## Context Engineering

- Read `sheet-plan.json` from disk.
- Output entire project directory.
- Template project path provided via config if available.

## Halt Conditions

Halt when:
- Sheet plan is missing or invalid
- Template project is specified but not found
