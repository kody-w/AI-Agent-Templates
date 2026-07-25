"""Customer Sentiment & Churn Agent — Financial Services industry solution (AIBAST).

Deliver AI-powered sentiment intelligence that detects churn risk early and enables proactive retention strategies.

Personas: Relationship Managers; Retention Specialists; Customer Success Teams.
Featured tools: Dynamics 365 CRM, Microsoft Teams.

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
                "reference": "CS-10680",
                "subject": "Alpine Ski House",
                "status": "open",
                "owner": "Relationship Managers",
                "metric": 25.5,
                "note": "Case for Alpine Ski House"
        },
        {
                "reference": "CS-10681",
                "subject": "Lucerne Publishing",
                "status": "in progress",
                "owner": "Retention Specialists",
                "metric": 29.2,
                "note": "Case for Lucerne Publishing"
        },
        {
                "reference": "CS-10682",
                "subject": "Coho Vineyard",
                "status": "resolved",
                "owner": "Customer Success Teams",
                "metric": 32.9,
                "note": "Case for Coho Vineyard"
        },
        {
                "reference": "CS-10683",
                "subject": "Margie's Travel",
                "status": "escalated",
                "owner": "Relationship Managers",
                "metric": 36.6,
                "note": "Case for Margie's Travel"
        },
        {
                "reference": "CS-10684",
                "subject": "Fourth Coffee",
                "status": "closed",
                "owner": "Retention Specialists",
                "metric": 40.3,
                "note": "Case for Fourth Coffee"
        }
]


class CustomerSentimentChurnAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's case records.",
        "Show CS-10680.",
        "What is the status of Lucerne Publishing?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "CustomerSentimentChurnAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Deliver AI-powered sentiment intelligence that detects churn risk early and enables proactive retention strategies. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a case by a name or a CS- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A case reference or a subject "
                                        "name, e.g. CS-10680 or 'Alpine Ski House'. Pass 'list' to "
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
            lines = ["## Customer Sentiment & Churn Agent — case records (Dataverse)"]
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
