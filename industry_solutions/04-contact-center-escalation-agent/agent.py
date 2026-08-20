"""Contact Center Escalation Agent — Cross-Industry, Contact Center industry solution (AIBAST).

Automate back-office contact center escalation workflows to deliver better service outcomes and retention rates.

Personas: Back-Office Agent; Escalation Manager; Quality Analyst.
Featured tools: Dynamics 365 CcaaS, Dynamics 365 CRM, SharePoint, Microsoft Teams, Microsoft Outlook.

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
                "reference": "CS-10080",
                "subject": "Trey Research",
                "status": "open",
                "owner": "Back-Office Agent",
                "metric": 86.5,
                "note": "Case for Trey Research"
        },
        {
                "reference": "CS-10081",
                "subject": "Woodgrove Bank",
                "status": "in progress",
                "owner": "Escalation Manager",
                "metric": 90.2,
                "note": "Case for Woodgrove Bank"
        },
        {
                "reference": "CS-10082",
                "subject": "Wingtip Toys",
                "status": "resolved",
                "owner": "Quality Analyst",
                "metric": 93.9,
                "note": "Case for Wingtip Toys"
        },
        {
                "reference": "CS-10083",
                "subject": "Tailwind Traders",
                "status": "escalated",
                "owner": "Back-Office Agent",
                "metric": 97.6,
                "note": "Case for Tailwind Traders"
        },
        {
                "reference": "CS-10084",
                "subject": "Proseware",
                "status": "closed",
                "owner": "Escalation Manager",
                "metric": 13.3,
                "note": "Case for Proseware"
        }
]


class ContactCenterEscalationAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's case records.",
        "Show CS-10080.",
        "What is the status of Woodgrove Bank?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "ContactCenterEscalationAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate back-office contact center escalation workflows to deliver better service outcomes and retention rates. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a case by a name or a CS- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A case reference or a subject "
                                        "name, e.g. CS-10080 or 'Trey Research'. Pass 'list' to "
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
            lines = ["## Contact Center Escalation Agent — case records (Dataverse)"]
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
