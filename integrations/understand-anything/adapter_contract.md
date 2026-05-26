# Adapter Contract: Understand Anything → Agile V

## Purpose

This document defines the formal boundary between the Understand Anything external graph format
and the Agile V normalized `SystemGraph` schema.

Agile V must not assume the Understand Anything graph schema is stable. The adapter layer
provides a versioned, tolerant translation.

---

## Boundary diagram

```text
Understand Anything native graph
  (.understand-anything/knowledge-graph.json)
            |
            v
  Agile V Graph Adapter
  (agilev/integrations/understand_anything/)
            |
            v
  Normalized SystemGraph
  (Agile V internal schema)
            |
      +-----+------+
      |            |
      v            v
  ImpactMap   GraphTraceabilityMatrix
```

---

## Input contract

### Required file

```text
.understand-anything/knowledge-graph.json
```

### Minimum required content

The adapter will attempt to locate node and edge arrays using a tolerant search strategy.
It will succeed if the graph file contains **at least one** of the following:

**Node arrays** (searched in order):
1. `nodes`
2. `graph.nodes`
3. `files`
4. `functions`
5. `classes`
6. `entities`

**Edge arrays** (searched in order):
1. `edges`
2. `relationships`
3. `links`
4. `dependencies`

If no node array is found, the adapter returns an empty graph with a warning (not an error).
This allows Agile V to continue with reduced context.

### Optional file

```text
.understand-anything/diff-overlay.json
```

Used by the `diff-evidence-agent` to compare predicted vs actual impact.

---

## Output contract

The adapter always produces a `SystemGraph` conforming to the Agile V JSON schema at:

```text
agentic_agile_v/schemas/system_graph.schema.json
```

### SystemGraph

```json
{
  "schema_version": "1.0.0",
  "source": "understand-anything",
  "source_graph_path": ".understand-anything/knowledge-graph.json",
  "source_graph_hash": "sha256:<hex>",
  "generated_at": "<ISO-8601>",
  "nodes": [ <SystemNode> ],
  "edges": [ <SystemEdge> ],
  "metadata": {
    "adapter_name": "understand-anything-adapter",
    "adapter_version": "0.1.0",
    "normalization_warnings": []
  }
}
```

### SystemNode

```json
{
  "id": "<string>",
  "type": "file|function|class|module|domain|flow|step|test|doc|unknown",
  "name": "<string>",
  "path": "<string or null>",
  "symbol": "<string or null>",
  "language": "<string or null>",
  "layer": "<string or null>",
  "summary": "<string or null>",
  "tags": [],
  "raw": {}
}
```

### SystemEdge

```json
{
  "id": "<string>",
  "source": "<node id>",
  "target": "<node id>",
  "type": "imports|calls|contains|extends|implements|uses|tests|documents|depends_on|unknown",
  "confidence": "high|medium|low",
  "raw": {}
}
```

---

## Normalization rules

### Node type mapping

| Understand Anything concept | Agile V type |
|---|---|
| file, source_file | `file` |
| function, method, procedure | `function` |
| class, struct, interface, enum | `class` |
| module, package, namespace | `module` |
| domain | `domain` |
| flow, workflow, pipeline | `flow` |
| step | `step` |
| test, test_file, spec | `test` |
| doc, documentation, readme | `doc` |
| anything else | `unknown` |

### Edge type mapping

| Understand Anything relationship | Agile V type |
|---|---|
| import, imports, require, requires | `imports` |
| call, calls, invokes | `calls` |
| contains, has, owns | `contains` |
| extends, inherits, subclasses | `extends` |
| implements, realizes | `implements` |
| uses, references, reads | `uses` |
| depends, depends_on, dependency | `depends_on` |
| tests, verifies, covers | `tests` |
| documents, describes | `documents` |
| anything else | `unknown` |

---

## Hashing

Every loaded graph must be SHA-256 hashed before normalization. The hash is:

- Stored in the `source_graph_hash` field of `SystemGraph`.
- Written to `.agile-v/understanding/knowledge_graph_hash.txt`.
- Included in the evidence bundle manifest.

This ensures that the evidence bundle references an immutable graph snapshot.

---

## Versioning and warnings

The adapter records normalization warnings for:

- Fields it could not map to any known type.
- Nodes missing a `path` or `id`.
- Edges referencing unknown node IDs.
- Unknown graph shape (fallback detection used).

Warnings are recorded in `SystemGraph.metadata.normalization_warnings` and surfaced to the user
as `[WARN]` lines. They are not errors; processing continues.

---

## Versioned adapter metadata

```json
{
  "adapter_name": "understand-anything-adapter",
  "adapter_version": "0.1.0",
  "source": "Lum1104/Understand-Anything",
  "source_graph_path": ".understand-anything/knowledge-graph.json",
  "source_graph_hash": "sha256:...",
  "normalization_warnings": []
}
```

The `adapter_version` must be incremented if the normalization logic changes in a way that could
alter the content of the output `SystemGraph`.

---

## Failure modes

| Situation | Behavior |
|---|---|
| Graph file not found | Return `None`; Agile V continues in `standalone` mode. |
| Graph file found but not valid JSON | Raise `GraphLoadError`; block Gate 0 with `EXIT_CODE=2`. |
| Graph found and valid but no nodes detected | Return empty `SystemGraph` with warning; continue. |
| Graph found but hash cannot be computed | Raise `GraphHashError`; block evidence export. |
| Diff overlay not found | Skip diff comparison; log info message; continue. |

---

## Do not couple to internals

The adapter must not import or call Understand Anything Python modules directly.

It must only read the JSON output files. This keeps the dependency optional and avoids version
coupling.
