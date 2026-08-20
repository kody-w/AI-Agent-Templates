"""Utility Leak Detection & Billing Agent — Energy and Utilities, State and Local Government industry solution (AIBAST).

Automate leak detection and billing processes to improve customer satisfaction, ensure policy compliance, and protect municipal revenue.

Personas: Customer Service Rep; Billing Specialist; Assistance Coordinator.
Featured tools: Dynamics 365 ERP, Dynamics 365 CRM, Dynamics 365 CcaaS, Microsoft Outlook, Microsoft Teams.

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
                "reference": "INV-10480",
                "subject": "Proseware",
                "status": "draft",
                "owner": "Customer Service Rep",
                "metric": 16.5,
                "note": "Invoice for Proseware"
        },
        {
                "reference": "INV-10481",
                "subject": "Litware",
                "status": "issued",
                "owner": "Billing Specialist",
                "metric": 20.2,
                "note": "Invoice for Litware"
        },
        {
                "reference": "INV-10482",
                "subject": "Alpine Ski House",
                "status": "paid",
                "owner": "Assistance Coordinator",
                "metric": 23.9,
                "note": "Invoice for Alpine Ski House"
        },
        {
                "reference": "INV-10483",
                "subject": "Lucerne Publishing",
                "status": "overdue",
                "owner": "Customer Service Rep",
                "metric": 27.6,
                "note": "Invoice for Lucerne Publishing"
        },
        {
                "reference": "INV-10484",
                "subject": "Coho Vineyard",
                "status": "disputed",
                "owner": "Billing Specialist",
                "metric": 31.3,
                "note": "Invoice for Coho Vineyard"
        }
]


class UtilityLeakDetectionBillingAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's invoice records.",
        "Show INV-10480.",
        "What is the status of Litware?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "UtilityLeakDetectionBillingAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate leak detection and billing processes to improve customer satisfaction, ensure policy compliance, and protect municipal revenue. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a invoice by a name or a INV- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A invoice reference or a subject "
                                        "name, e.g. INV-10480 or 'Proseware'. Pass 'list' to "
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
            lines = ["## Utility Leak Detection & Billing Agent — invoice records (Dataverse)"]
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
