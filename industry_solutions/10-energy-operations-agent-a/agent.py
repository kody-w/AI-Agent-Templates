"""Energy Operations Agent (a) — Energy and Utilities industry solution (AIBAST).

Deliver real-time insights, automate critical workflows, and enable guided decision making—boosting efficiency while reducing operational and compliance risk for energy organizations.

Personas: Plant Manager / Reliability Engineer; Compliance Manager; Sustainability Lead; Data Analyst.
Featured tools: Dynamics 365 ERP, SharePoint, Microsoft Teams.

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
                "reference": "SITE-10200",
                "subject": "Fabrikam",
                "status": "nominal",
                "owner": "Plant Manager / Reliability Engineer",
                "metric": 21.5,
                "note": "Site for Fabrikam"
        },
        {
                "reference": "SITE-10201",
                "subject": "Adatum",
                "status": "watch",
                "owner": "Compliance Manager",
                "metric": 25.2,
                "note": "Site for Adatum"
        },
        {
                "reference": "SITE-10202",
                "subject": "Trey Research",
                "status": "alert",
                "owner": "Sustainability Lead",
                "metric": 28.9,
                "note": "Site for Trey Research"
        },
        {
                "reference": "SITE-10203",
                "subject": "Woodgrove Bank",
                "status": "maintenance",
                "owner": "Data Analyst",
                "metric": 32.6,
                "note": "Site for Woodgrove Bank"
        },
        {
                "reference": "SITE-10204",
                "subject": "Wingtip Toys",
                "status": "resolved",
                "owner": "Plant Manager / Reliability Engineer",
                "metric": 36.3,
                "note": "Site for Wingtip Toys"
        }
]


class EnergyOperationsAgentA(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's site records.",
        "Show SITE-10200.",
        "What is the status of Adatum?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "EnergyOperationsAgentA"
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
                                        "name, e.g. SITE-10200 or 'Fabrikam'. Pass 'list' to "
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
            lines = ["## Energy Operations Agent (a) — site records (Dataverse)"]
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
