"""Denial Triage & Appeal Drafting / Peer-to-Peer Scheduling — steps 5-6 of the
Prior Authorization & Utilization Management process flow.

Step 5 — Denial Triage & Appeal Drafting: adverse determinations are triaged
by denial reason. Azure OpenAI drafts the appeal letter citing the payer's own
criteria and the member's clinical facts for UM nurse review. (Azure OpenAI,
Copilot Studio)

Step 6 — Peer-to-Peer Scheduling: when a physician review is required, Copilot
Studio negotiates a peer-to-peer slot between the ordering physician and the
payer medical director via calendar integration. (Copilot Studio,
Outlook / Graph)

Logic is REAL: a denied request gets a drafted appeal with the overturn
argument; a pended request needing physician review gets a proposed
peer-to-peer slot. Identify requests by NATURAL reference (patient name or
AUTH- ref). Data home: Microsoft Dataverse.
"""
try:
    from agents.basic_agent import BasicAgent
except ImportError:
    class BasicAgent:
        def __init__(self, name, metadata):
            self.name, self.metadata = name, metadata

_CANON = [
    {"authReference": "AUTH-88377", "patientName": "Marcus Bell",
     "service": "Proton beam therapy (CPT 77523)", "payer": "Fabrikam Insurance",
     "track": "denial",
     "denialReason": "Not medically necessary — equivalent-outcome conformal "
                     "radiotherapy considered available",
     "appeal": "Cite Fabrikam oncology policy §4.2 (proton indicated for "
               "re-irradiation near critical structures); attach dosimetry "
               "showing conformal RT exceeds cord tolerance",
     "peerToPeer": "n/a"},
    {"authReference": "AUTH-88350", "patientName": "Sam Okafor",
     "service": "Lumbar spinal fusion (CPT 22633)", "payer": "Woodgrove Health",
     "track": "peer-to-peer",
     "denialReason": "n/a (pended for physician review)",
     "appeal": "n/a",
     "peerToPeer": "Proposed: Thu 14:30-15:00 between Dr. Reyes (ordering) and "
                   "the Woodgrove medical director; documented instability + "
                   "failed 10-week PT to be presented"},
    {"authReference": "AUTH-88394", "patientName": "Priya Nair",
     "service": "Total knee arthroplasty (CPT 27447)", "payer": "Northwind Health",
     "track": "approved",
     "denialReason": "n/a", "appeal": "n/a", "peerToPeer": "n/a"},
]


class DenialAppealPeer(BasicAgent):
    CAPIR = {"binding": {"system": "Microsoft Dataverse", "table": "accounts"}}
    TRIGGERS = [
        "Draft an appeal for the denied proton therapy request AUTH-88377.",
        "Schedule a peer-to-peer for Sam Okafor's spinal fusion.",
        "Why was Marcus Bell's authorization denied?",
    ]
    RESPONSE = ("Present records as plain text fields. NEVER invent, guess, or "
                "fabricate URLs, deep links, or Power Apps/Power BI links — the "
                "packaged demo data contains no links. Refer to records by their "
                "plain reference (e.g. AUTH-88377) only. Keep answers under ~130 "
                "words, professional markdown, no emojis.")
    SYNTHETIC_DATA = list(_CANON)

    def __init__(self):
        self.name = "DenialAppealPeer"
        self.metadata = {
            "name": self.name,
            "description": (
                "Triages adverse determinations by denial reason and drafts the "
                "appeal letter citing the payer's own criteria and the member's "
                "clinical facts, and — when a physician review is required — "
                "proposes a peer-to-peer slot between the ordering physician and "
                "the payer medical director. Requests live in Microsoft "
                "Dataverse. Identify a request by NATURAL reference: a patient "
                "name or AUTH- reference; never ask the user for an internal id."),
            "parameters": {
                "type": "object",
                "properties": {
                    "authReference": {
                        "type": "string",
                        "description": ("Auth reference or patient name, e.g. "
                                        "AUTH-88377 or 'Marcus Bell'. Pass the "
                                        "word: list to see requests needing "
                                        "appeal or peer-to-peer — never ask the "
                                        "user for an id.")},
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
        ref = str(kwargs.get("authReference") or "").strip()
        if not ref or ref.lower() == "list":
            work = [a for a in _CANON if a["track"] in ("denial", "peer-to-peer")]
            lines = ["## Requests needing appeal or peer-to-peer (Dataverse)"]
            lines += [f"{i}. **{a['authReference']}** — {a['patientName']}, "
                      f"{a['service']} — {a['track']}"
                      for i, a in enumerate(work, 1)]
            return "\n".join(lines)
        hits = self._find(ref)
        if not hits:
            return (f"No request matches `{ref}`. Say 'list' for requests "
                    "needing appeal or peer-to-peer.")
        a = hits[0]
        if a["track"] == "approved":
            return (f"## {a['authReference']} — {a['patientName']}\n"
                    "Approved on review — no appeal or peer-to-peer needed.")
        if a["track"] == "denial":
            return "\n".join([
                f"## {a['authReference']} — {a['patientName']}",
                f"- Service: {a['service']} | Payer: {a['payer']}",
                "",
                "### Step 5 — Denial triage & appeal draft",
                f"- Denial reason: {a['denialReason']}.",
                f"- **Drafted appeal:** {a['appeal']}.",
                "- Ready for UM nurse review before submission.",
            ])
        return "\n".join([
            f"## {a['authReference']} — {a['patientName']}",
            f"- Service: {a['service']} | Payer: {a['payer']}",
            "",
            "### Step 6 — Peer-to-peer scheduling",
            f"- {a['peerToPeer']}.",
            "- Invite ready to send on nurse confirmation.",
        ])
