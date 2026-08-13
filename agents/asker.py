"""Asker — formulates one clear, deliberate question. Never answers."""
from __future__ import annotations
from core.protocol import AgentMessage, MessageBus

class Asker:
    name = "asker"
    def __init__(self, bus: MessageBus, llm=None):
        self.bus = bus
        self.llm = llm

    def formulate(self, raw_intent: str, context: str = "") -> AgentMessage:
        if self.llm:
            content = self.llm.complete(
                f"Formulate one clear question from: {raw_intent}\nContext: {context}"
            )
        else:
            cleaned = raw_intent.strip()
            content = cleaned if cleaned.endswith("?") else f"What is the precise action or decision required regarding: {cleaned}?"
        msg = AgentMessage(from_agent="asker", to_agent="responder", kind="question", content=content, metadata={"raw_intent": raw_intent})
        self.bus.send(msg)
        return msg
