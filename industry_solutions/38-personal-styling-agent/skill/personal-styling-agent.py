#!/usr/bin/env python3
"""Personal Styling Agent — portable skill. Deliver intelligent personal styling to strengthen customer experience, increase revenue, and elevate associate efficiency at scale.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "CX-10760",
                "subject": "Fourth Coffee",
                "status": "new",
                "owner": "Personal Shoppers",
                "metric": 99.5,
                "note": "Record for Fourth Coffee"
        },
        {
                "reference": "CX-10761",
                "subject": "Graphic Design Institute",
                "status": "engaged",
                "owner": "Clienteling Specialists",
                "metric": 15.2,
                "note": "Record for Graphic Design Institute"
        },
        {
                "reference": "CX-10762",
                "subject": "Contoso",
                "status": "converted",
                "owner": "Retail Managers",
                "metric": 18.9,
                "note": "Record for Contoso"
        },
        {
                "reference": "CX-10763",
                "subject": "Northwind Traders",
                "status": "lapsed",
                "owner": "Personal Shoppers",
                "metric": 22.6,
                "note": "Record for Northwind Traders"
        },
        {
                "reference": "CX-10764",
                "subject": "Fabrikam",
                "status": "nurture",
                "owner": "Clienteling Specialists",
                "metric": 26.3,
                "note": "Record for Fabrikam"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Personal Styling Agent — record records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No record matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Personal Styling Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="CX- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
