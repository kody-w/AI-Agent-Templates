"""Account Research Agent — Cross-Industry industry solution (AIBAST).

Automate account research and strategy planning to help sellers prepare faster, win more, and elevate deal quality.

Personas: Account Executive; Sales Director; Customer Success Manager.
Featured tools: Dynamics 365 CRM, SharePoint, Microsoft Teams.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a opportunity by NATURAL reference: a name or a
OPP- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "OPP-10380",
                "subject": "Graphic Design Institute",
                "status": "qualifying",
                "owner": "Account Executive",
                "metric": 100.0,
                "note": "Opportunity for Graphic Design Institute"
        },
        {
                "reference": "OPP-10381",
                "subject": "Contoso",
                "status": "proposal",
                "owner": "Sales Director",
                "metric": 15.7,
                "note": "Opportunity for Contoso"
        },
        {
                "reference": "OPP-10382",
                "subject": "Northwind Traders",
                "status": "negotiation",
                "owner": "Customer Success Manager",
                "metric": 19.4,
                "note": "Opportunity for Northwind Traders"
        },
        {
                "reference": "OPP-10383",
                "subject": "Fabrikam",
                "status": "won",
                "owner": "Account Executive",
                "metric": 23.1,
                "note": "Opportunity for Fabrikam"
        },
        {
                "reference": "OPP-10384",
                "subject": "Adatum",
                "status": "at risk",
                "owner": "Sales Director",
                "metric": 26.8,
                "note": "Opportunity for Adatum"
        }
]


class AccountResearchAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's opportunity records.",
        "Show OPP-10380.",
        "What is the status of Contoso?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "AccountResearchAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate account research and strategy planning to help sellers prepare faster, win more, and elevate deal quality. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a opportunity by a name or a OPP- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A opportunity reference or a subject "
                                        "name, e.g. OPP-10380 or 'Graphic Design Institute'. Pass 'list' to "
                                        "see every opportunity.")},
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
            lines = ["## Account Research Agent — opportunity records (Dataverse)"]
            lines += ["%d. **%s** — %s | status: %s | owner: %s"
                      % (n, r["reference"], r["subject"], r["status"], r["owner"])
                      for n, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a opportunity for its detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return "No opportunity matches `%s`. Say 'list' to see all." % ref
        r = hits[0]
        return "\n".join([
            "## %s — %s" % (r["reference"], r["subject"]),
            "- Status: **%s**" % r["status"],
            "- Owner: %s" % r["owner"],
            "- Key metric: %s" % r["metric"],
            "- %s" % r["note"],
        ])
