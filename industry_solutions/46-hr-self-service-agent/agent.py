"""HR Self-Service Agent — Cross-Industry industry solution (AIBAST).

Provide self-service HR inquiry handling that transforms the process from a manual ticket-based system to intelligent, automated resolutions.

Personas: Employees; Managers; HR Operations Staff.
Featured tools: Microsoft Outlook, Microsoft Teams.

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
                "reference": "CS-10920",
                "subject": "Wingtip Toys",
                "status": "open",
                "owner": "Employees",
                "metric": 71.5,
                "note": "Case for Wingtip Toys"
        },
        {
                "reference": "CS-10921",
                "subject": "Tailwind Traders",
                "status": "in progress",
                "owner": "Managers",
                "metric": 75.2,
                "note": "Case for Tailwind Traders"
        },
        {
                "reference": "CS-10922",
                "subject": "Proseware",
                "status": "resolved",
                "owner": "HR Operations Staff",
                "metric": 78.9,
                "note": "Case for Proseware"
        },
        {
                "reference": "CS-10923",
                "subject": "Litware",
                "status": "escalated",
                "owner": "Employees",
                "metric": 82.6,
                "note": "Case for Litware"
        },
        {
                "reference": "CS-10924",
                "subject": "Alpine Ski House",
                "status": "closed",
                "owner": "Managers",
                "metric": 86.3,
                "note": "Case for Alpine Ski House"
        }
]


class HrSelfServiceAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's case records.",
        "Show CS-10920.",
        "What is the status of Tailwind Traders?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "HrSelfServiceAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Provide self-service HR inquiry handling that transforms the process from a manual ticket-based system to intelligent, automated resolutions. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a case by a name or a CS- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A case reference or a subject "
                                        "name, e.g. CS-10920 or 'Wingtip Toys'. Pass 'list' to "
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
            lines = ["## HR Self-Service Agent — case records (Dataverse)"]
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
