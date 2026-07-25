#!/usr/bin/env python3
"""Mortgage Origination Agent — portable skill. Streamline mortgage origination with intelligent automation, enabling faster, more accurate loan decisions.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "APP-10740",
                "subject": "Litware",
                "status": "submitted",
                "owner": "Loan Officers",
                "metric": 81.0,
                "note": "Application for Litware"
        },
        {
                "reference": "APP-10741",
                "subject": "Alpine Ski House",
                "status": "in review",
                "owner": "Processors",
                "metric": 84.7,
                "note": "Application for Alpine Ski House"
        },
        {
                "reference": "APP-10742",
                "subject": "Lucerne Publishing",
                "status": "approved",
                "owner": "Underwriters",
                "metric": 88.4,
                "note": "Application for Lucerne Publishing"
        },
        {
                "reference": "APP-10743",
                "subject": "Coho Vineyard",
                "status": "referred",
                "owner": "Loan Officers",
                "metric": 92.1,
                "note": "Application for Coho Vineyard"
        },
        {
                "reference": "APP-10744",
                "subject": "Margie's Travel",
                "status": "declined",
                "owner": "Processors",
                "metric": 95.8,
                "note": "Application for Margie's Travel"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Mortgage Origination Agent — application records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No application matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Mortgage Origination Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="APP- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
