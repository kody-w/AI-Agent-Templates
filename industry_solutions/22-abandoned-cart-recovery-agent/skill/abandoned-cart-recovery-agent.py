#!/usr/bin/env python3
"""Abandoned Cart Recovery Agent — portable skill. Automate abandoned cart analysis and recovery campaigns to convert lost sales, protect margins, and improve customer engagement.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "CX-10440",
                "subject": "Fourth Coffee",
                "status": "new",
                "owner": "Marketing Manager",
                "metric": 67.5,
                "note": "Record for Fourth Coffee"
        },
        {
                "reference": "CX-10441",
                "subject": "Graphic Design Institute",
                "status": "engaged",
                "owner": "Digital Marketing Lead",
                "metric": 71.2,
                "note": "Record for Graphic Design Institute"
        },
        {
                "reference": "CX-10442",
                "subject": "Contoso",
                "status": "converted",
                "owner": "Growth Manager",
                "metric": 74.9,
                "note": "Record for Contoso"
        },
        {
                "reference": "CX-10443",
                "subject": "Northwind Traders",
                "status": "lapsed",
                "owner": "Marketing Manager",
                "metric": 78.6,
                "note": "Record for Northwind Traders"
        },
        {
                "reference": "CX-10444",
                "subject": "Fabrikam",
                "status": "nurture",
                "owner": "Digital Marketing Lead",
                "metric": 82.3,
                "note": "Record for Fabrikam"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Abandoned Cart Recovery Agent — record records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No record matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Abandoned Cart Recovery Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="CX- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
