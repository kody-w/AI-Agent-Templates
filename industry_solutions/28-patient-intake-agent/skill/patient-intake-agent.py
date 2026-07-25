#!/usr/bin/env python3
"""Patient Intake Agent — portable skill. Automate patient intake workflows to streamline operations, protect revenue from avoidable losses, and deliver a smoother patient experience.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "PT-10560",
                "subject": "Coho Vineyard",
                "status": "registered",
                "owner": "Front Desk Staff",
                "metric": 90.5,
                "note": "Record for Coho Vineyard"
        },
        {
                "reference": "PT-10561",
                "subject": "Margie's Travel",
                "status": "triaged",
                "owner": "Scheduling Coordinators",
                "metric": 94.2,
                "note": "Record for Margie's Travel"
        },
        {
                "reference": "PT-10562",
                "subject": "Fourth Coffee",
                "status": "in care",
                "owner": "Patient Access Reps",
                "metric": 97.9,
                "note": "Record for Fourth Coffee"
        },
        {
                "reference": "PT-10563",
                "subject": "Graphic Design Institute",
                "status": "discharged",
                "owner": "Front Desk Staff",
                "metric": 13.6,
                "note": "Record for Graphic Design Institute"
        },
        {
                "reference": "PT-10564",
                "subject": "Contoso",
                "status": "pending auth",
                "owner": "Scheduling Coordinators",
                "metric": 17.3,
                "note": "Record for Contoso"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Patient Intake Agent — record records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No record matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Patient Intake Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="PT- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
