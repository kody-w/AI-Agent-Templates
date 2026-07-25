#!/usr/bin/env python3
"""Energy Operations Agent (a) — portable skill. Deliver real-time insights, automate critical workflows, and enable guided decision making—boosting efficiency while reducing operational and compliance risk for energy organizations.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "SITE-10200",
                "subject": "Fabrikam",
                "status": "nominal",
                "owner": "Plant Manager / Reliability Engineer",
                "metric": 21.5,
                "note": "Site for Fabrikam"
        },
        {
                "reference": "SITE-10201",
                "subject": "Adatum",
                "status": "watch",
                "owner": "Compliance Manager",
                "metric": 25.2,
                "note": "Site for Adatum"
        },
        {
                "reference": "SITE-10202",
                "subject": "Trey Research",
                "status": "alert",
                "owner": "Sustainability Lead",
                "metric": 28.9,
                "note": "Site for Trey Research"
        },
        {
                "reference": "SITE-10203",
                "subject": "Woodgrove Bank",
                "status": "maintenance",
                "owner": "Data Analyst",
                "metric": 32.6,
                "note": "Site for Woodgrove Bank"
        },
        {
                "reference": "SITE-10204",
                "subject": "Wingtip Toys",
                "status": "resolved",
                "owner": "Plant Manager / Reliability Engineer",
                "metric": 36.3,
                "note": "Site for Wingtip Toys"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Energy Operations Agent (a) — site records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No site matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Energy Operations Agent (a) (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="SITE- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
