"""Prior Authorization Agent — Healthcare, Financial Services industry solution (AIBAST).

Automate insurance approval workflows to accelerate authorization processes, improve documentation accuracy, and reduce care delays.

Personas: Utilization Management Coordinators; Nurse Case Managers; Radiology Schedulers.
Featured tools: Microsoft Teams.

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
                "reference": "PT-10900",
                "subject": "Northwind Traders",
                "status": "registered",
                "owner": "Utilization Management Coordinators",
                "metric": 53.0,
                "note": "Record for Northwind Traders"
        },
        {
                "reference": "PT-10901",
                "subject": "Fabrikam",
                "status": "triaged",
                "owner": "Nurse Case Managers",
                "metric": 56.7,
                "note": "Record for Fabrikam"
        },
        {
                "reference": "PT-10902",
                "subject": "Adatum",
                "status": "in care",
                "owner": "Radiology Schedulers",
                "metric": 60.4,
                "note": "Record for Adatum"
        },
        {
                "reference": "PT-10903",
                "subject": "Trey Research",
                "status": "discharged",
                "owner": "Utilization Management Coordinators",
                "metric": 64.1,
                "note": "Record for Trey Research"
        },
        {
                "reference": "PT-10904",
                "subject": "Woodgrove Bank",
                "status": "pending auth",
                "owner": "Nurse Case Managers",
                "metric": 67.8,
                "note": "Record for Woodgrove Bank"
        }
]


class PriorAuthorizationAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's record records.",
        "Show PT-10900.",
        "What is the status of Fabrikam?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "PriorAuthorizationAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate insurance approval workflows to accelerate authorization processes, improve documentation accuracy, and reduce care delays. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a record by a name or a PT- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A record reference or a subject "
                                        "name, e.g. PT-10900 or 'Northwind Traders'. Pass 'list' to "
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
            lines = ["## Prior Authorization Agent — record records (Dataverse)"]
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
