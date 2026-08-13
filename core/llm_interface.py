"""
Thin LLM adapter.
Replace the complete() method with any provider.
"""

from __future__ import annotations
from typing import Optional


class LLMInterface:
    def complete(self, prompt: str, system: Optional[str] = None) -> str:
        raise NotImplementedError("Plug in a real backend")


class EchoLLM(LLMInterface):
    def complete(self, prompt: str, system: Optional[str] = None) -> str:
        return f"[EchoLLM] Received prompt of length {len(prompt)}. No real generation."


class OpenAILLM(LLMInterface):
    def __init__(self, model: str = "gpt-4o-mini", api_key: Optional[str] = None):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("pip install openai")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def complete(self, prompt: str, system: Optional[str] = None) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        resp = self.client.chat.completions.create(model=self.model, messages=messages)
        return resp.choices[0].message.content or ""
