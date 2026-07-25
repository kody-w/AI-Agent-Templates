"""Inventory Optimization Agent — Manufacturing industry solution (AIBAST).

Intelligently optimize inventory portfolios to improve cash flow and warehouse efficiency while reducing waste.

Personas: Supply Chain Managers; Inventory Managers; Procurement Manager.
Featured tools: Dynamics 365 ERP, Microsoft Teams, Dynamics 365 Commerce.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a SKU by NATURAL reference: a name or a
SKU- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "SKU-10140",
                "subject": "Adatum",
                "status": "in stock",
                "owner": "Supply Chain Managers",
                "metric": 54.0,
                "note": "Sku for Adatum"
        },
        {
                "reference": "SKU-10141",
                "subject": "Trey Research",
                "status": "low",
                "owner": "Inventory Managers",
                "metric": 57.7,
                "note": "Sku for Trey Research"
        },
        {
                "reference": "SKU-10142",
                "subject": "Woodgrove Bank",
                "status": "backordered",
                "owner": "Procurement Manager",
                "metric": 61.4,
                "note": "Sku for Woodgrove Bank"
        },
        {
                "reference": "SKU-10143",
                "subject": "Wingtip Toys",
                "status": "reorder",
                "owner": "Supply Chain Managers",
                "metric": 65.1,
                "note": "Sku for Wingtip Toys"
        },
        {
                "reference": "SKU-10144",
                "subject": "Tailwind Traders",
                "status": "overstock",
                "owner": "Inventory Managers",
                "metric": 68.8,
                "note": "Sku for Tailwind Traders"
        }
]


class InventoryOptimizationAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's SKU records.",
        "Show SKU-10140.",
        "What is the status of Trey Research?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "InventoryOptimizationAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Intelligently optimize inventory portfolios to improve cash flow and warehouse efficiency while reducing waste. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a SKU by a name or a SKU- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A SKU reference or a subject "
                                        "name, e.g. SKU-10140 or 'Adatum'. Pass 'list' to "
                                        "see every SKU.")},
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
            lines = ["## Inventory Optimization Agent — SKU records (Dataverse)"]
            lines += ["%d. **%s** — %s | status: %s | owner: %s"
                      % (n, r["reference"], r["subject"], r["status"], r["owner"])
                      for n, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a SKU for its detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return "No SKU matches `%s`. Say 'list' to see all." % ref
        r = hits[0]
        return "\n".join([
            "## %s — %s" % (r["reference"], r["subject"]),
            "- Status: **%s**" % r["status"],
            "- Owner: %s" % r["owner"],
            "- Key metric: %s" % r["metric"],
            "- %s" % r["note"],
        ])
