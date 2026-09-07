"""Render correction-01 workbook-retirement evidence as Markdown."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def pct(value):
    return "—" if value is None else f"{value:.2f}%"


def group_documents(rows, fields):
    grouped = defaultdict(list)
    for row in rows:
        key = " → ".join(str(row.get(field) or "(blank)") for field in fields)
        flags = ", ".join(row.get("flags") or [])
        if flags:
            key += f" ({flags})"
        grouped[key].append(row["document"])
    return grouped


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("current", type=Path)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--notes", type=Path)
    args = parser.parse_args()
    current = json.loads(args.current.read_text(encoding="utf-8"))
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    rec = current["reconciliation"]
    old = baseline["reconciliation"]
    amounts = current["amountBasis"]
    old_amounts = baseline["amountBasis"]
    counts = current["sourceCounts"]
    fresh = current["freshness"]
    verdict = current["verdict"]
    lpo_invoiced = sum(1 for row in rec["poStage"]["differences"] if row["workbookStep"] == "LPO sent/shared with supplier" and row["liveStage"] == "Invoiced")
    generous_po_matched = rec["poStage"]["matched"] + lpo_invoiced
    generous_po_percent = 100 * generous_po_matched / rec["poStage"]["compared"]
    pr_zero_amount_differences = sum(1 for row in amounts["pr.xlsx"]["differences"] if row["taxBasis"] == "zero amount")
    po_approval_event_differences = sum(1 for row in rec["poStage"]["differences"] if row["workbookStep"] != "LPO sent/shared with supplier")

    lines = [
        "# Workbook retirement correction 01 — 7 September 2026",
        "",
        "## Verdict",
        "",
        "**Cannot retire.** The corrected business rules remove the `PR in review` decision blocker, but three mandatory computed gates still fail. The safe-cutover stop applies before deployment or workbook removal.",
        "",
        "| Gate | 7 September verdict | Correction 01 | Result |",
        "|---|---:|---:|---|",
        f"| PR stage agreement | {old['prStage']['matched']:,}/{old['prStage']['compared']:,} ({pct(old['prStage']['agreementPercent'])}) | {rec['prStage']['matched']:,}/{rec['prStage']['compared']:,} ({pct(rec['prStage']['agreementPercent'])}) | {'PASS' if verdict['prStagePassed'] else 'FAIL'}; threshold 95% |",
        f"| PR procurement clock within one day | {old['prProcurementClock']['matchedWithinOneDay']:,}/{old['prProcurementClock']['compared']:,} ({pct(old['prProcurementClock']['agreementPercent'])}) | {rec['prProcurementClock']['matchedWithinOneDay']:,}/{rec['prProcurementClock']['compared']:,} ({pct(rec['prProcurementClock']['agreementPercent'])}) | {'PASS' if verdict['prClockPassed'] else 'FAIL'}; threshold 90% |",
        f"| PO stage agreement | {old['poStage']['matched']:,}/{old['poStage']['compared']:,} ({pct(old['poStage']['agreementPercent'])}) | {rec['poStage']['matched']:,}/{rec['poStage']['compared']:,} ({pct(rec['poStage']['agreementPercent'])}) | {'PASS' if verdict['poStagePassed'] else 'FAIL'}; threshold 95% |",
        f"| PR amount agreement | {old_amounts['pr.xlsx']['exactDocumentMatches']:,}/{old_amounts['pr.xlsx']['documentsCompared']:,} ({100 * old_amounts['pr.xlsx']['exactDocumentMatches'] / old_amounts['pr.xlsx']['documentsCompared']:.2f}%, old unadjusted basis) | {amounts['pr.xlsx']['matchedDocuments']:,}/{amounts['pr.xlsx']['documentsCompared']:,} ({pct(amounts['pr.xlsx']['agreementPercent'])}, corrected ex-VAT basis) | {'PASS' if verdict['prAmountPassed'] else 'FAIL'}; threshold 95% |",
        f"| PO amount agreement | {old_amounts['po.xlsx']['exactDocumentMatches']:,}/{old_amounts['po.xlsx']['documentsCompared']:,} ({100 * old_amounts['po.xlsx']['exactDocumentMatches'] / old_amounts['po.xlsx']['documentsCompared']:.2f}%, old unadjusted basis) | {amounts['po.xlsx']['matchedDocuments']:,}/{amounts['po.xlsx']['documentsCompared']:,} ({pct(amounts['po.xlsx']['agreementPercent'])}, corrected ex-VAT basis) | {'PASS' if verdict['poAmountPassed'] else 'FAIL'}; threshold 95% |",
        f"| Distinct-document count | Not a failing gate | {current['liveDatasetNumbers']['distinctResolvedDocuments']:,} resolved documents; {current['liveDatasetNumbers']['openWorkItems']:,} work items | {'PASS' if verdict['distinctDocumentCountsExact'] else 'FAIL'} |",
        "",
        f"Even if all {lpo_invoiced:,} workbook `LPO sent/shared with supplier` rows now marked `Invoiced` were accepted as later lifecycle progress, PO agreement would be {generous_po_matched:,}/{rec['poStage']['compared']:,} ({generous_po_percent:.2f}%), still below 95%. Correction 01 explicitly grants progression equivalence for `Receipt posted`, not for `Invoiced`; the measured gate above applies that rule literally.",
        "",
        "## Read-only source evidence",
        "",
        f"- Workbooks: {counts['workbookPR']:,} PR and {counts['workbookPO']:,} PO documents.",
        f"- F&O: {counts['livePRHeaders']:,} PR headers, {counts['livePRLines']:,} PR lines, {counts['livePOHeaders']:,} PO headers, {counts['livePOLines']:,} PO lines and {counts['livePackingSlipJournals']:,} packing-slip journals.",
        f"- Approval capture: {counts['captureSnapshots']:,} snapshots and {counts['captureCurrentWorkItems']:,} current work items.",
        f"- Dataset generated/F&O read: `{fresh['datasetGeneratedUtc']}` / `{fresh['fAndOReadUtc']}`.",
        f"- Approval capture reconciled/effective data time: `{fresh['approvalCaptureReconciledUtc']}` / `{fresh['effectiveDataTimeUtc']}`; capture age {fresh['captureAgeMinutes']:.2f} minutes.",
        "",
        "## Corrected amount basis",
        "",
        "Tax applicability comes from the exposed F&O sales-tax-group and item-tax-group pair. Live group descriptions confirm `SR-RCVR` is Standard Recoverable, `OS` is Out of Scope of VAT and `ZR` is Zero Rate. A standard-rate line requires both codes to be standard-rate; an OS/ZR code makes the line non-VAT. Standard-rate documents divide the workbook total by 1.05; non-VAT documents keep the workbook value. Mixed or blank pairs remain unmatched rather than being guessed. Zero matches only zero.",
        "",
    ]
    for kind in ("pr.xlsx", "po.xlsx"):
        data = amounts[kind]
        lines.extend([
            f"### {kind}",
            "",
            f"- Agreement: {data['matchedDocuments']:,}/{data['documentsCompared']:,} ({pct(data['agreementPercent'])}).",
            f"- Workbook including VAT: AED {data['workbookTotalIncludingVat']:,.2f}.",
            f"- Deterministically adjusted workbook excl. VAT: AED {data['adjustedWorkbookTotalExVat']:,.2f} across {data['documentsWithDeterministicTaxBasis']:,} documents.",
            f"- Live line total excl. VAT: AED {data['liveLineTotalExVat']:,.2f}.",
            "- Tax-basis counts: " + ", ".join(f"{name} {value:,}" for name, value in sorted(data['taxBasisCounts'].items())) + ".",
            "",
        ])

    lines.extend(["## PR stage differences", ""])
    for reason, documents in sorted(group_documents(rec["prStage"]["differences"], ("expectedStage", "liveStage")).items()):
        lines.append(f"- {reason}: " + ", ".join(documents))

    lines.extend(["", "## PO stage differences", ""])
    for reason, documents in sorted(group_documents(rec["poStage"]["differences"], ("expectedStage", "liveStage")).items()):
        lines.append(f"- {reason}: " + ", ".join(documents))

    lines.extend(["", "## PR procurement clock differences over one day", ""])
    for row in rec["prProcurementClock"]["differences"]:
        lines.append(f"- {row['document']}: {row['stage']}; workbook `{row['workbookClock']}`; F&O modified-time seed `{row['liveSeedClock']}`.")

    po_clock = rec["poClock"]
    lines.extend([
        "",
        "## PO clock evidence",
        "",
        f"Only like-for-like approval clocks are comparable: {po_clock['matchedWithinOneDay']:,}/{po_clock['comparedLikeForLikeApprovalClocks']:,} ({pct(po_clock['agreementPercent'])}) are within one day. The {len(po_clock['notComparableEventClocks']):,} workbook LPO-sent clocks are not compared with later receipt-posting dates because they are different events.",
        "",
    ])
    for row in po_clock["differences"]:
        lines.append(f"- {row['document']}: {row['stage']}; workbook `{row['workbookClock']}`; capture assignment `{row['liveClock']}`.")

    for kind in ("pr.xlsx", "po.xlsx"):
        lines.extend(["", f"## {kind} amount differences", ""])
        for row in amounts[kind]["differences"]:
            adjusted = "unavailable" if row["adjustedWorkbookExVat"] is None else f"AED {row['adjustedWorkbookExVat']:,.2f}"
            difference = "unavailable" if row["difference"] is None else f"AED {row['difference']:,.2f}"
            codes = ", ".join(row["taxCodes"]) or "no material live lines"
            lines.append(f"- {row['document']}: workbook AED {row['workbookAmount']:,.2f}; adjusted excl. VAT {adjusted}; live excl. VAT AED {row['liveLineAmountExVat']:,.2f}; difference {difference}; basis `{row['taxBasis']}`; codes `{codes}`.")

    lines.extend([
        "",
        "## Decisions applied",
        "",
        "- `PurchReqReviewTask` maps to `Sourcing`; the separate `PR in review` bucket is removed from the corrected comparison.",
        "- Amounts use live F&O line values excluding VAT. No amount is grossed up.",
        "- PO event stages are `Sent to supplier`, `Receipt posted` and `Invoiced`; a packing slip is a posting event, not a delivery date.",
        "- Approved dropped columns are not treated as retirement blockers. They remain untouched because the cutover stopped before code removal.",
        "",
        "## Workflow trigger proof",
        "",
        "- `.github/workflows/main_pr-po-dashboard-proxy.yml` in `pr-po-proxy` is manual-only and contains no deployment action.",
        "- `.github/workflows/deploy-ssg-prpo-proxy.yml` is manual-only, requires an exact tested SHA and targets only `ssg-prpo-proxy`.",
        "- Required secret: `AZURE_FUNCTIONAPP_PUBLISH_PROFILE_SSG_PRPO_PROXY`, containing only the authorised app's publish profile.",
        "",
        "## What I found",
        "",
        f"- Merging `PR in review` into `Sourcing` improves PR stage agreement, but current line pricing and zero-active-line cases still disagree with {len(rec['prStage']['differences']):,} workbook rows.",
        "- The PO workbook is substantially behind live lifecycle events. Old approval labels now coexist with sent, received or invoiced live orders.",
        f"- PR amount mismatch is dominated by {pr_zero_amount_differences:,} workbook-valued documents whose current live active-line amount is zero; tax adjustment cannot repair a missing/current-line basis difference.",
        "",
        "## Problems and risks",
        "",
        "- Deploying now would knowingly replace the workbook with a stage model below both 95% stage gates and a PR amount model below the 95% amount gate.",
        "- The PO sent timestamp is not exposed. Receipt posting and approval assignment have truthful clocks; the old LPO-sent time has no like-for-like live clock.",
        "- The live sources continue moving. All figures above belong to the recorded UTC evidence position.",
        "",
        "## Files changed",
        "",
        "- Reconciliation logic, correction evidence/report, `NOTES.md` and the unpublished change note in the dashboard repository.",
        "- Deployment workflows and safety documentation in `pr-po-proxy`.",
        "",
        "## What I did not change",
        "",
        "- No dashboard, Race Control, email, snapshot or proxy runtime path was cut over.",
        "- No workbook, generator, fallback, recipient, sender or quiet-mode setting was removed or changed.",
        "- No Dataverse or Azure resource was written. Neither function app was deployed.",
        "- Dashboard `main` was not updated because its legacy Pages source auto-publishes every main commit.",
        "",
        "## Testing performed",
        "",
        "- Python compile and JSON gate assertions.",
        "- Complete read-only reconciliation against both Dataverse organisations and both unchanged workbooks.",
        "- Existing dashboard JavaScript and weekly snapshot regression tests.",
        "- Dependency-free trigger/target assertions and manual YAML structure review for both proxy workflows.",
        "- Change-note visual check at desktop and 412 x 915 phone viewports.",
        "",
        "## Commands recorded",
        "",
        "- `python tests/reconcile_workbook_retirement.py --out evidence/workbook-retirement-correction-01.json` with short-lived Azure CLI tokens supplied only to the child process.",
        "- `python tests/render_retirement_correction.py evidence/workbook-retirement-correction-01.json evidence/workbook-retirement-reconciliation.json evidence/workbook-retirement-correction-01.md --notes NOTES.md`.",
        "- `node --test tests/dataverse-live.test.js tests/race-control.test.js`.",
        "- `python tests/test_weekly_snapshot.py`.",
        "- PowerShell trigger/target assertions for both proxy workflows; no YAML parser was installed.",
        "",
        "## Remaining risks",
        "",
        "- The failed document populations need a source-level correction or a newly approved reconciliation rule before another cutover attempt.",
        "- Production remains workbook-dependent and therefore still depends on the morning email chain.",
        "",
        "## Recommended next step",
        "",
        f"Investigate the {pr_zero_amount_differences:,} PR amount cases with no current active-line value and the {po_approval_event_differences:,} PO approval-to-event differences. Rerun the same gates after the sources or approved population rules change. Do not deploy or remove workbooks before all mandatory gates pass.",
        "",
    ])
    rendered = "\n".join(lines)
    args.target.parent.mkdir(parents=True, exist_ok=True)
    args.target.write_text(rendered, encoding="utf-8")
    if args.notes:
        marker = lines[0]
        notes = args.notes.read_text(encoding="utf-8")
        if marker in notes:
            notes = notes[:notes.index(marker)].rstrip() + "\n\n" + rendered
        else:
            notes = notes.rstrip() + "\n\n" + rendered
        args.notes.write_text(notes, encoding="utf-8")


if __name__ == "__main__":
    main()
