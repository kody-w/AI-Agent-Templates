"""Maintenance Work Order Agent — Energy Utilities.

Takes ranked assets (probabilities + drivers) and generates Field Service
work order drafts for any asset that crosses a configured probability threshold.
Each WO is shaped for D365 Field Service / ServiceNow ITSM-style ingestion.

By design this agent emits *draft* WOs in `pending_review` status. A human
dispatcher confirms before they hit the field-service queue.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from agents.basic_agent import BasicAgent
from datetime import datetime, timedelta
import hashlib


CLASS_TASKS = {
    "transformer": [
        ("Oil DGA Sample + Analyze", "specialist_oil_sampling_crew", 4, "P2"),
        ("Bushing IR + Capacitance Test", "transformer_test_crew", 3, "P2"),
        ("Cooler Bank Inspection", "substation_crew", 2, "P3"),
    ],
    "switchgear": [
        ("SF6 Leak Investigation", "switchgear_specialist", 3, "P1"),
        ("Contact Resistance Test", "substation_crew", 3, "P2"),
        ("Thermography Scan", "thermography_team", 1, "P3"),
    ],
    "underground_cable": [
        ("Partial Discharge Field Survey", "cable_pd_crew", 5, "P2"),
        ("Joint Inspection (selective)", "cable_splice_crew", 4, "P2"),
        ("Sheath Bonding Verification", "cable_test_crew", 3, "P3"),
    ],
    "overhead_line": [
        ("Aerial Patrol + LiDAR Resag Check", "aerial_patrol_team", 4, "P2"),
        ("Vegetation Management Dispatch", "vegetation_crew", 6, "P2"),
        ("Conductor Hotspot Inspection", "line_crew", 3, "P3"),
    ],
}


def _wo_id(asset_id: str, horizon: int) -> str:
    h = hashlib.sha256(f"{asset_id}|{horizon}|wo".encode()).hexdigest()
    return "WO-" + h[:10].upper()


def _due_by(priority: str) -> str:
    days = {"P1": 3, "P2": 14, "P3": 30}.get(priority, 21)
    return (datetime.utcnow() + timedelta(days=days)).date().isoformat()


class MaintenanceWorkOrderAgent(BasicAgent):
    def __init__(self):
        self.name = "MaintenanceWorkOrderAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Generates Field Service work order drafts for assets crossing a "
                "configured failure-probability threshold. Outputs are pending_review "
                "and shaped for D365 Field Service / ServiceNow-style ingestion."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ranked": {
                        "type": "array",
                        "description": "Ranked asset rows from FailureProbabilityRankerAgent.data.ranked.",
                    },
                    "horizon_days": {
                        "type": "integer",
                        "enum": [30, 90, 180],
                        "description": "Horizon to evaluate against. Defaults to 90.",
                    },
                    "threshold": {
                        "type": "number",
                        "description": "Minimum failure probability for the chosen horizon (0.0–1.0). Defaults to 0.30.",
                    },
                    "max_orders": {
                        "type": "integer",
                        "description": "Cap on number of WOs generated. Defaults to 50.",
                    },
                },
                "required": ["ranked"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        ranked = kwargs.get("ranked")
        if not ranked or not isinstance(ranked, list):
            return {
                "status": "needs_input",
                "agent": self.name,
                "message": "Provide `ranked` (list) from FailureProbabilityRankerAgent. No data will be fabricated.",
            }
        horizon = int(kwargs.get("horizon_days") or 90)
        if horizon not in (30, 90, 180):
            horizon = 90
        threshold = float(kwargs.get("threshold") or 0.30)
        max_orders = int(kwargs.get("max_orders") or 50)

        prob_key = f"p_fail_{horizon}d"
        eligible = [r for r in ranked if float(r.get(prob_key, 0)) >= threshold]
        eligible.sort(key=lambda r: r[prob_key], reverse=True)
        eligible = eligible[:max_orders]

        orders = []
        for r in eligible:
            klass = r.get("asset_class") or "transformer"
            tasks = CLASS_TASKS.get(klass, CLASS_TASKS["transformer"])
            priority = "P1" if r[prob_key] >= 0.75 else "P2" if r[prob_key] >= 0.50 else "P3"
            # Choose the highest-touch task that matches the priority
            task_name, crew, est_hours, _ = tasks[0]
            orders.append({
                "work_order_id": _wo_id(r["asset_id"], horizon),
                "status": "pending_review",
                "asset_id": r["asset_id"],
                "asset_class": klass,
                "substation": r.get("substation"),
                "priority": priority,
                "horizon_days": horizon,
                "failure_probability": r[prob_key],
                "condition_band": r.get("condition_band"),
                "task": task_name,
                "assigned_crew_type": crew,
                "estimated_hours": est_hours,
                "due_by": _due_by(priority),
                "rationale": "; ".join(r.get("key_drivers", []) or ["Threshold exceeded"]),
                "target_system": "D365 Field Service",
            })

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Drafted {len(orders)} work order(s) above {threshold:.0%} on {horizon}-day horizon.",
            "data": {
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
                "threshold": threshold,
                "horizon_days": horizon,
                "orders": orders,
            },
        }


if __name__ == "__main__":
    import json
    from asset_sensor_aggregator_agent import AssetSensorAggregatorAgent
    from asset_health_scorer_agent import AssetHealthScorerAgent
    from failure_probability_ranker_agent import FailureProbabilityRankerAgent
    snaps = AssetSensorAggregatorAgent().perform(sample_size=12)["data"]["snapshots"]
    scored = AssetHealthScorerAgent().perform(snapshots=snaps)["data"]["scored"]
    ranked = FailureProbabilityRankerAgent().perform(scored=scored, top_n=12)["data"]["ranked"]
    print(json.dumps(MaintenanceWorkOrderAgent().perform(ranked=ranked, threshold=0.30), indent=2))
