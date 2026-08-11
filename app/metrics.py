from __future__ import annotations

from collections import Counter
from math import ceil
from statistics import mean
from threading import Lock

REQUEST_LATENCIES: list[int] = []
REQUEST_COSTS: list[float] = []
REQUEST_TOKENS_IN: list[int] = []
REQUEST_TOKENS_OUT: list[int] = []
ERRORS: Counter[str] = Counter()
TRAFFIC: int = 0
QUALITY_SCORES: list[float] = []
_METRICS_LOCK = Lock()


def record_request(latency_ms: int, cost_usd: float, tokens_in: int, tokens_out: int, quality_score: float) -> None:
    global TRAFFIC
    with _METRICS_LOCK:
        TRAFFIC += 1
        REQUEST_LATENCIES.append(latency_ms)
        REQUEST_COSTS.append(cost_usd)
        REQUEST_TOKENS_IN.append(tokens_in)
        REQUEST_TOKENS_OUT.append(tokens_out)
        QUALITY_SCORES.append(quality_score)



def record_error(error_type: str) -> None:
    with _METRICS_LOCK:
        ERRORS[error_type] += 1



def percentile(values: list[int], p: int) -> float:
    if not values:
        return 0.0
    items = sorted(values)
    rank = ceil((max(0, min(100, p)) / 100) * len(items))
    idx = max(0, min(len(items) - 1, rank - 1))
    return float(items[idx])



def snapshot() -> dict:
    with _METRICS_LOCK:
        latencies = list(REQUEST_LATENCIES)
        costs = list(REQUEST_COSTS)
        quality_scores = list(QUALITY_SCORES)
        error_count = sum(ERRORS.values())
        requests_total = TRAFFIC + error_count
        return {
            "traffic": TRAFFIC,
            "requests_total": requests_total,
            "latency_p50": percentile(latencies, 50),
            "latency_p95": percentile(latencies, 95),
            "latency_p99": percentile(latencies, 99),
            "avg_cost_usd": round(mean(costs), 4) if costs else 0.0,
            "total_cost_usd": round(sum(costs), 4),
            "tokens_in_total": sum(REQUEST_TOKENS_IN),
            "tokens_out_total": sum(REQUEST_TOKENS_OUT),
            "error_breakdown": dict(ERRORS),
            "error_rate_pct": round(error_count / requests_total * 100, 4)
            if requests_total
            else 0.0,
            "quality_avg": round(mean(quality_scores), 4) if quality_scores else 0.0,
        }
