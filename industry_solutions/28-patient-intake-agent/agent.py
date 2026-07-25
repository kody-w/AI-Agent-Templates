"""Patient Intake Agent — Healthcare industry solution (AIBAST).

Automate patient intake workflows to streamline operations, protect revenue from avoidable losses, and deliver a smoother patient experience.

Personas: Front Desk Staff; Scheduling Coordinators; Patient Access Reps.
Featured tools: Dynamics 365 ERP, Dynamics 365 CcaaS, SharePoint.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a record by NATURAL reference: a name or a
PT- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "PT-10560",
                "subject": "Coho Vineyard",
                "status": "registered",
                "owner": "Front Desk Staff",
                "metric": 90.5,
                "note": "Record for Coho Vineyard"
        },
        {
                "reference": "PT-10561",
                "subject": "Margie's Travel",
                "status": "triaged",
                "owner": "Scheduling Coordinators",
                "metric": 94.2,
                "note": "Record for Margie's Travel"
        },
        {
                "reference": "PT-10562",
                "subject": "Fourth Coffee",
                "status": "in care",
                "owner": "Patient Access Reps",
                "metric": 97.9,
                "note": "Record for Fourth Coffee"
        },
        {
                "reference": "PT-10563",
                "subject": "Graphic Design Institute",
                "status": "discharged",
                "owner": "Front Desk Staff",
                "metric": 13.6,
                "note": "Record for Graphic Design Institute"
        },
        {
                "reference": "PT-10564",
                "subject": "Contoso",
                "status": "pending auth",
                "owner": "Scheduling Coordinators",
                "metric": 17.3,
                "note": "Record for Contoso"
        }
]


class PatientIntakeAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's record records.",
        "Show PT-10560.",
        "What is the status of Margie's Travel?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "PatientIntakeAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate patient intake workflows to streamline operations, protect revenue from avoidable losses, and deliver a smoother patient experience. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a record by a name or a PT- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A record reference or a subject "
                                        "name, e.g. PT-10560 or 'Coho Vineyard'. Pass 'list' to "
                                        "see every record.")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def _find(self, ref):
        low = ref.lower()
        return [r for r in _CANON if low == r["reference"].lower()
                or low in r["subject"].lower()]

    def perform(self, **kwargs):
        ref = str(kwargs.get("reference") or "").strip()
        if not ref or ref.lower() == "list":
            lines = ["## Patient Intake Agent — record records (Dataverse)"]
            lines += ["%d. **%s** — %s | status: %s | owner: %s"
                      % (n, r["reference"], r["subject"], r["status"], r["owner"])
                      for n, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a record for its detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return "No record matches `%s`. Say 'list' to see all." % ref
        r = hits[0]
        return "\n".join([
            "## %s — %s" % (r["reference"], r["subject"]),
            "- Status: **%s**" % r["status"],
            "- Owner: %s" % r["owner"],
            "- Key metric: %s" % r["metric"],
            "- %s" % r["note"],
        ])
