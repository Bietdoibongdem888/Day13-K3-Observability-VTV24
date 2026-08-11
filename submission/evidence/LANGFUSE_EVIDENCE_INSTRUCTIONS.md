# Langfuse and official-incident evidence checklist

This checklist is not evidence. Execute it only with the team's real Langfuse project and never capture `.env` or credentials.

## Configure and bootstrap prompts

1. Create a local ignored `.env` from `.env.example`; configure the three `LANGFUSE_*` connection values.
2. Run `python scripts/manage_prompts.py bootstrap`.
3. Start `uvicorn app.main:app --env-file .env`.
4. Run `python scripts/load_test.py --concurrency 5` and wait for queued spans to export.
5. Stop uvicorn gracefully with Ctrl+C so `flush()`/`shutdown()` run.
6. Confirm at least ten traces in Langfuse and save `05_langfuse_trace_list.png`.
7. Open a trace with agent → retrieval → fake-llm hierarchy and save `06_trace_waterfall.png`.

## Version/promotion/rollback

1. With `LANGFUSE_PROMPT_LABEL=baseline`, send a request and record its trace ID/version.
2. Run `python scripts/manage_prompts.py promote-v2`, restart the app with label `production`, send the same input and record the v2 trace.
3. Run `python scripts/manage_prompts.py rollback-v1`, restart/send again and record the post-rollback v1 trace.
4. Save real UI evidence as `07_prompt_v1.png`, `08_prompt_v2.png`, `09_prompt_v2_trace.png`, `10_prompt_rollback.png`, and `10b_prompt_rollback_trace.png`.

## Official rag_slow chain

1. Start the traced app and run `python scripts/inject_incident.py` followed by `python scripts/load_test.py --challenge --concurrency 5`.
2. Save the new metric window separately from the earlier untraced run.
3. Find a `feature=refund` trace in that window and record trace ID, correlation ID, total duration and retrieval duration.
4. Find the exact `response_sent` log with the same correlation ID.
5. Disable the incident with `python scripts/inject_incident.py --disable`.
6. Save `15_incident_metrics.png`, `16_incident_trace.png`, `17_incident_logs.md`, and `18_root_cause.md`.

Only after these files and IDs exist should `submission/REPORT.md` remove the Langfuse/incident blockers.
