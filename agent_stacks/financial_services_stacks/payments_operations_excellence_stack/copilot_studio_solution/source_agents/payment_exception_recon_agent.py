"""Exception Handling & Reconciliation — steps 3-4 of the Payments
Operations Excellence process flow.

Step 3 — Exception Handling: STP failures are routed to operations agents
with a cause analysis and suggested repair action. (Copilot Studio)

Step 4 — Reconciliation: Nostro and payment position reconciliation runs
automatically via Power Automate. Unreconciled items are flagged and
investigated. (Power Automate, ERP Finance Module)

The exception queue is drawn from the SAME canonical payments book as the
ingestion agent (PAY-731205/198/184/171), and the unreconciled nostro items
tie to the correspondent agent's limit board (JPMorgan USD, Deutsche Bank
EUR). 'repair <ref>' applies the suggested fix. Data home: Microsoft
Dataverse.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_EXCEPTIONS = [
    {"reference": "PAY-731205", "beneficiaryName": "Northwind Traders Ltd",
     "cause": "invalid beneficiary IBAN checksum",
     "repairAction": "correct the IBAN via customer callback, resubmit same-day"},
    {"reference": "PAY-731198", "beneficiaryName": "Adatum Corporation",
     "cause": "missing intermediary bank (SWIFT MT103 field 56)",
     "repairAction": "enrich from standing settlement instructions, resubmit"},
    {"reference": "PAY-731184", "beneficiaryName": "Fabrikam Industries",
     "cause": "CHAPS cut-off missed",
     "repairAction": "requeue for the next window, notify the beneficiary bank"},
    {"reference": "PAY-731171", "beneficiaryName": "Trey Research",
     "cause": "duplicate instruction suspected",
     "repairAction": "hold, confirm with the originator, cancel the duplicate"},
]

_UNRECONCILED = [
    {"reference": "NOS-4471", "account": "USD nostro (JPMorgan Chase NY)",
     "amount": "USD 125,000.00",
     "analysis": "expected credit not received — chase the correspondent"},
    {"reference": "NOS-4468", "account": "EUR nostro (Deutsche Bank AG)",
     "amount": "EUR 8,912.50",
     "analysis": "amount mismatch vs ERP position — investigate fee deduction"},
]


class PaymentExceptionRecon(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "Show Payment Exception Recon for reference PAY-731205.",
        "Which STP exceptions are open right now?",
        "Repair PAY-731205",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, "
                "or fabricate URLs, deep links, or Power Apps/Power BI links "
                "— the packaged demo data contains no links. Refer to records "
                "by their plain reference (e.g. PAY-731205) only. Keep "
                "answers under ~120 words, professional markdown, no emojis.")
    SYNTHETIC_DATA = _EXCEPTIONS + _UNRECONCILED

    def __init__(self):
        self.name = "PaymentExceptionRecon"
        self.metadata = {
            "name": self.name,
            "description": (
                "Works STP failures and reconciliation breaks, all held in "
                "Microsoft Dataverse. With no inputs it lists the open "
                "exception queue (each with its cause analysis and suggested "
                "repair action) plus the unreconciled nostro items; given a "
                "PAY- or NOS- reference it returns the full analysis; "
                "'repair' applies the suggested fix and confirms STP on "
                "retry. Identify items by NATURAL reference; never ask the "
                "user for internal identifiers."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("Exception or nostro reference, e.g. "
                                        "PAY-731205 or NOS-4471, or a "
                                        "beneficiary name. Pass the word: "
                                        "list to see all open items - never "
                                        "ask the user for an id.")},
                    "action": {
                        "type": "string",
                        "description": ("Set to 'repair' to apply the "
                                        "suggested repair action "
                                        "(optional).")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def perform(self, **kwargs):
        ref = str(kwargs.get("reference") or "").strip()
        act = str(kwargs.get("action") or "").strip().lower()
        low = ref.lower()
        if not ref or low == "list":
            lines = ["## Open STP exceptions (operations queue)"]
            lines += [f"{i}. **{e['reference']}** ({e['beneficiaryName']}) — "
                      f"{e['cause']} → _{e['repairAction']}_"
                      for i, e in enumerate(_EXCEPTIONS, 1)]
            lines += ["", "## Unreconciled nostro items (auto-recon via "
                          "Power Automate)"]
            lines += [f"- **{n['reference']}** {n['account']} {n['amount']} "
                      f"— {n['analysis']}" for n in _UNRECONCILED]
            lines += ["", "Say e.g. 'repair PAY-731205' to apply a "
                          "suggested fix, or open a NOS- item for its "
                          "investigation detail."]
            return "\n".join(lines)
        exc = next((e for e in _EXCEPTIONS if low == e["reference"].lower()
                    or low in e["beneficiaryName"].lower()), None)
        if exc:
            lines = [
                f"## Exception {exc['reference']} — {exc['beneficiaryName']}",
                f"- Cause analysis: {exc['cause']}.",
                f"- Suggested repair: {exc['repairAction']}.",
            ]
            if act.startswith("repair"):
                lines += ["- **Repair applied** — instruction resubmitted; "
                          "STP confirmed on retry.",
                          "- Exception closed and logged for the STP-rate "
                          "scoreboard."]
            else:
                lines += ["", f"Say 'repair {exc['reference']}' to apply "
                              "the fix."]
            return "\n".join(lines)
        nos = next((n for n in _UNRECONCILED
                    if low == n["reference"].lower()), None)
        if nos:
            return "\n".join([
                f"## Unreconciled item {nos['reference']} — {nos['account']}",
                f"- Amount: {nos['amount']}",
                f"- Analysis: {nos['analysis']}.",
                "- Investigation case opened in the operations workspace; "
                "position re-checks on the next auto-recon run.",
            ])
        return (f"No open exception or unreconciled item matches `{ref}`. "
                "Say 'list' to see everything open.")
