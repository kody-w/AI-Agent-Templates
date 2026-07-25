#!/usr/bin/env python3
"""Purchase Order Management Agent — portable skill. Automate purchase order management and vendor selection to enable faster and more cost-effective purchasing.

No framework dependency: run standalone (CLI) or import query(). Synthetic
demo data (Microsoft fictional companies) — no PII. Usable by any AI tool.
"""
import argparse

DATA = [
        {
                "reference": "PO-10120",
                "subject": "Fourth Coffee",
                "status": "placed",
                "owner": "Procurement Manager",
                "metric": 35.5,
                "note": "Order for Fourth Coffee"
        },
        {
                "reference": "PO-10121",
                "subject": "Graphic Design Institute",
                "status": "approved",
                "owner": "Finance Director",
                "metric": 39.2,
                "note": "Order for Graphic Design Institute"
        },
        {
                "reference": "PO-10122",
                "subject": "Contoso",
                "status": "in transit",
                "owner": "Department Approver",
                "metric": 42.9,
                "note": "Order for Contoso"
        },
        {
                "reference": "PO-10123",
                "subject": "Northwind Traders",
                "status": "delivered",
                "owner": "Procurement Manager",
                "metric": 46.6,
                "note": "Order for Northwind Traders"
        },
        {
                "reference": "PO-10124",
                "subject": "Fabrikam",
                "status": "delayed",
                "owner": "Finance Director",
                "metric": 50.3,
                "note": "Order for Fabrikam"
        }
]


def query(reference=""):
    ref = str(reference or "").strip().lower()
    if not ref or ref == "list":
        out = ["Purchase Order Management Agent — order records:"]
        out += ["- %s | %s | %s | owner %s" % (r["reference"], r["subject"], r["status"], r["owner"]) for r in DATA]
        return "\n".join(out)
    hits = [r for r in DATA if ref == r["reference"].lower() or ref in r["subject"].lower()]
    if not hits:
        return "No order matches %r. Try 'list'." % reference
    r = hits[0]
    return "%s — %s | status %s | owner %s | metric %s | %s" % (
        r["reference"], r["subject"], r["status"], r["owner"], r["metric"], r["note"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Purchase Order Management Agent (portable skill)")
    p.add_argument("reference", nargs="?", default="", help="PO- id, subject name, or 'list'")
    print(query(p.parse_args().reference))
