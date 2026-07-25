"""Wealth Insights Agent — Financial Services industry solution (AIBAST).

Deliver AI-powered portfolio intelligence to uncover hidden asset opportunities, strengthen client relationships, and drive advisory growth at scale.

Personas: Wealth Advisor; Relationship Managers; Advisory Directors.
Featured tools: Dynamics 365 CRM, Dynamics 365 ERP, Dynamics 365 CcaaS, Microsoft Outlook.

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
                "reference": "CS-10780",
                "subject": "Adatum",
                "status": "open",
                "owner": "Wealth Advisor",
                "metric": 30.0,
                "note": "Case for Adatum"
        },
        {
                "reference": "CS-10781",
                "subject": "Trey Research",
                "status": "in progress",
                "owner": "Relationship Managers",
                "metric": 33.7,
                "note": "Case for Trey Research"
        },
        {
                "reference": "CS-10782",
                "subject": "Woodgrove Bank",
                "status": "resolved",
                "owner": "Advisory Directors",
                "metric": 37.4,
                "note": "Case for Woodgrove Bank"
        },
        {
                "reference": "CS-10783",
                "subject": "Wingtip Toys",
                "status": "escalated",
                "owner": "Wealth Advisor",
                "metric": 41.1,
                "note": "Case for Wingtip Toys"
        },
        {
                "reference": "CS-10784",
                "subject": "Tailwind Traders",
                "status": "closed",
                "owner": "Relationship Managers",
                "metric": 44.8,
                "note": "Case for Tailwind Traders"
        }
]


class WealthInsightsAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's case records.",
        "Show CS-10780.",
        "What is the status of Trey Research?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "WealthInsightsAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Deliver AI-powered portfolio intelligence to uncover hidden asset opportunities, strengthen client relationships, and drive advisory growth at scale. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a case by a name or a CS- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A case reference or a subject "
                                        "name, e.g. CS-10780 or 'Adatum'. Pass 'list' to "
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
            lines = ["## Wealth Insights Agent — case records (Dataverse)"]
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
