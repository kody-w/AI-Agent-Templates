"""Loan Application Intake & Affordability — steps 1-2 of the Loan
Origination & Credit Decisioning process flow.

Step 1 — Application Submission: Customer submits a loan application via
digital channel or branch. Copilot Studio guides the application process,
ensuring all required data is captured correctly. (Copilot Studio, Power Apps)

Step 2 — Open Banking Data: With customer consent, Azure AI analyses Open
Banking transaction data to generate an enriched income and expenditure view
for affordability assessment. (Azure AI, Open Banking Platform)

Operating laws: identify applicants by NATURAL reference (name or LN- ref);
'list' shows the pipeline; new applications are captured with a deterministic
next reference; affordability maths is real (46% essential / 21%
discretionary bands over verified income). Data home: Microsoft Dataverse.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

# The canonical loan-origination book. The SAME applicants flow through the
# sibling agents (credit decisioning, offer & drawdown, referred cases) so
# every hop of the demo tells one coherent story.
_CANON = [
    {"applicationId": "LN-73214", "applicantName": "Priya Sharma",
     "loanAmount": 32000, "loanPurpose": "home improvement", "channel": "web",
     "monthlyIncome": 4820.00, "stage": "credit decisioning"},
    {"applicationId": "LN-73198", "applicantName": "Marcus Webb",
     "loanAmount": 18500, "loanPurpose": "debt consolidation",
     "channel": "mobile", "monthlyIncome": 3110.00,
     "stage": "credit decisioning"},
    {"applicationId": "LN-73186", "applicantName": "Elena Rossi",
     "loanAmount": 45000, "loanPurpose": "home extension", "channel": "branch",
     "monthlyIncome": 5240.00, "stage": "offer presented"},
    {"applicationId": "LN-73171", "applicantName": "David Chen",
     "loanAmount": 12000, "loanPurpose": "vehicle purchase", "channel": "web",
     "monthlyIncome": 2870.00, "stage": "declined"},
    {"applicationId": "LN-73155", "applicantName": "Amara Okafor",
     "loanAmount": 27500, "loanPurpose": "wedding", "channel": "mobile",
     "monthlyIncome": 3980.00, "stage": "referred to underwriter"},
    {"applicationId": "LN-73102", "applicantName": "Sofia Petrov",
     "loanAmount": 22000, "loanPurpose": "kitchen renovation",
     "channel": "web", "monthlyIncome": 4160.00, "stage": "drawn down"},
]

_ESSENTIAL, _DISCRETIONARY = 0.46, 0.21


def _affordability(income):
    essential = round(income * _ESSENTIAL, 2)
    discretionary = round(income * _DISCRETIONARY, 2)
    surplus = round(income - essential - discretionary, 2)
    return essential, discretionary, surplus


class LoanApplicationIntake(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        'Show Loan Application Intake for applicantname LN-73214.',
        'Show me the application pipeline',
        'Capture a new loan application for Robin Hale, £20,000, home improvement',
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference (e.g. LN-73214) only. Keep answers under ~120 "
                "words, professional markdown, no emojis.")
    SYNTHETIC_DATA = [
        {**r, "monthlySurplus": _affordability(r["monthlyIncome"])[2]}
        for r in _CANON
    ]

    def __init__(self):
        self.name = "LoanApplicationIntake"
        self.metadata = {
            "name": self.name,
            "description": (
                "Captures loan applications from any channel (digital or "
                "branch) and builds the consented Open Banking affordability "
                "view — verified income, expenditure bands, and monthly "
                "surplus — for each applicant. Application data lives in "
                "Microsoft Dataverse. Identify applicants by NATURAL "
                "reference: a name like 'Priya Sharma' or a reference like "
                "LN-73214; never ask the user for internal identifiers."),
            "parameters": {
                "type": "object",
                "properties": {
                    "applicantName": {
                        "type": "string",
                        "description": ("Applicant name or LN- reference, "
                                        "e.g. 'Priya Sharma' or LN-73214. "
                                        "Pass the word: list to see the "
                                        "application pipeline - never ask "
                                        "the user for an id.")},
                    "loanAmount": {
                        "type": "number",
                        "description": ("Requested amount in GBP for a NEW "
                                        "application (optional).")},
                    "loanPurpose": {
                        "type": "string",
                        "description": "Purpose of a NEW loan (optional)."},
                    "channel": {
                        "type": "string",
                        "description": ("Channel for a NEW application: web, "
                                        "mobile, or branch (optional).")},
                    "monthlyIncome": {
                        "type": "number",
                        "description": ("Stated monthly income for a NEW "
                                        "application (optional).")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def _find(self, ref):
        low = ref.lower()
        return [r for r in _CANON
                if low in r["applicantName"].lower()
                or low == r["applicationId"].lower()]

    def perform(self, **kwargs):
        ref = str(kwargs.get("applicantName") or "").strip()
        if not ref or ref.lower() == "list":
            lines = ["## Application pipeline (Dataverse)"]
            lines += [f"{i}. **{r['applicationId']}** — {r['applicantName']}, "
                      f"£{r['loanAmount']:,} {r['loanPurpose']} "
                      f"({r['channel']}) — {r['stage']}"
                      for i, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name an applicant for their affordability view, or "
                         "give me a name, amount, and purpose to capture a "
                         "new application.")
            return "\n".join(lines)

        hits = self._find(ref)
        if not hits and kwargs.get("loanAmount"):
            # Step 1: capture a NEW application with the next reference.
            next_id = "LN-%d" % (max(int(r["applicationId"][3:])
                                     for r in _CANON) + 7)
            income = float(kwargs.get("monthlyIncome") or 3600)
            essential, discretionary, surplus = _affordability(income)
            return "\n".join([
                f"## Application captured — {next_id}",
                f"Applicant: {ref} | Channel: "
                f"{kwargs.get('channel') or 'web'} | Amount: "
                f"£{float(kwargs.get('loanAmount')):,.0f} | Purpose: "
                f"{kwargs.get('loanPurpose') or 'personal'}",
                "Required data complete: identity, address, employment, and "
                "Open Banking consent captured.",
                "",
                "### Open Banking affordability view (12-month, consented)",
                f"- Verified monthly income: £{income:,.2f}",
                f"- Essential expenditure (46%): £{essential:,.2f}",
                f"- Discretionary spend (21%): £{discretionary:,.2f}",
                f"- **Monthly surplus available: £{surplus:,.2f}**",
                "",
                f"Next: run the credit decision for {next_id}.",
            ])
        if not hits:
            near = ", ".join(f"{r['applicantName']} ({r['applicationId']})"
                             for r in _CANON[:3])
            return (f"No application matches `{ref}`. Applicants on the "
                    f"book include: {near}. Say 'list' for the full "
                    "pipeline.")
        r = hits[0]
        essential, discretionary, surplus = _affordability(r["monthlyIncome"])
        return "\n".join([
            f"## {r['applicationId']} — {r['applicantName']}",
            f"£{r['loanAmount']:,} {r['loanPurpose']} via {r['channel']} — "
            f"stage: **{r['stage']}**",
            "",
            "### Open Banking affordability view (consented)",
            f"- Verified monthly income: £{r['monthlyIncome']:,.2f}",
            f"- Essential expenditure (46%): £{essential:,.2f}",
            f"- Discretionary spend (21%): £{discretionary:,.2f}",
            f"- **Monthly surplus available: £{surplus:,.2f}**",
            "",
            f"Next: run the credit decision for {r['applicationId']}.",
        ])
