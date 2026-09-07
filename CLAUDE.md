# PR/PO Pipeline source of truth

## Current production state

- The dashboard and email read the same proxy dataset revision.
- No workbook, workbook generator or workbook fallback is a production data source.
- Browser last-good cache is allowed only when visibly labelled stale.
- `pr.xlsx` and `po.xlsx` are live-generated legacy email outputs only, never data sources; delete them when sending moves to `ssg-prpo-proxy`.

## Live sources assessed

- F&O virtual entities provide current PR/PO headers, lines and packing-slip journals.
- Development Dataverse `ssg_` capture tables provide current approval instances and work items.
- Live Dataverse access for this project is read-only unless separately authorised.

## Retirement gate

Correction 04 replaces P1/P3 with P1a/P1b. P1a and P2 must remain 100%; P1b is a report of live-dated, seeded, first-observed and not-recorded clocks. Stage comes from F&O state or capture, independently from its clock.

## Protected systems

- Deploy only the authorised `ssg-prpo-proxy` function app after a passed cutover.
- Never deploy or modify Chandan's app, flow, OneDrive or tokens.
- Do not change senders, recipients or the `Report quiet mode` behaviour without explicit approval.
- Keep evidence timestamps in UTC and distinguish event, active-age and pending clocks.
- A packing-slip date is a posting date, never a delivery date.

## Evidence

- Human-readable verdict: `evidence/workbook-retirement-report.md`
- Machine reconciliation: `evidence/workbook-retirement-reconciliation.json`
- Correction 01 report: `evidence/workbook-retirement-correction-01.md`
- Correction 01 machine evidence: `evidence/workbook-retirement-correction-01.json`
- Correction 02 report: `evidence/workbook-retirement-correction-02.md`
- Correction 02 machine evidence: `evidence/workbook-retirement-correction-02.json`
- Correction 03 report: `evidence/workbook-retirement-correction-03.md`
- Correction 03 machine evidence: `evidence/workbook-retirement-correction-03.json`
- Correction 04 machine evidence: `evidence/workbook-retirement-correction-04.json`
- Reproduction script: `tests/reconcile_workbook_retirement.py`
