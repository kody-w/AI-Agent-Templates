"""Supply Chain Risk Agent — Retail, Manufacturing industry solution (AIBAST).

Detect and manage supply chain risks to defend against disruptions, protect revenue, and maintain operational continuity.

Personas: Supply Chain Planner; Operations Leader; Procurement Manager.
Featured tools: Dynamics 365 ERP, Microsoft Teams.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a work order by NATURAL reference: a name or a
WO- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "WO-10640",
                "subject": "Contoso",
                "status": "scheduled",
                "owner": "Supply Chain Planner",
                "metric": 76.5,
                "note": "Work order for Contoso"
        },
        {
                "reference": "WO-10641",
                "subject": "Northwind Traders",
                "status": "in progress",
                "owner": "Operations Leader",
                "metric": 80.2,
                "note": "Work order for Northwind Traders"
        },
        {
                "reference": "WO-10642",
                "subject": "Fabrikam",
                "status": "completed",
                "owner": "Procurement Manager",
                "metric": 83.9,
                "note": "Work order for Fabrikam"
        },
        {
                "reference": "WO-10643",
                "subject": "Adatum",
                "status": "overdue",
                "owner": "Supply Chain Planner",
                "metric": 87.6,
                "note": "Work order for Adatum"
        },
        {
                "reference": "WO-10644",
                "subject": "Trey Research",
                "status": "flagged",
                "owner": "Operations Leader",
                "metric": 91.3,
                "note": "Work order for Trey Research"
        }
]


class SupplyChainRiskAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's work order records.",
        "Show WO-10640.",
        "What is the status of Northwind Traders?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "SupplyChainRiskAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Detect and manage supply chain risks to defend against disruptions, protect revenue, and maintain operational continuity. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a work order by a name or a WO- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A work order reference or a subject "
                                        "name, e.g. WO-10640 or 'Contoso'. Pass 'list' to "
                                        "see every work order.")},
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
            lines = ["## Supply Chain Risk Agent — work order records (Dataverse)"]
            lines += ["%d. **%s** — %s | status: %s | owner: %s"
                      % (n, r["reference"], r["subject"], r["status"], r["owner"])
                      for n, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a work order for its detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return "No work order matches `%s`. Say 'list' to see all." % ref
        r = hits[0]
        return "\n".join([
            "## %s — %s" % (r["reference"], r["subject"]),
            "- Status: **%s**" % r["status"],
            "- Owner: %s" % r["owner"],
            "- Key metric: %s" % r["metric"],
            "- %s" % r["note"],
        ])
