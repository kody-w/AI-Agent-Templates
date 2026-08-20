#!/usr/bin/env python3
"""Campaign Design Agent — portable skill. Automate personalized campaign design and execution to boost engagement, accelerate revenue, and strengthen customer loyalty.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "CX-10280",
                "subject": "Wingtip Toys",
                "status": "new",
                "owner": "Marketing Director",
                "metric": 95.5,
                "note": "Record for Wingtip Toys"
        },
        {
                "reference": "CX-10281",
                "subject": "Tailwind Traders",
                "status": "engaged",
                "owner": "Campaign Manager",
                "metric": 99.2,
                "note": "Record for Tailwind Traders"
        },
        {
                "reference": "CX-10282",
                "subject": "Proseware",
                "status": "converted",
                "owner": "Marketing Director",
                "metric": 14.9,
                "note": "Record for Proseware"
        },
        {
                "reference": "CX-10283",
                "subject": "Litware",
                "status": "lapsed",
                "owner": "Campaign Manager",
                "metric": 18.6,
                "note": "Record for Litware"
        },
        {
                "reference": "CX-10284",
                "subject": "Alpine Ski House",
                "status": "nurture",
                "owner": "Marketing Director",
                "metric": 22.3,
                "note": "Record for Alpine Ski House"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Campaign Design Agent — record records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No record matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Campaign Design Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="CX- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
