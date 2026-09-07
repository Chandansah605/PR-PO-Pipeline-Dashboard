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

GitHub Pages run `34102463611` built and deployed merge commit `c512c00ffc25d0a52376eb2f84af0726f56fd17e` successfully. A fresh Chrome tab then signed in as the current Microsoft 365 user and completed the browser-side Dataverse read in under 30 seconds.

- Production displayed `Live Dataverse`, 4,405 PR rows, 3,184 PO rows, and `Data date: 07 Sept 2026, 09:06 · Live Dataverse` with no stale warning.
- Reloading within three minutes displayed `Cached live Dataverse` with the same 4,405 / 3,184 rows and data date.
- Forcing the token acquisition to fail in that tab switched automatically to 4,394 / 2,977 published rows, rendered 586 PR pipeline entries, and displayed `Live Dataverse read failed — File fallback is shown.` Reloading restored the cached live source.
- At 412 × 915, the source state remained visible, both sidebar and main content measured 412 pixels wide, and the document had no horizontal overflow.

### Live Dataverse production view

| View | Total rows | Live pipeline rows | Header buckets | Departments | Ageing |
|---|---:|---:|---|---|---|
| PR | 4,405 | 580 | Re-Assigned/Rejected 5; Procurement 92; Operations to Confirm 463; Dep Managers 14; Finance 6; Director 0; CEO 0 | Building 392; Cleaning 62; Security 2; Landscaping 30; Concierge 1; FitOut 9; Home Maintenance 67; Others 17 | 0–3: 56; 4–7: 54; 8–14: 62; 15–30: 117; 30+: 291 |
| PO | 3,184 | 909 | Procurement 29; Finance 22; Director 0; CEO 1; Sent to Supplier 614; Pending Invoicing 243 | Building 395; Cleaning 98; Security 28; Landscaping 19; Concierge 19; FitOut 73; Home Maintenance 89; Others 188 | 0–3: 36; 4–7: 35; 8–14: 30; 15–30: 57; 30+: 751 |

The full-source bucket differences above come from the 218 live-only rows and the few newer status values, not changes to grouping logic. Within shared rows, step and step-date mismatches were both zero for PR and PO; this is the direct same-record verification that stage assignment and ageing bands did not move because of the code change.

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

# Race Control first-screen release — 7 September 2026

## What I found

- The existing first-screen `AVERAGE AGING` KPI used the full filtered record set, including records outside the live pipeline. The source of truth for the requested clock is the existing `livePipelineFilter`, reconstructed header bucket and existing `aging` value.
- The companion `pr-po-proxy/src/functions/prpoEmail.js` personal queue uses the same reconstructed owners, excludes non-person PO stages, and normalises the same named aliases. It was inspected through the GitHub API and was not edited.
- The 6 September snapshot reproduces the quoted email counts for dinesh.laxman 356, shijil.c 61, Gokul.Krishna 46, Aparna.Pauly 33 and Adnan.Ullah 22. It shows roderick.red 30 instead of the email's 31 because `CPR-027356` is the one intended stuck item removed from his count.
- The current published workbooks had moved since that email. At the exact browser timestamp `2026-09-07T10:24:37.065Z`, the fallback holder counts were dinesh.laxman 366, shijil.c 60, Gokul.Krishna 44, roderick.red 35, Aparna.Pauly 29 and Adnan.Ullah 18.
- `PR-000104` is present in the maintained lane but is already outside the protected live-pipeline definition because it has no mapped current step. The other five maintained records are live and excluded. The read-only current Dataverse line check also found `PR-001216` with no returned line, so the live screen correctly shows 7 listed records and 6 active exclusions.

## Problems and risks

- A snapshot generator first pass failed to fall back to the pending approver when an operations-confirmation row used a department outside `DEPT_OPS_USER`. That made three current holder counts disagree with the browser. The fallback was corrected and regression-tested before the historical seeds were regenerated.
- File amounts are tax-inclusive while direct Dataverse amounts are pre-tax, as documented in the earlier source reconciliation. Race Control deliberately displays the value supplied by the active source and labels that source visibly.
- The automatic no-line rule can only be evaluated after the live PR-line query completes. File fallback still shows all six maintained records, but it does not claim an automatic line result.

## Files changed

