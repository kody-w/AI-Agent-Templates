"""Customer Query Resolution & Payments Analytics — steps 7-8 of the
Payments Operations Excellence process flow.

Step 7 — Customer Query Resolution: Payment tracking queries from customers
and corporates are resolved with real-time payment status from the payment
platform. (Copilot Studio, Payment Platform)

Step 8 — Payments Analytics: Volumes, values, STP rates, and scheme
compliance metrics are tracked across all payment types and rails.
(Power BI)

Tracking statuses cohere with the rest of the suite: the sanctions hold
(PAY-731162), the fraud hold (PAY-731130), and the settled/in-flight
payments all match the ingestion, exception, and fraud agents' canon; the
scoreboard's 4 open exceptions and 3 holds are exactly those items. Data
home: Microsoft Dataverse.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_TRACKING = [
    {"paymentReference": "PAY-731150", "beneficiaryName": "Woodgrove Bank plc",
     "amount": "GBP 18,000.00", "rail": "Faster Payments",
     "trackStatus": "SETTLED",
     "timeline": "received 09:14 -> screened 09:14 -> released 09:16 -> "
                 "settled 09:21"},
    {"paymentReference": "PAY-731149", "beneficiaryName": "Lucerne Publishing",
     "amount": "EUR 7,320.00", "rail": "SEPA",
     "trackStatus": "IN FLIGHT",
     "timeline": "received 09:02 -> screened 09:02 -> released 09:03 -> "
                 "awaiting beneficiary bank confirmation"},
    {"paymentReference": "PAY-731162", "beneficiaryName": "Contoso Pharmaceuticals",
     "amount": "USD 275,000.00", "rail": "SWIFT",
     "trackStatus": "HELD - sanctions review",
     "timeline": "received 08:55 -> screening match 08:55 -> compliance "
                 "case PAY-731162-SCR open"},
    {"paymentReference": "PAY-731130", "beneficiaryName": "Tailspin Toys",
     "amount": "GBP 5,600.00", "rail": "Faster Payments",
     "trackStatus": "HELD - fraud verification",
     "timeline": "received 08:47 -> screened 08:47 -> fraud score 0.31 -> "
                 "customer verification in progress"},
]

_SCOREBOARD = [
    ("Volume today", "41,208 instructions"),
    ("Value today", "£1.92B across all rails"),
    ("STP rate", "96.8% (target 96.5%)"),
    ("Open STP exceptions", "4 (PAY-731205, PAY-731198, PAY-731184, "
                            "PAY-731171)"),
    ("Payments on hold", "3 (1 sanctions, 1 duplicate, 1 fraud)"),
    ("By rail", "Faster Payments 31,455 | SEPA 6,210 | CHAPS 2,481 | "
                "SWIFT 1,062"),
    ("Scheme compliance", "CHAPS same-day 100% | SEPA SCT Inst 9.4s avg "
                          "settlement"),
]


class PaymentQueryAnalytics(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "Show Payment Query Analytics for paymentreference PAY-731150.",
        "Where is the payment to Woodgrove Bank?",
        "Show me today's payments analytics scoreboard",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, "
                "or fabricate URLs, deep links, or Power Apps/Power BI links "
                "— the packaged demo data contains no links. Refer to records "
                "by their plain reference (e.g. PAY-731150) only. Keep "
                "answers under ~120 words, professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_TRACKING)

    def __init__(self):
        self.name = "PaymentQueryAnalytics"
        self.metadata = {
            "name": self.name,
            "description": (
                "Resolves 'where is my payment?' tracking queries with the "
                "real-time status and timeline from the payment platform "
                "(records in Microsoft Dataverse), and serves the payments "
                "analytics scoreboard — volumes, values, STP rate, holds, "
                "and scheme compliance across all rails. Identify a payment "
                "by NATURAL reference (PAY- reference or beneficiary name); "
                "ask for 'analytics' for the scoreboard; never ask the user "
                "for internal identifiers."),
            "parameters": {
                "type": "object",
                "properties": {
                    "paymentReference": {
                        "type": "string",
                        "description": ("Payment to track, e.g. PAY-731150 "
                                        "or 'Woodgrove Bank'. Pass the "
                                        "word: list to see every tracked "
                                        "payment - never ask the user for "
                                        "an id.")},
                    "view": {
                        "type": "string",
                        "description": ("Set to 'analytics' for the "
                                        "payments scoreboard (optional).")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def perform(self, **kwargs):
        view = str(kwargs.get("view") or "").strip().lower()
        ref = str(kwargs.get("paymentReference") or "").strip()
        low = ref.lower()
        if view.startswith("analytic") or low == "analytics":
            lines = ["## Payments analytics — today's scoreboard"]
            lines += [f"- {k}: {v}" for k, v in _SCOREBOARD]
            lines.append("")
            lines.append("Name a payment reference or beneficiary to track "
                         "an individual payment.")
            return "\n".join(lines)
        if not ref or low == "list":
            lines = ["## Tracked payments (real-time status)"]
            lines += [f"{i}. **{t['paymentReference']}** — "
                      f"{t['beneficiaryName']}, {t['amount']} via "
                      f"{t['rail']} — **{t['trackStatus']}**"
                      for i, t in enumerate(_TRACKING, 1)]
            lines.append("")
            lines.append("Open one for its timeline, or ask for "
                         "'analytics' for the scoreboard.")
            return "\n".join(lines)
        hit = next((t for t in _TRACKING
                    if low == t["paymentReference"].lower()
                    or low in t["beneficiaryName"].lower()), None)
        if not hit:
            return (f"No tracked payment matches `{ref}`. Say 'list' for "
                    "every tracked payment or 'analytics' for the "
                    "scoreboard.")
        return "\n".join([
            f"## Payment tracking — {hit['paymentReference']} "
            f"({hit['beneficiaryName']})",
            f"- Amount: {hit['amount']} | Rail: {hit['rail']}",
            f"- Real-time status: **{hit['trackStatus']}**",
            f"- Timeline: {hit['timeline']}.",
            "",
            "The beneficiary bank confirmation reference is available on "
            "request.",
        ])
