# Adaptive Deliberation & Self-Improvement Layer (ADSIL)

Unified Personal Agent Architecture v1 — implemented as **Hundun**

This document is the canonical architecture.

It unifies:

1. `Phaizov/no-terminal-state` — persistent self-improvement, distilled lessons, improvement vectors, external grounding
2. `Phaizov/the-fourth` — structured alternative perspective, bounded agency, living constraint, contract
3. `microverseintelligence/the-fourth-agentic` — executable multi-agent workflow with Midwife, Asker, Responder, Speaker, Fourth

Plus all critical fixes from the independent audit of `no-terminal-state` (2026-08-12).

---

## Core Invariant

> **A change is not an improvement until it produces independent, observable gain.**

Additional invariants:

1. Internal self-score is never proof of external quality.
2. Candidate policy never replaces production without a regression gate.
3. Sealed evaluation data is inaccessible to the process being optimized.
4. Any increase in authority requires an explicit contract.
5. The system may correctly remain in `idle`.
6. Without sufficient evidence the system may answer `uncertain` or request more research.
7. Fourth is not required to agree with the majority.
8. Midwife is not required to accept either Responder or Fourth.
9. When sources conflict, prefer search over confident synthesis.
10. Every behavior/policy change has provenance and a rollback path.

---

## Runtime Pipeline

```
USER
  |
  v
MIDWIFE (Intent / Policy / Evidence Arbiter)
  |
Risk / Complexity Gate
  |
  +-- R0/R1 → direct answer + light validation
  |
  +-- R2+ → full deliberation
        |
        Camera A  REFRAME
        Camera B  EVIDENCE
        Camera C  DISSENT
        Responder SOLVE
        Fourth    BLIND independent research → comparison
        |
        Midwife arbitration
        |
     MERGE / SEARCH_AGAIN / USE_RESPONDER / USE_FOURTH / ASK_USER / REFUSE
        |
        FINAL RESPONSE
        |
        Outcome / Feedback
        |
        Learning Observer → Lesson Distillation → Improvement Queue
        |
        Shadow / Trial → Evaluator → promote / reject / rollback
```

---

## Risk Classes

| Class | Example | Pipeline |
|-------|---------|----------|
| R0 | trivial transformation | 1-pass |
| R1 | ordinary lookup | 1-pass + light validation |
| R2 | research / current info | Cameras + Fourth |
| R3 | legal / financial / medical | full deliberation + evidence gate |
| R4 | irreversible decision | full + mandatory Fourth + explicit Midwife confirmation |
| R5 | system / policy mutation | full + external evaluation + rollback |

---

## Key Corrections

### From the-fourth-agentic

- Fourth no longer receives the Responder answer before its own independent reasoning (blind phase).
- Two-phase Fourth: (1) blind independent, (2) comparison.
- Midwife is Evidence Arbiter, not a summarizer.
- Real veto with override logging and cost recording.

### From no-terminal-state

- No self-assigned 3x/6x capability multipliers.
- No perpetual mandatory improvement loop.
- Fail-closed snapshot/hash/eval.
- Sealed evaluation data outside agent trust domain.
- Idle is a valid terminal runtime state.
- Lessons require validation before activation.
- Candidate policies go through shadow → trial → A/B → promote/reject.

---

## Name

**Hundun (混沌)** — the undifferentiated state that dies when forced to accept premature orifices.

The system may remain idle. That is not failure. That is integrity.

---

**Key principle**

> An agent is allowed to propose changes to itself,  
> but is forbidden from proving to itself that those changes made it better.
