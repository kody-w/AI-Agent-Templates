"""Contract Review Agent — Professional Services, Consulting industry solution (AIBAST).

Automate contract review processes to enable faster, lower-risk, and more successful negotiations.

Personas: Legal Operations; Attorneys; Executives.
Featured tools: SharePoint, Microsoft Word.

Synthetic demo data only — no PII (Microsoft fictional companies). Records live
in Microsoft Dataverse. Identify a item by NATURAL reference: a name or a
REG- id; never ask the user for an internal id — pass 'list' to see all.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:  # portable / standalone
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
        {
                "reference": "REG-10040",
                "subject": "Alpine Ski House",
                "status": "open",
                "owner": "Legal Operations",
                "metric": 49.5,
                "note": "Item for Alpine Ski House"
        },
        {
                "reference": "REG-10041",
                "subject": "Lucerne Publishing",
                "status": "in review",
                "owner": "Attorneys",
                "metric": 53.2,
                "note": "Item for Lucerne Publishing"
        },
        {
                "reference": "REG-10042",
                "subject": "Coho Vineyard",
                "status": "cleared",
                "owner": "Executives",
                "metric": 56.9,
                "note": "Item for Coho Vineyard"
        },
        {
                "reference": "REG-10043",
                "subject": "Margie's Travel",
                "status": "flagged",
                "owner": "Legal Operations",
                "metric": 60.6,
                "note": "Item for Margie's Travel"
        },
        {
                "reference": "REG-10044",
                "subject": "Fourth Coffee",
                "status": "remediated",
                "owner": "Attorneys",
                "metric": 64.3,
                "note": "Item for Fourth Coffee"
        }
]


class ContractReviewAgent(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "List today's item records.",
        "Show REG-10040.",
        "What is the status of Lucerne Publishing?"
]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference only. Keep answers under ~120 words, "
                "professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "ContractReviewAgent"
        self.metadata = {
            "name": self.name,
            "description": (
                "Automate contract review processes to enable faster, lower-risk, and more successful negotiations. Records live in Microsoft Dataverse (synthetic, no "
                "PII). Identify a item by a name or a REG- "
                "reference; pass 'list' to see all — never ask for an id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": ("A item reference or a subject "
                                        "name, e.g. REG-10040 or 'Alpine Ski House'. Pass 'list' to "
                                        "see every item.")},
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
            lines = ["## Contract Review Agent — item records (Dataverse)"]
            lines += ["%d. **%s** — %s | status: %s | owner: %s"
                      % (n, r["reference"], r["subject"], r["status"], r["owner"])
                      for n, r in enumerate(_CANON, 1)]
            lines.append("")
            lines.append("Name a item for its detail.")
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return "No item matches `%s`. Say 'list' to see all." % ref
        r = hits[0]
        return "\n".join([
            "## %s — %s" % (r["reference"], r["subject"]),
            "- Status: **%s**" % r["status"],
            "- Owner: %s" % r["owner"],
            "- Key metric: %s" % r["metric"],
            "- %s" % r["note"],
        ])
