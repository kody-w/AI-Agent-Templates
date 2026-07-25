"""Product Line Optimization Agent — Manufacturing industry solution (AIBAST).

Provide intelligent production capacity analysis and optimization planning to boost throughput and efficiency while maintaining quality.

Personas: Plant Manager; Production Engineer; Operations Director.
Featured tools: Dynamics 365 ERP, PowerBI, Azure IoT Hub.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a record by NATURAL reference: a name or a
REC- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "REC-10020",
                "subject": "Woodgrove Bank",
                "status": "open",
                "owner": "Plant Manager",
                "metric": 31.0,
                "note": "Record for Woodgrove Bank"
        },
        {
                "reference": "REC-10021",
                "subject": "Wingtip Toys",
                "status": "in progress",
                "owner": "Production Engineer",
                "metric": 34.7,
                "note": "Record for Wingtip Toys"
        },
        {
                "reference": "REC-10022",
                "subject": "Tailwind Traders",
                "status": "resolved",
                "owner": "Operations Director",
                "metric": 38.4,
                "note": "Record for Tailwind Traders"
        },
        {
                "reference": "REC-10023",
                "subject": "Proseware",
                "status": "escalated",
                "owner": "Plant Manager",
                "metric": 42.1,
                "note": "Record for Proseware"
        },
        {
                "reference": "REC-10024",
                "subject": "Litware",
                "status": "closed",
                "owner": "Production Engineer",
                "metric": 45.8,
                "note": "Record for Litware"
        }
]


class ProductLineOptimizationAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's record records.",
        "Show REC-10020.",
        "What is the status of Wingtip Toys?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "ProductLineOptimizationAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Provide intelligent production capacity analysis and optimization planning to boost throughput and efficiency while maintaining quality. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a record by a name or a REC- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A record reference or a subject "
                                        "name, e.g. REC-10020 or 'Woodgrove Bank'. Pass 'list' to "
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
            lines = ["## Product Line Optimization Agent — record records (Dataverse)"]
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
