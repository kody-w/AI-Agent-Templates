"""Small standalone public demo agent for the NBCU Finance Reporting Copilot stack.

Scope, honestly stated: this file is NOT the production reporting engine. It
does not ingest workbooks, generate PPTX/XLSX artifacts, or run formula-
signature governance. The full engine (validation, driver-walk reconciliation,
Office file generation) is a private production package outside this public
repository. What lives here is a small, deterministic contract: fixed,
signed-off synthetic figures for the public demo, so downstream tooling
(scripted-demo runners, the M365 Copilot-style HTML demo, RAR consumers) can
render the same stable numbers online or from a static file with no network
access. All entity names and dollar figures are synthetic.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

import json
from datetime import datetime, timezone

from agents.basic_agent import BasicAgent


# The same fixed synthetic snapshot published at
# agent_stacks/financial_services_stacks/nbcu_finance_reporting_stack/files/
# nbcu_finance_reporting_snapshot.json -- kept in sync by hand, not derived,
# so this agent runs standalone with zero file I/O.
SYNTHETIC_SUMMARY = {
    "units": "USD millions",
    "status": "provisional-submitted-data-subtotal",
    "publishable": False,
    "missing_inputs": ["Local Political; last-known value 15.0 retained in exception context"],
    "total_current": 1536.8,
    "total_budget": 1472.0,
    "variance_vs_budget": 64.8,
    "variance_vs_prior_year": -152.8,
    "variance_vs_prior_pacing": 21.4,
    "variance_vs_prior_estimate": 36.8,
}

SYNTHETIC_EXCEPTIONS = [
    {
        "entity": "NBC Sports",
        "type": "reconciliation_gap",
        "severity": "medium",
        "blocking": True,
        "message": (
            "Current vs budget variance 12.0 does not equal configured "
            "drivers 11.5; residual 0.5."
        ),
        "owner": "Linear finance owner",
    },
    {
        "entity": "Local Political",
        "type": "missing_submission",
        "severity": "high",
        "blocking": True,
        # Design rule, honored here rather than just described: a missing
        # submission always carries its last-known value forward for
        # display. It is never coerced to zero.
        "message": (
            "Submission status is missing while the prior snapshot "
            "contained 15.0; missing data is never coerced to zero."
        ),
        "owner": "FP&A reviewer",
    },
    {
        "entity": "S09",
        "type": "cross_slide_mismatch",
        "severity": "high",
        "blocking": True,
        "message": (
            "variance_vs_budget on the Publication Decision slide (S09) is 63.8 but "
            "the canonical reconciled value is 64.8."
        ),
        "owner": "FP&A reviewer",
    },
    {
        "entity": "Digital Revenue Variance.xlsx!S5",
        "type": "stale_label",
        "severity": "medium",
        "blocking": False,
        "message": (
            "Expected label '2026 current view vs 2026 budget', found "
            "'2027 budget vs 2026 budget'."
        ),
        "owner": "FP&A reviewer",
    },
]

# Deterministic, keyword-matched canned answers for the three scripted demo
# turns. This is not a natural-language engine -- it exists only so a
# scripted-demo runner can replay the exact public demo conversation.
_SCRIPTED_REPLIES = [
    (
        ("summarize", "budget"),
        "Provisional submitted-data subtotal: Current Estimate $1,536.8 million "
        "vs Budget $1,472.0 million, variance +$64.8 million. Local Political "
        "remains missing; its last-known $15.0 million stays visible in the exception context but is "
        "not inserted into this subtotal or treated as zero. This is not a "
        "complete, publishable roll-up. "
        "3 blocking review items must be resolved before this package can "
        "route to Finance for approval; 1 advisory item is also open.",
    ),
    (
        ("blocking", "exception"),
        "3 blocking exceptions: a reconciliation gap at NBC Sports, a "
        "missing Local Political submission (its prior 15.0 was preserved, "
        "not zeroed), and a cross-slide mismatch on the Publication Decision "
        "slide (S09: 63.8 shown vs 64.8 canonical). 1 advisory: a stale label on "
        "Digital Revenue Variance.xlsx!S5.",
    ),
    (
        ("workbook", "deck"),
        "Review workbook and executive reporting deck staged. Status: "
        "DRAFT. Outputs remain withheld from distribution until a Finance "
        "owner clears the blocking exceptions and approves the package.",
    ),
]


class NbcuFinanceReportingDemoAgent(BasicAgent):
    def __init__(self):
        self.name = "NbcuFinanceReportingDemoAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Public demo-contract agent for the NBCU Finance Reporting "
                "Copilot stack. Returns the fixed, signed-off synthetic "
                "monthly-pacing snapshot (Current Estimate vs Budget/Prior "
                "Year/Prior Pacing/Prior Estimate, blocking exceptions, "
                "advisory findings). Does not generate Office artifacts or "
                "ingest real workbooks -- see module docstring for scope."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["status", "summary", "exceptions", "package", "chat"],
                        "description": (
                            "status: readiness; summary: Current Estimate vs "
                            "comparison totals; exceptions: blocking + "
                            "advisory findings; package: the full synthetic "
                            "snapshot; chat: a scripted, keyword-matched "
                            "reply for the three demo prompts."
                        ),
                    },
                    "message": {
                        "type": "string",
                        "description": "Analyst question for operation=chat.",
                    },
                },
                "required": ["operation"],
            },
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        operation = str(kwargs.get("operation") or "status").strip().lower()

        if operation == "status":
            return json.dumps(
                {
                    "status": "ready",
                    "agent": self.name,
                    "scope": "public demo contract only; not the production engine",
                    "synthetic": True,
                    "generated_at": datetime.now(timezone.utc)
                    .replace(microsecond=0)
                    .isoformat(),
                },
                indent=2,
            )

        if operation == "summary":
            return json.dumps({"synthetic": True, "summary": SYNTHETIC_SUMMARY}, indent=2)

        if operation == "exceptions":
            blocking = [e for e in SYNTHETIC_EXCEPTIONS if e["blocking"]]
            advisory = [e for e in SYNTHETIC_EXCEPTIONS if not e["blocking"]]
            return json.dumps(
                {
                    "synthetic": True,
                    "blocking_count": len(blocking),
                    "advisory_count": len(advisory),
                    "blocking": blocking,
                    "advisory": advisory,
                },
                indent=2,
            )

        if operation == "package":
            return json.dumps(
                {
                    "synthetic": True,
                    "notice": (
                        "Synthetic demo data only. No NBCUniversal customer "
                        "or production financial data is included. The total "
                        "is a provisional submitted-data subtotal. The missing "
                        "Local Political value remains visible in the exception "
                        "context but is not inserted or treated as zero."
                    ),
                    "summary": SYNTHETIC_SUMMARY,
                    "exceptions": SYNTHETIC_EXCEPTIONS,
                    "approval_required": True,
                },
                indent=2,
            )

        if operation == "chat":
            message = str(kwargs.get("message") or "").strip().lower()
            for keywords, reply in _SCRIPTED_REPLIES:
                if all(k in message for k in keywords):
                    return json.dumps({"synthetic": True, "reply": reply}, indent=2)
            return json.dumps(
                {
                    "synthetic": True,
                    "reply": (
                        "This demo agent only replays three scripted prompts "
                        "(summary, blocking exceptions, workbook/deck). Try "
                        "one of those, or see the full production package "
                        "for open-ended analyst chat."
                    ),
                },
                indent=2,
            )

        return json.dumps({"status": "error", "message": f"Unknown operation: {operation}"})


if __name__ == "__main__":
    agent = NbcuFinanceReportingDemoAgent()
    print(agent.perform(operation="status"))
    print(agent.perform(operation="summary"))
    print(agent.perform(operation="exceptions"))
    print(agent.perform(operation="chat", message="Summarize Current Estimate versus Budget"))
