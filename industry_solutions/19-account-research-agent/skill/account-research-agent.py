#!/usr/bin/env python3
"""Account Research Agent — portable skill. Automate account research and strategy planning to help sellers prepare faster, win more, and elevate deal quality.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "OPP-10380",
                "subject": "Graphic Design Institute",
                "status": "qualifying",
                "owner": "Account Executive",
                "metric": 100.0,
                "note": "Opportunity for Graphic Design Institute"
        },
        {
                "reference": "OPP-10381",
                "subject": "Contoso",
                "status": "proposal",
                "owner": "Sales Director",
                "metric": 15.7,
                "note": "Opportunity for Contoso"
        },
        {
                "reference": "OPP-10382",
                "subject": "Northwind Traders",
                "status": "negotiation",
                "owner": "Customer Success Manager",
                "metric": 19.4,
                "note": "Opportunity for Northwind Traders"
        },
        {
                "reference": "OPP-10383",
                "subject": "Fabrikam",
                "status": "won",
                "owner": "Account Executive",
                "metric": 23.1,
                "note": "Opportunity for Fabrikam"
        },
        {
                "reference": "OPP-10384",
                "subject": "Adatum",
                "status": "at risk",
                "owner": "Sales Director",
                "metric": 26.8,
                "note": "Opportunity for Adatum"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Account Research Agent — opportunity records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No opportunity matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Account Research Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="OPP- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
