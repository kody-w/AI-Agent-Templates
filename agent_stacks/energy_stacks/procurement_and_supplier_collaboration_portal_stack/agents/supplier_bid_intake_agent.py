"""Supplier Bid Intake Agent — Energy Utilities.

Receives supplier bid submissions for an RFQ and aggregates Copilot-assisted clarification Q&A. Synthetic.

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


class SupplierBidIntakeAgent(BasicAgent):
    def __init__(self):
        self.name = "SupplierBidIntakeAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Receives supplier bid submissions and aggregates clarification Q&A for an RFQ."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "rfq_id": {"type": "string"},
                    "shortlist": {"type": "array", "description": "Shortlist from RFQBuilderAgent."},
                    "category": {"type": "string"},
                },
                "required": ["rfq_id", "shortlist"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        if not kwargs.get("rfq_id") or not kwargs.get("shortlist"):
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `rfq_id` and `shortlist`."}

        rfq_id = kwargs["rfq_id"]
        shortlist = kwargs["shortlist"]
        if not isinstance(shortlist, list) or not shortlist:
            return {"status": "error", "agent": self.name,
                    "message": "`shortlist` must be a non-empty list."}

        bids = []
        queries = []
        for s in shortlist:
            sid = s.get("supplier_id")
            seed = _stable_seed("bid", rfq_id, sid)
            rng = random.Random(seed)
            base_price = round(rng.uniform(900_000, 2_400_000), 2)
            bids.append({
                "bid_id": f"BID-{seed % 1_000_000:06d}",
                "rfq_id": rfq_id,
                "supplier_id": sid,
                "price_usd": base_price,
                "lead_time_days": rng.randint(14, 90),
                "quality_certifications": rng.sample(["ISO9001", "ISO14001", "IEC60076"], k=rng.randint(1, 3)),
                "sustainability_score": round(rng.uniform(0.55, 0.95), 2),
                "submitted_utc": datetime.utcnow().isoformat() + "Z",
            })
            if rng.random() < 0.6:
                queries.append({
                    "query_id": f"Q-{seed % 1_000_000:06d}",
                    "supplier_id": sid,
                    "topic": rng.choice(["delivery_window", "spec_clarification", "payment_terms"]),
                    "status": "answered",
                })

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Intook {len(bids)} bid(s) and {len(queries)} clarification(s).",
            "data": {
                "rfq_id": rfq_id,
                "category": kwargs.get("category"),
                "bids": bids,
                "queries": queries,
                "intake_closed_utc": (datetime.utcnow() + timedelta(days=14)).isoformat() + "Z",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(SupplierBidIntakeAgent().perform(
        rfq_id="RFQ-100001", shortlist=[{"supplier_id": "SUP-CABLE-A"}, {"supplier_id": "SUP-CABLE-B"}],
    ), indent=2))
