"""Parts Planner Agent — Energy Utilities.

For a batch of pending work orders, computes the parts / materials demand,
identifies long-lead items, and emits procurement triggers so the materials
team can start sourcing before the crew rolls. Shaped for ERP / SAP MM /
D365 Supply Chain ingestion.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from agents.basic_agent import BasicAgent
from datetime import datetime, timedelta


# task → list of (material, qty_per_wo, lead_time_days, unit_cost_usd)
TASK_BOM = {
    "Oil DGA Sample + Analyze": [
        ("Oil sample kit", 1, 7, 85),
        ("DGA lab analysis", 1, 5, 220),
    ],
    "Bushing IR + Capacitance Test": [
        ("Replacement HV bushing (preorder)", 1, 90, 18500),
        ("Insulation oil top-up (drum)", 1, 14, 920),
    ],
    "Cooler Bank Inspection": [
        ("Cooler fan assembly", 1, 21, 1450),
        ("Radiator gasket set", 2, 14, 180),
    ],
    "SF6 Leak Investigation": [
        ("SF6 leak detector cartridge", 1, 7, 320),
        ("SF6 gas cylinder (50kg)", 1, 28, 4800),
    ],
    "Contact Resistance Test": [
        ("Micro-ohmmeter consumables", 1, 7, 95),
    ],
    "Thermography Scan": [
        ("IR camera battery pack", 1, 7, 280),
    ],
    "Partial Discharge Field Survey": [
        ("PD coupler kit", 1, 14, 1750),
    ],
    "Joint Inspection (selective)": [
        ("Cable joint kit (selective)", 1, 60, 4200),
        ("Heat-shrink sleeve set", 2, 14, 110),
    ],
    "Sheath Bonding Verification": [
        ("Sheath voltage limiter", 1, 21, 540),
    ],
    "Aerial Patrol + LiDAR Resag Check": [
        ("Drone battery (LiPo)", 2, 7, 240),
    ],
    "Vegetation Management Dispatch": [
        ("Chipper fuel + PPE pack", 1, 3, 320),
    ],
    "Conductor Hotspot Inspection": [
        ("Compression sleeve repair set", 2, 21, 410),
    ],
}

LONG_LEAD_DAYS = 30


class PartsPlannerAgent(BasicAgent):
    def __init__(self):
        self.name = "PartsPlannerAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Aggregates parts / materials demand from pending work orders, "
                "flags long-lead items, and emits procurement triggers shaped "
                "for SAP MM / D365 Supply Chain ingestion."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "orders": {
                        "type": "array",
                        "description": "Work orders from MaintenanceWorkOrderAgent.data.orders.",
                    },
                    "long_lead_threshold_days": {
                        "type": "integer",
                        "description": "Flag any item with lead time >= this many days. Defaults to 30.",
                    },
                },
                "required": ["orders"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        orders = kwargs.get("orders")
        if not orders or not isinstance(orders, list):
            return {
                "status": "needs_input",
                "agent": self.name,
                "message": "Provide `orders` (list) from MaintenanceWorkOrderAgent. No data will be fabricated.",
            }
        long_lead = int(kwargs.get("long_lead_threshold_days") or LONG_LEAD_DAYS)

        demand: dict[str, dict] = {}
        per_order_lines = []
        for o in orders:
            task = o.get("task")
            qty_mult = 1
            bom = TASK_BOM.get(task, [])
            for material, qty, lead, cost in bom:
                key = material
                entry = demand.setdefault(key, {
                    "material": material,
                    "total_qty": 0,
                    "lead_time_days": lead,
                    "unit_cost_usd": cost,
                    "linked_work_orders": [],
                    "long_lead": lead >= long_lead,
                })
                entry["total_qty"] += qty * qty_mult
                entry["linked_work_orders"].append(o.get("work_order_id"))
                per_order_lines.append({
                    "work_order_id": o.get("work_order_id"),
                    "asset_id": o.get("asset_id"),
                    "material": material,
                    "qty": qty * qty_mult,
                    "lead_time_days": lead,
                    "unit_cost_usd": cost,
                    "extended_cost_usd": qty * qty_mult * cost,
                })

        consolidated = []
        triggers = []
        for entry in demand.values():
            entry["extended_cost_usd"] = entry["total_qty"] * entry["unit_cost_usd"]
            consolidated.append(entry)
            if entry["long_lead"]:
                triggers.append({
                    "procurement_trigger_id": f"PR-{abs(hash(entry['material'])) % 10_000_000:07d}",
                    "material": entry["material"],
                    "qty": entry["total_qty"],
                    "lead_time_days": entry["lead_time_days"],
                    "needed_by": (datetime.utcnow() + timedelta(days=entry["lead_time_days"])).date().isoformat(),
                    "target_system": "SAP MM / D365 Supply Chain",
                    "linked_work_orders": entry["linked_work_orders"],
                })

        total_cost = round(sum(e["extended_cost_usd"] for e in consolidated), 2)

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Planned parts for {len(orders)} WO(s). {len(triggers)} long-lead trigger(s) emitted.",
            "data": {
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
                "long_lead_threshold_days": long_lead,
                "total_estimated_cost_usd": total_cost,
                "consolidated_demand": consolidated,
                "procurement_triggers": triggers,
                "per_order_lines": per_order_lines,
            },
        }


if __name__ == "__main__":
    import json
    from asset_sensor_aggregator_agent import AssetSensorAggregatorAgent
    from asset_health_scorer_agent import AssetHealthScorerAgent
    from failure_probability_ranker_agent import FailureProbabilityRankerAgent
    from maintenance_work_order_agent import MaintenanceWorkOrderAgent
    snaps = AssetSensorAggregatorAgent().perform(sample_size=12)["data"]["snapshots"]
    scored = AssetHealthScorerAgent().perform(snapshots=snaps)["data"]["scored"]
    ranked = FailureProbabilityRankerAgent().perform(scored=scored, top_n=12)["data"]["ranked"]
    orders = MaintenanceWorkOrderAgent().perform(ranked=ranked, threshold=0.30)["data"]["orders"]
    print(json.dumps(PartsPlannerAgent().perform(orders=orders), indent=2))
