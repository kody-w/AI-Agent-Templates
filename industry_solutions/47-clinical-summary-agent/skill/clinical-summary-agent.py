#!/usr/bin/env python3
"""Clinical Summary Agent — portable skill. Transform complex clinical histories into clear, actionable summaries for faster decision-making, better coordination, and safer care.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "PT-10940",
                "subject": "Lucerne Publishing",
                "status": "registered",
                "owner": "Primary care physicians",
                "metric": 90.0,
                "note": "Record for Lucerne Publishing"
        },
        {
                "reference": "PT-10941",
                "subject": "Coho Vineyard",
                "status": "triaged",
                "owner": "Surgeons",
                "metric": 93.7,
                "note": "Record for Coho Vineyard"
        },
        {
                "reference": "PT-10942",
                "subject": "Margie's Travel",
                "status": "in care",
                "owner": "Anesthesia teams",
                "metric": 97.4,
                "note": "Record for Margie's Travel"
        },
        {
                "reference": "PT-10943",
                "subject": "Fourth Coffee",
                "status": "discharged",
                "owner": "Primary care physicians",
                "metric": 13.1,
                "note": "Record for Fourth Coffee"
        },
        {
                "reference": "PT-10944",
                "subject": "Graphic Design Institute",
                "status": "pending auth",
                "owner": "Surgeons",
                "metric": 16.8,
                "note": "Record for Graphic Design Institute"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Clinical Summary Agent — record records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No record matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Clinical Summary Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="PT- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
