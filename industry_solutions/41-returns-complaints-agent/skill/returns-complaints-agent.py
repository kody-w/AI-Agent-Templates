#!/usr/bin/env python3
"""Returns & Complaints Agent — portable skill. Automate return decisions and complaint handling to speed resolution, reduce fraud, and protect customer loyalty.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "CS-10820",
                "subject": "Margie's Travel",
                "status": "open",
                "owner": "Customer Service Agents",
                "metric": 67.0,
                "note": "Case for Margie's Travel"
        },
        {
                "reference": "CS-10821",
                "subject": "Fourth Coffee",
                "status": "in progress",
                "owner": "Quality Teams",
                "metric": 70.7,
                "note": "Case for Fourth Coffee"
        },
        {
                "reference": "CS-10822",
                "subject": "Graphic Design Institute",
                "status": "resolved",
                "owner": "Loss Prevention Teams",
                "metric": 74.4,
                "note": "Case for Graphic Design Institute"
        },
        {
                "reference": "CS-10823",
                "subject": "Contoso",
                "status": "escalated",
                "owner": "Customer Service Agents",
                "metric": 78.1,
                "note": "Case for Contoso"
        },
        {
                "reference": "CS-10824",
                "subject": "Northwind Traders",
                "status": "closed",
                "owner": "Quality Teams",
                "metric": 81.8,
                "note": "Case for Northwind Traders"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Returns & Complaints Agent — case records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No case matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Returns & Complaints Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="CS- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
