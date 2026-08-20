"""Commercial Underwriting Agent — Financial Services industry solution (AIBAST).

Automate commercial underwriting analysis to accelerate evaluations, improve pricing accuracy, and maintain full compliance.

Personas: Underwriter; Risk Analyst.
Featured tools: Dynamics 365 ERP, Dynamics 365 CRM, Dynamics 365 Commerce, Microsoft Teams.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a application by NATURAL reference: a name or a
APP- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "APP-10600",
                "subject": "Wingtip Toys",
                "status": "submitted",
                "owner": "Underwriter",
                "metric": 39.5,
                "note": "Application for Wingtip Toys"
        },
        {
                "reference": "APP-10601",
                "subject": "Tailwind Traders",
                "status": "in review",
                "owner": "Risk Analyst",
                "metric": 43.2,
                "note": "Application for Tailwind Traders"
        },
        {
                "reference": "APP-10602",
                "subject": "Proseware",
                "status": "approved",
                "owner": "Underwriter",
                "metric": 46.9,
                "note": "Application for Proseware"
        },
        {
                "reference": "APP-10603",
                "subject": "Litware",
                "status": "referred",
                "owner": "Risk Analyst",
                "metric": 50.6,
                "note": "Application for Litware"
        },
        {
                "reference": "APP-10604",
                "subject": "Alpine Ski House",
                "status": "declined",
                "owner": "Underwriter",
                "metric": 54.3,
                "note": "Application for Alpine Ski House"
        }
]


class CommercialUnderwritingAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's application records.",
        "Show APP-10600.",
        "What is the status of Tailwind Traders?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "CommercialUnderwritingAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate commercial underwriting analysis to accelerate evaluations, improve pricing accuracy, and maintain full compliance. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a application by a name or a APP- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A application reference or a subject "
                                        "name, e.g. APP-10600 or 'Wingtip Toys'. Pass 'list' to "
                                        "see every application.")},
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
            lines = ["## Commercial Underwriting Agent — application records (Dataverse)"]
            lines += ["%d. **%s** — %s | status: %s | owner: %s"
                      % (n, r["reference"], r["subject"], r["status"], r["owner"])
                      for n, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a application for its detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return "No application matches `%s`. Say 'list' to see all." % ref
        r = hits[0]
        return "\n".join([
            "## %s — %s" % (r["reference"], r["subject"]),
            "- Status: **%s**" % r["status"],
            "- Owner: %s" % r["owner"],
            "- Key metric: %s" % r["metric"],
            "- %s" % r["note"],
        ])
