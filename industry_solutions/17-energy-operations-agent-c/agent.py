"""Energy Operations Agent (c) — Energy and Utilities industry solution (AIBAST).

Deliver real-time insights, automate critical workflows, and enable guided decision making—boosting efficiency while reducing operational and compliance risk for energy organizations.

Personas: Plant Manager / Reliability Engineer; Compliance Manager; Sustainability Lead; Data Analyst.
Featured tools: Dynamics 365 ERP, Dynamics 365 CRM, SharePoint, Microsoft Teams.

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
                "reference": "SITE-10340",
                "subject": "Woodgrove Bank",
                "status": "nominal",
                "owner": "Plant Manager / Reliability Engineer",
                "metric": 63.0,
                "note": "Site for Woodgrove Bank"
        },
        {
                "reference": "SITE-10341",
                "subject": "Wingtip Toys",
                "status": "watch",
                "owner": "Compliance Manager",
                "metric": 66.7,
                "note": "Site for Wingtip Toys"
        },
        {
                "reference": "SITE-10342",
                "subject": "Tailwind Traders",
                "status": "alert",
                "owner": "Sustainability Lead",
                "metric": 70.4,
                "note": "Site for Tailwind Traders"
        },
        {
                "reference": "SITE-10343",
                "subject": "Proseware",
                "status": "maintenance",
                "owner": "Data Analyst",
                "metric": 74.1,
                "note": "Site for Proseware"
        },
        {
                "reference": "SITE-10344",
                "subject": "Litware",
                "status": "resolved",
                "owner": "Plant Manager / Reliability Engineer",
                "metric": 77.8,
                "note": "Site for Litware"
        }
]


class EnergyOperationsAgentC(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's site records.",
        "Show SITE-10340.",
        "What is the status of Wingtip Toys?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "EnergyOperationsAgentC"
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
                                        "name, e.g. SITE-10340 or 'Woodgrove Bank'. Pass 'list' to "
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
            lines = ["## Energy Operations Agent (c) — site records (Dataverse)"]
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
