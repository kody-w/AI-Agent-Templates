"""Pre-Release Fraud Scorer Agent — Financial Services.

Scores transaction-level fraud risk before release. Domain-shaped heuristic using amount, beneficiary novelty, rail and time-of-day signals.

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


class PreReleaseFraudScorerAgent(BasicAgent):
    def __init__(self):
        self.name = "PreReleaseFraudScorerAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Scores fraud risk pre-release using amount, beneficiary novelty, rail "
                "and time-of-day signals. Returns score + driver list."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "payment_reference": {"type": "string"},
                    "amount": {"type": "number"},
                    "rail": {"type": "string", "enum": RAILS},
                    "beneficiary_new_to_originator": {"type": "boolean"},
                    "originator_avg_amount": {"type": "number"},
                    "submitted_hour_local": {"type": "integer", "description": "0-23"},
                },
                "required": ["payment_reference", "amount", "rail"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        for k in ("payment_reference", "amount", "rail"):
            if kwargs.get(k) in (None, ""):
                return {"status": "needs_input", "agent": self.name,
                        "message": f"Missing `{k}`."}

        amt = float(kwargs["amount"])
        rail = kwargs["rail"]
        avg = float(kwargs.get("originator_avg_amount") or 0)
        novelty = bool(kwargs.get("beneficiary_new_to_originator", False))
        hr = int(kwargs.get("submitted_hour_local") or 12)

        drivers = []
        score = 0.0
        if avg > 0 and amt > 5 * avg:
            score += 0.30; drivers.append("Amount >5x originator avg")
        if novelty:
            score += 0.25; drivers.append("First-time beneficiary")
        if hr < 5 or hr > 22:
            score += 0.15; drivers.append("Out-of-hours submission")
        if rail == "CHAPS" and amt > 1_000_000:
            score += 0.10; drivers.append("Large-value CHAPS")

        score = round(min(0.99, score + 0.05), 3)
        band = "Low" if score < 0.30 else "Medium" if score < 0.65 else "High"
        action = "release" if band == "Low" else "review" if band == "Medium" else "block_pending_review"

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Risk {band} ({score}).",
            "data": {
                "payment_reference": kwargs["payment_reference"],
                "fraud_score": score,
                "risk_band": band,
                "drivers": drivers or ["No notable risk signals"],
                "recommended_action": action,
                "model": "rule-based-v1 (heuristic, domain-shaped)",
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(PreReleaseFraudScorerAgent().perform(
        payment_reference="PMT-1", amount=2_500_000, rail="CHAPS",
        beneficiary_new_to_originator=True, originator_avg_amount=50_000, submitted_hour_local=23
    ), indent=2))
