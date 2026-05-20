"""Payment Exception Repair Agent — Financial Services.

Diagnoses why a payment failed and proposes a repair playbook. Operates on validation_result + scheme codes, never modifies payments.

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


REPAIR_PLAYBOOK = {
    "AMOUNT_OUT_OF_RANGE":  ["Split into multiple payments below rail ceiling", "Re-route via SWIFT correspondent"],
    "CURRENCY_NOT_SUPPORTED": ["Re-rail to a scheme that supports the currency", "FX conversion before rail submission"],
    "IBAN_REQUIRED":         ["Request IBAN from originator", "Reject with NACK to upstream system"],
    "BIC_MALFORMED":         ["Look up correct BIC via SWIFTRef", "Reject with NACK"],
    "INSUFFICIENT_COVER":    ["Request nostro funding top-up", "Queue until funding available"],
    "DUPLICATE_REFERENCE":   ["Reject as duplicate", "Confirm with originator before resubmit"],
}


class PaymentExceptionRepairAgent(BasicAgent):
    def __init__(self):
        self.name = "PaymentExceptionRepairAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Diagnoses payment-failure root cause and suggests a repair playbook. "
                "Never modifies the payment — analyst confirms."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "payment_reference": {"type": "string"},
                    "failure_codes": {"type": "array", "items": {"type": "string"}},
                    "rail": {"type": "string", "enum": RAILS},
                },
                "required": ["payment_reference", "failure_codes"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        if not kwargs.get("payment_reference") or not kwargs.get("failure_codes"):
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `payment_reference` and `failure_codes`."}

        codes = kwargs["failure_codes"]
        if not isinstance(codes, list) or not codes:
            return {"status": "error", "agent": self.name,
                    "message": "`failure_codes` must be a non-empty list."}

        suggestions = []
        unknown = []
        for code in codes:
            steps = REPAIR_PLAYBOOK.get(code)
            if steps:
                suggestions.append({"code": code, "repair_steps": steps})
            else:
                unknown.append(code)

        priority = "P1" if any(c in {"INSUFFICIENT_COVER", "DUPLICATE_REFERENCE"} for c in codes) else "P2"
        return {
            "status": "success",
            "agent": self.name,
            "message": f"Diagnosed {len(codes)} failure(s); {len(unknown)} unknown.",
            "data": {
                "payment_reference": kwargs["payment_reference"],
                "rail": kwargs.get("rail"),
                "root_causes": suggestions,
                "unknown_codes": unknown,
                "priority": priority,
                "next_action": "queue_for_analyst_repair",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(PaymentExceptionRepairAgent().perform(
        payment_reference="PMT-1", failure_codes=["IBAN_REQUIRED", "BIC_MALFORMED"], rail="SEPA"
    ), indent=2))
