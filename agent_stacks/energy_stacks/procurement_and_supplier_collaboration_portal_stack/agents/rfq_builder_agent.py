"""RFQ Builder Agent — Energy Utilities.

Builds an RFQ document and shortlists eligible suppliers by category, pre-qualification and on-time-delivery score.

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


CATEGORIES_TO_SUPPLIERS = {
    "cables":         ["SUP-CABLE-A", "SUP-CABLE-B", "SUP-CABLE-C"],
    "transformers":   ["SUP-XFMR-A", "SUP-XFMR-B"],
    "switchgear":     ["SUP-SWG-A", "SUP-SWG-B", "SUP-SWG-C"],
    "field_devices":  ["SUP-FLD-A", "SUP-FLD-B"],
    "conductors":     ["SUP-CON-A", "SUP-CON-B", "SUP-CON-C"],
    "structures":     ["SUP-STR-A", "SUP-STR-B"],
}


class RFQBuilderAgent(BasicAgent):
    def __init__(self):
        self.name = "RFQBuilderAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Builds an RFQ and shortlists eligible suppliers based on category "
                "and pre-qualification data."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "requisition": {"type": "object"},
                    "max_shortlist": {"type": "integer"},
                },
                "required": ["requisition"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        req = kwargs.get("requisition")
        if not req or not isinstance(req, dict) or not req.get("category"):
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `requisition` with at least `category` and `requisition_id`."}

        cat = req["category"]
        suppliers = CATEGORIES_TO_SUPPLIERS.get(cat) or []
        if not suppliers:
            return {"status": "error", "agent": self.name,
                    "message": f"No pre-qualified suppliers for category `{cat}`."}

        max_n = int(kwargs.get("max_shortlist") or 3)
        seed = _stable_seed("rfq", req.get("requisition_id", "x"), cat)
        rng = random.Random(seed)

        scored = []
        for s in suppliers:
            scored.append({
                "supplier_id": s,
                "otd_score": round(rng.uniform(0.70, 0.99), 3),
                "quality_score": round(rng.uniform(0.70, 0.99), 3),
                "framework_eligible": True,
            })
        scored.sort(key=lambda x: (x["otd_score"] + x["quality_score"]), reverse=True)
        shortlist = scored[:max_n]

        rfq_id = f"RFQ-{seed % 1_000_000:06d}"
        return {
            "status": "success",
            "agent": self.name,
            "message": f"Built {rfq_id} with {len(shortlist)} shortlisted supplier(s).",
            "data": {
                "rfq_id": rfq_id,
                "requisition_id": req.get("requisition_id"),
                "category": cat,
                "scope_summary": req.get("description", "Material supply"),
                "quantity": req.get("quantity"),
                "needed_by_utc": req.get("needed_by_utc"),
                "shortlist": shortlist,
                "issue_window_days": 14,
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(RFQBuilderAgent().perform(requisition={
        "requisition_id": "REQ-1", "category": "cables", "description": "MV cable replenishment",
        "quantity": 10, "needed_by_utc": "2026-08-01T00:00:00Z"
    }), indent=2))
