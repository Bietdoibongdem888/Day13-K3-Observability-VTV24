# Requirement-to-file ownership matrix

“Implementation role” records the team allocation. “Git integration” records actual authorship: Nguyễn Quang Huy performs the final integration under his real identity; this does not imply independent commits by other members.

| Requirement | File/function/config | Implementation role | Validation | Evidence/status | Git integration |
|---|---|---|---|---|---|
| JSON logging and correlation ID | `logging_config.py`, middleware, `main.chat` | Nguyễn Quang Huy | 100/100; 136 IDs | `02_validate_logs.txt`, `03_logging_samples.md` | Huy |
| Nested PII/secret redaction | `pii.scrub_value`, `scrub_event` | Nguyễn Quang Huy | 27 tests; 0 leaks | `04_nested_redaction.txt` | Huy |
| Langfuse metadata and lifecycle | `agent.py`, `tracing.py`, lifespan | Diễm Công Thành | auth pass; 22 real traces | API evidence complete | Huy final integration |
| Meaningful spans | `mock_rag.retrieve`, `mock_llm.generate` | Diễm Công Thành | root plus retrieval/fake-llm children | API waterfall verified; UI PNG missing | Huy final integration |
| Prompt V1/V2, labels, rollback | `prompt_management.py`, `manage_prompts.py` | Diễm Công Thành | V1 → V2 → V1 verified | `07`, `08`, `10` PNGs plus API evidence | Huy final integration |
| Six-panel dashboard | `dashboard.yaml`, `app/dashboard.py`, `/dashboard` | Nguyễn Văn Đạt | 6/6; HTTP 200 | `11_dashboard_validator.txt`, `12_dashboard_6_panels.png` | Huy final integration |
| SLO, alerts, runbooks | `slo.yaml`, `alert_rules.yaml`, `docs/alerts.md` | Nguyễn Văn Đạt | config review and dashboard thresholds | configs and runbooks complete | Huy final integration |
| Practice incident | incident endpoints/scripts | Nguyễn Quốc Việt | real HTTP 500 path | `14_practice_incident.md` | Huy final integration |
| Official incident | tracked `challenge.json`, trace/log investigation | Nguyễn Quốc Việt | metrics → trace → logs verified | `15_official_incident.md` | Huy final integration |
| Report, demo, security evidence | `submission/` | Nguyễn Quốc Việt | final audit | complete except three trace UI PNGs | Huy final integration |

## Remaining evidence gaps

- `05_langfuse_trace_list.png`
- `06_trace_waterfall.png`
- `09_prompt_version_trace.png`

No local matching screenshot or connected authenticated browser was available. These files are not fabricated.

## Verified authorship limitation

Independent Git commits by Diễm Công Thành, Nguyễn Văn Đạt and Nguyễn Quốc Việt are not verified. Role allocation above must not be read as Git authorship.
