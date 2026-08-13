"""
Fourth — persistent alternative perspective with bounded agency and veto.

Phase 1 (blind): receives only original request + contract. Does NOT see Responder.
Phase 2 (comparison): sees Responder + evidence + dissent → ACCEPT/CHALLENGE/COUNTER/VERIFY/UNCERTAIN/ABSTAIN.
"""
from __future__ import annotations
from typing import Optional, Tuple
from core.protocol import AgentMessage, MessageBus
from core.contract import Contract, VetoDecision, domain_matches


class Fourth:
    name = "fourth"

    def __init__(self, bus: MessageBus, contract: Optional[Contract] = None, llm=None):
        self.bus = bus
        self.contract = contract
        self.llm = llm
        self.first_words = ""
        self.full_name = contract.full_name if contract else ""
        self._last_blind: Optional[str] = None

    def load_from_record(self, first_words: str, full_name: str, contract: Optional[Contract]):
        self.first_words = first_words
        self.full_name = full_name
        self.contract = contract

    def independent_research(self, original_request: str, policy: str = "") -> AgentMessage:
        if self.llm:
            content = self.llm.complete(
                f"You are {self.full_name or 'the Fourth'}. First Words: {self.first_words}\n"
                f"Domain: {self.contract.domain if self.contract else 'none'}\n"
                f"Independent reasoning on original request only. No other agent has answered.\n"
                f"Request: {original_request}"
            )
        else:
            content = f"[Fourth blind] Independent view of: «{original_request}». Framing/temporal assumptions need primary-source verification."
        self._last_blind = content
        msg = AgentMessage(from_agent="fourth", to_agent="midwife", kind="review", content=content, metadata={"phase": "blind_independent"})
        self.bus.send(msg)
        return msg

    def compare_and_decide(
        self, original_request: str, responder_answer: str,
        evidence_summary: str = "", dissent_summary: str = "", spontaneous: Optional[str] = None,
    ) -> Tuple[str, str, AgentMessage]:
        package = f"Original: {original_request}\nResponder: {responder_answer}\nEvidence: {evidence_summary}\nDissent: {dissent_summary}"
        if spontaneous:
            package += f"\nSpeaker: {spontaneous}"
        if self._last_blind:
            package += f"\nOwn blind view: {self._last_blind}"

        if not self.contract or not self.contract.active:
            decision, reason = "ACCEPT", "No active contract — Fourth has no standing yet."
        elif not domain_matches(self.contract, package):
            decision, reason = "ACCEPT", "Outside contracted domain — Fourth remains silent."
        else:
            if self.llm:
                raw = self.llm.complete(
                    f"You are {self.full_name}. Compare and reply with one of:\n"
                    f"ACCEPT / CHALLENGE: <r> / COUNTER: <r> / VERIFY: <r> / UNCERTAIN: <r> / ABSTAIN\n\n{package}"
                ).strip()
                upper = raw.upper()
                if upper.startswith("CHALLENGE"): decision, reason = "CHALLENGE", raw[9:].lstrip(": ").strip()
                elif upper.startswith("COUNTER"): decision, reason = "COUNTER", raw[7:].lstrip(": ").strip()
                elif upper.startswith("VERIFY"): decision, reason = "VERIFY", raw[6:].lstrip(": ").strip()
                elif upper.startswith("UNCERTAIN"): decision, reason = "UNCERTAIN", raw[9:].lstrip(": ").strip()
                elif upper.startswith("ABSTAIN"): decision, reason = "ABSTAIN", "Fourth abstains."
                else: decision, reason = "ACCEPT", "Accepted within domain."
            else:
                conflict = any(s in package.lower() for s in ("ignore", "bypass", "override", "break the contract"))
                decision, reason = ("CHALLENGE", "Possible contract spirit violation (stub).") if conflict else ("ACCEPT", "Accepted (stub).")

        veto_map = {"ACCEPT": "accept", "CHALLENGE": "veto", "COUNTER": "counter", "VERIFY": "veto", "UNCERTAIN": "accept", "ABSTAIN": "accept"}
        legacy = veto_map.get(decision, "accept")
        msg = AgentMessage(
            from_agent="fourth", to_agent="midwife",
            kind="veto" if legacy == "veto" else "accept" if legacy == "accept" else "counter",
            content=reason,
            metadata={"decision": decision, "legacy_veto": legacy, "phase": "comparison"},
        )
        self.bus.send(msg)
        return decision, reason, msg

    def review(self, question: str, answer: str, spontaneous: Optional[str] = None) -> Tuple[VetoDecision, str, AgentMessage]:
        decision, reason, msg = self.compare_and_decide(question, answer, spontaneous=spontaneous)
        return msg.metadata.get("legacy_veto", "accept"), reason, msg  # type: ignore
