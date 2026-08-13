"""
Inter-agent message protocol.
All communication between Midwife, Asker, Responder, Speaker and Fourth
must go through AgentMessage. No free-form chat is allowed.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Literal
import uuid


AgentName = Literal["midwife", "asker", "responder", "speaker", "fourth"]
MessageKind = Literal[
    "request", "question", "answer", "spontaneous", "offering",
    "review", "veto", "accept", "counter", "decision", "constraint",
    "body", "first_words", "seal", "decree", "cost", "system",
]


@dataclass
class AgentMessage:
    from_agent: AgentName
    to_agent: AgentName
    kind: MessageKind
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "AgentMessage":
        return cls(**data)

    def __str__(self) -> str:
        return f"[{self.from_agent} → {self.to_agent}] ({self.kind}) {self.content[:120]}"


class MessageBus:
    """Simple in-memory + append-only log of all messages."""

    def __init__(self):
        self.history: list[AgentMessage] = []

    def send(self, msg: AgentMessage) -> AgentMessage:
        self.history.append(msg)
        return msg

    def last(self, n: int = 10) -> list[AgentMessage]:
        return self.history[-n:]

    def filter(self, from_agent: Optional[str] = None, kind: Optional[str] = None) -> list[AgentMessage]:
        result = self.history
        if from_agent:
            result = [m for m in result if m.from_agent == from_agent]
        if kind:
            result = [m for m in result if m.kind == kind]
        return result

    def dump(self) -> list[dict]:
        return [m.to_dict() for m in self.history]

    def load(self, data: list[dict]) -> None:
        self.history = [AgentMessage.from_dict(d) for d in data]
