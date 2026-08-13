"""Responder — direct functional answer to the exact question. No spontaneous advice."""
from __future__ import annotations
from core.protocol import AgentMessage, MessageBus

class Responder:
    name = "responder"
    def __init__(self, bus: MessageBus, llm=None):
        self.bus = bus
        self.llm = llm

    def answer(self, question: AgentMessage) -> AgentMessage:
        if question.kind != "question":
            raise ValueError("Responder only answers kind=question")
        if self.llm:
            content = self.llm.complete(f"Answer directly and functionally: {question.content}")
        else:
            content = f"[Responder — no LLM] Direct answer required for: «{question.content}»"
        msg = AgentMessage(from_agent="responder", to_agent="midwife", kind="answer", content=content, metadata={"in_reply_to": question.message_id})
        self.bus.send(msg)
        return msg
