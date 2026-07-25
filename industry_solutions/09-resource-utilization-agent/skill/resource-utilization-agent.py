#!/usr/bin/env python3
"""Resource Utilization Agent — portable skill. Provide intelligent resource analysis and recommendations to maximize billable utilization and reduce costs.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "CS-10180",
                "subject": "Margie's Travel",
                "status": "open",
                "owner": "Operations Leader",
                "metric": 91.0,
                "note": "Case for Margie's Travel"
        },
        {
                "reference": "CS-10181",
                "subject": "Fourth Coffee",
                "status": "in progress",
                "owner": "Resource Manager",
                "metric": 94.7,
                "note": "Case for Fourth Coffee"
        },
        {
                "reference": "CS-10182",
                "subject": "Graphic Design Institute",
                "status": "resolved",
                "owner": "Finance Director",
                "metric": 98.4,
                "note": "Case for Graphic Design Institute"
        },
        {
                "reference": "CS-10183",
                "subject": "Contoso",
                "status": "escalated",
                "owner": "Operations Leader",
                "metric": 14.1,
                "note": "Case for Contoso"
        },
        {
                "reference": "CS-10184",
                "subject": "Northwind Traders",
                "status": "closed",
                "owner": "Resource Manager",
                "metric": 17.8,
                "note": "Case for Northwind Traders"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Resource Utilization Agent — case records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No case matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Resource Utilization Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="CS- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
