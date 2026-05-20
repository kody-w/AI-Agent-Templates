"""Safety Analytics Agent — Energy Utilities.

Aggregates KPIs across permits over a window: average cycle time, on-time closure rate, near-miss rate, top hazards. Synthetic.

Portable. No PII. Plugs into the rapp_ai BasicAgent runtime.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from agents.basic_agent import BasicAgent
from datetime import datetime, timedelta
import hashlib
import random


def _stable_seed(*parts) -> int:
    h = hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()
    return int(h[:8], 16)


class SafetyAnalyticsAgent(BasicAgent):
    def __init__(self):
        self.name = "SafetyAnalyticsAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Aggregates permit-cycle KPIs over a rolling window: cycle time, "
                "on-time closure, near-miss rate, top hazards."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "window_days": {"type": "integer"},
                    "region": {"type": "string"},
                },
                "required": [],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        window = int(kwargs.get("window_days") or 30)
        region = kwargs.get("region") or "all"
        seed = _stable_seed("safety_kpi", window, region)
        rng = random.Random(seed)

        permits_issued = rng.randint(80, 240) * max(1, window // 7)
        permits_closed_on_time = int(permits_issued * rng.uniform(0.82, 0.96))
        near_misses = int(permits_issued * rng.uniform(0.01, 0.04))
        avg_cycle_hours = round(rng.uniform(12, 36), 1)

        top_hazards = rng.sample(
            ["Electric shock / arc flash", "Working at height", "Confined space",
             "Cable strike", "Manual handling", "SF6 exposure"], k=4
        )

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Safety KPIs computed over {window} day(s) for region `{region}`.",
            "data": {
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
                "window_days": window,
                "region": region,
                "permits_issued": permits_issued,
                "permits_closed_on_time": permits_closed_on_time,
                "on_time_closure_rate": round(permits_closed_on_time / permits_issued, 3),
                "near_miss_count": near_misses,
                "near_miss_rate_per_100_permits": round(100 * near_misses / permits_issued, 2),
                "avg_cycle_hours": avg_cycle_hours,
                "top_hazards": top_hazards,
                "data_quality": "synthetic; deterministic per (window, region)",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(SafetyAnalyticsAgent().perform(window_days=30), indent=2))
