#!/usr/bin/env python3
"""Smoke check that required Hundun layout exists (fail-closed)."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = [
    "ARCHITECTURE.md",
    "core/protocol.py", "core/state.py", "core/contract.py",
    "core/routing.py", "core/budget.py",
    "agents/midwife.py", "agents/fourth.py",
    "deliberation/camera_a_reframe.py",
    "deliberation/camera_b_evidence.py",
    "deliberation/camera_c_dissent.py",
]
missing = [p for p in REQUIRED if not (ROOT / p).exists()]
if missing:
    print("FAIL: missing required files:")
    for m in missing:
        print(" ", m)
    sys.exit(1)
print("OK: Hundun layout verified")
sys.exit(0)
