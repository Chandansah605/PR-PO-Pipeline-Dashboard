"""Correction 04 PO stage and clock reconciliation.

P1a proves the stage from authoritative F&O state or events. P1b reports the
clock separately and plans the one-time final-workbook seed without writing.
The actual seed is performed only after the safe-cutover pre-deploy proofs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

import reconcile_workbook_retirement as base


FO_STAGE_ORDER = {
    "Procurement": 0,
    "Finance": 1,
    "Director": 2,
    "CEO": 3,
    "Approval — unmapped element": 3,
    "Not yet sent": 4,
    "Sent to supplier": 5,
    "Receipt posted": 6,
    "Invoiced": 7,
}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fo_all(origin: str, token: str, entity: str, select: list[str]) -> list[dict]:
    params = {"cross-company": "true", "$select": ",".join(select)}
    url = f"{origin.rstrip('/')}/data/{entity}?{urllib.parse.urlencode(params)}"
    rows: list[dict] = []
    pages = 0
    while url:
        pages += 1
        if pages > 200:
            raise RuntimeError(f"F&O paging guard exceeded for {entity}")
        request = urllib.request.Request(
            url,
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=180) as response:
            payload = json.load(response)
        rows.extend(payload.get("value", []))
        url = payload.get("@odata.nextLink")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    fo_token = os.environ.get("PRPO_FO_TOKEN")
    fo_origin = os.environ.get("PRPO_FO_BASE")
    dev_token = os.environ.get("PRPO_DEV_TOKEN")
    if not fo_token or not fo_origin or not dev_token:
        raise SystemExit("PRPO_FO_TOKEN, PRPO_FO_BASE and PRPO_DEV_TOKEN are required")

    c2 = json.loads((args.repo / "evidence/workbook-retirement-correction-02.json").read_text(encoding="utf-8"))
    c3 = json.loads((args.repo / "evidence/workbook-retirement-correction-03.json").read_text(encoding="utf-8"))
    po_map = c2["approvalElementMaps"]["poMapped"]
    po_path = args.repo / "po.xlsx"
    po_book = pd.read_excel(po_path)
    po_book_by = {
        base.doc(row["Purchase order"]): row.to_dict()
        for _, row in po_book.iterrows()
    }

    headers = fo_all(fo_origin, fo_token, "PurchaseOrderHeadersV2", [
        "PurchaseOrderNumber", "PurchaseOrderStatus", "DocumentApprovalStatus",
        "dataAreaId", "AccountingDate", "OrderVendorAccountNumber",
    ])
    confirmations = fo_all(fo_origin, fo_token, "PurchaseOrderConfirmationHeaders", [
        "PurchaseOrderNumber", "ConfirmationDate", "ConfirmationNumber", "dataAreaId",
    ])
    packing = fo_all(fo_origin, fo_token, "VendPackingSlipJourBiEntities", [
        "PurchId", "PackingSlipId", "DocumentDate", "dataAreaId",
    ])
    invoices = fo_all(fo_origin, fo_token, "VendInvoiceJourBiEntities", [
        "PurchId", "InvoiceId", "InvoiceDate", "SysModifiedDateTime", "dataAreaId",
    ])
    snapshots = base.api_all(base.DEV, dev_token, "ssg_prpocurrentapprovalsnapshots", [
        "ssg_documentnumber", "ssg_documenttype", "ssg_pendingapprovercount",
        "ssg_pendingstepnames", "ssg_oldestpendingsince", "ssg_lastreconciledon",
    ])
    instances = base.api_all(base.DEV, dev_token, "ssg_prpoapprovalinstances", [
        "ssg_prpoapprovalinstanceid", "ssg_documentnumber", "ssg_documenttype",
        "ssg_lastreconciledon",
    ])
    workitems = base.api_all(base.DEV, dev_token, "ssg_prpoapprovalworkitems", [
        "_ssg_approvalinstance_value", "ssg_assignedon", "ssg_firstobservedon",
        "ssg_stepelementid", "ssg_lastobservedon",
    ], "ssg_iscurrent eq true")

    def entity_key(number, company) -> str:
        return f"{base.norm(company)}|{base.doc(number)}"

    header_groups: dict[str, list[dict]] = defaultdict(list)
    number_to_keys: dict[str, list[str]] = defaultdict(list)
    for row in headers:
        number = base.doc(row.get("PurchaseOrderNumber"))
        if not number:
            continue
        key = entity_key(number, row.get("dataAreaId"))
        header_groups[key].append(row)
        if key not in number_to_keys[number]:
            number_to_keys[number].append(key)
    header_by = {key: rows[0] for key, rows in header_groups.items()}

    def group_events(rows, number_field):
        grouped = defaultdict(list)
        for row in rows:
            grouped[entity_key(row.get(number_field), row.get("dataAreaId"))].append(row)
        return grouped

    confirmation_by = group_events(confirmations, "PurchaseOrderNumber")
    packing_by = group_events(packing, "PurchId")
    invoice_by = group_events(invoices, "PurchId")

    instance_by = {row["ssg_prpoapprovalinstanceid"]: row for row in instances}
    capture_by: dict[str, list[dict]] = defaultdict(list)
    for item in workitems:
        instance = instance_by.get(item.get("_ssg_approvalinstance_value"), {})
        if base.norm(instance.get("ssg_documenttype")) != "po":
            continue
        number = base.doc(instance.get("ssg_documentnumber"))
        if number and not number.startswith("UNRESOLVED-"):
            capture_by[number].append(item)
    snapshot_by = {}
    for row in snapshots:
        number = base.doc(row.get("ssg_documentnumber"))
        if (base.norm(row.get("ssg_documenttype")) == "po" and number
                and int(row.get("ssg_pendingapprovercount") or 0) > 0
                and not number.startswith("UNRESOLVED-")):
            snapshot_by[number] = row

    def capture_stage(number: str) -> tuple[str | None, list[str]]:
        if len(number_to_keys.get(number, [])) != 1:
            return None, ["CAPTURE_LEGAL_ENTITY_UNRESOLVED"] if number in snapshot_by else []
        value = base.clean(snapshot_by.get(number, {}).get("ssg_pendingstepnames")) or ""
        elements = {match.group(0).casefold() for match in base.GUID_RE.finditer(value)}
        if not elements:
            elements = {
                base.norm(item.get("ssg_stepelementid"))
                for item in capture_by.get(number, [])
                if base.clean(item.get("ssg_stepelementid"))
            }
        stages = {po_map[element] for element in elements if element in po_map}
        if len(stages) > 1:
            return None, ["CONTRADICTORY_APPROVAL_STAGES"]
        if stages:
            return next(iter(stages)), []
        if number in snapshot_by or capture_by.get(number):
            return "Approval — unmapped element", ["UNMAPPED_APPROVAL_ELEMENT"]
        return None, []

    def is_open(header: dict) -> bool:
        status = base.norm(header.get("PurchaseOrderStatus"))
        approval = base.norm(header.get("DocumentApprovalStatus"))
        return status not in {"invoiced", "closed", "cancelled", "canceled"} and approval != "rejected"

    def lifecycle(key: str) -> tuple[str | None, list[str]]:
        header = header_by[key]
        number = base.doc(header.get("PurchaseOrderNumber"))
        status = base.norm(header.get("PurchaseOrderStatus"))
        approval = base.norm(header.get("DocumentApprovalStatus"))
        captured, flags = capture_stage(number)
        if flags and "CONTRADICTORY_APPROVAL_STAGES" in flags:
            return None, flags
        if captured:
            return captured, flags
        # A posted invoice can be partial. Only the order's own terminal status
        # moves the whole PO to Invoiced; the journal supplies its clock.
        if status == "invoiced":
            return "Invoiced", flags
        if status == "received" or packing_by.get(key):
            return "Receipt posted", flags
        if approval == "confirmed" and status in {"backorder", "open order"}:
            return "Sent to supplier", flags
        if status in {"backorder", "open order"} and approval in {"draft", "approved", "in review", "inreview"}:
            return "Not yet sent", flags
        if not status or not approval:
            return None, flags + ["F_AND_O_STATUS_MISSING"]
        return None, flags + ["F_AND_O_STATUS_CONTRADICTORY"]

    def evidence(key: str, stage: str | None) -> tuple[str | None, datetime | None]:
        number = base.doc(header_by[key].get("PurchaseOrderNumber"))
        if stage in set(base.PO_APPROVAL.values()) | {"Approval — unmapped element"}:
            dates = [snapshot_by.get(number, {}).get("ssg_oldestpendingsince")]
            dates.extend(item.get("ssg_assignedon") or item.get("ssg_firstobservedon") for item in capture_by.get(number, []))
            return "approval capture assignment", base.earliest(dates)
        if stage == "Sent to supplier":
            return "PO confirmation", base.earliest(row.get("ConfirmationDate") for row in confirmation_by.get(key, []))
        if stage == "Receipt posted":
            return "posted packing slip", base.earliest(row.get("DocumentDate") for row in packing_by.get(key, []))
        if stage == "Invoiced":
            return "posted vendor invoice", base.earliest(
                row.get("SysModifiedDateTime") or row.get("InvoiceDate") for row in invoice_by.get(key, [])
            )
        return None, None

    def resolve_workbook_key(number: str, workbook: dict) -> tuple[str | None, str]:
        candidates = list(number_to_keys.get(number, []))
        if not candidates:
            return None, "WORKBOOK_PO_NOT_IN_F_AND_O"
        if len(candidates) == 1:
            return candidates[0], "UNIQUE_DOCUMENT_NUMBER"
        vendor = base.norm(workbook.get("Vendor account"))
        vendor_matches = [
            key for key in candidates
            if base.norm(header_by[key].get("OrderVendorAccountNumber")) == vendor
        ]
        if len(vendor_matches) == 1:
            return vendor_matches[0], "DOCUMENT_AND_VENDOR"
        workbook_status = base.norm(workbook.get("Purchase order status"))
        workbook_approval = base.norm(workbook.get("Approval status"))
        status_aliases = {"open order": "backorder"}
        workbook_status = status_aliases.get(workbook_status, workbook_status)
        status_matches = [
            key for key in (vendor_matches or candidates)
            if base.norm(header_by[key].get("PurchaseOrderStatus")) == workbook_status
            and base.norm(header_by[key].get("DocumentApprovalStatus")) == workbook_approval.replace(" ", "")
        ]
        if len(status_matches) == 1:
            return status_matches[0], "DOCUMENT_VENDOR_AND_STATUS"
        return None, "WORKBOOK_LEGAL_ENTITY_AMBIGUOUS"

    workbook_key_by = {}
    for number, workbook in po_book_by.items():
        key, resolution = resolve_workbook_key(number, workbook)
        if key:
            workbook_key_by[key] = (workbook, resolution)

    model = {}
    for key, header in sorted(header_by.items()):
        stage, flags = lifecycle(key)
        event_name, event_at = evidence(key, stage)
        model[key] = {
            "key": key,
            "document": base.doc(header.get("PurchaseOrderNumber")),
            "legalEntity": base.clean(header.get("dataAreaId")),
            "fAndOStatus": base.clean(header.get("PurchaseOrderStatus")),
            "fAndOApprovalStatus": base.clean(header.get("DocumentApprovalStatus")),
            "liveStage": stage or "STAGE_NOT_EVIDENCED",
            "stageReasonCode": "AUTHORITATIVE_F_AND_O_STAGE" if stage else "STAGE_NOT_EVIDENCED",
            "event": event_name,
            "eventTimestamp": base.iso(event_at),
            "flags": flags,
        }

    f_and_o_open = {key for key, header in header_by.items() if is_open(header)}
    live_open = {key: model[key] for key in f_and_o_open}
    p1a_differences = [row for row in live_open.values() if row["liveStage"] == "STAGE_NOT_EVIDENCED"]
    p1a_differences.sort(key=lambda row: (base.norm(row["legalEntity"]), row["document"]))
    p1a = {
        "targetPercent": 100,
        "population": len(live_open),
        "staged": len(live_open) - len(p1a_differences),
        "agreementPercent": round(100 * (len(live_open) - len(p1a_differences)) / len(live_open), 2),
        "stageDistribution": dict(sorted(Counter(row["liveStage"] for row in live_open.values()).items())),
        "passed": not p1a_differences,
        "differences": p1a_differences,
    }

    p1b_rows = []
    for key, row in sorted(live_open.items()):
        if row["eventTimestamp"]:
            provenance = "LIVE_EVENT_DATE"
            clock = row["eventTimestamp"]
            label = "since"
            workbook_value = None
        else:
            workbook, resolution = workbook_key_by.get(key, ({}, "NO_WORKBOOK_MATCH"))
            workbook_value = base.clean(workbook.get("Step date and time"))
            seed = base.parse_dt(workbook_value)
            if seed:
                provenance = "SEEDED_FROM_FINAL_WORKBOOK"
                clock = base.iso(seed)
                label = "since (from last export)"
            else:
                provenance = "NOT_RECORDED"
                clock = None
                label = "since — not recorded"
            row = {**row, "workbookJoin": resolution}
        p1b_rows.append({
            **row,
            "clockTimestamp": clock,
            "clockProvenance": provenance,
            "clockLabel": label,
            "workbookValue": str(workbook_value) if workbook_value is not None else None,
            "workbookExportTimestamp": base.iso(base.WORKBOOK_EXPORT_CUTOFF) if provenance == "SEEDED_FROM_FINAL_WORKBOOK" else None,
        })
    p1b_counts = Counter(row["clockProvenance"] for row in p1b_rows)
    p1b = {
        "gated": False,
        "population": len(p1b_rows),
        "liveDated": p1b_counts["LIVE_EVENT_DATE"],
        "seededFromFinalWorkbook": p1b_counts["SEEDED_FROM_FINAL_WORKBOOK"],
        "notRecorded": p1b_counts["NOT_RECORDED"],
        "rows": p1b_rows,
    }

    duplicate_headers = sorted(key for key, rows in header_groups.items() if len(rows) > 1)
    candidate_open = set(live_open)
    p2_differences = (
        [{"key": key, "reasonCode": "F_AND_O_OPEN_MISSING_FROM_LIVE"} for key in sorted(f_and_o_open - candidate_open)]
        + [{"key": key, "reasonCode": "NON_OPEN_PO_IN_LIVE_POPULATION"} for key in sorted(candidate_open - f_and_o_open)]
        + [{"key": key, "reasonCode": "DUPLICATE_F_AND_O_HEADER_KEY"} for key in duplicate_headers]
    )
    p2 = {
        "targetPercent": 100,
        "fAndOOpenDistinctDocuments": len(f_and_o_open),
        "liveOpenDistinctDocuments": len(candidate_open),
        "matchedDistinctDocuments": len(f_and_o_open & candidate_open),
        "agreementPercent": round(100 * len(f_and_o_open & candidate_open) / len(f_and_o_open), 2),
        "passed": not p2_differences and candidate_open == f_and_o_open,
        "differences": p2_differences,
    }

    capture_dates = [base.parse_dt(row.get("ssg_lastreconciledon")) for row in snapshots + instances]
    capture_dates += [base.parse_dt(row.get("ssg_lastobservedon")) for row in workitems]
    capture_dates = [value for value in capture_dates if value]
    generated = datetime.now(timezone.utc)
    settled = {
        "prStage": c2["reconciliation"]["prStage"],
        "prProcurementClock": c2["reconciliation"]["prProcurementClock"],
        "prAmount": c2["amountBasis"]["pr.xlsx"],
        "poAmount": c2["amountBasis"]["po.xlsx"],
        "distinctDocumentCountsExact": c2["verdict"]["distinctDocumentCountsExact"],
    }
    output = {
        "generatedAt": base.iso(generated),
        "readOnly": True,
        "workbook": {
            "path": "po.xlsx", "sha256": file_sha256(po_path), "rows": len(po_book),
            "exportTimestamp": base.iso(base.WORKBOOK_EXPORT_CUTOFF),
        },
        "sourceCounts": {
            "fAndOPOHeaders": len(headers), "fAndOOpenPOs": len(f_and_o_open),
            "fAndOConfirmations": len(confirmations), "fAndOPackingSlips": len(packing),
            "fAndOVendorInvoices": len(invoices), "capturePOSnapshots": len(snapshot_by),
            "capturePOCurrentWorkItems": sum(len(rows) for rows in capture_by.values()),
        },
        "freshness": {
            "fAndOReadUtc": base.iso(generated),
            "approvalCaptureReconciledUtc": base.iso(max(capture_dates) if capture_dates else None),
        },
        "settledCorrection02Gates": settled,
        "stalePopulationLane": c3["stalePopulationLane"],
        "poAcceptance": {
            "p1a": p1a,
            "p1b": p1b,
            "p2": p2,
            "p3": {"status": "RETIRED_BY_CORRECTION_04"},
            "p4": c3["poAcceptance"]["p4"],
            "p5": c3["poAcceptance"]["p5"],
        },
    }
    verdict = {
        "prStagePassed": c2["verdict"]["prStagePassed"],
        "prClockPassed": c2["verdict"]["prClockPassed"],
        "prAmountPassed": c2["verdict"]["prAmountPassed"],
        "poAmountPassed": c2["verdict"]["poAmountPassed"],
        "distinctDocumentCountsExact": c2["verdict"]["distinctDocumentCountsExact"],
        "p1aPassed": p1a["passed"], "p2Passed": p2["passed"],
        "p1bReported": sum(p1b_counts.values()) == len(p1b_rows),
        "p4BusinessCaseCount": c3["poAcceptance"]["p4"]["receivedOrInvoicedBusinessCaseCount"],
        "p5SampleComplete": c3["poAcceptance"]["p5"]["passed"],
    }
    verdict["canRetireTotally"] = all([
        verdict["prStagePassed"], verdict["prClockPassed"], verdict["prAmountPassed"],
        verdict["poAmountPassed"], verdict["distinctDocumentCountsExact"],
        verdict["p1aPassed"], verdict["p2Passed"],
    ])
    output["verdict"] = verdict

    text = json.dumps(output, indent=2, ensure_ascii=False, default=str) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(json.dumps({
        "generatedAt": output["generatedAt"], "sourceCounts": output["sourceCounts"],
        "p1a": {key: value for key, value in p1a.items() if key != "differences"},
        "p1b": {key: value for key, value in p1b.items() if key != "rows"},
        "p2": {key: value for key, value in p2.items() if key != "differences"},
        "verdict": verdict,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
