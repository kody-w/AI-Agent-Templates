"""Personal Styling Agent — Retail industry solution (AIBAST).

Deliver intelligent personal styling to strengthen customer experience, increase revenue, and elevate associate efficiency at scale.

Personas: Personal Shoppers; Clienteling Specialists; Retail Managers.
Featured tools: Dynamics 365 CRM, Microsoft Outlook.

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
                "reference": "CX-10760",
                "subject": "Fourth Coffee",
                "status": "new",
                "owner": "Personal Shoppers",
                "metric": 99.5,
                "note": "Record for Fourth Coffee"
        },
        {
                "reference": "CX-10761",
                "subject": "Graphic Design Institute",
                "status": "engaged",
                "owner": "Clienteling Specialists",
                "metric": 15.2,
                "note": "Record for Graphic Design Institute"
        },
        {
                "reference": "CX-10762",
                "subject": "Contoso",
                "status": "converted",
                "owner": "Retail Managers",
                "metric": 18.9,
                "note": "Record for Contoso"
        },
        {
                "reference": "CX-10763",
                "subject": "Northwind Traders",
                "status": "lapsed",
                "owner": "Personal Shoppers",
                "metric": 22.6,
                "note": "Record for Northwind Traders"
        },
        {
                "reference": "CX-10764",
                "subject": "Fabrikam",
                "status": "nurture",
                "owner": "Clienteling Specialists",
                "metric": 26.3,
                "note": "Record for Fabrikam"
        }
]


class PersonalStylingAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's record records.",
        "Show CX-10760.",
        "What is the status of Graphic Design Institute?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "PersonalStylingAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Deliver intelligent personal styling to strengthen customer experience, increase revenue, and elevate associate efficiency at scale. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a record by a name or a CX- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A record reference or a subject "
                                        "name, e.g. CX-10760 or 'Fourth Coffee'. Pass 'list' to "
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
            lines = ["## Personal Styling Agent — record records (Dataverse)"]
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
