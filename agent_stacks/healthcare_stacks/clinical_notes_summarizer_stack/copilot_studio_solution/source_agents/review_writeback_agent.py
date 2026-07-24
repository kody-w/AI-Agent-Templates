"""Clinician Review & Approval + EHR Write-Back — steps 5-6 of the Clinical
Documentation & Coding Automation process flow.

Step 5 — Clinician Review & Approval: The structured note and suggested
codes are presented to the clinician for rapid review, amendment, and
one-click approval.

Step 6 — EHR Write-Back: The approved clinical note and codes are written
back to the EHR System automatically, maintaining the complete
longitudinal patient record. (EHR System, Power Automate)

Recording a decision requires the clinician's explicit approve/amend
instruction. Data home: Microsoft Dataverse. Synthetic demo data.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
    {"encounterRef": "ENC-8801", "patientName": "Grace Holt",
     "reviewStatus": "APPROVED as suggested",
     "reviewNote": "one-click approval - no amendments",
     "ehrWriteback": "written to EHR - longitudinal record updated"},
    {"encounterRef": "ENC-8802", "patientName": "Omar Haddad",
     "reviewStatus": "APPROVED WITH AMENDMENT",
     "reviewNote": "clinician overrode CPT 99213 -> 99212 (visit "
                   "complexity lower than suggested)",
     "ehrWriteback": "written to EHR - longitudinal record updated"},
    {"encounterRef": "ENC-8803", "patientName": "Lena Novak",
     "reviewStatus": "APPROVED as suggested",
     "reviewNote": "one-click approval - no amendments",
     "ehrWriteback": "written to EHR - longitudinal record updated"},
    {"encounterRef": "ENC-8804", "patientName": "Marcus Reid",
     "reviewStatus": "AWAITING REVIEW",
     "reviewNote": "high-complexity ED note queued for Dr Osei",
     "ehrWriteback": "pending clinician approval"},
]


class ReviewWriteback(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "Show Review Writeback for encounterref ENC-8804.",
        "Which notes are awaiting clinician review?",
        "Approve ENC-8804 as suggested",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, "
                "or fabricate URLs or deep links. Refer to records by their "
                "plain reference (e.g. ENC-8804) only. Synthetic demo data. "
                "Keep answers under ~120 words, professional markdown, no "
                "emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "ReviewWriteback"
        self.metadata = {
            "name": self.name,
            "description": (
                "Tracks clinician review and approval of structured notes "
                "and suggested codes (approve as-is, amend, or override) "
                "and the automatic EHR write-back of approved notes. "
                "Review records live in Microsoft Dataverse. Identify "
                "encounters by NATURAL reference: a patient or ENC- "
                "reference; 'list' shows the review queue; recording an "
                "approval needs the clinician's explicit instruction."),
            "parameters": {
                "type": "object",
                "properties": {
                    "encounterRef": {
                        "type": "string",
                        "description": ("Encounter ENC- reference or "
                                        "patient name, e.g. ENC-8804 or "
                                        "'Marcus Reid'. Pass the word: "
                                        "list to see the review queue - "
                                        "never ask the user for an id.")},
                    "decision": {
                        "type": "string",
                        "description": ("Clinician decision to record: "
                                        "approve or amend, with any "
                                        "amendment detail (optional).")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def perform(self, **kwargs):
        ref = str(kwargs.get("encounterRef") or "").strip()
        decision = str(kwargs.get("decision") or "").strip()
        low = ref.lower()
        if not ref or low == "list":
            lines = ["## Review & write-back queue"]
            lines += [f"{i}. **{n['encounterRef']}** {n['patientName']} — "
                      f"{n['reviewStatus']} — {n['ehrWriteback']}"
                      for i, n in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Open an encounter, or record a decision with "
                         "e.g. 'approve ENC-8804 as suggested'.")
            return "\n".join(lines)
        hits = [n for n in _CANON if low == n["encounterRef"].lower()
                or low in n["patientName"].lower()]
        if not hits:
            return (f"No review record matches `{ref}`. Say 'list' for "
                    "the queue.")
        n = hits[0]
        if decision:
            return "\n".join([
                f"## Decision recorded — {n['encounterRef']} "
                f"({n['patientName']})",
                f"- Clinician decision: **{decision.upper()[:60]}**",
                "- Approved note and codes written back to the EHR "
                "automatically; longitudinal record updated.",
                "- Decision logged to the audit trail.",
            ])
        return "\n".join([
            f"## {n['encounterRef']} — {n['patientName']}",
            f"- Review: {n['reviewStatus']}",
            f"- Note: {n['reviewNote']}",
            f"- EHR: {n['ehrWriteback']}",
            "",
            f"Record a decision with 'approve {n['encounterRef']} as "
            "suggested' (or an amendment).",
        ])
