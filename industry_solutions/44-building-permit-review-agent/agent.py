"""Building Permit Review Agent — State and Local Government industry solution (AIBAST).

Automate building permit review processes to enable faster service, lower operational costs, and higher citizen satisfaction.

Personas: Permit Technicians; Plan Reviewers; Inspectors.
Featured tools: Dynamics 365 CRM, Dynamics 365 CcaaS, Microsoft Teams, SharePoint.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a permit by NATURAL reference: a name or a
PRM- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "PRM-10880",
                "subject": "Coho Vineyard",
                "status": "submitted",
                "owner": "Permit Technicians",
                "metric": 34.5,
                "note": "Permit for Coho Vineyard"
        },
        {
                "reference": "PRM-10881",
                "subject": "Margie's Travel",
                "status": "in review",
                "owner": "Plan Reviewers",
                "metric": 38.2,
                "note": "Permit for Margie's Travel"
        },
        {
                "reference": "PRM-10882",
                "subject": "Fourth Coffee",
                "status": "approved",
                "owner": "Inspectors",
                "metric": 41.9,
                "note": "Permit for Fourth Coffee"
        },
        {
                "reference": "PRM-10883",
                "subject": "Graphic Design Institute",
                "status": "needs revision",
                "owner": "Permit Technicians",
                "metric": 45.6,
                "note": "Permit for Graphic Design Institute"
        },
        {
                "reference": "PRM-10884",
                "subject": "Contoso",
                "status": "issued",
                "owner": "Plan Reviewers",
                "metric": 49.3,
                "note": "Permit for Contoso"
        }
]


class BuildingPermitReviewAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's permit records.",
        "Show PRM-10880.",
        "What is the status of Margie's Travel?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "BuildingPermitReviewAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate building permit review processes to enable faster service, lower operational costs, and higher citizen satisfaction. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a permit by a name or a PRM- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A permit reference or a subject "
                                        "name, e.g. PRM-10880 or 'Coho Vineyard'. Pass 'list' to "
                                        "see every permit.")},
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
            lines = ["## Building Permit Review Agent — permit records (Dataverse)"]
            lines += ["%d. **%s** — %s | status: %s | owner: %s"
                      % (n, r["reference"], r["subject"], r["status"], r["owner"])
                      for n, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a permit for its detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return "No permit matches `%s`. Say 'list' to see all." % ref
        r = hits[0]
        return "\n".join([
            "## %s — %s" % (r["reference"], r["subject"]),
            "- Status: **%s**" % r["status"],
            "- Owner: %s" % r["owner"],
            "- Key metric: %s" % r["metric"],
            "- %s" % r["note"],
        ])
