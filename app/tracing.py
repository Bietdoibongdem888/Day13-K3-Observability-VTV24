from __future__ import annotations

import os
from contextvars import ContextVar
from functools import wraps
from typing import Any

try:
    from langfuse import get_client, observe

    LANGFUSE_SDK_AVAILABLE = True
except ImportError:  # pragma: no cover - chỉ dùng khi chưa cài requirements
    LANGFUSE_SDK_AVAILABLE = False

    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func

        return decorator

    class _DummyClient:
        def update_current_trace(self, **kwargs: Any) -> None:
            return None

        def update_current_generation(self, **kwargs: Any) -> None:
            return None

    def get_client():
        return _DummyClient()


_TRACE_CONTEXT_ACTIVE: ContextVar[bool] = ContextVar(
    "langfuse_trace_context_active", default=False
)


class _NoopClient:
    def update_current_trace(self, **kwargs: Any) -> None:
        return None

    def update_current_generation(self, **kwargs: Any) -> None:
        return None


def get_langfuse_client():
    if not tracing_enabled():
        return _NoopClient()
    return get_client()


def flush_traces() -> None:
    """Flush queued spans during a graceful application shutdown."""
    if not tracing_enabled():
        return
    client = get_langfuse_client()
    client.flush()
    client.shutdown()


def tracing_enabled() -> bool:
    return LANGFUSE_SDK_AVAILABLE and bool(
        os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")
    )


def observe_when_enabled(*args: Any, root: bool = False, **kwargs: Any):
    """Apply Langfuse instrumentation only when both credentials are available."""
    def decorator(func):
        traced = observe(*args, **kwargs)(func)

        @wraps(func)
        def wrapper(*func_args: Any, **func_kwargs: Any):
            if not tracing_enabled():
                return func(*func_args, **func_kwargs)
            if not root and not _TRACE_CONTEXT_ACTIVE.get():
                return func(*func_args, **func_kwargs)
            if not root:
                return traced(*func_args, **func_kwargs)

            token = _TRACE_CONTEXT_ACTIVE.set(True)
            try:
                return traced(*func_args, **func_kwargs)
            finally:
                _TRACE_CONTEXT_ACTIVE.reset(token)

        return wrapper

    return decorator
