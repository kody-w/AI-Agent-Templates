#!/usr/bin/env python3
"""Energy Operations Agent (b) — portable skill. Deliver real-time insights, automate critical workflows, and enable guided decision making—boosting efficiency while reducing operational and compliance risk for energy organizations.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "SITE-10220",
                "subject": "Tailwind Traders",
                "status": "nominal",
                "owner": "Plant Manager / Reliability Engineer",
                "metric": 40.0,
                "note": "Site for Tailwind Traders"
        },
        {
                "reference": "SITE-10221",
                "subject": "Proseware",
                "status": "watch",
                "owner": "Compliance Manager",
                "metric": 43.7,
                "note": "Site for Proseware"
        },
        {
                "reference": "SITE-10222",
                "subject": "Litware",
                "status": "alert",
                "owner": "Sustainability Lead",
                "metric": 47.4,
                "note": "Site for Litware"
        },
        {
                "reference": "SITE-10223",
                "subject": "Alpine Ski House",
                "status": "maintenance",
                "owner": "Data Analyst",
                "metric": 51.1,
                "note": "Site for Alpine Ski House"
        },
        {
                "reference": "SITE-10224",
                "subject": "Lucerne Publishing",
                "status": "resolved",
                "owner": "Plant Manager / Reliability Engineer",
                "metric": 54.8,
                "note": "Site for Lucerne Publishing"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Energy Operations Agent (b) — site records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No site matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Energy Operations Agent (b) (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="SITE- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
