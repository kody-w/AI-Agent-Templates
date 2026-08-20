#!/usr/bin/env python3
"""Energy Operations Agent (d) — portable skill. Deliver real-time insights, automate critical workflows, and enable guided decision making—boosting efficiency while reducing operational and compliance risk for energy organizations.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "SITE-10360",
                "subject": "Alpine Ski House",
                "status": "nominal",
                "owner": "Plant Manager / Reliability Engineer",
                "metric": 81.5,
                "note": "Site for Alpine Ski House"
        },
        {
                "reference": "SITE-10361",
                "subject": "Lucerne Publishing",
                "status": "watch",
                "owner": "Compliance Manager",
                "metric": 85.2,
                "note": "Site for Lucerne Publishing"
        },
        {
                "reference": "SITE-10362",
                "subject": "Coho Vineyard",
                "status": "alert",
                "owner": "Sustainability Lead",
                "metric": 88.9,
                "note": "Site for Coho Vineyard"
        },
        {
                "reference": "SITE-10363",
                "subject": "Margie's Travel",
                "status": "maintenance",
                "owner": "Data Analyst",
                "metric": 92.6,
                "note": "Site for Margie's Travel"
        },
        {
                "reference": "SITE-10364",
                "subject": "Fourth Coffee",
                "status": "resolved",
                "owner": "Plant Manager / Reliability Engineer",
                "metric": 96.3,
                "note": "Site for Fourth Coffee"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Energy Operations Agent (d) — site records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No site matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Energy Operations Agent (d) (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="SITE- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
