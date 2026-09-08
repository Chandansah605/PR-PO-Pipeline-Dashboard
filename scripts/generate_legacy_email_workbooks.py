#!/usr/bin/env python3
"""Generate the temporary legacy-workbook input for the PR/PO email sender."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import subprocess
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
)

DEFAULT_DATASET_URL = (
    "https://ssg-prpo-proxy-h4cvfegaduftedhz.uaenorth-01.azurewebsites.net/api/dataset"
)
OUTPUT_NOTE = (
    "Temporary email compatibility output: verified PR/PO routing snapshot "
    "with current live ex-VAT amounts."
)
FIXED_ZIP_TIME = (2026, 9, 7, 0, 0, 0)
# Snapshot consumed by the successful 7 September 10:00 Dubai email run.
LEGACY_EMAIL_COMMIT = "d1fbf0482684b0f467cd9f8552af30cc28216ad0"

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
LEGACY_EMAIL_PR_STEPS = {
    "Handyman Services_Manager",
    "Building Services_Asst. Facility Managers 1",
    "PurchReqReviewTask",
    "Procurement sends inquiry/RFQ to suppliers",
    "Quotation received and logged/attached",
    "Quotation shared to Operations for confirmation",
    "Operations confirms material/scope",
    "Unit prices updated in PR lines",
    "Building Services_Asst. Facility Managers 2",
    "Building Services_Facilities Manager",
    "PAC Services_Manager",
    "Concierge Services_Manager",
    "Security Services_Manager",
    "Home Services_Operations Manager",
    "Landscaping_Manager",
    "Finance & Accounts_Accounting Manager",
    "Facilities Management_Director",
    "Commercial_Director",
    "Executive Management_CEO",
}


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


def load_legacy_rows(filename: str, columns: list[str], commit: str = LEGACY_EMAIL_COMMIT) -> list[dict]:
    """Load one last-known-good snapshot without changing its file contract."""
    result = subprocess.run(
        ["git", "show", f"{commit}:{filename}"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    workbook = load_workbook(io.BytesIO(result.stdout), read_only=True, data_only=True)
    sheet = workbook.active
    values = sheet.iter_rows(values_only=True)
    headers = list(next(values))
    if headers != columns:
        raise RuntimeError(f"last known-good {filename} headers do not match the protected contract")
    rows = []
    for cells in values:
        row = dict(zip(headers, cells))
        number_column = "Purchase requisition" if filename == "pr.xlsx" else "Purchase order"
        number = str(row.get(number_column) or "").strip().upper()
        if not number:
            continue
        rows.append({column: row.get(column) for column in columns})
    return rows


def fallback_pr_rows(live_rows: list[dict], legacy_rows: list[dict]) -> tuple[list[dict], Counter]:
    """Keep the proven routing snapshot but refresh every amount from live F&O."""
    live_amounts = {}
    for row in live_rows:
        number = str(row.get("Purchase requisition") or "").strip().upper()
        if not number:
            continue
        if number in live_amounts:
            raise RuntimeError(f"duplicate requisition in live dataset: {number}")
        live_amounts[number] = row.get("Total amount")

    output = []
    evidence = Counter()
    seen = set()
    for row in legacy_rows:
        number = str(row.get("Purchase requisition") or "").strip().upper()
        if number in seen:
            raise RuntimeError(f"duplicate requisition in fallback snapshot: {number}")
        seen.add(number)
        if number not in live_amounts:
            status = str(row.get("Status") or "")
            email_actionable = (
                str(row.get("Step name") or "") in LEGACY_EMAIL_PR_STEPS
                and status.lower() != "closed"
                and status not in {"Rejected", "Cancelled"}
            )
            if email_actionable:
                raise RuntimeError(f"actionable fallback requisition missing from live ex-VAT source: {number}")
            evidence["unavailable non-action row omitted"] += 1
            continue
        translated = {column: row.get(column) for column in PR_COLUMNS}
        translated["Total amount"] = live_amounts[number]
        owner = str(translated.get("Pending Approver/User") or "")
        if "," in owner:
            raise RuntimeError(f"fallback requisition has multiple owners: {number}")
        output.append(translated)
        evidence["live ex-VAT amount joined"] += 1
    return output, evidence


def fallback_po_rows(live_rows: list[dict], legacy_rows: list[dict]) -> tuple[list[dict], Counter]:
    """Keep the proven PO routing snapshot but refresh every amount from live F&O."""
    live_amounts = {}
    for row in live_rows:
        number = str(row.get("Purchase order") or "").strip().upper()
        vendor = str(row.get("Vendor account") or "").strip().upper()
        if not number:
            continue
        key = (number, vendor)
        if key in live_amounts:
            raise RuntimeError(f"duplicate purchase order/vendor in live dataset: {number}/{vendor}")
        live_amounts[key] = row.get("Total amount")

    output = []
    evidence = Counter()
    seen = set()
    for row in legacy_rows:
        number = str(row.get("Purchase order") or "").strip().upper()
        vendor = str(row.get("Vendor account") or "").strip().upper()
        key = (number, vendor)
        if key in seen:
            raise RuntimeError(f"duplicate purchase order/vendor in fallback snapshot: {number}/{vendor}")
        seen.add(key)
        if key not in live_amounts:
            raise RuntimeError(f"fallback purchase order missing from live ex-VAT source: {number}/{vendor}")
        translated = {column: row.get(column) for column in PO_COLUMNS}
        translated["Total amount"] = live_amounts[key]
        owner = str(translated.get("Pending Approver/User") or "")
        if "," in owner:
            raise RuntimeError(f"fallback purchase order has multiple owners: {number}")
        output.append(translated)
        evidence["live ex-VAT amount joined"] += 1
    return output, evidence


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
    legacy_pr_rows = load_legacy_rows("pr.xlsx", PR_COLUMNS)
    legacy_po_rows = load_legacy_rows("po.xlsx", PO_COLUMNS)
    pr_rows, pr_excluded = fallback_pr_rows(dataset["pr"]["rows"], legacy_pr_rows)
    po_rows, po_excluded = fallback_po_rows(dataset["po"]["rows"], legacy_po_rows)
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
        "pr": {
            "rows": len(pr_rows), "columns": PR_COLUMNS,
            "amountExVat": round(sum(float(row.get("Total amount") or 0) for row in pr_rows), 2),
            "sha256": sha256(pr_path), "routingRecovery": dict(pr_excluded),
            "operationsConfirmationRows": sum(
                row.get("Step name") in {
                    "Quotation shared to Operations for confirmation",
                    "Unit prices updated in PR lines",
                }
                for row in pr_rows
            ),
            "commaJoinedOwners": sum("," in str(row.get("Pending Approver/User") or "") for row in pr_rows),
        },
        "po": {
            "rows": len(po_rows), "columns": PO_COLUMNS,
            "amountExVat": round(sum(float(row.get("Total amount") or 0) for row in po_rows), 2),
            "sha256": sha256(po_path), "routingRecovery": dict(po_excluded),
            "commaJoinedOwners": sum("," in str(row.get("Pending Approver/User") or "") for row in po_rows),
        },
        "amountBasis": "live F&O active-line values excl. VAT",
        "datePolicy": "last successful PR/PO routing snapshot",
        "routingPolicy": (
            f"temporary one-morning PR/PO fallback from {LEGACY_EMAIL_COMMIT}; exact document-number join; "
            "all amounts replaced from the current live ex-VAT dataset"
        ),
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
