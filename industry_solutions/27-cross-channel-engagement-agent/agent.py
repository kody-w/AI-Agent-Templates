"""Cross-Channel Engagement Agent — Cross-Industry, Retail industry solution (AIBAST).

Deliver a single, unified view of cross-channel interactions for more strategic, streamlined support and stronger engagement.

Personas: Customer Experience Leader; Digital Engagement Manager; Contact Center Supervisor.
Featured tools: Dynamics 365 CRM, Dynamics 365 Commerce, Microsoft Outlook.

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
                "reference": "CX-10540",
                "subject": "Tailwind Traders",
                "status": "new",
                "owner": "Customer Experience Leader",
                "metric": 72.0,
                "note": "Record for Tailwind Traders"
        },
        {
                "reference": "CX-10541",
                "subject": "Proseware",
                "status": "engaged",
                "owner": "Digital Engagement Manager",
                "metric": 75.7,
                "note": "Record for Proseware"
        },
        {
                "reference": "CX-10542",
                "subject": "Litware",
                "status": "converted",
                "owner": "Contact Center Supervisor",
                "metric": 79.4,
                "note": "Record for Litware"
        },
        {
                "reference": "CX-10543",
                "subject": "Alpine Ski House",
                "status": "lapsed",
                "owner": "Customer Experience Leader",
                "metric": 83.1,
                "note": "Record for Alpine Ski House"
        },
        {
                "reference": "CX-10544",
                "subject": "Lucerne Publishing",
                "status": "nurture",
                "owner": "Digital Engagement Manager",
                "metric": 86.8,
                "note": "Record for Lucerne Publishing"
        }
]


class CrossChannelEngagementAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's record records.",
        "Show CX-10540.",
        "What is the status of Proseware?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "CrossChannelEngagementAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Deliver a single, unified view of cross-channel interactions for more strategic, streamlined support and stronger engagement. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a record by a name or a CX- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A record reference or a subject "
                                        "name, e.g. CX-10540 or 'Tailwind Traders'. Pass 'list' to "
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
            lines = ["## Cross-Channel Engagement Agent — record records (Dataverse)"]
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
