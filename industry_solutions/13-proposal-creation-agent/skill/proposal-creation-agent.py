#!/usr/bin/env python3
"""Proposal Creation Agent — portable skill. Automate proposal creation to accelerate deal cycles, improve win rates, and deliver consistent, high-quality responses.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "OPP-10260",
                "subject": "Northwind Traders",
                "status": "qualifying",
                "owner": "Account Executive",
                "metric": 77.0,
                "note": "Opportunity for Northwind Traders"
        },
        {
                "reference": "OPP-10261",
                "subject": "Fabrikam",
                "status": "proposal",
                "owner": "Sales Leader",
                "metric": 80.7,
                "note": "Opportunity for Fabrikam"
        },
        {
                "reference": "OPP-10262",
                "subject": "Adatum",
                "status": "negotiation",
                "owner": "Bid Manager",
                "metric": 84.4,
                "note": "Opportunity for Adatum"
        },
        {
                "reference": "OPP-10263",
                "subject": "Trey Research",
                "status": "won",
                "owner": "Account Executive",
                "metric": 88.1,
                "note": "Opportunity for Trey Research"
        },
        {
                "reference": "OPP-10264",
                "subject": "Woodgrove Bank",
                "status": "at risk",
                "owner": "Sales Leader",
                "metric": 91.8,
                "note": "Opportunity for Woodgrove Bank"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Proposal Creation Agent — opportunity records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No opportunity matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Proposal Creation Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="OPP- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
