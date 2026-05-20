"""Permit Clearance Agent — Energy Utilities.

Closes the permit on work completion: confirms personnel count, tools accounted for, work area left safe.

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


class PermitClearanceAgent(BasicAgent):
    def __init__(self):
        self.name = "PermitClearanceAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Closes a permit on work completion. Verifies personnel count, tools "
                "accounted, and area-safe status. Returns clearance envelope."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "permit_request_id": {"type": "string"},
                    "personnel_on_site_at_start": {"type": "integer"},
                    "personnel_on_site_at_close": {"type": "integer"},
                    "tools_issued": {"type": "integer"},
                    "tools_returned": {"type": "integer"},
                    "area_safe": {"type": "boolean"},
                    "work_complete": {"type": "boolean"},
                },
                "required": ["permit_request_id"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        if not kwargs.get("permit_request_id"):
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `permit_request_id`."}

        start = int(kwargs.get("personnel_on_site_at_start") or 0)
        end = int(kwargs.get("personnel_on_site_at_close") or 0)
        tools_out = int(kwargs.get("tools_issued") or 0)
        tools_in = int(kwargs.get("tools_returned") or 0)
        area_safe = bool(kwargs.get("area_safe", True))
        complete = bool(kwargs.get("work_complete", True))

        issues = []
        if start and end != start:
            issues.append(f"Personnel mismatch: {start} → {end}")
        if tools_out and tools_in != tools_out:
            issues.append(f"Tools mismatch: issued {tools_out}, returned {tools_in}")
        if not area_safe:
            issues.append("Area NOT confirmed safe")
        if not complete:
            issues.append("Work flagged as incomplete")

        clearance_status = "cleared" if not issues else "held_for_review"
        return {
            "status": "success",
            "agent": self.name,
            "message": f"Clearance: {clearance_status}.",
            "data": {
                "permit_request_id": kwargs["permit_request_id"],
                "clearance_status": clearance_status,
                "issues": issues,
                "closed_utc": datetime.utcnow().isoformat() + "Z",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(PermitClearanceAgent().perform(
        permit_request_id="PRQ-000123",
        personnel_on_site_at_start=3, personnel_on_site_at_close=3,
        tools_issued=12, tools_returned=12, area_safe=True, work_complete=True,
    ), indent=2))
