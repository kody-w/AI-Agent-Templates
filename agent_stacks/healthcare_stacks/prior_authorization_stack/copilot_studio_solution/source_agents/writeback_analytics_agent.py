"""Decision Write-Back & UM Analytics — steps 7-8 of the Prior Authorization &
Utilization Management process flow.

Step 7 — Decision Write-Back: approvals, auth numbers, validity windows, and
unit limits are written back to the EHR and scheduling system so care can be
booked immediately within the authorized scope. (EHR System, Power Automate)

Step 8 — UM Analytics: Power BI tracks turnaround by payer and service line,
denial and overturn rates, SLA breaches, and gold-carding eligibility for
governance review. (Power BI)

Write-back is REAL: an approved request carries an auth number, a validity
window, and unit limits. Analytics are computed deterministically from the
canon. Identify requests by NATURAL reference (patient name or AUTH- ref).
Data home: Microsoft Dataverse.
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
     "determination": "approved", "authNumber": "CON-4471902",
     "validFrom": "2026-07-24", "validTo": "2026-09-22", "units": "1 study",
     "tatHours": 0},
    {"authReference": "AUTH-88394", "patientName": "Priya Nair",
     "service": "Total knee arthroplasty", "payer": "Northwind Health",
     "determination": "approved", "authNumber": "NWH-880713",
     "validFrom": "2026-07-24", "validTo": "2026-10-22", "units": "1 procedure",
     "tatHours": 62},
    {"authReference": "AUTH-88377", "patientName": "Marcus Bell",
     "service": "Proton beam therapy", "payer": "Fabrikam Insurance",
     "determination": "denied (appeal in progress)", "authNumber": "n/a",
     "validFrom": "n/a", "validTo": "n/a", "units": "n/a", "tatHours": 312},
    {"authReference": "AUTH-88365", "patientName": "Elena Fischer",
     "service": "CT abdomen & pelvis", "payer": "Adatum Health",
     "determination": "approved", "authNumber": "ADA-551244",
     "validFrom": "2026-07-24", "validTo": "2026-08-07", "units": "1 study",
     "tatHours": 41},
    {"authReference": "AUTH-88350", "patientName": "Sam Okafor",
     "service": "Lumbar spinal fusion", "payer": "Woodgrove Health",
     "determination": "pended (peer-to-peer)", "authNumber": "n/a",
     "validFrom": "n/a", "validTo": "n/a", "units": "n/a", "tatHours": 320},
]


class WritebackAnalytics(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "Write back the approval for AUTH-88394 to the EHR.",
        "What's the auth number and validity window for Priya Nair's knee replacement?",
        "Show the UM analytics: approval rate and average turnaround by payer.",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference (e.g. AUTH-88394) only. Keep answers under ~130 "
                "words, professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "WritebackAnalytics"
        self.metadata = {
            "name": self.name,
            "description": (
                "Writes approved determinations back to the EHR and scheduling "
                "system — auth number, validity window, and unit limits so care "
                "books within the authorized scope — and reports UM analytics: "
                "approval and overturn rates, average turnaround by payer and "
                "service line, and SLA performance. Requests live in Microsoft "
                "Dataverse. Identify a request by NATURAL reference: a patient "
                "name or AUTH- reference; pass 'analytics' for the governance "
                "scoreboard. Never ask the user for an internal id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "authReference": {
                        "type": "string",
                        "description": ("Auth reference or patient name, e.g. "
                                        "AUTH-88394 or 'Priya Nair'. Pass the "
                                        "word: analytics for the UM scoreboard, "
                                        "or list for all determinations — never "
                                        "ask the user for an id.")},
                },
                "required": [],
            },
        }
        super().__init__(self.name, self.metadata)

    def _find(self, ref):
        low = ref.lower()
        return [a for a in _CANON if low == a["authReference"].lower()
                or low in a["patientName"].lower()]

    def perform(self, **kwargs):
        ref = str(kwargs.get("authReference") or "").strip().lower()
        if ref in ("analytics", "scoreboard", "metrics", "governance"):
            approved = [a for a in _CANON if a["determination"] == "approved"]
            decided = [a for a in _CANON if a["tatHours"] > 0]
            avg_tat = sum(a["tatHours"] for a in decided) / max(len(decided), 1)
            return "\n".join([
                "## UM analytics — governance scoreboard (Power BI)",
                f"- Requests: {len(_CANON)} | Approved: {len(approved)} "
                f"({100*len(approved)//len(_CANON)}%)",
                f"- Denied: 1 (appeal in progress) | Pended: 1 (peer-to-peer)",
                f"- Avg turnaround (decided): {avg_tat:.0f}h",
                "- Gold-carding: 1 order auto-exempt (Contoso / CPT 72148)",
                "- SLA: expedited case (AUTH-88365) cleared within 72h.",
            ])
        if not ref or ref == "list":
            lines = ["## Determinations — write-back status (Dataverse)"]
            lines += [f"{i}. **{a['authReference']}** — {a['patientName']}, "
                      f"{a['service']} — {a['determination']}"
                      + (f" (auth {a['authNumber']})"
                         if a["authNumber"] != "n/a" else "")
                      for i, a in enumerate(_CANON, 1)]
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return (f"No request matches `{ref}`. Say 'analytics' for the UM "
                    "scoreboard or 'list' for all determinations.")
        a = hits[0]
        lines = [
            f"## {a['authReference']} — {a['patientName']}",
            f"- Service: {a['service']} | Payer: {a['payer']} | "
            f"Determination: **{a['determination']}**",
        ]
        if a["authNumber"] != "n/a":
            lines += [
                "",
                "### Step 7 — Decision write-back (EHR + scheduling)",
                f"- Auth number: {a['authNumber']} | Units: {a['units']}",
                f"- Valid: {a['validFrom']} → {a['validTo']}",
                "- Written back; care can be booked within the authorized scope.",
            ]
        else:
            lines.append("- Not yet approved — nothing to write back "
                         "(see denial/peer-to-peer agent).")
        return "\n".join(lines)
