"""Correspondent Banking Management & Fraud Prevention — steps 5-6 of the
Payments Operations Excellence process flow.

Step 5 — Correspondent Banking Management: Correspondent banking
relationship data and limit monitoring is tracked, with alerts for limit
breaches and nostro funding requirements. (Copilot Studio)

Step 6 — Fraud Prevention: Transaction-level fraud indicators are assessed
by Azure AI before payment release. Suspicious payments trigger a customer
verification journey. (Azure AI, Copilot Studio)

Fraud rules are REAL and deterministic: a pre-release fraud score >= 0.25
HOLDS the payment and triggers the verification journey; below releases.
The limit board ties to the reconciliation agent's nostro items (JPMorgan
USD top-up, Deutsche Bank EUR). Data home: Microsoft Dataverse.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CORRESPONDENTS = [
    {"correspondentName": "Deutsche Bank AG", "currency": "EUR",
     "limitUtilisation": 0.78, "limitStatus": "within limit",
     "nostroNote": "EUR nostro carries unreconciled item NOS-4468"},
    {"correspondentName": "JPMorgan Chase NY", "currency": "USD",
     "limitUtilisation": 0.91, "limitStatus": "APPROACHING LIMIT",
     "nostroNote": "top-up USD 40M recommended before the New York window; "
                   "USD nostro awaiting credit NOS-4471"},
    {"correspondentName": "MUFG Tokyo", "currency": "JPY",
     "limitUtilisation": 0.44, "limitStatus": "within limit",
     "nostroNote": "no action needed"},
    {"correspondentName": "BNP Paribas", "currency": "EUR",
     "limitUtilisation": 0.62, "limitStatus": "within limit",
     "nostroNote": "no action needed"},
    {"correspondentName": "Standard Chartered SG", "currency": "SGD",
     "limitUtilisation": 0.53, "limitStatus": "within limit",
     "nostroNote": "no action needed"},
]

_FRAUD = [
    {"paymentReference": "PAY-731205", "beneficiaryName": "Northwind Traders Ltd",
     "fraudScore": 0.04},
    {"paymentReference": "PAY-731198", "beneficiaryName": "Adatum Corporation",
     "fraudScore": 0.07},
    {"paymentReference": "PAY-731171", "beneficiaryName": "Trey Research",
     "fraudScore": 0.19},
    {"paymentReference": "PAY-731130", "beneficiaryName": "Tailspin Toys",
     "fraudScore": 0.31},
]

_HOLD_AT = 0.25


class CorrespondentFraudMonitor(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "Show Correspondent Fraud Monitor for view limits",
        "Run the pre-release fraud assessment for PAY-731130",
        "Which correspondent banks are approaching their limits?",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, "
                "or fabricate URLs, deep links, or Power Apps/Power BI links "
                "— the packaged demo data contains no links. Refer to records "
                "by their plain reference (e.g. PAY-731130) only. Keep "
                "answers under ~120 words, professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CORRESPONDENTS)

    def __init__(self):
        self.name = "CorrespondentFraudMonitor"
        self.metadata = {
            "name": self.name,
            "description": (
                "Monitors correspondent banking limits and nostro funding "
                "from the correspondent workspace in Microsoft Dataverse "
                "(flagging limit breaches and top-up needs), and runs the "
                "Azure AI pre-release fraud assessment — a score of 0.25 or "
                "higher holds the payment and triggers the customer "
                "verification journey. Ask for the limit board, or name a "
                "payment (PAY- reference or beneficiary) to assess it; "
                "never ask the user for internal identifiers."),
            "parameters": {
                "type": "object",
                "properties": {
                    "view": {
                        "type": "string",
                        "description": ("Set to 'limits' for the "
                                        "correspondent limit and nostro "
                                        "funding board. Pass the word: list "
                                        "for the same view - never ask the "
                                        "user for an id.")},
                    "paymentReference": {
                        "type": "string",
                        "description": ("Payment to fraud-assess before "
                                        "release, e.g. PAY-731130 or a "
                                        "beneficiary name (optional).")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def perform(self, **kwargs):
        ref = str(kwargs.get("paymentReference") or "").strip()
        low = ref.lower()
        if ref and low not in ("list", "limits"):
            hit = next((f for f in _FRAUD
                        if low == f["paymentReference"].lower()
                        or low in f["beneficiaryName"].lower()), None)
            if not hit:
                names = ", ".join(f["paymentReference"] for f in _FRAUD)
                return (f"No pre-release assessment matches `{ref}`. "
                        f"Assessable payments: {names}.")
            held = hit["fraudScore"] >= _HOLD_AT
            lines = [
                f"## Pre-release fraud assessment — "
                f"{hit['paymentReference']} ({hit['beneficiaryName']})",
                f"- Transaction fraud score (Azure AI): "
                f"**{hit['fraudScore']:.2f}** (hold threshold "
                f"{_HOLD_AT:.2f})",
                "- Indicators assessed: velocity, beneficiary novelty, "
                "device and session signals.",
            ]
            if held:
                lines += [
                    "- **SUSPICIOUS — payment HELD.** Customer verification "
                    "journey triggered (push notification + step-up).",
                    "- Release or cancel on the verification outcome.",
                ]
            else:
                lines += ["- Inside appetite — payment released."]
            return "\n".join(lines)
        lines = ["## Correspondent banking — limits & nostro funding"]
        lines += [f"{i}. **{c['correspondentName']}** ({c['currency']}) — "
                  f"limit utilisation {c['limitUtilisation']:.0%} — "
                  f"{c['limitStatus']} — {c['nostroNote']}"
                  for i, c in enumerate(_CORRESPONDENTS, 1)]
        lines += ["", "JPMorgan USD utilisation has breached the 90% "
                      "early-warning threshold — recommend a USD 40M nostro "
                      "top-up before the New York window. Name a payment to "
                      "run its pre-release fraud assessment."]
        return "\n".join(lines)
