# Logging evidence

Actual sanitized records observed in `data/logs.jsonl` (generated log itself is gitignored):

```json
{"event":"request_received","correlation_id":"req-ab2beca4","payload":{"message_preview":"What is your refund policy? My email is [REDACTED_EMAIL]"}}
{"event":"request_received","correlation_id":"req-dae5cccf","payload":{"message_preview":"Here is my phone [REDACTED_PHONE_VN], what should be logged?"}}
{"event":"request_received","correlation_id":"req-1b8831f5","payload":{"message_preview":"What is the policy for PII and credit card [REDACTED_CREDIT_CARD]?"}}
```

The complete API records also contained `user_id_hash`, `session_id`, `feature`, `model`, and `env`. Validator scan found no raw email, Vietnamese phone, CCCD, or credit-card detector hits.
