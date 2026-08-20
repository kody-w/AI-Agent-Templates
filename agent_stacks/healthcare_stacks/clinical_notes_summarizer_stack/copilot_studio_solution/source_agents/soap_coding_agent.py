"""Clinical Note Structuring & ICD/CPT Code Suggestion — steps 3-4 of the
Clinical Documentation & Coding Automation process flow.

Step 3 — Clinical Note Structuring: The transcript is structured into SOAP
format (Subjective, Objective, Assessment, Plan) and key clinical entities
extracted: diagnoses, medications, procedures. (Azure OpenAI)

Step 4 — ICD & CPT Code Suggestion: Extracted clinical entities are matched
against ICD-10 and CPT code libraries, suggesting the most accurate codes
with confidence scores. (Copilot Studio, Azure AI, Clinical Coding
Libraries)

Identify notes by NATURAL reference (patient, clinician, or ENC-
reference). Data home: Microsoft Dataverse. Synthetic demo data — never
real clinical coding advice.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
    {"encounterRef": "ENC-8801", "patientName": "Grace Holt",
     "soapAssessment": "stable angina, hypertension review",
     "extractedEntities": "chest pain; GTN spray; ECG performed",
     "icdSuggestions": "I20.9 (angina pectoris, unspecified) conf 0.94; "
                       "I10 (essential hypertension) conf 0.91",
     "cptSuggestions": "99214 (established patient, moderate) conf 0.92; "
                       "93000 (ECG with interpretation) conf 0.95"},
    {"encounterRef": "ENC-8802", "patientName": "Omar Haddad",
     "soapAssessment": "lateral ankle sprain, rule out fracture",
     "extractedEntities": "ankle inversion injury; x-ray ordered; "
                          "RICE advice",
     "icdSuggestions": "S93.401 (sprain of unspecified ligament, right "
                       "ankle) conf 0.89",
     "cptSuggestions": "99213 (established patient, low-moderate) conf "
                       "0.93; 73600 (ankle x-ray, 2 views) conf 0.96"},
    {"encounterRef": "ENC-8803", "patientName": "Lena Novak",
     "soapAssessment": "acute pharyngitis, viral",
     "extractedEntities": "sore throat; fever 37.9; rapid strep negative",
     "icdSuggestions": "J02.9 (acute pharyngitis, unspecified) conf 0.95",
     "cptSuggestions": "99212 (established patient, straightforward) conf "
                       "0.94; 87880 (rapid strep test) conf 0.97"},
    {"encounterRef": "ENC-8804", "patientName": "Marcus Reid",
     "soapAssessment": "acute asthma exacerbation, moderate",
     "extractedEntities": "wheeze; salbutamol nebuliser; peak flow 55% "
                          "predicted; prednisolone course",
     "icdSuggestions": "J45.901 (unspecified asthma with acute "
                       "exacerbation) conf 0.96",
     "cptSuggestions": "99284 (ED visit, high complexity) conf 0.90; "
                       "94640 (nebuliser treatment) conf 0.95"},
]


class SoapCodingSuggestion(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "Show Soap Coding Suggestion for encounterref ENC-8804.",
        "What codes were suggested for Grace Holt's encounter?",
        "Which notes are structured and ready for review?",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, "
                "or fabricate URLs or deep links. Refer to records by their "
                "plain reference (e.g. ENC-8801) only. Synthetic demo data - "
                "never real clinical coding advice. Keep answers under ~120 "
                "words, professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "SoapCodingSuggestion"
        self.metadata = {
            "name": self.name,
            "description": (
                "Holds each encounter's SOAP-structured note (subjective, "
                "objective, assessment, plan) with extracted clinical "
                "entities, and the suggested ICD-10 and CPT codes with "
                "confidence scores matched from the coding libraries. "
                "Notes live in Microsoft Dataverse. Identify notes by "
                "NATURAL reference: a patient, clinician, or ENC- "
                "reference; 'list' shows every structured note."),
            "parameters": {
                "type": "object",
                "properties": {
                    "encounterRef": {
                        "type": "string",
                        "description": ("Encounter ENC- reference or "
                                        "patient name, e.g. ENC-8804 or "
                                        "'Marcus Reid'. Pass the word: "
                                        "list to see every structured "
                                        "note - never ask the user for "
                                        "an id.")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def perform(self, **kwargs):
        ref = str(kwargs.get("encounterRef") or "").strip()
        low = ref.lower()
        if not ref or low == "list":
            lines = ["## Structured notes with code suggestions"]
            lines += [f"{i}. **{n['encounterRef']}** {n['patientName']} — "
                      f"{n['soapAssessment']} — ICD: "
                      f"{n['icdSuggestions'].split(' ')[0]}"
                      for i, n in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Open a note for the full SOAP structure and code "
                         "suggestions. ENC-8805 has no note yet (recording "
                         "failed - re-dictation pending).")
            return "\n".join(lines)
        hits = [n for n in _CANON if low == n["encounterRef"].lower()
                or low in n["patientName"].lower()]
        if not hits:
            return (f"No structured note matches `{ref}`. Say 'list' for "
                    "every note (ENC-8805 is pending re-dictation).")
        n = hits[0]
        return "\n".join([
            f"## {n['encounterRef']} — {n['patientName']}",
            f"- SOAP assessment: {n['soapAssessment']}",
            f"- Extracted entities: {n['extractedEntities']}",
            f"- ICD-10 suggestions: {n['icdSuggestions']}",
            f"- CPT suggestions: {n['cptSuggestions']}",
            "",
            f"Next: clinician review and approval for "
            f"{n['encounterRef']}.",
        ])