- `index.html` — makes Race Control the default screen, adds tab navigation and holder drill-through, preserves all secondary views, fixes the sign-in logo path, and wires the read-only line tracker into the existing live load.
- `race-control.js` and `race-control.css` — isolated metrics, exclusions, week-on-week model, rendering and responsive Race Control styling.
- `stuck_items.json` — maintained six-record IT clean-up list with reason, reporter and date.
- `gen_weekly_snapshot.py` and `weekly_snapshots.json` — append holder/header-stage metrics and seed 30 August and 6 September without replacing the existing arrays.
- `strive-logo.svg` — exact official Strive SVG from the approved brand-system asset.
- `tests/race-control.test.js`, `tests/test_weekly_snapshot.py`, `tests/capture-race-control.js`, and `tests/serve-live-race-data.js` — calculation, preservation, screenshot and read-only live verification support.
- `evidence/race-control-desktop.png` and `evidence/race-control-mobile.png` — authenticated file-fallback first-screen evidence at 1440 × 1000 and 412 × 915.

## Exact changes made

- Race Control now opens first and answers, in order: current-step average/median, holder queue, three-position movement, and visible stuck-system records.
- Overall and stage figures use only existing live-pipeline rows. Active stuck documents are removed before all age, count and value aggregation.
- Holder rows use the existing reconstructed pending owner, show items/value/oldest/median/>7 days, and open the existing PR or PO detail table ring-fenced to that holder.
- Week-on-week columns read the live current model plus `raceControl` fields from the two prior Sunday snapshots. Missing historical holder data renders as a dash.
- `createLineTracker` observes the existing paged PR-line requests through response clones. It adds no network query, performs no write and leaves `dataverse-live.js` unchanged.
- The old dashboard, Analysis, heatmap, funnel, daily counts, status distribution and department × bucket views remain behind `PR detail`, `PO detail` and `Analysis` tabs.
- Excel-formatted fallback values such as `1,250.50` are parsed in Race Control without changing the protected workbook/live loader.

## Reconciliation evidence

### File fallback hand calculation

Independent Python calculation at the browser's exact timestamp matched the screen:

| Measure | Browser | Independent generator calculation |
|---|---:|---:|
| Included live action items | 1,374 | 1,374 |
| Total value | AED 27,346,702.94 | AED 27,346,702.94 |
| Average current-step age | 77.0 days | 77.0 days |
| Median current-step age | 70.0 days | 70.0 days |
| Oldest current-step age | 473 days | 473 days |
| Over 7 days | 1,193 | 1,193 |

The unchanged detail views still produced PR 586 and PO 793 live rows. Their header stages remained PR: Re-Assigned/Rejected 5, Procurement 91, Operations to Confirm 470, Dep Managers 14, Finance 6; PO: Procurement 30, Finance 19, CEO 1, Sent to Supplier 538, Pending Invoicing 205. Race Control is lower only by the five maintained records that were active in the fallback source.

### Read-only live Dataverse run

The live query returned 4,407 PR headers / 20,641 PR lines / 814 PR approvals and 3,185 PO headers / 14,962 PO lines / 10 PO approvals. Applying that payload to the new page changed the visible source to `Live Dataverse` without a reload and produced 1,483 included live items, AED 42,251,213.70 value, 86.7-day average, 76-day median and 1,298 items over seven days. The named holder counts after exclusions were dinesh.laxman 360, shijil.c 56, Gokul.Krishna 44, roderick.red 39, Aparna.Pauly 32 and Adnan.Ullah 17.

These later live counts do not equal the morning email because the operational source had moved. The seeded 6 September position proves the shared counting logic against the exact email numbers; the only intended difference is roderick.red's one excluded stuck record.

### Seeded weekly history

- 30 August used repository data from `fd54fa64a757d539afa5ca42cab9253f1cd2eb9c`: 1,360 items, 68-day median, 359 dinesh.laxman items.
- 6 September used repository data from `d1fbf0482684b0f467cd9f8552af30cc28216ad0`: 1,364 items, 71.5-day median, and the email-count reconciliation above.
- A structural comparison against `HEAD:weekly_snapshots.json` found no changed `PR` or `PO` arrays in any existing week. Only the new `raceControl` and `raceControlSource` properties were added to the two seeded weeks.

### Existing journey-board measurement

