"""Crew Acceptance Agent — Energy Utilities.

Captures on-site safety brief and individual crew-member acceptance signatures from the mobile app before work starts.

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


class CrewAcceptanceAgent(BasicAgent):
    def __init__(self):
        self.name = "CrewAcceptanceAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Captures on-site safety-brief acknowledgement and per-crew-member "
                "acceptance signatures. Returns a time-stamped acceptance record."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "permit_request_id": {"type": "string"},
                    "crew_member_ids": {"type": "array", "items": {"type": "string"}},
                    "brief_topics_covered": {"type": "array", "items": {"type": "string"}},
                    "all_present": {"type": "boolean"},
                },
                "required": ["permit_request_id", "crew_member_ids"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        if not kwargs.get("permit_request_id") or not kwargs.get("crew_member_ids"):
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `permit_request_id` and `crew_member_ids` (list)."}

        members = kwargs["crew_member_ids"]
        if not isinstance(members, list) or not members:
            return {"status": "error", "agent": self.name,
                    "message": "`crew_member_ids` must be a non-empty list."}

        now = datetime.utcnow()
        ack = []
        for i, mid in enumerate(members):
            ack.append({
                "crew_member_id": mid,
                "ack_utc": (now + timedelta(seconds=i * 30)).isoformat() + "Z",
                "signature_hash": hashlib.sha256(f"{mid}|{kwargs['permit_request_id']}".encode()).hexdigest()[:12],
            })

        topics = kwargs.get("brief_topics_covered") or [
            "Isolation confirmed", "PPE check", "Emergency contacts", "Site hazards"
        ]
        acceptance_status = "accepted" if kwargs.get("all_present", True) else "incomplete_attendance"

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Captured acceptance from {len(members)} crew member(s).",
            "data": {
                "permit_request_id": kwargs["permit_request_id"],
                "acceptance_status": acceptance_status,
                "brief_topics_covered": topics,
                "acknowledgements": ack,
                "brief_utc": now.isoformat() + "Z",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(CrewAcceptanceAgent().perform(
        permit_request_id="PRQ-000123", crew_member_ids=["EMP-101", "EMP-102", "EMP-103"]
    ), indent=2))
