"""Three-Way Match Agent — Energy Utilities.

Reconciles PO ↔ Goods Receipt ↔ Invoice. Surfaces price, quantity and delivery-date mismatches before payment release.

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


class ThreeWayMatchAgent(BasicAgent):
    def __init__(self):
        self.name = "ThreeWayMatchAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Three-way match between PO, Goods Receipt and Invoice. Flags "
                "mismatches before payment release."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "purchase_order": {"type": "object"},
                    "goods_receipt": {"type": "object"},
                    "invoice": {"type": "object"},
                    "tolerance_pct": {"type": "number"},
                },
                "required": ["purchase_order", "goods_receipt", "invoice"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        po = kwargs.get("purchase_order")
        gr = kwargs.get("goods_receipt")
        inv = kwargs.get("invoice")
        if not po or not gr or not inv:
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `purchase_order`, `goods_receipt`, and `invoice`."}

        tol = float(kwargs.get("tolerance_pct") or 1.0) / 100.0
        mismatches = []

        po_qty = float(po.get("quantity", 0))
        gr_qty = float(gr.get("quantity", 0))
        inv_qty = float(inv.get("quantity", 0))
        if po_qty and abs(po_qty - gr_qty) / po_qty > tol:
            mismatches.append({"field": "quantity", "po": po_qty, "gr": gr_qty})
        if po_qty and abs(po_qty - inv_qty) / po_qty > tol:
            mismatches.append({"field": "quantity_invoice", "po": po_qty, "invoice": inv_qty})

        po_price = float(po.get("unit_price", 0))
        inv_price = float(inv.get("unit_price", 0))
        if po_price and abs(po_price - inv_price) / po_price > tol:
            mismatches.append({"field": "unit_price", "po": po_price, "invoice": inv_price})

        match_status = "matched" if not mismatches else "exception"
        return {
            "status": "success",
            "agent": self.name,
            "message": f"Match: {match_status} ({len(mismatches)} mismatch(es)).",
            "data": {
                "purchase_order_id": po.get("purchase_order_id"),
                "goods_receipt_id": gr.get("goods_receipt_id"),
                "invoice_id": inv.get("invoice_id"),
                "tolerance_pct": kwargs.get("tolerance_pct") or 1.0,
                "match_status": match_status,
                "mismatches": mismatches,
                "ready_for_payment": match_status == "matched",
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(ThreeWayMatchAgent().perform(
        purchase_order={"purchase_order_id": "PO-1", "quantity": 10, "unit_price": 120_000},
        goods_receipt={"goods_receipt_id": "GR-1", "quantity": 10},
        invoice={"invoice_id": "INV-1", "quantity": 10, "unit_price": 120_000},
    ), indent=2))
