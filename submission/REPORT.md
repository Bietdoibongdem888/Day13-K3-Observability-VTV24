# Day 13 Observability Report

## 1. Submission identity

- Repository: `https://github.com/Bietdoibongdem888/Day13-K3-Observability-VTV24`
- Submission branch: `NGUYENQUANGHUY-2A202601873`
- Nguyễn Quang Huy — `2A202601873` — Logging & PII / final integration
- Diễm Công Thành — `2A202601689` — Tracing & Prompt Versioning
- Nguyễn Văn Đạt — `2A202602012` — Dashboard, SLO & Alert
- Nguyễn Quốc Việt — `2A202601737` — Incident, Report & Demo

Role allocation describes project responsibility, not Git authorship. Verified Git identities are reported separately; no author, PR, or co-author record is fabricated.

## 2. Verified technical result

- Pytest: **30 passed** using an isolated Windows temp directory (the default system pytest temp root has an external ACL problem).
- Log validator: **100/100** on 324 JSON records, 157 correlation IDs, zero missing required/enrichment fields, and zero detected PII leaks.
- Dashboard validator: **6/6**.
- Runtime: `/health`, `/chat`, `/metrics`, and `/dashboard` respond successfully; concurrent load returned 10/10 HTTP 200 responses.
- Dashboard: six panels, 60-minute window, 30-second refresh.

## 3. Logging and tracing

- Correlation IDs use `req-<8 hex>` and propagate through response headers, JSON logs, and traces.
- Request metadata includes hashed user ID, session, feature, model, and environment. Recursive PII/secret redaction runs before JSON rendering.
- Langfuse Cloud authentication: **PASS** during the network-enabled verification; no 401/403 export failure.
- Langfuse API count at verification: **22 real traces**.
- Waterfall trace `07ffc195d58f71d1cc4054a668923545`: root `run`, child `retrieval`, child `fake-llm`.
- Verified trace metadata includes correlation ID, session ID, feature, model, environment, prompt name, label, and version.
- Evidence: [Langfuse API verification](evidence/05_langfuse_api_evidence.md).

## 4. Prompt versioning

- Prompt: `day13-chat`; live label: `production`.
- V1 trace: `914192aa065813285f7fca37ded1c197`.
- Promoted V2 trace: `07ffc195d58f71d1cc4054a668923545`.
- Post-rollback V1 trace: `aa480f2d7814da903894ba4daf53cceb`.
- The **V1 → promote V2 → V2 trace → rollback V1 → V1 trace** chain was verified through Langfuse API data.
- Authenticated prompt UI evidence: [V1](evidence/07_prompt_v1.png), [V2](evidence/08_prompt_v2.png), [rollback](evidence/10_prompt_rollback.png).
- Remaining UI evidence gaps: `05_langfuse_trace_list.png`, `06_trace_waterfall.png`, and `09_prompt_version_trace.png`. API evidence is not represented as a substitute screenshot.

## 5. Dashboard, SLO, and alerts

- Panels: Latency p50/p95/p99, Traffic, Errors, Cost, Tokens, Quality.
- SLO window: 28 days; latency p95 ≤ 3000 ms, error rate ≤ 2%, daily cost ≤ 2.5 USD, mean quality ≥ 0.75.
- Alerts: `HighP95Latency`, `HighErrorRate`, and `QualityDegradation`, each with an explicit metric, operator, threshold, duration, severity, owner, and runbook.
- Runtime evidence: [12_dashboard_6_panels.png](evidence/12_dashboard_6_panels.png), 53,135 bytes, 1920×1080, visually verified.

## 6. Official incident

- Challenge `day13-k3-observability-v1`, scenario `rag_slow`, feature `refund`.
- Baseline p95 **151 ms**; incident p95 **2653 ms**; threshold **2000 ms**.
- Trace `16229089282a1f8b8fd1232620e96cb7`, total duration **2.654 s**.
- Retrieval span `f6fd112443631073`: **2.503 s**; fake-LLM span: **0.151 s**.
- Correlation ID `req-7506187a` maps to `response_sent`, `feature=refund`, `latency_ms=2653` in JSON logs.
- Root cause: the official `rag_slow` challenge adds approximately 2.5 seconds inside retrieval.
- Mitigation: disable/rollback the faulty retrieval behavior and monitor p95 recovery.
- Prevention: timeout, circuit breaker, caching/fallback, p95 alerting, and regression/load tests.
- Evidence: [official incident](evidence/15_official_incident.md).

## 7. Git and security audit

- `origin/main` is six commits ahead on its side and the submission branch is seven commits ahead on its side at the audited point.
- Main contains PR #1 plus later report changes, including a historical credential exposure that was later redacted. Those weaker/divergent commits were deliberately not merged into this stronger submission branch.
- Current branch and staged content contain no real Langfuse key, Bearer credential, `.env`, `.venv`, cache, generated log, or temporary runtime artifact.
- Local Langfuse credentials differ from the historically exposed pair. Repository evidence cannot prove revocation; the project owner must still confirm that the historical key was revoked/rotated.
- PR #1 is verified as merged from GitHub user `GiaoSuD`/Git author `Phùng Văn Đạt`; another main commit uses Git identity `thanhfdc`. These identities are not asserted to match roster members without independent proof.

## 8. Submission status

Implementation, automated tests, validators, runtime checks, Langfuse API verification, prompt workflow, dashboard screenshot, and incident chain are complete. The submission remains honestly blocked from an evidence-complete claim by the three authenticated Langfuse trace UI screenshots listed in section 4 and by owner confirmation that the historically exposed credential has been revoked.
