"""Client Health Score Agent — Professional Services, Consulting industry solution (AIBAST).

Automate client portfolio health monitoring and planning to improve client relationships, protect revenue, and optimize financial performance.

Personas: Client Success Leaders; Account Manager.
Featured tools: Dynamics 365 CRM, Microsoft Teams, Microsoft Outlook.

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
                "reference": "CS-10320",
                "subject": "Contoso",
                "status": "open",
                "owner": "Client Success Leaders",
                "metric": 44.5,
                "note": "Case for Contoso"
        },
        {
                "reference": "CS-10321",
                "subject": "Northwind Traders",
                "status": "in progress",
                "owner": "Account Manager",
                "metric": 48.2,
                "note": "Case for Northwind Traders"
        },
        {
                "reference": "CS-10322",
                "subject": "Fabrikam",
                "status": "resolved",
                "owner": "Client Success Leaders",
                "metric": 51.9,
                "note": "Case for Fabrikam"
        },
        {
                "reference": "CS-10323",
                "subject": "Adatum",
                "status": "escalated",
                "owner": "Account Manager",
                "metric": 55.6,
                "note": "Case for Adatum"
        },
        {
                "reference": "CS-10324",
                "subject": "Trey Research",
                "status": "closed",
                "owner": "Client Success Leaders",
                "metric": 59.3,
                "note": "Case for Trey Research"
        }
]


class ClientHealthScoreAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's case records.",
        "Show CS-10320.",
        "What is the status of Northwind Traders?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "ClientHealthScoreAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate client portfolio health monitoring and planning to improve client relationships, protect revenue, and optimize financial performance. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a case by a name or a CS- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A case reference or a subject "
                                        "name, e.g. CS-10320 or 'Contoso'. Pass 'list' to "
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
            lines = ["## Client Health Score Agent — case records (Dataverse)"]
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
