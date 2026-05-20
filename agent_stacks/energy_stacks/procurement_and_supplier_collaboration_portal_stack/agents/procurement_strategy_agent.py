"""Procurement Strategy Agent — Energy Utilities.

Recommends a procurement route per requisition (direct award / mini-comp / open tender) using value thresholds, category and urgency.

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


class ProcurementStrategyAgent(BasicAgent):
    def __init__(self):
        self.name = "ProcurementStrategyAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Recommends a procurement route for each requisition using value "
                "thresholds, category and urgency."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "requisitions": {
                        "type": "array",
                        "description": "Requisitions from DemandSignalRequisitionAgent.",
                    },
                    "direct_award_threshold_usd": {"type": "number"},
                    "mini_comp_threshold_usd": {"type": "number"},
                },
                "required": ["requisitions"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        reqs = kwargs.get("requisitions")
        if not reqs:
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `requisitions` (list)."}
        if not isinstance(reqs, list):
            return {"status": "error", "agent": self.name,
                    "message": "`requisitions` must be a list."}

        da = float(kwargs.get("direct_award_threshold_usd") or 250_000)
        mc = float(kwargs.get("mini_comp_threshold_usd") or 2_500_000)

        recos = []
        for r in reqs:
            val = float(r.get("estimated_value_usd") or 0)
            urgent = r.get("urgency") == "critical"
            if val <= da or (urgent and val <= da * 2):
                route = "direct_award"
                rationale = ("Below direct-award threshold" if val <= da
                             else "Urgent + within emergency framework")
            elif val <= mc:
                route = "mini_competition"
                rationale = "Mid-tier value; closed-list quick competition"
            else:
                route = "open_tender"
                rationale = "Above mini-comp threshold; open tender required"

            recos.append({
                "requisition_id": r.get("requisition_id"),
                "estimated_value_usd": val,
                "recommended_route": route,
                "rationale": rationale,
                "estimated_cycle_days": {"direct_award": 14, "mini_competition": 35, "open_tender": 75}[route],
            })

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Routed {len(recos)} requisition(s).",
            "data": {
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
                "thresholds": {"direct_award_usd": da, "mini_competition_usd": mc},
                "recommendations": recos,
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(ProcurementStrategyAgent().perform(requisitions=[
        {"requisition_id": "REQ-1", "estimated_value_usd": 80_000, "urgency": "standard"},
        {"requisition_id": "REQ-2", "estimated_value_usd": 5_500_000, "urgency": "standard"},
    ]), indent=2))
