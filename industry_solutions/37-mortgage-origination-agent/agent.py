"""Mortgage Origination Agent — Financial Services industry solution (AIBAST).

Streamline mortgage origination with intelligent automation, enabling faster, more accurate loan decisions.

Personas: Loan Officers; Processors; Underwriters.
Featured tools: Dynamics 365 CRM, Dynamics 365 ERP, Microsoft Teams.

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
                "reference": "APP-10740",
                "subject": "Litware",
                "status": "submitted",
                "owner": "Loan Officers",
                "metric": 81.0,
                "note": "Application for Litware"
        },
        {
                "reference": "APP-10741",
                "subject": "Alpine Ski House",
                "status": "in review",
                "owner": "Processors",
                "metric": 84.7,
                "note": "Application for Alpine Ski House"
        },
        {
                "reference": "APP-10742",
                "subject": "Lucerne Publishing",
                "status": "approved",
                "owner": "Underwriters",
                "metric": 88.4,
                "note": "Application for Lucerne Publishing"
        },
        {
                "reference": "APP-10743",
                "subject": "Coho Vineyard",
                "status": "referred",
                "owner": "Loan Officers",
                "metric": 92.1,
                "note": "Application for Coho Vineyard"
        },
        {
                "reference": "APP-10744",
                "subject": "Margie's Travel",
                "status": "declined",
                "owner": "Processors",
                "metric": 95.8,
                "note": "Application for Margie's Travel"
        }
]


class MortgageOriginationAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's application records.",
        "Show APP-10740.",
        "What is the status of Alpine Ski House?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "MortgageOriginationAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Streamline mortgage origination with intelligent automation, enabling faster, more accurate loan decisions. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a application by a name or a APP- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A application reference or a subject "
                                        "name, e.g. APP-10740 or 'Litware'. Pass 'list' to "
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
            lines = ["## Mortgage Origination Agent — application records (Dataverse)"]
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
