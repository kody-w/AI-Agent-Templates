"""Patient Contact & Identity Verification — steps 1-2 of the Intelligent
Patient Intake & Triage process flow.

Step 1 — Patient Contact & Channel Identification: Patient contacts via web
portal, mobile app, phone, or walk-in. The intake conversation is initiated
and the channel identified. (Copilot Studio)

Step 2 — Identity Verification & Record Matching: The patient's identity is
verified against the Patient Administration System and their existing
medical record retrieved if available. (Copilot Studio, Patient
Administration System)

Identify patients by NATURAL reference (name or PT- reference); 'list'
shows today's intake queue. Data home: Microsoft Dataverse.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

# Canonical intake book — the SAME patients flow through the sibling agents
# (symptom & triage, clinician queue & registration, insurance & EHR).
_CANON = [
    {"patientRef": "PT-4471", "patientName": "Grace Holt",
     "channel": "walk-in", "mrn": "MRN-002214",
     "identityStatus": "verified — record matched",
     "dateOfBirth": "1953-02-11"},
    {"patientRef": "PT-4472", "patientName": "Omar Haddad",
     "channel": "phone", "mrn": "MRN-009182",
     "identityStatus": "verified — record matched",
     "dateOfBirth": "1988-07-30"},
    {"patientRef": "PT-4473", "patientName": "Lena Novak",
     "channel": "web portal", "mrn": "MRN-011507",
     "identityStatus": "verified — record matched",
     "dateOfBirth": "1996-12-03"},
    {"patientRef": "PT-4474", "patientName": "Marcus Reid",
     "channel": "mobile app", "mrn": "none",
     "identityStatus": "NEW PATIENT — no existing record",
     "dateOfBirth": "2001-05-19"},
    {"patientRef": "PT-4475", "patientName": "Ana Sousa",
     "channel": "walk-in", "mrn": "MRN-007733",
     "identityStatus": "verification pending — DOB mismatch, re-check ID",
     "dateOfBirth": "1972-09-24"},
]


class PatientContactIdentity(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "Show Patient Contact Identity for patientref PT-4471.",
        "Who has arrived for intake today?",
        "Register a new patient contact: Jordan Blake via web portal",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, "
                "or fabricate URLs, deep links, or Power Apps/Power BI links "
                "— the packaged demo data contains no links. Refer to "
                "records by their plain reference (e.g. PT-4471) only. Keep "
                "answers under ~120 words, professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "PatientContactIdentity"
        self.metadata = {
            "name": self.name,
            "description": (
                "Handles first contact on any channel (web portal, mobile "
                "app, phone, walk-in), initiates the structured intake "
                "conversation, and verifies the patient's identity against "
                "the Patient Administration System — matching their "
                "existing medical record or flagging a new patient. Intake "
                "records live in Microsoft Dataverse. Identify patients by "
                "NATURAL reference: a name like 'Grace Holt' or a PT- "
                "reference; never ask for internal identifiers."),
            "parameters": {
                "type": "object",
                "properties": {
                    "patientRef": {
                        "type": "string",
                        "description": ("Patient name or PT- reference, "
                                        "e.g. 'Grace Holt' or PT-4471. "
                                        "Pass the word: list to see "
                                        "today's intake queue - never ask "
                                        "the user for an id.")},
                    "patientName": {
                        "type": "string",
                        "description": ("Name for a NEW patient contact "
                                        "(optional).")},
                    "channel": {
                        "type": "string",
                        "description": ("Channel for a NEW contact: web "
                                        "portal, mobile app, phone, or "
                                        "walk-in (optional).")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def perform(self, **kwargs):
        ref = str(kwargs.get("patientRef")
                  or kwargs.get("patientName") or "").strip()
        low = ref.lower()
        if not ref or low == "list":
            lines = ["## Today's intake contacts"]
            lines += [f"{i}. **{p['patientRef']}** — {p['patientName']} via "
                      f"{p['channel']} — {p['identityStatus']}"
                      for i, p in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a patient for their identity detail, or give "
                         "me a name and channel to register a new contact.")
            return "\n".join(lines)
        hits = [p for p in _CANON if low == p["patientRef"].lower()
                or low in p["patientName"].lower()]
        if not hits and kwargs.get("channel"):
            next_ref = "PT-%d" % (max(int(p["patientRef"][3:])
                                      for p in _CANON) + 1)
            return "\n".join([
                f"## New patient contact — {next_ref}",
                f"- Name: {ref or kwargs.get('patientName')} | Channel: "
                f"{kwargs.get('channel')}",
                "- Structured intake conversation initiated.",
                "- Identity check against the Patient Administration "
                "System: NO existing record — registered as a new patient.",
                "",
                f"Next: capture symptoms and history for {next_ref}.",
            ])
        if not hits:
            return (f"No intake contact matches `{ref}`. Say 'list' for "
                    "today's queue.")
        p = hits[0]
        return "\n".join([
            f"## {p['patientRef']} — {p['patientName']}",
            f"- Channel: {p['channel']} | DOB: {p['dateOfBirth']}",
            f"- Identity: {p['identityStatus']}",
            f"- Medical record: {p['mrn']}",
            "",
            f"Next: capture symptoms and history for {p['patientRef']}.",
        ])
