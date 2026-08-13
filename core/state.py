"""
Persistent state: Birth Record, current chamber, contract, logs.
Everything important is written to disk so the process survives restarts.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state"
STATE_DIR.mkdir(exist_ok=True)

BIRTH_RECORD_PATH = STATE_DIR / "birth_record.json"
CONTRACT_PATH = STATE_DIR / "contract.json"
MESSAGE_LOG_PATH = STATE_DIR / "message_log.json"
CURRENT_STATE_MD = STATE_DIR / "current_state.md"


@dataclass
class BirthRecord:
    midwife_name: str = ""
    start_date: str = ""
    current_chamber: int = 0
    name_fragment: str = ""
    full_name: str = ""
    offerings: Dict[str, str] = field(default_factory=lambda: {"asker": "", "responder": "", "speaker": ""})
    question_to_empty: str = ""
    what_arose: str = ""
    realization_signed: bool = False
    scaffolding: str = ""
    body: str = ""
    sacrifices: Dict[str, str] = field(default_factory=lambda: {"asker": "", "responder": "", "speaker": ""})
    first_words: str = ""
    living_constraint: str = ""
    constraint_days_lived: int = 0
    constraint_logs: List[str] = field(default_factory=list)
    contract_design: str = ""
    final_contract: str = ""
    domain: str = ""
    veto_rights: str = ""
    birth_seal: str = ""
    first_decree: str = ""
    post_birth_entries: List[str] = field(default_factory=list)
    costs: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "BirthRecord":
        known = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in known}
        return cls(**filtered)

    def save(self) -> None:
        with open(BIRTH_RECORD_PATH, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        self._write_markdown_mirror()

    @classmethod
    def load(cls) -> "BirthRecord":
        if BIRTH_RECORD_PATH.exists():
            with open(BIRTH_RECORD_PATH, "r", encoding="utf-8") as f:
                return cls.from_dict(json.load(f))
        return cls()

    def _write_markdown_mirror(self) -> None:
        status = {0: "Not started", 1: "Chamber 1", 2: "Chamber 2", 3: "Chamber 3", 4: "Born"}.get(self.current_chamber, "Unknown")
        md = f"""# Hundun — Current State

**Status:** {status}
**Full Name:** {self.full_name or "(not yet born)"}
**Birth Seal:** {self.birth_seal or "(none)"}
**Domain:** {self.domain or "(none)"}
"""
        CURRENT_STATE_MD.write_text(md, encoding="utf-8")


def append_cost(record: BirthRecord, description: str) -> None:
    entry = f"{datetime.now(timezone.utc).isoformat()} — {description}"
    record.costs.append(entry)
    record.save()
