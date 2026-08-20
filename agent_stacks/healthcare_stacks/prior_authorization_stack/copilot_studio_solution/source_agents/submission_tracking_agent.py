"""Payer Submission & Status Tracking / Pend Management — steps 3-4 of the
Prior Authorization & Utilization Management process flow.

Step 3 — Payer Submission: Power Automate submits the authorization request
through the payer portal or as an X12 278 transaction, attaching the assembled
evidence packet and flagging expedited requests. (Power Automate,
Payer Portal / X12 278)

Step 4 — Status Tracking & Pend Management: every open authorization is tracked
against its SLA clock. Pended requests trigger automated document chase;
approaching breaches escalate to the UM queue. (Power Automate, Power Apps)

SLA clocks are REAL: expedited = 72 hours, standard = 14 days. A request within
6 hours (expedited) or 2 days (standard) of breach is flagged ESCALATE.
Identify requests by NATURAL reference (patient name or AUTH- ref). Data home:
Microsoft Dataverse.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
    {"authReference": "AUTH-88401", "patientName": "Jordan Avery",
     "service": "MRI lumbar spine", "payer": "Contoso Health",
     "channel": "auto (gold-carded)", "slaType": "standard",
     "hoursOpen": 0, "hoursToSla": 336, "status": "approved at submission",
     "pend": "none"},
    {"authReference": "AUTH-88394", "patientName": "Priya Nair",
     "service": "Total knee arthroplasty", "payer": "Northwind Health",
     "channel": "Payer portal", "slaType": "standard",
     "hoursOpen": 60, "hoursToSla": 276, "status": "approved",
     "pend": "none"},
    {"authReference": "AUTH-88377", "patientName": "Marcus Bell",
     "service": "Proton beam therapy", "payer": "Fabrikam Insurance",
     "channel": "X12 278", "slaType": "standard",
     "hoursOpen": 300, "hoursToSla": 36, "status": "adverse determination",
     "pend": "none"},
    {"authReference": "AUTH-88365", "patientName": "Elena Fischer",
     "service": "CT abdomen & pelvis", "payer": "Adatum Health",
     "channel": "Payer portal (EXPEDITED)", "slaType": "expedited",
     "hoursOpen": 40, "hoursToSla": 32, "status": "approved",
     "pend": "none"},
    {"authReference": "AUTH-88350", "patientName": "Sam Okafor",
     "service": "Lumbar spinal fusion", "payer": "Woodgrove Health",
     "channel": "X12 278", "slaType": "standard",
     "hoursOpen": 320, "hoursToSla": 16, "status": "pended",
     "pend": "Awaiting conservative-care records — auto-chase sent to provider"},
]


class SubmissionTracking(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "What's the payer status of AUTH-88350?",
        "Track the SLA clock on Sam Okafor's spinal fusion request.",
        "Which prior-auth requests are close to an SLA breach?",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference (e.g. AUTH-88350) only. Keep answers under ~120 "
                "words, professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "SubmissionTracking"
        self.metadata = {
            "name": self.name,
            "description": (
                "Submits the authorization request to the payer (portal or X12 "
                "278 with the assembled evidence packet, flagging expedited "
                "cases) and tracks every open authorization against its SLA "
                "clock — expedited 72h, standard 14 days — chasing pended "
                "documents and escalating approaching breaches to the UM queue. "
                "Requests live in Microsoft Dataverse. Identify a request by "
                "NATURAL reference: a patient name or AUTH- reference; never ask "
                "the user for an internal id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "authReference": {
                        "type": "string",
                        "description": ("Auth reference or patient name, e.g. "
                                        "AUTH-88350 or 'Sam Okafor'. Pass the "
                                        "word: list for all open requests, or "
                                        "breaches for SLA-risk requests — never "
                                        "ask the user for an id.")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def _breach_risk(self, a):
        limit = 6 if a["slaType"] == "expedited" else 48
        return a["status"] in ("pended",) and a["hoursToSla"] <= limit

    def _find(self, ref):
        low = ref.lower()
        return [a for a in _CANON if low == a["authReference"].lower()
                or low in a["patientName"].lower()]

    def perform(self, **kwargs):
        ref = str(kwargs.get("authReference") or "").strip().lower()
        if ref in ("breach", "breaches", "sla", "escalate"):
            risk = [a for a in _CANON if self._breach_risk(a)]
            if not risk:
                return "No open requests are within their escalation window."
            lines = ["## SLA-risk prior-auth requests"]
            lines += [f"- **{a['authReference']}** ({a['patientName']}) — "
                      f"{a['hoursToSla']}h to {a['slaType']} SLA — {a['pend']}"
                      for a in risk]
            return "\n".join(lines)
        if not ref or ref == "list":
            lines = ["## Open prior-auth requests — SLA tracking (Dataverse)"]
            lines += [f"{i}. **{a['authReference']}** — {a['patientName']}, "
                      f"{a['service']} — {a['status']} "
                      f"({a['hoursToSla']}h to {a['slaType']} SLA)"
                      for i, a in enumerate(_CANON, 1)]
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return (f"No request matches `{ref}`. Say 'list' for open requests "
                    "or 'breaches' for SLA-risk ones.")
        a = hits[0]
        lines = [
            f"## {a['authReference']} — {a['patientName']}",
            f"- Service: {a['service']} | Payer: {a['payer']}",
            "",
            "### Step 3 — Payer submission",
            f"- Submitted via {a['channel']}; evidence packet attached.",
            "",
            "### Step 4 — Status & pend management",
            f"- Status: **{a['status']}** | SLA: {a['slaType']} "
            f"({a['hoursToSla']}h remaining of the "
            f"{'72h' if a['slaType'] == 'expedited' else '14-day'} clock).",
        ]
        if a["pend"] != "none":
            lines.append(f"- Pend: {a['pend']}.")
        if self._breach_risk(a):
            lines.append("- **ESCALATE** — within the breach window; routed to "
                         "the UM queue.")
        return "\n".join(lines)
