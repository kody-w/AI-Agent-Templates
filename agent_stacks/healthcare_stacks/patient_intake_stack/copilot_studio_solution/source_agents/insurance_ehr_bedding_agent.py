"""Insurance & Eligibility Verification + EHR Record Update & Bed
Allocation — steps 7-8 of the Intelligent Patient Intake & Triage process
flow.

Step 7 — Insurance & Eligibility Verification: An automated eligibility
check runs against the payer system, flagging coverage gaps or
pre-authorisation requirements to admissions staff. (Payer / Insurance
System)

Step 8 — EHR Record Update & Bed Allocation: Completed intake data is
written to the EHR System; the patient is assigned to the appropriate care
area and the receiving clinical team notified. (EHR System, Power Automate)

Data home: Microsoft Dataverse.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
    {"patientRef": "PT-4471", "patientName": "Grace Holt",
     "payerName": "Northwind Health Plus", "eligibilityStatus": "eligible - "
     "cardiac pathway covered",
     "preAuthRequired": "no", "ehrStatus": "intake written to EHR",
     "bedAllocation": "Majors bay 4 -> cardiology obs unit on review"},
    {"patientRef": "PT-4472", "patientName": "Omar Haddad",
     "payerName": "Contoso Care", "eligibilityStatus": "eligible",
     "preAuthRequired": "yes - MRI requires pre-authorisation",
     "ehrStatus": "intake written to EHR",
     "bedAllocation": "Minors - imaging queue (no bed required)"},
    {"patientRef": "PT-4473", "patientName": "Lena Novak",
     "payerName": "self-pay", "eligibilityStatus": "self-pay - estimate "
     "issued to patient",
     "preAuthRequired": "no", "ehrStatus": "intake written to EHR",
     "bedAllocation": "Ambulatory care (no bed required)"},
    {"patientRef": "PT-4474", "patientName": "Marcus Reid",
     "payerName": "Fabrikam Health", "eligibilityStatus": "COVERAGE GAP - "
     "policy lapsed last month; admissions staff flagged",
     "preAuthRequired": "n/a - emergency treatment proceeds regardless",
     "ehrStatus": "intake written to EHR",
     "bedAllocation": "Resus bay 1 -> respiratory HDU bed 3 allocated"},
    {"patientRef": "PT-4475", "patientName": "Ana Sousa",
     "payerName": "Northwind Health Plus", "eligibilityStatus": "eligible",
     "preAuthRequired": "no", "ehrStatus": "awaiting registration "
     "signature before EHR write",
     "bedAllocation": "Majors bay 7 (holding)"},
]


class InsuranceEhrBedding(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "Show Insurance Ehr Bedding for patientref PT-4474.",
        "Are there any coverage gaps or pre-auth flags today?",
        "Which beds have been allocated?",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, "
                "or fabricate URLs or deep links. Refer to records by their "
                "plain reference (e.g. PT-4474) only. Keep answers under "
                "~120 words, professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "InsuranceEhrBedding"
        self.metadata = {
            "name": self.name,
            "description": (
                "Runs the automated payer eligibility check (flagging "
                "coverage gaps and pre-authorisation requirements to "
                "admissions staff) and tracks the EHR intake write-back "
                "and bed/care-area allocation with receiving-team "
                "notification. Records live in Microsoft Dataverse. "
                "Identify patients by NATURAL reference: a name or PT- "
                "reference; 'list' shows every eligibility and bed status."),
            "parameters": {
                "type": "object",
                "properties": {
                    "patientRef": {
                        "type": "string",
                        "description": ("Patient name or PT- reference, "
                                        "e.g. 'Marcus Reid' or PT-4474. "
                                        "Pass the word: list to see every "
                                        "eligibility and bed status - "
                                        "never ask the user for an id.")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def perform(self, **kwargs):
        ref = str(kwargs.get("patientRef") or "").strip()
        low = ref.lower()
        if not ref or low == "list":
            lines = ["## Eligibility, EHR & bed status"]
            for i, p in enumerate(_CANON, 1):
                flag = (" ⚠" if "GAP" in p["eligibilityStatus"]
                        or "yes" in p["preAuthRequired"] else "")
                lines.append(f"{i}. **{p['patientRef']}** "
                             f"{p['patientName']} — "
                             f"{p['eligibilityStatus']}{flag} — "
                             f"{p['bedAllocation']}")
            lines.append("")
            lines.append("Open a patient for the full eligibility and EHR "
                         "detail.")
            return "\n".join(lines)
        hits = [p for p in _CANON if low == p["patientRef"].lower()
                or low in p["patientName"].lower()]
        if not hits:
            return (f"No record matches `{ref}`. Say 'list' for every "
                    "status.")
        p = hits[0]
        return "\n".join([
            f"## {p['patientRef']} — {p['patientName']}",
            f"- Payer: {p['payerName']}",
            f"- Eligibility: {p['eligibilityStatus']}",
            f"- Pre-authorisation: {p['preAuthRequired']}",
            f"- EHR: {p['ehrStatus']}",
            f"- Bed / care area: {p['bedAllocation']}",
        ])
