# Official incident — day13-k3-observability-v1

The tracked challenge file was released in Git commit `cd84f4f` and was not modified during this run.

## Symptom and impact

- Scenario: `rag_slow`.
- Affected feature: `refund`.
- Baseline application latencies: 150, 150, 151, 151, 151 ms; p95 = **151 ms**.
- Incident application latencies: 2652, 2652, 2652, 2652, 2653 ms; p95 = **2653 ms**.
- Official threshold: 2000 ms. All five incident requests exceeded the threshold while still returning HTTP 200.
- Incident window: `2026-08-11T04:17:54.247304Z`–`2026-08-11T04:17:57.831146Z`.

## Metrics → trace → logs

- Representative correlation ID: `req-7506187a`.
- Langfuse trace ID: `16229089282a1f8b8fd1232620e96cb7`.
- Root trace duration: 2.654 s.
- Retrieval span ID: `f6fd112443631073`; duration: **2.503 s**.
- Fake LLM span ID: `6f2413b85e653c1d`; duration: 0.151 s.
- JSON log: `2026-08-11T04:17:57.356795Z`, `event=response_sent`, `feature=refund`, `latency_ms=2653`, `correlation_id=req-7506187a`.
- Control logs: `incident_enabled` at `04:17:54.247304Z` and `incident_disabled` at `04:17:57.831146Z`, both with `payload.name=rag_slow`.

All five incident correlation IDs were found as real Langfuse traces.

## Root cause and response

- Root cause: the official `rag_slow` scenario adds approximately 2.5 seconds inside retrieval. The trace proves the latency is concentrated in the retrieval child span rather than the fake LLM span.
- Immediate mitigation: disable the scenario or roll back the slow retrieval change, then monitor p95 recovery.
- Permanent fix: enforce retrieval timeout/circuit breaker, caching, and a tested fallback.
- Preventive measure: alert on p95, retain retrieval-span timing, and run concurrent retrieval regression tests before release.

Status: **VERIFIED end-to-end**.
