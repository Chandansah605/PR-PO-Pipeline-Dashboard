"""Seed the PO stage clock once in operations-ifahr-dev.

Default mode is read-only. --apply writes only ssg_prpodocument rows using the
composite F&O legal-entity/document key recorded by correction 04.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import reconcile_workbook_retirement as base


PREFIX = "ifahr-live|PO|"


def compact_json(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def patch(token: str, key: str, payload: dict) -> None:
    literal = urllib.parse.quote(key.replace("'", "''"), safe="|-_")
    url = f"{base.DEV}/api/data/v9.2/ssg_prpodocuments(ssg_documentkey='{literal}')"
    request = urllib.request.Request(
        url,
        method="PATCH",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            if response.status not in {200, 201, 204}:
                raise RuntimeError(f"unexpected Dataverse status {response.status}")
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:800]
        raise RuntimeError(f"Dataverse seed failed for {key}: {error.code} {detail}") from error


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    token = os.environ.get("PRPO_DEV_TOKEN")
    if not token:
        raise SystemExit("PRPO_DEV_TOKEN is required")

    evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    rows = evidence["poAcceptance"]["p1b"]["rows"]
    if len(rows) != evidence["poAcceptance"]["p1a"]["population"]:
        raise SystemExit("P1a/P1b population mismatch")
    if any(row["liveStage"] == "STAGE_NOT_EVIDENCED" for row in rows):
        raise SystemExit("Refusing to seed: P1a contains STAGE_NOT_EVIDENCED")

    existing = base.api_all(base.DEV, token, "ssg_prpodocuments", [
        "ssg_documentkey", "ssg_documentnumber", "ssg_legalentity",
        "ssg_currentstepname", "ssg_observedpendingsince", "ssg_stepenteredon",
        "ssg_dataqualitynotes", "ssg_payloadhash", "ssg_sourceupdatedon",
    ], f"startswith(ssg_documentkey,'{PREFIX}')")
    # The approval capture already owns legacy keys shaped
    # ifahr-live|PO|<document>. Correction 04 exclusively owns the legal-entity
    # composite shape ifahr-live|PO|<company>|<document>.
    existing_by = {
        row["ssg_documentkey"]: row for row in existing
        if str(row.get("ssg_documentkey") or "").count("|") == 3
    }
    applied_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    writes = []
    for row in rows:
        key = f"{PREFIX}{str(row['legalEntity']).strip().lower()}|{row['document']}"
        notes = {
            "schema": "PRPO_STAGE_CLOCK_V1",
            "stage": row["liveStage"],
            "clockProvenance": row["clockProvenance"],
            "workbookValue": row.get("workbookValue"),
            "workbookExportTimestamp": row.get("workbookExportTimestamp"),
            "liveEvent": row.get("event"),
        }
        notes_text = compact_json(notes)
        payload = {
            "ssg_documentkey": key,
            "ssg_name": f"{row['legalEntity']} {row['document']}"[:100],
            "ssg_documentnumber": row["document"],
            "ssg_documenttype": "PO",
            "ssg_legalentity": str(row["legalEntity"]).strip().lower(),
            "ssg_sourceenvironment": "ifahr-live",
            "ssg_sourceentity": "F&O PO lifecycle stage observation",
            "ssg_currentstepname": row["liveStage"],
            "ssg_sourceupdatedon": applied_at,
            "ssg_dataqualitystatus": "Complete",
            "ssg_dataqualitynotes": notes_text,
            "ssg_isreportable": True,
            "ssg_payloadhash": hashlib.sha256(notes_text.encode("utf-8")).hexdigest(),
        }
        if row.get("clockTimestamp"):
            payload["ssg_observedpendingsince"] = row["clockTimestamp"]
        if row["clockProvenance"] == "LIVE_EVENT_DATE" and row.get("clockTimestamp"):
            payload["ssg_stepenteredon"] = row["clockTimestamp"]
        writes.append({"key": key, "payload": payload, "clockProvenance": row["clockProvenance"]})

    missing = []
    already_seeded = []
    for item in writes:
        old = existing_by.get(item["key"])
        if not old:
            missing.append(item)
        elif (old.get("ssg_currentstepname") == item["payload"]["ssg_currentstepname"]
              and old.get("ssg_payloadhash") == item["payload"]["ssg_payloadhash"]):
            already_seeded.append(item)
        else:
            raise SystemExit(
                f"Refusing to overwrite an existing stage observation: {item['key']} "
                f"({old.get('ssg_currentstepname')} / {old.get('ssg_payloadhash')})"
            )

    if args.apply:
        for index, item in enumerate(missing, 1):
            patch(token, item["key"], item["payload"])
            if index % 100 == 0:
                print(f"seeded {index}/{len(missing)}", flush=True)

    counts = {}
    for item in writes:
        name = item["clockProvenance"]
        counts[name] = counts.get(name, 0) + 1
    output = {
        "generatedAt": applied_at,
        "mode": "APPLIED" if args.apply else "DRY_RUN",
        "sourceEvidence": str(args.evidence.name),
        "sourceEvidenceSha256": hashlib.sha256(args.evidence.read_bytes()).hexdigest(),
        "existingRowsBefore": len(existing_by),
        "plannedRows": len(writes),
        "appliedRows": len(missing) if args.apply else 0,
        "alreadySeededRows": len(already_seeded),
        "clockCounts": counts,
        "seededRows": [
            {
                "key": item["key"],
                "stage": item["payload"]["ssg_currentstepname"],
                "clockTimestamp": item["payload"].get("ssg_observedpendingsince"),
                "workbookValue": json.loads(item["payload"]["ssg_dataqualitynotes"])["workbookValue"],
                "workbookExportTimestamp": json.loads(item["payload"]["ssg_dataqualitynotes"])["workbookExportTimestamp"],
                "flag": "SEEDED_FROM_FINAL_WORKBOOK",
            }
            for item in writes if item["clockProvenance"] == "SEEDED_FROM_FINAL_WORKBOOK"
        ],
        "beforeRows": existing,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in output.items() if key not in {"seededRows", "beforeRows"}}, indent=2))


if __name__ == "__main__":
    main()
