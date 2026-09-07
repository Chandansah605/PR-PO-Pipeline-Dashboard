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

Correction 01 approves merging `PR in review` into `Sourcing`, makes live line amounts excluding VAT authoritative and uses live PO lifecycle events. The corrected 7 September 2026 run still failed PR stage (89.67%), PO stage (43.68%) and PR amount (81.02%) gates. Do not remove the workbook path or deploy a Dataverse-only replacement until a fresh reconciliation passes every stated gate.

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
- Reproduction script: `tests/reconcile_workbook_retirement.py`
