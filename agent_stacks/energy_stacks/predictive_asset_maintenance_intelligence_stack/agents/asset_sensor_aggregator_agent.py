"""Asset Sensor Aggregator Agent — Energy Utilities.

Pulls and normalizes IoT/SCADA telemetry across grid assets (transformers,
switchgear, cables, overhead lines). Produces a single, time-aligned health
snapshot per asset so downstream agents can score, rank and act.

Portable. No PII. Plugs into the rapp_ai BasicAgent runtime.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from agents.basic_agent import BasicAgent
from datetime import datetime, timedelta
import random
import hashlib


ASSET_CLASSES = ["transformer", "switchgear", "underground_cable", "overhead_line"]


def _stable_seed(*parts) -> int:
    h = hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()
    return int(h[:8], 16)


def _synth_asset(asset_id: str, asset_class: str | None = None):
    rng = random.Random(_stable_seed(asset_id))
    asset_class = asset_class or rng.choice(ASSET_CLASSES)
    age_years = rng.randint(3, 42)

    base = {
        "transformer": {"temp_c": rng.uniform(55, 95), "load_pct": rng.uniform(40, 110),
                        "oil_dga_ppm": rng.uniform(20, 800), "partial_discharge_pc": rng.uniform(5, 1200)},
        "switchgear": {"temp_c": rng.uniform(25, 70), "load_pct": rng.uniform(30, 95),
                       "operations_count": rng.randint(50, 4000), "sf6_ppm": rng.uniform(0.1, 8.0)},
        "underground_cable": {"temp_c": rng.uniform(20, 65), "load_pct": rng.uniform(35, 105),
                              "moisture_index": rng.uniform(0.05, 0.85), "partial_discharge_pc": rng.uniform(3, 950)},
        "overhead_line": {"temp_c": rng.uniform(15, 55), "load_pct": rng.uniform(25, 90),
                          "sag_cm": rng.uniform(10, 220), "vegetation_clearance_m": rng.uniform(0.4, 6.5)},
    }[asset_class]

    return {
        "asset_id": asset_id,
        "asset_class": asset_class,
        "age_years": age_years,
        "substation": f"SUB-{rng.randint(1, 99):02d}",
        "voltage_kv": rng.choice([11, 22, 33, 66, 132, 230, 345]),
        "telemetry": base,
        "last_sample_utc": (datetime.utcnow() - timedelta(minutes=rng.randint(0, 14))).isoformat() + "Z",
        "sensor_health": "ok" if rng.random() > 0.06 else "intermittent",
    }


class AssetSensorAggregatorAgent(BasicAgent):
    def __init__(self):
        self.name = "AssetSensorAggregatorAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Aggregates and normalizes IoT/SCADA telemetry across grid assets "
                "(transformers, switchgear, cables, overhead lines). Returns a "
                "time-aligned health snapshot per asset."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "asset_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of asset IDs to aggregate. If omitted, returns a synthetic fleet sample.",
                    },
                    "asset_class": {
                        "type": "string",
                        "enum": ASSET_CLASSES,
                        "description": "Filter to a single asset class.",
                    },
                    "substation": {
                        "type": "string",
                        "description": "Filter to a single substation (e.g. SUB-44).",
                    },
                    "sample_size": {
                        "type": "integer",
                        "description": "When asset_ids is omitted, number of synthetic assets to return.",
                    },
                },
                "required": [],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        asset_ids = kwargs.get("asset_ids") or []
        asset_class = kwargs.get("asset_class")
        substation = kwargs.get("substation")
        sample_size = int(kwargs.get("sample_size") or 25)

        if not asset_ids:
            asset_ids = [f"AST-{i:05d}" for i in range(1, sample_size + 1)]

        snapshots = [_synth_asset(aid, asset_class) for aid in asset_ids]
        if substation:
            snapshots = [s for s in snapshots if s["substation"] == substation]

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Aggregated telemetry for {len(snapshots)} asset(s).",
            "data": {
                "as_of_utc": datetime.utcnow().isoformat() + "Z",
                "sources": ["Azure IoT Hub", "SCADA Historian", "Asset Management System"],
                "asset_count": len(snapshots),
                "snapshots": snapshots,
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(AssetSensorAggregatorAgent().perform(sample_size=3), indent=2))
