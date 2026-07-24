"""Charge Capture to Billing System + Audit Trail & Compliance Log — steps
7-8 of the Clinical Documentation & Coding Automation process flow.

Step 7 — Charge Capture to Billing System: Approved CPT codes and encounter
details pass to the Revenue Cycle Management system to generate the claim,
with supporting documentation attached. (Revenue Cycle Management, Power
Automate)

Step 8 — Audit Trail & Compliance Log: Every AI suggestion, clinician
acceptance or override, and system action is logged in an immutable audit
trail for compliance, quality, and training. (Azure Monitor, Power BI)

Claims cohere with the review agent: only APPROVED encounters carry
claims; the audit log records the exact accept/override actions. Data
home: Microsoft Dataverse. Synthetic demo data.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CLAIMS = [
    {"claimRef": "CLM-3301", "encounterRef": "ENC-8801",
     "patientName": "Grace Holt", "claimLines": "99214 + 93000",
     "claimAmount": 312.00, "claimStatus": "submitted to payer",
     "documentation": "SOAP note + ECG report attached"},
    {"claimRef": "CLM-3302", "encounterRef": "ENC-8802",
     "patientName": "Omar Haddad", "claimLines": "99212 + 73600",
     "claimAmount": 198.50, "claimStatus": "submitted to payer "
     "(amended code 99212 per clinician override)",
     "documentation": "SOAP note + x-ray order attached"},
    {"claimRef": "CLM-3303", "encounterRef": "ENC-8803",
     "patientName": "Lena Novak", "claimLines": "99212 + 87880",
     "claimAmount": 121.75, "claimStatus": "submitted to payer",
     "documentation": "SOAP note + rapid strep result attached"},
]

_AUDIT = [
    {"auditRef": "AUD-9101", "encounterRef": "ENC-8801",
     "auditAction": "AI suggested I20.9/I10 + 99214/93000; clinician "
                    "accepted all (one-click)"},
    {"auditRef": "AUD-9102", "encounterRef": "ENC-8802",
     "auditAction": "AI suggested 99213; clinician OVERRODE to 99212 - "
                    "override reason captured for model training"},
    {"auditRef": "AUD-9103", "encounterRef": "ENC-8803",
     "auditAction": "AI suggested J02.9 + 99212/87880; clinician accepted "
                    "all (one-click)"},
    {"auditRef": "AUD-9104", "encounterRef": "ENC-8804",
     "auditAction": "AI suggestions issued; awaiting clinician review - "
                    "no claim generated yet"},
]


class BillingAuditTrail(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "Show Billing Audit Trail for claimref CLM-3301.",
        "Which claims went to the payer today?",
        "Show me the audit trail for ENC-8802",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, "
                "or fabricate URLs or deep links. Refer to records by their "
                "plain reference (e.g. CLM-3301) only. Synthetic demo data. "
                "Keep answers under ~120 words, professional markdown, no "
                "emojis.")
    SYNTHETIC_DATA = _CLAIMS + _AUDIT

    def __init__(self):
        self.name = "BillingAuditTrail"
        self.metadata = {
            "name": self.name,
            "description": (
                "Tracks charge capture into the Revenue Cycle Management "
                "system (claims generated from approved CPT codes with "
                "documentation attached) and the immutable audit trail of "
                "every AI suggestion, clinician acceptance or override, "
                "and system action. Records live in Microsoft Dataverse. "
                "Identify items by NATURAL reference: a CLM-, AUD-, or "
                "ENC- reference or a patient name; 'list' shows claims "
                "and audit entries."),
            "parameters": {
                "type": "object",
                "properties": {
                    "claimRef": {
                        "type": "string",
                        "description": ("Claim CLM-, audit AUD-, encounter "
                                        "ENC- reference, or patient name, "
                                        "e.g. CLM-3301 or 'Grace Holt'. "
                                        "Pass the word: list to see every "
                                        "claim and audit entry - never "
                                        "ask the user for an id.")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def perform(self, **kwargs):
        ref = str(kwargs.get("claimRef") or "").strip()
        low = ref.lower()
        if not ref or low == "list":
            lines = ["## Claims (Revenue Cycle Management)"]
            lines += [f"{i}. **{c['claimRef']}** ({c['encounterRef']}, "
                      f"{c['patientName']}) — {c['claimLines']} — "
                      f"${c['claimAmount']:,.2f} — {c['claimStatus'][:44]}"
                      for i, c in enumerate(_CLAIMS, 1)]
            lines += ["", "## Audit trail (immutable)"]
            lines += [f"- **{a['auditRef']}** ({a['encounterRef']}): "
                      f"{a['auditAction']}" for a in _AUDIT]
            return "\n".join(lines)
        c = next((c for c in _CLAIMS if low in (c["claimRef"].lower(),
                                                c["encounterRef"].lower())
                  or low in c["patientName"].lower()), None)
        a = next((a for a in _AUDIT if low in (a["auditRef"].lower(),
                                               a["encounterRef"].lower())), None)
        if not c and not a:
            return (f"No claim or audit entry matches `{ref}`. Say 'list' "
                    "for everything.")
        lines = []
        if c:
            lines += [f"## Claim {c['claimRef']} — {c['patientName']} "
                      f"({c['encounterRef']})",
                      f"- Lines: {c['claimLines']} | Amount: "
                      f"${c['claimAmount']:,.2f}",
                      f"- Status: {c['claimStatus']}",
                      f"- Documentation: {c['documentation']}"]
        if a:
            lines += ["", f"## Audit {a['auditRef']} ({a['encounterRef']})",
                      f"- {a['auditAction']}"]
        return "\n".join(lines)
