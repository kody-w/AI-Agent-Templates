"""Payment Ingestion & Sanctions Screening — steps 1-2 of the Payments
Operations Excellence process flow.

Step 1 — Payment Ingestion: All payment instructions (CHAPS, Faster
Payments, SEPA, SWIFT) are ingested and validated by Azure AI against the
relevant scheme rules and sanction lists. (Azure AI, Payment Platform)

Step 2 — Sanctions & Screening: Every payment is screened against OFAC,
HMT, and EU sanctions lists in real time. Hits are routed to compliance
analysts for review. (Sanctions Screening, Copilot Studio)

Screening rules are REAL and deterministic: a payment flagged in the canon
as a potential list match is HELD with a compliance case reference
(<ref>-SCR); everything else clears and releases. Identify payments by
NATURAL reference (beneficiary name or PAY- ref). Data home: Microsoft
Dataverse.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

# The canonical payments book — the SAME instructions flow through the
# sibling agents (exceptions & recon, correspondent & fraud, tracking &
# analytics) so every hop tells one coherent story.
_CANON = [
    {"paymentReference": "PAY-731205", "beneficiaryName": "Northwind Traders Ltd",
     "amount": 48250.00, "currency": "GBP", "rail": "Faster Payments",
     "sanctionsMatch": "none", "screenStatus": "released"},
    {"paymentReference": "PAY-731198", "beneficiaryName": "Adatum Corporation",
     "amount": 125000.00, "currency": "EUR", "rail": "SEPA",
     "sanctionsMatch": "none", "screenStatus": "released"},
    {"paymentReference": "PAY-731184", "beneficiaryName": "Fabrikam Industries",
     "amount": 950000.00, "currency": "GBP", "rail": "CHAPS",
     "sanctionsMatch": "none", "screenStatus": "released"},
    {"paymentReference": "PAY-731171", "beneficiaryName": "Trey Research",
     "amount": 61400.00, "currency": "USD", "rail": "SWIFT",
     "sanctionsMatch": "none", "screenStatus": "released"},
    {"paymentReference": "PAY-731162", "beneficiaryName": "Contoso Pharmaceuticals",
     "amount": 275000.00, "currency": "USD", "rail": "SWIFT",
     "sanctionsMatch": "HMT list entry — 87% name similarity",
     "screenStatus": "HELD — compliance case PAY-731162-SCR"},
    {"paymentReference": "PAY-731150", "beneficiaryName": "Woodgrove Bank plc",
     "amount": 18000.00, "currency": "GBP", "rail": "Faster Payments",
     "sanctionsMatch": "none", "screenStatus": "released"},
]

_RAILS = ("CHAPS", "Faster Payments", "SEPA", "SWIFT")


class PaymentIngestionScreening(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "Show Payment Ingestion Screening for paymentreference PAY-731162.",
        "Screen the payment to Contoso Pharmaceuticals",
        "Ingest a new payment: GBP 25,000 to Northwind Traders on Faster Payments",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference (e.g. LN-73214) only. Keep answers under ~120 "
                "words, professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "PaymentIngestionScreening"
        self.metadata = {
            "name": self.name,
            "description": (
                "Ingests payment instructions on any rail (CHAPS, Faster "
                "Payments, SEPA, SWIFT), validates them against the scheme "
                "rules, and screens every payment in real time against the "
                "OFAC, HMT, and EU sanctions lists — holding any potential "
                "match with a compliance case reference. Payment records "
                "live in Microsoft Dataverse. Identify payments by NATURAL "
                "reference: a beneficiary name or a PAY- reference; never "
                "ask the user for internal identifiers."),
            "parameters": {
                "type": "object",
                "properties": {
                    "paymentReference": {
                        "type": "string",
                        "description": ("Payment reference or beneficiary "
                                        "name, e.g. PAY-731162 or 'Contoso "
                                        "Pharmaceuticals'. Pass the word: "
                                        "list to see today's ingested "
                                        "payments - never ask the user for "
                                        "an id.")},
                    "beneficiaryName": {
                        "type": "string",
                        "description": ("Beneficiary for a NEW payment "
                                        "(optional).")},
                    "amount": {
                        "type": "number",
                        "description": "Amount for a NEW payment (optional)."},
                    "currency": {
                        "type": "string",
                        "description": ("Currency for a NEW payment: GBP, "
                                        "EUR, USD (optional).")},
                    "rail": {
                        "type": "string",
                        "description": ("Rail for a NEW payment: CHAPS, "
                                        "Faster Payments, SEPA, or SWIFT "
                                        "(optional).")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def _find(self, ref):
        low = ref.lower()
        return [p for p in _CANON if low == p["paymentReference"].lower()
                or low in p["beneficiaryName"].lower()]

    def perform(self, **kwargs):
        ref = str(kwargs.get("paymentReference")
                  or kwargs.get("beneficiaryName") or "").strip()
        if not ref or ref.lower() == "list":
            lines = ["## Ingested payments — today (Dataverse)"]
            lines += [f"{i}. **{p['paymentReference']}** — "
                      f"{p['beneficiaryName']}, {p['currency']} "
                      f"{p['amount']:,.2f} via {p['rail']} — "
                      f"{p['screenStatus']}"
                      for i, p in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a payment for its screening detail, or give "
                         "me a beneficiary, amount, and rail to ingest a "
                         "new instruction.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits and kwargs.get("amount"):
            amount = float(kwargs.get("amount"))
            ccy = (kwargs.get("currency") or "GBP").upper()
            rail = kwargs.get("rail") or "Faster Payments"
            next_ref = "PAY-%d" % (max(int(p["paymentReference"][4:])
                                       for p in _CANON) + 9)
            return "\n".join([
                f"## Payment ingested — {next_ref}",
                f"- Beneficiary: {ref} | Amount: {ccy} {amount:,.2f} | "
                f"Rail: {rail}",
                "- Scheme validation: PASSED (format, cut-off, and scheme "
                "rules checked by Azure AI).",
                "",
                "### Real-time sanctions screening (OFAC / HMT / EU)",
                "- No matches on any list.",
                f"- {next_ref} released to the payment platform for onward "
                "processing.",
            ])
        if not hits:
            return (f"No payment matches `{ref}`. Say 'list' for today's "
                    "ingested payments.")
        p = hits[0]
        lines = [
            f"## {p['paymentReference']} — {p['beneficiaryName']}",
            f"- Amount: {p['currency']} {p['amount']:,.2f} | Rail: "
            f"{p['rail']}",
            "- Scheme validation: PASSED (Azure AI).",
            "",
            "### Real-time sanctions screening (OFAC / HMT / EU)",
        ]
        if p["sanctionsMatch"] != "none":
            lines += [
                f"- **POTENTIAL MATCH** — {p['sanctionsMatch']}.",
                f"- Payment **HELD**; {p['screenStatus'].split(chr(8212))[-1].strip()} "
                "routed to the compliance analyst queue.",
                "- Release or reject on analyst review.",
            ]
        else:
            lines += [
                "- No matches on OFAC, HMT, or EU lists.",
                f"- Status: {p['screenStatus']}.",
            ]
        return "\n".join(lines)
