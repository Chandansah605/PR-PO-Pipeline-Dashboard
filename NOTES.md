# Dataverse live-read implementation notes

Evidence was collected on 7 September 2026 (Dubai time) from the production Dataverse organisation and the same-day published `pr.xlsx` / `po.xlsx` files. The live system continued changing during the checks, so the recorded counts are a point-in-time snapshot.

## What I found

- The signed-in account can call Dataverse directly. `WhoAmI` returned HTTP 200 and all six required header, line, and approval reads completed with delegated `user_impersonation` access.
- The approval virtual entities are historical work-item rows. They expose an element GUID and work-item RecId, but no status or date. A later RecId is not reliable proof of the current step.
- The published workflow record remains the current-step and step-date guard for records already in the files. The copied GUID maps are used only when a document is absent from the published workflow data.
- F&O ledger dimensions are fixed-position strings with meaningful empty slots. The browser now reads contract, department, and location from positions 1, 3, and 5 without shifting values when an account dimension is present.
- PO numbers are not globally unique: 35 numbers occur in more than one legal entity. No duplicate PR number was found. PO headers and lines are therefore joined by legal entity plus PO number; the same key had no duplicates.
- `mserp_lineamount` is pre-tax. Most workbook totals are tax-inclusive: 2,783 shared PR rows and 2,886 shared PO rows reconcile exactly after applying 5% VAT. The live dashboard deliberately shows the requested direct line value and does not invent a tax amount that the virtual entities do not expose.

## Problems and risks

- The direct approval entities cannot replace the current workflow clock. Removing the published workflow guard would regress stage and ageing accuracy.
- Live status fields can be newer than the daily files. Eight shared PR statuses, two PO approval statuses, and one PO order status differed during the snapshot.
- A small number of populated line dimensions differ because the live line now has a newer or different value: PR department 2, location 4, contract 1; PO location 2. The remaining dimension differences fill fields that were blank in the files.
- Public holidays are not encoded. “Working day” currently means Monday to Friday, matching the task's requested working-day threshold without adding an unmaintained holiday table.

## Files changed

- `index.html` — live source orchestration, automatic fallback, source/date status, cache, warning, and mobile status/filter layout.
- `dataverse-live.js` — read-only paged Dataverse client and record mapping.
- `stepMap.json`, `poStepMap.json` — copied workflow element maps from the companion repository.
- `tests/dataverse-live.test.js` — deterministic mapping, dimension, duplicate-PO, workflow-guard, date, and entity-path checks.
- `tests/live-dataverse-check.js` — read-only live integration and workbook reconciliation check.
- `NOTES.md` — this evidence and handoff record.

## Exact changes made

- The existing dashboard and published workbooks render first. A background request then silently acquires a Dataverse token for the signed-in user and reads all pages from the confirmed plural entity sets.
- A 120-second timeout, visible checking state, three-minute IndexedDB cache, and forced Refresh path handle the F&O virtual-entity cold start without freezing or blanking the page.
- Any token, permission, timeout, network, mapping, or workbook-support failure keeps the file dashboard working and shows `File fallback` plus a plain-English reason.
- The header reports the newest step or created date in the rows actually displayed, in Dubai time, and identifies Live Dataverse, cached live Dataverse, manual file, or file fallback.
- A visible warning appears when the displayed data date is more than one Monday-to-Friday working day old. Today's clock is never presented as the data date.
- Existing stage maps, reconstructed header buckets, SLA thresholds, and step-date-to-created-date ageing fallback are reused unchanged.
- Manual Excel upload remains available. A partial manual upload is paired with the corresponding published workbook, never with live rows.
- No token, client secret, connection string, or live data payload is stored in the repository.

## Same-day source reconciliation

Point-in-time direct read at 12:45 Dubai:

