# Hundun Agent

**Hundun does not claim progress.  
It only records what survived external contact.**

---

Hundun is the executable form of the **Adaptive Deliberation & Self-Improvement Layer (ADSIL)**.

It unifies three lineages:

1. Structured alternative perspective and contractual veto (`the-fourth`)
2. Executable multi-agent orchestration (`the-fourth-agentic`)
3. Persistent lessons + external grounding without self-scoring (`no-terminal-state`)

And applies the critical corrections from the independent audit of `no-terminal-state`.

---

## Core invariant

> A change is not an improvement until it produces independent, observable gain.

Hundun is allowed to propose changes to itself.  
It is forbidden from proving to itself that those changes made it better.

---

## What runs

```
USER
  → Midwife (Evidence Arbiter)
  → Risk / Complexity Gate (R0–R5)
  → Camera A  REFRAME
  → Camera B  EVIDENCE
  → Camera C  DISSENT
  → Responder
  → Fourth (blind independent → comparison)
  → Midwife arbitration
  → MERGE / SEARCH_AGAIN / USE_RESPONDER / USE_FOURTH / REFUSE
  → Outcome
  → (later) Lesson → Trial → External Evaluation → Promote / Rollback
```

Fourth never sees the Responder’s answer before its own independent reasoning.

---

## Layout

```
Hundun-agent/
├── ARCHITECTURE.md          # full design
├── agents/                  # Midwife, Asker, Responder, Speaker, Fourth
├── core/                    # protocol, state, contract, routing, budget
├── deliberation/            # three cameras
├── tools/verify_layout.py
└── README.md
```

---

## Status

Phase 0–2 foundation is present:

- Risk-based routing
- Budget limits
- Three epistemic cameras
- Blind Fourth + comparison
- Midwife as Evidence Arbiter
- Real veto / override logging

Memory, improvement trials, and sealed external evaluation are next.

---

## Name

Hundun (混沌) — the undifferentiated state that dies when forced to accept premature orifices.

The system may remain idle.  
That is not failure. That is integrity.
