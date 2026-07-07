# openwiki-agent

Governs when and how an Agile-V agent consults and trusts the
[OpenWiki](https://github.com/langchain-ai/openwiki)-generated repository
knowledge layer (`openwiki/`), via the `agilev wiki` CLI implemented in the
`agentic_agile_v` repository (`src/agilev/wiki/`).

This skill is informational/supporting, not a Human Gate: a missing or
stale knowledge layer is a signal to reduce confidence in specific claims,
never a reason to block a task on its own.

## Key behaviors

| Step | Command | Purpose |
|---|---|---|
| 1 | `agilev wiki status --json` | Check whether `openwiki/` exists at all |
| 2 | `agilev wiki validate --json` | Decide whether to trust it (structural pass/fail + staleness) |
| 3 | — | Read only the pages relevant to the current task |
| 4 | — | Record what was checked/trusted in the evidence summary |
| 5 | `agilev wiki snapshot --task <id>` | Persist a `knowledge_snapshot` into the task's evidence file |

## See also

- `SKILL.md` — full skill specification
- `metadata.json` — machine-readable skill metadata
- `../../integrations/openwiki/README.md` — CLI/evidence mapping and examples
- `agentic_agile_v` repo: `src/agilev/wiki/`, `docs/integrations/openwiki.md`
