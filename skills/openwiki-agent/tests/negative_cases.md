# Negative Cases: openwiki-agent

## When should this skill NOT block progress?

| Case | Condition | Expected behavior |
|---|---|---|
| NC-001 | `openwiki/` does not exist | Do NOT halt. Note absence, recommend `agilev wiki init`, continue task using normal repo exploration. |
| NC-002 | `agilev wiki validate` fails (structural error) | Do NOT halt the whole task. Mark the knowledge layer as untrusted, continue using direct source inspection instead of citing wiki pages as fact. |
| NC-003 | `agilev` CLI is not installed/available in the environment | Do NOT halt. Skip the CLI-based checks, note that the knowledge layer could not be verified, proceed. |
| NC-004 | Pages are stale relative to source but validation otherwise passes | Do NOT discard the whole wiki. Reduce confidence only in the specific stale page(s); other pages remain usable. |

## What this skill must NOT do

- Must NOT generate or edit `openwiki/` page content itself (that is the
  real `openwiki` CLI's job, run by a human or scheduled CI, not this
  skill).
- Must NOT run the real, LLM-backed `openwiki --init`/`--update`/`-p`
  commands automatically without explicit user request (they require an
  API key and produce real, potentially costly, generation calls).
- Must NOT treat a stale or failed-validation wiki as fatal to the task.
- Must NOT fabricate a `knowledge_snapshot` if `agilev` is unavailable —
  simply omit that evidence field and say so, rather than inventing
  plausible-looking values.
- Must NOT read every page in `openwiki/` regardless of task relevance;
  target only pages relevant to the current change.
