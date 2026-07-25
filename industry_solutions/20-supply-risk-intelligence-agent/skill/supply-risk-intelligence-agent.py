#!/usr/bin/env python3
"""Supply Risk Intelligence Agent — portable skill. Deliver real-time risk intelligence and planning to protect production continuity and reduce disruption exposure.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
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


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Supply Risk Intelligence Agent — work order records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No work order matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Supply Risk Intelligence Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="WO- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
