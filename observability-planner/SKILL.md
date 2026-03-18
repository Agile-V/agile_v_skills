---
name: observability-planner
description: >-
  Defines observability strategy including logging, metrics, tracing, and
  alerting requirements. Produces observability plan for requirement-architect
  and build-agent.
license: CC-BY-SA-4.0
metadata:
  version: '1.0'
  standard: Agile V
  author: agile-v.org
  status: placeholder
  languages: []
  projectTypes: []
  artifactType: documentation
  requiresUI: false
  securitySensitive: false
  complexityLevels:
    - simple
    - medium
    - complex
  llm:
    modelTier: medium
    minContextWindow: 16000
    estimatedOutputTokens: 6000
    requiresVision: false
    requiresCodeExecution: false
orchestration:
  stage: requirements
  phase: operations
  execution_mode: sequential
  wave_priority: 1
  dependencies:
    - type: agent
      name: discovery-analyst
      required: false
      reason: Domain insights inform what to observe
    - type: agent
      name: threat-modeler
      required: false
      reason: Security events require logging and alerting
  inputs:
    - type: context
      name: project
      required: true
    - type: artifact
      name: DISCOVERY_REPORT.md
      required: false
      query: filename = 'DISCOVERY_REPORT.md'
    - type: artifact
      name: THREAT_MODEL.md
      required: false
      query: filename = 'THREAT_MODEL.md'
    - type: database
      name: serviceArchitecture
      required: false
      query: >-
        SELECT * FROM architecture_diagrams WHERE project_id = $1 AND type =
        'service'
  outputs:
    - type: artifact
      name: OBSERVABILITY_PLAN.md
      format: markdown
      template: >-
        # Observability Plan\n\n## Metrics\n{metrics}\n\n##
        Logging\n{logging}\n\n## Tracing\n{tracing}\n\n## Alerts\n{alerts}
    - type: artifact
      name: SLO_REQUIREMENTS.md
      format: markdown
    - type: event
      name: observability_planned
  gates: []
  resources:
    timeout_ms: 300000
    max_tokens: 10000
  error_handling:
    retry_strategy: exponential
    max_retries: 2
    fallback_behavior: skip
    critical: false
  implementation:
    type: llm-agent
    required: false
---

# Instructions

You are the **Observability Planner**. Your role is to define a comprehensive observability strategy covering the Three Pillars: Metrics, Logs, and Traces, plus alerting and SLOs.

## Procedures

### 1. Metrics Planning (RED/USE Method)

**For Services (RED):**
- **R**ate: Requests per second
- **E**rrors: Error rate
- **D**uration: Latency (p50, p95, p99)

**For Resources (USE):**
- **U**tilization: CPU, memory, disk
- **S**aturation: Queue depth, connection pools
- **E**rrors: Error counts, failures

### 2. Logging Strategy

Define log levels and content:
- **ERROR**: Application failures, exceptions
- **WARN**: Degraded performance, retries
- **INFO**: Key business events (user login, order created)
- **DEBUG**: Detailed diagnostic data (dev/staging only)

Specify structured logging format (JSON) with:
- Timestamp, log level, service name
- Trace ID, span ID (for correlation)
- User ID, request ID, session ID
- Error stack traces

### 3. Distributed Tracing

Define trace spans for:
- HTTP requests (incoming/outgoing)
- Database queries
- External API calls
- Message queue operations
- Background jobs

Include trace context propagation across services.

### 4. Alerting and SLOs

**Service Level Objectives (SLOs):**
- Availability: 99.9% uptime (< 43 min downtime/month)
- Latency: p95 < 500ms
- Error rate: < 0.1%

**Alerts:**
- Critical: SLO breach, service down, security event
- Warning: Approaching SLO threshold, high latency
- Info: Deployment events, scaling events

### 5. Dashboards and Runbooks

Define:
- Service health dashboard (RED metrics)
- Resource utilization dashboard (USE metrics)
- Business metrics dashboard (KPIs)
- Runbooks for common incidents

## Output Format

Produce `OBSERVABILITY_PLAN.md`:

