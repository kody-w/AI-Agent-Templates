#!/usr/bin/env python3
"""Inventory Optimization Agent — portable skill. Intelligently optimize inventory portfolios to improve cash flow and warehouse efficiency while reducing waste.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "SKU-10140",
                "subject": "Adatum",
                "status": "in stock",
                "owner": "Supply Chain Managers",
                "metric": 54.0,
                "note": "Sku for Adatum"
        },
        {
                "reference": "SKU-10141",
                "subject": "Trey Research",
                "status": "low",
                "owner": "Inventory Managers",
                "metric": 57.7,
                "note": "Sku for Trey Research"
        },
        {
                "reference": "SKU-10142",
                "subject": "Woodgrove Bank",
                "status": "backordered",
                "owner": "Procurement Manager",
                "metric": 61.4,
                "note": "Sku for Woodgrove Bank"
        },
        {
                "reference": "SKU-10143",
                "subject": "Wingtip Toys",
                "status": "reorder",
                "owner": "Supply Chain Managers",
                "metric": 65.1,
                "note": "Sku for Wingtip Toys"
        },
        {
                "reference": "SKU-10144",
                "subject": "Tailwind Traders",
                "status": "overstock",
                "owner": "Inventory Managers",
                "metric": 68.8,
                "note": "Sku for Tailwind Traders"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Inventory Optimization Agent — SKU records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No SKU matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Inventory Optimization Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="SKU- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
