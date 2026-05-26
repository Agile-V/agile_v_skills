# Understand Anything Integration

## What is Understand Anything?

[Understand Anything](https://github.com/Lum1104/Understand-Anything) is an open-source codebase
comprehension tool that builds a knowledge graph from a repository's files, functions, classes,
imports, and relationships. It can produce plain-English summaries, architectural layer views,
domain flow views, onboarding guides, diff impact overlays, and chat over the project graph.

## What this integration adds to Agile V

Agile V uses Understand Anything outputs to improve:

- **System context before building** — agents understand what they are changing before touching code.
- **Impact analysis** — identify files, functions, and tests likely affected by a change.
- **Regression-test selection** — select tests from the graph rather than guessing.
- **Graph-level traceability** — link requirements to graph nodes, changed files, and test results.
- **Audit-ready evidence** — include system understanding artifacts in the evidence bundle.

The combined positioning:

> Understand the system. Change it safely. Prove what changed.

## Integration modes

Agile V supports three modes:

| Mode | Description |
|---|---|
| `standalone` | Agile V runs without Understand Anything. All existing skills and workflows work unchanged. |
| `consume-graph` | Agile V reads an existing `.understand-anything/knowledge-graph.json`. **Recommended first mode.** |
| `invoke-understand` | Agile V triggers Understand Anything before running (requires UA installed in the environment). |

Start with `consume-graph`. Run Understand Anything separately and point Agile V at its output.

## New lifecycle with Understand Anything

```text
0. Understand   ← NEW: Gate 0, system context, impact map
1. Specify       requirements, acceptance criteria
2. Contract      interface contract
3. Build         implementation
4. Gate          executable smoke gate
5. Test          independent test design
6. Red Team      runtime + evidence verification
7. Evidence      bundle with understanding artifacts
8. Release
```

## New skills added

| Skill | Purpose |
|---|---|
| `system-understanding-agent` | Consume graph, produce system overview and architecture map |
| `impact-analysis-agent` | Map change request to affected components and regression tests |
| `graph-traceability-agent` | Link requirements to graph nodes, files, and tests |
| `regression-selection-agent` | Select and prioritize regression tests from the impact map |
| `diff-evidence-agent` | Explain the actual diff against the predicted impact |

Skills live in `agile_v_skills/skills/` following the existing pattern.

## Example workflow

```bash
# 1. Generate the knowledge graph (Understand Anything step, outside Agile V)
understand --repo .

# 2. Agile V detects the graph and runs Gate 0
agilev understand --repo .

# 3. Analyze impact of the change request
agilev impact --change-request change_request.md

# 4. Proceed through the normal Agile V lifecycle with graph context
agilev specify --from-impact .agile-v/impact/impact_map.md
agilev contract generate
agilev build
agilev test design
agilev redteam
agilev trace graph
agilev evidence export --include-understanding
```

## Example change request

See `examples/existing_repo_change_request.md`.

## Example impact map

See `examples/impact_analysis_example.md`.

## Example traceability matrix

See `examples/evidence_bundle_example.md`.

## Graph location

Agile V looks for the knowledge graph at:

```text
.understand-anything/knowledge-graph.json
```

and the diff overlay at:

```text
.understand-anything/diff-overlay.json
```

Both paths are relative to the repository root.

## Adapter contract

See `adapter_contract.md` for the formal boundary between Understand Anything graph format and
the Agile V normalized `SystemGraph` schema.

## Evidence mapping

See `evidence_mapping.md` for how graph artifacts map to Agile V evidence bundle sections.

## Security and privacy

See `security_and_privacy.md` before including knowledge graph artifacts in evidence exports.

## License note

Understand Anything is MIT-licensed. Do not vendor Understand Anything source into Agile V.
Consume its generated graph as an optional external artifact only.
