#!/usr/bin/env python3
"""Expansion Opportunity Agent — portable skill. Identify and prioritize expansion opportunities to drive revenue growth and strengthen customer relationships.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "OPP-10500",
                "subject": "Margie's Travel",
                "status": "qualifying",
                "owner": "Sales Leader",
                "metric": 35.0,
                "note": "Opportunity for Margie's Travel"
        },
        {
                "reference": "OPP-10501",
                "subject": "Fourth Coffee",
                "status": "proposal",
                "owner": "Sales Operations Manager",
                "metric": 38.7,
                "note": "Opportunity for Fourth Coffee"
        },
        {
                "reference": "OPP-10502",
                "subject": "Graphic Design Institute",
                "status": "negotiation",
                "owner": "Enablement Manager",
                "metric": 42.4,
                "note": "Opportunity for Graphic Design Institute"
        },
        {
                "reference": "OPP-10503",
                "subject": "Contoso",
                "status": "won",
                "owner": "Sales Leader",
                "metric": 46.1,
                "note": "Opportunity for Contoso"
        },
        {
                "reference": "OPP-10504",
                "subject": "Northwind Traders",
                "status": "at risk",
                "owner": "Sales Operations Manager",
                "metric": 49.8,
                "note": "Opportunity for Northwind Traders"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Expansion Opportunity Agent — opportunity records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No opportunity matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Expansion Opportunity Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="OPP- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
