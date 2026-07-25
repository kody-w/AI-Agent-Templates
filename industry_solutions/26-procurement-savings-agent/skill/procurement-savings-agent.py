#!/usr/bin/env python3
"""Procurement Savings Agent — portable skill. Identify and optimize savings opportunities across vendors, contracts, and purchasing cycles to reduce costs and increase procurement efficiency.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "PO-10520",
                "subject": "Fabrikam",
                "status": "placed",
                "owner": "Procurement Manager",
                "metric": 53.5,
                "note": "Order for Fabrikam"
        },
        {
                "reference": "PO-10521",
                "subject": "Adatum",
                "status": "approved",
                "owner": "Finance Director",
                "metric": 57.2,
                "note": "Order for Adatum"
        },
        {
                "reference": "PO-10522",
                "subject": "Trey Research",
                "status": "in transit",
                "owner": "Category Buyer",
                "metric": 60.9,
                "note": "Order for Trey Research"
        },
        {
                "reference": "PO-10523",
                "subject": "Woodgrove Bank",
                "status": "delivered",
                "owner": "Procurement Manager",
                "metric": 64.6,
                "note": "Order for Woodgrove Bank"
        },
        {
                "reference": "PO-10524",
                "subject": "Wingtip Toys",
                "status": "delayed",
                "owner": "Finance Director",
                "metric": 68.3,
                "note": "Order for Wingtip Toys"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Procurement Savings Agent — order records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No order matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Procurement Savings Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="PO- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
