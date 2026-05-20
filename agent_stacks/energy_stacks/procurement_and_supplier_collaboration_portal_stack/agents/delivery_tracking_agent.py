"""Delivery Tracking Agent — Energy Utilities.

Tracks supplier ASN (Advance Shipment Notice) and goods movement against PO. Flags deviations against committed delivery schedule.

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


class DeliveryTrackingAgent(BasicAgent):
    def __init__(self):
        self.name = "DeliveryTrackingAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Tracks ASN + delivery against PO. Flags deviations vs committed "
                "schedule."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "purchase_order_id": {"type": "string"},
                    "expected_delivery_utc": {"type": "string"},
                },
                "required": ["purchase_order_id"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        if not kwargs.get("purchase_order_id"):
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `purchase_order_id`."}

        po_id = kwargs["purchase_order_id"]
        seed = _stable_seed("delivery", po_id)
        rng = random.Random(seed)

        stages = ["po_issued", "supplier_ack", "in_production", "asn_received", "in_transit", "delivered", "gr_completed"]
        idx = rng.randint(1, len(stages) - 1)
        current = stages[idx]

        slip_days = rng.choice([0, 0, 0, 1, 3, -1])
        deviation = "on_track" if slip_days <= 0 else "delayed"

        return {
            "status": "success",
            "agent": self.name,
            "message": f"{po_id}: {current} ({deviation}).",
            "data": {
                "purchase_order_id": po_id,
                "current_stage": current,
                "stage_history": stages[: idx + 1],
                "slip_days": slip_days,
                "deviation_flag": deviation,
                "expected_delivery_utc": kwargs.get("expected_delivery_utc"),
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(DeliveryTrackingAgent().perform(purchase_order_id="PO-123456"), indent=2))
