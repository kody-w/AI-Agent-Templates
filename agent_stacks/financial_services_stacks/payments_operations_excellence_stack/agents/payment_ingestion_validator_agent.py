"""Payment Ingestion Validator Agent — Financial Services.

Validates an inbound payment against scheme rules for the chosen rail (CHAPS / Faster Payments / SEPA / SWIFT). Returns structured errors.

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


SCHEME_RULES = {
    "CHAPS":          {"max_amount": 10_000_000_000, "min_amount": 0.01, "currencies": ["GBP"], "iban_required": False},
    "FasterPayments": {"max_amount": 1_000_000,      "min_amount": 0.01, "currencies": ["GBP"], "iban_required": False},
    "SEPA":           {"max_amount": 999_999_999.99, "min_amount": 0.01, "currencies": ["EUR"], "iban_required": True},
    "SWIFT":          {"max_amount": 10_000_000_000, "min_amount": 0.01, "currencies": ["USD", "EUR", "GBP", "JPY", "CHF", "AUD"], "iban_required": False},
}


class PaymentIngestionValidatorAgent(BasicAgent):
    def __init__(self):
        self.name = "PaymentIngestionValidatorAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Validates a payment against scheme rules for the chosen rail "
                "(CHAPS / Faster Payments / SEPA / SWIFT)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "payment_reference": {"type": "string"},
                    "rail": {"type": "string", "enum": RAILS},
                    "amount": {"type": "number"},
                    "currency": {"type": "string"},
                    "debtor_bic": {"type": "string"},
                    "creditor_bic": {"type": "string"},
                    "creditor_iban": {"type": "string"},
                    "value_date": {"type": "string"},
                },
                "required": ["payment_reference", "rail", "amount", "currency"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        for k in ("payment_reference", "rail", "amount", "currency"):
            if kwargs.get(k) in (None, ""):
                return {"status": "needs_input", "agent": self.name,
                        "message": f"Missing `{k}`."}

        rail = kwargs["rail"]
        rules = SCHEME_RULES.get(rail)
        if not rules:
            return {"status": "error", "agent": self.name,
                    "message": f"Unknown rail `{rail}`."}

        errors = []
        if not (rules["min_amount"] <= float(kwargs["amount"]) <= rules["max_amount"]):
            errors.append({"code": "AMOUNT_OUT_OF_RANGE",
                           "detail": f"{rail} accepts {rules['min_amount']} – {rules['max_amount']}"})
        if kwargs["currency"] not in rules["currencies"]:
            errors.append({"code": "CURRENCY_NOT_SUPPORTED",
                           "detail": f"{rail} supports {rules['currencies']}"})
        if rules["iban_required"] and not kwargs.get("creditor_iban"):
            errors.append({"code": "IBAN_REQUIRED",
                           "detail": f"{rail} requires creditor IBAN"})
        for bic_field in ("debtor_bic", "creditor_bic"):
            v = kwargs.get(bic_field)
            if v and not (8 <= len(v) <= 11 and v.isalnum()):
                errors.append({"code": "BIC_MALFORMED", "detail": f"`{bic_field}` shape invalid"})

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Validation: {'pass' if not errors else 'fail'}.",
            "data": {
                "payment_reference": kwargs["payment_reference"],
                "rail": rail,
                "validation_result": "pass" if not errors else "fail",
                "errors": errors,
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(PaymentIngestionValidatorAgent().perform(
        payment_reference="PMT-1", rail="CHAPS", amount=12345.67, currency="GBP",
        debtor_bic="BANKGB22XXX", creditor_bic="BARCGB22"
    ), indent=2))
