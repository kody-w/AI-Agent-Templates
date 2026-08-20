"""Encounter Recording & Speech-to-Text Transcription — steps 1-2 of the
Clinical Documentation & Coding Automation process flow.

Step 1 — Encounter Recording: The clinician records the patient encounter
via voice dictation into the clinical workspace or uses ambient AI
listening during the consultation. (Azure AI Speech)

Step 2 — Speech-to-Text Transcription: The audio recording is converted
into a structured transcript in real time, identifying speaker roles
(clinician vs patient). (Azure AI Speech)

Identify encounters by NATURAL reference (clinician, patient, or ENC-
reference); 'list' shows today's recordings. Data home: Microsoft
Dataverse. Synthetic demo data — never real clinical records.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

# Canonical encounter book — the SAME encounters flow through the sibling
# agents (SOAP & coding, review & write-back, billing & audit).
_CANON = [
    {"encounterRef": "ENC-8801", "patientName": "Grace Holt",
     "clinicianName": "Dr Amara Osei", "captureMode": "ambient AI listening",
     "durationMinutes": 14,
     "transcriptStatus": "transcribed - speakers identified "
                         "(clinician/patient), 98.4% confidence"},
    {"encounterRef": "ENC-8802", "patientName": "Omar Haddad",
     "clinicianName": "Dr Priya Nair", "captureMode": "voice dictation",
     "durationMinutes": 6,
     "transcriptStatus": "transcribed - single speaker, 99.1% confidence"},
    {"encounterRef": "ENC-8803", "patientName": "Lena Novak",
     "clinicianName": "Dr Priya Nair", "captureMode": "ambient AI listening",
     "durationMinutes": 9,
     "transcriptStatus": "transcribed - speakers identified, 97.8% "
                         "confidence"},
    {"encounterRef": "ENC-8804", "patientName": "Marcus Reid",
     "clinicianName": "Dr Amara Osei", "captureMode": "ambient AI listening",
     "durationMinutes": 22,
     "transcriptStatus": "transcribed - 3 speakers (registrar present), "
                         "96.9% confidence"},
    {"encounterRef": "ENC-8805", "patientName": "Ana Sousa",
     "clinicianName": "Dr Tomas Weber", "captureMode": "voice dictation",
     "durationMinutes": 5,
     "transcriptStatus": "RECORDING FAILED at 0:42 - clinician re-dictation "
                         "requested"},
]


class EncounterTranscription(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "Show Encounter Transcription for encounterref ENC-8801.",
        "Which encounters were recorded today?",
        "Did any transcriptions fail?",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, "
                "or fabricate URLs or deep links. Refer to records by their "
                "plain reference (e.g. ENC-8801) only. Synthetic demo data - "
                "never real clinical records. Keep answers under ~120 "
                "words, professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "EncounterTranscription"
        self.metadata = {
            "name": self.name,
            "description": (
                "Tracks encounter recordings (voice dictation or ambient AI "
                "listening) and their real-time speech-to-text transcripts "
                "with speaker-role identification and confidence. Encounter "
                "records live in Microsoft Dataverse. Identify encounters "
                "by NATURAL reference: a clinician, a patient, or an ENC- "
                "reference; never ask for internal identifiers."),
            "parameters": {
                "type": "object",
                "properties": {
                    "encounterRef": {
                        "type": "string",
                        "description": ("Encounter ENC- reference, patient, "
                                        "or clinician name, e.g. ENC-8801 "
                                        "or 'Dr Amara Osei'. Pass the "
                                        "word: list to see today's "
                                        "recordings - never ask the user "
                                        "for an id.")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def perform(self, **kwargs):
        ref = str(kwargs.get("encounterRef") or "").strip()
        low = ref.lower()
        if not ref or low == "list":
            lines = ["## Today's encounter recordings"]
            lines += [f"{i}. **{e['encounterRef']}** — "
                      f"{e['patientName']} with {e['clinicianName']} "
                      f"({e['captureMode']}, {e['durationMinutes']} min) — "
                      f"{e['transcriptStatus'][:52]}"
                      for i, e in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Open an encounter for its transcript detail.")
            return "\n".join(lines)
        hits = [e for e in _CANON if low == e["encounterRef"].lower()
                or low in e["patientName"].lower()
                or low in e["clinicianName"].lower()]
        if not hits:
            return (f"No recording matches `{ref}`. Say 'list' for today's "
                    "encounters.")
        e = hits[0]
        return "\n".join([
            f"## {e['encounterRef']} — {e['patientName']} with "
            f"{e['clinicianName']}",
            f"- Capture: {e['captureMode']} | Duration: "
            f"{e['durationMinutes']} min",
            f"- Transcript: {e['transcriptStatus']}",
            "",
            f"Next: structure the note and suggest codes for "
            f"{e['encounterRef']}.",
        ])
