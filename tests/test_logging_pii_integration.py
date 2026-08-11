from __future__ import annotations

import concurrent.futures
import json
from pathlib import Path

from fastapi.testclient import TestClient

from app import logging_config
from app.incidents import STATE
from app.main import app
from app.pii import hash_user_id, scrub_text, scrub_value


def _records(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_extended_pii_and_nested_secrets_are_redacted_idempotently() -> None:
    raw = {
        "user": {"email": "abc+test@example.co.uk", "phone": "+84912345678"},
        "payments": [{"card": "4111 1111 1111 1111"}],
        "headers": {"Authorization": "Bearer synthetic-token-value"},
        "credentials": {
            "api-key": "synthetic-api-key",
            "id_token": "synthetic-id-token",
            "database_password": "synthetic-password",
        },
    }

    safe = scrub_value(raw)
    rendered = json.dumps(safe)

    for sensitive_value in (
        "abc+test@example.co.uk",
        "+84912345678",
        "4111 1111 1111 1111",
        "synthetic-token-value",
        "synthetic-api-key",
        "synthetic-id-token",
        "synthetic-password",
    ):
        assert sensitive_value not in rendered
    assert safe["user"]["email"] == "[REDACTED_EMAIL]"
    assert safe["headers"]["Authorization"] == "[REDACTED_SECRET]"
    assert scrub_value(safe) == safe
    assert scrub_text("[REDACTED_EMAIL]") == "[REDACTED_EMAIL]"


def test_user_hash_is_deterministic_and_not_reversible_encoding() -> None:
    first = hash_user_id("student-privacy-id")
    second = hash_user_id("student-privacy-id")

    assert first == second
    assert first != "student-privacy-id"
    assert "student" not in first


def test_request_preserves_valid_id_and_logs_required_metadata(
    monkeypatch, tmp_path: Path
) -> None:
    log_path = tmp_path / "metadata.jsonl"
    monkeypatch.setattr(logging_config, "LOG_PATH", log_path)

    with TestClient(app) as client:
        response = client.post(
            "/chat",
            headers={"x-request-id": "req-deadbeef"},
            json={
                "user_id": "raw-user-must-not-be-logged",
                "session_id": "metadata-session",
                "feature": "qa",
                "message": (
                    "Contact abc+test@example.co.uk, +84912345678, "
                    "or card 4111 1111 1111 1111"
                ),
            },
        )

    assert response.status_code == 200
    assert response.json()["correlation_id"] == "req-deadbeef"
    assert response.headers["x-request-id"] == "req-deadbeef"
    assert float(response.headers["x-response-time-ms"]) >= 0
    raw_log = log_path.read_text(encoding="utf-8")
    assert "raw-user-must-not-be-logged" not in raw_log
    assert "abc+test@example.co.uk" not in raw_log
    assert "+84912345678" not in raw_log
    assert "4111 1111 1111 1111" not in raw_log

    api_records = [record for record in _records(log_path) if record.get("service") == "api"]
    assert {record["event"] for record in api_records} == {"request_received", "response_sent"}
    for record in api_records:
        assert record["correlation_id"] == "req-deadbeef"
        assert record["user_id_hash"] == hash_user_id("raw-user-must-not-be-logged")
        assert record["session_id"] == "metadata-session"
        assert record["feature"] == "qa"
        assert record["model"]
        assert record["env"]


def test_concurrent_requests_do_not_leak_correlation_context(
    monkeypatch, tmp_path: Path
) -> None:
    log_path = tmp_path / "concurrent.jsonl"
    monkeypatch.setattr(logging_config, "LOG_PATH", log_path)

    with TestClient(app) as client:
        def send(index: int) -> tuple[str, str]:
            response = client.post(
                "/chat",
                json={
                    "user_id": f"concurrent-user-{index}",
                    "session_id": f"concurrent-session-{index}",
                    "feature": "qa",
                    "message": "Explain observability",
                },
            )
            assert response.status_code == 200
            return response.json()["correlation_id"], response.headers["x-request-id"]

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            identifiers = list(executor.map(send, range(12)))

    body_ids = [body_id for body_id, header_id in identifiers if body_id == header_id]
    assert len(body_ids) == 12
    assert len(set(body_ids)) == 12

    api_records = [record for record in _records(log_path) if record.get("service") == "api"]
    for correlation_id in body_ids:
        request_records = [
            record for record in api_records if record["correlation_id"] == correlation_id
        ]
        assert {record["event"] for record in request_records} == {
            "request_received",
            "response_sent",
        }
        assert len({record["session_id"] for record in request_records}) == 1


def test_error_log_is_sanitized_and_investigation_ready(
    monkeypatch, tmp_path: Path
) -> None:
    log_path = tmp_path / "error.jsonl"
    monkeypatch.setattr(logging_config, "LOG_PATH", log_path)
    STATE["tool_fail"] = True
    try:
        with TestClient(app) as client:
            response = client.post(
                "/chat",
                json={
                    "user_id": "error-user",
                    "session_id": "error-session",
                    "feature": "monitoring",
                    "message": "password=synthetic-secret email=error@example.test",
                },
            )
    finally:
        STATE["tool_fail"] = False

    assert response.status_code == 500
    raw_log = log_path.read_text(encoding="utf-8")
    assert "synthetic-secret" not in raw_log
    assert "error@example.test" not in raw_log
    failure = next(record for record in _records(log_path) if record["event"] == "request_failed")
    assert failure["level"] == "error"
    assert failure["status_code"] == 500
    assert failure["error_type"] == "RuntimeError"
    assert isinstance(failure["latency_ms"], int)
    assert failure["correlation_id"].startswith("req-")
    assert failure["session_id"] == "error-session"
