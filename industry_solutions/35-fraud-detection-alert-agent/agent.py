"""Fraud Detection & Alert Agent — Financial Services industry solution (AIBAST).

Deploy AI-driven fraud monitoring and identification to accelerate investigations, enhance detection rates, and improve prevention.

Personas: Fraud Analysts; SIU Investigators; Risk Leaders.
Featured tools: Dynamics 365 ERP, Microsoft Teams.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a case by NATURAL reference: a name or a
FRD- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "FRD-10700",
                "subject": "Graphic Design Institute",
                "status": "flagged",
                "owner": "Fraud Analysts",
                "metric": 44.0,
                "note": "Case for Graphic Design Institute"
        },
        {
                "reference": "FRD-10701",
                "subject": "Contoso",
                "status": "under review",
                "owner": "SIU Investigators",
                "metric": 47.7,
                "note": "Case for Contoso"
        },
        {
                "reference": "FRD-10702",
                "subject": "Northwind Traders",
                "status": "cleared",
                "owner": "Risk Leaders",
                "metric": 51.4,
                "note": "Case for Northwind Traders"
        },
        {
                "reference": "FRD-10703",
                "subject": "Fabrikam",
                "status": "confirmed fraud",
                "owner": "Fraud Analysts",
                "metric": 55.1,
                "note": "Case for Fabrikam"
        },
        {
                "reference": "FRD-10704",
                "subject": "Adatum",
                "status": "escalated",
                "owner": "SIU Investigators",
                "metric": 58.8,
                "note": "Case for Adatum"
        }
]


class FraudDetectionAlertAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's case records.",
        "Show FRD-10700.",
        "What is the status of Contoso?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "FraudDetectionAlertAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Deploy AI-driven fraud monitoring and identification to accelerate investigations, enhance detection rates, and improve prevention. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a case by a name or a FRD- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A case reference or a subject "
                                        "name, e.g. FRD-10700 or 'Graphic Design Institute'. Pass 'list' to "
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
            lines = ["## Fraud Detection & Alert Agent — case records (Dataverse)"]
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
