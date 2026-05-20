"""Demand Signal Requisition Agent — Energy Utilities.

Aggregates demand signals from the maintenance plan and capital programme and emits structured requisitions with quantity, urgency and budget.

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


SOURCES = ["maintenance_plan", "capital_programme", "emergency_replenishment"]


class DemandSignalRequisitionAgent(BasicAgent):
    def __init__(self):
        self.name = "DemandSignalRequisitionAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Aggregates demand from maintenance + capital plans into structured "
                "requisitions ready for procurement strategy."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "source_plan": {"type": "string", "enum": SOURCES},
                    "horizon_days": {"type": "integer"},
                    "category_filter": {"type": "string"},
                },
                "required": [],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        source = kwargs.get("source_plan") or "maintenance_plan"
        horizon = int(kwargs.get("horizon_days") or 90)
        cat = kwargs.get("category_filter")
        seed = _stable_seed("req", source, horizon, cat or "any")
        rng = random.Random(seed)

        catalogue = [
            ("MV cable replenishment", "cables", 350_000, 21),
            ("Distribution transformer", "transformers", 1_200_000, 90),
            ("Switchgear panel", "switchgear", 750_000, 60),
            ("Pole-mounted recloser", "field_devices", 95_000, 45),
            ("OH conductor (ACSR)", "conductors", 220_000, 30),
            ("Wood pole 12 m", "structures", 38_000, 14),
        ]
        if cat:
            catalogue = [c for c in catalogue if c[1] == cat]
            if not catalogue:
                return {"status": "error", "agent": self.name,
                        "message": f"No catalogue items in category `{cat}`."}

        n = rng.randint(3, min(6, len(catalogue)))
        items = rng.sample(catalogue, k=n)
        reqs = []
        for i, (desc, c, base_value, lead) in enumerate(items):
            qty = rng.randint(2, 25)
            value = round(base_value * qty * rng.uniform(0.8, 1.2), 2)
            reqs.append({
                "requisition_id": f"REQ-{seed % 1_000_000:06d}-{i+1}",
                "description": desc,
                "category": c,
                "quantity": qty,
                "estimated_value_usd": value,
                "expected_lead_time_days": lead,
                "needed_by_utc": (datetime.utcnow() + timedelta(days=rng.randint(20, horizon))).isoformat() + "Z",
                "urgency": "critical" if lead < 30 else "standard",
            })

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Built {len(reqs)} requisition(s) from `{source}`.",
            "data": {
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
                "source_plan": source,
                "horizon_days": horizon,
                "requisitions": reqs,
                "total_value_usd": round(sum(r["estimated_value_usd"] for r in reqs), 2),
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(DemandSignalRequisitionAgent().perform(source_plan="maintenance_plan", horizon_days=90), indent=2))
