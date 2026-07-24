"""Offer Presentation & Drawdown Processing — steps 5-6 of the Loan
Origination & Credit Decisioning process flow.

Step 5 — Offer Presentation: Approved applicants receive a personalised
offer via Copilot Studio. The offer presentation is dynamically optimised
for conversion while staying within risk appetite. (Copilot Studio)

Step 6 — Drawdown Processing: Accepted offers trigger automated drawdown
processing in the core banking system. Funds are credited within the
required regulatory timeframe. (Power Automate, Core Banking System)

Repayments use REAL annuity maths: payment = P*r / (1 - (1+r)^-n) at the
offer's monthly rate over the term. Offer state lives in Microsoft
Dataverse; drawdown runs only on explicit acceptance.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

# Canonical offers — approved applicants from the credit-decision agent.
_CANON = [
    {"applicationId": "LN-73186", "applicantName": "Elena Rossi",
     "loanAmount": 45000, "apr": 6.4, "termMonths": 60,
     "offerStatus": "presented — awaiting acceptance"},
    {"applicationId": "LN-73102", "applicantName": "Sofia Petrov",
     "loanAmount": 22000, "apr": 7.1, "termMonths": 48,
     "offerStatus": "accepted — drawdown complete, funds credited T+1"},
    {"applicationId": "LN-73088", "applicantName": "James Whitfield",
     "loanAmount": 15500, "apr": 8.2, "termMonths": 36,
     "offerStatus": "accepted — drawdown complete, funds credited T+1"},
    {"applicationId": "LN-73076", "applicantName": "Nadia Hussain",
     "loanAmount": 30000, "apr": 5.9, "termMonths": 60,
     "offerStatus": "expired — 30-day validity lapsed"},
]


def _repayment(amount, apr, months):
    """Standard annuity payment at apr% nominal, monthly compounding."""
    r = apr / 100.0 / 12.0
    if r == 0:
        return round(amount / months, 2)
    return round(amount * r / (1.0 - (1.0 + r) ** -months), 2)


class LoanOfferDrawdown(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        'Show Loan Offer Drawdown for applicantname LN-73186.',
        'Present the offer for Elena Rossi',
        'Elena accepts the offer — run drawdown',
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference (e.g. LN-73214) only. Keep answers under ~120 "
                "words, professional markdown, no emojis.")
    SYNTHETIC_DATA = [
        {**o, "monthlyRepayment": _repayment(o["loanAmount"], o["apr"],
                                             o["termMonths"])}
        for o in _CANON
    ]

    def __init__(self):
        self.name = "LoanOfferDrawdown"
        self.metadata = {
            "name": self.name,
            "description": (
                "Presents the personalised loan offer for an approved "
                "applicant — APR, term, and a correctly computed monthly "
                "repayment, optimised for conversion within risk appetite — "
                "and on explicit acceptance runs automated drawdown in the "
                "core banking system with funds credited inside the "
                "regulatory timeframe (T+1). Offer records live in Microsoft "
                "Dataverse. Identify offers by NATURAL reference: applicant "
                "name or LN- reference."),
            "parameters": {
                "type": "object",
                "properties": {
                    "applicantName": {
                        "type": "string",
                        "description": ("Applicant name or LN- reference, "
                                        "e.g. 'Elena Rossi' or LN-73186. "
                                        "Pass the word: list to see every "
                                        "open offer - never ask the user "
                                        "for an id.")},
                    "accepted": {
                        "type": "string",
                        "description": ("Set to 'yes' when the customer "
                                        "accepts, to run drawdown "
                                        "(optional).")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def perform(self, **kwargs):
        ref = str(kwargs.get("applicantName") or "").strip()
        accepted = str(kwargs.get("accepted") or "").strip().lower() in (
            "yes", "y", "true", "accept", "accepted")
        if not ref or ref.lower() == "list":
            lines = ["## Offer book (Dataverse)"]
            for o in _CANON:
                pay = _repayment(o["loanAmount"], o["apr"], o["termMonths"])
                lines.append(f"- **{o['applicationId']}** "
                             f"{o['applicantName']} £{o['loanAmount']:,} @ "
                             f"{o['apr']}% x {o['termMonths']}mo "
                             f"(£{pay:,.2f}/mo) — {o['offerStatus']}")
            lines.append("")
            lines.append("Name an applicant to present or act on their "
                         "offer.")
            return "\n".join(lines)
        low = ref.lower()
        hits = [o for o in _CANON if low in o["applicantName"].lower()
                or low == o["applicationId"].lower()]
        if not hits:
            return (f"No offer matches `{ref}`. Offers exist for: "
                    + ", ".join(o["applicantName"] for o in _CANON)
                    + ". Say 'list' for the offer book.")
        o = hits[0]
        pay = _repayment(o["loanAmount"], o["apr"], o["termMonths"])
        total = round(pay * o["termMonths"], 2)
        lines = [
            f"## Personalised offer — {o['applicationId']} "
            f"({o['applicantName']})",
            f"- Amount: £{o['loanAmount']:,}  |  APR: {o['apr']}% "
            "representative",
            f"- Term: {o['termMonths']} months  |  Monthly repayment: "
            f"**£{pay:,.2f}**  |  Total repayable: £{total:,.2f}",
            f"- Status: {o['offerStatus']}",
        ]
        if accepted and "presented" in o["offerStatus"]:
            lines += [
                "",
                "### Drawdown processed",
                f"- Core banking instruction {o['applicationId']}-DD "
                "executed via Power Automate.",
                "- Funds credited to the nominated account inside the "
                "regulatory timeframe (T+1).",
                "- Welcome pack and first-repayment schedule issued.",
            ]
        elif accepted:
            lines += ["", f"This offer is not open for acceptance "
                          f"({o['offerStatus']})."]
        else:
            lines += ["", "Say 'accept the offer' to trigger drawdown, or "
                          "ask for the portfolio scoreboard."]
        return "\n".join(lines)
