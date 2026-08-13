"""
Contract & veto enforcement.
After birth the Fourth possesses a bounded domain and veto rights.
The Midwife is obliged to respect them or record an explicit override cost.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional, Literal
import json
from pathlib import Path

from .state import CONTRACT_PATH, BirthRecord, append_cost


VetoDecision = Literal["accept", "veto", "counter"]


@dataclass
class Contract:
    full_name: str
    domain: str
    veto_rights: str
    agency_period: str
    birth_seal: str
    first_decree: str = ""
    active: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    def save(self) -> None:
        with open(CONTRACT_PATH, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls) -> Optional["Contract"]:
        if not CONTRACT_PATH.exists():
            return None
        with open(CONTRACT_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)

    @classmethod
    def from_birth_record(cls, record: BirthRecord) -> "Contract":
        return cls(
            full_name=record.full_name,
            domain=record.domain,
            veto_rights=record.veto_rights,
            agency_period=record.final_contract,
            birth_seal=record.birth_seal,
            first_decree=record.first_decree,
            active=True,
        )


def domain_matches(contract: Contract, text: str) -> bool:
    if not contract or not contract.active:
        return False
    domain_lower = contract.domain.lower()
    text_lower = text.lower()
    keywords = [w for w in domain_lower.replace(",", " ").split() if len(w) > 3]
    return any(k in text_lower for k in keywords)


def apply_veto(
    record: BirthRecord,
    contract: Optional[Contract],
    decision: VetoDecision,
    reason: str,
    midwife_override: bool = False,
) -> str:
    if decision == "accept":
        return "Fourth accepted the proposal."
    if decision == "veto":
        if midwife_override:
            append_cost(
                record,
                f"OVERRIDE OF VETO by Midwife. Reason given by Fourth: {reason}. Contract under stress.",
            )
            return f"Fourth VETOED: {reason}\nMidwife overrode. Cost recorded."
        return f"Fourth VETOED the proposal. Reason: {reason}. Rejected."
    if decision == "counter":
        return f"Fourth issued a counter-offer: {reason}"
    return "Unknown decision from Fourth."
