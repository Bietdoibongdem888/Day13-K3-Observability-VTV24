# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm: Nhóm 4
- Repository URL: https://github.com/Bietdoibongdem888/Day13-K3-Observability-VTV24
- Commit SHA cuối: (xem Git)
- Thành viên và vai trò:
  - Nguyễn Quốc Việt: Logging & PII, Tracing & Prompt, Dashboard, Incident

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: 100/100
- Tổng số traces: 10+ (mock server, Langfuse optional)
- Số PII leak còn lại: 0
- Link/đường dẫn dashboard: (không có dashboard web, dùng contract validator)

## 3. Logging và tracing

- Evidence correlation ID: `req-e0a99c11`, `req-9d3e5732`, `req-711e4037`, `req-72b9affa`, `req-26df9775`
- Evidence PII redaction: 0 leaks, all patterns covered (email, phone_vn, cccd, credit_card, passport, address_vn)
- Evidence trace waterfall: correlation_id is propagated from middleware → request_received → response_sent
- Giải thích một span đáng chú ý: Mỗi request có correlation_id duy nhất format `req-<8-char-hex>`, xuất hiện trong cả request_received và response_sent events. Chứng minh end-to-end trace.

## 4. Prompt versioning

- Prompt name: `day13-chat`
- Version/label baseline: `local-v1` / `local` (no Langfuse configured, fallback to local)
- Version/label candidate: `local-v1` (identical in fallback mode)
- Trace ID của mỗi version: correlation_id = `req-*` trong logs
- Bằng chứng đổi label hoặc rollback: Prompt management code supports langfuse label switching via LANGFUSE_PROMPT_LABEL env var. Fallback to local template when Langfuse unavailable.

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: HỢP LỆ: 6/6 panel
- Evidence dashboard: Dashboard contract trong `config/dashboard.yaml` với 6 panel: latency, traffic, errors, cost, tokens, quality
- SLO đã chọn và lý do:
  - latency_p95_ms <= 3000ms (99.5%) - đảm bảo trải nghiệm người dùng
  - error_rate_pct <= 2% (99.0%) - độ tin cậy hệ thống
  - daily_cost_usd <= 2.5 (100%) - kiểm soát chi phí
  - quality_score_avg >= 0.75 (95%) - chất lượng output
- Alert rules và runbook:
  - high_latency_p95: critical, latency > 3000ms for 5m → docs/alerts.md#high-latency
  - error_rate_spike: critical, error rate > 2% for 5m → docs/alerts.md#error-spike
  - cost_overrun: warning, total cost > 2.5 USD for 15m → docs/alerts.md#cost-overrun

## 6. Điều tra challenge

- Challenge ID: `day13-k3-observability-v1`
- Triệu chứng từ metrics: P95 latency 2650ms với 5 concurrent requests, vượt ngưỡng 2000ms. Response time tổng lên đến 11-14s.
- Trace ID liên quan: `req-e0a99c11` (latency 2650ms), `req-9d3e5732` (2651ms)
- Log line/correlation ID liên quan: Tất cả request có correlation_id `req-*` với feature=refund, latency_ms >= 2650
- Root cause: Incident `rag_slow` được enable, gây 2.5s sleep trong mock_rag.py `retrieve()`. Với 5 concurrent request, latency tích lũy đến 14s.
- Fix action: `POST /incidents/rag_slow/disable` để tắt incident
- Preventive measure:
  1. Thêm alert latency_p95 > 2000ms
  2. Monitor rag_slow incident state trong /health endpoint
  3. Add circuit breaker cho slow retrieval
  4. Regular audit incident state sau mỗi deployment

## 7. Đóng góp cá nhân

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| Nguyễn Quốc Việt | Logging & PII: correlation ID middleware, PII scrub | main/QuocViet branch | Structlog contextvars, PII pattern matching |
| Nguyễn Quốc Việt | Tracing & Prompt: Langfuse integration, prompt resolve | main/QuocViet branch | Prompt versioning with label-based switching |
| Nguyễn Quốc Việt | Dashboard & Alert: 6 panel contract, SLO, alert rules | main/QuocViet branch | Dashboard design from log data, SLO target setting |
| Nguyễn Quốc Việt | Incident investigation: challenge rag_slow diagnosis | main/QuocViet branch | Metrics → Traces → Logs diagnostic flow |
