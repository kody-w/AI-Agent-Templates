#!/usr/bin/env python3
"""Branch Banking Advisory Agent — portable skill. Automate branch banking and advisory workflows to streamline customer interactions, strengthen compliance, and improve financial guidance.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "CS-10960",
                "subject": "Contoso",
                "status": "open",
                "owner": "Branch Bankers",
                "metric": 20.5,
                "note": "Case for Contoso"
        },
        {
                "reference": "CS-10961",
                "subject": "Northwind Traders",
                "status": "in progress",
                "owner": "Financial Advisors",
                "metric": 24.2,
                "note": "Case for Northwind Traders"
        },
        {
                "reference": "CS-10962",
                "subject": "Fabrikam",
                "status": "resolved",
                "owner": "Compliance Officers",
                "metric": 27.9,
                "note": "Case for Fabrikam"
        },
        {
                "reference": "CS-10963",
                "subject": "Adatum",
                "status": "escalated",
                "owner": "Branch Bankers",
                "metric": 31.6,
                "note": "Case for Adatum"
        },
        {
                "reference": "CS-10964",
                "subject": "Trey Research",
                "status": "closed",
                "owner": "Financial Advisors",
                "metric": 35.3,
                "note": "Case for Trey Research"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Branch Banking Advisory Agent — case records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No case matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Branch Banking Advisory Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="CS- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
