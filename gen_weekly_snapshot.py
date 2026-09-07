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

The existing PR/PO row arrays remain the sub-bucket history contract. New
snapshots also include a separate raceControl object with holder, header-stage,
and current-step-age metrics. --race-control-only backfills that object without
replacing an existing week's PR/PO arrays.
"""
import argparse, json, math, os
from datetime import datetime, date, timezone

import openpyxl

PR_STEPS_MAP = {"Handyman Services_Manager":"Dep Managers","Building Services_Asst. Facility Managers 1":"Dep Managers","PurchReqReviewTask":"PR In Review","Procurement sends inquiry/RFQ to suppliers":"RFQ to suppliers","Quotation received and logged/attached":"Qt received & Logged","Quotation shared to Operations for confirmation":"Qt Shared to Op","Operations confirms material/scope":"OP confirms material","Unit prices updated in PR lines":"Unit Price Updated","Building Services_Asst. Facility Managers 2":"Dep Managers","Building Services_Facilities Manager":"Dep Managers","PAC Services_Manager":"Dep Managers","Concierge Services_Manager":"Dep Managers","Security Services_Manager":"Dep Managers","Home Services_Operations Manager":"Dep Managers","Landscaping_Manager":"Dep Managers","Finance & Accounts_Accounting Manager":"Finance","Facilities Management_Director":"Director","Commercial_Director":"Director","Executive Management_CEO":"CEO"}
PO_STEPS_MAP = {"Advance payment request submitted (if applicable)":"Procurement","Procurement Manager":"Procurement","Accounting Manager":"Finance","Finance and Accounts Director":"Director","CEO":"CEO","LPO sent/shared with supplier":"Sent to Supplier"}

USER_DEPT = {"Abdul Basit Raza":"Building Services","Abdul.basit":"IT","Abdul.Muqeet":"Security Services","Admin":"IT","admin.hk":"Housekeeping Services","Adnan.Ullah":"Procurement","Ahamed Noorullah Mohamed":"Accomodation Services","Ahmed.Odeh":"Building Services","Aparna.Pauly":"Procurement","arman.b":"Accounts & Tax","ayman.g":"Accounts & Tax","Ayman.ismail":"Accounts & Tax","Buying Agent Concierge":"Concierge Services","D365CRM ADMIN":"IT","D365CRMADMIN":"IT","Dinesh Laxman Laxman":"Building Services","dinesh.laxman":"Building Services","Gokul Krishna Pillai":"Contracted Cleaning Services","Gokul.Krishna":"Contracted Cleaning Services","IT DEPARTMENT":"IT","Joe Orlain Jamisola":"Concierge Services","Judhin.prabhakar":"Contracted Cleaning Services","Layusha.cleatus":"Procurement","Mohamed.Ashraf":"Procurement","Mohammad.w":"Building Services","Muhammad Shehzad Ahmeduddin":"IT","muhammad.mustajab":"Accounts & Tax","Nathan.Buys":"Building Services","Patrick.Smith":"Accounts & Tax","Pramod Chandrasenan Chandrasenan":"Security Services","pramod.c":"Security Services","Qasim Jahangir":"QHSE","Roderick Red Palma":"Procurement","roderick.red":"Procurement","Shaik.baba":"Housekeeping Services","Shakir Ameer Bakhsh":"FitOut Services","Shijil Choyaprath Chandran":"Home Maintenance Services","shijil.c":"Home Maintenance Services","Sirinikhil":"Housekeeping Services","teena.k":"Concierge Services","Ubaid":"IT","Zaheer Ahmed Ameer":"Accomodation Services","Zaheer.Ahmed":"Accomodation Services"}
DEPT_OPS_USER = {"Building Services":"dinesh.laxman","Landscaping Services":"dinesh.laxman","Contracted Cleaning Services":"Gokul.Krishna","Security Services":"pramod.c","FitOut Services":"Shakir Ameer Bakhsh","Home Maintenance Services":"shijil.c"}
USER_ALIAS = {"dinesh laxman laxman":"dinesh.laxman","gokul krishna pillai":"Gokul.Krishna","pramod chandrasenan chandrasenan":"pramod.c","shijil choyaprath chandran":"shijil.c","zaheer ahmed ameer":"Zaheer.Ahmed","d365crm admin":"it.solutions","d365crmadmin":"it.solutions","it department":"it.solutions"}
PR_PROC_BUCKETS = {"PR In Review","RFQ to suppliers","Qt received & Logged","OP confirms material","Procurement (in process)"}
PR_OPS_BUCKETS = {"Qt Shared to Op","Unit Price Updated"}
PR_HEADER_STAGES = ["Re-Assigned/Rejected","Procurement","Operations to Confirm","Dep Managers","Finance","Director","CEO"]
PO_HEADER_STAGES = ["Procurement","Finance","Director","CEO","Sent to Supplier","Pending Invoicing"]

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


def norm(value):
    return " ".join(str(value or "").strip().lower().split())


def canonical_owner(value):
    original = str(value or "").strip()
    return USER_ALIAS.get(norm(original), original)


def dept_for_user(value):
    wanted = norm(value)
    for user, department in USER_DEPT.items():
        if norm(user) == wanted:
            return department
    return ""


def role_of(value):
    department = dept_for_user(value)
    user = norm(value)
    if department == "Accounts & Tax":
        if user == "ayman.g":
            return "Director"
        if user == "patrick.smith":
            return "CEO"
        return "Finance"
    return "Procurement" if department == "Procurement" else ""


def median(values):
    usable = sorted(v for v in values if v is not None)
    if not usable:
        return None
    middle = len(usable) // 2
    return usable[middle] if len(usable) % 2 else (usable[middle - 1] + usable[middle]) / 2


def one_decimal(value):
    return None if value is None else round(value, 1)


def race_metric(items):
    ages = [item["age"] for item in items if item.get("age") is not None]
    return {
        "items": len(items),
        "value": round(sum(float(item.get("value") or 0) for item in items), 2),
        "averageDays": one_decimal(sum(ages) / len(ages)) if ages else None,
        "medianDays": one_decimal(median(ages)),
        "oldestDays": max(ages) if ages else None,
        "over7": len([age for age in ages if age > 7]),
    }


def pr_type(doc):
    s = str(doc or "").upper()
    if s.startswith("CPR"):
        return "CPR"
    if s.startswith("PR"):
        return "PR"
    return "OTHER"


def read_rows(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        ws = wb.active
        it = ws.iter_rows(values_only=True)
        hdr = [str(h) if h is not None else "" for h in next(it)]
        for row in it:
            if row is None or all(v is None for v in row):
                continue
            yield dict(zip(hdr, row))
    finally:
        wb.close()


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


def load_stuck_documents(path):
    if not path or not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    return {str(item.get("documentNumber") or "").strip().upper()
            for item in payload.get("items", []) if item.get("documentNumber")}


def race_pr_items(path, asof_end):
    items = []
    for r in read_rows(path):
        step = r.get("Step name")
        bucket = PR_STEPS_MAP.get(step)
        status = str(r.get("Status") or "—")
        if not bucket or status in ("Closed", "Rejected", "Cancelled"):
            continue
        if bucket in PR_PROC_BUCKETS:
            home = "Procurement"
        elif bucket in PR_OPS_BUCKETS:
            home = "Operations to Confirm"
        else:
            home = bucket
        if status == "Draft":
            pending = str(r.get("Preparer") or "").strip()
        elif status == "Approved":
            pending = str(r.get("Accepted By/Assign To") or "").strip()
        else:
            pending = str(r.get("Pending Approver/User") or "").strip()
        department = str(r.get("Department") or "").strip()
        owner = ((DEPT_OPS_USER.get(department) or pending)
                 if home == "Operations to Confirm" else pending) or "(unassigned)"
        role = role_of(owner)
        in_review = status == "In review"
        if role in ("Finance", "Director", "CEO"):
            stage = role
        elif role == "Procurement":
            stage = "Re-Assigned/Rejected" if home == "Operations to Confirm" and in_review else "Procurement"
        else:
            stage = "Re-Assigned/Rejected" if home == "Procurement" and in_review else ("Operations to Confirm" if home == "Operations to Confirm" else "Dep Managers")
        created = parse_dt(r.get("Created date"))
        step_date = parse_dt(r.get("Step date and time"))
        items.append({
            "document": str(r.get("Purchase requisition") or "").strip().upper(),
            "type": "PR", "stage": stage, "owner": owner, "personPending": True,
            "age": days_between(step_date or created, asof_end),
            "value": float(r.get("Total amount") or 0),
        })
    return items


def race_po_items(path, asof_end):
    items = []
    for r in read_rows(path):
        step = r.get("Step name")
        approval = str(r.get("Approval status") or "")
        po_status = str(r.get("Purchase order status") or "")
        bucket = PO_STEPS_MAP.get(step) if step else None
        if approval == "Confirmed" and po_status == "Received":
            bucket = "Pending Invoicing"
        if not bucket or approval == "Rejected" or po_status in ("Canceled", "Invoiced"):
            continue
        vendor_stage = bucket in ("Sent to Supplier", "Pending Invoicing")
        if vendor_stage:
            owner = str(r.get("Vendor name") or "-").strip()
            person_pending = False
            stage = bucket
        elif approval == "In review":
            owner = str(r.get("Pending Approver/User") or "").strip() or "(unassigned)"
            person_pending = True
            role = role_of(owner)
            stage = role if role in ("Finance", "Director", "CEO") else "Procurement"
        elif approval == "Draft":
            owner = str(r.get("Created by") or r.get("Created By") or r.get("Pending Approver/User") or "").strip() or "(unassigned)"
            person_pending = True
            role = role_of(owner)
            stage = role if role in ("Finance", "Director", "CEO") else "Procurement"
        else:
            owner = str(r.get("Pending Approver/User") or "").strip() or "(unassigned)"
            person_pending = False
            role = role_of(owner)
            stage = role if role in ("Finance", "Director", "CEO") else "Procurement"
        created = parse_dt(r.get("Created date and time")) or parse_dt(r.get("Requested receipt date"))
        step_date = parse_dt(r.get("Step date and time"))
        items.append({
            "document": str(r.get("Purchase order") or "").strip().upper(),
            "type": "PO", "stage": stage, "owner": owner, "personPending": person_pending,
            "age": days_between(step_date or created, asof_end),
            "value": float(r.get("Total amount") or 0),
        })
    return items


def race_control_snapshot(pr_path, po_path, asof_end, stuck_documents):
    source_pr_items = race_pr_items(pr_path, asof_end)
    excluded_maintained = len([item for item in source_pr_items if item["document"] in stuck_documents])
    pr_items = [item for item in source_pr_items if item["document"] not in stuck_documents]
    po_items = race_po_items(po_path, asof_end)
    all_items = pr_items + po_items

    holder_groups = {}
    for item in all_items:
        if not item["personPending"] or item["stage"] in ("Director", "CEO", "Sent to Supplier", "Pending Invoicing"):
            continue
        owner = canonical_owner(item["owner"])
        if not owner or owner == "(unassigned)":
            continue
        key = norm(owner)
        group = holder_groups.setdefault(key, {"key": key, "name": owner, "items": []})
        group["items"].append(item)

    holders = []
    for group in holder_groups.values():
        stats = race_metric(group["items"])
        stats.update({
            "key": group["key"], "name": group["name"],
            "prItems": len([item for item in group["items"] if item["type"] == "PR"]),
            "poItems": len([item for item in group["items"] if item["type"] == "PO"]),
        })
        holders.append(stats)
    holders.sort(key=lambda item: (-item["items"], -(item["oldestDays"] or -1), item["name"].lower()))

    stages = []
    for item_type, order, source in (("PR", PR_HEADER_STAGES, pr_items), ("PO", PO_HEADER_STAGES, po_items)):
        for name in order:
            matching = [item for item in source if item["stage"] == name]
            if not matching:
                continue
            stats = race_metric(matching)
            stats.update({"key": f"{item_type}|{name}", "type": item_type, "name": name})
            stages.append(stats)

    return {
        "overall": race_metric(all_items),
        "holders": holders,
        "stages": stages,
        "excludedMaintainedItems": excluded_maintained,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pr", default="pr.xlsx")
    ap.add_argument("--po", default="po.xlsx")
    ap.add_argument("--asof", required=True, help="Week-end date YYYY-MM-DD (Sunday)")
    ap.add_argument("--out", default="weekly_snapshots.json")
    ap.add_argument("--source", default="live")
    ap.add_argument("--stuck-items", default="stuck_items.json")
    ap.add_argument("--race-control-only", action="store_true",
                    help="Add Race Control metrics without replacing existing PR/PO row arrays")
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
    if not os.path.exists(args.pr) or not os.path.exists(args.po):
        raise SystemExit("Both PR and PO workbooks are required for Race Control metrics")
    race_control = race_control_snapshot(
        args.pr, args.po, asof_end, load_stuck_documents(args.stuck_items)
    )
    existing_week = data["weeks"].get(args.asof)
    if args.race_control_only:
        if not existing_week:
            raise SystemExit("--race-control-only requires an existing week")
        existing_week["raceControl"] = race_control
        existing_week["raceControlSource"] = args.source
    else:
        data["weeks"][args.asof] = {"PR": pr_rows, "PO": po_rows, "source": args.source,
                                    "counts": {"PR": len(pr_rows), "PO": len(po_rows)},
                                    "raceControl": race_control}

    # keep only the most recent MAX_WEEKS_KEPT week-ends
    keys = sorted(data["weeks"].keys())
    for k in keys[:-MAX_WEEKS_KEPT]:
        del data["weeks"][k]

    data["generatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print(f"[ok] {args.asof}: PR={len(pr_rows)} PO={len(po_rows)} "
          f"holders={len(race_control['holders'])} → {args.out}")


if __name__ == "__main__":
    main()
