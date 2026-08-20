"""Month-End Billing Agent — Professional Services, Consulting industry solution (AIBAST).

Automate month-end billing cycles to accelerate invoicing, reduce risk, and ensure audit-ready compliance.

Personas: Finance VP; Billing Manager.
Featured tools: Dynamics 365 ERP, SharePoint, Microsoft Teams.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a invoice by NATURAL reference: a name or a
INV- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "INV-10160",
                "subject": "Proseware",
                "status": "draft",
                "owner": "Finance VP",
                "metric": 72.5,
                "note": "Invoice for Proseware"
        },
        {
                "reference": "INV-10161",
                "subject": "Litware",
                "status": "issued",
                "owner": "Billing Manager",
                "metric": 76.2,
                "note": "Invoice for Litware"
        },
        {
                "reference": "INV-10162",
                "subject": "Alpine Ski House",
                "status": "paid",
                "owner": "Finance VP",
                "metric": 79.9,
                "note": "Invoice for Alpine Ski House"
        },
        {
                "reference": "INV-10163",
                "subject": "Lucerne Publishing",
                "status": "overdue",
                "owner": "Billing Manager",
                "metric": 83.6,
                "note": "Invoice for Lucerne Publishing"
        },
        {
                "reference": "INV-10164",
                "subject": "Coho Vineyard",
                "status": "disputed",
                "owner": "Finance VP",
                "metric": 87.3,
                "note": "Invoice for Coho Vineyard"
        }
]


class MonthEndBillingAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's invoice records.",
        "Show INV-10160.",
        "What is the status of Litware?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "MonthEndBillingAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate month-end billing cycles to accelerate invoicing, reduce risk, and ensure audit-ready compliance. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a invoice by a name or a INV- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A invoice reference or a subject "
                                        "name, e.g. INV-10160 or 'Proseware'. Pass 'list' to "
                                        "see every invoice.")},
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
            lines = ["## Month-End Billing Agent — invoice records (Dataverse)"]
            lines += ["%d. **%s** — %s | status: %s | owner: %s"
                      % (n, r["reference"], r["subject"], r["status"], r["owner"])
                      for n, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a invoice for its detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return "No invoice matches `%s`. Say 'list' to see all." % ref
        r = hits[0]
        return "\n".join([
            "## %s — %s" % (r["reference"], r["subject"]),
            "- Status: **%s**" % r["status"],
            "- Owner: %s" % r["owner"],
            "- Key metric: %s" % r["metric"],
            "- %s" % r["note"],
        ])
