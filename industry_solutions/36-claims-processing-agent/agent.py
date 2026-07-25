"""Claims Processing Agent — Financial Services industry solution (AIBAST).

Automate claims processing workflows to deliver faster, consistent, and more compliant claim outcomes.

Personas: Claims Adjusters / Managers; SIU Teams; Operations Leaders.
Featured tools: Dynamics 365 CRM, Dynamics 365 CcaaS.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a claim by NATURAL reference: a name or a
CLM- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "CLM-10720",
                "subject": "Trey Research",
                "status": "received",
                "owner": "Claims Adjusters / Managers",
                "metric": 62.5,
                "note": "Claim for Trey Research"
        },
        {
                "reference": "CLM-10721",
                "subject": "Woodgrove Bank",
                "status": "in adjudication",
                "owner": "SIU Teams",
                "metric": 66.2,
                "note": "Claim for Woodgrove Bank"
        },
        {
                "reference": "CLM-10722",
                "subject": "Wingtip Toys",
                "status": "approved",
                "owner": "Operations Leaders",
                "metric": 69.9,
                "note": "Claim for Wingtip Toys"
        },
        {
                "reference": "CLM-10723",
                "subject": "Tailwind Traders",
                "status": "denied",
                "owner": "Claims Adjusters / Managers",
                "metric": 73.6,
                "note": "Claim for Tailwind Traders"
        },
        {
                "reference": "CLM-10724",
                "subject": "Proseware",
                "status": "paid",
                "owner": "SIU Teams",
                "metric": 77.3,
                "note": "Claim for Proseware"
        }
]


class ClaimsProcessingAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's claim records.",
        "Show CLM-10720.",
        "What is the status of Woodgrove Bank?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "ClaimsProcessingAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate claims processing workflows to deliver faster, consistent, and more compliant claim outcomes. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a claim by a name or a CLM- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A claim reference or a subject "
                                        "name, e.g. CLM-10720 or 'Trey Research'. Pass 'list' to "
                                        "see every claim.")},
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
            lines = ["## Claims Processing Agent — claim records (Dataverse)"]
            lines += ["%d. **%s** — %s | status: %s | owner: %s"
                      % (n, r["reference"], r["subject"], r["status"], r["owner"])
                      for n, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a claim for its detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return "No claim matches `%s`. Say 'list' to see all." % ref
        r = hits[0]
        return "\n".join([
            "## %s — %s" % (r["reference"], r["subject"]),
            "- Status: **%s**" % r["status"],
            "- Owner: %s" % r["owner"],
            "- Key metric: %s" % r["metric"],
            "- %s" % r["note"],
        ])
