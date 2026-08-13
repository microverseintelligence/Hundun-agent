"""Speaker — unsolicited insight. May stay silent."""
from __future__ import annotations
from typing import Optional
from core.protocol import AgentMessage, MessageBus
import random

class Speaker:
    name = "speaker"
    def __init__(self, bus: MessageBus, llm=None, speak_probability: float = 0.35):
        self.bus = bus
        self.llm = llm
        self.speak_probability = speak_probability

    def maybe_speak(self, context: str, force: bool = False) -> Optional[AgentMessage]:
        if not force and random.random() > self.speak_probability:
            return None
        if self.llm:
            content = self.llm.complete(f"Spontaneous insight only if something real arises, else SILENCE.\n{context}").strip()
            if content.upper() == "SILENCE" or not content:
                return None
        else:
            candidates = [
                "There is a cost here that has not been named yet.",
                "The question itself may already contain a hidden assumption.",
                None, None,
            ]
            content = random.choice(candidates)
            if content is None:
                return None
        msg = AgentMessage(from_agent="speaker", to_agent="midwife", kind="spontaneous", content=content, metadata={"forced": force})
        self.bus.send(msg)
        return msg
