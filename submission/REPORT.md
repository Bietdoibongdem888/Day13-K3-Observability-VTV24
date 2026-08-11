# Báo cáo Day 13 Observability

## 1. Nhóm và chế độ tích hợp

- Repository: `https://github.com/Bietdoibongdem888/Day13-K3-Observability`.
- Final submission commit: xem SHA được nộp hoặc chạy `git rev-parse HEAD`; không ghi SHA vào report để tránh vòng lặp commit.
- Nguyễn Quang Huy — `2A202601873` — Logging & PII / final integration.
- Diễm Công Thành — `2A202601689` — Tracing & Prompt Versioning.
- Nguyễn Văn Đạt — `2A202602012` — Dashboard, SLO & Alert.
- Nguyễn Quốc Việt — `2A202601737` — Incident, Report & Demo.

Role allocation mô tả trách nhiệm kỹ thuật của nhóm. Verified Git authorship được báo cáo riêng; final integration được commit bằng identity thật của Nguyễn Quang Huy và không giả danh thành viên khác.

## 2. Kết quả kỹ thuật

- Stable Windows runner: **27 passed**.
- Log validator: **100/100** trên 276 records; 136 correlation IDs; 0 missing required fields; 0 missing enrichment; 0 PII leak.
- Dashboard validator: **6/6**.
- Runtime API: `/health` HTTP 200, `/chat` HTTP 200, background load test 10/10 HTTP 200; không còn `WinError 10061`.
- Dashboard: HTTP 200, sáu panel, time range 60 phút, refresh 30 giây.

## 3. Logging và tracing

- Correlation ID dạng `req-<8 hex>` được bind bằng contextvars và dùng xuyên suốt response, JSON logs và traces.
- Request log có hashed user ID, session, feature, model và environment; nested PII/secret redaction chạy trước JSON renderer.
- Langfuse Cloud authentication: **PASS**; không có 401/403/export failure trong lượt xác minh có network.
- Langfuse trace API: **22 real traces**.
- Waterfall trace `07ffc195d58f71d1cc4054a668923545`: root `run`, child `retrieval`, child `fake-llm`.
- Metadata đã xác minh: correlation ID, session ID, feature, model, environment, prompt name, label và version.
- API evidence: [Langfuse API evidence](evidence/05_langfuse_api_evidence.md).

## 4. Prompt versioning

- Prompt name: `day13-chat`; production label: `production`.
- V1 trace: `914192aa065813285f7fca37ded1c197`.
- V2 trace sau promotion: `07ffc195d58f71d1cc4054a668923545`.
- Post-rollback V1 trace: `aa480f2d7814da903894ba4daf53cceb`.
- Chuỗi **V1 → promote V2 → V2 trace → rollback V1 → V1 trace** đã xác minh qua Langfuse API.
- UI evidence: [V1](evidence/07_prompt_v1.png), [V2](evidence/08_prompt_v2.png), [rollback](evidence/10_prompt_rollback.png). Các file được sao chép nguyên byte từ ảnh authenticated do người dùng cung cấp.
- Ba UI screenshots vẫn thiếu: trace list `05_langfuse_trace_list.png`, waterfall `06_trace_waterfall.png`, và V2 trace/prompt `09_prompt_version_trace.png`. API evidence không được trình bày như ảnh UI thay thế.

## 5. Dashboard, SLO và alerts

- Panels: Latency p50/p95/p99, Traffic, Errors, Cost, Tokens, Quality.
- SLO window: 28 ngày; latency p95 ≤ 3000 ms, error rate ≤ 2%, daily cost ≤ 2.5 USD, mean quality ≥ 0.75.
- Alerts: `HighP95Latency`, `HighErrorRate`, `QualityDegradation`, kèm duration, severity, owner và runbook.
- Runtime screenshot: [12_dashboard_6_panels.png](evidence/12_dashboard_6_panels.png), 53,135 bytes, đã kiểm tra trực quan.

## 6. Official incident

- Challenge: `day13-k3-observability-v1`; scenario `rag_slow`; affected feature `refund`.
- Baseline p95: **151 ms**; incident p95: **2653 ms**; threshold: **2000 ms**.
- Incident trace ID: `16229089282a1f8b8fd1232620e96cb7`; total duration **2.654 s**.
- Slow retrieval span: `f6fd112443631073`, duration **2.503 s**.
- Fake LLM span duration: **0.151 s**.
- Correlation ID: `req-7506187a`.
- Matching JSON log: `response_sent`, `feature=refund`, `latency_ms=2653`.
- Root cause: official `rag_slow` introduces approximately 2.5 seconds of latency inside retrieval.
- Immediate mitigation: disable/rollback the problematic retrieval behavior and monitor p95 recovery.
- Preventive controls: retrieval timeout, circuit breaker, cache, fallback, p95 alert, and load/regression tests.
- Evidence: [official incident](evidence/15_official_incident.md).

## 7. Role allocation và verified Git authorship

| Thành viên | Implementation ownership | Verified Git authorship |
|---|---|---|
| Nguyễn Quang Huy | Logging & PII / final integration | Verified: `2bd7abe`, `e6dd46c`, `95069a1`, `9ba4b9e`, `e11b869`; final integration commit is created separately |
| Diễm Công Thành | Tracing & Prompt Versioning | Independent member commit not verified |
| Nguyễn Văn Đạt | Dashboard, SLO & Alert | Independent member commit not verified |
| Nguyễn Quốc Việt | Incident, Report & Demo | Independent member commit not verified |

Không tạo fake author, fake PR hoặc `Co-authored-by` trailer. Single-contributor final integration không được dùng để tuyên bố cả bốn Git contributions đã được xác minh.

## 8. Submission status

Technical implementation, automated validation, Langfuse API verification, prompt workflow, dashboard screenshot và official incident chain đều hoàn tất. Submission evidence vẫn thiếu đúng ba Langfuse trace UI screenshots nêu ở mục 4. Final commit/SHA được xác minh bên ngoài nội dung report sau khi commit.
