"""Camera B — EVIDENCE"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

@dataclass
class Claim:
    claim: str
    sources: List[str] = field(default_factory=list)
    source_dates: List[str] = field(default_factory=list)
    authority: str = "low"
    confidence: float = 0.0

@dataclass
class EvidenceResult:
    claims: List[Claim] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)

def gather_evidence(intent: str, subquestions: List[str], llm=None, tools=None) -> EvidenceResult:
    return EvidenceResult(claims=[], contradictions=[])
