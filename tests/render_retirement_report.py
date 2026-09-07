"""Render the machine reconciliation as a compact Markdown evidence section."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def pct(value):
    return "—" if value is None else f"{value:.2f}%"


def docs_by_reason(rows, keys):
    grouped = defaultdict(list)
    for row in rows:
        reason = " → ".join(str(row.get(key) or "—") for key in keys)
        flags = ", ".join(row.get("flags") or [])
        if flags:
            reason += f" ({flags})"
        grouped[reason].append(row["document"])
    return grouped


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    data = json.loads(args.source.read_text(encoding="utf-8"))
    counts = data["sourceCounts"]
    fresh = data["freshness"]
    live = data["liveDatasetNumbers"]
    rec = data["reconciliation"]

    lines = [
        "# Workbook retirement verdict — 7 September 2026",
        "",
        "## Verdict",
        "",
        "**Cannot retire.** The mandatory cutover gates failed. The current workbook path remains intact and no live replacement was deployed.",
        "",
        "The decisive business blocker is `PR in review`: current capture element `f51900e9-7be4-4b68-9974-a08f70dedaa6` is shared by 30 workbook `PR in review` documents, 109 `Sourcing` documents and 297 `Priced — awaiting approval` documents. Four other current elements also mix `PR in review` with `Sourcing` or `Priced`. The addendum says to stop rather than merge `PR in review` into `Sourcing` without Waqas's decision.",
        "",
        "The measured PR stage agreement was " + pct(rec["prStage"]["agreementPercent"]) + f" ({rec['prStage']['matched']}/{rec['prStage']['compared']}), below the 95% gate. The procurement clock passed at " + pct(rec["prProcurementClock"]["agreementPercent"]) + f" ({rec['prProcurementClock']['matchedWithinOneDay']}/{rec['prProcurementClock']['compared']}) within one day. PO stage agreement was " + pct(rec["poStage"]["agreementPercent"]) + f" ({rec['poStage']['matched']}/{rec['poStage']['compared']}); posted packing slips classify many still-open orders differently from the workbook.",
        "",
        "## Read-only source evidence",
        "",
        "| Source | Rows/documents |",
        "|---|---:|",
        f"| Last PR workbook | {counts['workbookPR']:,} documents |",
        f"| Last PO workbook | {counts['workbookPO']:,} documents |",
        f"| Live F&O PR headers / lines / BI headers | {counts['livePRHeaders']:,} / {counts['livePRLines']:,} / {counts['livePRBiHeaders']:,} |",
        f"| Live F&O PO headers / lines / packing-slip journals | {counts['livePOHeaders']:,} / {counts['livePOLines']:,} / {counts['livePackingSlipJournals']:,} |",
        f"| Approval capture snapshots / current work items | {counts['captureSnapshots']:,} / {counts['captureCurrentWorkItems']:,} |",
        f"| Resolved distinct documents / unresolved work items | {counts['captureResolvedDistinctDocuments']:,} / {counts['captureUnresolvedWorkItems']:,} |",
        "",
        f"- Dataset generated: `{fresh['datasetGeneratedUtc']}`.",
        f"- F&O read completed: `{fresh['fAndOReadUtc']}`.",
        f"- Approval capture reconciled: `{fresh['approvalCaptureReconciledUtc']}`.",
        f"- Effective data time (oldest required source): `{fresh['effectiveDataTimeUtc']}`; capture age {fresh['captureAgeMinutes']:.2f} minutes.",
        "",
        "## Workbook column replacement evidence",
        "",
    ]

    for workbook in ("pr.xlsx", "po.xlsx"):
        lines.extend([
            f"### `{workbook}`",
            "",
            "| Workbook column | Proposed live source | Non-blank | Compared | Matched | Agreement |",
            "|---|---|---:|---:|---:|---:|",
        ])
        for item in data["columns"][workbook]:
            source = item["liveSource"]
            if item["noLiveEquivalent"]:
                source = "**No live equivalent:** " + source
            lines.append(
                f"| {item['column']} | {source} | {item['workbookNonBlank']:,} | {item['compared']:,} | {item['matched']:,} | {pct(item['agreementPercent'])} |"
            )
        lines.append("")

    amounts = data["amountBasis"]
    lines.extend([
        "### Amount-basis gap",
        "",
        f"- PR: {amounts['pr.xlsx']['exactDocumentMatches']:,}/{amounts['pr.xlsx']['documentsCompared']:,} exact document matches. Workbook total AED {amounts['pr.xlsx']['workbookTotal']:,.2f}; live line total AED {amounts['pr.xlsx']['liveLineTotal']:,.2f}.",
        f"- PO: {amounts['po.xlsx']['exactDocumentMatches']:,}/{amounts['po.xlsx']['documentsCompared']:,} exact document matches. Workbook total AED {amounts['po.xlsx']['workbookTotal']:,.2f}; live line total AED {amounts['po.xlsx']['liveLineTotal']:,.2f}.",
        "- The workbook amounts are tax-inclusive while the exposed line amounts are pre-tax/current. No business approval in this task defines those as interchangeable.",
        "",
        "## Live headline and secondary counts",
        "",
        f"- Distinct resolved documents: **{live['distinctResolvedDocuments']:,}**.",
        f"- Open work items (secondary): **{live['openWorkItems']:,}**.",
        f"- Unresolved approval work items (separate): **{live['unresolvedApprovalWorkItems']:,}**.",
        f"- Documents with parallel approvals: **{live['parallelApprovalDocuments']:,}**.",
        f"- Documents with an F&O live header: **{live['documentsWithLiveHeader']:,}**; missing live headers: **{live['missingLiveHeaderDocuments']:,}**.",
        f"- Approval documents requiring the explicit unmapped label: **{live['approvalUnmappedDocuments']:,}**.",
        "",
        "Stage counts from the blocked candidate model:",
        "",
        "| Stage | Distinct documents |",
        "|---|---:|",
    ])
    for stage, value in sorted(live["stageCounts"].items()):
        lines.append(f"| {stage.replace('|', ' — ')} | {value:,} |")

    lines.extend([
        "",
        "## Approver reconciliation",
        "",
        f"The current comparable population was {rec['approver']['compared']:,}. Classifications: " + ", ".join(f"{key} {value:,}" for key, value in sorted(rec["approver"]["classifications"].items())) + ". `UNRESOLVED-*` work items are not documents and are excluded from the distinct-document count.",
        "",
    ])
    approver_groups = defaultdict(list)
    for row in rec["approver"]["details"]:
        approver_groups[row["category"]].append(f"{row['document']} [{row['workbookUser']} → {', '.join(row['captureUsers']) or 'blank'}]")
    for category, values in sorted(approver_groups.items()):
        lines.append(f"- {category}: " + "; ".join(values))

    lines.extend(["", "## Document-level stage differences", ""])
    for title, rows in (("PR", rec["prStage"]["differences"]), ("PO", rec["poStage"]["differences"])):
        lines.extend([f"### {title}", ""])
        groups = docs_by_reason(rows, ("expectedStage", "liveStage"))
        for reason, documents in sorted(groups.items()):
            lines.append(f"- {reason}: " + ", ".join(documents))
        lines.append("")

    lines.extend(["## PR procurement clock differences over one day", ""])
    for row in rec["prProcurementClock"]["differences"]:
        lines.append(f"- {row['document']}: {row['stage']}; workbook `{row['workbookClock']}`; F&O modified-time seed `{row['liveSeedClock']}`.")

    lines.extend([
        "",
        "## PO workbook stage assumption check",
        "",
        "The exact non-blank PO steps are `LPO sent/shared with supplier` (1,425), `Procurement Manager` (59), `Accounting Manager` (45), `Advance payment request submitted (if applicable)` (10), `Finance and Accounts Director` (2), `CEO` (1) and `PurchTableApproval` (1); 1,434 rows are blank. This confirms there are no hidden workbook sourcing sub-steps, but `PurchTableApproval` still needs an explicit mapping.",
        "",
        "## Problems and risks",
        "",
        "- The live sources cannot truthfully separate `PR in review` from `Sourcing` for shared elements. Line pricing can separate `Priced`, but cannot establish whether an unpriced document is still in review or already sourcing.",
        "- `Submission Status`, `Accepted By/Assign To`, PR RFQ case, PO RFQ number and PO `Created by` have no exposed like-for-like live source for the non-blank counts above.",
        "- Current approval identities do not fully reproduce the older workbook owner. Parallel, reassigned, older-workbook and unexplained cases are listed above.",
        "- A posted packing slip is a receipt event, not a delivery date. Partial receipts create a materially different PO stage result from the workbook's single `LPO sent/shared with supplier` step.",
        "- The cloned `pr-po-proxy` repository's only workflow targets the out-of-scope `pr-po-dashboard-proxy`, not authorised `ssg-prpo-proxy`. It was not run; repository documentation now warns against using it.",
        "",
        "## Files changed",
        "",
        "- `tests/reconcile_workbook_retirement.py` — reproducible, read-only reconciliation.",
        "- `evidence/workbook-retirement-reconciliation.json` — complete machine evidence and document differences.",
        "- `docs/workbook-retirement-change-note.md` and `.html` — unpublished blocked change-note draft.",
        "- Both repositories' `README.md` / `CLAUDE.md` — current truth and deployment guardrails.",
        "- `NOTES.md` — this verdict and evidence.",
        "",
        "## What I did not change",
        "",
        "- No workbook, fallback, snapshot generator, workflow, dashboard logic, email logic, recipient, sender, quiet-mode setting or stage map was removed or changed.",
        "- No write was made to either Dataverse organisation. No Azure resource or app registration was created or changed.",
        "- Neither function app was deployed. Chandan's app, flow, OneDrive and tokens were not touched; only the stale documentation naming his app as the target was corrected.",
        "",
        "## Testing performed",
        "",
        "- Python compile check passed for the reconciliation script.",
        "- One complete read-only reconciliation succeeded against both live organisations and both unchanged workbooks.",
        "- The evidence contains every PR/PO stage mismatch and every PR clock mismatch over one day.",
        "- Verification level: code verified; reconciliation verified live; build not applicable; deployment deliberately not performed; production workbook behaviour unchanged.",
        "",
        "## Remaining risks",
        "",
        "- The operational systems continue moving. The UTC timestamps above identify this exact evidence position.",
        "- The business decision below is required before a safe candidate stage model can be built and tested.",
        "",
        "## Recommended next step",
        "",
        "Waqas must decide whether unpriced documents on shared procurement elements may be reported in one combined `PR in review / Sourcing` stage, or provide another deterministic exposed rule that separates them. After that decision, rerun this reconciliation before implementing any cutover.",
        "",
    ])
    args.target.parent.mkdir(parents=True, exist_ok=True)
    args.target.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
