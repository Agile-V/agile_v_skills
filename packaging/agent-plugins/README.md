# Agent Plugins 1.0 packaging

Portable [Agent Plugins 1.0](https://agent-plugins.org/specification) packages are **generated release artifacts**. Skills stay in their canonical directories; nothing here is a second copy.

| File | Purpose |
|---|---|
| `profiles.yaml` | Distribution profiles (source of truth) |
| `profile.schema.json` | Schema for `profiles.yaml` |
| `schemas/1.0.0/` | Vendored, unmodified upstream `plugin.schema.json` / `mcp.schema.json` (Apache-2.0) with `PROVENANCE.yaml` digests |

## Profiles

| Package | Channel | Contents |
|---|---|---|
| `agile-v-core` | stable | `agile-v-core`, `requirement-architect`, `logic-gatekeeper` |
| `agile-v-verified-build` | stable | core + `build-agent`, `test-designer`, `red-team-verifier`, `agile-v-quality-gates`. Add a `domains/build-agent-*` skill manually if needed. |
| `agile-v-regulated` | stable | verified-build + `agile-v-compliance`, `agile-v-control-matrix`, `compliance-auditor`, `validation-agent`, `safety-engineer`, `threat-modeler`, `release-manager`, `observability-planner` (released skills only; mirrors `docs/INSTALL_PROFILES.md`) |
| `agile-v-embedded` | stable | verified-build + `agile-v-behavioral`, `build-agent-embedded`, `safety-engineer`, `schematic-generator` |
| `agile-v-regulated-preview` | preview | `agile-v-regulated` + draft `agile-v-aibom`, `agile-v-human-oversight`, `agile-v-gxp-qualification` |

`agile-v-embedded` also includes `agile-v-behavioral` because `build-agent-embedded` declares it as a prerequisite; the builder rejects profiles with unsatisfied prerequisites. Including embedded skills does **not** claim PCB or firmware assurance.

## Build

```bash
python tools/build_agent_plugins.py --check                         # profiles + composition only
python tools/build_agent_plugins.py --out dist/agent-plugins --zip  # stable packages, ZIPs, SHA256SUMS
python tools/build_agent_plugins.py --out dist/agent-plugins --zip --include-preview
```

Each package contains `plugin.json`, `skills/`, `LICENSE`, `CHANGELOG.md` and `AGILE_V_PACKAGE_MANIFEST.json` (per-skill source path, source commit, version, status and SHA-256 digests). No `mcp.json` is shipped until a stable runtime MCP contract exists. Client-specific data lives only under `extensions["org.agile-v"]`.

The builder rejects: unknown skills, missing prerequisites, draft skills or draft-only capability dependencies in stable profiles, missing required capabilities, conflicts, duplicate exclusive capabilities, superseded capabilities, symlinks and paths escaping the plugin root. See [`docs/agile-v-runtime/18_CAPABILITY_COMPOSITION.md`](../../docs/agile-v-runtime/18_CAPABILITY_COMPOSITION.md).

Package digests and attestations prove **integrity and provenance of the package bytes**, not that the skills are correct or enforced by any runtime.
