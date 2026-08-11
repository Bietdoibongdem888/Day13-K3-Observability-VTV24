from collections import Counter

from app import metrics
from app.metrics import percentile


def test_percentile_basic() -> None:
    assert percentile([], 95) == 0.0
    assert percentile([100, 200, 300, 400], 0) == 100.0
    assert percentile([100, 200, 300, 400], 50) == 200.0
    assert percentile([100, 200, 300, 400], 95) == 400.0
    assert percentile([100, 200, 300, 400], 100) == 400.0


def test_snapshot_exposes_total_requests_and_error_rate(monkeypatch) -> None:
    monkeypatch.setattr(metrics, "TRAFFIC", 3)
    monkeypatch.setattr(metrics, "ERRORS", Counter({"TimeoutError": 1}))
    monkeypatch.setattr(metrics, "REQUEST_LATENCIES", [100, 200, 300])
    monkeypatch.setattr(metrics, "REQUEST_COSTS", [0.1, 0.2, 0.3])
    monkeypatch.setattr(metrics, "REQUEST_TOKENS_IN", [10, 20, 30])
    monkeypatch.setattr(metrics, "REQUEST_TOKENS_OUT", [20, 30, 40])
    monkeypatch.setattr(metrics, "QUALITY_SCORES", [0.8, 0.9, 1.0])

    result = metrics.snapshot()

    assert result["requests_total"] == 4
    assert result["traffic"] == 3
    assert result["error_rate_pct"] == 25.0
    assert result["error_breakdown"] == {"TimeoutError": 1}
