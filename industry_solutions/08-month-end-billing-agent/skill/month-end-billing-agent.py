#!/usr/bin/env python3
"""Month-End Billing Agent — portable skill. Automate month-end billing cycles to accelerate invoicing, reduce risk, and ensure audit-ready compliance.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "INV-10160",
                "subject": "Proseware",
                "status": "draft",
                "owner": "Finance VP",
                "metric": 72.5,
                "note": "Invoice for Proseware"
        },
        {
                "reference": "INV-10161",
                "subject": "Litware",
                "status": "issued",
                "owner": "Billing Manager",
                "metric": 76.2,
                "note": "Invoice for Litware"
        },
        {
                "reference": "INV-10162",
                "subject": "Alpine Ski House",
                "status": "paid",
                "owner": "Finance VP",
                "metric": 79.9,
                "note": "Invoice for Alpine Ski House"
        },
        {
                "reference": "INV-10163",
                "subject": "Lucerne Publishing",
                "status": "overdue",
                "owner": "Billing Manager",
                "metric": 83.6,
                "note": "Invoice for Lucerne Publishing"
        },
        {
                "reference": "INV-10164",
                "subject": "Coho Vineyard",
                "status": "disputed",
                "owner": "Finance VP",
                "metric": 87.3,
                "note": "Invoice for Coho Vineyard"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Month-End Billing Agent — invoice records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No invoice matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Month-End Billing Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="INV- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
