#!/usr/bin/env python3
"""
gen_weekly_snapshot.py — capture a week-end snapshot of the live PR/PO pipeline
per sub-bucket (D365 step), for the dashboard's "Sub-bucket Weekly Comparison".

Mirrors the JS logic in index.html (buildPRRecords / buildPORecords /
livePipelineFilter) so client-side filters can be re-applied to snapshot rows.

Usage:
  python3 gen_weekly_snapshot.py --pr pr.xlsx --po po.xlsx --asof 2026-08-09 \
      --out weekly_snapshots.json [--source git:abc1234]

Appends/overwrites weeks[asof] in --out (creates the file if missing).
Row fields: [doc, step, bucket, dept, project, status, created, aging, prType]
"""
import argparse, json, math, os
from datetime import datetime, date

import openpyxl

PR_STEPS_MAP = {"Handyman Services_Manager":"Dep Managers","Building Services_Asst. Facility Managers 1":"Dep Managers","PurchReqReviewTask":"PR In Review","Procurement sends inquiry/RFQ to suppliers":"RFQ to suppliers","Quotation received and logged/attached":"Qt received & Logged","Quotation shared to Operations for confirmation":"Qt Shared to Op","Operations confirms material/scope":"OP confirms material","Unit prices updated in PR lines":"Unit Price Updated","Building Services_Asst. Facility Managers 2":"Dep Managers","Building Services_Facilities Manager":"Dep Managers","PAC Services_Manager":"Dep Managers","Concierge Services_Manager":"Dep Managers","Security Services_Manager":"Dep Managers","Home Services_Operations Manager":"Dep Managers","Landscaping_Manager":"Dep Managers","Finance & Accounts_Accounting Manager":"Finance","Facilities Management_Director":"Director","Commercial_Director":"Director","Executive Management_CEO":"CEO"}
PO_STEPS_MAP = {"Advance payment request submitted (if applicable)":"Procurement","Procurement Manager":"Procurement","Accounting Manager":"Finance","Finance and Accounts Director":"Director","CEO":"CEO","LPO sent/shared with supplier":"Sent to Supplier"}

MAX_WEEKS_KEPT = 12


def parse_dt(v):
    if v is None or v == "":
        return None
    if isinstance(v, datetime):
        return v
    if isinstance(v, date):
        return datetime(v.year, v.month, v.day)
    s = str(v).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%m/%d/%Y %H:%M:%S", "%m/%d/%Y",
                "%d/%m/%Y %H:%M:%S", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    return None


def days_between(d1, d2):
    if not d1 or not d2:
        return None
    return max(0, math.floor((d2 - d1).total_seconds() / 86400))


def pr_type(doc):
    s = str(doc or "").upper()
    if s.startswith("CPR"):
        return "CPR"
    if s.startswith("PR"):
        return "PR"
    return "OTHER"


def read_rows(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    it = ws.iter_rows(values_only=True)
    hdr = [str(h) if h is not None else "" for h in next(it)]
    for row in it:
        if row is None or all(v is None for v in row):
            continue
        yield dict(zip(hdr, row))


def snap_pr(path, asof_end):
    rows = []
    for r in read_rows(path):
        step = r.get("Step name")
        if not step or step not in PR_STEPS_MAP:
            continue                      # unmapped → not live pipeline
        status = str(r.get("Status") or "—")
        if status in ("Closed", "Rejected", "Cancelled"):
            continue
        created = parse_dt(r.get("Created date"))
        step_dt = parse_dt(r.get("Step date and time"))
        ref = step_dt or created
        aging = days_between(ref, asof_end)
        doc = r.get("Purchase requisition") or ""
        rows.append([doc, step, PR_STEPS_MAP[step],
                     r.get("Department") or "—", r.get("Location") or "—",
                     status, created.strftime("%Y-%m-%d") if created else None,
                     aging, pr_type(doc)])
    return rows


def snap_po(path, asof_end):
    rows = []
    for r in read_rows(path):
        step = r.get("Step name")
        approval = str(r.get("Approval status") or "")
        po_status = str(r.get("Purchase order status") or "")
        bucket = PO_STEPS_MAP.get(step) if step else None
        # Status-based override (highest priority) — mirrors index.html
        if approval == "Confirmed" and po_status == "Received":
            bucket = "Pending Invoicing"
        if not bucket:
            continue                      # unmapped → not live pipeline
        if approval in ("Rejected",) or po_status in ("Canceled", "Invoiced"):
            continue
        created = parse_dt(r.get("Created date and time")) or parse_dt(r.get("Requested receipt date"))
        step_dt = parse_dt(r.get("Step date and time"))
        ref = step_dt or created
        aging = days_between(ref, asof_end)
        doc = r.get("Purchase order") or ""
        rows.append([doc, step or "—", bucket,
                     r.get("Department") or "—", r.get("Location") or "—",
                     approval or "—", created.strftime("%Y-%m-%d") if created else None,
                     aging, pr_type(r.get("Purchase requisition") or "")])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pr", default="pr.xlsx")
    ap.add_argument("--po", default="po.xlsx")
    ap.add_argument("--asof", required=True, help="Week-end date YYYY-MM-DD (Sunday)")
    ap.add_argument("--out", default="weekly_snapshots.json")
    ap.add_argument("--source", default="live")
    args = ap.parse_args()

    asof = datetime.strptime(args.asof, "%Y-%m-%d")
    asof_end = asof.replace(hour=23, minute=59, second=59)

    data = {"fields": ["doc", "step", "bucket", "dept", "project", "status", "created", "aging", "prType"],
            "weekStartsOn": "Mon", "weeks": {}}
    if os.path.exists(args.out):
        with open(args.out, encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("weeks", {})

    pr_rows = snap_pr(args.pr, asof_end) if os.path.exists(args.pr) else []
    po_rows = snap_po(args.po, asof_end) if os.path.exists(args.po) else []
    data["weeks"][args.asof] = {"PR": pr_rows, "PO": po_rows, "source": args.source,
                                "counts": {"PR": len(pr_rows), "PO": len(po_rows)}}

    # keep only the most recent MAX_WEEKS_KEPT week-ends
    keys = sorted(data["weeks"].keys())
    for k in keys[:-MAX_WEEKS_KEPT]:
        del data["weeks"][k]

    data["generatedAt"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print(f"[ok] {args.asof}: PR={len(pr_rows)} PO={len(po_rows)} → {args.out}")


if __name__ == "__main__":
    main()
