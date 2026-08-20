#!/usr/bin/env python3
"""HR Self-Service Agent — portable skill. Provide self-service HR inquiry handling that transforms the process from a manual ticket-based system to intelligent, automated resolutions.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "CS-10920",
                "subject": "Wingtip Toys",
                "status": "open",
                "owner": "Employees",
                "metric": 71.5,
                "note": "Case for Wingtip Toys"
        },
        {
                "reference": "CS-10921",
                "subject": "Tailwind Traders",
                "status": "in progress",
                "owner": "Managers",
                "metric": 75.2,
                "note": "Case for Tailwind Traders"
        },
        {
                "reference": "CS-10922",
                "subject": "Proseware",
                "status": "resolved",
                "owner": "HR Operations Staff",
                "metric": 78.9,
                "note": "Case for Proseware"
        },
        {
                "reference": "CS-10923",
                "subject": "Litware",
                "status": "escalated",
                "owner": "Employees",
                "metric": 82.6,
                "note": "Case for Litware"
        },
        {
                "reference": "CS-10924",
                "subject": "Alpine Ski House",
                "status": "closed",
                "owner": "Managers",
                "metric": 86.3,
                "note": "Case for Alpine Ski House"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["HR Self-Service Agent — case records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No case matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="HR Self-Service Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="CS- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
