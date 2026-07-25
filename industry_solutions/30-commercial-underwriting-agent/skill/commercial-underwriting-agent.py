#!/usr/bin/env python3
"""Commercial Underwriting Agent — portable skill. Automate commercial underwriting analysis to accelerate evaluations, improve pricing accuracy, and maintain full compliance.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "APP-10600",
                "subject": "Wingtip Toys",
                "status": "submitted",
                "owner": "Underwriter",
                "metric": 39.5,
                "note": "Application for Wingtip Toys"
        },
        {
                "reference": "APP-10601",
                "subject": "Tailwind Traders",
                "status": "in review",
                "owner": "Risk Analyst",
                "metric": 43.2,
                "note": "Application for Tailwind Traders"
        },
        {
                "reference": "APP-10602",
                "subject": "Proseware",
                "status": "approved",
                "owner": "Underwriter",
                "metric": 46.9,
                "note": "Application for Proseware"
        },
        {
                "reference": "APP-10603",
                "subject": "Litware",
                "status": "referred",
                "owner": "Risk Analyst",
                "metric": 50.6,
                "note": "Application for Litware"
        },
        {
                "reference": "APP-10604",
                "subject": "Alpine Ski House",
                "status": "declined",
                "owner": "Underwriter",
                "metric": 54.3,
                "note": "Application for Alpine Ski House"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Commercial Underwriting Agent — application records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No application matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Commercial Underwriting Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="APP- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
