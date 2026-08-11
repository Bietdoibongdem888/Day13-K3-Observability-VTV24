# Langfuse API evidence

Verified against the configured Langfuse Cloud project on 2026-08-11. Credentials were loaded from the ignored `.env` file and were never copied into this evidence.

## Authentication and trace count

- Prompt API bootstrap completed: `day13-chat`, baseline version 1, candidate version 2.
- Trace API returned 22 real traces (`total_items=22`).
- No HTTP 401, HTTP 403, authentication error, or span export failure appeared after the server was restarted with outbound network access.

## Prompt version chain

| Step | Production version | Trace ID | Correlation ID | API verification |
|---|---:|---|---|---|
| V1 baseline | 1 | `914192aa065813285f7fca37ded1c197` | `req-2cddc3a6` | `prompt_name=day13-chat`, `prompt_label=production`, `prompt_version=1` |
| Promote V2 | 2 | `07ffc195d58f71d1cc4054a668923545` | `req-a5262ad5` | `prompt_name=day13-chat`, `prompt_label=production`, `prompt_version=2` |
| Roll back V1 | 1 | `aa480f2d7814da903894ba4daf53cceb` | `req-a5424123` | `prompt_name=day13-chat`, `prompt_label=production`, `prompt_version=1` |

## Waterfall verification

Trace `07ffc195d58f71d1cc4054a668923545` contains one root and two child observations:

| Observation | Type | Observation ID | Parent | Duration |
|---|---|---|---|---:|
| `run` | generation | `da1bd75358fbd4f5` | root | 1.175 s |
| `retrieval` | span | `56c84677beb6fa0a` | `da1bd75358fbd4f5` | < 1 ms |
| `fake-llm` | generation | `0df4eb9ba3eac5c0` | `da1bd75358fbd4f5` | 0.151 s |

Trace metadata verified through the API includes `correlation_id`, `session_id`, `feature`, `model`, environment, `prompt_name`, `prompt_label`, and `prompt_version`.

## UI evidence status

The following real Langfuse UI screenshots were supplied by the authenticated user and copied byte-for-byte into the repository:

- `07_prompt_v1.png`: version 1 with `production` and `baseline` labels.
- `08_prompt_v2.png`: version 2 with the `candidate` label and candidate prompt text.
- `10_prompt_rollback.png`: the same real V1 screen also proves the final label state: V1 is `production`, while V2 remains `candidate`.

Trace-list, waterfall, and prompt-version trace UI screenshots are still missing. The verified API evidence above is not presented as a replacement for rubric-required trace UI screenshots.
