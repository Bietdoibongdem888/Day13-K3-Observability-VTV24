# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm: VTV24
- Repository URL: local (Day13-K3-Observability)
- Commit SHA cuối: cd84f4f
- Thành viên và vai trò: 
  Diêm Công Thành – 2A202601689  | Tracing & Prompt Version | traces, metadata, prompt v1/v2, label/rollback | trace gắn đúng prompt version |
  huy
## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: **100/100**
  - Basic JSON schema: PASSED
  - Correlation ID propagation: PASSED (44 unique IDs)
  - Log enrichment: PASSED
  - PII scrubbing: PASSED (0 leaks)

- Tổng số logs: 85+ records
- **Tổng số traces Langfuse: 47 traces**
- Số PII leak còn lại: 0
- Link/đường dẫn dashboard: `config/dashboard.yaml` (6/6 panel validated)

## 3. Logging và tracing

### Evidence correlation ID
- File: `submission/evidence/evidence_summary.json`
- Sample correlation IDs:
  - `req-660c7a10` - normal request
  - `req-681a1be6` - Langfuse traced request

### Evidence PII redaction
- Email `student@vinuni.edu.vn` → `[REDACTED_EMAIL]`
- Vietnamese phone `0987654321` → `[REDACTED_PHONE_VN]`
- Credit card `4111 1111 1111 1111` → `[REDACTED_CREDIT_CARD]`
- Xem chi tiết trong `submission/evidence/logs_sample.jsonl`

### Evidence trace Langfuse
- **Project**: 
- **Total traces**: 47
- **URL**: https://cloud.langfuse.com/project/
- Evidence file: `submission/evidence/langfuse_traces.json`

### Giải thích một span đáng chú ý
- Trace ID: `session_direct_test` (baseline v2)
- Latency: 1053ms
- Trace metadata:
  - `prompt_name`: 'day13-chat'
  - `prompt_label`: 'baseline'
  - `prompt_version`: 2
  - `prompt_source`: 'langfuse'

## 4. Prompt versioning

- **Prompt name**: `day13-chat`
- **Langfuse Project**: cmso3s4r303yzad0imhk4v3zq
- **Prompts URL**: https://cloud.langfuse.com/project/

### Version 1 (production)
- **Labels**: `production`, `latest`
- **Traces**: 37
- **Content**:
  ```
  Feature={{feature}}
  Docs={{docs}}
  Question={{message}}
  ```

### Version 2 (baseline/candidate)
- **Labels**: `candidate`, `baseline`, `latest`
- **Traces**: 10
- **Content**:
  ```
  Answer concisely.
  Feature={{feature}}
  Docs={{docs}}
  Question={{message}}
  ```

### Trace IDs theo version
| Version | Label | Số traces | Sample session |
|---------|-------|-----------|----------------|
| 1 | production | 37 | session_prod_0, session_prod_1, ... |
| 2 | baseline | 10 | session_v2_direct_0, session_v2_direct_1, ... |

### Bằng chứng đổi label
- Production label gắn với version 1
- Baseline/Candidate labels gắn với version 2
- Quản lý tại: https://cloud.langfuse.com/project/
## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: **HỢP LỆ: 6/6 panel**
- Evidence dashboard: `config/dashboard.yaml`
- SLO đã chọn và lý do:
  - `latency_p95_ms`: 3000ms - ngưỡng chuẩn cho AI API
  - `error_rate_pct`: 2% - ngưỡng SLA phổ biến
  - `daily_cost_usd`: 2.5 - giới hạn chi phí
  - `quality_score_avg`: 0.75 - quality floor

### Alert rules (`config/alert_rules.yaml`)
1. `high_latency_p95`: warning - P95 > 3000ms trong 5 phút
2. `high_error_rate`: critical - Error rate > 2% trong 2 phút
3. `high_daily_cost`: warning - Cost > $2.5 trong 1 giờ

## 6. Điều tra challenge

- Challenge ID: Chưa được release (Lab Coach chưa cung cấp `config/challenge.json`)
- Triệu chứng từ metrics: N/A
- Trace ID liên quan: N/A
- Log line/correlation ID liên quan: N/A
- Root cause: N/A
- Fix action: N/A
- Preventive measure: N/A

**Practice incident đã test**:
- Scenario: `rag_slow`
- Baseline latency: ~150ms
- With incident latency: ~2650ms (tăng 17x)
- Evidence: `submission/evidence/evidence_summary.json`

## 7. Đóng góp cá nhân

| Thành viên | Phần việc | Commit | Điều đã học |
|---|---|---|---|
| GiaoSuD | Hoàn thiện TODO (middleware, logging, PII) | - | Correlation ID propagation, structlog contextvars |
| GiaoSuD | Alert rules và SLO | - | SLO/SLI design |
| GiaoSuD | Langfuse tracing và prompt versioning | - | Langfuse SDK, prompt labels và versions |
| GiaoSuD | Testing và evidence | - | Validators và test coverage |

## 8. Files đã sửa đổi

1. `app/middleware.py` - Hoàn thiện CorrelationIdMiddleware
2. `app/logging_config.py` - Bật PII scrubbing
3. `app/main.py` - Thêm log enrichment
4. `app/pii.py` - Thêm patterns cho IP, passport, Vietnamese address
5. `config/alert_rules.yaml` - Cấu hình 3 alert rules
6. `.env` - Thêm Langfuse credentials

## 9. Evidence Files

| File | Mô tả |
|------|--------|
| `submission/evidence/logs_sample.jsonl` | 63 log records mẫu |
| `submission/evidence/evidence_summary.json` | Summary về incident |
| `submission/evidence/langfuse_traces.json` | Chi tiết 47 Langfuse traces |


