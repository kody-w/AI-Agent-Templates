"""Permit Request Capture Agent — Energy Utilities.

Captures a permit-to-work request from the Power Apps mobile form: substation, asset, work type, requested window, crew. Produces a structured permit-request envelope ready for risk-assessment.

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


class PermitRequestCaptureAgent(BasicAgent):
    def __init__(self):
        self.name = "PermitRequestCaptureAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Captures a permit-to-work request from the Power Apps mobile form "
                "(substation, asset, work type, requested window, crew). Returns a "
                "structured permit request ready for risk assessment."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "substation": {"type": "string", "description": "Substation code, e.g. SUB-12."},
                    "asset_id": {"type": "string", "description": "Asset identifier the work targets."},
                    "asset_class": {"type": "string", "enum": ["transformer", "switchgear", "underground_cable", "overhead_line"]},
                    "work_type": {"type": "string", "description": "e.g. overhaul, replacement, inspection, vegetation_management."},
                    "requested_start_utc": {"type": "string", "description": "ISO timestamp."},
                    "requested_duration_hours": {"type": "number"},
                    "crew_id": {"type": "string"},
                    "crew_size": {"type": "integer"},
                },
                "required": ["substation", "asset_id", "work_type"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        for required in ("substation", "asset_id", "work_type"):
            if not kwargs.get(required):
                return {
                    "status": "needs_input",
                    "agent": self.name,
                    "message": f"Missing required field `{required}`. No request fabricated.",
                }

        substation = kwargs["substation"]
        asset_id = kwargs["asset_id"]
        seed = _stable_seed(substation, asset_id, kwargs["work_type"])
        rng = random.Random(seed)
        prq_id = f"PRQ-{seed % 1_000_000:06d}"

        completeness = []
        for hint in ("requested_start_utc", "requested_duration_hours", "crew_id", "crew_size", "asset_class"):
            if not kwargs.get(hint):
                completeness.append(hint)

        request = {
            "permit_request_id": prq_id,
            "substation": substation,
            "asset_id": asset_id,
            "asset_class": kwargs.get("asset_class") or rng.choice(["transformer", "switchgear", "underground_cable", "overhead_line"]),
            "work_type": kwargs["work_type"],
            "requested_start_utc": kwargs.get("requested_start_utc") or (datetime.utcnow() + timedelta(days=2)).isoformat() + "Z",
            "requested_duration_hours": float(kwargs.get("requested_duration_hours") or 4.0),
            "crew_id": kwargs.get("crew_id") or f"CREW-{rng.randint(100, 999)}",
            "crew_size": int(kwargs.get("crew_size") or 3),
            "status": "captured",
            "captured_utc": datetime.utcnow().isoformat() + "Z",
        }
        return {
            "status": "success",
            "agent": self.name,
            "message": f"Captured permit request {prq_id}.",
            "data": {
                "permit_request": request,
                "missing_optional_fields": completeness,
                "next_stage": "risk_assessment",
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(PermitRequestCaptureAgent().perform(
        substation="SUB-12", asset_id="AST-00042", work_type="transformer_overhaul"
    ), indent=2))
