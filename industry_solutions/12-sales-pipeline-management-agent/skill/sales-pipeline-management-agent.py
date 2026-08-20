#!/usr/bin/env python3
"""Sales Pipeline Management Agent — portable skill. Automate sales pipeline management to keep deals moving, increase forecast confidence, and improve team productivity.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "OPP-10240",
                "subject": "Coho Vineyard",
                "status": "qualifying",
                "owner": "Account Executive",
                "metric": 58.5,
                "note": "Opportunity for Coho Vineyard"
        },
        {
                "reference": "OPP-10241",
                "subject": "Margie's Travel",
                "status": "proposal",
                "owner": "Sales Director",
                "metric": 62.2,
                "note": "Opportunity for Margie's Travel"
        },
        {
                "reference": "OPP-10242",
                "subject": "Fourth Coffee",
                "status": "negotiation",
                "owner": "Account Executive",
                "metric": 65.9,
                "note": "Opportunity for Fourth Coffee"
        },
        {
                "reference": "OPP-10243",
                "subject": "Graphic Design Institute",
                "status": "won",
                "owner": "Sales Director",
                "metric": 69.6,
                "note": "Opportunity for Graphic Design Institute"
        },
        {
                "reference": "OPP-10244",
                "subject": "Contoso",
                "status": "at risk",
                "owner": "Account Executive",
                "metric": 73.3,
                "note": "Opportunity for Contoso"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Sales Pipeline Management Agent — opportunity records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No opportunity matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Sales Pipeline Management Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="OPP- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
