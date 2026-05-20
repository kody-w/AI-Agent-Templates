"""Permit Authorisation Workflow Agent — Energy Utilities.

Routes the permit through digital sign-off stages (Person-in-Charge → Authorised Person → Manager) with deadlines.

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


STAGES = [
    {"stage": "PIC_review", "role": "Person In Charge", "sla_hours": 4},
    {"stage": "AP_authorise", "role": "Authorised Person", "sla_hours": 6},
    {"stage": "Manager_endorse", "role": "Site Manager", "sla_hours": 12},
    {"stage": "Issued", "role": "Permit Office", "sla_hours": 1},
]


class PermitAuthorisationWorkflowAgent(BasicAgent):
    def __init__(self):
        self.name = "PermitAuthorisationWorkflowAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Advances the permit through staged digital sign-offs. Returns the "
                "next stage, accountable role, and deadline."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "permit_request_id": {"type": "string"},
                    "current_stage": {"type": "string", "description": "Stage just completed."},
                    "validation_status": {"type": "string", "enum": ["pass", "fail"]},
                    "residual_risk_score": {"type": "number"},
                },
                "required": ["permit_request_id"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        if not kwargs.get("permit_request_id"):
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `permit_request_id`."}

        if (kwargs.get("validation_status") or "pass") == "fail":
            return {
                "status": "blocked",
                "agent": self.name,
                "message": "Permit blocked: isolation validation failed. Return to RAMS revision.",
                "data": {
                    "permit_request_id": kwargs["permit_request_id"],
                    "blocked_at_stage": "PIC_review",
                    "return_to": "risk_assessment",
                },
            }

        current = kwargs.get("current_stage")
        try:
            idx = next(i for i, s in enumerate(STAGES) if s["stage"] == current)
            next_idx = idx + 1
        except StopIteration:
            next_idx = 0

        if next_idx >= len(STAGES):
            return {
                "status": "success",
                "agent": self.name,
                "message": "Permit fully authorised and issued.",
                "data": {
                    "permit_request_id": kwargs["permit_request_id"],
                    "workflow_complete": True,
                    "final_status": "Issued",
                },
            }

        nxt = STAGES[next_idx]
        deadline = (datetime.utcnow() + timedelta(hours=nxt["sla_hours"])).isoformat() + "Z"
        risk = float(kwargs.get("residual_risk_score") or 0.4)
        priority = "P1" if risk > 0.7 else "P2" if risk > 0.4 else "P3"

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Routed to {nxt['role']} ({nxt['stage']}).",
            "data": {
                "permit_request_id": kwargs["permit_request_id"],
                "next_stage": nxt["stage"],
                "accountable_role": nxt["role"],
                "deadline_utc": deadline,
                "sla_hours": nxt["sla_hours"],
                "priority": priority,
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(PermitAuthorisationWorkflowAgent().perform(
        permit_request_id="PRQ-000123", validation_status="pass", residual_risk_score=0.5
    ), indent=2))
