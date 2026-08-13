"""Camera C — DISSENT / ADVERSARIAL"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

@dataclass
class DissentResult:
    challenge: str
    counter_hypotheses: List[str] = field(default_factory=list)
    missing_considerations: List[str] = field(default_factory=list)
    severity: str = "low"
    requires_research: bool = False

def dissent(intent: str, responder_answer: str = "", evidence_summary: str = "", llm=None) -> DissentResult:
    if llm:
        _ = llm.complete(f"DISSENT on: {intent}")
    return DissentResult(
        challenge="Possible framing or temporal assumption has not been independently verified.",
        counter_hypotheses=["The request may conflate related but distinct categories or dates."],
        missing_considerations=["Primary source dates and jurisdiction boundaries."],
        severity="medium",
        requires_research=True,
    )
