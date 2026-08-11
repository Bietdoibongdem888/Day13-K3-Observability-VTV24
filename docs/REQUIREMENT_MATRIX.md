# Requirement-to-file ownership matrix

“Implementation role” records the team allocation. “Git evidence” records only observed authorship and never infers a roster identity from a similar name.

| Requirement | File/function/config | Implementation role | Validation | Status | Evidence / Git evidence |
|---|---|---|---|---|---|
| JSON logging and correlation ID | `logging_config.py`, middleware, `main.chat` | Nguyễn Quang Huy | 100/100; 157 IDs | PASS | `02_validate_logs.txt`, `03_logging_samples.md`; Huy commits verified |
| Recursive PII/secret redaction | `pii.scrub_value`, `scrub_event` | Nguyễn Quang Huy | 30 tests; zero leaks | PASS | `04_nested_redaction.txt`; Huy commits verified |
| Langfuse metadata and lifecycle | `agent.py`, `tracing.py`, lifespan | Diễm Công Thành | Auth pass; 22 real traces | PASS | API evidence; integrated by Huy |
| Meaningful spans | `mock_rag.retrieve`, `mock_llm.generate` | Diễm Công Thành | Root plus retrieval/fake-llm children | PARTIAL EVIDENCE | API waterfall verified; UI PNG missing |
| Prompt V1/V2, labels, rollback | `prompt_management.py`, `manage_prompts.py` | Diễm Công Thành | V1 → V2 → V1 verified | PASS | `07`, `08`, `10` UI PNGs plus API evidence |
| Six-panel dashboard | `dashboard.yaml`, `app/dashboard.py`, `/dashboard` | Nguyễn Văn Đạt | 6/6; HTTP 200 | PASS | `11_dashboard_validator.txt`, `12_dashboard_6_panels.png` |
| Metrics edge behavior | `app/metrics.py` | Nguyễn Văn Đạt | Exact percentile/error-rate tests | PASS | Nearest-rank percentiles; total/error-rate snapshot |
| SLO, alerts, runbooks | `slo.yaml`, `alert_rules.yaml`, `docs/alerts.md` | Nguyễn Văn Đạt | Config and threshold review | PASS | Explicit metric/operator/threshold/duration and runbooks |
| Practice incident | Incident endpoints/scripts | Nguyễn Quốc Việt | Real HTTP 500 path | PASS | `14_practice_incident.md` |
| Official incident | `challenge.json`, trace/log investigation | Nguyễn Quốc Việt | Metrics → trace → logs | PASS | `15_official_incident.md` |
| Report, demo, security | `submission/` | Nguyễn Quốc Việt | Final audit | PARTIAL EVIDENCE | Missing three trace UI PNGs; owner must confirm old key revocation |

## Remaining evidence gaps

- `05_langfuse_trace_list.png`
- `06_trace_waterfall.png`
- `09_prompt_version_trace.png`

No matching local image or connected authenticated browser session was available. These files are not fabricated.

## Verified Git facts

- Submission branch: `NGUYENQUANGHUY-2A202601873`.
- Verified Huy commits precede the final integration commit.
- GitHub PR #1 is merged under user `GiaoSuD`; its commit author is `Phùng Văn Đạt`.
- A separate main commit uses identity `thanhfdc`.
- These external identities are not mapped to Nguyễn Văn Đạt or Diễm Công Thành without independent evidence.
- Divergent main commits were reviewed but not merged because they are superseded and include a historical secret exposure in report history.
