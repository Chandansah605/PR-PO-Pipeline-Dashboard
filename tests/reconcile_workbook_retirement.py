"""Read-only workbook-retirement reconciliation for the PR/PO dashboard.

The script never writes to Dataverse. It reads the last committed workbooks,
the F&O virtual entities in operations-ifahr-live, and the PR/PO approval
capture in operations-ifahr-dev. Access tokens are supplied through process
environment variables and are never persisted in the report.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


LIVE = "https://operations-ifahr-live.crm15.dynamics.com"
DEV = "https://operations-ifahr-dev.crm15.dynamics.com"
FORMATTED = "@OData.Community.Display.V1.FormattedValue"
GUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)

PR_APPROVAL = {
    "Building Services_Facilities Manager": "Dep Managers",
    "Building Services_Asst. Facility Managers 1": "Dep Managers",
    "Building Services_Asst. Facility Managers 2": "Dep Managers",
    "Home Services_Operations Manager": "Dep Managers",
    "PAC Services_Manager": "Dep Managers",
    "Housekeeping_Asst. Manager": "Dep Managers",
    "Security Services_Manager": "Dep Managers",
    "Handyman Services_Manager": "Dep Managers",
    "Concierge Services_Manager": "Dep Managers",
    "Landscaping_Manager": "Dep Managers",
    "Finance & Accounts_Accounting Manager": "Finance",
    "Facilities Management_Director": "Director",
    "Commercial_Director": "Director",
    "Executive Management_CEO": "CEO",
}
PR_PROCUREMENT = {
    "PurchReqReviewTask": "PR in review",
    "PurchReqReviewApproval": "PR in review",
    "Procurement sends inquiry/RFQ to suppliers": "Sourcing",
    "Quotation received and logged/attached": "Sourcing",
    "Quotation shared to Operations for confirmation": "Sourcing",
    "Operations confirms material/scope": "Sourcing",
    "Unit prices updated in PR lines": "Priced — awaiting approval",
}
PO_APPROVAL = {
    "Advance payment request submitted (if applicable)": "Procurement",
    "Procurement Manager": "Procurement",
    "Accounting Manager": "Finance",
    "Finance and Accounts Director": "Director",
    "CEO": "CEO",
}


def clean(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    text = str(value).strip()
    return text or None


def norm(value):
    return re.sub(r"\s+", " ", clean(value) or "").casefold()


def doc(value):
    return (clean(value) or "").upper()


def parse_dt(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    stamp = pd.to_datetime(value, utc=True, errors="coerce")
    if pd.isna(stamp):
        return None
    return stamp.to_pydatetime()


def iso(value):
    dt = parse_dt(value)
    return dt.isoformat().replace("+00:00", "Z") if dt else None


def earliest(values):
    parsed = [parse_dt(value) for value in values]
    parsed = [value for value in parsed if value]
    return min(parsed) if parsed else None


def formatted(row, field):
    return clean(row.get(field + FORMATTED)) or clean(row.get(field + "name")) or clean(row.get(field))


def api_all(origin, token, entity, select, filter_text=None):
    params = {"$select": ",".join(select)}
    if filter_text:
        params["$filter"] = filter_text
    url = f"{origin}/api/data/v9.2/{entity}?{urllib.parse.urlencode(params)}"
    rows = []
    pages = 0
    while url:
        pages += 1
        if pages > 200:
            raise RuntimeError(f"paging guard exceeded for {entity}")
        request = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Prefer": 'odata.maxpagesize=5000,odata.include-annotations="OData.Community.Display.V1.FormattedValue"',
            },
        )
        with urllib.request.urlopen(request, timeout=180) as response:
            payload = json.load(response)
        rows.extend(payload.get("value", []))
        url = payload.get("@odata.nextLink")
    return rows


def parse_dimension(value):
    parts = [part.strip() for part in str(value or "").split("-")]
    return {
        "Contract": parts[1] if len(parts) > 1 and parts[1] else None,
        "Department": parts[3] if len(parts) > 3 and parts[3] else None,
        "Location": parts[5] if len(parts) > 5 and parts[5] else None,
    }


def compare_string(workbook, live):
    return norm(workbook) == norm(live)


def compare_date(workbook, live, tolerance_days=0):
    left, right = parse_dt(workbook), parse_dt(live)
    if not left or not right:
        return False
    return abs((left - right).total_seconds()) <= tolerance_days * 86400


def compare_amount(workbook, live):
    try:
        return abs(float(workbook) - float(live)) <= 0.01
    except (TypeError, ValueError):
        return False


def column_result(rows, workbook_column, source, comparator, live_getter, affected=None):
    eligible = [row for row in rows if clean(row["workbook"].get(workbook_column)) is not None]
    compared = [row for row in eligible if live_getter(row) is not None]
    matched = sum(1 for row in compared if comparator(row["workbook"].get(workbook_column), live_getter(row)))
    return {
        "column": workbook_column,
        "liveSource": source,
        "workbookNonBlank": len(eligible) if affected is None else affected,
        "compared": len(compared),
        "matched": matched,
        "agreementPercent": round(100 * matched / len(compared), 2) if compared else None,
        "noLiveEquivalent": False,
    }


def no_equivalent(frame, column, reason):
    return {
        "column": column,
        "liveSource": reason,
        "workbookNonBlank": int(frame[column].notna().sum()),
        "compared": 0,
        "matched": 0,
        "agreementPercent": None,
        "noLiveEquivalent": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    live_token = os.environ.get("PRPO_LIVE_TOKEN")
    dev_token = os.environ.get("PRPO_DEV_TOKEN")
    if not live_token or not dev_token:
        raise SystemExit("PRPO_LIVE_TOKEN and PRPO_DEV_TOKEN are required")

    pr_book = pd.read_excel(args.repo / "pr.xlsx")
    po_book = pd.read_excel(args.repo / "po.xlsx")
    pr_book_by = {doc(row["Purchase requisition"]): row.to_dict() for _, row in pr_book.iterrows()}
    po_book_by = {doc(row["Purchase order"]): row.to_dict() for _, row in po_book.iterrows()}

    pr_headers = api_all(LIVE, live_token, "mserp_purchaserequisitionheaderv2entities", [
        "mserp_requisitionnumber", "mserp_requisitionname", "mserp_requisitionstatus",
        "mserp_requisitionpurpose", "mserp_preparerpersonnelnumber", "mserp_defaultprojectid",
        "mserp_defaultaccountingdate", "mserp_defaultrequesteddate", "mserp_ifahrquotationreference",
        "mserp_projectbuyinglegalentityid",
    ])
    pr_lines = api_all(LIVE, live_token, "mserp_purchaserequisitionlinev2entities", [
        "mserp_requisitionnumber", "mserp_lineamount", "mserp_purchaseprice", "mserp_linestatus",
        "mserp_defaultledgerdimensiondisplayvalue", "mserp_deliveryaddressname", "mserp_projectid",
        "mserp_buyinglegalentityid",
    ])
    pr_bi = api_all(LIVE, live_token, "mserp_purchreqtablebientities", [
        "mserp_purchreqid", "mserp_transdate", "mserp_submitteddatetime", "mserp_submittedby",
        "mserp_sysmodifieddatetime", "mserp_requisitionstatus", "mserp_onhold",
    ])
    po_headers = api_all(LIVE, live_token, "mserp_purchpurchaseorderheaderv2entities", [
        "mserp_purchaseordernumber", "mserp_ordervendoraccountnumber", "mserp_invoicevendoraccountnumber",
        "mserp_purchaseordername", "mserp_purchaseorderstatus", "mserp_documentapprovalstatus",
        "mserp_dataareaid", "mserp_currencycode", "mserp_accountingdate", "mserp_requesteddeliverydate",
        "mserp_deliveryaddressname", "mserp_projectid", "mserp_defaultledgerdimensiondisplayvalue",
        "mserp_ordererpersonnelnumber",
    ])
    po_lines = api_all(LIVE, live_token, "mserp_purchpurchaseorderlinev2entities", [
        "mserp_purchaseordernumber", "mserp_lineamount", "mserp_defaultledgerdimensiondisplayvalue",
        "mserp_deliveryaddressname", "mserp_projectid", "mserp_purchaserequisitionid", "mserp_dataareaid",
    ])
    packing = api_all(LIVE, live_token, "mserp_vendpackingslipjourbientities", [
        "mserp_purchid", "mserp_packingslipid", "mserp_documentdate", "mserp_dataareaid",
    ])
    snapshots = api_all(DEV, dev_token, "ssg_prpocurrentapprovalsnapshots", [
        "ssg_documentnumber", "ssg_documenttype", "ssg_pendingapprovercount", "ssg_pendingapprovernames",
        "ssg_pendinguserids", "ssg_pendingstepnames", "ssg_lastreconciledon", "ssg_oldestpendingsince",
        "ssg_dataqualitystatus", "ssg_unresolvedcount",
    ])
    instances = api_all(DEV, dev_token, "ssg_prpoapprovalinstances", [
        "ssg_prpoapprovalinstanceid", "ssg_documentnumber", "ssg_documenttype", "ssg_lastreconciledon",
        "ssg_dataqualitystatus", "ssg_parentrecordid",
    ])
    workitems = api_all(DEV, dev_token, "ssg_prpoapprovalworkitems", [
        "ssg_prpoapprovalworkitemid", "_ssg_approvalinstance_value", "ssg_approveruserid", "ssg_approvername",
        "ssg_assignedon", "ssg_firstobservedon", "ssg_iscurrent", "ssg_isunresolved",
        "ssg_stepelementid", "ssg_stepname", "ssg_delegatedfromuserid", "ssg_delegatedfromname",
        "ssg_dataqualitystatus", "ssg_lastobservedon",
    ], "ssg_iscurrent eq true")

    pr_header_by = {doc(row.get("mserp_requisitionnumber")): row for row in pr_headers}
    pr_bi_by = {doc(row.get("mserp_purchreqid")): row for row in pr_bi}
    po_header_by = {doc(row.get("mserp_purchaseordernumber")): row for row in po_headers}
    instance_by = {row["ssg_prpoapprovalinstanceid"]: row for row in instances}
    capture_by = defaultdict(list)
    unresolved_items = []
    for item in workitems:
        instance = instance_by.get(item.get("_ssg_approvalinstance_value"), {})
        number = doc(instance.get("ssg_documentnumber"))
        enriched = dict(item)
        enriched["documentNumber"] = number
        enriched["documentType"] = clean(instance.get("ssg_documenttype"))
        if not number or number.startswith("UNRESOLVED-"):
            unresolved_items.append(enriched)
        else:
            capture_by[number].append(enriched)

    snapshot_by = {}
    for snapshot in snapshots:
        number = doc(snapshot.get("ssg_documentnumber"))
        if number and not number.startswith("UNRESOLVED-") and int(snapshot.get("ssg_pendingapprovercount") or 0) > 0:
            snapshot_by[number] = snapshot

    def snapshot_users(number):
        value = clean(snapshot_by.get(number, {}).get("ssg_pendinguserids")) or clean(snapshot_by.get(number, {}).get("ssg_pendingapprovernames"))
        return {clean(part) for part in re.split(r"[;,\n]+", value or "") if clean(part)}

    def snapshot_elements(number):
        value = clean(snapshot_by.get(number, {}).get("ssg_pendingstepnames")) or ""
        return {match.group(0).casefold() for match in GUID_RE.finditer(value)}

    pr_line_by = defaultdict(list)
    for line in pr_lines:
        pr_line_by[doc(line.get("mserp_requisitionnumber"))].append(line)
    po_line_by = defaultdict(list)
    for line in po_lines:
        po_line_by[doc(line.get("mserp_purchaseordernumber"))].append(line)
    packing_by = defaultdict(list)
    for row in packing:
        packing_by[doc(row.get("mserp_purchid"))].append(row)

    def line_summary(lines, pr=False):
        active = [line for line in lines if "cancel" not in norm(formatted(line, "mserp_linestatus"))]
        first = active[0] if active else (lines[0] if lines else {})
        dims = parse_dimension(first.get("mserp_defaultledgerdimensiondisplayvalue"))
        result = {
            "count": len(active),
            "amount": round(sum(float(line.get("mserp_lineamount") or 0) for line in active), 2),
            "dimension": dims,
            "location": dims["Location"] or clean(first.get("mserp_projectid")) or clean(first.get("mserp_deliveryaddressname")),
            "linkedPR": clean(first.get("mserp_purchaserequisitionid")),
        }
        if pr:
            result["allPriced"] = bool(active) and all(float(line.get("mserp_purchaseprice") or 0) > 0 for line in active)
            result["zeroPriceLines"] = sum(float(line.get("mserp_purchaseprice") or 0) <= 0 for line in active)
        return result

    element_steps_pr = defaultdict(Counter)
    element_steps_po = defaultdict(Counter)
    for number, snapshot in snapshot_by.items():
        workbook = pr_book_by.get(number) or po_book_by.get(number)
        if not workbook:
            continue
        step = clean(workbook.get("Step name"))
        if not step:
            continue
        target = element_steps_pr if number in pr_book_by else element_steps_po
        for element in snapshot_elements(number):
            if element:
                target[element][step] += 1

    def unambiguous_approval_map(distributions, allowed):
        mapped, ambiguous = {}, {}
        for element, counts in distributions.items():
            stages = {allowed[name] for name in counts if name in allowed}
            nonapproval = {name for name in counts if name not in allowed}
            if len(stages) == 1 and not nonapproval:
                mapped[element] = next(iter(stages))
            elif stages or nonapproval:
                ambiguous[element] = dict(counts)
        return mapped, ambiguous

    pr_approval_map, pr_ambiguous = unambiguous_approval_map(element_steps_pr, PR_APPROVAL)
    po_approval_map, po_ambiguous = unambiguous_approval_map(element_steps_po, PO_APPROVAL)
    procurement_elements = {
        element for element, counts in element_steps_pr.items()
        if any(name in PR_PROCUREMENT for name in counts)
    }

    def pr_live_stage(number):
        items = capture_by.get(number, [])
        elements = snapshot_elements(number) or {norm(item.get("ssg_stepelementid")) for item in items if clean(item.get("ssg_stepelementid"))}
        approval_stages = {pr_approval_map[element] for element in elements if element in pr_approval_map}
        if approval_stages:
            return (next(iter(approval_stages)), [] if len(approval_stages) == 1 else ["CONFLICTING_APPROVAL_STAGES"])
        if elements & procurement_elements:
            lines = line_summary(pr_line_by.get(number, []), pr=True)
            flags = []
            if not lines["count"]:
                flags.append("ZERO_ACTIVE_LINES")
                return "Approval — unmapped element", flags
            if lines["allPriced"]:
                return "Priced — awaiting approval", flags
            if lines["zeroPriceLines"]:
                flags.append("ZERO_PRICE_LINES")
            # The live sources do not distinguish PR-in-review from sourcing here.
            flags.append("PR_REVIEW_SOURCING_NOT_SEPARABLE")
            return "Sourcing", flags
        if number in snapshot_by or items:
            return "Approval — unmapped element", ["UNMAPPED_ELEMENT"]
        return None, ["NO_CURRENT_WORK_ITEM"]

    def po_live_stage(number):
        items = capture_by.get(number, [])
        elements = snapshot_elements(number) or {norm(item.get("ssg_stepelementid")) for item in items if clean(item.get("ssg_stepelementid"))}
        approval_stages = {po_approval_map[element] for element in elements if element in po_approval_map}
        if approval_stages:
            return next(iter(approval_stages)), [] if len(approval_stages) == 1 else ["CONFLICTING_APPROVAL_STAGES"]
        header = po_header_by.get(number, {})
        po_status = formatted(header, "mserp_purchaseorderstatus")
        approval = formatted(header, "mserp_documentapprovalstatus")
        if norm(approval) == "confirmed" and packing_by.get(number):
            return "Pending Invoicing", []
        if norm(approval) == "confirmed" and norm(po_status) == "open order":
            return "Sent to Supplier", []
        if number in snapshot_by or items:
            return "Approval — unmapped element", ["UNMAPPED_ELEMENT"]
        return None, ["NO_CURRENT_WORK_ITEM_OR_OPEN_STAGE"]

    pr_stage_rows, pr_stage_differences = [], []
    pr_clock_rows, pr_clock_differences = [], []
    for number, workbook in pr_book_by.items():
        old_step = clean(workbook.get("Step name"))
        expected = PR_APPROVAL.get(old_step) or PR_PROCUREMENT.get(old_step)
        if not expected or number not in pr_header_by:
            continue
        actual, flags = pr_live_stage(number)
        if not actual:
            continue
        row = {"document": number, "workbookStep": old_step, "expectedStage": expected, "liveStage": actual, "flags": flags}
        pr_stage_rows.append(row)
        if expected != actual:
            pr_stage_differences.append(row)
        if expected in {"PR in review", "Sourcing", "Priced — awaiting approval"}:
            modified = pr_bi_by.get(number, {}).get("mserp_sysmodifieddatetime")
            within = compare_date(workbook.get("Step date and time"), modified, 1)
            clock = {"document": number, "stage": expected, "workbookClock": iso(workbook.get("Step date and time")), "liveSeedClock": iso(modified), "withinOneDay": within}
            pr_clock_rows.append(clock)
            if not within:
                pr_clock_differences.append(clock)

    po_stage_rows, po_stage_differences = [], []
    for number, workbook in po_book_by.items():
        old_step = clean(workbook.get("Step name"))
        if not old_step or number not in po_header_by:
            continue
        if old_step == "LPO sent/shared with supplier":
            expected = "Pending Invoicing" if norm(workbook.get("Purchase order status")) == "received" else "Sent to Supplier"
        else:
            expected = PO_APPROVAL.get(old_step)
        if not expected:
            continue
        actual, flags = po_live_stage(number)
        if not actual:
            continue
        row = {"document": number, "workbookStep": old_step, "expectedStage": expected, "liveStage": actual, "flags": flags}
        po_stage_rows.append(row)
        if expected != actual:
            po_stage_differences.append(row)

    approver_classes = Counter()
    approver_details = []
    for number, workbook in {**pr_book_by, **po_book_by}.items():
        workbook_user = clean(workbook.get("Pending Approver/User"))
        if not workbook_user or number not in snapshot_by:
            continue
        items = capture_by.get(number, [])
        users = sorted(snapshot_users(number), key=lambda value: value.casefold())
        delegated = {norm(item.get("ssg_delegatedfromuserid")) for item in items if clean(item.get("ssg_delegatedfromuserid"))}
        if norm(workbook_user) in {norm(user) for user in users}:
            category = "matched"
        elif norm(workbook_user) in delegated or any(clean(item.get("ssg_delegatedfromuserid")) for item in items):
            category = "delegated/reassigned"
        elif len(users) > 1:
            category = "parallel approvers"
        else:
            assigned = parse_dt(snapshot_by[number].get("ssg_oldestpendingsince"))
            book_date = parse_dt(workbook.get("Step date and time"))
            category = "workbook older than capture" if assigned and book_date and book_date < assigned else "unexplained"
        approver_classes[category] += 1
        if category != "matched":
            approver_details.append({"document": number, "workbookUser": workbook_user, "captureUsers": users, "category": category})

    pr_rows = []
    for number, workbook in pr_book_by.items():
        header = pr_header_by.get(number)
        if not header:
            continue
        lines = line_summary(pr_line_by.get(number, []), pr=True)
        bi = pr_bi_by.get(number, {})
        cap = capture_by.get(number, [])
        stage, _ = pr_live_stage(number)
        assigned = parse_dt(snapshot_by.get(number, {}).get("ssg_oldestpendingsince"))
        live = {
            "number": number,
            "quotation": clean(header.get("mserp_ifahrquotationreference")),
            "name": clean(header.get("mserp_requisitionname")),
            "preparer": clean(header.get("mserp_preparerpersonnelnumber")),
            "status": formatted(header, "mserp_requisitionstatus"),
            "created": clean(bi.get("mserp_transdate")) or clean(header.get("mserp_defaultaccountingdate")) or clean(header.get("mserp_defaultrequesteddate")),
            "submitted": clean(bi.get("mserp_submitteddatetime")),
            "purpose": formatted(header, "mserp_requisitionpurpose"),
            "department": lines["dimension"]["Department"],
            "location": lines["location"],
            "contract": lines["dimension"]["Contract"],
            "amount": lines["amount"],
            "users": {norm(user) for user in snapshot_users(number)},
            "stage": stage,
            "clock": clean(bi.get("mserp_sysmodifieddatetime")) if stage in {"PR in review", "Sourcing", "Priced — awaiting approval"} else assigned,
        }
        pr_rows.append({"workbook": workbook, "live": live})

    po_rows = []
    for number, workbook in po_book_by.items():
        header = po_header_by.get(number)
        if not header:
            continue
        lines = line_summary(po_line_by.get(number, []))
        cap = capture_by.get(number, [])
        stage, _ = po_live_stage(number)
        assigned = parse_dt(snapshot_by.get(number, {}).get("ssg_oldestpendingsince"))
        pack_date = earliest(item.get("mserp_documentdate") for item in packing_by.get(number, []))
        live = {
            "number": number,
            "vendorAccount": clean(header.get("mserp_ordervendoraccountnumber")),
            "invoiceAccount": clean(header.get("mserp_invoicevendoraccountnumber")),
            "vendorNameCandidate": clean(header.get("mserp_purchaseordername")),
            "purchaseType": "Purchase order",
            "approvalStatus": formatted(header, "mserp_documentapprovalstatus"),
            "poStatus": formatted(header, "mserp_purchaseorderstatus"),
            "currency": clean(header.get("mserp_currencycode")),
            "requested": clean(header.get("mserp_requesteddeliverydate")),
            "created": clean(header.get("mserp_accountingdate")),
            "linkedPR": clean(lines["linkedPR"]),
            "amount": lines["amount"],
            "department": lines["dimension"]["Department"],
            "location": lines["location"] or clean(header.get("mserp_deliveryaddressname")) or clean(header.get("mserp_projectid")),
            "contract": lines["dimension"]["Contract"],
            "users": {norm(user) for user in snapshot_users(number)},
            "stage": stage,
            "clock": assigned or pack_date,
            "createdByCandidate": clean(header.get("mserp_ordererpersonnelnumber")),
        }
        po_rows.append({"workbook": workbook, "live": live})

    s = compare_string
    d1 = lambda left, right: compare_date(left, right, 1)
    users = lambda row: row["live"]["users"] if row["live"]["users"] else None
    stage_cmp = lambda left, right: (PR_APPROVAL.get(clean(left)) or PR_PROCUREMENT.get(clean(left))) == right
    pr_columns = [
        column_result(pr_rows, "Purchase requisition", "F&O PR header", s, lambda r: r["live"]["number"]),
        column_result(pr_rows, "Quotation reference", "F&O PR header", s, lambda r: r["live"]["quotation"]),
        column_result(pr_rows, "Name", "F&O PR header", s, lambda r: r["live"]["name"]),
        column_result(pr_rows, "Preparer", "F&O PR header", s, lambda r: r["live"]["preparer"]),
        column_result(pr_rows, "Status", "F&O PR header", s, lambda r: r["live"]["status"]),
        column_result(pr_rows, "Created date", "F&O PR BI header", d1, lambda r: r["live"]["created"]),
        column_result(pr_rows, "Submitted date", "F&O PR BI header", d1, lambda r: r["live"]["submitted"]),
        column_result(pr_rows, "Requisition purpose", "F&O PR header", s, lambda r: r["live"]["purpose"]),
        no_equivalent(pr_book, "Submission Status", "no exposed live equivalent"),
        no_equivalent(pr_book, "Accepted By/Assign To", "capture has current approvers, not accepted-by"),
        column_result(pr_rows, "Department", "F&O line financial dimension", s, lambda r: r["live"]["department"]),
        column_result(pr_rows, "Location", "F&O line dimension/address/project", s, lambda r: r["live"]["location"]),
        column_result(pr_rows, "Contract", "F&O line financial dimension", s, lambda r: r["live"]["contract"]),
        no_equivalent(pr_book, "Request for quotation case", "no general exposed live equivalent"),
        column_result(pr_rows, "Total amount", "sum of F&O PR line amounts", compare_amount, lambda r: r["live"]["amount"]),
        column_result(pr_rows, "Pending Approver/User", "approval capture current work items", lambda left, right: norm(left) in right, users),
        column_result(pr_rows, "Step name", "derived live stage; approved sourcing consolidation", stage_cmp, lambda r: r["live"]["stage"]),
        column_result(pr_rows, "Step date and time", "F&O header modified seed or capture assignment", d1, lambda r: r["live"]["clock"]),
    ]
    po_columns = [
        column_result(po_rows, "Purchase order", "F&O PO header", s, lambda r: r["live"]["number"]),
        column_result(po_rows, "Vendor account", "F&O PO header", s, lambda r: r["live"]["vendorAccount"]),
        column_result(po_rows, "Invoice account", "F&O PO header", s, lambda r: r["live"]["invoiceAccount"]),
        column_result(po_rows, "Vendor name", "F&O purchase-order name candidate", s, lambda r: r["live"]["vendorNameCandidate"]),
        column_result(po_rows, "Purchase type", "constant for PO header entity", s, lambda r: r["live"]["purchaseType"]),
        column_result(po_rows, "Approval status", "F&O PO header", s, lambda r: r["live"]["approvalStatus"]),
        column_result(po_rows, "Purchase order status", "F&O PO header", s, lambda r: r["live"]["poStatus"]),
        column_result(po_rows, "Currency", "F&O PO header", s, lambda r: r["live"]["currency"]),
        column_result(po_rows, "Requested receipt date", "F&O PO header", d1, lambda r: r["live"]["requested"]),
        column_result(po_rows, "Created date and time", "F&O accounting date", d1, lambda r: r["live"]["created"]),
        column_result(po_rows, "Purchase requisition", "F&O PO line", s, lambda r: r["live"]["linkedPR"]),
        no_equivalent(po_book, "RFQ number", "no exposed live equivalent"),
        column_result(po_rows, "Total amount", "sum of F&O PO line amounts", compare_amount, lambda r: r["live"]["amount"]),
        column_result(po_rows, "Department", "F&O line financial dimension", s, lambda r: r["live"]["department"]),
        column_result(po_rows, "Location", "F&O line dimension/address/project", s, lambda r: r["live"]["location"]),
        column_result(po_rows, "Contract", "F&O line financial dimension", s, lambda r: r["live"]["contract"]),
        column_result(po_rows, "Pending Approver/User", "approval capture current work items", lambda left, right: norm(left) in right, users),
        column_result(po_rows, "Step name", "capture approval map plus F&O status/packing slip", lambda left, right: (PO_APPROVAL.get(clean(left)) or ("Pending Invoicing" if clean(left) == "LPO sent/shared with supplier" else None)) in {right, "Sent to Supplier"}, lambda r: r["live"]["stage"]),
        column_result(po_rows, "Step date and time", "capture assignment or packing-slip document date", d1, lambda r: r["live"]["clock"]),
        no_equivalent(po_book, "Created by", "orderer personnel number is not created-by"),
    ]

    review_elements = {}
    for element, counts in element_steps_pr.items():
        review = sum(count for name, count in counts.items() if PR_PROCUREMENT.get(name) == "PR in review")
        sourcing = sum(count for name, count in counts.items() if PR_PROCUREMENT.get(name) == "Sourcing")
        priced = sum(count for name, count in counts.items() if PR_PROCUREMENT.get(name) == "Priced — awaiting approval")
        if review or sourcing or priced:
            review_elements[element] = {"PR in review": review, "Sourcing": sourcing, "Priced": priced, "workbookSteps": dict(counts)}

    resolved_current = set(snapshot_by)
    snapshot_dates = [parse_dt(row.get("ssg_lastreconciledon")) for row in snapshots]
    snapshot_dates = [date for date in snapshot_dates if date]
    workitem_dates = [parse_dt(row.get("ssg_lastobservedon")) for row in workitems]
    workitem_dates = [date for date in workitem_dates if date]
    generated = datetime.now(timezone.utc)
    latest_capture = max(snapshot_dates + workitem_dates) if snapshot_dates or workitem_dates else None
    effective_data_time = min(generated, latest_capture) if latest_capture else generated
    stage_counts = Counter()
    stageable_documents = 0
    unmapped_documents = 0
    missing_live_headers = 0
    for number in sorted(snapshot_by):
        if number in pr_header_by:
            stage, _ = pr_live_stage(number)
            kind = "PR"
        elif number in po_header_by:
            stage, _ = po_live_stage(number)
            kind = "PO"
        else:
            missing_live_headers += 1
            continue
        if stage:
            stage_counts[f"{kind}|{stage}"] += 1
            stageable_documents += 1
            if stage == "Approval — unmapped element":
                unmapped_documents += 1

    def amount_summary(rows, column):
        return {
            "documentsCompared": len(rows),
            "workbookTotal": round(sum(float(row["workbook"].get(column) or 0) for row in rows), 2),
            "liveLineTotal": round(sum(float(row["live"].get("amount") or 0) for row in rows), 2),
            "exactDocumentMatches": sum(compare_amount(row["workbook"].get(column), row["live"].get("amount")) for row in rows),
        }

    output = {
        "generatedAt": generated.isoformat().replace("+00:00", "Z"),
        "readOnly": True,
        "sourceCounts": {
            "workbookPR": len(pr_book), "workbookPO": len(po_book),
            "livePRHeaders": len(pr_headers), "livePRLines": len(pr_lines), "livePRBiHeaders": len(pr_bi),
            "livePOHeaders": len(po_headers), "livePOLines": len(po_lines), "livePackingSlipJournals": len(packing),
            "captureSnapshots": len(snapshots), "captureCurrentWorkItems": len(workitems),
            "captureResolvedDistinctDocuments": len(resolved_current), "captureUnresolvedWorkItems": len(unresolved_items),
            "captureParallelDocuments": sum(1 for number in snapshot_by if int(snapshot_by[number].get("ssg_pendingapprovercount") or 0) > 1),
        },
        "freshness": {
            "datasetGeneratedUtc": generated.isoformat().replace("+00:00", "Z"),
            "fAndOReadUtc": generated.isoformat().replace("+00:00", "Z"),
            "approvalCaptureReconciledUtc": latest_capture.isoformat().replace("+00:00", "Z") if latest_capture else None,
            "effectiveDataTimeUtc": effective_data_time.isoformat().replace("+00:00", "Z"),
            "captureAgeMinutes": round((generated - latest_capture).total_seconds() / 60, 2) if latest_capture else None,
        },
        "liveDatasetNumbers": {
            "distinctResolvedDocuments": len(snapshot_by),
            "openWorkItems": len(workitems),
            "unresolvedApprovalWorkItems": len(unresolved_items),
            "parallelApprovalDocuments": sum(1 for number in snapshot_by if int(snapshot_by[number].get("ssg_pendingapprovercount") or 0) > 1),
            "documentsWithLiveHeader": len(snapshot_by) - missing_live_headers,
            "stageableDocuments": stageable_documents,
            "approvalUnmappedDocuments": unmapped_documents,
            "missingLiveHeaderDocuments": missing_live_headers,
            "stageCounts": dict(stage_counts),
        },
        "prInReviewSeparability": {
            "separable": not any(v["PR in review"] and (v["Sourcing"] or v["Priced"]) for v in review_elements.values()),
            "elementDistributions": review_elements,
        },
        "approvalElementMaps": {
            "prMapped": pr_approval_map, "prAmbiguous": pr_ambiguous,
            "poMapped": po_approval_map, "poAmbiguous": po_ambiguous,
        },
        "reconciliation": {
            "prStage": {
                "compared": len(pr_stage_rows),
                "matched": len(pr_stage_rows) - len(pr_stage_differences),
                "agreementPercent": round(100 * (len(pr_stage_rows) - len(pr_stage_differences)) / len(pr_stage_rows), 2) if pr_stage_rows else None,
                "differences": pr_stage_differences,
            },
            "prProcurementClock": {
                "compared": len(pr_clock_rows),
                "matchedWithinOneDay": len(pr_clock_rows) - len(pr_clock_differences),
                "agreementPercent": round(100 * (len(pr_clock_rows) - len(pr_clock_differences)) / len(pr_clock_rows), 2) if pr_clock_rows else None,
                "differences": pr_clock_differences,
            },
            "poStage": {
                "compared": len(po_stage_rows),
                "matched": len(po_stage_rows) - len(po_stage_differences),
                "agreementPercent": round(100 * (len(po_stage_rows) - len(po_stage_differences)) / len(po_stage_rows), 2) if po_stage_rows else None,
                "differences": po_stage_differences,
            },
            "approver": {"compared": sum(approver_classes.values()), "classifications": dict(approver_classes), "details": approver_details},
        },
        "columns": {"pr.xlsx": pr_columns, "po.xlsx": po_columns},
        "amountBasis": {"pr.xlsx": amount_summary(pr_rows, "Total amount"), "po.xlsx": amount_summary(po_rows, "Total amount")},
        "poWorkbookStepCounts": {str(key): int(value) for key, value in po_book["Step name"].fillna("(blank)").value_counts().items()},
    }
    # Deliberate cutover gate. Failure of either requested threshold prohibits deletion.
    output["verdict"] = {
        "stageThresholdPercent": 95,
        "clockThresholdPercent": 90,
        "prStagePassed": (output["reconciliation"]["prStage"]["agreementPercent"] or 0) >= 95,
        "prClockPassed": (output["reconciliation"]["prProcurementClock"]["agreementPercent"] or 0) >= 90,
        "prInReviewSeparable": output["prInReviewSeparability"]["separable"],
        "canRetireTotally": False,
    }
    text = json.dumps(output, indent=2, ensure_ascii=False, default=str) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(json.dumps({
        "sourceCounts": output["sourceCounts"],
        "freshness": output["freshness"],
        "prInReviewSeparability": output["prInReviewSeparability"],
        "prStage": {key: value for key, value in output["reconciliation"]["prStage"].items() if key != "differences"},
        "prProcurementClock": {key: value for key, value in output["reconciliation"]["prProcurementClock"].items() if key != "differences"},
        "poStage": {key: value for key, value in output["reconciliation"]["poStage"].items() if key != "differences"},
        "approver": {key: value for key, value in output["reconciliation"]["approver"].items() if key != "details"},
        "verdict": output["verdict"],
    }, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
