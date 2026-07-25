#!/usr/bin/env python3
"""Claims Processing Agent — portable skill. Automate claims processing workflows to deliver faster, consistent, and more compliant claim outcomes.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "CLM-10720",
                "subject": "Trey Research",
                "status": "received",
                "owner": "Claims Adjusters / Managers",
                "metric": 62.5,
                "note": "Claim for Trey Research"
        },
        {
                "reference": "CLM-10721",
                "subject": "Woodgrove Bank",
                "status": "in adjudication",
                "owner": "SIU Teams",
                "metric": 66.2,
                "note": "Claim for Woodgrove Bank"
        },
        {
                "reference": "CLM-10722",
                "subject": "Wingtip Toys",
                "status": "approved",
                "owner": "Operations Leaders",
                "metric": 69.9,
                "note": "Claim for Wingtip Toys"
        },
        {
                "reference": "CLM-10723",
                "subject": "Tailwind Traders",
                "status": "denied",
                "owner": "Claims Adjusters / Managers",
                "metric": 73.6,
                "note": "Claim for Tailwind Traders"
        },
        {
                "reference": "CLM-10724",
                "subject": "Proseware",
                "status": "paid",
                "owner": "SIU Teams",
                "metric": 77.3,
                "note": "Claim for Proseware"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Claims Processing Agent — claim records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No claim matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Claims Processing Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="CLM- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
