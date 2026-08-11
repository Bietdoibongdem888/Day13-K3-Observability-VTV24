from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path
from statistics import mean
from typing import Any

from .metrics import percentile


def load_recent_records(path: Path, *, minutes: int = 60) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
            timestamp = datetime.fromisoformat(str(record["ts"]).replace("Z", "+00:00"))
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            continue
        if timestamp >= cutoff:
            records.append(record)
    return records


def dashboard_values(records: list[dict[str, Any]], *, minutes: int = 60) -> dict[str, str]:
    received = [record for record in records if record.get("event") == "request_received"]
    responses = [record for record in records if record.get("event") == "response_sent"]
    failures = [record for record in records if record.get("event") == "request_failed"]
    latencies = [int(record["latency_ms"]) for record in responses if isinstance(record.get("latency_ms"), int)]
    costs = [float(record["cost_usd"]) for record in responses if isinstance(record.get("cost_usd"), (int, float))]
    quality = [float(record["quality_score"]) for record in responses if isinstance(record.get("quality_score"), (int, float))]
    tokens_in = sum(int(record.get("tokens_in", 0)) for record in responses)
    tokens_out = sum(int(record.get("tokens_out", 0)) for record in responses)
    denominator = len(received) or 1
    error_types: dict[str, int] = {}
    for record in failures:
        error_type = str(record.get("error_type", "Unknown"))
        error_types[error_type] = error_types.get(error_type, 0) + 1

    return {
        "latency": f"p50 {percentile(latencies, 50):.0f} · p95 {percentile(latencies, 95):.0f} · p99 {percentile(latencies, 99):.0f}",
        "traffic": f"{len(received)} total · {len(received) / minutes:.2f} per minute",
        "errors": f"{len(failures) / denominator * 100:.2f}% · {error_types or 'no errors'}",
        "cost": f"${sum(costs):.6f} total",
        "tokens": f"{tokens_in} input · {tokens_out} output",
        "quality": f"{mean(quality):.2f}" if quality else "0.00",
    }


def render_dashboard(records: list[dict[str, Any]]) -> str:
    values = dashboard_values(records)
    panels = (
        ("Latency percentiles", values["latency"], "ms", "SLO: p95 ≤ 3000 ms"),
        ("Request traffic", values["traffic"], "requests/minute", "Expected ≥ 1 request/minute"),
        ("Error rate and breakdown", values["errors"], "%", "SLO: error rate ≤ 2%"),
        ("Cost over time", values["cost"], "USD", "Budget: total ≤ $2.50"),
        ("Input and output tokens", values["tokens"], "tokens", "Budget: total ≤ 50,000"),
        ("Quality proxy", values["quality"], "score 0–1", "SLO: mean ≥ 0.75"),
    )
    cards = "".join(
        f"<section><h2>{escape(title)}</h2><p class='value'>{escape(value)}</p>"
        f"<p>{escape(unit)}</p><p class='threshold'>{escape(threshold)}</p></section>"
        for title, value, unit, threshold in panels
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="30">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Day 13 AI Observability</title>
<style>body{{font:16px system-ui;margin:0;background:#0b1220;color:#e5e7eb}}main{{max-width:1100px;margin:auto;padding:32px}}.meta{{color:#93c5fd}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}}section{{background:#172033;border:1px solid #334155;border-radius:12px;padding:20px}}h2{{font-size:1rem}}.value{{font-size:1.45rem;font-weight:700}}.threshold{{color:#fbbf24}}</style>
</head><body><main><h1>Day 13 AI Observability</h1><p class="meta">Time range: last 60 minutes · Refresh: 30 seconds · Records: {len(records)}</p><div class="grid">{cards}</div></main></body></html>"""
