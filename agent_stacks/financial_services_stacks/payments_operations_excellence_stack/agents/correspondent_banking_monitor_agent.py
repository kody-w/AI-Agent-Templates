"""Correspondent Banking Monitor Agent — Financial Services.

Monitors correspondent-bank limits and nostro-funding utilisation. Flags when a correspondent is approaching its credit / liquidity limit.

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


class CorrespondentBankingMonitorAgent(BasicAgent):
    def __init__(self):
        self.name = "CorrespondentBankingMonitorAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Monitors correspondent-bank limit / nostro-funding utilisation. "
                "Flags approaching breaches."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "correspondent_id": {"type": "string"},
                    "currency": {"type": "string"},
                },
                "required": ["correspondent_id"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        if not kwargs.get("correspondent_id"):
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `correspondent_id`."}

        cid = kwargs["correspondent_id"]
        seed = _stable_seed("corr", cid)
        rng = random.Random(seed)

        credit_limit = round(rng.uniform(50_000_000, 500_000_000), 2)
        credit_used = round(credit_limit * rng.uniform(0.4, 0.97), 2)
        nostro_balance = round(rng.uniform(5_000_000, 80_000_000), 2)
        intraday_drawdown = round(rng.uniform(0.05, 0.70), 2)

        util_pct = round(100 * credit_used / credit_limit, 1)
        alert = "OK"
        if util_pct >= 95:
            alert = "BREACH_IMMINENT"
        elif util_pct >= 85:
            alert = "WATCH"

        return {
            "status": "success",
            "agent": self.name,
            "message": f"{cid}: utilisation {util_pct}% — {alert}.",
            "data": {
                "correspondent_id": cid,
                "currency": kwargs.get("currency") or "USD",
                "credit_limit": credit_limit,
                "credit_used": credit_used,
                "utilisation_pct": util_pct,
                "nostro_balance": nostro_balance,
                "intraday_drawdown_pct": intraday_drawdown * 100,
                "alert_level": alert,
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(CorrespondentBankingMonitorAgent().perform(correspondent_id="CORR-USD-001"), indent=2))
