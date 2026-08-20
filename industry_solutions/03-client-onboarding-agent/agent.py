"""Client Onboarding Agent — Cross-Industry, Financial Services industry solution (AIBAST).

Orchestrate client onboarding journeys with unified workflows to accelerate revenue and mitigate compliance risk.

Personas: Onboarding Specialist; Relationship Manager; Compliance Officer.
Featured tools: Dynamics 365 ERP, SharePoint, Microsoft Teams.

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
                "reference": "CS-10060",
                "subject": "Graphic Design Institute",
                "status": "open",
                "owner": "Onboarding Specialist",
                "metric": 68.0,
                "note": "Case for Graphic Design Institute"
        },
        {
                "reference": "CS-10061",
                "subject": "Contoso",
                "status": "in progress",
                "owner": "Relationship Manager",
                "metric": 71.7,
                "note": "Case for Contoso"
        },
        {
                "reference": "CS-10062",
                "subject": "Northwind Traders",
                "status": "resolved",
                "owner": "Compliance Officer",
                "metric": 75.4,
                "note": "Case for Northwind Traders"
        },
        {
                "reference": "CS-10063",
                "subject": "Fabrikam",
                "status": "escalated",
                "owner": "Onboarding Specialist",
                "metric": 79.1,
                "note": "Case for Fabrikam"
        },
        {
                "reference": "CS-10064",
                "subject": "Adatum",
                "status": "closed",
                "owner": "Relationship Manager",
                "metric": 82.8,
                "note": "Case for Adatum"
        }
]


class ClientOnboardingAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's case records.",
        "Show CS-10060.",
        "What is the status of Contoso?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "ClientOnboardingAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Orchestrate client onboarding journeys with unified workflows to accelerate revenue and mitigate compliance risk. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a case by a name or a CS- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A case reference or a subject "
                                        "name, e.g. CS-10060 or 'Graphic Design Institute'. Pass 'list' to "
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
            lines = ["## Client Onboarding Agent — case records (Dataverse)"]
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
