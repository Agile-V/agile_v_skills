# Security and Privacy Considerations

## Overview

Knowledge graphs contain file paths, function names, class names, summaries, and potentially
code snippets. Before exporting a knowledge graph or a normalized graph in an evidence bundle,
review this document.

---

## What knowledge graphs may contain

| Category | Risk level | Notes |
|---|---|---|
| File paths | Low | Usually safe; may reveal internal directory structure. |
| Function and class names | Low–Medium | May reveal business logic or proprietary naming. |
| Plain-English summaries | Medium | May contain proprietary algorithm descriptions. |
| Code snippets or signatures | Medium–High | May contain proprietary implementation details. |
| Comments embedded in graph | Medium–High | May contain internal design notes or TODOs. |
| Hardcoded secrets in graph | Critical | Scan before any export. |

---

## Export modes

### Default (safe)

The default `agilev evidence export` output includes:

```text
knowledge_graph_hash.txt     ← hash only, not the graph
normalized_graph.json        ← summarized node/edge list, no raw code
system_overview.md           ← human-readable summary
architecture_map.md          ← layer and component names
```

### Full export (internal use only)

```bash
agilev evidence export --include-understanding --include-raw-graph
```

Includes the full `knowledge_graph.json`. Use only for internal evidence bundles.

### External audit safe

```bash
agilev evidence export --external-audit-safe
```

Includes:
- `knowledge_graph_hash.txt`
- `system_overview.md`
- `architecture_map.md`
- `understanding_gate_decision.md`
- `impact_map.md`
- `graph_traceability_matrix.md`
- `validation_summary.md`

Excludes all raw source files, the full graph, and file paths beyond what is in the traceability
matrix.

### Redacted export

```bash
agilev evidence export --redact-source    # strip code snippets
agilev evidence export --redact-paths     # replace file paths with hashes
```

---

## Sensitive data scan

Before exporting any evidence bundle, `agilev evidence export` runs a scan for:

```text
- Hardcoded secrets (API keys, tokens, passwords, private keys)
- PII patterns (email addresses, phone numbers, SSNs)
- Internal URLs or hostnames
- Customer or patient data references
- Credentials or auth headers in graph summaries
```

If any are found, the export is blocked with `EXIT_CODE=1` and a report is generated at:

```text
.agile-v/evidence/sensitive_data_scan.md
```

Override with `--skip-sensitive-scan` only if you have reviewed the report and accepted the risk.

---

## Regulated environments

In regulated environments (ISO 13485, FDA, GxP, HIPAA, SOC 2, etc.):

1. Do not include the full `knowledge_graph.json` in any shared or externally accessible evidence bundle.
2. Use only the hash (`knowledge_graph_hash.txt`) to prove graph identity.
3. Use `--external-audit-safe` for any auditor-facing bundles.
4. Store the full graph in a controlled internal evidence repository, not in the shared bundle.
5. Document which version of the graph was used in `understanding_gate_decision.md`.

---

## Graph storage recommendations

| Environment | Recommendation |
|---|---|
| Open-source project | Commit `.understand-anything/` to the repository if no secrets are present. |
| Internal commercial project | Gitignore `.understand-anything/knowledge-graph.json`; generate on demand. |
| Regulated or proprietary | Store graph in a controlled artifact store; reference by hash in evidence. |

Add to `.gitignore` if needed:

```gitignore
.understand-anything/knowledge-graph.json
.understand-anything/diff-overlay.json
```

---

## License note

Understand Anything is MIT-licensed. Verify the license before including its output files in
any product distribution or commercial evidence bundle.

Do not vendor Understand Anything source code into Agile V. Use only the generated JSON outputs.
