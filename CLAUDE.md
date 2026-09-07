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

Correction 02 measures the production dashboard population, accepts exact amount equality regardless of tax classification and accepts only timestamp-proven post-export progression. The corrected 7 September 2026 run passes PR stage (95.25%), PR procurement clock (97.45%), PR amount (98.23%) and PO amount (99.02%), but still fails PO stage (44.02%). Do not remove the workbook path or deploy a Dataverse-only replacement until a fresh reconciliation passes every stated gate.

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
- Reproduction script: `tests/reconcile_workbook_retirement.py`