The unchanged journey-board logic measured 1,329 completed PR → PO journeys. Median raised-to-LPO-sent time was 18 working days against the existing 10-working-day target; 37.5% completed within target. P90 was 90 working days. This confirms the meeting's “18 working days” statement as the measured median, not a target or an arithmetic sum of stage medians.

## What I did not change

- No edit to `dataverse-live.js`, live/fallback/cache/status semantics, live-pipeline definition, stage names, stage groupings or the 3/7-day bands.
- No edit to `.github/workflows/*`, daily email code, workbooks, workflow maps, Dataverse, Azure configuration or app registration.
- No Dataverse write, secret, package installation, deletion of secondary views or rewrite of historical PR/PO snapshot arrays.

## Testing performed

- `node --check race-control.js` and `node tests/race-control.test.js` — passed calculations, aliases, exclusions, currency parsing and response-clone line tracking.
- `python -m py_compile gen_weekly_snapshot.py` and `python tests/test_weekly_snapshot.py` — passed holder/stage metrics, unknown-department owner fallback and history preservation.
- `node --check dataverse-live.js` and `node tests/dataverse-live.test.js` — protected data-layer checks passed unchanged.
- Parsed both inline `index.html` scripts with `vm.Script` — passed.
- `node tests/live-dataverse-check.js` with a short-lived Azure CLI token — passed all six read-only paged Dataverse reads; the token was removed from the process environment afterward.
- `node tests/serve-live-race-data.js 8766` plus browser injection — live payload replaced file figures and identified the automatic no-line item without a Dataverse write.
- Holder click test — dinesh.laxman's row opened PR detail with 366 file-fallback rows ring-fenced to that name.
- First paint — 247 ms from navigation start on published workbooks, below the two-second requirement.
- 412 × 915 browser test — document width 397 px in a 412 px viewport; stage and holder tables each fit their 349 px containers with no page-level horizontal scroll.
- `node tests/capture-race-control.js http://127.0.0.1:8765/ evidence` — produced both required authenticated screenshots.
- `git diff --check` — passed apart from Git's informational LF-to-CRLF working-copy warning.

Screenshot evidence: [desktop](evidence/race-control-desktop.png) and [412 × 915 mobile](evidence/race-control-mobile.png).

## Production verification

- GitHub Pages run `34112020617` deployed commit `23a4d1b0b0d9012919b7372e75101884f7f27b59` successfully to `https://strive-services-group.github.io/PR-PO-Pipeline-Dashboard/`.
- A fresh Chrome visit rendered the official Strive sign-in screen. The real Microsoft `SIGN IN` flow completed using the existing work session and the screen changed to `Live Dataverse`.
- At the production screen's displayed data date of 7 September 2026 09:06, Race Control showed 1,475 included live action items, 87.0-day average, 76.0-day median and 1,290 items over seven days.
- The production holder rows showed dinesh.laxman 360, shijil.c 56, Gokul.Krishna 44, roderick.red 39, Aparna.Pauly 32 and Adnan.Ullah 17. These were read from the authenticated page, not the file fallback.
- The production stage rows showed PR 5 / 97 / 459 / 11 / 2 and PO 30 / 21 / 1 / 615 / 234 in the protected display order.
- The production stuck lane showed all six maintained records plus automatic live no-line item `PR-001216`. Five maintained records and that automatic record were active exclusions; `PR-000104` was correctly labelled `Not in live queue`.
- The production week-on-week board rendered 30 August, 6 September and Live now for overall, holders and stages. Missing historical holder cells rendered as dashes.
- The authenticated production page had no desktop-level horizontal overflow: document and viewport widths were both 1,905 px within the 1,920 px browser viewport.
- The production values changed slightly from the immediately preceding read-only payload replay because Dataverse was active during verification. The source label, timestamp and browser evidence distinguish the two observations.

## Remaining risks

- Current-step dates still use the published workflow overlay when Dataverse has no authoritative current dated work item; this is the protected 87516e3 design.
- Holder and stage figures can change between an email, Sunday snapshot and meeting because Dataverse is operationally active. Each screen position therefore labels its source and snapshot date.
- Live authentication depends on the user's Microsoft session and existing Dataverse permissions; no anonymous data path was added.

## Recommended next step

Align the separate daily-email task to consume the maintained stuck list, then monitor automatic no-line additions with IT before promoting them into the maintained list.
