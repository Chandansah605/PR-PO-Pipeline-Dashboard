# PR/PO Pipeline source of truth

## Current production state

- The emailed PR and PO workbooks remain part of the production data path.
- The dashboard must not claim that Dataverse alone reproduces workbook stages.
- The existing workbook fallback, snapshots, scheduled jobs and email behaviour are protected.

## Live sources assessed

- F&O virtual entities provide current PR/PO headers, lines and packing-slip journals.
- Development Dataverse `ssg_` capture tables provide current approval instances and work items.
- Live Dataverse access for this project is read-only unless separately authorised.

## Retirement gate

Correction 03 retires the invalid all-stage PO workbook gate. The settled PR stage (95.25%), PR procurement clock (97.45%), PR amount (98.23%), PO amount (99.02%) and document counts still pass. The replacement PO tests do not: P1 dated-stage evidence is 512/983 (52.09%) and P3 maintained approval-step parity is 3/61 (4.92%); P2 population parity is exact at 983/983. Do not remove the workbook path or deploy a Dataverse-only replacement until P1–P3 pass.

## Protected systems

- Deploy only the authorised `ssg-prpo-proxy` function app after a passed cutover.
- Never deploy or modify Chandan's app, flow, OneDrive or tokens.
- Do not change senders, recipients or the `Report quiet mode` behaviour without explicit approval.
- Keep evidence timestamps in UTC and distinguish event, active-age and pending clocks.

## Evidence

- Human-readable verdict: `evidence/workbook-retirement-report.md`
- Machine reconciliation: `evidence/workbook-retirement-reconciliation.json`
- Correction 01 report: `evidence/workbook-retirement-correction-01.md`
- Correction 01 machine evidence: `evidence/workbook-retirement-correction-01.json`
- Correction 02 report: `evidence/workbook-retirement-correction-02.md`
- Correction 02 machine evidence: `evidence/workbook-retirement-correction-02.json`
- Correction 03 report: `evidence/workbook-retirement-correction-03.md`
- Correction 03 machine evidence: `evidence/workbook-retirement-correction-03.json`
- Reproduction script: `tests/reconcile_workbook_retirement.py`
