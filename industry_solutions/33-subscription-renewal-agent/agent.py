"""Subscription Renewal Agent — Software Tech industry solution (AIBAST).

Streamline subscription renewal management and expansion planning, turning risk into growth opportunities while increasing win probability.

Personas: Account Executives; Customer Success Managers; Sales Leadership.
Featured tools: Dynamics 365 CRM, Microsoft Teams.

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
                "reference": "OPP-10660",
                "subject": "Woodgrove Bank",
                "status": "qualifying",
                "owner": "Account Executives",
                "metric": 95.0,
                "note": "Opportunity for Woodgrove Bank"
        },
        {
                "reference": "OPP-10661",
                "subject": "Wingtip Toys",
                "status": "proposal",
                "owner": "Customer Success Managers",
                "metric": 98.7,
                "note": "Opportunity for Wingtip Toys"
        },
        {
                "reference": "OPP-10662",
                "subject": "Tailwind Traders",
                "status": "negotiation",
                "owner": "Sales Leadership",
                "metric": 14.4,
                "note": "Opportunity for Tailwind Traders"
        },
        {
                "reference": "OPP-10663",
                "subject": "Proseware",
                "status": "won",
                "owner": "Account Executives",
                "metric": 18.1,
                "note": "Opportunity for Proseware"
        },
        {
                "reference": "OPP-10664",
                "subject": "Litware",
                "status": "at risk",
                "owner": "Customer Success Managers",
                "metric": 21.8,
                "note": "Opportunity for Litware"
        }
]


class SubscriptionRenewalAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's opportunity records.",
        "Show OPP-10660.",
        "What is the status of Wingtip Toys?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "SubscriptionRenewalAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Streamline subscription renewal management and expansion planning, turning risk into growth opportunities while increasing win probability. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a opportunity by a name or a OPP- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A opportunity reference or a subject "
                                        "name, e.g. OPP-10660 or 'Woodgrove Bank'. Pass 'list' to "
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
            lines = ["## Subscription Renewal Agent — opportunity records (Dataverse)"]
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
