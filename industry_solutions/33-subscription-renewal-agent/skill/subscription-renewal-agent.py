#!/usr/bin/env python3
"""Subscription Renewal Agent — portable skill. Streamline subscription renewal management and expansion planning, turning risk into growth opportunities while increasing win probability.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "OPP-10660",
                "subject": "Woodgrove Bank",
                "status": "qualifying",
                "owner": "Account Executives",
                "metric": 95.0,
                "note": "Opportunity for Woodgrove Bank"
        },
        {
                "reference": "OPP-10661",
                "subject": "Wingtip Toys",
                "status": "proposal",
                "owner": "Customer Success Managers",
                "metric": 98.7,
                "note": "Opportunity for Wingtip Toys"
        },
        {
                "reference": "OPP-10662",
                "subject": "Tailwind Traders",
                "status": "negotiation",
                "owner": "Sales Leadership",
                "metric": 14.4,
                "note": "Opportunity for Tailwind Traders"
        },
        {
                "reference": "OPP-10663",
                "subject": "Proseware",
                "status": "won",
                "owner": "Account Executives",
                "metric": 18.1,
                "note": "Opportunity for Proseware"
        },
        {
                "reference": "OPP-10664",
                "subject": "Litware",
                "status": "at risk",
                "owner": "Customer Success Managers",
                "metric": 21.8,
                "note": "Opportunity for Litware"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Subscription Renewal Agent — opportunity records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No opportunity matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Subscription Renewal Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="OPP- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
