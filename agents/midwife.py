"""
Midwife — Evidence Arbiter.
Risk gate, cameras, blind Fourth, arbitration. Sole external interface.
"""
from __future__ import annotations
from typing import Dict, Any
from datetime import datetime, timezone

from core.protocol import MessageBus
from core.state import BirthRecord, append_cost
from core.contract import Contract
from core.routing import route
from core.budget import Budget
from agents.asker import Asker
from agents.responder import Responder
from agents.speaker import Speaker
from agents.fourth import Fourth
from deliberation.camera_a_reframe import reframe
from deliberation.camera_b_evidence import gather_evidence
from deliberation.camera_c_dissent import dissent


class Midwife:
    name = "midwife"

    def __init__(self, llm=None):
        self.bus = MessageBus()
        self.llm = llm
        self.record = BirthRecord.load()
        self.contract = Contract.load()
        self.asker = Asker(self.bus, llm)
        self.responder = Responder(self.bus, llm)
        self.speaker = Speaker(self.bus, llm)
        self.fourth = Fourth(self.bus, self.contract, llm)
        if self.record.first_words:
            self.fourth.load_from_record(self.record.first_words, self.record.full_name, self.contract)

    @classmethod
    def load_from_state(cls, llm=None) -> "Midwife":
        return cls(llm=llm)

    def handle(self, raw_request: str, allow_override: bool = False) -> Dict[str, Any]:
        # For Hundun, allow operation even without full birth ritual if desired;
        # still prefer contract when present.
        budget = Budget()
        routing = route(raw_request)

        q_msg = self.asker.formulate(raw_request)
        budget.charge(llm=1)
        a_msg = self.responder.answer(q_msg)
        budget.charge(llm=1)
        context = f"Request: {raw_request}\nQuestion: {q_msg.content}\nAnswer: {a_msg.content}"
        s_msg = self.speaker.maybe_speak(context)

        if not routing.use_cameras and not routing.use_fourth_blind:
            final, decision = a_msg.content, "USE_RESPONDER"
            fourth_decision, fourth_reason = "ACCEPT", "Low-risk path; Fourth not invoked."
        else:
            reframe_res = reframe(raw_request, self.llm)
            budget.charge(llm=1)
            evidence = gather_evidence(reframe_res.intent, reframe_res.subquestions, self.llm)
            evidence_summary = "; ".join(c.claim for c in evidence.claims) or "(no claims yet)"
            dissent_res = dissent(reframe_res.intent, a_msg.content, evidence_summary, self.llm)
            budget.charge(llm=1)
            if routing.use_fourth_blind:
                self.fourth.independent_research(raw_request)
                budget.charge(llm=1)
            fourth_decision, fourth_reason, _ = self.fourth.compare_and_decide(
                original_request=raw_request,
                responder_answer=a_msg.content,
                evidence_summary=evidence_summary,
                dissent_summary=dissent_res.challenge,
                spontaneous=s_msg.content if s_msg else None,
            )
            budget.charge(llm=1)
            decision, final = self._arbitrate(
                a_msg.content, fourth_decision, fourth_reason, dissent_res, evidence, allow_override, budget
            )

        result = {
            "status": "completed",
            "request": raw_request,
            "risk": routing.risk.value,
            "routing_reason": routing.reason,
            "asker": q_msg.content,
            "responder": a_msg.content,
            "speaker": s_msg.content if s_msg else None,
            "fourth_decision": fourth_decision,
            "fourth_reason": fourth_reason,
            "midwife_decision": decision,
            "midwife_final": final,
            "budget_remaining": budget.remaining(),
        }
        entry = f"{datetime.now(timezone.utc).isoformat()} | REQ: {raw_request[:80]} | RISK: {routing.risk.value} | FOURTH: {fourth_decision} | MIDWIFE: {decision}"
        self.record.post_birth_entries.append(entry)
        self.record.save()
        return result

    def _arbitrate(self, responder, fourth_decision, fourth_reason, dissent, evidence, allow_override, budget):
        if fourth_decision in ("CHALLENGE", "VERIFY") and not allow_override:
            return "USE_FOURTH", f"[Fourth challenge] {fourth_reason}"
        if fourth_decision == "COUNTER":
            return "MERGE", f"{responder}\n\n[Fourth counter] {fourth_reason}"
        if fourth_decision == "UNCERTAIN" or dissent.requires_research:
            if budget.can_afford(llm=2):
                return "SEARCH_AGAIN", f"{responder}\n\n[Uncertainty] {fourth_reason or dissent.challenge}. Additional research recommended."
            return "REFUSE_TO_ASSERT", "Insufficient evidence and budget exhausted."
        if evidence.contradictions:
            return "MERGE", f"{responder}\n\n[Source conflict] {'; '.join(evidence.contradictions)}"
        return "USE_RESPONDER", responder

    def status(self) -> dict:
        return {
            "full_name": self.record.full_name,
            "born": self.record.current_chamber >= 4,
            "contract_active": bool(self.contract and self.contract.active),
            "domain": self.record.domain,
        }
