#!/usr/bin/env python3
"""Generate pr.xlsx and po.xlsx from the shared live PR/PO dataset.

These files are a one-way compatibility output for Chandan's frozen email app.
Nothing in the dashboard or current email path reads them.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from openpyxl import Workbook, load_workbook
from openpyxl.comments import Comment
from openpyxl.worksheet.table import Table, TableStyleInfo

from legacy_email_stage_map import (
    NO_EXACT_OLD_EQUIVALENT,
    PO_STAGE_RULES,
    PR_MANAGER_STEP_BY_DEPARTMENT,
    PR_STAGE_RULES,
)

DEFAULT_DATASET_URL = (
    "https://ssg-prpo-proxy-h4cvfegaduftedhz.uaenorth-01.azurewebsites.net/api/dataset"
)
OUTPUT_NOTE = (
    "Generated from the live dataset for the legacy email app only; not a data "
    "source; delete when the sender moves to ssg-prpo-proxy."
)
FIXED_ZIP_TIME = (2026, 9, 7, 0, 0, 0)

PR_COLUMNS = [
    "Purchase requisition", "Quotation reference", "Name", "Preparer", "Status",
    "Created date", "Submitted date", "Requisition purpose", "Submission Status",
    "Accepted By/Assign To", "Department", "Location", "Contract",
    "Request for quotation case", "Total amount", "Pending Approver/User",
    "Step name", "Step date and time",
]
PO_COLUMNS = [
    "Purchase order", "Vendor account", "Invoice account", "Vendor name",
    "Purchase type", "Approval status", "Purchase order status", "Currency",
    "Requested receipt date", "Created date and time", "Purchase requisition",
    "RFQ number", "Total amount", "Department", "Location", "Contract",
    "Pending Approver/User", "Step name", "Step date and time", "Created by",
]
PR_WIDTHS = [24, 23, 8, 12, 10, 16, 18, 23, 21, 25, 14, 12, 12, 30, 16, 25, 13, 22]
PO_WIDTHS = [18, 18, 19, 15, 17, 19, 25, 12, 26, 25, 24, 14, 16, 14, 12, 12, 25, 13, 22, 14]
PR_DATE_COLUMNS = {"Created date": "mm-dd-yy", "Submitted date": "mm-dd-yy", "Step date and time": "m/d/yy h:mm"}
PO_DATE_COLUMNS = {"Requested receipt date": "mm-dd-yy", "Created date and time": "m/d/yy h:mm", "Step date and time": "m/d/yy h:mm"}


def fetch_dataset(url: str) -> dict:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "prpo-legacy-output/1.0"})
    with urlopen(request, timeout=180) as response:
        payload = json.load(response)
    if payload.get("sourceState") != "LIVE":
        raise RuntimeError(f"dataset sourceState must be LIVE, got {payload.get('sourceState')!r}")
    if not payload.get("revision"):
        raise RuntimeError("dataset revision is missing")
    return payload


def parse_datetime(value):
    if value in (None, "") or isinstance(value, datetime):
        return value or None
    if not isinstance(value, str):
        return value
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    # Excel cannot represent F&O's year-0001 sentinel. Keep the source ISO text
    # verbatim so it is not silently converted into a false 1900 date.
    if parsed.year < 1900:
        return value
    if parsed.tzinfo:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


def pr_workbook_step(row: dict) -> str:
    stage = str(row.get("Step name") or "")
    rule = PR_STAGE_RULES.get(stage)
    if not rule:
        raise RuntimeError(f"displayed PR stage has no legacy mapping: {stage!r}")
    if stage == "Dep Managers":
        return PR_MANAGER_STEP_BY_DEPARTMENT.get(
            str(row.get("Department") or ""), rule["workbook_step"]
        )
    return rule["workbook_step"]


def dashboard_pr_rows(rows: list[dict]) -> tuple[list[dict], Counter]:
    output = []
    excluded = Counter()
    for row in rows:
        status = str(row.get("Status") or "").strip().lower()
        stage = str(row.get("Step name") or "")
        if status not in {"in review", "approved"}:
            continue
        if stage not in PR_STAGE_RULES:
            excluded[stage or "(blank)"] += 1
            continue
        translated = {column: row.get(column) for column in PR_COLUMNS}
        translated["Step name"] = pr_workbook_step(row)
        output.append(translated)
    return output, excluded


def dashboard_po_rows(rows: list[dict]) -> tuple[list[dict], Counter]:
    output = []
    excluded = Counter()
    for row in rows:
        stage = str(row.get("Live stage") or row.get("Step name") or "")
        if not row.get("Open pipeline"):
            if stage in NO_EXACT_OLD_EQUIVALENT["PO"]:
                excluded[stage] += 1
            continue
        if stage == "STAGE_NOT_EVIDENCED":
            raise RuntimeError("P1a failure: open PO has STAGE_NOT_EVIDENCED")
        rule = PO_STAGE_RULES.get(stage)
        if not rule:
            raise RuntimeError(f"displayed PO stage has no legacy mapping: {stage!r}")
        translated = {column: row.get(column) for column in PO_COLUMNS}
        translated["Step name"] = rule["workbook_step"]
        # Chandan's frozen logic recognizes Pending Invoicing only from
        # Confirmed + Received. A posted packing slip is therefore expressed
        # through that legacy compatibility status even for a partially open
        # live order; the live dataset remains authoritative and unchanged.
        if rule.get("approval_status_override"):
            translated["Approval status"] = rule["approval_status_override"]
        if rule.get("purchase_order_status_override"):
            translated["Purchase order status"] = rule["purchase_order_status_override"]
        translated["Step date and time"] = (
            None if row.get("Clock provenance") == "NOT_RECORDED" else row.get("Step date and time")
        )
        output.append(translated)
    return output, excluded


def stable_sort(rows: list[dict], columns: list[str]) -> list[dict]:
    return sorted(rows, key=lambda row: tuple("" if row.get(c) is None else str(row.get(c)) for c in columns))


def content_hash(rows: list[dict], columns: list[str]) -> str:
    material = [[row.get(column) for column in columns] for row in stable_sort(rows, columns)]
    return hashlib.sha256(
        json.dumps(material, ensure_ascii=False, separators=(",", ":"), default=str).encode("utf-8")
    ).hexdigest()


def workbook_bytes(rows: list[dict], columns: list[str], widths: list[int], date_columns: dict[str, str]) -> bytes:
    workbook = Workbook()
    workbook.properties.creator = "Strive Services Group"
    workbook.properties.title = "Legacy PR/PO email compatibility output"
    workbook.properties.description = OUTPUT_NOTE
    fixed = datetime(2026, 9, 7, 0, 0, 0)
    workbook.properties.created = fixed
    workbook.properties.modified = fixed
    sheet = workbook.active
    sheet.title = "Sheet1"
    sheet.append(columns)
    sheet["A1"].comment = Comment(OUTPUT_NOTE, "Strive Services Group")
    for row in stable_sort(rows, columns):
        values = []
        for column in columns:
            value = row.get(column)
            if column in date_columns:
                value = parse_datetime(value)
            values.append(value)
        sheet.append(values)
    for index, width in enumerate(widths, 1):
        sheet.column_dimensions[sheet.cell(1, index).column_letter].width = width
    for index, column in enumerate(columns, 1):
        if column in date_columns:
            for cell in sheet.iter_cols(min_col=index, max_col=index, min_row=2, max_row=sheet.max_row):
                cell[0].number_format = date_columns[column]
        elif column == "Total amount":
            for cell in sheet.iter_cols(min_col=index, max_col=index, min_row=2, max_row=sheet.max_row):
                cell[0].number_format = "#,##0.00"
        else:
            for cell in sheet.iter_cols(min_col=index, max_col=index, min_row=2, max_row=sheet.max_row):
                cell[0].number_format = "@"
    table = Table(displayName="AxTable1", ref=f"A1:{sheet.cell(sheet.max_row, len(columns)).coordinate}")
    table.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2", showFirstColumn=False, showLastColumn=False,
        showRowStripes=True, showColumnStripes=False,
    )
    sheet.add_table(table)
    raw = io.BytesIO()
    workbook.save(raw)
    raw.seek(0)
    deterministic = io.BytesIO()
    with ZipFile(raw, "r") as source, ZipFile(deterministic, "w", ZIP_DEFLATED, compresslevel=9) as target:
        for name in sorted(source.namelist()):
            original = source.getinfo(name)
            info = ZipInfo(name, FIXED_ZIP_TIME)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = original.external_attr
            info.flag_bits = original.flag_bits
            target.writestr(info, source.read(name))
    return deterministic.getvalue()


def validate_saved(path: Path, columns: list[str], expected_rows: int) -> None:
    workbook = load_workbook(path, read_only=False, data_only=False)
    sheet = workbook.active
    headers = [sheet.cell(1, index).value for index in range(1, sheet.max_column + 1)]
    if headers != columns:
        raise RuntimeError(f"{path.name}: header mismatch: {headers!r}")
    if sheet.max_row - 1 != expected_rows:
        raise RuntimeError(f"{path.name}: expected {expected_rows} rows, got {sheet.max_row - 1}")
    if sheet["A1"].comment is None or sheet["A1"].comment.text != OUTPUT_NOTE:
        raise RuntimeError(f"{path.name}: legacy-output note missing")
    if list(sheet.tables) != ["AxTable1"]:
        raise RuntimeError(f"{path.name}: AxTable1 missing")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-url", default=DEFAULT_DATASET_URL)
    parser.add_argument("--dataset-json")
    parser.add_argument("--output-dir", default=".")
    parser.add_argument("--state-file", default=".legacy-email-workbook-content.json")
    parser.add_argument("--evidence")
    args = parser.parse_args()
    dataset = json.loads(Path(args.dataset_json).read_text(encoding="utf-8")) if args.dataset_json else fetch_dataset(args.dataset_url)
    if dataset.get("sourceState") != "LIVE":
        raise RuntimeError("refusing to generate from a stale or failed dataset")
    pr_rows, pr_excluded = dashboard_pr_rows(dataset["pr"]["rows"])
    po_rows, po_excluded = dashboard_po_rows(dataset["po"]["rows"])
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pr_path, po_path = output_dir / "pr.xlsx", output_dir / "po.xlsx"
    state_path = output_dir / args.state_file
    state = {
        "formatVersion": 2,
        "prContentSha256": content_hash(pr_rows, PR_COLUMNS),
        "poContentSha256": content_hash(po_rows, PO_COLUMNS),
    }
    previous = None
    if state_path.exists():
        try:
            previous = json.loads(state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            previous = None
    content_changed = previous != state or not pr_path.exists() or not po_path.exists()
    if content_changed:
        pr_path.write_bytes(workbook_bytes(pr_rows, PR_COLUMNS, PR_WIDTHS, PR_DATE_COLUMNS))
        po_path.write_bytes(workbook_bytes(po_rows, PO_COLUMNS, PO_WIDTHS, PO_DATE_COLUMNS))
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    validate_saved(pr_path, PR_COLUMNS, len(pr_rows))
    validate_saved(po_path, PO_COLUMNS, len(po_rows))
    summary = {
        "datasetRevision": dataset["revision"],
        "sourceState": dataset["sourceState"],
        "pr": {"rows": len(pr_rows), "columns": PR_COLUMNS, "amountExVat": round(sum(float(row.get("Total amount") or 0) for row in pr_rows), 2), "sha256": sha256(pr_path), "excludedNoEquivalent": dict(pr_excluded)},
        "po": {"rows": len(po_rows), "columns": PO_COLUMNS, "amountExVat": round(sum(float(row.get("Total amount") or 0) for row in po_rows), 2), "sha256": sha256(po_path), "clockCounts": dataset["po"].get("clockCounts", {}), "notRecordedDatesBlank": sum(1 for row in dataset["po"]["rows"] if row.get("Open pipeline") and row.get("Clock provenance") == "NOT_RECORDED" and not row.get("Step date and time")), "excludedNoEquivalent": dict(po_excluded)},
        "amountBasis": "live F&O active-line values excl. VAT",
        "datePolicy": "live event, final-workbook seed, or blank for NOT_RECORDED",
        "outputNote": OUTPUT_NOTE,
        "contentChanged": content_changed,
        "noExactOldEquivalent": NO_EXACT_OLD_EQUIVALENT,
    }
    rendered = json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    print(rendered, end="")
    if args.evidence:
        Path(args.evidence).write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
