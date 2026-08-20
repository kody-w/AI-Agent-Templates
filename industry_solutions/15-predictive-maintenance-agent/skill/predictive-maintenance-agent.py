#!/usr/bin/env python3
"""Predictive Maintenance Agent — portable skill. Perform predictive maintenance analysis and scheduling orchestration to prevent unplanned downtime and protect production capacity.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "WO-10300",
                "subject": "Lucerne Publishing",
                "status": "scheduled",
                "owner": "Maintenance Manager",
                "metric": 26.0,
                "note": "Work order for Lucerne Publishing"
        },
        {
                "reference": "WO-10301",
                "subject": "Coho Vineyard",
                "status": "in progress",
                "owner": "Production Supervisor",
                "metric": 29.7,
                "note": "Work order for Coho Vineyard"
        },
        {
                "reference": "WO-10302",
                "subject": "Margie's Travel",
                "status": "completed",
                "owner": "Operation Leader",
                "metric": 33.4,
                "note": "Work order for Margie's Travel"
        },
        {
                "reference": "WO-10303",
                "subject": "Fourth Coffee",
                "status": "overdue",
                "owner": "Maintenance Manager",
                "metric": 37.1,
                "note": "Work order for Fourth Coffee"
        },
        {
                "reference": "WO-10304",
                "subject": "Graphic Design Institute",
                "status": "flagged",
                "owner": "Production Supervisor",
                "metric": 40.8,
                "note": "Work order for Graphic Design Institute"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Predictive Maintenance Agent — work order records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No work order matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Predictive Maintenance Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="WO- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
