from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

load_dotenv(REPO_ROOT / ".env")

from app.cli import configure_utf8_stdio
from app.tracing import get_langfuse_client, tracing_enabled


PROMPT_NAME = os.getenv("LANGFUSE_PROMPT_NAME", "day13-chat")
PROMPT_V1 = "Feature={{feature}}\nDocs={{docs}}\nQuestion={{message}}"
PROMPT_V2 = (
    "Feature={{feature}}\nDocs={{docs}}\nQuestion={{message}}\n"
    "Answer concisely and ground the response in Docs."
)


def require_client():
    if not tracing_enabled():
        raise RuntimeError(
            "Thiếu LANGFUSE_PUBLIC_KEY/LANGFUSE_SECRET_KEY; không thể thay đổi prompt thật."
        )
    return get_langfuse_client()


def get_by_label(client, label: str):
    try:
        return client.get_prompt(PROMPT_NAME, label=label, type="text", cache_ttl_seconds=0)
    except Exception:
        return None


def bootstrap(client) -> tuple[int, int]:
    baseline = get_by_label(client, "baseline")
    if baseline is None:
        baseline = client.create_prompt(
            name=PROMPT_NAME,
            prompt=PROMPT_V1,
            labels=["baseline", "production"],
            type="text",
            commit_message="Create Day 13 baseline prompt",
        )
    candidate = get_by_label(client, "candidate")
    if candidate is None:
        candidate = client.create_prompt(
            name=PROMPT_NAME,
            prompt=PROMPT_V2,
            labels=["candidate"],
            type="text",
            commit_message="Create Day 13 candidate prompt",
        )
    return int(baseline.version), int(candidate.version)


def main() -> int:
    configure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Quản lý prompt Day 13 thật trên Langfuse")
    parser.add_argument("action", choices=["bootstrap", "promote-v2", "rollback-v1"])
    args = parser.parse_args()
    try:
        client = require_client()
        baseline_version, candidate_version = bootstrap(client)
        if args.action == "promote-v2":
            client.update_prompt(
                name=PROMPT_NAME,
                version=candidate_version,
                new_labels=["candidate", "production"],
            )
        elif args.action == "rollback-v1":
            client.update_prompt(
                name=PROMPT_NAME,
                version=baseline_version,
                new_labels=["baseline", "production"],
            )
        print(
            f"OK: {PROMPT_NAME} baseline=v{baseline_version}, "
            f"candidate=v{candidate_version}, action={args.action}"
        )
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
