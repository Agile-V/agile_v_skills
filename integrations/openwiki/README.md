# OpenWiki Integration

This directory documents the integration between Agile-V and
[OpenWiki](https://github.com/langchain-ai/openwiki), an external CLI that
generates and maintains agent-facing repository documentation
(`openwiki --init`, `openwiki --update`, `openwiki -p`).

The **skill** for this integration is `../../skills/openwiki-agent/`. This
directory holds the deeper reference material the skill points to.

## Division of responsibility

| Layer | Lives in | Responsibility |
|---|---|---|
| `openwiki` (external CLI) | Installed via `npm install -g openwiki` | Generates/refreshes `openwiki/` content (LLM-backed) |
| `agilev.wiki` (Python package) | `agentic_agile_v` repo, `src/agilev/wiki/` | Tracks, validates, and proves that content: manifest, source map, freshness, `agilev wiki` CLI, evidence bundle integration |
| `openwiki-agent` (this skill) | `agile_v_skills` repo, `skills/openwiki-agent/` | Tells an AI agent *when* and *how much* to trust `openwiki/` content during a session |

## CLI command reference

All commands below are provided by `agentic_agile_v`'s `agilev` CLI, not by
this skills repository. See that repo's `docs/integrations/openwiki.md`
for full detail.

| Command | Effect | Safe to run automatically? |
|---|---|---|
| `agilev wiki init` | Scaffolds required `openwiki/` page skeletons + records manifest. No LLM call. | Yes |
| `agilev wiki init --run-openwiki` | Also invokes the real `openwiki --init` (LLM-backed, needs API key). | No — ask first |
| `agilev wiki update` | Recomputes manifest/source-map/freshness from current `openwiki/`. No LLM call. | Yes |
| `agilev wiki update --run-openwiki` | Also invokes the real `openwiki --update`. | No — ask first |
| `agilev wiki validate [--json]` | Structural + freshness check. Exit 1 only on structural failure. | Yes |
| `agilev wiki status [--json]` | Freshness/validation summary. | Yes |
| `agilev wiki snapshot --task <id>` | Writes `knowledge_snapshot` into the task's evidence file. | Yes |

## Evidence mapping

`agilev wiki snapshot` (or the automatic collection in
`EvidenceAdapter.collect_evidence()`) writes a `knowledge_snapshot` object
into a task's `evidence.json` / `evidence_bundle.json` under the
`knowledge_snapshot` key, matching the optional property added to
`schemas/evidence_bundle.schema.json` in `agentic_agile_v`. See
`examples/knowledge_snapshot_example.md` for a full example.

## Relationship to Understand Anything

OpenWiki and [Understand Anything](https://github.com/Lum1104/Understand-Anything)
are complementary, not redundant:

- **OpenWiki** produces curated, human-readable narrative documentation
  (`openwiki/*.md`) — architecture overviews, onboarding, domain guides.
- **Understand Anything** produces a structural knowledge graph
  (`.understand-anything/knowledge-graph.json`) — components, dependencies,
  impact analysis.

A repository may have either, both, or neither. When both are present, run
`openwiki-agent` for narrative context and `system-understanding-agent` for
structural/impact context; neither supersedes the other.

## GitHub Wiki mirroring: not part of this integration

This integration intentionally does not mirror `openwiki/` into the
separate GitHub Wiki feature (the `.wiki.git` repository GitHub provides
per repository). See `agentic_agile_v`'s
`docs/integrations/openwiki.md` ("GitHub Wiki Mirroring: Explicitly Out of
Scope") for the rationale: repository-local docs under version control are
reviewable through normal pull requests and existing CI quality gates.

## See also

- `examples/knowledge_snapshot_example.md`
- `../../skills/openwiki-agent/SKILL.md`
- `agentic_agile_v` repo: `src/agilev/wiki/`, `docs/integrations/openwiki.md`
