#!/usr/bin/env python3
"""Order Status & Delay Agent — portable skill. Automate proactive order updates, delay management, and customer communications to protect relationships and revenue.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "PO-10840",
                "subject": "Fabrikam",
                "status": "placed",
                "owner": "Customer Service Rep",
                "metric": 85.5,
                "note": "Order for Fabrikam"
        },
        {
                "reference": "PO-10841",
                "subject": "Adatum",
                "status": "approved",
                "owner": "Account Manager",
                "metric": 89.2,
                "note": "Order for Adatum"
        },
        {
                "reference": "PO-10842",
                "subject": "Trey Research",
                "status": "in transit",
                "owner": "Operations Leader",
                "metric": 92.9,
                "note": "Order for Trey Research"
        },
        {
                "reference": "PO-10843",
                "subject": "Woodgrove Bank",
                "status": "delivered",
                "owner": "Customer Service Rep",
                "metric": 96.6,
                "note": "Order for Woodgrove Bank"
        },
        {
                "reference": "PO-10844",
                "subject": "Wingtip Toys",
                "status": "delayed",
                "owner": "Account Manager",
                "metric": 100.3,
                "note": "Order for Wingtip Toys"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Order Status & Delay Agent — order records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No order matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Order Status & Delay Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="PO- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
