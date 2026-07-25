#!/usr/bin/env python3
"""Utility Leak Detection & Billing Agent — portable skill. Automate leak detection and billing processes to improve customer satisfaction, ensure policy compliance, and protect municipal revenue.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "INV-10480",
                "subject": "Proseware",
                "status": "draft",
                "owner": "Customer Service Rep",
                "metric": 16.5,
                "note": "Invoice for Proseware"
        },
        {
                "reference": "INV-10481",
                "subject": "Litware",
                "status": "issued",
                "owner": "Billing Specialist",
                "metric": 20.2,
                "note": "Invoice for Litware"
        },
        {
                "reference": "INV-10482",
                "subject": "Alpine Ski House",
                "status": "paid",
                "owner": "Assistance Coordinator",
                "metric": 23.9,
                "note": "Invoice for Alpine Ski House"
        },
        {
                "reference": "INV-10483",
                "subject": "Lucerne Publishing",
                "status": "overdue",
                "owner": "Customer Service Rep",
                "metric": 27.6,
                "note": "Invoice for Lucerne Publishing"
        },
        {
                "reference": "INV-10484",
                "subject": "Coho Vineyard",
                "status": "disputed",
                "owner": "Billing Specialist",
                "metric": 31.3,
                "note": "Invoice for Coho Vineyard"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Utility Leak Detection & Billing Agent — invoice records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No invoice matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Utility Leak Detection & Billing Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="INV- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
