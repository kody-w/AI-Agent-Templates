#!/usr/bin/env python3
"""Customer Sentiment & Churn Agent — portable skill. Deliver AI-powered sentiment intelligence that detects churn risk early and enables proactive retention strategies.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "CS-10680",
                "subject": "Alpine Ski House",
                "status": "open",
                "owner": "Relationship Managers",
                "metric": 25.5,
                "note": "Case for Alpine Ski House"
        },
        {
                "reference": "CS-10681",
                "subject": "Lucerne Publishing",
                "status": "in progress",
                "owner": "Retention Specialists",
                "metric": 29.2,
                "note": "Case for Lucerne Publishing"
        },
        {
                "reference": "CS-10682",
                "subject": "Coho Vineyard",
                "status": "resolved",
                "owner": "Customer Success Teams",
                "metric": 32.9,
                "note": "Case for Coho Vineyard"
        },
        {
                "reference": "CS-10683",
                "subject": "Margie's Travel",
                "status": "escalated",
                "owner": "Relationship Managers",
                "metric": 36.6,
                "note": "Case for Margie's Travel"
        },
        {
                "reference": "CS-10684",
                "subject": "Fourth Coffee",
                "status": "closed",
                "owner": "Retention Specialists",
                "metric": 40.3,
                "note": "Case for Fourth Coffee"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Customer Sentiment & Churn Agent — case records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No case matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Customer Sentiment & Churn Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="CS- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
