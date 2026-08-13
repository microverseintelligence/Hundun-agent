"""
Per-request budget tracking.
Prevents unbounded recursion and cost explosions.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict


@dataclass
class Budget:
    max_llm_calls: int = 8
    max_tool_calls: int = 12
    max_latency_ms: int = 120_000
    max_cost_units: float = 10.0

    llm_calls: int = 0
    tool_calls: int = 0
    cost_units: float = 0.0
    started_ms: int = 0

    def remaining(self) -> Dict[str, float]:
        return {
            "llm_calls": max(0, self.max_llm_calls - self.llm_calls),
            "tool_calls": max(0, self.max_tool_calls - self.tool_calls),
            "cost_units": max(0.0, self.max_cost_units - self.cost_units),
        }

    def can_afford(self, llm: int = 0, tools: int = 0, cost: float = 0.0) -> bool:
        return (
            self.llm_calls + llm <= self.max_llm_calls
            and self.tool_calls + tools <= self.max_tool_calls
            and self.cost_units + cost <= self.max_cost_units
        )

    def charge(self, llm: int = 0, tools: int = 0, cost: float = 0.0) -> None:
        self.llm_calls += llm
        self.tool_calls += tools
        self.cost_units += cost

    def exhausted(self) -> bool:
        r = self.remaining()
        return r["llm_calls"] <= 0 or r["cost_units"] <= 0
