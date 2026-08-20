#!/usr/bin/env python3
"""Client Health Score Agent — portable skill. Automate client portfolio health monitoring and planning to improve client relationships, protect revenue, and optimize financial performance.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "CS-10320",
                "subject": "Contoso",
                "status": "open",
                "owner": "Client Success Leaders",
                "metric": 44.5,
                "note": "Case for Contoso"
        },
        {
                "reference": "CS-10321",
                "subject": "Northwind Traders",
                "status": "in progress",
                "owner": "Account Manager",
                "metric": 48.2,
                "note": "Case for Northwind Traders"
        },
        {
                "reference": "CS-10322",
                "subject": "Fabrikam",
                "status": "resolved",
                "owner": "Client Success Leaders",
                "metric": 51.9,
                "note": "Case for Fabrikam"
        },
        {
                "reference": "CS-10323",
                "subject": "Adatum",
                "status": "escalated",
                "owner": "Account Manager",
                "metric": 55.6,
                "note": "Case for Adatum"
        },
        {
                "reference": "CS-10324",
                "subject": "Trey Research",
                "status": "closed",
                "owner": "Client Success Leaders",
                "metric": 59.3,
                "note": "Case for Trey Research"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Client Health Score Agent — case records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No case matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Client Health Score Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="CS- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
