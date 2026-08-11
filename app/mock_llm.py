from __future__ import annotations

import random
import time
from dataclasses import dataclass

from .incidents import STATE
from .tracing import observe_when_enabled


@dataclass
class FakeUsage:
    input_tokens: int
    output_tokens: int


@dataclass
class FakeResponse:
    text: str
    usage: FakeUsage
    model: str


class FakeLLM:
    def __init__(self, model: str = "claude-sonnet-4-5") -> None:
        self.model = model

    @observe_when_enabled(name="fake-llm", as_type="generation", capture_input=False, capture_output=False)
    def generate(self, prompt: str) -> FakeResponse:
        time.sleep(0.15)
        input_tokens = max(20, len(prompt) // 4)
        output_tokens = random.randint(80, 180)
        if STATE["cost_spike"]:
            output_tokens *= 4
        docs = prompt.partition("Docs=")[2].partition("\nQuestion=")[0].strip()
        if docs and not docs.startswith("No domain document matched"):
            answer = f"Based on the retrieved context: {docs}"
        else:
            answer = (
                "I do not have matching domain context for this question. "
                "Please provide more detail or consult the relevant service owner."
            )
        return FakeResponse(text=answer, usage=FakeUsage(input_tokens, output_tokens), model=self.model)
