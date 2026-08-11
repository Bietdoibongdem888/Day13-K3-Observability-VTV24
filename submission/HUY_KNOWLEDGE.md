# Nguyễn Quang Huy — Logging & PII review notes

## Structured logging

Structured logging ghi event thành các field có schema, thay vì ghép một câu text. JSONL cho phép mỗi dòng được `json.loads`, dễ filter theo correlation ID, latency, error type hoặc feature và tránh parser dựa vào câu chữ mong manh.

## Correlation ID

Correlation ID là định danh của một request xuyên qua middleware, endpoint, agent, trace và logs. Nó giúp nối nhiều event của cùng request. Với async concurrency, global variable có thể bị request khác ghi đè; context-local storage và cleanup trong `finally` ngăn A dùng nhầm ID của B.

## PII, redaction, masking và hashing

- PII là dữ liệu có thể nhận diện hoặc liên hệ một người; email, phone, card và raw user ID là ví dụ.
- Redaction thay toàn bộ giá trị bằng marker an toàn.
- Masking giữ lại một phần có chủ đích, ví dụ last four; project này không cần nên card được redact toàn bộ.
- Hashing tạo pseudonym deterministic để cùng user vẫn phân tích được mà không ghi raw ID.
- Hash một chiều khác encryption có thể giải mã bằng key. Hash cũng khác redaction: hash giữ khả năng correlation, redaction chủ động bỏ giá trị.

## Logs, metrics và traces

Metrics trả lời “có bất thường gì và khi nào”; trace chỉ ra request/span nào chậm hoặc lỗi; log cung cấp event và field cụ thể để giải thích. Correlation ID nối trace metadata với đúng log. Dashboard aggregate từ logs nhưng không thay thế trace waterfall.

## Security

Authorization header, bearer token, API key và password có thể cấp quyền trực tiếp nên không được persistence. `.env` thường chứa credentials theo môi trường; commit file này làm secret tồn tại trong Git history ngay cả khi xóa ở commit sau.

## Incident handoff mẫu

```text
Nguyễn Quang Huy — Logging Evidence
Correlation ID: req-79932387
Timestamp: 2026-08-11T03:24:00.992075Z
Relevant event: request_failed
Relevant fields: status_code=500, error_type=RuntimeError, latency_ms=2,
                 feature=monitoring, session_id=huy-error-evidence
Log evidence: payload.detail="Vector store timeout"; message preview đã redact.
Interpretation: retrieval dependency failed before model generation.
Does this support the suspected root cause? YES for the tool_fail practice incident.
```
