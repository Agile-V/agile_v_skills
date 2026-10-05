# OpenTelemetry Contract

**Contract version: 1.0.** Registry keys `opentelemetry_contract` and `agile_v_telemetry_event`. Schema: [`AGILE_V_TELEMETRY_EVENT`](../../schemas/AGILE_V_TELEMETRY_EVENT.schema.json).

> **Normative.** Defines how Agile-V lifecycle, evidence and gate events map onto [OpenTelemetry](https://opentelemetry.io/docs/specs/semconv/). Agile-V does not define a proprietary tracing format or collector. **Telemetry is observability, never evidence admission:** a span saying `admitted` is not a Gate Receipt and cannot authorize a transition.

## 1. Reuse first

Use existing OpenTelemetry semantic conventions wherever they apply (`gen_ai.*` for model/agent/tool operations, `service.*`, `deployment.*`, `code.*`, `error.*`, `vcs.*`, `session.*`). Define `agilev.*` attributes only for assurance concepts that have no OpenTelemetry equivalent. Other namespaces are rejected by the schema to prevent accidental leakage.

## 2. Span/event names

`agilev.task.create`, `agilev.requirements.freeze`, `agilev.risk.classify`, `agilev.evidence.collect`, `agilev.evidence.admit`, `agilev.evidence.reject`, `agilev.verify`, `agilev.gate.evaluate`, `agilev.gate.authorize`, `agilev.approval.consume`, `agilev.revalidation.evaluate`, `agilev.delegation.evaluate`, `agilev.transition.execute`.

Agent and model calls inside a task SHOULD be emitted with the GenAI conventions (e.g. `invoke_agent`, `execute_tool`, `chat`) as children of the Agile-V span.

## 3. Attributes

| Attribute | Meaning |
|---|---|
| `agilev.task.id` | Required on every event |
| `agilev.risk.level` | `L0`-`L4` |
| `agilev.subject.type` / `.ref` / `.digest` | Evaluated subject state |
| `agilev.policy.digest` | Frozen policy digest |
| `agilev.claim.id`, `agilev.evidence.id`, `agilev.evidence.source_profile` | Claim/evidence identity; source profile from the [Evidence Adapter Registry](15_EVIDENCE_ADAPTER_REGISTRY.md) |
| `agilev.gate.id`, `agilev.gate.receipt_id` | Gate and the authoritative Gate Receipt |
| `agilev.decision.status`, `agilev.reason_codes` | Decision and the evaluator's reason codes (array of `UPPER_SNAKE` strings) |
| `agilev.independence.class` | `I0`-`I4` |
| `agilev.approval.ref`, `agilev.exception.ref` | Referenced records (never their content) |
| `agilev.revalidation.status` | Change-Aware Revalidation result |
| `agilev.agent_run.id` | Correlates to `AI_RUN_MANIFEST.identity.run_id` |
| `agilev.delegation.id`, `agilev.context.profile` | Delegation v2 record; Context Source Profile |

Gate events require gate id, decision, reason codes, subject digest and policy digest; evidence admit/reject events require evidence id, source profile, decision and reason codes; a reject requires at least one reason code.

## 4. Privacy defaults

The `default` privacy profile MUST NOT emit prompt text, completion text, system instructions, raw tool arguments/results (`gen_ai.input.messages`, `gen_ai.output.messages`, `gen_ai.system_instructions`, `gen_ai.tool.call.arguments`, `gen_ai.tool.call.result`, `gen_ai.tool.definitions`), PII, or proprietary source content. **No profile** may emit hidden chain-of-thought/reasoning, secrets, credentials, API or private keys, or authorization headers; the schema rejects attribute names containing such terms. Prefer IDs, digests, versions, classifications, reason codes and timestamps. The `extended` profile permits GenAI content attributes only under an explicit local data-handling decision.

## 5. Export

Events map 1:1 to OTLP spans. `tools/telemetry_to_otlp.py` converts examples to OTLP/JSON for any OTLP/HTTP collector (`/v1/traces`). Examples: [`examples/telemetry/`](../../examples/telemetry/).

## 6. Non-claims

Emitting this telemetry does not show that a runtime enforces Agile-V contracts. Conformance is established only by the [runtime conformance](../../conformance/RUNTIME_STATUS.md) process.
