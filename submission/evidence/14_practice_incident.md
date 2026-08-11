# Practice incident — tool_fail

- Scenario enabled through `python scripts/inject_incident.py --scenario tool_fail`.
- Actual `/chat` result: HTTP 500.
- Scenario disabled through `python scripts/inject_incident.py --scenario tool_fail --disable`.
- Log timestamp: `2026-08-11T03:10:07.001961Z`.
- Correlation ID: `req-73339961`.
- Event: `request_failed`.
- Error type: `RuntimeError`.
- Concrete detail: `Vector store timeout`.
- Feature/session: `monitoring` / `practice-session`.

Root cause: the practice scenario makes the vector retrieval dependency raise before generation. Mitigation: disable the scenario/use a tested retrieval fallback. Preventive action: dependency timeout/fallback tests and error-rate alert.
