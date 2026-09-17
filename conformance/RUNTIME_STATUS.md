# Runtime conformance status — issue #42

## Observed baseline

| Repository | Observation on 2026-09-14 |
|---|---|
| `Agile-V/agentic_agile_v` | Public `main` tree contains no path matching compatibility, conformance, assurance, or admission. |
| Local runtime checkout | `54eaa5451fcbfe9fa1c59355584deddbf7cef342`, branch `chore/remove-openwiki`, with pre-existing CLI/schema changes and extensive wiki deletions. |
| Skills | Reference aggregate tests exist; they are not a second runtime implementation. |

## Local cross-repository result

A runtime-owned preview implementation now exists on local branch
`fix/issue-42-runtime-conformance`, based on the commit above, in an isolated
worktree. `python -m agilev.assurance --manifest` exports its versioned packaged
manifest. Its evaluator does not import the skills evaluator.

On 2026-09-14, `tests/test_runtime_conformance.py` passed **24 checks**:
23 identical serialized positive/adversarial requests plus the runtime manifest.
The comparison checks status and normalized reason-code sets. Covered cases:
source/property resolver absence, state/policy mismatch, adapter drift,
property overclaim/understatement, approval digest/scope/authorship/expiry/replay,
critical risk, independence, cross-task substitution, complete/incomplete waiver,
and complete/partial/unknown/missing/stale reuse coverage.

The same 24 checks passed against a non-editable wheel installed in a fresh
Python 3.12 environment, with the runtime invoked outside its source checkout
and without a source `PYTHONPATH`. Seven runtime protocol tests cover manifest
export, malformed/duplicate/non-finite JSON, and explicit trusted-context CLI
arguments. The skills suite with runtime conformance enabled reported
**669 passed, 1 skipped**; the skip is live-agent prompt-injection behavior.

```bash
AGILEV_RUNTIME_CHECKOUT=/path/to/agentic_agile_v python -m pytest tests/test_runtime_conformance.py -q
AGILEV_RUNTIME_PYTHON=/path/to/installed/venv/bin/python python -m pytest tests/test_runtime_conformance.py -q
```

**Companion PR published; release pending.** Runtime commit
`b0b5cdc55e67bb56ec97512c2018e1126b338803` is available through [runtime PR #12](https://github.com/Agile-V/agentic_agile_v/pull/12)
on branch `fix/issue-42-runtime-conformance`. The packaged manifest is in
`src/agilev/assurance/compatibility.json` on that branch. No released runtime
version is claimed. The compatibility declaration stays `unverified`,
`minimum_version: null` pending review and supported-route integration.
Local subset equivalence does not establish legacy CLI/hook
integration, real authentication, protected CI, or atomic transition authority.

## Handoff to the runtime implementation

1. Publish a manifest binding runtime commit/version, implemented contract
   versions from `contracts/versions.yaml`, supported capabilities, and exact
   fixture-corpus/reference revisions.
2. Provide an installed command accepting JSON test requests on stdin and
   returning `{status, findings}` as JSON on stdout. Run with test-only trusted
   providers and no production credentials. It must invoke the runtime's own
   admission route, not relabel a direct call to the skills test helper.
3. Execute the positive control and all issue #42 aggregate negative scenarios
   (including state/policy/profile/authority/scope/risk/reuse cases).
4. Compare normalized status/reason codes, retain process exit status and
   interpreter/runtime identity, and publish the result with the manifest.
5. Only then update the verified compatibility declaration.

Required decision fixtures and synthetic provider boundaries are in
`tests/admission_support.py`, `tests/test_issue42_trust_closure.py`, and
`tests/test_runtime_conformance.py`. Routine CI skips the opt-in runtime suite
if neither runtime location is configured; skipped runs are not conformance.
