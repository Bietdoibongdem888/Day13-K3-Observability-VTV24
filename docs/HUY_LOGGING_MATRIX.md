# Nguyễn Quang Huy — Logging & PII requirement matrix

MSSV: `2A202601873`. Matrix này giới hạn ở Role 1 và các integration point bắt buộc.

| Requirement | Actual file | Function/class | Status | Implementation | Test | Validator | Evidence |
|---|---|---|---|---|---|---|---|
| JSONL hợp lệ | `app/logging_config.py` | `JsonlFileProcessor` | Pass | JSONRenderer + write lock, một object mỗi dòng | logging integration | `validate_logs.py` | `02_validate_logs.txt` |
| Correlation ID | `app/middleware.py` | `CorrelationIdMiddleware.dispatch` | Pass | preserve `x-request-id` hợp lệ hoặc sinh `req-<8 hex>` | metadata + concurrency tests | validator | `05_concurrency.txt` |
| Context lifecycle | `app/middleware.py` | `dispatch` | Pass | clear/bind/finally clear contextvars | 12-request focused test | validator | `05_concurrency.txt` |
| Request metadata | `app/main.py` | `chat` | Pass | hash/session/feature/model/env bind trước log đầu tiên | metadata test | validator | `03_logging_samples.md` |
| User pseudonym | `app/pii.py` | `hash_user_id` | Pass | deterministic SHA-256 prefix; không log raw ID | hashing + integration test | validator | `03_logging_samples.md` |
| Email/phone/card | `app/pii.py` | `scrub_text` | Pass | regex cho email `+`, VN phone, CCCD/card | focused PII tests | validator | `06_manual_pii_secret_test.txt` |
| Nested secret/PII | `app/pii.py` | `scrub_value` | Pass | recurse dict/list/tuple; redact sensitive key/token suffix | nested/idempotence test | validator | `04_nested_redaction.txt` |
| Sanitization before persistence | `app/logging_config.py` | `scrub_event` processor | Pass | scrub trước renderer và file processor | integration test | validator | `02_validate_logs.txt` |
| Safe error evidence | `app/main.py` | exception branch in `chat` | Pass | error level, type, status, latency, metadata, sanitized detail | error-path test | validator | `07_error_log.md` |
| Token/cost/quality retention | `app/main.py` | success log | Pass | numeric agent results forwarded unchanged | chat observability test | validator/dashboard | response records |
| Trace integration | `app/agent.py` | trace metadata | Pass locally | correlation ID lấy từ same contextvars | agent trace test | pytest | external screenshot pending |
| Incident log handoff | `submission/evidence` | actual error/slow records | Pass | timestamp + correlation + event + relevant fields | runtime practice | validator | `07_error_log.md`, `15_official_incident.md` |
| Git contribution | branch/history | Git | Partial | branch riêng đã tạo | `git status/log` | n/a | commit chưa tạo do author chưa xác minh |

Request flow đã xác minh:

```text
Client → FastAPI middleware → correlation context → /chat metadata context
→ threadpool agent → metrics/trace → structured logger → recursive scrub
→ JSON renderer → locked logs.jsonl write → dashboard/incident lookup
```
