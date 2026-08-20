"""Resource Utilization Agent — Professional Services, Consulting industry solution (AIBAST).

Provide intelligent resource analysis and recommendations to maximize billable utilization and reduce costs.

Personas: Operations Leader; Resource Manager; Finance Director.
Featured tools: Dynamics 365 ERP, Microsoft Teams.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a case by NATURAL reference: a name or a
CS- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "CS-10180",
                "subject": "Margie's Travel",
                "status": "open",
                "owner": "Operations Leader",
                "metric": 91.0,
                "note": "Case for Margie's Travel"
        },
        {
                "reference": "CS-10181",
                "subject": "Fourth Coffee",
                "status": "in progress",
                "owner": "Resource Manager",
                "metric": 94.7,
                "note": "Case for Fourth Coffee"
        },
        {
                "reference": "CS-10182",
                "subject": "Graphic Design Institute",
                "status": "resolved",
                "owner": "Finance Director",
                "metric": 98.4,
                "note": "Case for Graphic Design Institute"
        },
        {
                "reference": "CS-10183",
                "subject": "Contoso",
                "status": "escalated",
                "owner": "Operations Leader",
                "metric": 14.1,
                "note": "Case for Contoso"
        },
        {
                "reference": "CS-10184",
                "subject": "Northwind Traders",
                "status": "closed",
                "owner": "Resource Manager",
                "metric": 17.8,
                "note": "Case for Northwind Traders"
        }
]


class ResourceUtilizationAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's case records.",
        "Show CS-10180.",
        "What is the status of Fourth Coffee?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "ResourceUtilizationAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Provide intelligent resource analysis and recommendations to maximize billable utilization and reduce costs. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a case by a name or a CS- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A case reference or a subject "
                                        "name, e.g. CS-10180 or 'Margie's Travel'. Pass 'list' to "
                                        "see every case.")},
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
            lines = ["## Resource Utilization Agent — case records (Dataverse)"]
            lines += ["%d. **%s** — %s | status: %s | owner: %s"
                      % (n, r["reference"], r["subject"], r["status"], r["owner"])
                      for n, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a case for its detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return "No case matches `%s`. Say 'list' to see all." % ref
        r = hits[0]
        return "\n".join([
            "## %s — %s" % (r["reference"], r["subject"]),
            "- Status: **%s**" % r["status"],
            "- Owner: %s" % r["owner"],
            "- Key metric: %s" % r["metric"],
            "- %s" % r["note"],
        ])
