#!/usr/bin/env python3
"""Contract Review Agent — portable skill. Automate contract review processes to enable faster, lower-risk, and more successful negotiations.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "REG-10040",
                "subject": "Alpine Ski House",
                "status": "open",
                "owner": "Legal Operations",
                "metric": 49.5,
                "note": "Item for Alpine Ski House"
        },
        {
                "reference": "REG-10041",
                "subject": "Lucerne Publishing",
                "status": "in review",
                "owner": "Attorneys",
                "metric": 53.2,
                "note": "Item for Lucerne Publishing"
        },
        {
                "reference": "REG-10042",
                "subject": "Coho Vineyard",
                "status": "cleared",
                "owner": "Executives",
                "metric": 56.9,
                "note": "Item for Coho Vineyard"
        },
        {
                "reference": "REG-10043",
                "subject": "Margie's Travel",
                "status": "flagged",
                "owner": "Legal Operations",
                "metric": 60.6,
                "note": "Item for Margie's Travel"
        },
        {
                "reference": "REG-10044",
                "subject": "Fourth Coffee",
                "status": "remediated",
                "owner": "Attorneys",
                "metric": 64.3,
                "note": "Item for Fourth Coffee"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Contract Review Agent — item records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No item matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Contract Review Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="REG- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
