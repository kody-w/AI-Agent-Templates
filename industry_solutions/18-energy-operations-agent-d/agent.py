"""Energy Operations Agent (d) — Energy and Utilities industry solution (AIBAST).

Deliver real-time insights, automate critical workflows, and enable guided decision making—boosting efficiency while reducing operational and compliance risk for energy organizations.

Personas: Plant Manager / Reliability Engineer; Compliance Manager; Sustainability Lead; Data Analyst.
Featured tools: Dynamics 365 CcaaS, Dynamics 365 ERP, Microsoft Teams, SharePoint.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a site by NATURAL reference: a name or a
SITE- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "SITE-10360",
                "subject": "Alpine Ski House",
                "status": "nominal",
                "owner": "Plant Manager / Reliability Engineer",
                "metric": 81.5,
                "note": "Site for Alpine Ski House"
        },
        {
                "reference": "SITE-10361",
                "subject": "Lucerne Publishing",
                "status": "watch",
                "owner": "Compliance Manager",
                "metric": 85.2,
                "note": "Site for Lucerne Publishing"
        },
        {
                "reference": "SITE-10362",
                "subject": "Coho Vineyard",
                "status": "alert",
                "owner": "Sustainability Lead",
                "metric": 88.9,
                "note": "Site for Coho Vineyard"
        },
        {
                "reference": "SITE-10363",
                "subject": "Margie's Travel",
                "status": "maintenance",
                "owner": "Data Analyst",
                "metric": 92.6,
                "note": "Site for Margie's Travel"
        },
        {
                "reference": "SITE-10364",
                "subject": "Fourth Coffee",
                "status": "resolved",
                "owner": "Plant Manager / Reliability Engineer",
                "metric": 96.3,
                "note": "Site for Fourth Coffee"
        }
]


class EnergyOperationsAgentD(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's site records.",
        "Show SITE-10360.",
        "What is the status of Lucerne Publishing?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "EnergyOperationsAgentD"
        self.metadata = {
            "name": self.name,
            "description": (
                "Deliver real-time insights, automate critical workflows, and enable guided decision making—boosting efficiency while reducing operational and compliance risk for energy organizations. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a site by a name or a SITE- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A site reference or a subject "
                                        "name, e.g. SITE-10360 or 'Alpine Ski House'. Pass 'list' to "
                                        "see every site.")},
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
            lines = ["## Energy Operations Agent (d) — site records (Dataverse)"]
            lines += ["%d. **%s** — %s | status: %s | owner: %s"
                      % (n, r["reference"], r["subject"], r["status"], r["owner"])
                      for n, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a site for its detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return "No site matches `%s`. Say 'list' to see all." % ref
        r = hits[0]
        return "\n".join([
            "## %s — %s" % (r["reference"], r["subject"]),
            "- Status: **%s**" % r["status"],
            "- Owner: %s" % r["owner"],
            "- Key metric: %s" % r["metric"],
            "- %s" % r["note"],
        ])
