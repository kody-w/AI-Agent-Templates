#!/usr/bin/env python3
"""Supply Chain Risk Agent — portable skill. Detect and manage supply chain risks to defend against disruptions, protect revenue, and maintain operational continuity.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "WO-10640",
                "subject": "Contoso",
                "status": "scheduled",
                "owner": "Supply Chain Planner",
                "metric": 76.5,
                "note": "Work order for Contoso"
        },
        {
                "reference": "WO-10641",
                "subject": "Northwind Traders",
                "status": "in progress",
                "owner": "Operations Leader",
                "metric": 80.2,
                "note": "Work order for Northwind Traders"
        },
        {
                "reference": "WO-10642",
                "subject": "Fabrikam",
                "status": "completed",
                "owner": "Procurement Manager",
                "metric": 83.9,
                "note": "Work order for Fabrikam"
        },
        {
                "reference": "WO-10643",
                "subject": "Adatum",
                "status": "overdue",
                "owner": "Supply Chain Planner",
                "metric": 87.6,
                "note": "Work order for Adatum"
        },
        {
                "reference": "WO-10644",
                "subject": "Trey Research",
                "status": "flagged",
                "owner": "Operations Leader",
                "metric": 91.3,
                "note": "Work order for Trey Research"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Supply Chain Risk Agent — work order records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No work order matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Supply Chain Risk Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="WO- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
