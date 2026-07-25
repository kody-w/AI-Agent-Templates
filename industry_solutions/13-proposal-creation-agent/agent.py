"""Proposal Creation Agent — Cross-Industry industry solution (AIBAST).

Automate proposal creation to accelerate deal cycles, improve win rates, and deliver consistent, high-quality responses.

Personas: Account Executive; Sales Leader; Bid Manager.
Featured tools: Dynamics 365 CRM, Microsoft Teams, Microsoft Word, Microsoft PowerPoint.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a opportunity by NATURAL reference: a name or a
OPP- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "OPP-10260",
                "subject": "Northwind Traders",
                "status": "qualifying",
                "owner": "Account Executive",
                "metric": 77.0,
                "note": "Opportunity for Northwind Traders"
        },
        {
                "reference": "OPP-10261",
                "subject": "Fabrikam",
                "status": "proposal",
                "owner": "Sales Leader",
                "metric": 80.7,
                "note": "Opportunity for Fabrikam"
        },
        {
                "reference": "OPP-10262",
                "subject": "Adatum",
                "status": "negotiation",
                "owner": "Bid Manager",
                "metric": 84.4,
                "note": "Opportunity for Adatum"
        },
        {
                "reference": "OPP-10263",
                "subject": "Trey Research",
                "status": "won",
                "owner": "Account Executive",
                "metric": 88.1,
                "note": "Opportunity for Trey Research"
        },
        {
                "reference": "OPP-10264",
                "subject": "Woodgrove Bank",
                "status": "at risk",
                "owner": "Sales Leader",
                "metric": 91.8,
                "note": "Opportunity for Woodgrove Bank"
        }
]


class ProposalCreationAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's opportunity records.",
        "Show OPP-10260.",
        "What is the status of Fabrikam?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "ProposalCreationAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate proposal creation to accelerate deal cycles, improve win rates, and deliver consistent, high-quality responses. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a opportunity by a name or a OPP- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A opportunity reference or a subject "
                                        "name, e.g. OPP-10260 or 'Northwind Traders'. Pass 'list' to "
                                        "see every opportunity.")},
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
            lines = ["## Proposal Creation Agent — opportunity records (Dataverse)"]
            lines += ["%d. **%s** — %s | status: %s | owner: %s"
                      % (n, r["reference"], r["subject"], r["status"], r["owner"])
                      for n, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a opportunity for its detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return "No opportunity matches `%s`. Say 'list' to see all." % ref
        r = hits[0]
        return "\n".join([
            "## %s — %s" % (r["reference"], r["subject"]),
            "- Status: **%s**" % r["status"],
            "- Owner: %s" % r["owner"],
            "- Key metric: %s" % r["metric"],
            "- %s" % r["note"],
        ])
