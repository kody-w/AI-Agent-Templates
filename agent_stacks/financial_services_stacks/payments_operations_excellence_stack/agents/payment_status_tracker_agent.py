"""Payment Status Tracker Agent — Financial Services.

Returns the full lifecycle state of a payment by reference: ingestion, screening, repair, fraud, release, scheme ack, settlement. Synthetic.

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


RAILS = ["CHAPS", "FasterPayments", "SEPA", "SWIFT"]


STAGES = ["ingested", "validated", "screened", "fraud_checked", "released", "scheme_ack", "settled"]


class PaymentStatusTrackerAgent(BasicAgent):
    def __init__(self):
        self.name = "PaymentStatusTrackerAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Returns lifecycle state of a payment by reference: every stage with "
                "timestamps and current state."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "payment_reference": {"type": "string"},
                    "rail": {"type": "string", "enum": RAILS},
                },
                "required": ["payment_reference"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        if not kwargs.get("payment_reference"):
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `payment_reference`."}

        ref = kwargs["payment_reference"]
        seed = _stable_seed("trk", ref)
        rng = random.Random(seed)

        current_idx = rng.randint(2, len(STAGES) - 1)
        now = datetime.utcnow()
        history = []
        for i, stage in enumerate(STAGES[: current_idx + 1]):
            ts = now - timedelta(minutes=(current_idx - i) * rng.randint(2, 20))
            history.append({"stage": stage, "at_utc": ts.isoformat() + "Z"})

        current = STAGES[current_idx]
        eta = (now + timedelta(minutes=rng.randint(5, 240))).isoformat() + "Z" if current != "settled" else None
        return {
            "status": "success",
            "agent": self.name,
            "message": f"{ref} currently `{current}`.",
            "data": {
                "payment_reference": ref,
                "rail": kwargs.get("rail"),
                "current_state": current,
                "history": history,
                "eta_to_settlement_utc": eta,
                "as_of_utc": now.isoformat() + "Z",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(PaymentStatusTrackerAgent().perform(payment_reference="PMT-12345"), indent=2))
