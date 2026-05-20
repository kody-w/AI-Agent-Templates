"""Isolation Plan Validator Agent — Energy Utilities.

Compares the RAMS against the published asset isolation plan and flags any missing isolation points before authorisation.

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


class IsolationPlanValidatorAgent(BasicAgent):
    def __init__(self):
        self.name = "IsolationPlanValidatorAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Validates the RAMS against the asset isolation plan. Flags missing "
                "or out-of-date isolation points."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "permit_request_id": {"type": "string"},
                    "asset_id": {"type": "string"},
                    "rams_method_steps": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Method statement steps from RiskAssessmentAgent.",
                    },
                    "isolation_plan_id": {"type": "string"},
                },
                "required": ["permit_request_id", "asset_id"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        if not kwargs.get("permit_request_id") or not kwargs.get("asset_id"):
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `permit_request_id` and `asset_id`."}

        asset_id = kwargs["asset_id"]
        seed = _stable_seed("isolation", asset_id)
        rng = random.Random(seed)

        # Synthetic published isolation points for this asset
        canonical_points = [
            {"id": f"ISO-{asset_id}-A", "type": "primary_disconnector", "state_required": "open"},
            {"id": f"ISO-{asset_id}-B", "type": "earth_switch", "state_required": "closed"},
            {"id": f"ISO-{asset_id}-C", "type": "lockout_padlock", "state_required": "applied"},
        ]
        if rng.random() < 0.5:
            canonical_points.append(
                {"id": f"ISO-{asset_id}-D", "type": "voltage_proving_point", "state_required": "tested"}
            )

        rams_steps = kwargs.get("rams_method_steps") or []
        rams_blob = " | ".join(rams_steps).lower()

        addressed = []
        missing = []
        for p in canonical_points:
            keyword = p["type"].split("_")[0]
            if keyword in rams_blob or "isolation" in rams_blob:
                addressed.append(p)
            else:
                missing.append(p)

        validation_status = "pass" if not missing else "fail"
        return {
            "status": "success",
            "agent": self.name,
            "message": f"Validation: {validation_status} ({len(missing)} missing).",
            "data": {
                "permit_request_id": kwargs["permit_request_id"],
                "isolation_plan_id": kwargs.get("isolation_plan_id") or f"IP-{asset_id}",
                "canonical_isolation_points": canonical_points,
                "addressed_points": addressed,
                "missing_points": missing,
                "validation_status": validation_status,
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(IsolationPlanValidatorAgent().perform(
        permit_request_id="PRQ-000123", asset_id="AST-00042",
        rams_method_steps=["Confirm isolation + voltage proving"]
    ), indent=2))