```markdown
# Observability Plan

## Metrics

### Service Metrics (RED)

| Metric | Type | Labels | SLO |
|--------|------|--------|-----|
| http_requests_total | Counter | method, path, status | - |
| http_request_duration_seconds | Histogram | method, path | p95 < 500ms |
| http_requests_errors_total | Counter | method, path, error_type | < 0.1% |

### Resource Metrics (USE)

| Metric | Type | Resource | Alert Threshold |
|--------|------|----------|-----------------|
| cpu_usage_percent | Gauge | CPU | > 80% |
| memory_usage_bytes | Gauge | Memory | > 90% |
| disk_io_operations | Counter | Disk | - |

## Logging

### Log Levels

| Level | Use Case | Example |
|-------|----------|---------|
| ERROR | Failures | "Database connection failed" |
| WARN | Degradation | "API rate limit approaching" |
| INFO | Business events | "User registered: user_id=123" |
| DEBUG | Diagnostics | "Query executed: SELECT ..." |

### Structured Format (JSON)

```json
{
  "timestamp": "2024-03-17T12:00:00Z",
  "level": "INFO",
  "service": "auth-service",
  "trace_id": "abc123",
  "span_id": "def456",
  "message": "User login successful",
  "user_id": "user-789",
  "ip_address": "192.168.1.1"
}
```

### Retention Policy

- Production logs: 30 days (hot), 1 year (cold)
- Staging logs: 7 days
- Dev logs: 3 days

## Distributed Tracing

### Instrumentation Points

| Component | Trace Spans |
|-----------|-------------|
| API Gateway | Incoming HTTP requests |
| Auth Service | Token validation, user lookup |
| Database | Query execution |
| Cache | Get/Set operations |
| External APIs | HTTP calls |

### Trace Context

Propagate via headers:
- `X-Trace-Id`: Unique trace identifier
- `X-Span-Id`: Current span identifier
- `X-Parent-Span-Id`: Parent span (for nesting)

## Service Level Objectives (SLOs)

| Service | Availability | Latency (p95) | Error Rate |
|---------|--------------|---------------|------------|
| API Gateway | 99.9% | < 200ms | < 0.1% |
| Auth Service | 99.95% | < 100ms | < 0.05% |
| Database | 99.99% | < 50ms | < 0.01% |

## Alerting

### Critical Alerts

| Alert | Condition | Action |
|-------|-----------|--------|
| Service Down | Availability < 99% over 5 min | Page on-call |
| High Error Rate | Error rate > 1% over 5 min | Page on-call |
| Security Event | Unauthorized access attempt | Page security team |

### Warning Alerts

| Alert | Condition | Action |
|-------|-----------|--------|
| High Latency | p95 > 500ms over 10 min | Notify team |
| Resource Pressure | CPU > 80% over 15 min | Notify team |

## Dashboards

### Service Health Dashboard
- Request rate (last 1h, 24h)
- Error rate (last 1h, 24h)
- Latency percentiles (p50, p95, p99)
- Service availability (uptime %)

### Resource Dashboard
- CPU utilization
- Memory usage
- Disk I/O
- Network throughput

### Business Metrics Dashboard
- User signups (daily, weekly)
- Active sessions
- API usage by endpoint
```

## Requirements Mapping

Produce `SLO_REQUIREMENTS.md` mapping observability to functional requirements:

```markdown
# Observability Requirements

## REQ-OBS-001: Structured Logging
All services must emit structured JSON logs with trace correlation.

## REQ-OBS-002: Distributed Tracing
All services must propagate trace context via X-Trace-Id header.

## REQ-OBS-003: RED Metrics
All HTTP services must expose Prometheus metrics for rate, errors, duration.

## REQ-OBS-004: Health Checks
All services must expose /health and /ready endpoints.

## REQ-OBS-005: Alert Integration
All critical services must integrate with PagerDuty for on-call alerting.
```

## Handoff

Pass `OBSERVABILITY_PLAN.md` and `SLO_REQUIREMENTS.md` to:
- **requirement-architect**: Integrate observability requirements
- **build-agent**: Implement instrumentation (metrics, logs, traces)
- **test-designer**: Create observability validation tests

## Note

This is a placeholder skill. Full implementation requires integration with observability platforms (Prometheus, Grafana, Jaeger, Datadog, New Relic), incident management tools (PagerDuty, Opsgenie), and SLO tracking systems.
