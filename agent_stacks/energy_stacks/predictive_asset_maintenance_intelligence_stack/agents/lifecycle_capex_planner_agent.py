"""Lifecycle Capex Planner Agent — Energy Utilities.

Looks across the scored / ranked fleet and produces a multi-year capital
replacement pipeline: which assets are candidates for replacement, in which
fiscal year, at what indicative cost, and the avoided-failure value behind
the case.

Output is suitable for capex committee review (not auto-approval).
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from agents.basic_agent import BasicAgent
from datetime import datetime


# Indicative replacement cost (USD) and avoided-failure value per asset class
CLASS_ECONOMICS = {
    "transformer": {"replace_cost_usd": 950_000, "avoided_failure_usd": 4_800_000},
    "switchgear": {"replace_cost_usd": 320_000, "avoided_failure_usd": 1_500_000},
    "underground_cable": {"replace_cost_usd": 1_100_000, "avoided_failure_usd": 3_200_000},
    "overhead_line": {"replace_cost_usd": 480_000, "avoided_failure_usd": 1_800_000},
}


def _fiscal_year_offset(p180: float, age_years: int) -> int:
    """Return number of years out before the asset is slated for replacement."""
    # Critical: this FY. Highly stressed or aged: next FY. Etc.
    if p180 >= 0.65 or age_years >= 40:
        return 0
    if p180 >= 0.45 or age_years >= 32:
        return 1
    if p180 >= 0.30 or age_years >= 25:
        return 2
    return 3


class LifecycleCapexPlannerAgent(BasicAgent):
    def __init__(self):
        self.name = "LifecycleCapexPlannerAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Produces a multi-year capital replacement pipeline from the "
                "scored / ranked fleet: candidates, fiscal year placement, "
                "indicative cost, and avoided-failure value."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ranked": {
                        "type": "array",
                        "description": "Ranked rows from FailureProbabilityRankerAgent.data.ranked (must include 180-day prob).",
                    },
                    "current_fiscal_year": {
                        "type": "integer",
                        "description": "Current FY (e.g. 2026). Defaults to current calendar year.",
                    },
                    "horizon_years": {
                        "type": "integer",
                        "description": "How many FYs forward to plan. Defaults to 4.",
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
        cfy = int(kwargs.get("current_fiscal_year") or datetime.utcnow().year)
        horizon = int(kwargs.get("horizon_years") or 4)

        # `age_years` isn't in the ranked rows by default — synthesise from anomaly if missing
        pipeline = []
        for r in ranked:
            klass = r.get("asset_class") or "transformer"
            economics = CLASS_ECONOMICS.get(klass, CLASS_ECONOMICS["transformer"])
            age_years = int(r.get("age_years", 0))  # tolerated if absent
            p180 = float(r.get("p_fail_180d", 0.0))
            fy_offset = _fiscal_year_offset(p180, age_years)
            if fy_offset >= horizon:
                continue  # outside the planning window
            pipeline.append({
                "asset_id": r["asset_id"],
                "asset_class": klass,
                "substation": r.get("substation"),
                "anomaly_score": r.get("anomaly_score"),
                "p_fail_180d": p180,
                "condition_band": r.get("condition_band"),
                "planned_fiscal_year": cfy + fy_offset,
                "indicative_replace_cost_usd": economics["replace_cost_usd"],
                "avoided_failure_value_usd": economics["avoided_failure_usd"],
                "benefit_cost_ratio": round(
                    economics["avoided_failure_usd"] * p180 / max(1, economics["replace_cost_usd"]), 2
                ),
                "justification_drivers": r.get("key_drivers", []),
            })

        pipeline.sort(key=lambda x: (x["planned_fiscal_year"], -x["benefit_cost_ratio"]))

        by_fy: dict[int, dict] = {}
        for row in pipeline:
            fy = row["planned_fiscal_year"]
            agg = by_fy.setdefault(fy, {
                "fiscal_year": fy,
                "candidates": 0,
                "total_replace_cost_usd": 0,
                "total_avoided_failure_value_usd": 0,
                "by_class": {},
            })
            agg["candidates"] += 1
            agg["total_replace_cost_usd"] += row["indicative_replace_cost_usd"]
            agg["total_avoided_failure_value_usd"] += row["avoided_failure_value_usd"]
            agg["by_class"][row["asset_class"]] = agg["by_class"].get(row["asset_class"], 0) + 1
        by_fy_sorted = [by_fy[k] for k in sorted(by_fy.keys())]

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Planned {len(pipeline)} candidate(s) across {len(by_fy_sorted)} fiscal year(s).",
            "data": {
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
                "current_fiscal_year": cfy,
                "horizon_years": horizon,
                "annual_summary": by_fy_sorted,
                "pipeline": pipeline,
            },
        }


if __name__ == "__main__":
    import json
    from asset_sensor_aggregator_agent import AssetSensorAggregatorAgent
    from asset_health_scorer_agent import AssetHealthScorerAgent
    from failure_probability_ranker_agent import FailureProbabilityRankerAgent
    snaps = AssetSensorAggregatorAgent().perform(sample_size=20)["data"]["snapshots"]
    scored = AssetHealthScorerAgent().perform(snapshots=snaps)["data"]["scored"]
    ranked = FailureProbabilityRankerAgent().perform(scored=scored, top_n=20)["data"]["ranked"]
    print(json.dumps(LifecycleCapexPlannerAgent().perform(ranked=ranked), indent=2))
