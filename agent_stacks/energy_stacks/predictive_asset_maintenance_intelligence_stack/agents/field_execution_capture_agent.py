"""Field Execution Capture Agent — Energy Utilities.

Captures and structures field-execution outcomes from a Power Apps mobile-style
form: actual hours, completion status, findings, photos count, quality flags,
and parts-consumed-vs-planned. Produces the JSON that closes out the WO and
feeds the asset register write-back.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from agents.basic_agent import BasicAgent
from datetime import datetime


VALID_COMPLETION = {"completed", "partial", "deferred", "escalated"}
VALID_QUALITY = {"pass", "pass_with_observations", "fail"}


class FieldExecutionCaptureAgent(BasicAgent):
    def __init__(self):
        self.name = "FieldExecutionCaptureAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Captures and structures field-execution outcomes from the "
                "Power Apps mobile form. Produces the closeout JSON that "
                "updates the WO and feeds the asset register."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "work_order_id": {"type": "string", "description": "WO identifier from MaintenanceWorkOrderAgent."},
                    "asset_id": {"type": "string", "description": "Asset under maintenance."},
                    "crew_id": {"type": "string", "description": "Crew identifier."},
                    "started_utc": {"type": "string", "description": "ISO timestamp."},
                    "completed_utc": {"type": "string", "description": "ISO timestamp."},
                    "completion_status": {
                        "type": "string",
                        "enum": list(VALID_COMPLETION),
                        "description": "Disposition.",
                    },
                    "actual_hours": {"type": "number", "description": "Hours on tools."},
                    "findings": {"type": "array", "items": {"type": "string"}, "description": "Free-text findings."},
                    "photos_count": {"type": "integer", "description": "Photos captured."},
                    "quality_check": {"type": "string", "enum": list(VALID_QUALITY)},
                    "parts_consumed": {
                        "type": "array",
                        "description": "List of {material, qty} consumed in the field.",
                    },
                    "next_action": {"type": "string", "description": "Recommended next action."},
                },
                "required": ["work_order_id", "asset_id", "completion_status"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        wo = kwargs.get("work_order_id")
        asset = kwargs.get("asset_id")
        completion = kwargs.get("completion_status")

        missing = [k for k, v in {
            "work_order_id": wo,
            "asset_id": asset,
            "completion_status": completion,
        }.items() if not v]
        if missing:
            return {
                "status": "needs_input",
                "agent": self.name,
                "message": f"Missing required field(s): {', '.join(missing)}.",
            }
        if completion not in VALID_COMPLETION:
            return {
                "status": "error",
                "agent": self.name,
                "message": f"completion_status must be one of {sorted(VALID_COMPLETION)}.",
            }

        quality = kwargs.get("quality_check")
        if quality and quality not in VALID_QUALITY:
            return {
                "status": "error",
                "agent": self.name,
                "message": f"quality_check must be one of {sorted(VALID_QUALITY)}.",
            }

        capture = {
            "capture_id": f"FC-{abs(hash(wo)) % 10_000_000:07d}",
            "work_order_id": wo,
            "asset_id": asset,
            "crew_id": kwargs.get("crew_id"),
            "started_utc": kwargs.get("started_utc"),
            "completed_utc": kwargs.get("completed_utc") or datetime.utcnow().isoformat() + "Z",
            "completion_status": completion,
            "actual_hours": kwargs.get("actual_hours"),
            "findings": kwargs.get("findings") or [],
            "photos_count": int(kwargs.get("photos_count") or 0),
            "quality_check": quality or "pass",
            "parts_consumed": kwargs.get("parts_consumed") or [],
            "next_action": kwargs.get("next_action"),
            "source_system": "Power Apps Mobile",
            "ready_for_writeback": completion in {"completed", "partial"},
        }

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Captured execution for {wo}.",
            "data": capture,
        }


if __name__ == "__main__":
    import json
    out = FieldExecutionCaptureAgent().perform(
        work_order_id="WO-ABCDEF0123",
        asset_id="AST-00001",
        crew_id="CREW-TX-09",
        completion_status="completed",
        actual_hours=4.5,
        findings=["Oil DGA elevated but stable", "No external leaks"],
        photos_count=11,
        quality_check="pass_with_observations",
        parts_consumed=[{"material": "Oil sample kit", "qty": 1}],
        next_action="Retest in 30 days",
    )
    print(json.dumps(out, indent=2))
