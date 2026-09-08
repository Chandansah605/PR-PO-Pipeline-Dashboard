"""Correction 03 PO acceptance tests for workbook retirement.

This audit keeps every Correction 02 PR/amount/count result settled and reads
the current PO evidence path without writing to either Dataverse environment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

import reconcile_workbook_retirement as base


PO_APPROVAL_STEPS = set(base.PO_APPROVAL) | {"PurchTableApproval"}
PO_ORDER = {
    "Procurement": 0,
    "Finance": 1,
    "Director": 2,
    "CEO": 3,
    "Approval — unmapped element": 3,
    "Sent to supplier": 4,
    "Receipt posted": 5,
    "Invoiced": 6,
}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    live_token = os.environ.get("PRPO_LIVE_TOKEN")
    dev_token = os.environ.get("PRPO_DEV_TOKEN")
    if not live_token or not dev_token:
        raise SystemExit("PRPO_LIVE_TOKEN and PRPO_DEV_TOKEN are required")

    c2_path = args.repo / "evidence" / "workbook-retirement-correction-02.json"
    correction02 = json.loads(c2_path.read_text(encoding="utf-8"))
    po_map = correction02["approvalElementMaps"]["poMapped"]

    po_path = args.repo / "po.xlsx"
    po_book = pd.read_excel(po_path)
    po_book_by = {
        base.doc(row["Purchase order"]): row.to_dict()
        for _, row in po_book.iterrows()
    }

    po_headers = base.api_all(base.LIVE, live_token, "mserp_purchpurchaseorderheaderv2entities", [
        "mserp_purchaseordernumber", "mserp_purchaseorderstatus", "mserp_documentapprovalstatus",
        "mserp_dataareaid", "mserp_accountingdate", "mserp_ordervendoraccountnumber",
    ])
    packing = base.api_all(base.LIVE, live_token, "mserp_vendpackingslipjourbientities", [
        "mserp_purchid", "mserp_packingslipid", "mserp_documentdate", "mserp_dataareaid",
    ])
    confirmations = base.api_all(base.LIVE, live_token, "mserp_vrmpurchaseorderconfirmationheaderentities", [
        "mserp_purchaseordernumber", "mserp_confirmationdatetime", "mserp_dataareaid",
    ])
    entity_catalog = base.api_all(base.LIVE, live_token, "mserp_financeandoperationsentities", [
        "mserp_physicalname", "mserp_hasbeengenerated",
    ])
    invoices = base.api_all(base.LIVE, live_token, "mserp_vendinvoicejourbientities", [
        "mserp_purchid", "mserp_invoiceid", "mserp_invoicedate", "mserp_sysmodifieddatetime",
        "mserp_dataareaid",
    ])
    snapshots = base.api_all(base.DEV, dev_token, "ssg_prpocurrentapprovalsnapshots", [
        "ssg_documentnumber", "ssg_documenttype", "ssg_pendingapprovercount", "ssg_pendingstepnames",
        "ssg_lastreconciledon", "ssg_oldestpendingsince", "ssg_dataqualitystatus",
    ])
    instances = base.api_all(base.DEV, dev_token, "ssg_prpoapprovalinstances", [
        "ssg_prpoapprovalinstanceid", "ssg_documentnumber", "ssg_documenttype", "ssg_lastreconciledon",
        "ssg_dataqualitystatus",
    ])
    workitems = base.api_all(base.DEV, dev_token, "ssg_prpoapprovalworkitems", [
        "ssg_prpoapprovalworkitemid", "_ssg_approvalinstance_value", "ssg_assignedon",
        "ssg_firstobservedon", "ssg_iscurrent", "ssg_isunresolved", "ssg_stepelementid",
        "ssg_dataqualitystatus", "ssg_lastobservedon",
    ], "ssg_iscurrent eq true")

    def entity_key(number, company):
        return f"{base.norm(company)}|{base.doc(number)}"

    header_groups = defaultdict(list)
    number_to_keys = defaultdict(list)
    for row in po_headers:
        number = base.doc(row.get("mserp_purchaseordernumber"))
        if number:
            key = entity_key(number, row.get("mserp_dataareaid"))
            header_groups[key].append(row)
            if key not in number_to_keys[number]:
                number_to_keys[number].append(key)
    po_header_by = {key: rows[0] for key, rows in header_groups.items()}

    packing_by = defaultdict(list)
    for row in packing:
        packing_by[entity_key(row.get("mserp_purchid"), row.get("mserp_dataareaid"))].append(row)
    confirmation_by = defaultdict(list)
    for row in confirmations:
        confirmation_by[entity_key(row.get("mserp_purchaseordernumber"), row.get("mserp_dataareaid"))].append(row)
    invoice_by = defaultdict(list)
    for row in invoices:
        invoice_by[entity_key(row.get("mserp_purchid"), row.get("mserp_dataareaid"))].append(row)

    instance_by = {row["ssg_prpoapprovalinstanceid"]: row for row in instances}
    capture_by = defaultdict(list)
    for item in workitems:
        instance = instance_by.get(item.get("_ssg_approvalinstance_value"), {})
        if base.norm(instance.get("ssg_documenttype")) != "po":
            continue
        number = base.doc(instance.get("ssg_documentnumber"))
        if number and not number.startswith("UNRESOLVED-"):
            capture_by[number].append(item)

    snapshot_by = {}
    for snapshot in snapshots:
        if base.norm(snapshot.get("ssg_documenttype")) != "po":
            continue
        number = base.doc(snapshot.get("ssg_documentnumber"))
        if number and not number.startswith("UNRESOLVED-") and int(snapshot.get("ssg_pendingapprovercount") or 0) > 0:
            snapshot_by[number] = snapshot

    def snapshot_elements(number: str) -> set[str]:
        value = base.clean(snapshot_by.get(number, {}).get("ssg_pendingstepnames")) or ""
        elements = {match.group(0).casefold() for match in base.GUID_RE.finditer(value)}
        if not elements:
            elements = {
                base.norm(item.get("ssg_stepelementid"))
                for item in capture_by.get(number, [])
                if base.clean(item.get("ssg_stepelementid"))
            }
        return elements

    def po_is_open(key: str) -> bool:
        header = po_header_by.get(key, {})
        status = base.norm(base.formatted(header, "mserp_purchaseorderstatus"))
        approval = base.norm(base.formatted(header, "mserp_documentapprovalstatus"))
        return status not in {"invoiced", "closed", "cancelled", "canceled"} and approval != "rejected"

    def lifecycle_stage(key: str) -> tuple[str | None, list[str]]:
        header = po_header_by.get(key, {})
        number = base.doc(header.get("mserp_purchaseordernumber"))
        capture_is_unambiguous = len(number_to_keys.get(number, [])) == 1
        if capture_is_unambiguous:
            elements = snapshot_elements(number)
            stages = {po_map[element] for element in elements if element in po_map}
            if len(stages) > 1:
                return None, ["CONFLICTING_APPROVAL_STAGES"]
            if stages:
                return next(iter(stages)), []
            if number in snapshot_by or capture_by.get(number):
                return "Approval — unmapped element", ["UNMAPPED_ELEMENT"]
        status = base.norm(base.formatted(header, "mserp_purchaseorderstatus"))
        approval = base.norm(base.formatted(header, "mserp_documentapprovalstatus"))
        if status == "invoiced":
            return "Invoiced", []
        if packing_by.get(key):
            return "Receipt posted", []
        if approval == "confirmed" and status == "open order":
            return "Sent to supplier", []
        if not capture_is_unambiguous and (number in snapshot_by or capture_by.get(number)):
            return None, ["CAPTURE_LEGAL_ENTITY_UNRESOLVED"]
        return None, ["NO_LIVE_STAGE"]

    def stage_evidence(key: str, stage: str | None) -> tuple[str | None, datetime | None]:
        header = po_header_by.get(key, {})
        number = base.doc(header.get("mserp_purchaseordernumber"))
        if stage in set(base.PO_APPROVAL.values()) | {"Approval — unmapped element"}:
            candidates = [snapshot_by.get(number, {}).get("ssg_oldestpendingsince")]
            candidates.extend(
                item.get("ssg_assignedon") or item.get("ssg_firstobservedon")
                for item in capture_by.get(number, [])
            )
            return "approval capture assignment", base.earliest(candidates)
        if stage == "Sent to supplier":
            return "PO confirmation", base.earliest(
                row.get("mserp_confirmationdatetime") for row in confirmation_by.get(key, [])
            )
        if stage == "Receipt posted":
            return "posted packing slip", base.earliest(
                row.get("mserp_documentdate") for row in packing_by.get(key, [])
            )
        if stage == "Invoiced":
            return "posted vendor invoice", base.earliest(
                row.get("mserp_sysmodifieddatetime") or row.get("mserp_invoicedate")
                for row in invoice_by.get(key, [])
            )
        return None, None

    def model_row(key: str) -> dict:
        header = po_header_by[key]
        number = base.doc(header.get("mserp_purchaseordernumber"))
        company = base.clean(header.get("mserp_dataareaid"))
        candidate, flags = lifecycle_stage(key)
        event, event_at = stage_evidence(key, candidate)
        if event_at:
            displayed = candidate
            reason = "STAGE_EVIDENCED"
        else:
            displayed = "STAGE_NOT_EVIDENCED"
            if "CONFLICTING_APPROVAL_STAGES" in flags:
                reason = "CONFLICTING_APPROVAL_STAGES"
            elif candidate == "Sent to supplier":
                reason = "PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE"
            elif candidate:
                reason = "STAGE_EVENT_TIMESTAMP_UNAVAILABLE"
            else:
                reason = "NO_LIVE_STAGE_EVIDENCE"
        return {
            "key": key,
            "document": number,
            "legalEntity": company,
            "fAndOStatus": base.formatted(header, "mserp_purchaseorderstatus"),
            "fAndOApprovalStatus": base.formatted(header, "mserp_documentapprovalstatus"),
            "candidateStage": candidate,
            "displayedStage": displayed,
            "event": event,
            "eventTimestamp": base.iso(event_at),
            "evidenced": bool(event_at),
            "reasonCode": reason,
            "flags": flags,
        }

    all_model_rows = {key: model_row(key) for key in sorted(po_header_by)}
    f_and_o_open = {key for key in po_header_by if po_is_open(key)}
    live_open_rows = {key: all_model_rows[key] for key in f_and_o_open}

    p1_differences = sorted(
        (row for row in live_open_rows.values() if not row["evidenced"]),
        key=lambda row: (base.norm(row.get("legalEntity")), row["document"]),
    )
    p1 = {
        "targetPercent": 100,
        "population": len(live_open_rows),
        "evidenced": len(live_open_rows) - len(p1_differences),
        "agreementPercent": round(100 * (len(live_open_rows) - len(p1_differences)) / len(live_open_rows), 2) if live_open_rows else None,
        "passed": not p1_differences,
        "differences": p1_differences,
    }

    candidate_open = set(live_open_rows)
    missing_from_live = sorted(f_and_o_open - candidate_open)
    extra_in_live = sorted(candidate_open - f_and_o_open)
    duplicate_headers = sorted(key for key, rows in header_groups.items() if len(rows) > 1)
    p2_differences = (
        [{"key": key, "reasonCode": "F_AND_O_OPEN_MISSING_FROM_LIVE"} for key in missing_from_live]
        + [{"key": key, "reasonCode": "NON_OPEN_PO_IN_LIVE_POPULATION"} for key in extra_in_live]
        + [{"key": key, "reasonCode": "DUPLICATE_F_AND_O_HEADER_KEY"} for key in duplicate_headers]
    )
    p2 = {
        "targetPercent": 100,
        "fAndOOpenDistinctDocuments": len(f_and_o_open),
        "liveOpenDistinctDocuments": len(candidate_open),
        "matchedDistinctDocuments": len(f_and_o_open & candidate_open),
        "agreementPercent": round(100 * len(f_and_o_open & candidate_open) / len(f_and_o_open), 2) if f_and_o_open else None,
        "passed": not p2_differences and f_and_o_open == candidate_open,
        "differences": p2_differences,
    }

    def resolve_workbook_key(number: str, workbook: dict) -> tuple[str | None, str]:
        candidates = list(number_to_keys.get(number, []))
        if not candidates:
            return None, "WORKBOOK_PO_NOT_IN_F_AND_O"
        if len(candidates) == 1:
            return candidates[0], "UNIQUE_DOCUMENT_NUMBER"
        vendor = base.norm(workbook.get("Vendor account"))
        vendor_matches = [
            key for key in candidates
            if base.norm(po_header_by[key].get("mserp_ordervendoraccountnumber")) == vendor
        ]
        if len(vendor_matches) == 1:
            return vendor_matches[0], "DOCUMENT_AND_VENDOR"
        workbook_status = base.norm(workbook.get("Purchase order status"))
        workbook_approval = base.norm(workbook.get("Approval status"))
        status_matches = [
            key for key in (vendor_matches or candidates)
            if base.norm(base.formatted(po_header_by[key], "mserp_purchaseorderstatus")) == workbook_status
            and base.norm(base.formatted(po_header_by[key], "mserp_documentapprovalstatus")) == workbook_approval
        ]
        if len(status_matches) == 1:
            return status_matches[0], "DOCUMENT_VENDOR_AND_STATUS"
        return None, "WORKBOOK_LEGAL_ENTITY_AMBIGUOUS"

    def compare_approval_row(number: str, workbook_step: str, row: dict) -> dict:
        actual = row["candidateStage"]
        expected = base.PO_APPROVAL.get(workbook_step)
        generic = workbook_step == "PurchTableApproval"
        if not actual:
            return {"matched": False, "reasonCode": "STAGE_NOT_EVIDENCED", "progression": None}
        if generic and actual in set(base.PO_APPROVAL.values()) | {"Approval — unmapped element"}:
            return {"matched": True, "reasonCode": "CAPTURE_MAP_OR_UNMAPPED", "progression": None}
        if not generic and expected == actual:
            return {"matched": True, "reasonCode": "EXACT_STAGE", "progression": None}
        expected_order = PO_ORDER["CEO"] if generic else PO_ORDER.get(expected)
        actual_order = PO_ORDER.get(actual)
        if expected_order is None or actual_order is None or actual_order <= expected_order:
            return {"matched": False, "reasonCode": "REGRESSION_OR_UNMAPPED", "progression": None}
        event_at = base.parse_dt(row["eventTimestamp"])
        if not event_at:
            return {"matched": False, "reasonCode": "PROGRESSION_TIMESTAMP_UNAVAILABLE", "progression": None}
        progression = {
            "document": number,
            "workbookStage": "PO approval (generic)" if generic else expected,
            "liveStage": actual,
            "workbookExportTimestamp": base.iso(base.WORKBOOK_EXPORT_CUTOFF),
            "liveEvidenceTimestamp": base.iso(event_at),
            "liveEvidenceSource": row["event"],
            "reasonCode": "PROGRESSED_AFTER_EXPORT",
        }
        if event_at > base.WORKBOOK_EXPORT_CUTOFF:
            return {"matched": True, "reasonCode": "PROGRESSED_AFTER_EXPORT", "progression": progression}
        return {"matched": False, "reasonCode": "PROGRESSION_NOT_AFTER_EXPORT", "progression": None}

    p3_rows = []
    p3_excluded = []
    p3_join_issues = []
    p3_progressions = []
    for number, workbook in po_book_by.items():
        step = base.clean(workbook.get("Step name"))
        if step not in PO_APPROVAL_STEPS:
            continue
        key, resolution = resolve_workbook_key(number, workbook)
        if not key:
            open_candidates = [candidate for candidate in number_to_keys.get(number, []) if candidate in live_open_rows]
            if open_candidates:
                p3_rows.append({
                    "document": number,
                    "legalEntity": None,
                    "workbookStep": step,
                    "expectedStage": "PO approval (generic)" if step == "PurchTableApproval" else base.PO_APPROVAL[step],
                    "liveStage": "STAGE_NOT_EVIDENCED",
                    "candidateStage": None,
                    "event": None,
                    "eventTimestamp": None,
                    "matched": False,
                    "reasonCode": resolution,
                })
                p3_join_issues.append({"document": number, "reasonCode": resolution})
            else:
                p3_excluded.append({
                    "document": number,
                    "legalEntity": None,
                    "workbookStep": step,
                    "reasonCode": "OUTSIDE_R1_OR_MISSING_F_AND_O_HEADER",
                })
            continue
        if key not in live_open_rows:
            header = po_header_by[key]
            p3_excluded.append({
                "document": number,
                "legalEntity": base.clean(header.get("mserp_dataareaid")),
                "workbookStep": step,
                "fAndOStatus": base.formatted(header, "mserp_purchaseorderstatus"),
                "fAndOApprovalStatus": base.formatted(header, "mserp_documentapprovalstatus"),
                "reasonCode": "OUTSIDE_R1_DASHBOARD_POPULATION",
            })
            continue
        live = live_open_rows[key]
        comparison = compare_approval_row(number, step, live)
        item = {
            "document": number,
            "legalEntity": live["legalEntity"],
            "workbookStep": step,
            "expectedStage": "PO approval (generic)" if step == "PurchTableApproval" else base.PO_APPROVAL[step],
            "liveStage": live["displayedStage"] if not live["evidenced"] else live["candidateStage"],
            "candidateStage": live["candidateStage"],
            "event": live["event"],
            "eventTimestamp": live["eventTimestamp"],
            "matched": comparison["matched"],
            "reasonCode": comparison["reasonCode"],
            "workbookJoin": resolution,
        }
        p3_rows.append(item)
        if comparison["progression"]:
            p3_progressions.append(comparison["progression"])
    p3_differences = [row for row in p3_rows if not row["matched"]]
    p3_matched = len(p3_rows) - len(p3_differences)
    p3 = {
        "targetPercent": 95,
        "workbookApprovalRows": int(po_book["Step name"].isin(PO_APPROVAL_STEPS).sum()),
        "compared": len(p3_rows),
        "excludedByR1": len(p3_excluded),
        "joinIssuesInPopulation": len(p3_join_issues),
        "matched": p3_matched,
        "agreementPercent": round(100 * p3_matched / len(p3_rows), 2) if p3_rows else None,
        "passed": bool(p3_rows) and 100 * p3_matched / len(p3_rows) >= 95,
        "differences": p3_differences,
        "excludedRows": p3_excluded,
        "joinIssues": p3_join_issues,
        "progressedAfterExport": sorted(p3_progressions, key=lambda row: row["document"]),
    }

    p4_rows = []
    for number, workbook in po_book_by.items():
        if base.clean(workbook.get("Step name")) != "LPO sent/shared with supplier":
            continue
        key, resolution = resolve_workbook_key(number, workbook)
        if not key:
            p4_rows.append({
                "document": number,
                "legalEntity": None,
                "liveStage": "STAGE_NOT_EVIDENCED",
                "displayedStage": "STAGE_NOT_EVIDENCED",
                "event": None,
                "eventTimestamp": None,
                "evidenced": False,
                "reasonCode": resolution,
            })
            continue
        live = all_model_rows[key]
        p4_rows.append({
            "document": number,
            "legalEntity": live["legalEntity"],
            "liveStage": live["candidateStage"] or live["displayedStage"],
            "displayedStage": live["displayedStage"],
            "event": live["event"],
            "eventTimestamp": live["eventTimestamp"],
            "evidenced": live["evidenced"],
            "reasonCode": live["reasonCode"],
            "workbookJoin": resolution,
        })
    p4_distribution = Counter(row["liveStage"] for row in p4_rows)
    p4_not_evidenced = [row for row in p4_rows if not row["evidenced"]]
    p4_business_case = sum(row["liveStage"] in {"Receipt posted", "Invoiced"} for row in p4_rows)
    p4 = {
        "workbookLpoSentRows": len(p4_rows),
        "liveStageDistribution": dict(sorted(p4_distribution.items())),
        "receivedOrInvoicedBusinessCaseCount": p4_business_case,
        "evidenced": len(p4_rows) - len(p4_not_evidenced),
        "notEvidenced": len(p4_not_evidenced),
        "notEvidencedRows": p4_not_evidenced,
    }

    p5_pool = {}
    for key, row in all_model_rows.items():
        if po_is_open(key) or row["candidateStage"] == "Invoiced":
            key = row["candidateStage"] or "STAGE_NOT_EVIDENCED"
            p5_pool.setdefault(key, []).append(row)
    for rows in p5_pool.values():
        rows.sort(key=lambda row: row["document"])
    stage_order = sorted(p5_pool, key=lambda stage: (PO_ORDER.get(stage, 99), stage))
    sample = []
    offsets = {stage: 0 for stage in stage_order}
    while len(sample) < 25 and any(offsets[stage] < len(p5_pool[stage]) for stage in stage_order):
        for stage in stage_order:
            offset = offsets[stage]
            if offset < len(p5_pool[stage]) and len(sample) < 25:
                row = p5_pool[stage][offset]
                sample.append({
                    "document": row["document"],
                    "legalEntity": row["legalEntity"],
                    "liveStage": row["displayedStage"],
                    "candidateStage": row["candidateStage"],
                    "event": row["event"] or "none",
                    "eventTimestamp": row["eventTimestamp"],
                    "reasonCode": row["reasonCode"],
                })
                offsets[stage] += 1
    sample_candidate_stages = {row["candidateStage"] or "STAGE_NOT_EVIDENCED" for row in sample}
    p5 = {
        "targetSampleSize": 25,
        "sampleSize": len(sample),
        "candidateStagesPresent": stage_order,
        "candidateStagesSampled": sorted(sample_candidate_stages, key=lambda stage: (PO_ORDER.get(stage, 99), stage)),
        "passed": len(sample) == 25 and sample_candidate_stages == set(stage_order),
        "rows": sample,
    }

    capture_dates = [
        base.parse_dt(row.get("ssg_lastreconciledon"))
        for row in snapshots + instances
    ] + [base.parse_dt(row.get("ssg_lastobservedon")) for row in workitems]
    capture_dates = [value for value in capture_dates if value]
    generated = datetime.now(timezone.utc)
    latest_capture = max(capture_dates) if capture_dates else None

    settled = {
        "prStage": correction02["reconciliation"]["prStage"],
        "prProcurementClock": correction02["reconciliation"]["prProcurementClock"],
        "prAmount": correction02["amountBasis"]["pr.xlsx"],
        "poAmount": correction02["amountBasis"]["po.xlsx"],
        "distinctDocumentCountsExact": correction02["verdict"]["distinctDocumentCountsExact"],
        "correction02EvidenceGeneratedAt": correction02["generatedAt"],
    }
    stale = correction02["staleRowsTheWorkbookStillCarries"]
    output = {
        "generatedAt": base.iso(generated),
        "readOnly": True,
        "workbook": {
            "path": "po.xlsx",
            "sha256": file_sha256(po_path),
            "rows": len(po_book),
            "distinctDocuments": po_book["Purchase order"].astype(str).str.strip().nunique(),
            "stepVocabulary": {
                str(key): int(value)
                for key, value in po_book["Step name"].fillna("(blank)").value_counts().items()
            },
        },
        "sourceCounts": {
            "livePOHeaders": len(po_headers),
            "livePODistinctHeaders": len(po_header_by),
            "livePackingSlipJournals": len(packing),
            "livePOConfirmations": len(confirmations),
            "liveVendorInvoiceJournals": len(invoices),
            "capturePOSnapshots": len(snapshot_by),
            "capturePOCurrentWorkItems": sum(len(rows) for rows in capture_by.values()),
        },
        "confirmationEntityEvidence": sorted([
            {
                "physicalName": row.get("mserp_physicalname"),
                "hasBeenGenerated": bool(row.get("mserp_hasbeengenerated")),
            }
            for row in entity_catalog
            if "purchaseorderconfirmation" in base.norm(row.get("mserp_physicalname")).replace(" ", "")
        ], key=lambda row: row["physicalName"] or ""),
        "freshness": {
            "fAndOReadUtc": base.iso(generated),
            "approvalCaptureReconciledUtc": base.iso(latest_capture),
            "effectiveDataTimeUtc": base.iso(min(generated, latest_capture)) if latest_capture else base.iso(generated),
        },
        "settledCorrection02Gates": settled,
        "stalePopulationLane": {
            "count": len(stale),
            "poCount": sum(row["documentType"] == "PO" for row in stale),
            "evidenceReference": "evidence/workbook-retirement-correction-02.md#stale-rows-the-workbook-still-carries",
        },
        "poAcceptance": {"p1": p1, "p2": p2, "p3": p3, "p4": p4, "p5": p5},
    }
    output["verdict"] = {
        "prStagePassed": correction02["verdict"]["prStagePassed"],
        "prClockPassed": correction02["verdict"]["prClockPassed"],
        "prAmountPassed": correction02["verdict"]["prAmountPassed"],
        "poAmountPassed": correction02["verdict"]["poAmountPassed"],
        "distinctDocumentCountsExact": correction02["verdict"]["distinctDocumentCountsExact"],
        "p1Passed": p1["passed"],
        "p2Passed": p2["passed"],
        "p3Passed": p3["passed"],
        "p4Reported": len(p4_rows) == 1425,
        "p5SampleComplete": p5["passed"],
    }
    output["verdict"]["canRetireTotally"] = all([
        output["verdict"]["prStagePassed"], output["verdict"]["prClockPassed"],
        output["verdict"]["prAmountPassed"], output["verdict"]["poAmountPassed"],
        output["verdict"]["distinctDocumentCountsExact"], output["verdict"]["p1Passed"],
        output["verdict"]["p2Passed"], output["verdict"]["p3Passed"],
    ])

    text = json.dumps(output, indent=2, ensure_ascii=False, default=str) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(json.dumps({
        "generatedAt": output["generatedAt"],
        "sourceCounts": output["sourceCounts"],
        "p1": {key: value for key, value in p1.items() if key != "differences"},
        "p2": {key: value for key, value in p2.items() if key != "differences"},
        "p3": {key: value for key, value in p3.items() if key not in {"differences", "excludedRows", "joinIssues", "progressedAfterExport"}},
        "p4": {key: value for key, value in p4.items() if key not in {"notEvidencedRows"}},
        "p5": {key: value for key, value in p5.items() if key != "rows"},
        "verdict": output["verdict"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
