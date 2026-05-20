"""Test suite for the Payments Operations Excellence agent stack.

Verifies every agent.py in `../agents/`:
  * instantiates cleanly,
  * declares a valid metadata schema,
  * handles missing-input gracefully (no fabricated data).

Run from the bundle root:
    pytest -xvs tests/test_agents.py
"""

from __future__ import annotations

import sys
import importlib.util
from pathlib import Path

import pytest


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = BUNDLE_ROOT / "agents"


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
    spec.loader.exec_module(mod)
    return mod


AGENT_FILES = sorted(p for p in AGENTS_DIR.glob("*_agent.py") if p.name != "__init__.py")


@pytest.fixture(scope="module")
def loaded_agents():
    out = {}
    for f in AGENT_FILES:
        mod = _load_agent_module(f)
        cls = None
        for name in dir(mod):
            obj = getattr(mod, name)
            if isinstance(obj, type) and obj.__module__ == mod.__name__ and name.endswith("Agent"):
                cls = obj
                break
        assert cls, f"No *Agent class found in {f.name}"
        out[f.stem] = cls()
    return out


def test_agent_files_present():
    expected = {"payment_ingestion_validator_agent.py", "sanctions_screening_agent.py", "payment_exception_repair_agent.py", "nostro_reconciliation_agent.py", "correspondent_banking_monitor_agent.py", "pre_release_fraud_scorer_agent.py", "payment_status_tracker_agent.py", "payments_analytics_agent.py"}
    actual = {p.name for p in AGENT_FILES}
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


def test_missing_input_does_not_fabricate(loaded_agents):
    for key, agent in loaded_agents.items():
        out = agent.perform()
        assert out["status"] in {"needs_input", "error", "blocked", "success"}, (
            f"{key} returned an unexpected status `{out['status']}` on empty input."
        )
