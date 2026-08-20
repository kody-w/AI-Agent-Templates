"""Abandoned Cart Recovery Agent — Cross-Industry, Software Tech industry solution (AIBAST).

Automate abandoned cart analysis and recovery campaigns to convert lost sales, protect margins, and improve customer engagement.

Personas: Marketing Manager; Digital Marketing Lead; Growth Manager.
Featured tools: Dynamics 365 ERP, Microsoft Outlook, Microsoft Teams.

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
                "reference": "CX-10440",
                "subject": "Fourth Coffee",
                "status": "new",
                "owner": "Marketing Manager",
                "metric": 67.5,
                "note": "Record for Fourth Coffee"
        },
        {
                "reference": "CX-10441",
                "subject": "Graphic Design Institute",
                "status": "engaged",
                "owner": "Digital Marketing Lead",
                "metric": 71.2,
                "note": "Record for Graphic Design Institute"
        },
        {
                "reference": "CX-10442",
                "subject": "Contoso",
                "status": "converted",
                "owner": "Growth Manager",
                "metric": 74.9,
                "note": "Record for Contoso"
        },
        {
                "reference": "CX-10443",
                "subject": "Northwind Traders",
                "status": "lapsed",
                "owner": "Marketing Manager",
                "metric": 78.6,
                "note": "Record for Northwind Traders"
        },
        {
                "reference": "CX-10444",
                "subject": "Fabrikam",
                "status": "nurture",
                "owner": "Digital Marketing Lead",
                "metric": 82.3,
                "note": "Record for Fabrikam"
        }
]


class AbandonedCartRecoveryAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's record records.",
        "Show CX-10440.",
        "What is the status of Graphic Design Institute?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "AbandonedCartRecoveryAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate abandoned cart analysis and recovery campaigns to convert lost sales, protect margins, and improve customer engagement. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a record by a name or a CX- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A record reference or a subject "
                                        "name, e.g. CX-10440 or 'Fourth Coffee'. Pass 'list' to "
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
            lines = ["## Abandoned Cart Recovery Agent — record records (Dataverse)"]
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
