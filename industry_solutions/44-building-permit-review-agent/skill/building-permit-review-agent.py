#!/usr/bin/env python3
"""Building Permit Review Agent — portable skill. Automate building permit review processes to enable faster service, lower operational costs, and higher citizen satisfaction.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "PRM-10880",
                "subject": "Coho Vineyard",
                "status": "submitted",
                "owner": "Permit Technicians",
                "metric": 34.5,
                "note": "Permit for Coho Vineyard"
        },
        {
                "reference": "PRM-10881",
                "subject": "Margie's Travel",
                "status": "in review",
                "owner": "Plan Reviewers",
                "metric": 38.2,
                "note": "Permit for Margie's Travel"
        },
        {
                "reference": "PRM-10882",
                "subject": "Fourth Coffee",
                "status": "approved",
                "owner": "Inspectors",
                "metric": 41.9,
                "note": "Permit for Fourth Coffee"
        },
        {
                "reference": "PRM-10883",
                "subject": "Graphic Design Institute",
                "status": "needs revision",
                "owner": "Permit Technicians",
                "metric": 45.6,
                "note": "Permit for Graphic Design Institute"
        },
        {
                "reference": "PRM-10884",
                "subject": "Contoso",
                "status": "issued",
                "owner": "Plan Reviewers",
                "metric": 49.3,
                "note": "Permit for Contoso"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Building Permit Review Agent — permit records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No permit matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Building Permit Review Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="PRM- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
