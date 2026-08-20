"""Order Status & Delay Agent — Manufacturing industry solution (AIBAST).

Automate proactive order updates, delay management, and customer communications to protect relationships and revenue.

Personas: Customer Service Rep; Account Manager; Operations Leader.
Featured tools: Dynamics 365 CRM, Dynamics 365 CcaaS, Microsoft Teams.

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
                "reference": "PO-10840",
                "subject": "Fabrikam",
                "status": "placed",
                "owner": "Customer Service Rep",
                "metric": 85.5,
                "note": "Order for Fabrikam"
        },
        {
                "reference": "PO-10841",
                "subject": "Adatum",
                "status": "approved",
                "owner": "Account Manager",
                "metric": 89.2,
                "note": "Order for Adatum"
        },
        {
                "reference": "PO-10842",
                "subject": "Trey Research",
                "status": "in transit",
                "owner": "Operations Leader",
                "metric": 92.9,
                "note": "Order for Trey Research"
        },
        {
                "reference": "PO-10843",
                "subject": "Woodgrove Bank",
                "status": "delivered",
                "owner": "Customer Service Rep",
                "metric": 96.6,
                "note": "Order for Woodgrove Bank"
        },
        {
                "reference": "PO-10844",
                "subject": "Wingtip Toys",
                "status": "delayed",
                "owner": "Account Manager",
                "metric": 100.3,
                "note": "Order for Wingtip Toys"
        }
]


class OrderStatusDelayAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's order records.",
        "Show PO-10840.",
        "What is the status of Adatum?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "OrderStatusDelayAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate proactive order updates, delay management, and customer communications to protect relationships and revenue. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a order by a name or a PO- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A order reference or a subject "
                                        "name, e.g. PO-10840 or 'Fabrikam'. Pass 'list' to "
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
            lines = ["## Order Status & Delay Agent — order records (Dataverse)"]
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
