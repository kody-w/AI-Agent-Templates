"""Campaign Design Agent — Retail industry solution (AIBAST).

Automate personalized campaign design and execution to boost engagement, accelerate revenue, and strengthen customer loyalty.

Personas: Marketing Director; Campaign Manager.
Featured tools: Dynamics 365 CRM, Microsoft Teams.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a record by NATURAL reference: a name or a
CX- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "CX-10280",
                "subject": "Wingtip Toys",
                "status": "new",
                "owner": "Marketing Director",
                "metric": 95.5,
                "note": "Record for Wingtip Toys"
        },
        {
                "reference": "CX-10281",
                "subject": "Tailwind Traders",
                "status": "engaged",
                "owner": "Campaign Manager",
                "metric": 99.2,
                "note": "Record for Tailwind Traders"
        },
        {
                "reference": "CX-10282",
                "subject": "Proseware",
                "status": "converted",
                "owner": "Marketing Director",
                "metric": 14.9,
                "note": "Record for Proseware"
        },
        {
                "reference": "CX-10283",
                "subject": "Litware",
                "status": "lapsed",
                "owner": "Campaign Manager",
                "metric": 18.6,
                "note": "Record for Litware"
        },
        {
                "reference": "CX-10284",
                "subject": "Alpine Ski House",
                "status": "nurture",
                "owner": "Marketing Director",
                "metric": 22.3,
                "note": "Record for Alpine Ski House"
        }
]


class CampaignDesignAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's record records.",
        "Show CX-10280.",
        "What is the status of Tailwind Traders?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "CampaignDesignAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate personalized campaign design and execution to boost engagement, accelerate revenue, and strengthen customer loyalty. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a record by a name or a CX- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A record reference or a subject "
                                        "name, e.g. CX-10280 or 'Wingtip Toys'. Pass 'list' to "
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
            lines = ["## Campaign Design Agent — record records (Dataverse)"]
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
