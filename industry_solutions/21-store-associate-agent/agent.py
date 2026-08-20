"""Store Associate Agent — Retail industry solution (AIBAST).

Deliver real-time product intelligence and transaction support to deliver faster service and boost sales performance.

Personas: Store Associate; Sales Manager; Floor Specialist.
Featured tools: Dynamics 365 CRM, Dynamics 365 ERP, Microsoft Teams, Microsoft Outlook.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a record by NATURAL reference: a name or a
REC- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "REC-10420",
                "subject": "Litware",
                "status": "open",
                "owner": "Store Associate",
                "metric": 49.0,
                "note": "Record for Litware"
        },
        {
                "reference": "REC-10421",
                "subject": "Alpine Ski House",
                "status": "in progress",
                "owner": "Sales Manager",
                "metric": 52.7,
                "note": "Record for Alpine Ski House"
        },
        {
                "reference": "REC-10422",
                "subject": "Lucerne Publishing",
                "status": "resolved",
                "owner": "Floor Specialist",
                "metric": 56.4,
                "note": "Record for Lucerne Publishing"
        },
        {
                "reference": "REC-10423",
                "subject": "Coho Vineyard",
                "status": "escalated",
                "owner": "Store Associate",
                "metric": 60.1,
                "note": "Record for Coho Vineyard"
        },
        {
                "reference": "REC-10424",
                "subject": "Margie's Travel",
                "status": "closed",
                "owner": "Sales Manager",
                "metric": 63.8,
                "note": "Record for Margie's Travel"
        }
]


class StoreAssociateAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's record records.",
        "Show REC-10420.",
        "What is the status of Alpine Ski House?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "StoreAssociateAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Deliver real-time product intelligence and transaction support to deliver faster service and boost sales performance. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a record by a name or a REC- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A record reference or a subject "
                                        "name, e.g. REC-10420 or 'Litware'. Pass 'list' to "
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
            lines = ["## Store Associate Agent — record records (Dataverse)"]
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
