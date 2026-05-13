"""Asset Health Scorer Agent — Energy Utilities.

Takes the normalized telemetry snapshots produced by the Asset Sensor Aggregator
and computes:
  - anomaly_score   (0.0–1.0, higher = more anomalous)
  - health_score    (0–100, higher = healthier)
  - rul_days        (Remaining Useful Life, days)
  - condition_band  (Healthy / Watch / Degraded / Critical)

Heuristics are domain-shaped (load %, temperature, DGA, partial discharge,
moisture, vegetation clearance) — not real ML, but realistic-shaped so the
downstream agents and human reviewers get useful, plausible numbers.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from agents.basic_agent import BasicAgent
from datetime import datetime
import math


def _norm(x: float, lo: float, hi: float) -> float:
    if hi <= lo:
        return 0.0
    return max(0.0, min(1.0, (x - lo) / (hi - lo)))


def _score_snapshot(snap: dict) -> dict:
    klass = snap.get("asset_class")
    t = snap.get("telemetry") or {}
    age = snap.get("age_years", 10)
    age_factor = _norm(age, 0, 50)  # older = worse

    if klass == "transformer":
        stress = max(
            _norm(t.get("temp_c", 60), 50, 110),
            _norm(t.get("load_pct", 50), 60, 130),
            _norm(t.get("oil_dga_ppm", 100), 50, 1000),
            _norm(t.get("partial_discharge_pc", 50), 100, 1500),
        )
    elif klass == "switchgear":
        stress = max(
            _norm(t.get("temp_c", 30), 30, 80),
            _norm(t.get("load_pct", 50), 60, 110),
            _norm(t.get("operations_count", 500), 1000, 5000),
            _norm(t.get("sf6_ppm", 1), 1, 10),
        )
    elif klass == "underground_cable":
        stress = max(
            _norm(t.get("temp_c", 30), 30, 70),
            _norm(t.get("load_pct", 50), 60, 120),
            _norm(t.get("moisture_index", 0.2), 0.2, 1.0),
            _norm(t.get("partial_discharge_pc", 50), 80, 1200),
        )
    else:  # overhead_line
        stress = max(
            _norm(t.get("temp_c", 25), 20, 60),
            _norm(t.get("load_pct", 50), 50, 100),
            _norm(t.get("sag_cm", 60), 80, 250),
            1.0 - _norm(t.get("vegetation_clearance_m", 3.0), 0.5, 5.0),
        )

    anomaly = round(min(1.0, 0.65 * stress + 0.35 * age_factor), 3)
    health = int(round(100 * (1 - anomaly)))

    # Plausible RUL curve: a healthy asset gets years; a stressed one collapses fast.
    rul_days = max(7, int(round(3650 * math.exp(-2.6 * anomaly))))

    if anomaly < 0.30:
        band = "Healthy"
    elif anomaly < 0.55:
        band = "Watch"
    elif anomaly < 0.78:
        band = "Degraded"
    else:
        band = "Critical"

    return {
        "asset_id": snap.get("asset_id"),
        "asset_class": klass,
        "substation": snap.get("substation"),
        "anomaly_score": anomaly,
        "health_score": health,
        "rul_days": rul_days,
        "condition_band": band,
        "key_drivers": _drivers(klass, t),
    }


def _drivers(klass, t):
    drivers = []
    if klass == "transformer":
        if t.get("oil_dga_ppm", 0) > 400:
            drivers.append("Elevated DGA")
        if t.get("temp_c", 0) > 85:
            drivers.append("High oil temp")
        if t.get("load_pct", 0) > 95:
            drivers.append("Sustained overload")
        if t.get("partial_discharge_pc", 0) > 600:
            drivers.append("Partial discharge activity")
    elif klass == "switchgear":
        if t.get("sf6_ppm", 0) > 4:
            drivers.append("SF6 leak signal")
        if t.get("operations_count", 0) > 2500:
            drivers.append("High operations count")
        if t.get("temp_c", 0) > 55:
            drivers.append("Hotspot trend")
    elif klass == "underground_cable":
        if t.get("moisture_index", 0) > 0.5:
            drivers.append("Moisture ingress")
        if t.get("partial_discharge_pc", 0) > 500:
            drivers.append("Insulation degradation")
        if t.get("load_pct", 0) > 90:
            drivers.append("Thermal cycling")
    else:
        if t.get("sag_cm", 0) > 180:
            drivers.append("Excessive sag")
        if t.get("vegetation_clearance_m", 5) < 1.5:
            drivers.append("Vegetation encroachment")
        if t.get("temp_c", 0) > 50:
            drivers.append("Conductor heating")
    return drivers or ["Normal operating envelope"]


class AssetHealthScorerAgent(BasicAgent):
    def __init__(self):
        self.name = "AssetHealthScorerAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Computes anomaly score, health score, condition band and "
                "Remaining Useful Life (RUL) for each asset from normalized "
                "telemetry snapshots."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "snapshots": {
                        "type": "array",
                        "description": "Array of asset snapshots from AssetSensorAggregatorAgent.",
                    },
                },
                "required": ["snapshots"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        snapshots = kwargs.get("snapshots")
        if not snapshots or not isinstance(snapshots, list):
            return {
                "status": "needs_input",
                "agent": self.name,
                "message": "Provide `snapshots` (list) from AssetSensorAggregatorAgent. No data will be fabricated.",
            }
        scored = [_score_snapshot(s) for s in snapshots]
        band_counts = {b: 0 for b in ("Healthy", "Watch", "Degraded", "Critical")}
        for s in scored:
            band_counts[s["condition_band"]] += 1
        return {
            "status": "success",
            "agent": self.name,
            "message": f"Scored {len(scored)} asset(s).",
            "data": {
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
                "model": "rule-based-v1 (heuristic, domain-shaped)",
                "summary": band_counts,
                "scored": scored,
            },
        }


if __name__ == "__main__":
    import json
    from asset_sensor_aggregator_agent import AssetSensorAggregatorAgent
    snaps = AssetSensorAggregatorAgent().perform(sample_size=3)["data"]["snapshots"]
    print(json.dumps(AssetHealthScorerAgent().perform(snapshots=snaps), indent=2))
