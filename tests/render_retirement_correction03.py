"""Render Correction 03 workbook-retirement evidence and append it to NOTES."""

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
    parser.add_argument("correction03", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--notes", type=Path)
    args = parser.parse_args()

    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    c1 = json.loads(args.correction01.read_text(encoding="utf-8"))
    c2 = json.loads(args.correction02.read_text(encoding="utf-8"))
    c3 = json.loads(args.correction03.read_text(encoding="utf-8"))
    b_rec, c1_rec, c2_rec = baseline["reconciliation"], c1["reconciliation"], c2["reconciliation"]
    b_amt, c1_amt, c2_amt = baseline["amountBasis"], c1["amountBasis"], c2["amountBasis"]
    p1, p2, p3, p4, p5 = (c3["poAcceptance"][key] for key in ("p1", "p2", "p3", "p4", "p5"))
    old_pr_amount = 100 * b_amt["pr.xlsx"]["exactDocumentMatches"] / b_amt["pr.xlsx"]["documentsCompared"]
    old_po_amount = 100 * b_amt["po.xlsx"]["exactDocumentMatches"] / b_amt["po.xlsx"]["documentsCompared"]
    p1_reasons = Counter(row["reasonCode"] for row in p1["differences"])
    p3_reasons = Counter(row["reasonCode"] for row in p3["differences"])

    lines = [
        "# Workbook retirement correction 03 — 7 September 2026",
        "",
        "## Verdict",
        "",
        "**Cannot retire.** The replacement PO tests are valid, but P1 and P3 fail. The safe-cutover stop applies before deployment, merge to `main`, or workbook removal.",
        "",
        "| Gate | 7 Sep verdict | Correction 01 | Correction 02 | Correction 03 |",
        "|---|---:|---:|---:|---:|",
        f"| PR stage | {ratio(b_rec['prStage'])} | {ratio(c1_rec['prStage'])} | {ratio(c2_rec['prStage'])} | {ratio(c2_rec['prStage'])} settled PASS |",
        f"| PR procurement clock | {ratio(b_rec['prProcurementClock'], 'matchedWithinOneDay')} | {ratio(c1_rec['prProcurementClock'], 'matchedWithinOneDay')} | {ratio(c2_rec['prProcurementClock'], 'matchedWithinOneDay')} | {ratio(c2_rec['prProcurementClock'], 'matchedWithinOneDay')} settled PASS |",
        f"| PO stage | {ratio(b_rec['poStage'])} | {ratio(c1_rec['poStage'])} | {ratio(c2_rec['poStage'])} | RETIRED |",
        f"| PO P1 stage evidence | — | — | — | {p1['evidenced']:,}/{p1['population']:,} ({pct(p1['agreementPercent'])}) FAIL |",
        f"| PO P2 F&O population parity | — | — | — | {p2['matchedDistinctDocuments']:,}/{p2['fAndOOpenDistinctDocuments']:,} ({pct(p2['agreementPercent'])}) PASS |",
        f"| PO P3 maintained approval steps | — | — | — | {p3['matched']:,}/{p3['compared']:,} ({pct(p3['agreementPercent'])}) FAIL |",
        f"| PO P4 LPO-sent distribution | — | — | — | Reported; {p4['receivedOrInvoicedBusinessCaseCount']:,} received or invoiced |",
        f"| PO P5 human sample | — | — | — | {p5['sampleSize']:,}/{p5['targetSampleSize']:,} complete |",
        f"| PR amount | {b_amt['pr.xlsx']['exactDocumentMatches']:,}/{b_amt['pr.xlsx']['documentsCompared']:,} ({old_pr_amount:.2f}%) | {amount_ratio(c1_amt['pr.xlsx'])} | {amount_ratio(c2_amt['pr.xlsx'])} | {amount_ratio(c2_amt['pr.xlsx'])} settled PASS |",
        f"| PO amount | {b_amt['po.xlsx']['exactDocumentMatches']:,}/{b_amt['po.xlsx']['documentsCompared']:,} ({old_po_amount:.2f}%) | {amount_ratio(c1_amt['po.xlsx'])} | {amount_ratio(c2_amt['po.xlsx'])} | {amount_ratio(c2_amt['po.xlsx'])} settled PASS |",
        "| Distinct documents | Exact | Exact | Exact | Exact settled PASS |",
        "",
        "Correction 03 carries the accepted Correction 02 PR, amount and document-count results unchanged. It replaces only the retired PO stage gate.",
        "",
        "## P1 — every live PO stage is evidenced",
        "",
        f"Result: **FAIL**. {p1['evidenced']:,}/{p1['population']:,} open F&O purchase orders have a dated event ({pct(p1['agreementPercent'])}); {len(p1['differences']):,} are displayed as `STAGE_NOT_EVIDENCED`.",
        "",
        "Reason counts: " + ", ".join(f"`{reason}` {count:,}" for reason, count in sorted(p1_reasons.items())) + ".",
        "",
    ]
    for row in p1["differences"]:
        candidate = row["candidateStage"] or "none"
        lines.append(
            f"- {row['legalEntity']} / {row['document']}: candidate `{candidate}`; displayed `STAGE_NOT_EVIDENCED`; "
            f"F&O `{row['fAndOStatus']}` / approval `{row['fAndOApprovalStatus']}`; `{row['reasonCode']}`."
        )

    lines.extend([
        "",
        "## P2 — population parity with F&O",
        "",
        f"Result: **PASS**. The candidate live population contains {p2['liveOpenDistinctDocuments']:,}/{p2['fAndOOpenDistinctDocuments']:,} open legal-entity/document keys ({pct(p2['agreementPercent'])}). Purchase-order numbers reused across companies are keyed by legal entity and are not collapsed.",
        "",
    ])
    if p2["differences"]:
        for row in p2["differences"]:
            lines.append(f"- {row.get('key') or row.get('document')}: `{row['reasonCode']}`.")
    else:
        lines.append("- Differences: none.")

    lines.extend([
        "",
        "## P3 — workbook parity where the workbook is maintained",
        "",
        f"Result: **FAIL**. {p3['matched']:,}/{p3['compared']:,} R1-population approval rows agree after R2 ({pct(p3['agreementPercent'])}); the target is 95%.",
        f"The supplied count of 108 is not the workbook count: the six named approval values total {p3['workbookApprovalRows']:,}. Of those, {p3['compared']:,} are in the current R1 population and {p3['excludedByR1']:,} are outside it. This arithmetic is reported rather than forced to 108.",
        "",
        "Reason counts: " + ", ".join(f"`{reason}` {count:,}" for reason, count in sorted(p3_reasons.items())) + ".",
        "",
    ])
    for row in p3["differences"]:
        event = row.get("event") or "none"
        event_at = row.get("eventTimestamp") or "none"
        lines.append(
            f"- {row.get('legalEntity') or 'unresolved'} / {row['document']}: workbook `{row['workbookStep']}` → "
            f"live `{row['liveStage']}`; event `{event}` at `{event_at}`; `{row['reasonCode']}`."
        )
    lines.extend(["", "### P3 rows excluded by R1", ""])
    for row in p3["excludedRows"]:
        lines.append(
            f"- {row.get('legalEntity') or 'unresolved'} / {row['document']}: workbook `{row['workbookStep']}`; "
            f"F&O `{row.get('fAndOStatus') or 'unavailable'}` / approval `{row.get('fAndOApprovalStatus') or 'unavailable'}`; `{row['reasonCode']}`."
        )
    lines.extend(["", "### P3 PROGRESSED_AFTER_EXPORT matches", ""])
    if p3["progressedAfterExport"]:
        for row in p3["progressedAfterExport"]:
            lines.append(
                f"- {row['document']}: {row['workbookStage']} → {row['liveStage']}; workbook export "
                f"`{row['workbookExportTimestamp']}`; live evidence `{row['liveEvidenceTimestamp']}`; "
                f"source `{row['liveEvidenceSource']}`; `PROGRESSED_AFTER_EXPORT`."
            )
    else:
        lines.append("- None. No P3 progression had qualifying post-export evidence.")

    lines.extend([
        "",
        "## P4 — LPO-sent rows reported, not gated",
        "",
        f"The business-case number is **{p4['receivedOrInvoicedBusinessCaseCount']:,}**: that many purchase orders still shown as merely `LPO sent` in the workbook are `Receipt posted` or `Invoiced` in F&O.",
        "",
        "Live distribution: " + ", ".join(f"`{stage}` {count:,}" for stage, count in p4["liveStageDistribution"].items()) + ".",
        f"Evidence coverage: {p4['evidenced']:,}/{p4['workbookLpoSentRows']:,}; {p4['notEvidenced']:,} do not have the dated event P1 requires.",
        "",
        "### P4 rows without dated stage evidence",
        "",
    ])
    for row in p4["notEvidencedRows"]:
        lines.append(
            f"- {row.get('legalEntity') or 'unresolved'} / {row['document']}: candidate `{row['liveStage']}`; "
            f"displayed `{row['displayedStage']}`; `{row['reasonCode']}`."
        )

    lines.extend([
        "",
        "## P5 — 25 purchase orders with human-checkable evidence",
        "",
        "| Legal entity | Purchase order | Displayed live stage | Candidate stage | Evidence event | Event date (UTC) |",
        "|---|---|---|---|---|---|",
    ])
    for row in p5["rows"]:
        lines.append(
            f"| {row.get('legalEntity') or 'unresolved'} | {row['document']} | {row['liveStage']} | "
            f"{row.get('candidateStage') or 'none'} | {row['event']} | {row.get('eventTimestamp') or 'none'} |"
        )

    stale = c3["stalePopulationLane"]
    counts = c3["sourceCounts"]
    fresh = c3["freshness"]
    lines.extend([
        "",
        "## Source and stale-population evidence",
        "",
        f"- `po.xlsx`: {c3['workbook']['rows']:,} rows, {c3['workbook']['distinctDocuments']:,} distinct order numbers, SHA-256 `{c3['workbook']['sha256']}`.",
        f"- F&O: {counts['livePOHeaders']:,} PO header keys, {counts['livePackingSlipJournals']:,} packing slips, {counts['liveVendorInvoiceJournals']:,} invoice journals and {counts['livePOConfirmations']:,} exposed confirmation rows.",
        f"- Approval capture: {counts['capturePOSnapshots']:,} current PO snapshots and {counts['capturePOCurrentWorkItems']:,} current PO work items.",
        f"- Evidence time: F&O read `{fresh['fAndOReadUtc']}`; approval capture `{fresh['approvalCaptureReconciledUtc']}`; effective `{fresh['effectiveDataTimeUtc']}`.",
        f"- Stale workbook lane retained from Correction 02: {stale['count']:,} rows total, including {stale['poCount']:,} PO rows. The complete list remains at `{stale['evidenceReference']}`.",
        "",
        "### F&O confirmation entity catalogue",
        "",
    ])
    for row in c3["confirmationEntityEvidence"]:
        lines.append(f"- `{row['physicalName']}`: generated in Dataverse = `{str(row['hasBeenGenerated']).lower()}`.")

    lines.extend([
        "",
        "## What I found",
        "",
        "- The retired all-stage workbook comparison was invalid because `po.xlsx` has no receipt or invoice stage value.",
        "- P2 proves the candidate open population is complete when legal entity forms part of the PO key.",
        f"- P1 still blocks cutover because the enabled confirmation entity has no rows and {len(p1['differences']):,} open POs lack dated stage evidence.",
        f"- P3 independently blocks cutover because only {p3['matched']:,} of {p3['compared']:,} maintained approval rows agree under R2.",
        "",
        "## Problems and risks",
        "",
        "- Calling an undated confirmed/open status `Sent to supplier` would violate P1.",
        "- Treating pre-export receipts as progress after export would violate R2.",
        "- Joining PO number without legal entity silently collapses reused order numbers across companies.",
        "",
        "## Files changed",
        "",
        "- Added isolated Correction 03 reconciliation, evidence and report generation.",
        "- Updated the blocked project status and unpublished change note with the P4 number.",
        "",
        "## Exact changes made",
        "",
        "- Replaced the obsolete PO stage gate in the audit verdict with P1–P5.",
        "- Added `STAGE_NOT_EVIDENCED`, composite PO identity, full exception lists and a 25-order sample.",
        "- Carried accepted Correction 02 PR, amount, count and stale-lane evidence unchanged.",
        "",
        "## What I did not change",
        "",
        "- No dashboard, Race Control, snapshot, email or proxy runtime path was cut over.",
        "- No workbook, generator, fallback or workflow was removed.",
        "- No Dataverse or Azure resource was written. No function app or GitHub Pages site was deployed.",
        "- Basit's morning email and Chandan's parallel chain remain untouched.",
        "",
        "## Testing performed",
        "",
        "- Python compile and machine-evidence assertions for P1–P5.",
        "- Complete read-only PO reconciliation against both Dataverse organisations and the unchanged workbook.",
        "- Existing dashboard JavaScript and weekly-snapshot regression tests.",
        "- Desktop browser visual check and responsive-rule inspection of the unpublished change note.",
        "- Git diff and remote-branch verification; production remained unchanged.",
        "",
        "## Commands recorded",
        "",
        "- `python tests/reconcile_workbook_retirement_correction03.py --out evidence/workbook-retirement-correction-03.json` with short-lived Azure CLI tokens supplied only to the child process.",
        "- `python tests/render_retirement_correction03.py evidence/workbook-retirement-reconciliation.json evidence/workbook-retirement-correction-01.json evidence/workbook-retirement-correction-02.json evidence/workbook-retirement-correction-03.json evidence/workbook-retirement-correction-03.md --notes NOTES.md`.",
        "- `python -m py_compile tests/reconcile_workbook_retirement.py tests/reconcile_workbook_retirement_correction03.py tests/render_retirement_correction02.py tests/render_retirement_correction03.py tests/validate_retirement_correction03.py`.",
        "- `python tests/validate_retirement_correction03.py`.",
        "- `node --test tests/dataverse-live.test.js tests/race-control.test.js`.",
        "- `python tests/test_weekly_snapshot.py`.",
        "- `git diff --check`, scoped status/diff review, and remote ref verification.",
        "",
        "## Assumptions",
        "",
        "- The accepted Correction 02 gates stay settled as instructed and are not recalculated into a new verdict.",
        "- R1 identity is legal entity plus purchase-order number because F&O reuses order numbers between companies.",
        "- An empty enabled confirmation entity is not evidence of a confirmation event.",
        "",
        "## Remaining risks",
        "",
        f"- P1 has {len(p1['differences']):,} exact blockers and P3 has {len(p3['differences']):,}; retirement is prohibited.",
        "- Production remains workbook-dependent and still depends on the morning email chain.",
        "",
        "## Recommended next step",
        "",
        "Expose a dated F&O PO confirmation event through an already-authorised read path and resolve the P3 historical approval discrepancies. Then rerun the same P1–P5 tests without weakening P1 or R2.",
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
