"""Credit Decisioning & Fraud Risk Scoring — steps 3-4 of the Loan
Origination & Credit Decisioning process flow.

Step 3 — Credit Decisioning: The credit decision engine runs an automated
scorecard incorporating bureau data, application data, and behavioural
scores. Azure AI flags anomaly cases. (Azure AI / ML, Credit Decision
Engine, Credit Bureau API)

Step 4 — Fraud Risk Scoring: The fraud risk engine runs concurrently with
the credit decision, assessing identity, device, and application-level
fraud indicators. (Azure AI, Fraud Prevention Platform)

Decision rules are REAL and deterministic: APPROVE when bureau >= 720 and
fraud < 0.15 with no anomaly; DECLINE when bureau < 620 or fraud >= 0.25;
otherwise REFER to an underwriter. Data home: Microsoft Dataverse.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

# Canonical book — same applicants as the intake / offer / referred agents.
_CANON = [
    {"applicationId": "LN-73214", "applicantName": "Priya Sharma",
     "loanAmount": 32000, "bureauScore": 742, "behaviouralScore": 83,
     "fraudScore": 0.11, "anomalyFlag": "income variance"},
    {"applicationId": "LN-73198", "applicantName": "Marcus Webb",
     "loanAmount": 18500, "bureauScore": 648, "behaviouralScore": 66,
     "fraudScore": 0.09, "anomalyFlag": "none"},
    {"applicationId": "LN-73186", "applicantName": "Elena Rossi",
     "loanAmount": 45000, "bureauScore": 781, "behaviouralScore": 88,
     "fraudScore": 0.06, "anomalyFlag": "none"},
    {"applicationId": "LN-73171", "applicantName": "David Chen",
     "loanAmount": 12000, "bureauScore": 598, "behaviouralScore": 58,
     "fraudScore": 0.13, "anomalyFlag": "thin file"},
    {"applicationId": "LN-73155", "applicantName": "Amara Okafor",
     "loanAmount": 27500, "bureauScore": 733, "behaviouralScore": 79,
     "fraudScore": 0.21, "anomalyFlag": "device indicator"},
    {"applicationId": "LN-73102", "applicantName": "Sofia Petrov",
     "loanAmount": 22000, "bureauScore": 758, "behaviouralScore": 85,
     "fraudScore": 0.05, "anomalyFlag": "none"},
]


def _decide(r):
    """The scorecard, applied for real. Returns (decision, rationale)."""
    anomaly = r["anomalyFlag"] not in ("", "none", None)
    if r["bureauScore"] < 620 or r["fraudScore"] >= 0.25:
        return "DECLINE", "scorecard below cut-off or fraud outside appetite"
    if r["bureauScore"] >= 720 and r["fraudScore"] < 0.15 and not anomaly:
        return "APPROVE", ("scorecard cleared cut-off, no anomaly flags, "
                           "fraud inside appetite")
    return "REFER", ("borderline scorecard or anomaly flag — route to an "
                     "underwriter with the full AI assessment")


class CreditDecisionEngine(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        'Show Credit Decision Engine for applicantname LN-73214.',
        'Run the credit decision for Elena Rossi',
        'Which applications are on the decision queue?',
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference (e.g. LN-73214) only. Keep answers under ~120 "
                "words, professional markdown, no emojis.")
    SYNTHETIC_DATA = [
        {**r, "decision": _decide(r)[0]} for r in _CANON
    ]

    def __init__(self):
        self.name = "CreditDecisionEngine"
        self.metadata = {
            "name": self.name,
            "description": (
                "Runs the automated credit scorecard (bureau + application + "
                "behavioural scores, from the Credit Bureau API) and the "
                "concurrent Azure AI fraud risk assessment (identity, device, "
                "application-level indicators) for a loan application, "
                "returning APPROVE / REFER / DECLINE with the rationale. "
                "Decisions are recorded in Microsoft Dataverse. Identify the "
                "case by NATURAL reference: applicant name or LN- reference."),
            "parameters": {
                "type": "object",
                "properties": {
                    "applicantName": {
                        "type": "string",
                        "description": ("Applicant name or LN- reference, "
                                        "e.g. 'Elena Rossi' or LN-73186. "
                                        "Pass the word: list to see every "
                                        "pending decision - never ask the "
                                        "user for an id.")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def perform(self, **kwargs):
        ref = str(kwargs.get("applicantName") or "").strip()
        if not ref or ref.lower() == "list":
            lines = ["## Credit decisions (scorecard applied live)"]
            for r in _CANON:
                d, _ = _decide(r)
                lines.append(f"- **{r['applicationId']}** "
                             f"{r['applicantName']} £{r['loanAmount']:,} — "
                             f"bureau {r['bureauScore']}, fraud "
                             f"{r['fraudScore']:.2f} → **{d}**")
            lines.append("")
            lines.append("Name an applicant for the full assessment.")
            return "\n".join(lines)
        low = ref.lower()
        hits = [r for r in _CANON if low in r["applicantName"].lower()
                or low == r["applicationId"].lower()]
        if not hits:
            return (f"No application matches `{ref}`. Say 'list' to see "
                    "every case on the decision queue.")
        r = hits[0]
        decision, rationale = _decide(r)
        anomaly = r["anomalyFlag"] not in ("", "none", None)
        nxt = {"APPROVE": f"present the offer for {r['applicationId']}",
               "REFER": f"open the referred case for {r['applicationId']}",
               "DECLINE": "capture the decline reason letter"}[decision]
        return "\n".join([
            f"## Credit decision — {r['applicationId']} "
            f"({r['applicantName']}, £{r['loanAmount']:,})",
            f"- Bureau score: {r['bureauScore']} (cut-off 620, approve band "
            "720+)",
            f"- Behavioural score: {r['behaviouralScore']}/100",
            f"- Fraud risk score: {r['fraudScore']:.2f} (identity, device, "
            "application indicators; appetite < 0.15)",
            f"- Azure AI anomaly flag: "
            f"{r['anomalyFlag'] if anomaly else 'none'}",
            "",
            f"**Decision: {decision}** — {rationale}.",
            "Decision and rationale recorded for model feedback and "
            "governance MI.",
            f"Next: {nxt}.",
        ])
