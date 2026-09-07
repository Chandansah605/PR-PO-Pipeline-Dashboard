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

The 7 September 2026 reconciliation could not separate workbook `PR in review` from `Sourcing` for shared workflow elements. It also measured PR stage agreement below 95% and material PO stage differences. Do not remove the workbook path or deploy a Dataverse-only replacement until Waqas approves a deterministic mapping and a fresh reconciliation passes every stated gate.

## Protected systems

- Deploy only the authorised `ssg-prpo-proxy` function app after a passed cutover.
- Never deploy or modify Chandan's app, flow, OneDrive or tokens.
- Do not change senders, recipients or the `Report quiet mode` behaviour without explicit approval.
- Keep evidence timestamps in UTC and distinguish event, active-age and pending clocks.

## Evidence

- Human-readable verdict: `evidence/workbook-retirement-report.md`
- Machine reconciliation: `evidence/workbook-retirement-reconciliation.json`
- Reproduction script: `tests/reconcile_workbook_retirement.py`
