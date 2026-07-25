"""Procurement Savings Agent — Cross-Industry industry solution (AIBAST).

Identify and optimize savings opportunities across vendors, contracts, and purchasing cycles to reduce costs and increase procurement efficiency.

Personas: Procurement Manager; Finance Director; Category Buyer.
Featured tools: Dynamics 365 ERP, Dynamics 365 CRM, Dynamics 365 Commerce, Microsoft Teams.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a order by NATURAL reference: a name or a
PO- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "PO-10520",
                "subject": "Fabrikam",
                "status": "placed",
                "owner": "Procurement Manager",
                "metric": 53.5,
                "note": "Order for Fabrikam"
        },
        {
                "reference": "PO-10521",
                "subject": "Adatum",
                "status": "approved",
                "owner": "Finance Director",
                "metric": 57.2,
                "note": "Order for Adatum"
        },
        {
                "reference": "PO-10522",
                "subject": "Trey Research",
                "status": "in transit",
                "owner": "Category Buyer",
                "metric": 60.9,
                "note": "Order for Trey Research"
        },
        {
                "reference": "PO-10523",
                "subject": "Woodgrove Bank",
                "status": "delivered",
                "owner": "Procurement Manager",
                "metric": 64.6,
                "note": "Order for Woodgrove Bank"
        },
        {
                "reference": "PO-10524",
                "subject": "Wingtip Toys",
                "status": "delayed",
                "owner": "Finance Director",
                "metric": 68.3,
                "note": "Order for Wingtip Toys"
        }
]


class ProcurementSavingsAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's order records.",
        "Show PO-10520.",
        "What is the status of Adatum?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "ProcurementSavingsAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Identify and optimize savings opportunities across vendors, contracts, and purchasing cycles to reduce costs and increase procurement efficiency. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a order by a name or a PO- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A order reference or a subject "
                                        "name, e.g. PO-10520 or 'Fabrikam'. Pass 'list' to "
                                        "see every order.")},
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
            lines = ["## Procurement Savings Agent — order records (Dataverse)"]
            lines += ["%d. **%s** — %s | status: %s | owner: %s"
                      % (n, r["reference"], r["subject"], r["status"], r["owner"])
                      for n, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a order for its detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return "No order matches `%s`. Say 'list' to see all." % ref
        r = hits[0]
        return "\n".join([
            "## %s — %s" % (r["reference"], r["subject"]),
            "- Status: **%s**" % r["status"],
            "- Owner: %s" % r["owner"],
            "- Key metric: %s" % r["metric"],
            "- %s" % r["note"],
        ])