| Measure | Published file | Live Dataverse | Explanation |
|---|---:|---:|---|
| PR rows | 4,394 | 4,405 | 11 live-only rows; no file-only rows |
| PO rows | 2,977 | 3,184 | 207 live-only rows; no file-only rows |
| Shared PR step mismatches | — | 0 / 4,394 | Published workflow guard retained |
| Shared PR step-date mismatches | — | 0 / 4,394 | Published step clock retained |
| Shared PO step mismatches | — | 0 / 2,977 | Published workflow guard retained |
| Shared PO step-date mismatches | — | 0 / 2,977 | Published step clock retained |
| PR line/header/approval rows read | — | 20,639 / 4,405 / 818 | All OData pages |
| PO line/header/approval rows read | — | 14,960 / 3,184 / 16 | All OData pages |

The newest date present in both loaded sources was `2026-09-07T05:06:39Z` (09:06 Dubai). Amount differences are the pre-tax versus tax-inclusive definition described above; source status and newly filled dimensions explain the remaining differences.

## Dashboard distributions

The unchanged file path produced this same-day UI baseline. Live UI values were recorded after GitHub Pages publication in the production-verification section below.

### Published file baseline

| View | Total rows | Live pipeline rows | Header buckets | Departments | Ageing |
|---|---:|---:|---|---|---|
| PR | 4,394 | 586 | Re-Assigned/Rejected 5; Procurement 91; Operations to Confirm 470; Dep Managers 14; Finance 6; Director 0; CEO 0 | Building 394; Cleaning 62; Security 2; Landscaping 30; Concierge 1; FitOut 10; Home Maintenance 70; Others 17 | 0–3: 56; 4–7: 57; 8–14: 63; 15–30: 119; 30+: 291 |
| PO | 2,977 | 793 | Procurement 30; Finance 19; Director 0; CEO 1; Sent to Supplier 538; Pending Invoicing 205 | Building 196; Cleaning 53; Security 4; Landscaping 8; Concierge 6; FitOut 33; Home Maintenance 52; Others 441 | 0–3: 34; 4–7: 34; 8–14: 29; 15–30: 50; 30+: 646 |

## Testing performed

- `node --check dataverse-live.js` — passed.
- `node tests/dataverse-live.test.js` — passed.
- Parsed both inline `index.html` scripts with Node's `vm.Script` — passed.
- `node tests/live-dataverse-check.js` with a short-lived Azure CLI access token — passed all six paged reads and produced the reconciliation above. The token was removed from the process environment immediately afterward.
- Local authenticated-shell test with no Dataverse account — page rendered 586 PR pipeline rows from the current published files and displayed `Dataverse sign-in is unavailable — File fallback is shown.`
- Forced stale-date test using 2 September 2026 — displayed `Warning: this data is 3 working days old.` The page was reloaded afterward.
- Responsive test at 412 × 915 — source/date/warning remained visible, filters used a two-column mobile grid, and the document width stayed within the viewport.
- Desktop test at 1920 × 855 — dashboard, source state, and fallback warning rendered without horizontal overflow.
- `git diff --check` — passed apart from Git's informational LF-to-CRLF working-copy warning.

## Production verification

Pending GitHub Pages publication. This section will be completed from the signed-in production page before final handoff.

## What I did not change

- No Dataverse write, Azure setting, app registration, or `pr-po-proxy` repository change.
- No change to `.github/workflows/*`, `fetch_from_onedrive.py`, `gen_pr_steps.py`, `refresh_data.py`, or `gen_weekly_snapshot.py`.
- No deletion or edit of `pr.xlsx`, `po.xlsx`, `pr_steps.json`, or `weekly_snapshots.json`.
- No change to weekly history, weekly comparison, stage names, stage groupings, `PR_BUCKET_ORDER`, `PO_BUCKET_ORDER`, `PR_HEADER_BUCKETS`, `PO_HEADER_BUCKETS`, `SLA_NORMAL_MAX`, or `SLA_WARN_MAX`.
- No package installation or unrelated refactor.

## Remaining risks

- Current step dates still depend on the published fallback chain until an authoritative, dated current-workflow entity is available.
- First access after an F&O virtual-entity cold start can still take up to two minutes; the file dashboard remains usable during that wait.
- Live figures can move while reconciliation runs because the production system is active.

## Recommended next step

Monitor live-read failures and fallback use after release. Replace the published workflow guard only when Dataverse exposes an authoritative current work item with a reliable timestamp.
