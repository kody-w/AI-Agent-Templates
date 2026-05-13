"""Test suite for the Predictive Asset Maintenance Intelligence agent stack.

Verifies every agent.py in `../agents/`:
  * instantiates cleanly,
  * declares a valid metadata schema,
  * handles its happy-path call with a structured success response,
  * handles missing-input gracefully (no fabricated data).

Also runs the full 8-agent pipeline end-to-end to catch contract drift
between agents (output of one feeds the next).

Run from the bundle root:
    pytest -xvs tests/test_agents.py
"""

from __future__ import annotations

import os
import sys
import importlib.util
from pathlib import Path

import pytest


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = BUNDLE_ROOT / "agents"


# --- BasicAgent stub on the import path -----------------------------------
# The agent files do `from agents.basic_agent import BasicAgent`. When running
# under the real rapp_ai runtime that resolves to rapp_ai/agents/basic_agent.py.
# Here we provide a minimal shim so the tests are runtime-independent.
def _ensure_basic_agent_stub():
    stub_root = BUNDLE_ROOT / "tests" / "_stub_runtime"
    pkg = stub_root / "agents"
    pkg.mkdir(parents=True, exist_ok=True)
    (pkg / "__init__.py").write_text("")
    basic = pkg / "basic_agent.py"
    if not basic.exists():
        basic.write_text(
            "class BasicAgent:\n"
            "    def __init__(self, name, metadata):\n"
            "        self.name = name\n"
            "        self.metadata = metadata\n"
            "    def perform(self, **kwargs):\n"
            "        raise NotImplementedError\n"
        )
    sys.path.insert(0, str(stub_root))


_ensure_basic_agent_stub()


def _load_agent_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    # The agent files do their own sys.path tweak that walks up four levels
    # looking for `agents.basic_agent`. That walk lands outside this repo on
    # most machines, so we make sure our stub takes precedence.
    spec.loader.exec_module(mod)
    return mod


AGENT_FILES = sorted(p for p in AGENTS_DIR.glob("*_agent.py") if p.name != "__init__.py")


@pytest.fixture(scope="module")
def loaded_agents():
    out = {}
    for f in AGENT_FILES:
        mod = _load_agent_module(f)
        # Find the single class that subclasses BasicAgent
        cls = None
        for name in dir(mod):
            obj = getattr(mod, name)
            if isinstance(obj, type) and obj.__module__ == mod.__name__ and name.endswith("Agent"):
                cls = obj
                break
        assert cls, f"No *Agent class found in {f.name}"
        out[f.stem] = cls()
    return out


# --- Structural tests ------------------------------------------------------

def test_eight_agent_files_present():
    expected = {
        "asset_sensor_aggregator_agent.py",
        "asset_health_scorer_agent.py",
        "failure_probability_ranker_agent.py",
        "maintenance_work_order_agent.py",
        "parts_planner_agent.py",
        "field_execution_capture_agent.py",
        "asset_register_writeback_agent.py",
        "lifecycle_capex_planner_agent.py",
    }
    actual = {p.name for p in AGENT_FILES}
    # Keep the legacy single-file scaffold tolerated but require the eight new ones
    missing = expected - actual
    assert not missing, f"Missing agent files: {missing}"


def test_each_agent_has_valid_metadata(loaded_agents):
    for name, agent in loaded_agents.items():
        md = agent.metadata
        assert "name" in md and md["name"] == agent.name, f"{name}: bad name"
        assert "description" in md and md["description"], f"{name}: missing description"
        assert "parameters" in md, f"{name}: missing parameters"
        assert md["parameters"].get("type") == "object", f"{name}: parameters.type"
        assert "properties" in md["parameters"], f"{name}: parameters.properties"


# --- Happy-path: full pipeline (output of one feeds the next) -------------

