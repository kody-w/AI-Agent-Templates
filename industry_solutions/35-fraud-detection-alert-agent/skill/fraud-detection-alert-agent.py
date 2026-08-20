#!/usr/bin/env python3
"""Fraud Detection & Alert Agent — portable skill. Deploy AI-driven fraud monitoring and identification to accelerate investigations, enhance detection rates, and improve prevention.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "FRD-10700",
                "subject": "Graphic Design Institute",
                "status": "flagged",
                "owner": "Fraud Analysts",
                "metric": 44.0,
                "note": "Case for Graphic Design Institute"
        },
        {
                "reference": "FRD-10701",
                "subject": "Contoso",
                "status": "under review",
                "owner": "SIU Investigators",
                "metric": 47.7,
                "note": "Case for Contoso"
        },
        {
                "reference": "FRD-10702",
                "subject": "Northwind Traders",
                "status": "cleared",
                "owner": "Risk Leaders",
                "metric": 51.4,
                "note": "Case for Northwind Traders"
        },
        {
                "reference": "FRD-10703",
                "subject": "Fabrikam",
                "status": "confirmed fraud",
                "owner": "Fraud Analysts",
                "metric": 55.1,
                "note": "Case for Fabrikam"
        },
        {
                "reference": "FRD-10704",
                "subject": "Adatum",
                "status": "escalated",
                "owner": "SIU Investigators",
                "metric": 58.8,
                "note": "Case for Adatum"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Fraud Detection & Alert Agent — case records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No case matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Fraud Detection & Alert Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="FRD- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
