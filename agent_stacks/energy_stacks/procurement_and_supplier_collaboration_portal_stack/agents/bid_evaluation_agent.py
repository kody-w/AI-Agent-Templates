"""Bid Evaluation Agent — Energy Utilities.

Scores bids across weighted criteria: price, lead time, quality, sustainability. Returns ranked bids and a recommended award.

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


DEFAULT_WEIGHTS = {"price": 0.40, "lead_time": 0.20, "quality": 0.25, "sustainability": 0.15}


class BidEvaluationAgent(BasicAgent):
    def __init__(self):
        self.name = "BidEvaluationAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Scores bids across weighted price / lead-time / quality / sustainability. "
                "Returns ranked bids and recommended award."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "bids": {"type": "array", "description": "Bids from SupplierBidIntakeAgent."},
                    "weights": {"type": "object", "description": "Override default weights."},
                },
                "required": ["bids"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        bids = kwargs.get("bids")
        if not bids:
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `bids` (list)."}
        if not isinstance(bids, list) or not bids:
            return {"status": "error", "agent": self.name,
                    "message": "`bids` must be a non-empty list."}

        w = {**DEFAULT_WEIGHTS, **(kwargs.get("weights") or {})}
        total_w = sum(w.values()) or 1.0
        w = {k: v / total_w for k, v in w.items()}

        prices = [float(b["price_usd"]) for b in bids]
        lts = [float(b["lead_time_days"]) for b in bids]
        p_min, p_max = min(prices), max(prices) or 1.0
        l_min, l_max = min(lts), max(lts) or 1.0

        def norm(x, lo, hi, invert=True):
            if hi == lo:
                return 1.0
            n = (x - lo) / (hi - lo)
            return 1.0 - n if invert else n

        scored = []
        for b in bids:
            price_score = norm(float(b["price_usd"]), p_min, p_max, invert=True)
            lt_score = norm(float(b["lead_time_days"]), l_min, l_max, invert=True)
            q_score = min(1.0, len(b.get("quality_certifications", [])) / 3)
            s_score = float(b.get("sustainability_score", 0))
            total = round(
                price_score * w["price"]
                + lt_score * w["lead_time"]
                + q_score * w["quality"]
                + s_score * w["sustainability"], 4
            )
            scored.append({
                "bid_id": b.get("bid_id"),
                "supplier_id": b.get("supplier_id"),
                "price_usd": float(b["price_usd"]),
                "lead_time_days": float(b["lead_time_days"]),
                "score_breakdown": {"price": price_score, "lead_time": lt_score,
                                    "quality": q_score, "sustainability": s_score},
                "total_score": total,
            })

        scored.sort(key=lambda x: x["total_score"], reverse=True)
        return {
            "status": "success",
            "agent": self.name,
            "message": f"Scored {len(scored)} bid(s).",
            "data": {
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
                "weights_used": w,
                "ranked_bids": scored,
                "recommended_award": scored[0] if scored else None,
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(BidEvaluationAgent().perform(bids=[
        {"bid_id": "BID-1", "supplier_id": "S1", "price_usd": 1_000_000, "lead_time_days": 30,
         "quality_certifications": ["ISO9001"], "sustainability_score": 0.7},
        {"bid_id": "BID-2", "supplier_id": "S2", "price_usd": 1_200_000, "lead_time_days": 21,
         "quality_certifications": ["ISO9001", "ISO14001"], "sustainability_score": 0.85},
    ]), indent=2))
