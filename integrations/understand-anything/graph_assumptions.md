# Graph Assumptions

## What Agile V assumes about the Understand Anything knowledge graph

This document records the assumptions Agile V makes when consuming a knowledge graph. Any
deviation from these assumptions may produce warnings or reduced-quality outputs, but will
not cause a hard failure unless the graph is unreadable.

---

## Format assumptions

| Assumption | Fallback if violated |
|---|---|
| The graph is a JSON file. | `GraphLoadError` — processing blocked. |
| The graph contains at least one discoverable array of nodes. | Empty `SystemGraph` with warning. |
| Node objects have at least one of: `id`, `name`, `path`. | Synthetic ID generated; warning recorded. |
| Edge objects reference source and target node IDs that exist in the node array. | Edge recorded with `confidence: low`; warning recorded. |
| The graph file is UTF-8 encoded. | Attempt Latin-1 fallback; warning recorded. |

---

## Content assumptions

| Assumption | Impact if wrong |
|---|---|
| Node types (file, function, class, etc.) are present or inferable. | Default type `unknown` assigned. |
| File paths are relative to the repository root. | Impact analysis may miss cross-file links. |
| Edge relationship labels are consistent across the graph. | Unknown labels mapped to `unknown` type. |
| Summaries (plain-English descriptions) are in English. | No translation; summaries used as-is. |
| The graph reflects the current state of the repository at scan time. | Stale graph risk; recorded in `system_understanding_confidence.md`. |

---

## Size assumptions

The adapter does not impose a hard size limit. However:

- Graphs larger than 50 MB are flagged with a `[LARGE GRAPH]` warning.
- Only relevant subgraphs (nodes connected to the change request) are passed to the Build Agent.
- The full normalized graph is written to disk; only excerpts go into context windows.

---

## Freshness assumption

Agile V does not verify that the graph was generated from the current HEAD of the repository.

The user is responsible for regenerating the graph before running `agilev understand` if the
codebase has changed significantly since the last graph generation.

The hash stored in `knowledge_graph_hash.txt` can be used to detect whether the graph has
changed between runs.

---

## What Agile V does NOT assume

- That Understand Anything is installed in the current environment.
- That the graph covers 100% of the codebase.
- That the graph is accurate for recently added or deleted files.
- That the graph schema matches the format documented here.

The adapter is deliberately tolerant and preserves unknown fields in the `raw` field of each
`SystemNode` and `SystemEdge`.

---

## Known Understand Anything graph shapes (as of v0.1 adapter)

The adapter has been tested against the following likely shapes. If Understand Anything releases
a new format, update the adapter and increment `adapter_version`.

### Shape A: Top-level nodes and edges arrays

```json
{
  "nodes": [ { "id": "...", "type": "...", "name": "...", "path": "..." } ],
  "edges": [ { "id": "...", "source": "...", "target": "...", "type": "..." } ]
}
```

### Shape B: Nested under "graph" key

```json
{
  "graph": {
    "nodes": [ ... ],
    "edges": [ ... ]
  }
}
```

### Shape C: Domain-specific keys

```json
{
  "files": [ ... ],
  "functions": [ ... ],
  "dependencies": [ ... ]
}
```

All three shapes are handled by the tolerant detection strategy in `detector.py` and `loader.py`.
