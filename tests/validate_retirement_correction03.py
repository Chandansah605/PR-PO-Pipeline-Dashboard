"""Validate the checked-in Correction 03 evidence and stakeholder note."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def main() -> None:
    evidence_path = REPO / "evidence" / "workbook-retirement-correction-03.json"
    report_path = REPO / "evidence" / "workbook-retirement-correction-03.md"
    change_note_path = REPO / "docs" / "workbook-retirement-change-note.md"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    p1, p2, p3, p4, p5 = (
        evidence["poAcceptance"][key] for key in ("p1", "p2", "p3", "p4", "p5")
    )

    assert (p1["evidenced"], p1["population"], p1["agreementPercent"], p1["passed"]) == (
        512, 983, 52.09, False
    )
    assert len(p1["differences"]) == 471
    assert Counter(row["reasonCode"] for row in p1["differences"]) == {
        "PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE": 389,
        "NO_LIVE_STAGE_EVIDENCE": 79,
        "STAGE_EVENT_TIMESTAMP_UNAVAILABLE": 3,
    }
    assert all(row["displayedStage"] == "STAGE_NOT_EVIDENCED" for row in p1["differences"])

    assert (
        p2["matchedDistinctDocuments"],
        p2["fAndOOpenDistinctDocuments"],
        p2["passed"],
        len(p2["differences"]),
    ) == (983, 983, True, 0)

    assert (
        p3["workbookApprovalRows"],
        p3["compared"],
        p3["excludedByR1"],
        p3["matched"],
        p3["agreementPercent"],
        p3["passed"],
    ) == (118, 61, 57, 3, 4.92, False)
    assert len(p3["differences"]) == 58
    assert Counter(row["reasonCode"] for row in p3["differences"]) == {
        "PROGRESSION_TIMESTAMP_UNAVAILABLE": 33,
        "PROGRESSION_NOT_AFTER_EXPORT": 16,
        "STAGE_NOT_EVIDENCED": 9,
    }
    assert not p3["progressedAfterExport"]

    assert p4["workbookLpoSentRows"] == 1425
    assert p4["receivedOrInvoicedBusinessCaseCount"] == 1099
    assert (p4["evidenced"], p4["notEvidenced"]) == (1098, 327)
    assert p4["liveStageDistribution"] == {
        "Invoiced": 758,
        "Receipt posted": 341,
        "STAGE_NOT_EVIDENCED": 20,
        "Sent to supplier": 306,
    }

    assert p5["sampleSize"] == p5["targetSampleSize"] == 25
    assert p5["passed"]
    assert set(p5["candidateStagesPresent"]) == set(p5["candidateStagesSampled"])
    assert evidence["stalePopulationLane"]["count"] == 2944
    assert evidence["stalePopulationLane"]["poCount"] == 829
    assert not evidence["verdict"]["canRetireTotally"]

    workbook_hash = hashlib.sha256((REPO / "po.xlsx").read_bytes()).hexdigest()
    assert workbook_hash == evidence["workbook"]["sha256"]

    report = report_path.read_text(encoding="utf-8")
    reported_rows = (
        p1["differences"] + p3["differences"] + p4["notEvidencedRows"] + p5["rows"]
    )
    assert all(row["document"] in report for row in reported_rows)
    assert "| Gate | 7 Sep verdict | Correction 01 | Correction 02 | Correction 03 |" in report

    change_note = change_note_path.read_text(encoding="utf-8")
    for required in ("1,099", "Receipt posted", "Invoiced", "never a delivery date"):
        assert required in change_note

    print("Correction 03 evidence validation passed")


if __name__ == "__main__":
    main()
