"""Omnichannel Inventory Agent — Retail industry solution (AIBAST).

Deliver real-time cross-channel inventory intelligence to prevent stockouts, reduce overstock, and maximize omnichannel retail performance.

Personas: Inventory Planners; Store Managers; Category Managers.
Featured tools: Dynamics 365 Commerce, Microsoft Teams.

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
                "reference": "SKU-10620",
                "subject": "Lucerne Publishing",
                "status": "in stock",
                "owner": "Inventory Planners",
                "metric": 58.0,
                "note": "Sku for Lucerne Publishing"
        },
        {
                "reference": "SKU-10621",
                "subject": "Coho Vineyard",
                "status": "low",
                "owner": "Store Managers",
                "metric": 61.7,
                "note": "Sku for Coho Vineyard"
        },
        {
                "reference": "SKU-10622",
                "subject": "Margie's Travel",
                "status": "backordered",
                "owner": "Category Managers",
                "metric": 65.4,
                "note": "Sku for Margie's Travel"
        },
        {
                "reference": "SKU-10623",
                "subject": "Fourth Coffee",
                "status": "reorder",
                "owner": "Inventory Planners",
                "metric": 69.1,
                "note": "Sku for Fourth Coffee"
        },
        {
                "reference": "SKU-10624",
                "subject": "Graphic Design Institute",
                "status": "overstock",
                "owner": "Store Managers",
                "metric": 72.8,
                "note": "Sku for Graphic Design Institute"
        }
]


class OmnichannelInventoryAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's SKU records.",
        "Show SKU-10620.",
        "What is the status of Coho Vineyard?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "OmnichannelInventoryAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Deliver real-time cross-channel inventory intelligence to prevent stockouts, reduce overstock, and maximize omnichannel retail performance. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a SKU by a name or a SKU- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A SKU reference or a subject "
                                        "name, e.g. SKU-10620 or 'Lucerne Publishing'. Pass 'list' to "
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
            lines = ["## Omnichannel Inventory Agent — SKU records (Dataverse)"]
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
