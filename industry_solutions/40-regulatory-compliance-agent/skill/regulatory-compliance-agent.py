#!/usr/bin/env python3
"""Regulatory Compliance Agent — portable skill. Automate compliance monitoring and regulatory reporting to achieve proactive risk management with real-time surveillance.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "REG-10800",
                "subject": "Proseware",
                "status": "open",
                "owner": "Chief Compliance Officers",
                "metric": 48.5,
                "note": "Item for Proseware"
        },
        {
                "reference": "REG-10801",
                "subject": "Litware",
                "status": "in review",
                "owner": "Compliance Managers",
                "metric": 52.2,
                "note": "Item for Litware"
        },
        {
                "reference": "REG-10802",
                "subject": "Alpine Ski House",
                "status": "cleared",
                "owner": "Trading Desk Supervisors",
                "metric": 55.9,
                "note": "Item for Alpine Ski House"
        },
        {
                "reference": "REG-10803",
                "subject": "Lucerne Publishing",
                "status": "flagged",
                "owner": "Chief Compliance Officers",
                "metric": 59.6,
                "note": "Item for Lucerne Publishing"
        },
        {
                "reference": "REG-10804",
                "subject": "Coho Vineyard",
                "status": "remediated",
                "owner": "Compliance Managers",
                "metric": 63.3,
                "note": "Item for Coho Vineyard"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Regulatory Compliance Agent — item records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No item matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Regulatory Compliance Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="REG- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
