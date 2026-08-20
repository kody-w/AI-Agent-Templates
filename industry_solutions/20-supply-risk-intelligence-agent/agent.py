"""Supply Risk Intelligence Agent — Manufacturing industry solution (AIBAST).

Deliver real-time risk intelligence and planning to protect production continuity and reduce disruption exposure.

Personas: Procurement Manager; Supply Chain Director.
Featured tools: Dynamics 365 ERP, Microsoft Teams.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a work order by NATURAL reference: a name or a
WO- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "WO-10400",
                "subject": "Trey Research",
                "status": "scheduled",
                "owner": "Procurement Manager",
                "metric": 30.5,
                "note": "Work order for Trey Research"
        },
        {
                "reference": "WO-10401",
                "subject": "Woodgrove Bank",
                "status": "in progress",
                "owner": "Supply Chain Director",
                "metric": 34.2,
                "note": "Work order for Woodgrove Bank"
        },
        {
                "reference": "WO-10402",
                "subject": "Wingtip Toys",
                "status": "completed",
                "owner": "Procurement Manager",
                "metric": 37.9,
                "note": "Work order for Wingtip Toys"
        },
        {
                "reference": "WO-10403",
                "subject": "Tailwind Traders",
                "status": "overdue",
                "owner": "Supply Chain Director",
                "metric": 41.6,
                "note": "Work order for Tailwind Traders"
        },
        {
                "reference": "WO-10404",
                "subject": "Proseware",
                "status": "flagged",
                "owner": "Procurement Manager",
                "metric": 45.3,
                "note": "Work order for Proseware"
        }
]


class SupplyRiskIntelligenceAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's work order records.",
        "Show WO-10400.",
        "What is the status of Woodgrove Bank?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "SupplyRiskIntelligenceAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Deliver real-time risk intelligence and planning to protect production continuity and reduce disruption exposure. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a work order by a name or a WO- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A work order reference or a subject "
                                        "name, e.g. WO-10400 or 'Trey Research'. Pass 'list' to "
                                        "see every work order.")},
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
            lines = ["## Supply Risk Intelligence Agent — work order records (Dataverse)"]
            lines += ["%d. **%s** — %s | status: %s | owner: %s"
                      % (n, r["reference"], r["subject"], r["status"], r["owner"])
                      for n, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a work order for its detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return "No work order matches `%s`. Say 'list' to see all." % ref
        r = hits[0]
        return "\n".join([
            "## %s — %s" % (r["reference"], r["subject"]),
            "- Status: **%s**" % r["status"],
            "- Owner: %s" % r["owner"],
            "- Key metric: %s" % r["metric"],
            "- %s" % r["note"],
        ])
