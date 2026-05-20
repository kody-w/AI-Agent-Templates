"""Payments Analytics Agent — Financial Services.

Computes operational KPIs across rails: volumes, STP rate, exception rate, average cycle time, scheme-compliance metrics.

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


class PaymentsAnalyticsAgent(BasicAgent):
    def __init__(self):
        self.name = "PaymentsAnalyticsAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Operational KPIs across rails: volumes, STP rate, exception rate, "
                "scheme-compliance metrics."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "window_days": {"type": "integer"},
                    "rails": {"type": "array", "items": {"type": "string", "enum": RAILS}},
                },
                "required": [],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        window = int(kwargs.get("window_days") or 1)
        rails = kwargs.get("rails") or RAILS
        seed = _stable_seed("payments_kpi", window, *rails)
        rng = random.Random(seed)

        by_rail = []
        total_vol = 0
        total_value = 0.0
        total_excs = 0
        for rail in rails:
            r = random.Random(_stable_seed(rail, window))
            vol = r.randint(15_000, 240_000) * max(1, window)
            value = round(vol * r.uniform(1_500, 80_000), 2)
            stp = round(r.uniform(0.86, 0.995), 4)
            excs = int(vol * (1 - stp))
            by_rail.append({
                "rail": rail,
                "volume": vol,
                "value_total": value,
                "stp_rate": stp,
                "exception_count": excs,
                "avg_cycle_seconds": int(r.uniform(2, 60) * 60),
                "scheme_compliance_pct": round(r.uniform(98.5, 99.99), 2),
            })
            total_vol += vol
            total_value += value
            total_excs += excs

        return {
            "status": "success",
            "agent": self.name,
            "message": f"KPIs computed over {window} day(s) across {len(rails)} rail(s).",
            "data": {
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
                "window_days": window,
                "totals": {
                    "volume": total_vol,
                    "value_total": total_value,
                    "exceptions": total_excs,
                    "stp_rate": round(1 - total_excs / max(1, total_vol), 4),
                },
                "by_rail": by_rail,
                "data_quality": "synthetic; deterministic per (window, rails)",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(PaymentsAnalyticsAgent().perform(window_days=1), indent=2))
