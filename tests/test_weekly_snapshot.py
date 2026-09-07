import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gen_weekly_snapshot as snapshot


def write_book(path, headers, rows):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(headers)
    for row in rows:
        sheet.append([row.get(header) for header in headers])
    workbook.save(path)


with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary)
    pr_path = root / "pr.xlsx"
    po_path = root / "po.xlsx"
    pr_headers = ["Purchase requisition", "Step name", "Status", "Department", "Preparer",
                  "Accepted By/Assign To", "Pending Approver/User", "Created date",
                  "Step date and time", "Total amount"]
    po_headers = ["Purchase order", "Step name", "Approval status", "Purchase order status",
                  "Pending Approver/User", "Created by", "Vendor name", "Created date and time",
                  "Step date and time", "Total amount"]
    write_book(pr_path, pr_headers, [
        {"Purchase requisition": "PR-ONE", "Step name": "Quotation shared to Operations for confirmation",
         "Status": "In review", "Department": "Building Services", "Pending Approver/User": "Layusha.cleatus",
         "Created date": "2026-08-20", "Step date and time": "2026-08-30", "Total amount": 100},
        {"Purchase requisition": "PR-TWO", "Step name": "Building Services_Asst. Facility Managers 1",
         "Status": "In review", "Department": "Building Services", "Pending Approver/User": "Dinesh Laxman Laxman",
         "Created date": "2026-08-20", "Step date and time": "2026-08-24", "Total amount": 200},
        {"Purchase requisition": "PR-STUCK", "Step name": "Building Services_Asst. Facility Managers 1",
         "Status": "In review", "Department": "Building Services", "Pending Approver/User": "dinesh.laxman",
         "Created date": "2026-08-01", "Step date and time": "2026-08-01", "Total amount": 500},
        {"Purchase requisition": "PR-THREE", "Step name": "Quotation shared to Operations for confirmation",
         "Status": "In review", "Department": "Transportation", "Pending Approver/User": "dinesh.laxman",
         "Created date": "2026-08-20", "Step date and time": "2026-08-28", "Total amount": 25},
    ])
    write_book(po_path, po_headers, [
        {"Purchase order": "PO-ONE", "Step name": "Procurement Manager", "Approval status": "In review",
         "Purchase order status": "Open order", "Pending Approver/User": "Aparna.Pauly",
         "Created date and time": "2026-08-25", "Step date and time": "2026-08-29", "Total amount": 50},
        {"Purchase order": "PO-TWO", "Step name": "LPO sent/shared with supplier", "Approval status": "Confirmed",
         "Purchase order status": "Open order", "Vendor name": "Vendor", "Created date and time": "2026-08-20",
         "Step date and time": "2026-08-25", "Total amount": 80},
    ])

    result = snapshot.race_control_snapshot(
        str(pr_path), str(po_path), datetime(2026, 8, 30, 23, 59, 59), {"PR-STUCK"}
    )
    assert result["overall"]["items"] == 5
    assert result["excludedMaintainedItems"] == 1
    assert result["overall"]["medianDays"] == 2.0
    assert result["holders"][0]["name"] == "dinesh.laxman"
    assert result["holders"][0]["items"] == 3
    assert result["holders"][0]["value"] == 325
    assert not any(holder["name"] == "Vendor" for holder in result["holders"])
    assert any(stage["key"] == "PO|Sent to Supplier" for stage in result["stages"])

    existing = {
        "fields": ["doc", "step"],
        "weekStartsOn": "Mon",
        "weeks": {"2026-08-30": {"PR": [["unchanged-pr"]], "PO": [["unchanged-po"]], "source": "old", "counts": {"PR": 1, "PO": 1}}}
    }
    out_path = root / "weekly.json"
    stuck_path = root / "stuck.json"
    out_path.write_text(json.dumps(existing, separators=(",", ":")), encoding="utf-8")
    stuck_path.write_text(json.dumps({"items": [{"documentNumber": "PR-STUCK"}]}), encoding="utf-8")
    original_pr = json.dumps(existing["weeks"]["2026-08-30"]["PR"], separators=(",", ":"))
    original_po = json.dumps(existing["weeks"]["2026-08-30"]["PO"], separators=(",", ":"))

    import subprocess
    subprocess.run([
        "python", "gen_weekly_snapshot.py", "--pr", str(pr_path), "--po", str(po_path),
        "--asof", "2026-08-30", "--out", str(out_path), "--stuck-items", str(stuck_path),
        "--race-control-only", "--source", "test-history"
    ], check=True, capture_output=True, text=True)
    updated = json.loads(out_path.read_text(encoding="utf-8"))
    assert json.dumps(updated["weeks"]["2026-08-30"]["PR"], separators=(",", ":")) == original_pr
    assert json.dumps(updated["weeks"]["2026-08-30"]["PO"], separators=(",", ":")) == original_po
    assert updated["weeks"]["2026-08-30"]["raceControl"]["overall"]["items"] == 5

print("Weekly snapshot Race Control tests passed")
