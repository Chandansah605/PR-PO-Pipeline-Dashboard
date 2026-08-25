#!/usr/bin/env python3
"""Independent XLSX reconciliation for the rendered Journey Board anchors.

This verification script intentionally does not import gen_journey_board.py.
"""
from collections import defaultdict
from datetime import date, datetime
from statistics import median

import numpy as np
import openpyxl


def rows(path):
    sheet = openpyxl.load_workbook(path, read_only=True, data_only=True).active
    iterator = sheet.iter_rows(values_only=True)
    headers = [str(value).strip() if value is not None else "" for value in next(iterator)]
    return [dict(zip(headers, row)) for row in iterator]


def stamp(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    return datetime.fromisoformat(str(value).replace("T", " "))


def workdays(start, end):
    return int(np.busday_count(stamp(start).date(), stamp(end).date()))


def division(department):
    if department in {
        "Building Services", "Concierge Services", "Leisure Services", "Security Services",
        "Landscaping Services", "Contracted Cleaning Services",
    }:
        return "FM"
    if department in {"Home Maintenance Services", "Housekeeping Services", "Laundry"}:
        return "HS"
    if department in {"FitOut Services", "Surveying Services"}:
        return "FITOUT"
    return "FACTORY"


pr_rows, po_rows = rows("pr.xlsx"), rows("po.xlsx")
eligible = {
    row["Purchase requisition"]: row
    for row in pr_rows
    if stamp(row.get("Created date"))
    and stamp(row["Created date"]).date() >= date(2026, 4, 1)
    and str(row.get("Status") or "").strip().lower() not in {"cancelled", "rejected"}
}
completed = []
for po in po_rows:
    pr = eligible.get(po.get("Purchase requisition"))
    step = str(po.get("Step name") or "").lower()
    status = str(po.get("Purchase order status") or "").lower()
    if not pr or not (status in {"received", "invoiced"} or "lpo sent" in step or "shared with supplier" in step):
        continue
    milestones = [
        stamp(pr.get("Created date")), stamp(pr.get("Submitted date")),
        stamp(po.get("Created date and time")), stamp(po.get("Step date and time")),
    ]
    if not all(milestones) or not milestones[0] <= milestones[1] <= milestones[2] <= milestones[3]:
        continue
    cumulative = [workdays(milestones[0], milestone) for milestone in milestones[1:]]
    req_type = "CPR" if str(pr["Purchase requisition"]).startswith("CPR-") else "PR"
    completed.append((*cumulative, division(pr.get("Department")), req_type, milestones[3]))

end_to_end = [row[2] for row in completed]
print(
    f"ALL n={len(end_to_end)} submitted={median(row[0] for row in completed):.1f} "
    f"po={median(row[1] for row in completed):.1f} lpo={median(end_to_end):.1f} "
    f"p90={np.percentile(end_to_end, 90):.0f} "
    f"within10={sum(value <= 10 for value in end_to_end) / len(end_to_end) * 100:.1f}%"
)
for div, req_type, label in (
    ("HS", "CPR", "HS CPR"), ("FACTORY", "PR", "Factory PR"),
    ("FM", "PR", "FM PR"), ("FITOUT", "CPR", "FitOut CPR"), ("FM", "CPR", "FM CPR"),
):
    lane = [row for row in completed if row[3] == div and row[4] == req_type]
    submitted, po_created = median(row[0] for row in lane), median(row[1] for row in lane)
    print(
        f"{label}: n={len(lane)} median={median(row[2] for row in lane):.1f} "
        f"within10={sum(row[2] <= 10 for row in lane) / len(lane) * 100:.1f}% "
        f"submitted_to_po={po_created - submitted:.1f}"
    )

weeks = defaultdict(list)
for row in completed:
    weeks[row[5].isocalendar()[1]].append(row[2])
print("TREND W27-W34=" + ",".join(f"{median(weeks[week]):g}" for week in range(27, 35)))

queues = defaultdict(list)
as_of = datetime(2026, 8, 25)
for pr in eligible.values():
    if str(pr.get("Status") or "").strip().lower() != "in review" or not stamp(pr.get("Step date and time")):
        continue
    step = str(pr.get("Step name") or "").lower()
    if "purchreqreview" in step:
        gate = "PR Review"
    elif "rfq" in step or "inquiry" in step:
        gate = "RFQ to Suppliers"
    elif "quotation received" in step:
        gate = "Quotation Received"
    elif "shared to operations" in step or "operations confirms" in step or "operations for confirmation" in step:
        gate = "Ops Confirmation"
    elif "unit prices" in step:
        gate = "Prices Updated"
    else:
        gate = "Mgmt Approvals"
    queues[gate].append(max(0, (as_of - stamp(pr["Step date and time"])).total_seconds() / 86400))
print(f"DEEPEST Prices Updated n={len(queues['Prices Updated'])} median={median(queues['Prices Updated']):.1f}d")
