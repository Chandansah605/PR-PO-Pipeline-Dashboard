"""Render correction-02 workbook-retirement evidence as Markdown."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def pct(value):
    return "—" if value is None else f"{value:.2f}%"


def ratio(data, matched="matched", compared="compared"):
    return f"{data[matched]:,}/{data[compared]:,} ({pct(data['agreementPercent'])})"


def amount_ratio(data):
    return f"{data['matchedDocuments']:,}/{data['documentsCompared']:,} ({pct(data['agreementPercent'])})"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    parser.add_argument("correction01", type=Path)
    parser.add_argument("correction02", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--notes", type=Path)
    args = parser.parse_args()

    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    c1 = json.loads(args.correction01.read_text(encoding="utf-8"))
    c2 = json.loads(args.correction02.read_text(encoding="utf-8"))
    b_rec, c1_rec, c2_rec = baseline["reconciliation"], c1["reconciliation"], c2["reconciliation"]
    c2_all = c2_rec["correction02AllRows"]
    b_amt, c1_amt = baseline["amountBasis"], c1["amountBasis"]
    c2_all_amt, c2_amt = c2["correction02AllRowsAmountBasis"], c2["amountBasis"]
    verdict = c2["verdict"]
    counts = c2["sourceCounts"]
    fresh = c2["freshness"]
    stale = c2["staleRowsTheWorkbookStillCarries"]
    progressed = c2["progressedAfterExport"]
    po_reasons = Counter(row["reasonCode"] for row in c2_rec["poStage"]["differences"])
    stale_types = Counter(row["documentType"] for row in stale)

    old_pr_amount = 100 * b_amt["pr.xlsx"]["exactDocumentMatches"] / b_amt["pr.xlsx"]["documentsCompared"]
    old_po_amount = 100 * b_amt["po.xlsx"]["exactDocumentMatches"] / b_amt["po.xlsx"]["documentsCompared"]

    lines = [
        "# Workbook retirement correction 02 — 7 September 2026",
        "",
        "## Verdict",
        "",
        "**Cannot retire.** Measuring the documents the dashboard displays fixes the PR stage and both amount gates, but the PO stage gate remains below 95%. The safe-cutover stop applies before deployment or workbook removal.",
        "",
        "| Gate | 7 Sep verdict | Correction 01 | Correction 02: all rows / dashboard population | Result |",
        "|---|---:|---:|---:|---|",
        f"| PR stage | {ratio(b_rec['prStage'])} | {ratio(c1_rec['prStage'])} | {ratio(c2_all['prStage'])} / {ratio(c2_rec['prStage'])} | {'PASS' if verdict['prStagePassed'] else 'FAIL'}; threshold 95% |",
        f"| PR procurement clock within one day | {ratio(b_rec['prProcurementClock'], 'matchedWithinOneDay')} | {ratio(c1_rec['prProcurementClock'], 'matchedWithinOneDay')} | {ratio(c2_all['prProcurementClock'], 'matchedWithinOneDay')} / {ratio(c2_rec['prProcurementClock'], 'matchedWithinOneDay')} | {'PASS' if verdict['prClockPassed'] else 'FAIL'}; threshold 90% |",
        f"| PO stage | {ratio(b_rec['poStage'])} | {ratio(c1_rec['poStage'])} | {ratio(c2_all['poStage'])} / {ratio(c2_rec['poStage'])} | {'PASS' if verdict['poStagePassed'] else 'FAIL'}; threshold 95% |",
        f"| PR amount | {b_amt['pr.xlsx']['exactDocumentMatches']:,}/{b_amt['pr.xlsx']['documentsCompared']:,} ({old_pr_amount:.2f}%) | {amount_ratio(c1_amt['pr.xlsx'])} | {amount_ratio(c2_all_amt['pr.xlsx'])} / {amount_ratio(c2_amt['pr.xlsx'])} | {'PASS' if verdict['prAmountPassed'] else 'FAIL'}; threshold 95% |",
        f"| PO amount | {b_amt['po.xlsx']['exactDocumentMatches']:,}/{b_amt['po.xlsx']['documentsCompared']:,} ({old_po_amount:.2f}%) | {amount_ratio(c1_amt['po.xlsx'])} | {amount_ratio(c2_all_amt['po.xlsx'])} / {amount_ratio(c2_amt['po.xlsx'])} | {'PASS' if verdict['poAmountPassed'] else 'FAIL'}; threshold 95% |",
        f"| Distinct documents | Exact | Exact | Exact / Exact | {'PASS' if verdict['distinctDocumentCountsExact'] else 'FAIL'} |",
        "",
        "The two Correction 02 figures show all workbook rows first and the dashboard population second. No excluded row is hidden; every excluded row appears in the stale lane below.",
        "",
        "## Why the PO stage gate still fails",
        "",
        f"The dashboard population contains {c2_rec['poStage']['compared']:,} comparable PO rows. {c2_rec['poStage']['matched']:,} match and {len(c2_rec['poStage']['differences']):,} do not. "
        f"Of the differences, {po_reasons['PROGRESSION_NOT_AFTER_EXPORT']:,} have a later live stage whose event occurred before the export cutoff, and {po_reasons['PROGRESSION_TIMESTAMP_UNAVAILABLE']:,} have no exposed event timestamp. The exposed PO-confirmation entity returned {counts['livePOConfirmations']:,} rows, so an approval-to-sent progression cannot be assumed.",
        "",
        "## Measurement rules applied",
        "",
        f"- Workbook export cutoff: `{c2['measurementRules']['workbookExportCutoffUtc']}` ({c2['measurementRules']['workbookExportCutoffBasis']}).",
        "- PR population: live status `In review` or `Approved`, with a mapped workbook step, matching the production live-pipeline predicate.",
        "- PO population: mapped rows excluding invoiced/closed/cancelled POs and rejected approvals, matching the production live-pipeline predicate.",
        "- A later stage matches only when its authoritative live timestamp is after the export cutoff. It is tagged `PROGRESSED_AFTER_EXPORT`.",
        "- Amount equality within AED 0.01 matches first. Standard, mixed or unknown tax basis also tests workbook divided by 1.05.",
        "",
        "## Read-only source evidence",
        "",
        f"- Workbooks: {counts['workbookPR']:,} PR and {counts['workbookPO']:,} PO documents; neither file was modified.",
        f"- F&O: {counts['livePRHeaders']:,} PR headers, {counts['livePRLines']:,} PR lines, {counts['livePOHeaders']:,} PO headers and {counts['livePOLines']:,} PO lines.",
        f"- PO events: {counts['livePackingSlipJournals']:,} packing slips, {counts['livePOConfirmations']:,} exposed confirmations and {counts['liveVendorInvoiceJournals']:,} invoice-journal rows.",
        f"- Approval capture: {counts['captureSnapshots']:,} snapshots and {counts['captureCurrentWorkItems']:,} current work items.",
        f"- Dataset generated/F&O read: `{fresh['datasetGeneratedUtc']}`; approval capture reconciled: `{fresh['approvalCaptureReconciledUtc']}`; effective data time: `{fresh['effectiveDataTimeUtc']}`.",
        "",
        "## PROGRESSED_AFTER_EXPORT matches",
        "",
        f"Count: {len(progressed):,}. Each row records the two timestamps used by R2.",
        "",
    ]
    for row in progressed:
        lines.append(
            f"- {row['document']}: {row['workbookStage']} → {row['liveStage']}; "
            f"workbook export `{row['workbookExportTimestamp']}`; live evidence `{row['liveEvidenceTimestamp']}`; "
            f"source `{row['liveEvidenceSource']}`; `PROGRESSED_AFTER_EXPORT`."
        )

    lines.extend(["", "## PR stage differences in dashboard population", ""])
    for row in c2_rec["prStage"]["differences"]:
        lines.append(
            f"- {row['document']}: {row['expectedStage']} → {row['liveStage']}; `{row['reasonCode']}`"
            + (f"; flags `{', '.join(row['flags'])}`." if row.get("flags") else ".")
        )

    lines.extend(["", "## PO stage differences in dashboard population", ""])
    for row in c2_rec["poStage"]["differences"]:
        lines.append(
            f"- {row['document']}: {row['expectedStage']} → {row['liveStage']}; `{row['reasonCode']}`"
            + (f"; flags `{', '.join(row['flags'])}`." if row.get("flags") else ".")
        )

    lines.extend(["", "## PR procurement clock differences over one day", ""])
    for row in c2_rec["prProcurementClock"]["differences"]:
        lines.append(
            f"- {row['document']}: {row['stage']}; workbook `{row['workbookClock']}`; live seed `{row['liveSeedClock']}`."
        )

    po_clock = c2_rec["poClock"]
    lines.extend([
        "",
        "## PO clock evidence",
        "",
        f"- Like-for-like approval clocks: {po_clock['matchedWithinOneDay']:,}/{po_clock['comparedLikeForLikeApprovalClocks']:,} ({pct(po_clock['agreementPercent'])}) within one day.",
        f"- Receipt-posted clocks: {po_clock['receiptPostedWithPostedOn']:,}/{po_clock['receiptPostedDocuments']:,} current receipt rows have a packing-slip `Posted on` date.",
        "- Workbook `LPO sent` clocks remain non-comparable with receipt posting and are not a gate.",
        "",
    ])
    for row in po_clock["differences"]:
        lines.append(
            f"- {row['document']}: {row['stage']}; workbook `{row['workbookClock']}`; capture `{row['liveClock']}`."
        )

    for kind in ("pr.xlsx", "po.xlsx"):
        data = c2_amt[kind]
        lines.extend([
            "",
            f"## {kind} amount differences in dashboard population",
            "",
            f"Agreement: {amount_ratio(data)}. Match rules: " + ", ".join(f"{key} {value:,}" for key, value in sorted(data['matchRuleCounts'].items())) + ".",
            "",
        ])
        for row in data["differences"]:
            compared = "unavailable" if row["adjustedWorkbookExVat"] is None else f"AED {row['adjustedWorkbookExVat']:,.2f}"
            difference = "unavailable" if row["difference"] is None else f"AED {row['difference']:,.2f}"
            lines.append(
                f"- {row['document']}: workbook AED {row['workbookAmount']:,.2f}; compared ex-VAT {compared}; "
                f"live ex-VAT AED {row['liveLineAmountExVat']:,.2f}; difference {difference}; "
                f"basis `{row['taxBasis']}`; `{row['reasonCode']}`."
            )

    lines.extend([
        "",
        "## Stale rows the workbook still carries",
        "",
        f"Count: {len(stale):,} ({stale_types['PR']:,} PR; {stale_types['PO']:,} PO). These rows retain a workbook step but are outside the production dashboard's live-pipeline population. They do not enter a gate.",
        "",
    ])
    for row in stale:
        approval = f"; approval `{row['approvalStatus']}`" if row.get("approvalStatus") else ""
        lines.append(
            f"- {row['documentType']} {row['document']}: workbook step `{row['workbookStep']}`; "
            f"live status `{row['liveStatus']}`{approval}; `{row['reasonCode']}`."
        )

    lines.extend([
        "",
        "## What I found",
        "",
        "- R1 removes closed, cancelled, rejected and invoiced rows from the gate without deleting or hiding their evidence.",
        "- R3 fixes exact-equality false negatives and lifts both dashboard-population amount gates above 95%.",
        "- PO stage still fails because most current receipt events pre-date the export and the exposed confirmation entity has no rows.",
        "",
        "## Problems and risks",
        "",
        "- Counting old PO events as post-export progression would directly violate R2.",
        "- Deploying now would replace the workbook with a PO stage model measured at 44.02% agreement.",
        "- The operational systems continue moving; the UTC evidence position above identifies this run.",
        "",
        "## Files changed",
        "",
        "- Reconciliation logic, Correction 02 evidence/report, project status documentation and the unpublished change note.",
        "",
        "## What I did not change",
        "",
        "- No dashboard, Race Control, email, snapshot or proxy runtime path was cut over.",
        "- No workbook, generator, fallback or workbook workflow was removed.",
        "- No Dataverse or Azure resource was written. No function app or GitHub Pages site was deployed.",
        "- The proxy guard on `main` remains unchanged and prevents push deployment to Chandan's app.",
        "",
        "## Testing performed",
        "",
        "- Python compile and machine-evidence assertions.",
        "- Complete read-only reconciliation against both Dataverse organisations and both unchanged workbooks.",
        "- Existing dashboard JavaScript and weekly-snapshot regression tests.",
        "- Desktop browser visual check and inspection of the existing 700 px responsive rule in the unpublished change note.",
        "- Git diff and remote-branch verification; production remained unchanged.",
        "",
        "## Commands recorded",
        "",
        "- `python tests/reconcile_workbook_retirement.py --out evidence/workbook-retirement-correction-02.json` with short-lived Azure CLI tokens supplied only to the child process.",
        "- `python tests/render_retirement_correction02.py evidence/workbook-retirement-reconciliation.json evidence/workbook-retirement-correction-01.json evidence/workbook-retirement-correction-02.json evidence/workbook-retirement-correction-02.md --notes NOTES.md`.",
        "- `node --test tests/dataverse-live.test.js tests/race-control.test.js`.",
        "- `python tests/test_weekly_snapshot.py`.",
        "",
        "## Remaining risks",
        "",
        "- The 393 reason-coded PO stage differences prevent retirement under the supplied rules.",
        "- Production remains workbook-dependent and still depends on the morning email chain.",
        "",
        "## Recommended next step",
        "",
        "Do not invent another progression rule. Resolve the PO event-timing gap at source or explicitly change R2, then rerun the same dashboard-population gates.",
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
