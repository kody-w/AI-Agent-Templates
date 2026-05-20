"""Risk Assessment Agent — Energy Utilities.

Drafts a Risk Assessment & Method Statement (RAMS) tailored to the asset class and work type. Lists hazards, controls, PPE and residual risk score.

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


HAZARD_LIBRARY = {
    "transformer": [
        ("Electric shock / arc flash", "De-energise, lockout-tagout, voltage proving, arc-rated PPE"),
        ("Hot oil contact", "Cooling period, oil-handling PPE, drip-tray"),
        ("Manual handling of bushings/tap-changer", "Mechanical lift, two-person carry, gloves"),
    ],
    "switchgear": [
        ("Internal arc flash on operation", "Remote racking, arc-rated PPE, exclusion zone"),
        ("SF6 exposure", "Atmosphere check, ventilation, gas-tight PPE"),
        ("Trip / fall in confined enclosure", "Three-point contact, harness where elevated"),
    ],
    "underground_cable": [
        ("Cable strike from excavation", "Cable-route plans, CAT/Genny scan, hand-dig within 0.5 m"),
        ("Confined space (manhole / pit)", "Atmosphere monitor, top-person, rescue plan"),
        ("Heavy cable handling", "Mechanical roller, lifting beam, two-crew lift"),
    ],
    "overhead_line": [
        ("Working at height", "MEWP / pole climbing kit, fall-arrest, exclusion zone"),
        ("Adjacent live conductors", "Safe distance, insulated tools, earth-shorting"),
        ("Vegetation / wildlife interaction", "Site survey, biosecurity PPE"),
    ],
}


class RiskAssessmentAgent(BasicAgent):
    def __init__(self):
        self.name = "RiskAssessmentAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Drafts a Risk Assessment + Method Statement (RAMS) for the requested permit. "
                "Returns hazards, controls, PPE, and residual risk score."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "permit_request_id": {"type": "string"},
                    "asset_class": {"type": "string", "enum": list(HAZARD_LIBRARY.keys())},
                    "work_type": {"type": "string"},
                    "weather_factor": {"type": "string", "description": "calm / windy / wet / icy."},
                    "competence_level": {"type": "string", "enum": ["authorised", "senior_authorised"]},
                },
                "required": ["permit_request_id", "asset_class"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        if not kwargs.get("permit_request_id") or not kwargs.get("asset_class"):
            return {"status": "needs_input", "agent": self.name,
                    "message": "Provide `permit_request_id` and `asset_class`."}

        klass = kwargs["asset_class"]
        if klass not in HAZARD_LIBRARY:
            return {"status": "error", "agent": self.name,
                    "message": f"Unknown asset_class `{klass}`."}

        seed = _stable_seed(kwargs["permit_request_id"], klass)
        rng = random.Random(seed)

        hazards = [{"hazard": h, "controls": c.split(", ")} for h, c in HAZARD_LIBRARY[klass]]
        ppe = {
            "transformer": ["Arc-rated coveralls", "Insulated gloves Class 2", "Face shield"],
            "switchgear": ["Arc-rated coveralls", "Insulated gloves Class 2", "Hearing protection"],
            "underground_cable": ["Coveralls", "Cut-resistant gloves", "Hard hat with chin strap"],
            "overhead_line": ["Climbing kit / harness", "Insulated gloves Class 0", "High-vis"],
        }[klass]

        weather = (kwargs.get("weather_factor") or "calm").lower()
        weather_uplift = {"calm": 0.0, "windy": 0.10, "wet": 0.15, "icy": 0.25}.get(weather, 0.0)
        competence = kwargs.get("competence_level") or "authorised"
        competence_reduction = 0.10 if competence == "senior_authorised" else 0.0

        base_risk = 0.45 + rng.uniform(-0.08, 0.08)
        residual = round(max(0.05, min(0.95, base_risk + weather_uplift - competence_reduction)), 2)

        return {
            "status": "success",
            "agent": self.name,
            "message": f"Drafted RAMS for {kwargs['permit_request_id']}.",
            "data": {
                "permit_request_id": kwargs["permit_request_id"],
                "asset_class": klass,
                "hazards": hazards,
                "ppe": ppe,
                "method_statement_steps": [
                    "Tool-box talk + site sign-in",
                    "Confirm isolation + voltage proving",
                    "Erect barriers + signage",
                    "Perform work to method statement",
                    "Tidy site + clearance",
                ],
                "residual_risk_score": residual,
                "risk_band": "Low" if residual < 0.25 else "Medium" if residual < 0.55 else "High",
                "weather_factor": weather,
                "competence_level": competence,
            },
        }


if __name__ == "__main__":
    import json
    print(json.dumps(RiskAssessmentAgent().perform(
        permit_request_id="PRQ-000123", asset_class="transformer", work_type="overhaul"
    ), indent=2))
