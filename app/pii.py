from __future__ import annotations

import hashlib
import re
from typing import Any

PII_PATTERNS: dict[str, str] = {
    "email": r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}",
    "phone_vn": r"(?<!\d)(?:\+84|0)(?:[ .-]?\d){9}(?!\d)",
    "cccd": r"\b\d{12}\b",
    "credit_card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
    "passport": r"(?i)\b(?:passport\s*(?:no\.?|number|#)?\s*[:=-]?\s*)[A-Z]\d{7,8}\b",
    "api_key": r"(?i)\b(?:api[_ -]?key|access[_ -]?token)\s*[:=]\s*[^\s,;]+",
    "bearer_token": r"(?i)\bBearer\s+[A-Za-z0-9._~+\-/]+=*",
    "password": r"(?i)\b(?:password|passwd|pwd|secret)\s*[:=]\s*[^\s,;]+",
}

SENSITIVE_KEYS = frozenset(
    {
        "authorization", "cookie", "password", "passwd", "secret", "api_key",
        "apikey", "access_token", "refresh_token", "token",
    }
)


def _is_sensitive_key(key: str) -> bool:
    normalized = key.lower().replace("-", "_").replace(" ", "_")
    return (
        normalized in SENSITIVE_KEYS
        or normalized.endswith("_token")
        or "password" in normalized
        or "secret" in normalized
        or "api_key" in normalized
    )


def scrub_text(text: str) -> str:
    safe = text
    for name, pattern in PII_PATTERNS.items():
        safe = re.sub(pattern, f"[REDACTED_{name.upper()}]", safe)
    return safe


def scrub_value(value: Any, *, key: str | None = None) -> Any:
    """Recursively remove PII and secret values before structured serialization."""
    if key and _is_sensitive_key(key):
        return "[REDACTED_SECRET]"
    if isinstance(value, str):
        return scrub_text(value)
    if isinstance(value, dict):
        return {item_key: scrub_value(item, key=str(item_key)) for item_key, item in value.items()}
    if isinstance(value, list):
        return [scrub_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(scrub_value(item) for item in value)
    return value


def summarize_text(text: str, max_len: int = 80) -> str:
    safe = scrub_text(text).strip().replace("\n", " ")
    return safe[:max_len] + ("..." if len(safe) > max_len else "")


def hash_user_id(user_id: str) -> str:
    return hashlib.sha256(user_id.encode("utf-8")).hexdigest()[:12]
