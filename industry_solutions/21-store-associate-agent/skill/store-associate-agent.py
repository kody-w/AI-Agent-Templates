#!/usr/bin/env python3
"""Store Associate Agent — portable skill. Deliver real-time product intelligence and transaction support to deliver faster service and boost sales performance.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "REC-10420",
                "subject": "Litware",
                "status": "open",
                "owner": "Store Associate",
                "metric": 49.0,
                "note": "Record for Litware"
        },
        {
                "reference": "REC-10421",
                "subject": "Alpine Ski House",
                "status": "in progress",
                "owner": "Sales Manager",
                "metric": 52.7,
                "note": "Record for Alpine Ski House"
        },
        {
                "reference": "REC-10422",
                "subject": "Lucerne Publishing",
                "status": "resolved",
                "owner": "Floor Specialist",
                "metric": 56.4,
                "note": "Record for Lucerne Publishing"
        },
        {
                "reference": "REC-10423",
                "subject": "Coho Vineyard",
                "status": "escalated",
                "owner": "Store Associate",
                "metric": 60.1,
                "note": "Record for Coho Vineyard"
        },
        {
                "reference": "REC-10424",
                "subject": "Margie's Travel",
                "status": "closed",
                "owner": "Sales Manager",
                "metric": 63.8,
                "note": "Record for Margie's Travel"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Store Associate Agent — record records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No record matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Store Associate Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="REC- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