def test_full_pipeline_e2e(loaded_agents):
    agg = loaded_agents["asset_sensor_aggregator_agent"]
    scorer = loaded_agents["asset_health_scorer_agent"]
    ranker = loaded_agents["failure_probability_ranker_agent"]
    wo = loaded_agents["maintenance_work_order_agent"]
    parts = loaded_agents["parts_planner_agent"]
    capture = loaded_agents["field_execution_capture_agent"]
    writeback = loaded_agents["asset_register_writeback_agent"]
    capex = loaded_agents["lifecycle_capex_planner_agent"]

    # 1. Aggregate telemetry
    agg_out = agg.perform(sample_size=20)
    assert agg_out["status"] == "success"
    assert agg_out["data"]["asset_count"] == 20
    snaps = agg_out["data"]["snapshots"]

    # 2. Score
    score_out = scorer.perform(snapshots=snaps)
    assert score_out["status"] == "success"
    scored = score_out["data"]["scored"]
    assert len(scored) == 20
    for row in scored:
        assert 0.0 <= row["anomaly_score"] <= 1.0
        assert 0 <= row["health_score"] <= 100
        assert row["rul_days"] > 0
        assert row["condition_band"] in {"Healthy", "Watch", "Degraded", "Critical"}

    # 3. Rank
    rank_out = ranker.perform(scored=scored, horizon_days=90, top_n=20)
    assert rank_out["status"] == "success"
    ranked = rank_out["data"]["ranked"]
    assert len(ranked) > 0
    # Monotonic-ish — highest first
    probs = [r["p_fail_90d"] for r in ranked]
    assert probs == sorted(probs, reverse=True)
    for r in ranked:
        assert 0.0 <= r["p_fail_30d"] <= r["p_fail_90d"] <= r["p_fail_180d"] <= 1.0

    # 4. WO generation at low threshold so we always get some orders
    wo_out = wo.perform(ranked=ranked, threshold=0.10, horizon_days=90)
    assert wo_out["status"] == "success"
    orders = wo_out["data"]["orders"]
    assert isinstance(orders, list)
    for o in orders:
        assert o["status"] == "pending_review"
        assert o["priority"] in {"P1", "P2", "P3"}
        assert o["work_order_id"].startswith("WO-")
        assert o["due_by"]

    # 5. Parts planning
    if orders:
        parts_out = parts.perform(orders=orders)
        assert parts_out["status"] == "success"
        assert parts_out["data"]["total_estimated_cost_usd"] >= 0
        # any long-lead item should be flagged
        for trig in parts_out["data"]["procurement_triggers"]:
            assert trig["lead_time_days"] >= parts_out["data"]["long_lead_threshold_days"]
            assert trig["procurement_trigger_id"].startswith("PR-")

    # 6. Field execution capture (synthetic close-out on first order if any)
    if orders:
        cap_out = capture.perform(
            work_order_id=orders[0]["work_order_id"],
            asset_id=orders[0]["asset_id"],
            crew_id="CREW-TEST",
            completion_status="completed",
            actual_hours=4.0,
            findings=["Within envelope"],
            photos_count=8,
            quality_check="pass",
        )
        assert cap_out["status"] == "success"
        capture_data = cap_out["data"]
        assert capture_data["ready_for_writeback"] is True

        # 7. Write-back staging
        wb_out = writeback.perform(
            capture=capture_data,
            new_condition_band="Watch",
            useful_life_delta_years=1.0,
            book_value_adjustment_usd=-5000,
        )
        assert wb_out["status"] == "success"
        envelopes = wb_out["data"]["envelopes"]
        targets = {e["target_system"] for e in envelopes}
        assert "Asset Management System (AMS)" in targets
        assert "ERP Fixed-Asset Register" in targets

    # 8. Lifecycle capex (always)
    capex_out = capex.perform(ranked=ranked, current_fiscal_year=2026, horizon_years=4)
    assert capex_out["status"] == "success"
    annual = capex_out["data"]["annual_summary"]
    assert all(2026 <= row["fiscal_year"] <= 2029 for row in annual)


# --- Missing-input behavior: no fabrication ------------------------------

@pytest.mark.parametrize("agent_key", [
    "asset_health_scorer_agent",
    "failure_probability_ranker_agent",
    "maintenance_work_order_agent",
    "parts_planner_agent",
    "asset_register_writeback_agent",
    "lifecycle_capex_planner_agent",
])
def test_missing_input_does_not_fabricate(loaded_agents, agent_key):
    agent = loaded_agents[agent_key]
    out = agent.perform()  # no args
    assert out["status"] in {"needs_input", "error", "blocked"}, (
        f"{agent_key} returned {out['status']!r} on empty input; should not fabricate."
    )


def test_capture_requires_three_fields(loaded_agents):
    agent = loaded_agents["field_execution_capture_agent"]
    out = agent.perform()
    assert out["status"] == "needs_input"
    out2 = agent.perform(work_order_id="WO-X", asset_id="AST-Y", completion_status="not_a_status")
    assert out2["status"] == "error"


# --- Determinism: same input → same output ------------------------------

def test_determinism_aggregator(loaded_agents):
    agg = loaded_agents["asset_sensor_aggregator_agent"]
    a = agg.perform(asset_ids=["AST-FIXED-1", "AST-FIXED-2"])
    b = agg.perform(asset_ids=["AST-FIXED-1", "AST-FIXED-2"])
    # Telemetry derives from a stable per-asset seed; identical content expected
    assert a["data"]["snapshots"][0]["asset_class"] == b["data"]["snapshots"][0]["asset_class"]
    assert a["data"]["snapshots"][0]["substation"] == b["data"]["snapshots"][0]["substation"]
    assert a["data"]["snapshots"][0]["telemetry"] == b["data"]["snapshots"][0]["telemetry"]
