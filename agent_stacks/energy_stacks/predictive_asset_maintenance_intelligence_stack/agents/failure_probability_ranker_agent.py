"""Failure Probability Ranker Agent — Energy Utilities.

Takes scored assets from the Asset Health Scorer and produces failure
probability across 30 / 90 / 180-day horizons, then ranks the fleet so an
operator can immediately see "which assets should I worry about, and over
what window?".

Output is deterministic for a given input snapshot (same anomaly → same
probability), so demos and reviews are reproducible.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from agents.basic_agent import BasicAgent
from datetime import datetime
import math


def _prob(anomaly: float, horizon_days: int) -> float:
    # Exponential survival model. Hazard rate grows quadratically with anomaly,
    # so a healthy asset stays low even on a 180-day horizon, while a critical
    # one spikes fast — and p(180) >= p(90) >= p(30) always.
    hazard_per_day = 0.0008 + (max(0.0, min(1.0, anomaly)) ** 2) * 0.015
    p = 1.0 - math.exp(-hazard_per_day * horizon_days)
    return round(p, 4)


class FailureProbabilityRankerAgent(BasicAgent):
    def __init__(self):
        self.name = "FailureProbabilityRankerAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Ranks assets by failure probability across 30 / 90 / 180-day "
                "horizons using the anomaly scores produced by AssetHealthScorerAgent."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "scored": {
                        "type": "array",
                        "description": "Array of scored assets from AssetHealthScorerAgent.data.scored.",
                    },
                    "horizon_days": {
                        "type": "integer",
                        "enum": [30, 90, 180],
                        "description": "Horizon to sort by. Defaults to 90.",
                    },
                    "top_n": {
                        "type": "integer",
                        "description": "Return only the top N highest-risk assets. Defaults to 25.",
                    },
                    "min_probability": {
                        "type": "number",
                        "description": "Filter to assets at or above this probability for the chosen horizon (0.0–1.0).",
                    },
                },
                "required": ["scored"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        scored = kwargs.get("scored")
        if not scored or not isinstance(scored, list):
            return {
                "status": "needs_input",
                "agent": self.name,
                "message": "Provide `scored` (list) from AssetHealthScorerAgent. No data will be fabricated.",
            }
        horizon = int(kwargs.get("horizon_days") or 90)
        if horizon not in (30, 90, 180):
            horizon = 90
        top_n = int(kwargs.get("top_n") or 25)
        min_prob = float(kwargs.get("min_probability") or 0.0)

        ranked = []
        for s in scored:
            anomaly = float(s.get("anomaly_score", 0.0))
            row = {
                "asset_id": s.get("asset_id"),
                "asset_class": s.get("asset_class"),
                "substation": s.get("substation"),
                "anomaly_score": anomaly,
                "health_score": s.get("health_score"),
                "rul_days": s.get("rul_days"),
                "condition_band": s.get("condition_band"),
                "p_fail_30d": _prob(anomaly, 30),
                "p_fail_90d": _prob(anomaly, 90),
                "p_fail_180d": _prob(anomaly, 180),
                "key_drivers": s.get("key_drivers", []),
            }
            ranked.append(row)

        ranked.sort(key=lambda r: r[f"p_fail_{horizon}d"], reverse=True)
        if min_prob > 0:
            ranked = [r for r in ranked if r[f"p_fail_{horizon}d"] >= min_prob]
        ranked = ranked[:top_n]

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Ranked {len(ranked)} asset(s) by {horizon}-day failure probability.",
            "data": {
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
                "horizon_days": horizon,
                "top_n": top_n,
                "min_probability": min_prob,
                "ranked": ranked,
            },
        }


if __name__ == "__main__":
    import json
    from asset_sensor_aggregator_agent import AssetSensorAggregatorAgent
    from asset_health_scorer_agent import AssetHealthScorerAgent
    snaps = AssetSensorAggregatorAgent().perform(sample_size=8)["data"]["snapshots"]
    scored = AssetHealthScorerAgent().perform(snapshots=snaps)["data"]["scored"]
    print(json.dumps(FailureProbabilityRankerAgent().perform(scored=scored, horizon_days=90, top_n=5), indent=2))
