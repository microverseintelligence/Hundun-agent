"""Camera A — REFRAME"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

@dataclass
class ReframeResult:
    intent: str
    subquestions: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    unknowns: List[str] = field(default_factory=list)
    risk_flags: List[str] = field(default_factory=list)

def reframe(raw_request: str, llm=None) -> ReframeResult:
    if llm:
        _ = llm.complete(f"REFRAME the request: {raw_request}")
    return ReframeResult(
        intent=raw_request.strip(),
        subquestions=[raw_request.strip()],
        success_criteria=["Source-backed answer if factual; clear decision if actionable."],
        unknowns=["Whether primary sources are required."],
        risk_flags=[],
    )
