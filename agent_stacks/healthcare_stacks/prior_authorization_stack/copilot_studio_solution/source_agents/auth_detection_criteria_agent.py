"""Auth Requirement Detection & Clinical Criteria Assembly — steps 1-2 of the
Prior Authorization & Utilization Management process flow.

Step 1 — Auth Requirement Detection: when an order is placed, Copilot Studio
checks the payer rules engine to determine whether the CPT/HCPCS code and plan
require prior authorization, honouring gold-carding exemptions for
high-approval providers. (Copilot Studio, Payer Rules Engine)

Step 2 — Clinical Criteria Assembly: Azure OpenAI extracts the supporting
clinical evidence from the EHR — diagnoses, prior conservative treatment,
imaging — and maps it against the payer's medical-necessity criteria
(MCG / InterQual) for the requested service. (Azure OpenAI, EHR System)

Rules are REAL and deterministic: a gold-carded CPT/plan skips review; other
orders require prior auth and get a criteria packet assembled. Identify
requests by NATURAL reference (patient name, CPT code, or AUTH- ref). Data
home: Microsoft Dataverse.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

# The canonical prior-auth book — the SAME requests flow through the sibling
# agents (submission & tracking, denial & peer-to-peer, write-back & analytics)
# so every hop tells one coherent utilization-management story.
_CANON = [
    {"authReference": "AUTH-88401", "patientName": "Jordan Avery",
     "service": "MRI lumbar spine", "cpt": "72148", "payer": "Contoso Health",
     "urgency": "standard", "goldCarded": True,
     "requirement": "EXEMPT — provider gold-carded for 72148 on this plan",
     "criteria": "n/a (auto-approved at order)", "determination": "approved"},
    {"authReference": "AUTH-88394", "patientName": "Priya Nair",
     "service": "Total knee arthroplasty", "cpt": "27447",
     "payer": "Northwind Health", "urgency": "standard", "goldCarded": False,
     "requirement": "REQUIRED — 27447 needs prior auth on this plan",
     "criteria": "MCG: >=3 months failed conservative therapy + imaging-confirmed "
                 "OA — MET",
     "determination": "approved"},
    {"authReference": "AUTH-88377", "patientName": "Marcus Bell",
     "service": "Proton beam therapy", "cpt": "77523",
     "payer": "Fabrikam Insurance", "urgency": "standard", "goldCarded": False,
     "requirement": "REQUIRED — 77523 needs prior auth on this plan",
     "criteria": "InterQual: equivalent-outcome conformal RT available — NOT MET",
     "determination": "denied"},
    {"authReference": "AUTH-88365", "patientName": "Elena Fischer",
     "service": "CT abdomen & pelvis w/ contrast", "cpt": "74178",
     "payer": "Adatum Health", "urgency": "expedited",
     "goldCarded": False,
     "requirement": "REQUIRED — expedited (72h SLA) review",
     "criteria": "MCG: acute abdomen with red-flag symptoms — MET",
     "determination": "approved"},
    {"authReference": "AUTH-88350", "patientName": "Sam Okafor",
     "service": "Lumbar spinal fusion", "cpt": "22633",
     "payer": "Woodgrove Health", "urgency": "standard", "goldCarded": False,
     "requirement": "REQUIRED — 22633 needs prior auth on this plan",
     "criteria": "MCG: instability documented; conservative-care duration "
                 "borderline — PEER-TO-PEER required",
     "determination": "pended"},
]


class AuthDetectionCriteria(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "Does AUTH-88401 need prior authorization?",
        "Assemble the medical-necessity criteria for Priya Nair's knee replacement.",
        "Check whether CPT 77523 requires prior auth for Marcus Bell.",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference (e.g. AUTH-88401) only. Keep answers under ~120 "
                "words, professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "AuthDetectionCriteria"
        self.metadata = {
            "name": self.name,
            "description": (
                "Detects whether a placed order requires prior authorization by "
                "checking the CPT/HCPCS code and plan against the payer rules "
                "engine (honouring gold-carding exemptions), then assembles the "
                "clinical-evidence packet from the EHR and maps it against the "
                "payer's MCG/InterQual medical-necessity criteria. Requests live "
                "in Microsoft Dataverse. Identify a request by NATURAL reference: "
                "a patient name, CPT code, or AUTH- reference; never ask the user "
                "for an internal id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "authReference": {
                        "type": "string",
                        "description": ("Auth reference, patient name, or CPT "
                                        "code, e.g. AUTH-88401, 'Priya Nair', "
                                        "or 72148. Pass the word: list to see "
                                        "today's orders — never ask the user "
                                        "for an id.")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def _find(self, ref):
        low = ref.lower()
        return [a for a in _CANON if low == a["authReference"].lower()
                or low in a["patientName"].lower() or low == a["cpt"]]

    def perform(self, **kwargs):
        ref = str(kwargs.get("authReference") or "").strip()
        if not ref or ref.lower() == "list":
            lines = ["## Orders under prior-auth review — today (Dataverse)"]
            lines += [f"{i}. **{a['authReference']}** — {a['patientName']}, "
                      f"{a['service']} (CPT {a['cpt']}), {a['payer']} — "
                      f"{'gold-carded' if a['goldCarded'] else a['urgency']}"
                      for i, a in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a request for its auth-requirement and "
                         "medical-necessity detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return (f"No order matches `{ref}`. Say 'list' for today's orders "
                    "under review.")
        a = hits[0]
        lines = [
            f"## {a['authReference']} — {a['patientName']}",
            f"- Service: {a['service']} (CPT {a['cpt']}) | Payer: {a['payer']} "
            f"| Urgency: {a['urgency']}",
            "",
            "### Step 1 — Auth requirement (payer rules engine)",
            f"- {a['requirement']}.",
        ]
        if a["goldCarded"]:
            lines.append("- No review needed; order proceeds to scheduling.")
            return "\n".join(lines)
        lines += [
            "",
            "### Step 2 — Clinical criteria assembly (EHR → MCG/InterQual)",
            f"- {a['criteria']}.",
            f"- Assembled evidence packet ready for payer submission "
            f"({a['authReference']}).",
        ]
        return "\n".join(lines)
