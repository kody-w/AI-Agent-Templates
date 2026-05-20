"""Sanctions Screening Agent — Financial Services.

Screens payment parties (debtor / creditor / ordering customer) against OFAC, HMT and EU consolidated lists. Synthetic match probability.

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


class SanctionsScreeningAgent(BasicAgent):
    def __init__(self):
        self.name = "SanctionsScreeningAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Screens payment parties against OFAC / HMT / EU sanctions lists. "
                "Returns match decisions and recommended action."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "payment_reference": {"type": "string"},
                    "parties": {
                        "type": "array",
                        "description": "List of objects: {role, party_ref_hash}. NO real names.",
                        "items": {"type": "object"},
                    },
                    "lists": {
                        "type": "array",
                        "items": {"type": "string", "enum": ["OFAC", "HMT", "EU"]},
                    },
                },
                "required": ["payment_reference", "parties"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        if not kwargs.get("payment_reference") or not kwargs.get("parties"):
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `payment_reference` and `parties` (list)."}

        if not isinstance(kwargs["parties"], list) or not kwargs["parties"]:
            return {"status": "error", "agent": self.name,
                    "message": "`parties` must be a non-empty list."}

        lists = kwargs.get("lists") or ["OFAC", "HMT", "EU"]
        results = []
        for p in kwargs["parties"]:
            ref = p.get("party_ref_hash") or hashlib.sha256(str(p).encode()).hexdigest()[:12]
            seed = _stable_seed(ref, *lists)
            rng = random.Random(seed)
            score = round(rng.random(), 4)
            hit = score > 0.97
            results.append({
                "role": p.get("role", "party"),
                "party_ref_hash": ref,
                "lists_checked": lists,
                "match_score": score,
                "hit": hit,
                "decision": "hold_for_review" if hit else "clear",
            })

        any_hit = any(r["hit"] for r in results)
        return {
            "status": "success",
            "agent": self.name,
            "message": f"Screened {len(results)} party/parties: {'HIT' if any_hit else 'all clear'}.",
            "data": {
                "payment_reference": kwargs["payment_reference"],
                "lists_checked": lists,
                "parties": results,
                "overall_decision": "hold_for_review" if any_hit else "release_eligible",
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(SanctionsScreeningAgent().perform(
        payment_reference="PMT-1",
        parties=[{"role": "debtor", "party_ref_hash": "ab12cd34"}, {"role": "creditor", "party_ref_hash": "ef56gh78"}],
    ), indent=2))
