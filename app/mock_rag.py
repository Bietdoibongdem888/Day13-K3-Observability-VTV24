from __future__ import annotations

import time

from .incidents import STATE
from .tracing import observe_when_enabled

CORPUS = {
    "refund": ["Refunds are available within 7 days with proof of purchase."],
    "monitoring": ["Metrics detect incidents, traces localize them, logs explain root cause."],
    "policy": ["Do not expose PII or other sensitive data in logs. Use sanitized summaries only."],
}


@observe_when_enabled(name="retrieval", as_type="span", capture_input=False, capture_output=False)
def retrieve(message: str) -> list[str]:
    if STATE["tool_fail"]:
        raise RuntimeError("Vector store timeout")
    if STATE["rag_slow"]:
        time.sleep(2.5)
    lowered = message.lower()
    for key, docs in CORPUS.items():
        if key in lowered:
            return docs
    if any(keyword in lowered for keyword in ("metric", "trace", "observability")):
        return CORPUS["monitoring"]
    if any(keyword in lowered for keyword in ("pii", "sensitive", "app logs", "logging")):
        return CORPUS["policy"]
    return ["No domain document matched. Use general fallback answer."]
