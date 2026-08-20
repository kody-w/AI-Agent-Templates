"""Clinician Alert & Queue Assignment + Registration Form Pre-Population —
steps 5-6 of the Intelligent Patient Intake & Triage process flow.

Step 5 — Clinician Alert & Queue Assignment: The duty clinician is notified
of high-priority patients in real time and the patient is placed in the
appropriate care queue. (Power Automate)

Step 6 — Registration Form Pre-Population: The registration form is
pre-populated from the collected data and presented to the patient for
review and digital signature on a tablet or mobile device.

Queue placement follows the triage category from the assessment agent (RED
-> resus, ORANGE -> majors, YELLOW -> minors/majors, GREEN -> ambulatory).
Data home: Microsoft Dataverse.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
    {"patientRef": "PT-4474", "patientName": "Marcus Reid",
     "careQueue": "Resus bay 1", "clinicianAlerted": "Dr Amara Osei "
     "(duty consultant) - real-time alert sent",
     "registrationStatus": "pre-populated - signature deferred (clinical "
                           "priority)"},
    {"patientRef": "PT-4471", "patientName": "Grace Holt",
     "careQueue": "Majors bay 4", "clinicianAlerted": "Dr Amara Osei "
     "(duty consultant) - real-time alert sent",
     "registrationStatus": "pre-populated - signed on tablet"},
    {"patientRef": "PT-4472", "patientName": "Omar Haddad",
     "careQueue": "Minors - imaging queue", "clinicianAlerted": "queue "
     "notification only (YELLOW)",
     "registrationStatus": "pre-populated - signed on tablet"},
    {"patientRef": "PT-4475", "patientName": "Ana Sousa",
     "careQueue": "Majors bay 7", "clinicianAlerted": "queue notification "
     "only (YELLOW)",
     "registrationStatus": "pre-populated - awaiting signature"},
    {"patientRef": "PT-4473", "patientName": "Lena Novak",
     "careQueue": "Ambulatory care", "clinicianAlerted": "none required "
     "(GREEN)",
     "registrationStatus": "pre-populated - signed on mobile"},
]


class ClinicianQueueRegistration(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "Show Clinician Queue Registration for patientref PT-4474.",
        "Which care queue is each patient in?",
        "Has Grace Holt signed her registration form?",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, "
                "or fabricate URLs or deep links. Refer to records by their "
                "plain reference (e.g. PT-4474) only. Keep answers under "
                "~120 words, professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "ClinicianQueueRegistration"
        self.metadata = {
            "name": self.name,
            "description": (
                "Tracks the clinician alerting and care-queue placement "
                "driven by each patient's triage category (RED to resus, "
                "ORANGE to majors, YELLOW to minors/majors, GREEN to "
                "ambulatory) and the pre-populated registration form's "
                "signature status. Queue and registration records live in "
                "Microsoft Dataverse. Identify patients by NATURAL "
                "reference: a name or PT- reference; 'list' shows every "
                "queue placement."),
            "parameters": {
                "type": "object",
                "properties": {
                    "patientRef": {
                        "type": "string",
                        "description": ("Patient name or PT- reference, "
                                        "e.g. 'Grace Holt' or PT-4471. "
                                        "Pass the word: list to see every "
                                        "care-queue placement - never ask "
                                        "the user for an id.")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def perform(self, **kwargs):
        ref = str(kwargs.get("patientRef") or "").strip()
        low = ref.lower()
        if not ref or low == "list":
            lines = ["## Care-queue placements"]
            lines += [f"{i}. **{p['patientRef']}** {p['patientName']} — "
                      f"{p['careQueue']} — {p['registrationStatus']}"
                      for i, p in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Open a patient for the alert and registration "
                         "detail.")
            return "\n".join(lines)
        hits = [p for p in _CANON if low == p["patientRef"].lower()
                or low in p["patientName"].lower()]
        if not hits:
            return (f"No queue placement matches `{ref}`. Say 'list' for "
                    "all placements.")
        p = hits[0]
        return "\n".join([
            f"## {p['patientRef']} — {p['patientName']}",
            f"- Care queue: **{p['careQueue']}**",
            f"- Clinician alert: {p['clinicianAlerted']}",
            f"- Registration: {p['registrationStatus']}",
            "",
            f"Next: verify insurance and eligibility for "
            f"{p['patientRef']}.",
        ])
