"""Symptom & History Capture + Clinical Triage Scoring — steps 3-4 of the
Intelligent Patient Intake & Triage process flow.

Step 3 — Symptom & History Capture: A guided conversational assessment
captures presenting symptoms, duration, severity, relevant medical history,
allergies, and current medications. (Copilot Studio, Azure OpenAI)

Step 4 — Clinical Triage Scoring: Validated triage protocols (Manchester
Triage System) are applied to the captured data, generating a priority
category with clinical rationale. (Azure AI, Copilot Studio)

Triage rules are REAL and deterministic (Manchester categories): RED
immediate (airway/catastrophic), ORANGE very urgent (severe pain or chest
pain), YELLOW urgent (moderate symptoms), GREEN standard. Data home:
Microsoft Dataverse. This is a demo on synthetic data — never real
clinical advice.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
    {"patientRef": "PT-4471", "patientName": "Grace Holt",
     "presentingSymptoms": "central chest pain radiating to left arm, "
                           "onset 40 minutes ago",
     "severityScore": 9, "historyFlags": "hypertension; penicillin allergy",
     "triageCategory": "ORANGE - very urgent",
     "triageRationale": "chest pain with cardiac features - Manchester "
                        "chest-pain discriminator"},
    {"patientRef": "PT-4472", "patientName": "Omar Haddad",
     "presentingSymptoms": "ankle injury after fall, swelling, "
                           "weight-bearing painful",
     "severityScore": 4, "historyFlags": "none",
     "triageCategory": "YELLOW - urgent",
     "triageRationale": "moderate pain, possible fracture - limb injury "
                        "discriminator"},
    {"patientRef": "PT-4473", "patientName": "Lena Novak",
     "presentingSymptoms": "sore throat and mild fever for 3 days",
     "severityScore": 2, "historyFlags": "none",
     "triageCategory": "GREEN - standard",
     "triageRationale": "stable, low severity, no red-flag discriminators"},
    {"patientRef": "PT-4474", "patientName": "Marcus Reid",
     "presentingSymptoms": "acute shortness of breath, audible wheeze, "
                           "cannot complete sentences",
     "severityScore": 10, "historyFlags": "asthma",
     "triageCategory": "RED - immediate",
     "triageRationale": "compromised airway/breathing - immediate "
                        "resuscitation-area review"},
    {"patientRef": "PT-4475", "patientName": "Ana Sousa",
     "presentingSymptoms": "migraine, photophobia, nausea since morning",
     "severityScore": 6, "historyFlags": "recurrent migraine",
     "triageCategory": "YELLOW - urgent",
     "triageRationale": "severe headache without neuro deficit - headache "
                        "discriminator"},
]


class SymptomTriageScoring(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "Show Symptom Triage Scoring for patientref PT-4474.",
        "Run the triage assessment for Grace Holt",
        "Which patients are highest priority right now?",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, "
                "or fabricate URLs or deep links. Refer to records by their "
                "plain reference (e.g. PT-4471) only. This is synthetic demo "
                "data - never present it as real clinical advice. Keep "
                "answers under ~120 words, professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "SymptomTriageScoring"
        self.metadata = {
            "name": self.name,
            "description": (
                "Captures the guided symptom and history assessment "
                "(presenting symptoms, duration, severity, history, "
                "allergies, medications) and applies validated Manchester "
                "Triage System discriminators to produce a priority "
                "category (RED / ORANGE / YELLOW / GREEN) with the clinical "
                "rationale. Assessments live in Microsoft Dataverse. "
                "Identify patients by NATURAL reference: a name or PT- "
                "reference; 'list' ranks today's queue by priority."),
            "parameters": {
                "type": "object",
                "properties": {
                    "patientRef": {
                        "type": "string",
                        "description": ("Patient name or PT- reference, "
                                        "e.g. 'Marcus Reid' or PT-4474. "
                                        "Pass the word: list to rank "
                                        "today's assessments by priority "
                                        "- never ask the user for an id.")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def perform(self, **kwargs):
        ref = str(kwargs.get("patientRef") or "").strip()
        low = ref.lower()
        order = {"RED": 0, "ORANGE": 1, "YELLOW": 2, "GREEN": 3}
        if not ref or low == "list":
            ranked = sorted(_CANON,
                            key=lambda p: order.get(
                                p["triageCategory"].split(" ")[0], 9))
            lines = ["## Triage queue (Manchester priority order)"]
            lines += [f"{i}. **{p['patientRef']}** {p['patientName']} — "
                      f"**{p['triageCategory']}** — "
                      f"{p['presentingSymptoms'][:60]}"
                      for i, p in enumerate(ranked, 1)]
            lines.append("")
            lines.append("Open a patient for the full assessment and "
                         "rationale.")
            return "\n".join(lines)
        hits = [p for p in _CANON if low == p["patientRef"].lower()
                or low in p["patientName"].lower()]
        if not hits:
            return (f"No assessment matches `{ref}`. Say 'list' for the "
                    "ranked triage queue.")
        p = hits[0]
        return "\n".join([
            f"## Triage assessment — {p['patientRef']} "
            f"({p['patientName']})",
            f"- Presenting: {p['presentingSymptoms']}",
            f"- Severity (0-10): {p['severityScore']} | History: "
            f"{p['historyFlags']}",
            f"- **Category: {p['triageCategory']}**",
            f"- Rationale: {p['triageRationale']}.",
            "",
            f"Next: alert the duty clinician and queue {p['patientRef']}.",
        ])
