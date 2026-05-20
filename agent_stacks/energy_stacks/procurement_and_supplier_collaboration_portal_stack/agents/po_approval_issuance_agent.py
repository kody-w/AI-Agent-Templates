"""PO Approval Issuance Agent — Energy Utilities.

Drafts a purchase order from the recommended award, routes for internal approval and issues to the supplier when approved. Pending_review by design.

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


class POApprovalIssuanceAgent(BasicAgent):
    def __init__(self):
        self.name = "POApprovalIssuanceAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Drafts and routes a purchase order based on the recommended award. "
                "Status is `pending_review` until human approval."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "rfq_id": {"type": "string"},
                    "recommended_award": {"type": "object"},
                    "requisition": {"type": "object"},
                },
                "required": ["rfq_id", "recommended_award"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        if not kwargs.get("rfq_id") or not kwargs.get("recommended_award"):
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `rfq_id` and `recommended_award`."}

        award = kwargs["recommended_award"]
        rfq_id = kwargs["rfq_id"]
        seed = _stable_seed("po", rfq_id, award.get("supplier_id", ""))
        po_id = f"PO-{seed % 1_000_000:06d}"

        value = float(award.get("price_usd", 0))
        if value >= 5_000_000:
            approver = "CFO"; sla_hours = 48
        elif value >= 1_000_000:
            approver = "Procurement Director"; sla_hours = 24
        elif value >= 250_000:
            approver = "Category Manager"; sla_hours = 12
        else:
            approver = "Buyer"; sla_hours = 4

        req = kwargs.get("requisition") or {}
        return {
            "status": "success",
            "agent": self.name,
            "message": f"Draft {po_id} routed to {approver}.",
            "data": {
                "purchase_order_id": po_id,
                "rfq_id": rfq_id,
                "supplier_id": award.get("supplier_id"),
                "value_usd": value,
                "lead_time_days": award.get("lead_time_days"),
                "requisition_id": req.get("requisition_id"),
                "approval_status": "pending_review",
                "approver": approver,
                "deadline_utc": (datetime.utcnow() + timedelta(hours=sla_hours)).isoformat() + "Z",
                "supplier_ack_status": "awaiting_release",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(POApprovalIssuanceAgent().perform(
        rfq_id="RFQ-100001",
        recommended_award={"supplier_id": "SUP-CABLE-A", "price_usd": 1_200_000, "lead_time_days": 28},
    ), indent=2))
