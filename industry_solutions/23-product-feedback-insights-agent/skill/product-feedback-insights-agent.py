#!/usr/bin/env python3
"""Product Feedback Insights Agent — portable skill. Turn fragmented feedback into actionable insights that accelerate product improvements, prevent churn, and optimize engineering priorities.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "CX-10460",
                "subject": "Adatum",
                "status": "new",
                "owner": "Product Manager",
                "metric": 86.0,
                "note": "Record for Adatum"
        },
        {
                "reference": "CX-10461",
                "subject": "Trey Research",
                "status": "engaged",
                "owner": "Engineering Lead",
                "metric": 89.7,
                "note": "Record for Trey Research"
        },
        {
                "reference": "CX-10462",
                "subject": "Woodgrove Bank",
                "status": "converted",
                "owner": "Director of Product",
                "metric": 93.4,
                "note": "Record for Woodgrove Bank"
        },
        {
                "reference": "CX-10463",
                "subject": "Wingtip Toys",
                "status": "lapsed",
                "owner": "Product Manager",
                "metric": 97.1,
                "note": "Record for Wingtip Toys"
        },
        {
                "reference": "CX-10464",
                "subject": "Tailwind Traders",
                "status": "nurture",
                "owner": "Engineering Lead",
                "metric": 12.8,
                "note": "Record for Tailwind Traders"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Product Feedback Insights Agent — record records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No record matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Product Feedback Insights Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="CX- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
