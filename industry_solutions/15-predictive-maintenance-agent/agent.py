"""Predictive Maintenance Agent — Manufacturing industry solution (AIBAST).

Perform predictive maintenance analysis and scheduling orchestration to prevent unplanned downtime and protect production capacity.

Personas: Maintenance Manager; Production Supervisor; Operation Leader.
Featured tools: Dynamics 365 ERP, Dynamics 365 CcaaS, Microsoft Teams.

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
                "reference": "WO-10300",
                "subject": "Lucerne Publishing",
                "status": "scheduled",
                "owner": "Maintenance Manager",
                "metric": 26.0,
                "note": "Work order for Lucerne Publishing"
        },
        {
                "reference": "WO-10301",
                "subject": "Coho Vineyard",
                "status": "in progress",
                "owner": "Production Supervisor",
                "metric": 29.7,
                "note": "Work order for Coho Vineyard"
        },
        {
                "reference": "WO-10302",
                "subject": "Margie's Travel",
                "status": "completed",
                "owner": "Operation Leader",
                "metric": 33.4,
                "note": "Work order for Margie's Travel"
        },
        {
                "reference": "WO-10303",
                "subject": "Fourth Coffee",
                "status": "overdue",
                "owner": "Maintenance Manager",
                "metric": 37.1,
                "note": "Work order for Fourth Coffee"
        },
        {
                "reference": "WO-10304",
                "subject": "Graphic Design Institute",
                "status": "flagged",
                "owner": "Production Supervisor",
                "metric": 40.8,
                "note": "Work order for Graphic Design Institute"
        }
]


class PredictiveMaintenanceAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's work order records.",
        "Show WO-10300.",
        "What is the status of Coho Vineyard?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "PredictiveMaintenanceAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Perform predictive maintenance analysis and scheduling orchestration to prevent unplanned downtime and protect production capacity. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a work order by a name or a WO- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A work order reference or a subject "
                                        "name, e.g. WO-10300 or 'Lucerne Publishing'. Pass 'list' to "
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
            lines = ["## Predictive Maintenance Agent — work order records (Dataverse)"]
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
