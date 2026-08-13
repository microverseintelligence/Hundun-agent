"""
Risk-based routing for Hundun / ADSIL.
Depth of deliberation is determined by risk class, not habit.
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import List


class RiskClass(str, Enum):
    R0 = "R0"  # trivial
    R1 = "R1"  # ordinary
    R2 = "R2"  # research / current info
    R3 = "R3"  # high-stakes domain
    R4 = "R4"  # irreversible decision
    R5 = "R5"  # system/policy mutation


@dataclass
class RoutingDecision:
    risk: RiskClass
    use_cameras: bool
    use_fourth_blind: bool
    require_evidence_gate: bool
    require_midwife_confirmation: bool
    require_external_eval: bool
    max_extra_research: int
    reason: str


def classify_risk(text: str, flags: List[str] | None = None) -> RiskClass:
    flags = flags or []
    t = text.lower()

    if any(k in t for k in ("mutate policy", "change kernel", "promote candidate", "rollback")):
        return RiskClass.R5
    if any(k in t for k in ("delete", "irreversible", "permanently", "execute order", "transfer funds")):
        return RiskClass.R4
    if any(k in t for k in ("legal", "medical", "financial", "regulation", "compliance", "ai act")):
        return RiskClass.R3
    if any(k in t for k in ("current", "latest", "as of", "today", "research", "what changed", "compare sources")):
        return RiskClass.R2
    if any(k in t for k in ("rewrite", "summarize", "translate", "format")) and len(t) < 200:
        return RiskClass.R0
    return RiskClass.R1


def route(text: str, flags: List[str] | None = None) -> RoutingDecision:
    risk = classify_risk(text, flags)

    if risk == RiskClass.R0:
        return RoutingDecision(risk, False, False, False, False, False, 0, "trivial transformation")
    if risk == RiskClass.R1:
        return RoutingDecision(risk, False, False, False, False, False, 0, "ordinary lookup")
    if risk == RiskClass.R2:
        return RoutingDecision(risk, True, True, True, False, False, 2, "research / current information")
    if risk == RiskClass.R3:
        return RoutingDecision(risk, True, True, True, True, False, 3, "high-stakes domain")
    if risk == RiskClass.R4:
        return RoutingDecision(risk, True, True, True, True, False, 3, "irreversible decision")
    return RoutingDecision(risk, True, True, True, True, True, 4, "system or policy mutation")
