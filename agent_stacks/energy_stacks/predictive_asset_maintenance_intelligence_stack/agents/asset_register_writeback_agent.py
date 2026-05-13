"""Asset Register Write-back Agent — Energy Utilities.

Takes a field-execution capture (from FieldExecutionCaptureAgent) and stages
the resulting updates to the Asset Management System and the ERP fixed-asset
register: condition_band update, last_maintenance_date, useful-life
recalibration, and book-value adjustment hints for finance.

Emits a structured write-back envelope per target system. Does not actually
make the API calls — that's the integration runtime's job.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from agents.basic_agent import BasicAgent
from datetime import datetime


class AssetRegisterWritebackAgent(BasicAgent):
    def __init__(self):
        self.name = "AssetRegisterWritebackAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Stages updates to the Asset Management System and ERP fixed-asset "
                "register based on completed maintenance work and the post-work "
                "condition band."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "capture": {
                        "type": "object",
                        "description": "Capture envelope from FieldExecutionCaptureAgent.data.",
                    },
                    "new_condition_band": {
                        "type": "string",
                        "enum": ["Healthy", "Watch", "Degraded", "Critical"],
                        "description": "Operator's post-work condition assessment.",
                    },
                    "useful_life_delta_years": {
                        "type": "number",
                        "description": "Adjustment to useful life in years (positive = extended).",
                    },
                    "book_value_adjustment_usd": {
                        "type": "number",
                        "description": "Optional adjustment to book value in USD.",
                    },
                },
                "required": ["capture"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        capture = kwargs.get("capture")
        if not capture or not isinstance(capture, dict):
            return {
                "status": "needs_input",
                "agent": self.name,
                "message": "Provide `capture` (dict) from FieldExecutionCaptureAgent. No data will be fabricated.",
            }
        if not capture.get("ready_for_writeback", False):
            return {
                "status": "blocked",
                "agent": self.name,
                "message": "Capture is not ready for writeback (completion_status not completed/partial).",
                "data": {"capture_id": capture.get("capture_id")},
            }

        asset_id = capture.get("asset_id")
        wo = capture.get("work_order_id")
        new_band = kwargs.get("new_condition_band") or "Watch"
        life_delta = float(kwargs.get("useful_life_delta_years") or 0.0)
        book_adj = float(kwargs.get("book_value_adjustment_usd") or 0.0)

        ams_envelope = {
            "target_system": "Asset Management System (AMS)",
            "asset_id": asset_id,
            "patch": {
                "condition_band": new_band,
                "last_maintenance_date_utc": capture.get("completed_utc") or datetime.utcnow().isoformat() + "Z",
                "last_work_order_id": wo,
                "useful_life_delta_years": life_delta,
                "field_findings": capture.get("findings") or [],
                "quality_check": capture.get("quality_check"),
            },
        }

        erp_envelope = {
            "target_system": "ERP Fixed-Asset Register",
            "asset_id": asset_id,
            "patch": {
                "last_maintenance_journal_ref": wo,
                "last_maintenance_date_utc": capture.get("completed_utc") or datetime.utcnow().isoformat() + "Z",
                "book_value_adjustment_usd": book_adj,
                "useful_life_delta_years": life_delta,
                "requires_finance_review": abs(book_adj) > 0 or abs(life_delta) >= 1,
            },
        }

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Staged write-back for asset {asset_id}.",
            "data": {
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
                "asset_id": asset_id,
                "envelopes": [ams_envelope, erp_envelope],
                "dispatch_state": "ready_for_integration_runtime",
            },
        }


if __name__ == "__main__":
    import json
    from field_execution_capture_agent import FieldExecutionCaptureAgent
    cap = FieldExecutionCaptureAgent().perform(
        work_order_id="WO-ABCDEF0123",
        asset_id="AST-00001",
        completion_status="completed",
        actual_hours=4.5,
        quality_check="pass",
    )["data"]
    print(json.dumps(AssetRegisterWritebackAgent().perform(
        capture=cap,
        new_condition_band="Watch",
        useful_life_delta_years=1.5,
        book_value_adjustment_usd=-12500,
    ), indent=2))
