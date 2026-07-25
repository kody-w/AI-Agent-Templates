"""Product Feedback Insights Agent — Cross-Industry industry solution (AIBAST).

Turn fragmented feedback into actionable insights that accelerate product improvements, prevent churn, and optimize engineering priorities.

Personas: Product Manager; Engineering Lead; Director of Product.
Featured tools: Dynamics 365 ERP, Microsoft Teams, Dynamics 365 CRM.

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
                "reference": "CX-10460",
                "subject": "Adatum",
                "status": "new",
                "owner": "Product Manager",
                "metric": 86.0,
                "note": "Record for Adatum"
        },
        {
                "reference": "CX-10461",
                "subject": "Trey Research",
                "status": "engaged",
                "owner": "Engineering Lead",
                "metric": 89.7,
                "note": "Record for Trey Research"
        },
        {
                "reference": "CX-10462",
                "subject": "Woodgrove Bank",
                "status": "converted",
                "owner": "Director of Product",
                "metric": 93.4,
                "note": "Record for Woodgrove Bank"
        },
        {
                "reference": "CX-10463",
                "subject": "Wingtip Toys",
                "status": "lapsed",
                "owner": "Product Manager",
                "metric": 97.1,
                "note": "Record for Wingtip Toys"
        },
        {
                "reference": "CX-10464",
                "subject": "Tailwind Traders",
                "status": "nurture",
                "owner": "Engineering Lead",
                "metric": 12.8,
                "note": "Record for Tailwind Traders"
        }
]


class ProductFeedbackInsightsAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's record records.",
        "Show CX-10460.",
        "What is the status of Trey Research?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "ProductFeedbackInsightsAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Turn fragmented feedback into actionable insights that accelerate product improvements, prevent churn, and optimize engineering priorities. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a record by a name or a CX- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A record reference or a subject "
                                        "name, e.g. CX-10460 or 'Adatum'. Pass 'list' to "
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
            lines = ["## Product Feedback Insights Agent — record records (Dataverse)"]
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
