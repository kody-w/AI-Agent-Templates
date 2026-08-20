"""Referred Case Management & Portfolio MI — steps 7-8 of the Loan
Origination & Credit Decisioning process flow.

Step 7 — Referred Case Management: Referred applications are presented to
underwriters with a full AI-generated assessment. Decision and rationale
are captured for model feedback. (Power Apps, Copilot Studio)

Step 8 — Portfolio MI: Approval rates, bad debt by vintage, and model
performance are tracked at a scoreboard level for governance committee
review. (Power BI)

The referral queue is EXACTLY the REFER outcomes from the credit-decision
agent (same canonical book), and the scoreboard's decision split is
computed from those rows — the story stays coherent hop to hop. Data home:
Microsoft Dataverse.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

# Referred cases = the REFER rows of the canonical book, with the AI
# assessment an underwriter sees in Power Apps.
_QUEUE = [
    {"caseReference": "LN-73214", "applicantName": "Priya Sharma",
     "amount": 32000, "aiAssessment": ("bureau 742 / fraud 0.11 — income "
                                       "variance anomaly: two salary sources "
                                       "in the Open Banking view"),
     "queueStatus": "awaiting underwriter"},
    {"caseReference": "LN-73198", "applicantName": "Marcus Webb",
     "amount": 18500, "aiAssessment": ("bureau 648 — borderline scorecard; "
                                       "strong affordability surplus "
                                       "£1,026/mo"),
     "queueStatus": "awaiting underwriter"},
    {"caseReference": "LN-73155", "applicantName": "Amara Okafor",
     "amount": 27500, "aiAssessment": ("fraud 0.21 — new-device indicator; "
                                       "identity and bureau both strong"),
     "queueStatus": "awaiting underwriter"},
]

_SCOREBOARD = {
    "approvalRate": "68.4% (+2.1pts vs prior month)",
    "autoDecisionRate": "81.2%",
    "referralRate": "13.6%",
    "badDebtByVintage": "2024H2 0.9% | 2025H1 1.2% | 2025H2 1.4% (watch)",
    "scorecardGini": "0.61 (stable)",
    "fraudModelAuc": "0.88",
}


class ReferredCasePortfolio(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        'Show Referred Case Portfolio for casereference LN-73214.',
        'Which referred applications await an underwriter?',
        'Show me the portfolio governance scoreboard',
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference (e.g. LN-73214) only. Keep answers under ~120 "
                "words, professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_QUEUE)

    def __init__(self):
        self.name = "ReferredCasePortfolio"
        self.metadata = {
            "name": self.name,
            "description": (
                "Works the underwriter referral queue and the governance "
                "portfolio scoreboard, both held in Microsoft Dataverse. "
                "With no inputs it lists the referred applications with "
                "their full AI-generated assessments; given a case and a "
                "decision it records the outcome and rationale for model "
                "feedback; ask for 'portfolio' to get the governance "
                "scoreboard (approval rates, bad debt by vintage, model "
                "performance)."),
            "parameters": {
                "type": "object",
                "properties": {
                    "caseReference": {
                        "type": "string",
                        "description": ("Referred case to open or decide, "
                                        "e.g. LN-73214 or an applicant "
                                        "name. Pass the word: list for the "
                                        "queue - never ask the user for an "
                                        "id.")},
                    "decision": {
                        "type": "string",
                        "description": ("Underwriter decision to record: "
                                        "approve or decline (optional).")},
                    "rationale": {
                        "type": "string",
                        "description": ("Decision rationale, captured for "
                                        "model feedback (optional).")},
                    "view": {
                        "type": "string",
                        "description": ("Set to 'portfolio' for the "
                                        "governance MI scoreboard "
                                        "(optional).")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def perform(self, **kwargs):
        view = str(kwargs.get("view") or "").strip().lower()
        ref = str(kwargs.get("caseReference") or "").strip()
        decision = str(kwargs.get("decision") or "").strip().lower()
        if view.startswith("portfolio"):
            s = _SCOREBOARD
            return "\n".join([
                "## Portfolio MI — governance scoreboard (Power BI)",
                f"- Approval rate (rolling 30d): {s['approvalRate']}",
                f"- Auto-decision rate: {s['autoDecisionRate']} | "
                f"Referral rate: {s['referralRate']}",
                f"- Referred cases open now: {len(_QUEUE)} "
                "(all awaiting underwriter)",
                f"- Bad debt by vintage: {s['badDebtByVintage']}",
                f"- Scorecard Gini: {s['scorecardGini']} | Fraud model "
                f"AUC: {s['fraudModelAuc']}",
                "- Next governance committee review: first Tuesday of the "
                "month.",
            ])
        low = ref.lower()
        hit = next((c for c in _QUEUE if low == c["caseReference"].lower()
                    or (low and low in c["applicantName"].lower())), None)
        if hit and decision:
            return "\n".join([
                f"## Decision recorded — {hit['caseReference']} "
                f"({hit['applicantName']})",
                f"- Underwriter decision: **{decision.upper()}**",
                f"- Rationale: {kwargs.get('rationale') or 'captured'}",
                "- Fed back to the decisioning model and logged for "
                "governance MI.",
                "Ask for 'portfolio' to see the scoreboard.",
            ])
        if hit:
            return "\n".join([
                f"## Referred case — {hit['caseReference']} "
                f"({hit['applicantName']}, £{hit['amount']:,})",
                f"- AI assessment: {hit['aiAssessment']}",
                f"- Status: {hit['queueStatus']}",
                "",
                f"Record an outcome with e.g. 'approve "
                f"{hit['caseReference']} — variance explained by contract "
                "renewal'.",
            ])
        lines = ["## Referred applications awaiting an underwriter"]
        lines += [f"{i}. **{c['caseReference']}** — {c['applicantName']}, "
                  f"£{c['amount']:,} — {c['aiAssessment']}"
                  for i, c in enumerate(_QUEUE, 1)]
        lines.append("")
        lines.append("Open a case by reference or name, or ask for "
                     "'portfolio' for the governance scoreboard.")
        return "\n".join(lines)
