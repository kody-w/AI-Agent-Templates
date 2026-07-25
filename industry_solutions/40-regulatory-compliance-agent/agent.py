"""Regulatory Compliance Agent — Financial Services industry solution (AIBAST).

Automate compliance monitoring and regulatory reporting to achieve proactive risk management with real-time surveillance.

Personas: Chief Compliance Officers; Compliance Managers; Trading Desk Supervisors.
Featured tools: Microsoft Teams.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a item by NATURAL reference: a name or a
REG- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "REG-10800",
                "subject": "Proseware",
                "status": "open",
                "owner": "Chief Compliance Officers",
                "metric": 48.5,
                "note": "Item for Proseware"
        },
        {
                "reference": "REG-10801",
                "subject": "Litware",
                "status": "in review",
                "owner": "Compliance Managers",
                "metric": 52.2,
                "note": "Item for Litware"
        },
        {
                "reference": "REG-10802",
                "subject": "Alpine Ski House",
                "status": "cleared",
                "owner": "Trading Desk Supervisors",
                "metric": 55.9,
                "note": "Item for Alpine Ski House"
        },
        {
                "reference": "REG-10803",
                "subject": "Lucerne Publishing",
                "status": "flagged",
                "owner": "Chief Compliance Officers",
                "metric": 59.6,
                "note": "Item for Lucerne Publishing"
        },
        {
                "reference": "REG-10804",
                "subject": "Coho Vineyard",
                "status": "remediated",
                "owner": "Compliance Managers",
                "metric": 63.3,
                "note": "Item for Coho Vineyard"
        }
]


class RegulatoryComplianceAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's item records.",
        "Show REG-10800.",
        "What is the status of Litware?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "RegulatoryComplianceAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate compliance monitoring and regulatory reporting to achieve proactive risk management with real-time surveillance. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a item by a name or a REG- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A item reference or a subject "
                                        "name, e.g. REG-10800 or 'Proseware'. Pass 'list' to "
                                        "see every item.")},
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
            lines = ["## Regulatory Compliance Agent — item records (Dataverse)"]
            lines += ["%d. **%s** — %s | status: %s | owner: %s"
                      % (n, r["reference"], r["subject"], r["status"], r["owner"])
                      for n, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a item for its detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return "No item matches `%s`. Say 'list' to see all." % ref
        r = hits[0]
        return "\n".join([
            "## %s — %s" % (r["reference"], r["subject"]),
            "- Status: **%s**" % r["status"],
            "- Owner: %s" % r["owner"],
            "- Key metric: %s" % r["metric"],
            "- %s" % r["note"],
        ])
