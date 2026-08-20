"""Purchase Order Management Agent — Cross-Industry industry solution (AIBAST).

Automate purchase order management and vendor selection to enable faster and more cost-effective purchasing.

Personas: Procurement Manager; Finance Director; Department Approver.
Featured tools: Dynamics 365 ERP, Microsoft Teams.

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
                "reference": "PO-10120",
                "subject": "Fourth Coffee",
                "status": "placed",
                "owner": "Procurement Manager",
                "metric": 35.5,
                "note": "Order for Fourth Coffee"
        },
        {
                "reference": "PO-10121",
                "subject": "Graphic Design Institute",
                "status": "approved",
                "owner": "Finance Director",
                "metric": 39.2,
                "note": "Order for Graphic Design Institute"
        },
        {
                "reference": "PO-10122",
                "subject": "Contoso",
                "status": "in transit",
                "owner": "Department Approver",
                "metric": 42.9,
                "note": "Order for Contoso"
        },
        {
                "reference": "PO-10123",
                "subject": "Northwind Traders",
                "status": "delivered",
                "owner": "Procurement Manager",
                "metric": 46.6,
                "note": "Order for Northwind Traders"
        },
        {
                "reference": "PO-10124",
                "subject": "Fabrikam",
                "status": "delayed",
                "owner": "Finance Director",
                "metric": 50.3,
                "note": "Order for Fabrikam"
        }
]


class PurchaseOrderManagementAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's order records.",
        "Show PO-10120.",
        "What is the status of Graphic Design Institute?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "PurchaseOrderManagementAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate purchase order management and vendor selection to enable faster and more cost-effective purchasing. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a order by a name or a PO- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A order reference or a subject "
                                        "name, e.g. PO-10120 or 'Fourth Coffee'. Pass 'list' to "
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
            lines = ["## Purchase Order Management Agent — order records (Dataverse)"]
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
