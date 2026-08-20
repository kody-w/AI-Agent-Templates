#!/usr/bin/env python3
"""Loyalty Insights Agent — portable skill. Deliver AI-driven loyalty insights and planning to reduce points liability, improve engagement results, and boost member retention.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "CX-10860",
                "subject": "Tailwind Traders",
                "status": "new",
                "owner": "Loyalty Program Director",
                "metric": 16.0,
                "note": "Record for Tailwind Traders"
        },
        {
                "reference": "CX-10861",
                "subject": "Proseware",
                "status": "engaged",
                "owner": "CRM Manager",
                "metric": 19.7,
                "note": "Record for Proseware"
        },
        {
                "reference": "CX-10862",
                "subject": "Litware",
                "status": "converted",
                "owner": "Marketing Leader",
                "metric": 23.4,
                "note": "Record for Litware"
        },
        {
                "reference": "CX-10863",
                "subject": "Alpine Ski House",
                "status": "lapsed",
                "owner": "Loyalty Program Director",
                "metric": 27.1,
                "note": "Record for Alpine Ski House"
        },
        {
                "reference": "CX-10864",
                "subject": "Lucerne Publishing",
                "status": "nurture",
                "owner": "CRM Manager",
                "metric": 30.8,
                "note": "Record for Lucerne Publishing"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Loyalty Insights Agent — record records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No record matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Loyalty Insights Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="CX- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
