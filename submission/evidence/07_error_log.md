# Sanitized error logging evidence

Actual practice request with `tool_fail` enabled:

```json
{
  "ts": "2026-08-11T03:24:00.992075Z",
  "level": "error",
  "event": "request_failed",
  "correlation_id": "req-79932387",
  "user_id_hash": "b60cf0cca905",
  "session_id": "huy-error-evidence",
  "feature": "monitoring",
  "model": "claude-sonnet-4-5",
  "env": "dev",
  "status_code": 500,
  "error_type": "RuntimeError",
  "latency_ms": 2,
  "payload": {
    "detail": "Vector store timeout",
    "message_preview": "[REDACTED_EMAIL] [REDACTED_PASSWORD]"
  }
}
```

The synthetic raw email and password used in the request were absent from persisted logs. The incident was disabled after the request.
