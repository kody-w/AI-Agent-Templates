"""Clinical Summary Agent — Healthcare industry solution (AIBAST).

Transform complex clinical histories into clear, actionable summaries for faster decision-making, better coordination, and safer care.

Personas: Primary care physicians; Surgeons; Anesthesia teams.
Featured tools: Dynamics 365 ERP.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a record by NATURAL reference: a name or a
PT- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "PT-10940",
                "subject": "Lucerne Publishing",
                "status": "registered",
                "owner": "Primary care physicians",
                "metric": 90.0,
                "note": "Record for Lucerne Publishing"
        },
        {
                "reference": "PT-10941",
                "subject": "Coho Vineyard",
                "status": "triaged",
                "owner": "Surgeons",
                "metric": 93.7,
                "note": "Record for Coho Vineyard"
        },
        {
                "reference": "PT-10942",
                "subject": "Margie's Travel",
                "status": "in care",
                "owner": "Anesthesia teams",
                "metric": 97.4,
                "note": "Record for Margie's Travel"
        },
        {
                "reference": "PT-10943",
                "subject": "Fourth Coffee",
                "status": "discharged",
                "owner": "Primary care physicians",
                "metric": 13.1,
                "note": "Record for Fourth Coffee"
        },
        {
                "reference": "PT-10944",
                "subject": "Graphic Design Institute",
                "status": "pending auth",
                "owner": "Surgeons",
                "metric": 16.8,
                "note": "Record for Graphic Design Institute"
        }
]


class ClinicalSummaryAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's record records.",
        "Show PT-10940.",
        "What is the status of Coho Vineyard?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "ClinicalSummaryAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Transform complex clinical histories into clear, actionable summaries for faster decision-making, better coordination, and safer care. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a record by a name or a PT- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A record reference or a subject "
                                        "name, e.g. PT-10940 or 'Lucerne Publishing'. Pass 'list' to "
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
            lines = ["## Clinical Summary Agent — record records (Dataverse)"]
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
