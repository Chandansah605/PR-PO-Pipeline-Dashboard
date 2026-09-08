# Journey board extension preview — 8 September 2026

## What I found

- `journey-board.html` already contained the CEO-approved page-one composition, but its live bridge received only a derived object from `index.html`. That object does not contain CRM quote fields, the PO receiving warehouse or line-level PR lineage. `index.html` is protected in this task, so the extension uses an embedded, reproducible snapshot and keeps the existing bridge intact.
- The existing Entra application `8a4338bf-6c78-4a70-9c62-478bb19b171c` already has the Dynamics `user_impersonation` delegated permission (`78ce3f0f-a1ce-49c2-8cde-64b5c0896db4`). A read-only `WhoAmI` call to `operations-ifahr-live.crm15.dynamics.com` returned HTTP 200. The board therefore reuses the signed-in Microsoft session for a silent Dynamics token; no proxy change or second sign-in is required.
- The current live data moved during implementation. The final frozen dataset was generated at **8 September 2026 15:45 Dubai** and the CRM/F&O extension read completed at **15:46 Dubai**. Counts below belong to proxy revision `9b557938c95b55caf5371a496a4328a53a7b4a53c97e8700f820568c4b1ba679` unless stated otherwise.
- The CRM exact join is real: `quotes.ssg_prnumber` maps requisition number to quote; Q-7097 maps to CPR-000004. The builder chooses the row matching both requisition number and quotation reference, then uses the most recently modified exact duplicate only when CRM contains duplicated quote rows. No fuzzy match is used.
- The supplied 831-record legacy exclusion is a historical board rule, not the size of today's open pre-April population. Removing the date/exclusion rule restores every resolvable open CPR. At the final read there were 758 open CRM-born CPRs: 753 exact quote matches and five unresolved. Of 258 still-open pre-April CPRs, 253 matched and five remained unresolved. Of 757 populated quote references, 753 resolved.
- The quote supplies department, community project/location, division, customer, scope, quoted value, total cost and its cost-calculation timestamp. For matched CPRs the snapshot takes department and location from CRM first and retains F&O only as a fallback.
- The W001 store definition reconciled exactly inside the final read: 948 total = 204 open + 48 received awaiting invoice + 685 invoiced + 11 cancelled. The two-order increase from the supplied 946/202 measurement was live source movement; received, invoiced and cancelled were unchanged. The same header read contained 2,252 non-store orders, 3,200 total.

## Problems and risks

- F&O has never supplied the approval step, step date or holder. The three-minute approval capture is the only source for the middle gates after 7 August. If capture stops, the middle must go dark rather than age from a guessed event.
- Pre-7-August clocks can only be the one-time final-workbook seed or `not recorded`. The supplied audit found 67 orders without a start and 35 placeholder starts on 1 January 1900; both remain visible exclusions from medians and are never converted to zero.
- PR-to-PO lineage remains incomplete. The supplied 983-row audit linked 743 rows and found 11 order numbers associated with more than one requisition. The refreshed legal-entity-plus-order read linked 740 of 993 current open orders: PO-line route 739, requisition-BI route 740, union 740, 253 unresolved. No current composite order key had multiple requisitions. Both facts are shown; no conversion figure is published.
- The browser automation surface blocked `file://` navigation under its URL safety policy. I did not bypass that restriction. Offline safety, parsing, interactions and data invariants were verified structurally; a final human visual pass of the local file remains prudent before approval.

## Files changed

- `journey-board.html` — preserved wallboard shell, added clock ownership, honesty, division/store circuits, department expansion, filters and record drill.
- `journey-preview.html` — generated self-contained 1,016,603-byte offline review snapshot with 1,869 actionable records and no external scripts or styles.
- `scripts/build_journey_preview.mjs` — repeatable read-only snapshot builder using the proxy, exact CRM quote join, W001 header filter and both line routes.
- `tests/journey-board-extension.test.js` — offline, reconciliation, department, drill, owner, clock and filter regression checks.
- `NOTES.md` — source route, point-in-time figures, assumptions and verification.

## Exact changes made

- Kept the existing 1920 × 1080 layout, Montserrat/Gotham fallback stack, Strive colour tokens, headline, trend, main circuit, Pit Wall and existing copy. Added one compact sequence/honesty strip and reused the same circuit/card geometry.
- Removed the stale “until then excluded” message. Pit Wall now states **753 recovered / 5 unresolved** for the 758 open CRM-born requisitions and explicitly says the 831-record legacy exclusion is removed.
- Replaced the five mixed division/type rows at snapshot application with Facilities Management, Home Services, FitOut Solutions, Factory — Head Office, explicit Division not recorded, and Store orders. Each opens to canonical departments; zero-current departments remain visible instead of disappearing.
- Department rows use the same maximum elapsed-time scale as their parent division rows. Store rows use the same card footprint but label their four sections as lifecycle counts, not elapsed time.
- Added an in-board modal with document number, what it is, gate, holder, waited time, value excluding VAT and next action. Filters cover circuit, work type, gate and text search. Missing and numeric-only owners are normalised to lowercase `not recorded`.
- Drew the full corrected sequence as three explicitly owned bands: procurement through price-back-to-CRM, customer through LPO/won, and delivery through invoice. Contracted work is labelled as having no customer quote; only variations start in CRM.
- Added five always-visible honesty cards for capture dependency, pre-August seeds, unmapped approvals, invalid/missing PO starts, line coverage and conversion withholding.
- `journey-board.html` keeps the normal parent data bridge. Its frozen enrichment renders immediately and its same-session silent token check uses the registered Dynamics delegated scope; failure leaves the clearly stamped snapshot instead of a blank board.

## What I did not change

- `main`, `index.html`, `journey-live.html`, the live site, GitHub Pages, sign-in behaviour, daily emails, workflow capture, `pr.xlsx`, `po.xlsx`, and `.github/workflows/publish-legacy-email-workbooks.yml` were not changed.
- No Azure Function, Dataverse row, app registration, permission, production setting or source workbook was changed.
- No Basit export, fuzzy quote match, guessed owner, customer-clock duration or PR-to-PO conversion was introduced.
- The supplied headline/trend values remain the approved frozen cohort; the new circuit rows are explicitly labelled as current-gate age so an incomplete line link cannot masquerade as end-to-end conversion.

## Testing performed

- `node scripts/build_journey_preview.mjs` — passed; acquired a read-only Dynamics token, rebuilt exact quote/store/line measures and generated both embedded snapshots.
- `node --test tests/*.test.js` — **30 of 30 passed**, including seven new journey extension tests and all protected sign-in/data/race-control tests.
- Parsed all six inline scripts in `journey-board.html` and all seven in `journey-preview.html` with `vm.Script` — passed.
- `node --check scripts/build_journey_preview.mjs` — passed.
- `git diff --check` — passed; only the existing Git line-ending notice appeared.
- Offline inspection — preview is 1,016,603 bytes, contains no external `<script src>` or `<link href>`, has the preview guard set before rendering, embeds every required record, and carries the top snapshot stamp.
- Protected-file hash comparison against starting commit `451a85e65dc14d787b84fab434a27d984f485f29` — `index.html`, the workbook workflow, sign-in script, `pr.xlsx` and `po.xlsx` all matched exactly.

## Remaining risks

- Counts are point-in-time and the source was actively changing; rebuilding the preview later will legitimately change them.
- Direct visual automation of the offline file was not available because the browser safety layer blocks local-file URLs. The HTML and interaction contracts passed, but Waqas should still open `journey-preview.html` locally for the approval viewing pass.
- The CRM quote-line `modifiedon`/cost-calculation date is displayed only as evidence of the price-back handover. It is not treated as an approval event or charged to procurement after the handover.

## Recommended next step

Open `journey-preview.html` locally and review the unchanged board composition plus each division/store department drill. If approved, merge/deploy can be authorised separately; this branch does neither.

---

# Sign-in empty-straight correction — 8 September 2026

## What I found

- `signin-lights-out.js` was the only runtime consumer of the rear-view car. It selected, decoded, tinted, positioned, reflected, shadowed and drew the image. The only other active references were assertions in `tests/signin-lights-out.test.js`; no dashboard, email, authentication or data path used any file under `assets/car/`.
- The large gantry title had no relationship to the DOM headline bounds, so an approaching sign could draw its stage name through `PR / PO PIPELINE`.
- `flash=1` triggered a translucent full-canvas fill both at lights-out and at every passed gantry. That was the pale wash visible in the recording.
- The lamp lenses used maroon colours even when off, while the lit treatment lacked a separate white core, glass rim and broad bloom.
- `run()` reset the button to `Sign in with Microsoft`, then the release and reduced-motion paths changed it to `Lights out · Sign in`.
- The protected popup/redirect implementation from `bd667e9` remains in `index.html`; none of its MSAL lines needed a change.

## Files changed

- `signin-lights-out.js` — empty-straight composition, headline mask, local track sweep, glass lamps and stable button label.
- `tests/signin-lights-out.test.js` — no-car, title-mask, night-transition, lamp and label regression guards.
- `assets/car/` — all seven unused car files deleted, 953,959 tracked bytes removed.
- `evidence/signin-empty-straight/` — reproducible measurement/capture harness, metrics, full sequence and three required frames.
- `NOTES.md` — implementation, measurements, frames and production verification.

## Exact changes made

- Removed car source selection, image loading/decoding, texture tinting, position, sway, contact shadow, reflection, light pool, speed streaks, state reporting and every image draw.
- Deleted `car-front-900.webp`, four rear-view files and both side-view files. `assets/car/` no longer exists in the repository.
- Widened the road from 110 to 122 world units and added paired steel-blue perspective guides. The centre stripe, kerbs, walls and five gantries now form a deliberate empty launch corridor instead of framing a missing object.
- Measured the DOM hero on resize. Gantry titles have zero opacity until the whole sign top is below the headline safe boundary, then fade in over the next 42 pixels. Lamps and gantry structure can pass behind the headline, but stage wording cannot.
- Replaced the full-frame flash with a narrow, low-alpha steel-blue sweep clipped to the road polygon. The camera shake and speed lines still deliver the release without lifting the night sky, UI or whole frame.
- Rebuilt each lamp as black housing, dark neutral glass, cool rim and restrained specular highlight when off. Lit lamps add a white core, red lens, bright rim and radial bloom. The existing five timers still fill left-to-right; the single release callback sets `lit=0`, so all five extinguish together.
- Kept `Sign in with Microsoft` in the initial, running, release and reduced-motion states. The release still adds the existing `go` emphasis without changing text.

## Protected behaviour

- The clock, race/session/lap chip, sector chips, session-target strip, gantry stage names/order and `Race Control · Procurement · Head office is the engine` line are unchanged.
- MSAL client/tenant/scopes, popup selection, popup-to-redirect fallback, redirect-return handling, session keys and sign-out are unchanged.
- Everything outside `signin-lights-out.js`, its focused tests/evidence, the deleted assets and this note is unchanged.
- The cancelled tyre-movement task was not implemented; no wheel or tyre animation exists.

## Measurements

The checked-in harness opened an isolated Chrome 152 page at an exact 1920 × 1080 foreground document viewport and DPR 1. Its dedicated seven-second performance pass recorded 420 frames over 6,999.9 ms: **60.001 fps**, 16.7 ms median, 16.9 ms p95, 17.1 ms maximum and zero frames above 20 ms. Canvas CSS and backing dimensions were both 1920 × 1080.

Average scene luminance was sampled from a 64 × 36 downsample every 100 ms through the complete sequence. Resting luminance was 13.315 on a 0–100 scale; the maximum was 14.644. The largest rise was therefore **1.329 luminance points**. There is no full-frame transition draw; the only transition overlay is clipped to the road.

The full-resolution lamp-panel crops contained zero bright-red pixels at rest, 4,428 with three lamps lit, and zero at lights-out. This confirms dark glass when off, a high-contrast lit state, and simultaneous extinction. Runtime sampling observed only `Sign in with Microsoft`.

Reduced-motion emulation produced the immediate released state with five completed sector chips, zero animation frame, an active Dubai clock and the same sign-in label. Freezing the page produced a `visibilitychange` state with both animation and clock stopped. The normal foreground path resumed as before.

## Full sequence capture

![Full empty-straight start sequence](evidence/signin-empty-straight/full-sequence.webp)

## Required frames

### Rest — five dark glass lamps

![Empty straight at rest](evidence/signin-empty-straight/rest.jpg)

### Mid-transition — three lamps lit

![Empty straight with three lit lamps](evidence/signin-empty-straight/mid-transition.jpg)

### Lights-out — all lamps extinguished and acceleration underway

![Empty straight at lights-out](evidence/signin-empty-straight/lights-out.jpg)

## Testing performed

- `node --check signin-lights-out.js` — passed.
- `node --test tests/signin-lights-out.test.js tests/auth-flow.test.js` — 20 of 20 focused scene/auth tests passed.
- `node evidence/signin-empty-straight/measure-sequence.js http://127.0.0.1:43991/` — generated the sequence evidence and measurements above.
- 1920 × 1080 visual review — empty composition, dark/lit lamps, release, title clearance and fixed label checked.
- 390 × 844 visual review — no horizontal overflow; action, headline, chips and panel remained legible and usable.
- `node --test tests/*.test.js` — all 23 repository tests passed.
- `gh run watch 34216826141 --exit-status` — the GitHub Pages Jekyll build, deploy and status jobs all passed for implementation commit `323c4f13f4f7cbb1fe20c9f60bf3983988acf8cf`.

## Production verification

- Production `index.html` and `signin-lights-out.js` returned HTTP 200. The deployed script contains the empty-road composition and clipped track sweep, and contains no car asset path, car draw function or alternate sign-in label.
- All seven former `assets/car/` URLs returned HTTP 404 after deployment.
- A normal Chrome window was signed out, then the deployed `Sign in with Microsoft` action completed through the existing Microsoft popup/SSO path. The popup closed, the production overlay became `login-overlay hidden`, and Race Control rendered.
- A separate named popup-style Chrome window loaded the deployed page signed out. Its sign-in action used the protected same-window redirect path, returned to the registered GitHub Pages URI with `strive_auth=true`, hid the overlay and rendered Race Control.
- No credential, token or authentication-dialog content was read, entered or recorded. The existing browser work session completed both provider round trips.

## Brand check

This remains a Strive Services Group interface. The change reuses the existing Steel blue `#618FB4`, light steel blue `#9CC0E0`, deep ocean blue `#145A95`, white and night-navy scene tokens. The official inline Strive logo geometry and every logo colour/effect remain untouched. Desktop and mobile were checked; no brand-font or asset limitation was introduced.

---

# Dead source-column correction — 8 September 2026

## What I found

- Six source fields used by the screen cannot provide the values the UI expected: `Submission Status`, `Accepted By/Assign To`, `Request for quotation case`, `Purchase type`, `RFQ number`, and `Created by`. The supplied 820-row PR and 983-row PO snapshots had no populated values in those columns.
- `Preparer` is not a displayable owner. In the supplied PR snapshot, 753 of 820 rows were `000000`; the other 67 rows contained five distinct personnel numbers. All five numbers matched `mserp_hcmworkerbientities`, but that entity exposes only personnel number and person RecId. The available person/name entity sets returned zero rows, so none of the five could be resolved to a name.
- The old `No RFQ issued` card selected a Procurement-stage requisition older than seven days when `Request for quotation case` was blank. Because that field was blank everywhere, it measured stage membership and age rather than missing quotation activity. Basit's own pre-cutover export also had RFQ case blank on all 802 open requisitions, so the finding was wrong before the cutover as well as after it.
- `Quotation reference` is a populated, document-level source signal. It is the only honest available substitute for whether quotation activity was recorded, so the card is now `No quotation recorded` and uses that field.
- No purchase-order header route provides requisition lineage: `po.xlsx` had a requisition number on 0 of 983 supplied rows, and the live purchase-order header entity does not expose one.

## Purchase-order to requisition join audit

The line-level entity check was read-only against the production Dataverse organisation. Counts below use all 983 rows in the supplied open-order workbook; that file contains 961 distinct purchase-order numbers because 22 rows repeat an order number.

| Route tested | Joined workbook rows | Joined distinct orders | Finding |
|---|---:|---:|---|
| `po.xlsx` `Purchase requisition` | 0 / 983 | 0 / 961 | Column is wholly empty |
| Live PO header entity | 0 / 983 | 0 / 961 | No requisition field is exposed |
| `mserp_purchaserequisitionlinev2entities` | 0 / 983 | 0 / 961 | No purchase-order field is exposed |
| `mserp_purchreqlinebientities` | 743 / 983 | 728 / 961 | Joined through requisition BI header source key |
| Purchase-order line entity | 742 / 983 | 727 / 961 | Joined through `mserp_purchaserequisitionid` |
| Union of the two usable line routes | 743 / 983 | 728 / 961 | 240 workbook rows remain unlinked |
| Basit's daily export, supplied finding | 469 / 983 | not supplied | 887 orders appear; 469 carry a requisition |

An authoritative purchase-order-to-requisition join therefore exists in live line data, but it is incomplete: the union covers 75.6% of the supplied workbook rows, leaves 240 unlinked, and maps 11 distinct orders to more than one requisition. Where both live line routes return a link, their requisition sets agree; the BI route adds one order cohort missed by the PO-line route. This is not reliable enough to publish a root-to-fruit conversion journey, so no conversion count or order-to-requisition link is displayed.

## Problems and risks

- Treating a blank unavailable source column as a business exception creates false counts.
- Showing `000000`, a personnel number, or an empty owner implies knowledge the source does not contain.
- A journey conversion built from the current line join would silently exclude 24.4% of supplied rows and would need a defined rule for orders linked to multiple requisitions.
- The source files are refreshed independently of code deployments. While this correction was being rebased, automation commit `52b8d76` refreshed PR from 820 to 821 rows and PO from 983 to 984 rows. That refresh was not produced by this change.

## Files changed

- `index.html` — removed dead display/calculation paths, corrected owner fallback and quotation exception, and withheld incomplete journey metrics.
- `divisions.html` — removed dead owner inputs from the daily-email display path and made unresolved owners explicit.
- `race-control.js` — canonicalised unavailable owners to `not recorded` and excluded that placeholder from person rankings.
- `tests/dead-source-columns.test.js` — guards against reintroducing the dead source fields or invalid journey labels.
- `tests/live-display-check.js` — compares the pre-change and current UI models against one live dataset revision.
- `tests/race-control.test.js` — covers blank, zero, and personnel-number owner fallbacks.

## Exact changes made

- Replaced `No RFQ issued` with `No quotation recorded`. It now selects requisitions in Procurement, Sourcing, or Priced — awaiting approval that are older than seven days and have no `Quotation reference`.
- Removed displayed RFQ-issued and PO-created funnel steps. The remaining `Procurement activity` panel presents PR and PO activity separately and explicitly says PR-to-PO conversion is withheld because lineage is incomplete.
- Removed the visible linked-PR and purchase-type PO fields, filters, cells, and exports. The dormant journey sub-tabs are not rendered or initialised.
- Removed `Preparer`, `Accepted By/Assign To`, and `Created by` as owner inputs. PR ownership now uses only the captured pending approver; PO approval stages use the pending approver and supplier-side stages use the vendor.
- Every blank, all-zero, or numeric-only unresolved owner renders lowercase `not recorded`. The race-control summary says `Owner not recorded in source`, and the placeholder is excluded from person rankings.
- The Ops confirmer mapping, live data path, approval capture, seeded-clock treatment, sign-in implementation, amounts, stages, and reconciled counts were left intact.

## What I did not change

- `pr.xlsx`, `po.xlsx`, and `.github/workflows/publish-legacy-email-workbooks.yml` were not edited by this correction.
- The workbook headers and column order remain the publishing contract, including the intentionally empty legacy columns.
- No source render, package, API write, Dataverse row, sign-in file, stage mapping, amount formula, or seeded clock was changed.
- I did not publish the partial line-level join as a journey metric. A business rule and better source coverage are required first.

## Regression and display figures

`tests/live-display-check.js` evaluated the pre-change UI logic and the corrected UI logic against the same live dataset revision, `7ecdc5a3eaf68d6f26ae646cecdc2022f959525745c5e09e85a276c4ef328b6f`. The figures below were identical before and after:

| Measure | Before | After |
|---|---:|---:|
| Loaded PR rows | 4,422 | 4,422 |
| Loaded PO rows | 3,189 | 3,189 |
| Open PR rows | 824 | 824 |
| Open PO rows | 984 | 984 |
| PR amount | AED 49,016,441.25 | AED 49,016,441.25 |
| PO amount | AED 52,630,137.30 | AED 52,630,137.30 |
| Open PR amount | AED 15,392,219.32 | AED 15,392,219.32 |
| Open PO amount | AED 37,694,491.25 | AED 37,694,491.25 |
| PR stages | Sourcing 267; Priced 555; Dep Managers 2 | unchanged |
| PO stages | Procurement 84; Receipt posted 510; Sent 384; Director 2; Finance 4 | unchanged |

The corrected owner model produced zero blank owners, zero `000000` owners, zero numeric-only owners, and 82 explicit `not recorded` owners. The corrected production exception shows **39** requisitions and **AED 5,455 excl. VAT**.

## Workbook-shape verification

The original supplied 820-row/983-row headers were captured before implementation. After deployment, both GitHub Pages workbooks opened with `openpyxl`; a header-array diff against the baseline was empty. The independently refreshed production files now contain 821 PR rows and 984 PO rows.

- `pr.xlsx`: 18 headers, 92,122 bytes, SHA-256 `699E59579F7B1028B6FCC1AB1D6FE8209BBF67DE1A20318F5563A9A7ACA741B8`.
- `po.xlsx`: 20 headers, 90,222 bytes, SHA-256 `09484D9C79353BD407B2ABA1CEBA4E009DAA9F280B3AAD58EE88B8A7ADA7C2E9`.
- PR header order remains: Purchase requisition; Quotation reference; Name; Preparer; Status; Created date; Submitted date; Requisition purpose; Submission Status; Accepted By/Assign To; Department; Location; Contract; Request for quotation case; Total amount; Pending Approver/User; Step name; Step date and time.
- PO header order remains: Purchase order; Vendor account; Invoice account; Vendor name; Purchase type; Approval status; Purchase order status; Currency; Requested receipt date; Created date and time; Purchase requisition; RFQ number; Total amount; Department; Location; Contract; Pending Approver/User; Step name; Step date and time; Created by.

## Production screenshots and verification

- Before: the authenticated Analysis view showed `RFQ issued 0`, `PO created 0`, and `No RFQ issued 0 / AED 0`, despite the structural source failure.
- After: the authenticated production Analysis view showed `Procurement activity` with separate PR and PO measures, no RFQ-issued or PO-created step, and `No quotation recorded 39 / AED 5,455`.
- Both 1904 × 900 browser captures were taken in the authenticated production session during this run. They are verification evidence in the Codex task, not repository artifacts.
- The deployed PO data contains visible `not recorded` owner treatments. A literal `000000` can still occur inside a legitimate purchase-order identifier such as `P0000000009`; owner assertions independently confirm that it never appears as an owner.
- GitHub Pages build/deploy/report run `34211439606` completed successfully for implementation commit `26b195bd36db05930593e66a57f4b48729845f32`.

## Testing performed

- `node --test tests/*.test.js` — 20 of 20 tests passed, including authentication redirect, sign-in DPR/car/lights, live proxy, dead-field guards, and owner behaviour.
- `node tests/live-display-check.js` — live before/after regression passed with identical counts, amounts, and stages; corrected owner and quotation checks passed.
- `node --check race-control.js` and `node --check dataverse-live.js` — passed.
- Parsed both inline `index.html` scripts and the inline `divisions.html` script with Node `vm.Script` — passed.
- `git diff --check` — passed apart from informational LF-to-CRLF working-copy warnings.
- Direct read-only Dataverse OData audit — tested worker/person and all requested requisition/PO line routes; counts are recorded above. No writes were made.
- `gh run watch 34211439606 --exit-status` — production GitHub Pages build and deployment passed.
- Downloaded both deployed workbooks, opened them with `openpyxl`, and compared their header arrays with the captured baseline — passed with an empty diff.
- The repository has no local package manifest or production build command. The production build is the GitHub Pages/Jekyll job, which passed.

## Remaining risks

- Line-level requisition lineage remains incomplete and ambiguous for some orders. It must not be used for an executive conversion metric without a settled business rule and improved source coverage.
- If F&O later exposes person names or a complete lineage entity, the UI can be extended after a fresh metadata and coverage audit. Personnel numbers must not be presented as names.

## Recommended next step

Keep the corrected quotation-reference exception and explicit owner fallback. Treat the PR-to-PO journey as unavailable until a source can cover all in-scope orders and a rule is agreed for orders linked to multiple requisitions.

---

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

---

# Workbook retirement verdict — 7 September 2026

## Verdict

**Cannot retire.** The mandatory cutover gates failed. The current workbook path remains intact and no live replacement was deployed.

The decisive business blocker is `PR in review`: current capture element `f51900e9-7be4-4b68-9974-a08f70dedaa6` is shared by 30 workbook `PR in review` documents, 109 `Sourcing` documents and 297 `Priced — awaiting approval` documents. Four other current elements also mix `PR in review` with `Sourcing` or `Priced`. The addendum says to stop rather than merge `PR in review` into `Sourcing` without Waqas's decision.

The measured PR stage agreement was 85.64% (489/571), below the 95% gate. The procurement clock passed at 95.92% (541/564) within one day. PO stage agreement was 28.80% (430/1493); posted packing slips classify many still-open orders differently from the workbook.

## Read-only source evidence

| Source | Rows/documents |
|---|---:|
| Last PR workbook | 4,394 documents |
| Last PO workbook | 2,977 documents |
| Live F&O PR headers / lines / BI headers | 4,413 / 20,700 / 4,413 |
| Live F&O PO headers / lines / packing-slip journals | 3,188 / 14,977 / 3,868 |
| Approval capture snapshots / current work items | 1,780 / 1,430 |
| Resolved distinct documents / unresolved work items | 924 / 221 |

- Dataset generated: `2026-09-07T13:13:21.277070Z`.
- F&O read completed: `2026-09-07T13:13:21.277070Z`.
- Approval capture reconciled: `2026-09-07T13:12:22Z`.
- Effective data time (oldest required source): `2026-09-07T13:12:22Z`; capture age 0.99 minutes.

## Workbook column replacement evidence

### `pr.xlsx`

| Workbook column | Proposed live source | Non-blank | Compared | Matched | Agreement |
|---|---|---:|---:|---:|---:|
| Purchase requisition | F&O PR header | 4,394 | 4,394 | 4,394 | 100.00% |
| Quotation reference | F&O PR header | 2,898 | 2,898 | 2,898 | 100.00% |
| Name | F&O PR header | 4,394 | 4,394 | 4,391 | 99.93% |
| Preparer | F&O PR header | 4,394 | 4,394 | 0 | 0.00% |
| Status | F&O PR header | 4,394 | 4,394 | 4,377 | 99.61% |
| Created date | F&O PR BI header | 4,394 | 4,394 | 4,327 | 98.48% |
| Submitted date | F&O PR BI header | 4,394 | 4,337 | 4,335 | 99.95% |
| Requisition purpose | F&O PR header | 4,394 | 4,394 | 4,394 | 100.00% |
| Submission Status | **No live equivalent:** no exposed live equivalent | 2,889 | 0 | 0 | — |
| Accepted By/Assign To | **No live equivalent:** capture has current approvers, not accepted-by | 2,731 | 0 | 0 | — |
| Department | F&O line financial dimension | 2,728 | 2,727 | 2,726 | 99.96% |
| Location | F&O line dimension/address/project | 2,726 | 2,725 | 2,722 | 99.89% |
| Contract | F&O line financial dimension | 2,725 | 2,724 | 2,724 | 100.00% |
| Request for quotation case | **No live equivalent:** no general exposed live equivalent | 45 | 0 | 0 | — |
| Total amount | sum of F&O PR line amounts | 4,394 | 4,394 | 819 | 18.64% |
| Pending Approver/User | approval capture current work items | 2,683 | 571 | 526 | 92.12% |
| Step name | derived live stage; approved sourcing consolidation | 2,681 | 571 | 489 | 85.64% |
| Step date and time | F&O header modified seed or capture assignment | 4,394 | 893 | 527 | 59.01% |

### `po.xlsx`

| Workbook column | Proposed live source | Non-blank | Compared | Matched | Agreement |
|---|---|---:|---:|---:|---:|
| Purchase order | F&O PO header | 2,977 | 2,977 | 2,977 | 100.00% |
| Vendor account | F&O PO header | 2,977 | 2,977 | 2,947 | 98.99% |
| Invoice account | F&O PO header | 2,977 | 2,977 | 2,947 | 98.99% |
| Vendor name | F&O purchase-order name candidate | 2,977 | 2,977 | 2,947 | 98.99% |
| Purchase type | constant for PO header entity | 2,977 | 2,977 | 2,977 | 100.00% |
| Approval status | F&O PO header | 2,977 | 2,977 | 2,958 | 99.36% |
| Purchase order status | F&O PO header | 2,977 | 2,977 | 2,935 | 98.59% |
| Currency | F&O PO header | 2,977 | 2,977 | 2,977 | 100.00% |
| Requested receipt date | F&O PO header | 2,977 | 2,977 | 2,947 | 98.99% |
| Created date and time | F&O accounting date | 2,977 | 2,977 | 2,947 | 98.99% |
| Purchase requisition | F&O PO line | 1,490 | 1,481 | 1,481 | 100.00% |
| RFQ number | **No live equivalent:** no exposed live equivalent | 13 | 0 | 0 | — |
| Total amount | sum of F&O PO line amounts | 2,977 | 2,977 | 85 | 2.86% |
| Department | F&O line financial dimension | 1,207 | 1,199 | 1,199 | 100.00% |
| Location | F&O line dimension/address/project | 1,150 | 1,150 | 1,139 | 99.04% |
| Contract | F&O line financial dimension | 1,154 | 1,145 | 1,145 | 100.00% |
| Pending Approver/User | approval capture current work items | 1,167 | 3 | 3 | 100.00% |
| Step name | capture approval map plus F&O status/packing slip | 1,543 | 1,493 | 1,101 | 73.74% |
| Step date and time | capture assignment or packing-slip document date | 2,977 | 2,338 | 48 | 2.05% |
| Created by | **No live equivalent:** orderer personnel number is not created-by | 2,977 | 0 | 0 | — |

### Amount-basis gap

- PR: 819/4,394 exact document matches. Workbook total AED 53,093,720.31; live line total AED 49,313,877.25.
- PO: 85/2,977 exact document matches. Workbook total AED 36,836,401.82; live line total AED 48,799,682.23.
- The workbook amounts are tax-inclusive while the exposed line amounts are pre-tax/current. No business approval in this task defines those as interchangeable.

## Live headline and secondary counts

- Distinct resolved documents: **924**.
- Open work items (secondary): **1,430**.
- Unresolved approval work items (separate): **221**.
- Documents with parallel approvals: **113**.
- Documents with an F&O live header: **924**; missing live headers: **0**.
- Approval documents requiring the explicit unmapped label: **68**.

Stage counts from the blocked candidate model:

| Stage | Distinct documents |
|---|---:|
| PO — Approval — unmapped element | 5 |
| PO — Finance | 8 |
| PR — Approval — unmapped element | 63 |
| PR — Dep Managers | 2 |
| PR — Finance | 1 |
| PR — Priced — awaiting approval | 576 |
| PR — Sourcing | 269 |

## Approver reconciliation

The current comparable population was 574. Classifications: matched 529, parallel approvers 6, unexplained 12, workbook older than capture 27. `UNRESOLVED-*` work items are not documents and are excluded from the distinct-document count.

- parallel approvers: CPR-000971 [Aparna.Pauly → Adnan.Ullah, Layusha.cleatus, roderick.red]; CPR-010959 [D365CRMADMIN → Adnan.Ullah, Layusha.cleatus, roderick.red]; CPR-011059 [D365CRMADMIN → Adnan.Ullah, Layusha.cleatus, roderick.red]; CPR-011816 [D365CRMADMIN → Adnan.Ullah, Layusha.cleatus, roderick.red]; CPR-011832 [D365CRMADMIN → Adnan.Ullah, Layusha.cleatus, roderick.red]; CPR-030136 [D365CRMADMIN → Adnan.Ullah, Aparna.Pauly, Layusha.cleatus, roderick.red]
- unexplained: CPR-011003 [D365CRMADMIN → Layusha.cleatus]; CPR-026422 [D365CRMADMIN → roderick.red]; CPR-028298 [Adnan.Ullah → Aparna.Pauly]; CPR-031380 [Adnan.Ullah → Aparna.Pauly]; CPR-032447 [Adnan.Ullah → Aparna.Pauly]; CPR-034805 [Aparna.Pauly → roderick.red]; CPR-034832 [Layusha.cleatus → Adnan.Ullah]; CPR-034902 [roderick.red → Adnan.Ullah]; CPR-034911 [Aparna.Pauly → roderick.red]; CPR-034808 [Aparna.Pauly → roderick.red]; CPR-034914 [Aparna.Pauly → roderick.red]; CPR-034920 [Aparna.Pauly → roderick.red]
- workbook older than capture: CPR-000081 [D365CRMADMIN → Layusha.cleatus]; CPR-000432 [Abdul.basit → Adnan.Ullah]; CPR-000437 [D365CRMADMIN → Adnan.Ullah]; CPR-000440 [D365CRMADMIN → roderick.red]; CPR-000232 [D365CRMADMIN → Layusha.cleatus]; CPR-001486 [D365CRMADMIN → roderick.red]; CPR-001538 [D365CRMADMIN → roderick.red]; CPR-001548 [D365CRMADMIN → Adnan.Ullah]; CPR-010607 [D365CRMADMIN → Adnan.Ullah]; CPR-010937 [D365CRMADMIN → Layusha.cleatus]; CPR-018190 [Adnan.Ullah → Aparna.Pauly]; CPR-022436 [Adnan.Ullah → Aparna.Pauly]; CPR-022938 [Adnan.Ullah → roderick.red]; CPR-024581 [Adnan.Ullah → Aparna.Pauly]; CPR-026145 [Adnan.Ullah → Aparna.Pauly]; CPR-027280 [Layusha.cleatus → roderick.red]; CPR-027520 [Adnan.Ullah → Aparna.Pauly]; CPR-027521 [Adnan.Ullah → Aparna.Pauly]; CPR-028299 [Adnan.Ullah → Aparna.Pauly]; CPR-028662 [Adnan.Ullah → Aparna.Pauly]; PR-001654 [Mohammad.w → arman.b]; PR-001694 [Judhin.prabhakar → arman.b]; PR-001700 [Layusha.cleatus → arman.b]; PR-001701 [Aparna.Pauly → arman.b]; PR-001702 [Adnan.Ullah → arman.b]; PR-001725 [roderick.red → Abdul.Muqeet]; PR-001743 [Mohammad.w → arman.b]

## Document-level stage differences

### PR

- Dep Managers → Priced — awaiting approval: PR-001694, PR-001743
- Dep Managers → Sourcing (ZERO_PRICE_LINES, PR_REVIEW_SOURCING_NOT_SEPARABLE): PR-001654
- Finance → Priced — awaiting approval: PR-001684
- PR in review → Approval — unmapped element (ZERO_ACTIVE_LINES): PR-000121, CPR-000081, CPR-000432, CPR-000437, CPR-000440, CPR-000232, CPR-001486, CPR-001538, CPR-001548, CPR-010607, CPR-010937, CPR-010959, CPR-011003, CPR-011059, CPR-011816, CPR-011832, CPR-026422, CPR-030136
- PR in review → Priced — awaiting approval: CPR-000971, CPR-022436, CPR-028662, CPR-028843, CPR-029367, CPR-029477, PR-001545, CPR-030133, CPR-030558, CPR-032057, CPR-032136, CPR-032260, PR-001622, PR-001623, CPR-033076, CPR-033128, CPR-033260, PR-001682, PR-001700, PR-001701, PR-001702, CPR-034069, PR-001725, CPR-034902, CPR-034908
- PR in review → Sourcing (ZERO_PRICE_LINES, PR_REVIEW_SOURCING_NOT_SEPARABLE): PR-001446, CPR-031380, CPR-032061, PR-001661, CPR-033214, PR-001698, PR-001726, PR-001728, CPR-034382, PR-001744, PR-001747, PR-001750, PR-001751, PR-001753, PR-001754, CPR-034805, CPR-034832, PR-001761, CPR-034878, CPR-034911, CPR-034808, CPR-034914, CPR-034920, CPR-034930
- Priced — awaiting approval → Sourcing (ZERO_PRICE_LINES, PR_REVIEW_SOURCING_NOT_SEPARABLE): CPR-030786, CPR-034165
- Sourcing → Priced — awaiting approval: CPR-026592, CPR-027046, CPR-028312, CPR-033658, CPR-033852, CPR-034541, CPR-034582, CPR-034663, CPR-034667

### PO

- CEO → Pending Invoicing: P0000000011
- Finance → Pending Invoicing: P0000000151, SCBM-PO2600420, SCBM-PO2600430, SCBM-PO2600431, SCBM-PO2600436, SCBM-PO2600451, SCBM-PO2600512, SCBM-PO2600525, SCBM-PO2600568, SCBM-PO2600576, SCBM-PO2600692, SCBM-PO2600777, SCBM-PO2600780, SCBM-PO2600783, SCBM-PO2600784, SCBM-PO2601220, SCBM-PO2601243, SCBM-PO2601356, SCBM-PO2601391
- Finance → Sent to Supplier: SCBM-PO2600399, SCBM-PO2600624, SCBM-PO2601344, SCBM-PO2601421, SCBM-PO2601434, SCBM-PO2601534, SCBM-PO2601581, SCBM-PO2601589, SCBM-PO2601590, SCBM-PO2601591
- Procurement → Pending Invoicing: SCBM-PO2600218, SCBM-PO2600317, SCBM-PO2600547, SCBM-PO2600748, SCBM-PO2600958, SCBM-PO2600973, SCBM-PO2601037, SCBM-PO2601040, SCBM-PO2601041, SCBM-PO2601042, SCBM-PO2601046, SCBM-PO2601091, SCBM-PO2601103, SCBM-PO2601124, SCBM-PO2601156, SCBM-PO2601187, SCBM-PO2601189, SCBM-PO2601222, SCBM-PO2601223, SCBM-PO2601229, SCBM-PO2601281, SCBM-PO2601350, SCBM-PO2601351, SCBM-PO2601362, SCBM-PO2601370, SCBM-PO2601396, SCBM-PO2601408, SCBM-PO2601425, SCBM-PO2601428, SCBM-PO2601441, SCBM-PO2601507, SCBM-PO2601532, SCBM-PO2601558
- Procurement → Sent to Supplier: SCBM-PO2600902, SCBM-PO2601092, SCBM-PO2601093, SCBM-PO2601104, SCBM-PO2601158, SCBM-PO2601176, SCBM-PO2601180, SCBM-PO2601182, SCBM-PO2601273, SCBM-PO2601398, SCBM-PO2601524, SCBM-PO2601526, SCBM-PO2601546, SCBM-PO2601551, SCBM-PO2601561, SCBM-PO2601562, SCBM-PO2601586, SCBM-PO2601592, SCBM-PO2601593, SCBM-PO2601594, SCBM-PO2601595, SCBM-PO2601596, SCBM-PO2601597
- Sent to Supplier → Pending Invoicing: P0000000008, P0000000002, P0000000016, P0000000004, P0000000005, P0000000032, P0000000048, P0000000049, P0000000052, P0000000062, P0000000123, P0000000127, P0000000128, P0000000129, P0000000137, P0000000138, P0000000142, P0000000147, P0000000159, P0000000160, P0000000146, P0000000161, P0000000169, P0000000172, P0000000176, P0000000178, P0000000179, P0000000180, P0000000188, P0000000191, P0000000202, P0000000203, P0000000209, P0000000210, P0000000217, P0000000229, P0000000214, P0000000340, P0000000325, P0000000345, P0000000347, P0000000348, P0000000349, P0000000350, P0000000351, P0000000366, P0000000370, P0000000359, P0000000373, P0000000376, P0000000419, P0000000422, P0000000467, P0000000479, P0000000483, P0000000484, P0000000488, P0000000582, P0000000606, P0000000654, P0000000680, P0000000710, P0000000693, P0000000694, P0000000737, P0000000764, P0000000767, P0000000770, P0000000793, P0000000794, P0000000795, P0000000869, P0000000878, P0000000875, P0000000886, P0000000889, P0000000930, P0000000962, P0000000969, P0000000988, P0000000994, P0000001003, P0000001017, P0000001036, P0000001042, P0000001052, P0000001110, P0000001118, P0000001156, P0000001168, P0000001179, P0000001193, P0000001196, P0000001200, P0000001202, P0000001227, P0000001225, P0000001248, P0000001249, P0000001250, P0000001254, P0000001255, P0000001256, P0000001257, P0000001258, P0000001260, P0000001261, P0000001246, P0000001262, P0000001263, P0000001267, P0000001268, P0000001273, P0000001275, P0000001277, P0000001283, P0000001285, P0000001287, P0000001288, P0000001289, P0000001290, P0000001291, P0000001293, P0000001297, P0000001298, P0000001299, P0000001300, P0000001301, P0000001302, P0000001303, P0000001304, P0000001305, P0000001306, P0000001307, P0000001294, P0000001295, P0000001312, P0000001308, P0000001321, P0000001324, P0000001337, P0000001416, P0000001422, P0000001437, P0000001438, P0000001439, P0000001443, P0000001455, P0000001464, P0000001489, P0000001497, P0000001499, P0000001500, P0000001567, SCBM-PO2600021, SCBM-PO2600024, SCBM-PO2600038, SCBM-PO2600054, SCBM-PO2600055, SCBM-PO2600056, SCBM-PO2600057, SCBM-PO2600072, SCBM-PO2600073, SCBM-PO2600074, SCBM-PO2600076, SCBM-PO2600077, SCBM-PO2600078, SCBM-PO2600079, SCBM-PO2600080, SCBM-PO2600084, SCBM-PO2600085, SCBM-PO2600087, SCBM-PO2600089, SCBM-PO2600090, SCBM-PO2600091, SCBM-PO2600092, SCBM-PO2600108, SCBM-PO2600115, SCBM-PO2600135, SCBM-PO2600136, SCBM-PO2600137, SCBM-PO2600138, SCBM-PO2600139, SCBM-PO2600142, SCBM-PO2600154, SCBM-PO2600163, SCBM-PO2600170, SCBM-PO2600171, SCBM-PO2600172, SCBM-PO2600174, SCBM-PO2600176, SCBM-PO2600177, SCBM-PO2600178, SCBM-PO2600179, SCBM-PO2600180, SCBM-PO2600181, SCBM-PO2600192, SCBM-PO2600195, SCBM-PO2600198, SCBM-PO2600208, SCBM-PO2600220, SCBM-PO2600226, SCBM-PO2600250, SCBM-PO2600252, SCBM-PO2600253, SCBM-PO2600261, SCBM-PO2600270, SCBM-PO2600272, SCBM-PO2600284, SCBM-PO2600304, SCBM-PO2600305, SCBM-PO2600306, SCBM-PO2600309, SCBM-PO2600327, SCBM-PO2600332, SCBM-PO2600333, SCBM-PO2600337, SCBM-PO2600343, SCBM-PO2600354, SCBM-PO2600378, SCBM-PO2600382, SCBM-PO2600387, SCBM-PO2600388, SCBM-PO2600389, SCBM-PO2600398, SCBM-PO2600402, SCBM-PO2600408, SCBM-PO2600409, SCBM-PO2600418, SCBM-PO2600419, SCBM-PO2600422, SCBM-PO2600423, SCBM-PO2600424, SCBM-PO2600425, SCBM-PO2600427, SCBM-PO2600428, SCBM-PO2600433, SCBM-PO2600434, SCBM-PO2600437, SCBM-PO2600438, SCBM-PO2600439, SCBM-PO2600440, SCBM-PO2600441, SCBM-PO2600442, SCBM-PO2600443, SCBM-PO2600444, SCBM-PO2600445, SCBM-PO2600447, SCBM-PO2600448, SCBM-PO2600449, SCBM-PO2600450, SCBM-PO2600452, SCBM-PO2600453, SCBM-PO2600454, SCBM-PO2600455, SCBM-PO2600456, SCBM-PO2600457, SCBM-PO2600458, SCBM-PO2600459, SCBM-PO2600460, SCBM-PO2600461, SCBM-PO2600462, SCBM-PO2600463, SCBM-PO2600464, SCBM-PO2600465, SCBM-PO2600466, SCBM-PO2600467, SCBM-PO2600468, SCBM-PO2600470, SCBM-PO2600471, SCBM-PO2600472, SCBM-PO2600473, SCBM-PO2600474, SCBM-PO2600476, SCBM-PO2600477, SCBM-PO2600478, SCBM-PO2600481, SCBM-PO2600482, SCBM-PO2600489, SCBM-PO2600490, SCBM-PO2600491, SCBM-PO2600492, SCBM-PO2600493, SCBM-PO2600494, SCBM-PO2600495, SCBM-PO2600496, SCBM-PO2600497, SCBM-PO2600498, SCBM-PO2600499, SCBM-PO2600501, SCBM-PO2600502, SCBM-PO2600503, SCBM-PO2600504, SCBM-PO2600505, SCBM-PO2600506, SCBM-PO2600507, SCBM-PO2600508, SCBM-PO2600509, SCBM-PO2600510, SCBM-PO2600511, SCBM-PO2600513, SCBM-PO2600514, SCBM-PO2600515, SCBM-PO2600516, SCBM-PO2600517, SCBM-PO2600518, SCBM-PO2600519, SCBM-PO2600520, SCBM-PO2600521, SCBM-PO2600522, SCBM-PO2600524, SCBM-PO2600527, SCBM-PO2600528, SCBM-PO2600529, SCBM-PO2600530, SCBM-PO2600531, SCBM-PO2600532, SCBM-PO2600533, SCBM-PO2600534, SCBM-PO2600535, SCBM-PO2600537, SCBM-PO2600539, SCBM-PO2600540, SCBM-PO2600541, SCBM-PO2600542, SCBM-PO2600544, SCBM-PO2600546, SCBM-PO2600545, SCBM-PO2600548, SCBM-PO2600549, SCBM-PO2600550, SCBM-PO2600551, SCBM-PO2600553, SCBM-PO2600554, SCBM-PO2600555, SCBM-PO2600556, SCBM-PO2600557, SCBM-PO2600559, SCBM-PO2600562, SCBM-PO2600563, SCBM-PO2600564, SCBM-PO2600565, SCBM-PO2600566, SCBM-PO2600567, SCBM-PO2600570, SCBM-PO2600571, SCBM-PO2600572, SCBM-PO2600573, SCBM-PO2600574, SCBM-PO2600575, SCBM-PO2600578, SCBM-PO2600579, SCBM-PO2600581, SCBM-PO2600582, SCBM-PO2600584, SCBM-PO2600585, SCBM-PO2600586, SCBM-PO2600587, SCBM-PO2600588, SCBM-PO2600589, SCBM-PO2600591, SCBM-PO2600592, SCBM-PO2600593, SCBM-PO2600594, SCBM-PO2600595, SCBM-PO2600596, SCBM-PO2600597, SCBM-PO2600598, SCBM-PO2600599, SCBM-PO2600600, SCBM-PO2600601, SCBM-PO2600602, SCBM-PO2600605, SCBM-PO2600607, SCBM-PO2600608, SCBM-PO2600610, SCBM-PO2600611, SCBM-PO2600612, SCBM-PO2600616, SCBM-PO2600617, SCBM-PO2600618, SCBM-PO2600619, SCBM-PO2600620, SCBM-PO2600621, SCBM-PO2600622, SCBM-PO2600623, SCBM-PO2600625, SCBM-PO2600626, SCBM-PO2600627, SCBM-PO2600628, SCBM-PO2600630, SCBM-PO2600631, SCBM-PO2600632, SCBM-PO2600633, SCBM-PO2600634, SCBM-PO2600636, SCBM-PO2600639, SCBM-PO2600640, SCBM-PO2600641, SCBM-PO2600642, SCBM-PO2600643, SCBM-PO2600644, SCBM-PO2600646, SCBM-PO2600647, SCBM-PO2600648, SCBM-PO2600649, SCBM-PO2600650, SCBM-PO2600652, SCBM-PO2600654, SCBM-PO2600656, SCBM-PO2600657, SCBM-PO2600660, SCBM-PO2600662, SCBM-PO2600663, SCBM-PO2600664, SCBM-PO2600667, SCBM-PO2600669, SCBM-PO2600670, SCBM-PO2600671, SCBM-PO2600672, SCBM-PO2600673, SCBM-PO2600676, SCBM-PO2600677, SCBM-PO2600678, SCBM-PO2600679, SCBM-PO2600680, SCBM-PO2600681, SCBM-PO2600682, SCBM-PO2600683, SCBM-PO2600684, SCBM-PO2600685, SCBM-PO2600686, SCBM-PO2600687, SCBM-PO2600688, SCBM-PO2600689, SCBM-PO2600691, SCBM-PO2600693, SCBM-PO2600696, SCBM-PO2600697, SCBM-PO2600698, SCBM-PO2600699, SCBM-PO2600700, SCBM-PO2600701, SCBM-PO2600702, SCBM-PO2600703, SCBM-PO2600704, SCBM-PO2600705, SCBM-PO2600707, SCBM-PO2600709, SCBM-PO2600710, SCBM-PO2600711, SCBM-PO2600712, SCBM-PO2600715, SCBM-PO2600716, SCBM-PO2600717, SCBM-PO2600718, SCBM-PO2600719, SCBM-PO2600720, SCBM-PO2600721, SCBM-PO2600722, SCBM-PO2600723, SCBM-PO2600724, SCBM-PO2600725, SCBM-PO2600726, SCBM-PO2600727, SCBM-PO2600728, SCBM-PO2600729, SCBM-PO2600730, SCBM-PO2600734, SCBM-PO2600735, SCBM-PO2600739, SCBM-PO2600742, SCBM-PO2600743, SCBM-PO2600745, SCBM-PO2600746, SCBM-PO2600747, SCBM-PO2600749, SCBM-PO2600750, SCBM-PO2600751, SCBM-PO2600752, SCBM-PO2600756, SCBM-PO2600757, SCBM-PO2600758, SCBM-PO2600760, SCBM-PO2600761, SCBM-PO2600762, SCBM-PO2600763, SCBM-PO2600764, SCBM-PO2600765, SCBM-PO2600766, SCBM-PO2600768, SCBM-PO2600769, SCBM-PO2600770, SCBM-PO2600771, SCBM-PO2600773, SCBM-PO2600774, SCBM-PO2600775, SCBM-PO2600776, SCBM-PO2600778, SCBM-PO2600779, SCBM-PO2600781, SCBM-PO2600782, SCBM-PO2600785, SCBM-PO2600786, SCBM-PO2600787, SCBM-PO2600788, SCBM-PO2600789, SCBM-PO2600790, SCBM-PO2600791, SCBM-PO2600792, SCBM-PO2600793, SCBM-PO2600794, SCBM-PO2600797, SCBM-PO2600798, SCBM-PO2600799, SCBM-PO2600800, SCBM-PO2600801, SCBM-PO2600802, SCBM-PO2600803, SCBM-PO2600804, SCBM-PO2600805, SCBM-PO2600808, SCBM-PO2600809, SCBM-PO2600810, SCBM-PO2600812, SCBM-PO2600814, SCBM-PO2600815, SCBM-PO2600817, SCBM-PO2600818, SCBM-PO2600820, SCBM-PO2600821, SCBM-PO2600822, SCBM-PO2600823, SCBM-PO2600824, SCBM-PO2600825, SCBM-PO2600826, SCBM-PO2600828, SCBM-PO2600830, SCBM-PO2600831, SCBM-PO2600832, SCBM-PO2600833, SCBM-PO2600834, SCBM-PO2600836, SCBM-PO2600838, SCBM-PO2600839, SCBM-PO2600840, SCBM-PO2600841, SCBM-PO2600842, SCBM-PO2600843, SCBM-PO2600844, SCBM-PO2600848, SCBM-PO2600849, SCBM-PO2600851, SCBM-PO2600852, SCBM-PO2600853, SCBM-PO2600854, SCBM-PO2600855, SCBM-PO2600856, SCBM-PO2600857, SCBM-PO2600859, SCBM-PO2600860, SCBM-PO2600862, SCBM-PO2600863, SCBM-PO2600864, SCBM-PO2600865, SCBM-PO2600866, SCBM-PO2600867, SCBM-PO2600868, SCBM-PO2600869, SCBM-PO2600871, SCBM-PO2600872, SCBM-PO2600873, SCBM-PO2600875, SCBM-PO2600876, SCBM-PO2600877, SCBM-PO2600878, SCBM-PO2600881, SCBM-PO2600882, SCBM-PO2600883, SCBM-PO2600884, SCBM-PO2600887, SCBM-PO2600888, SCBM-PO2600890, SCBM-PO2600892, SCBM-PO2600894, SCBM-PO2600896, SCBM-PO2600898, SCBM-PO2600899, SCBM-PO2600900, SCBM-PO2600901, SCBM-PO2600905, SCBM-PO2600906, SCBM-PO2600907, SCBM-PO2600908, SCBM-PO2600909, SCBM-PO2600910, SCBM-PO2600911, SCBM-PO2600912, SCBM-PO2600913, SCBM-PO2600914, SCBM-PO2600915, SCBM-PO2600916, SCBM-PO2600917, SCBM-PO2600918, SCBM-PO2600920, SCBM-PO2600921, SCBM-PO2600924, SCBM-PO2600925, SCBM-PO2600926, SCBM-PO2600927, SCBM-PO2600928, SCBM-PO2600930, SCBM-PO2600931, SCBM-PO2600932, SCBM-PO2600933, SCBM-PO2600934, SCBM-PO2600935, SCBM-PO2600936, SCBM-PO2600937, SCBM-PO2600938, SCBM-PO2600940, SCBM-PO2600941, SCBM-PO2600942, SCBM-PO2600943, SCBM-PO2600944, SCBM-PO2600945, SCBM-PO2600946, SCBM-PO2600947, SCBM-PO2600949, SCBM-PO2600951, SCBM-PO2600952, SCBM-PO2600953, SCBM-PO2600955, SCBM-PO2600956, SCBM-PO2600959, SCBM-PO2600960, SCBM-PO2600962, SCBM-PO2600963, SCBM-PO2600969, SCBM-PO2600970, SCBM-PO2600971, SCBM-PO2600972, SCBM-PO2600974, SCBM-PO2600975, SCBM-PO2600977, SCBM-PO2600978, SCBM-PO2600981, SCBM-PO2600982, SCBM-PO2600983, SCBM-PO2600984, SCBM-PO2600987, SCBM-PO2600988, SCBM-PO2600989, SCBM-PO2600990, SCBM-PO2600991, SCBM-PO2600992, SCBM-PO2600993, SCBM-PO2600994, SCBM-PO2600996, SCBM-PO2600997, SCBM-PO2600998, SCBM-PO2600999, SCBM-PO2601000, SCBM-PO2601001, SCBM-PO2601003, SCBM-PO2601004, SCBM-PO2601005, SCBM-PO2601007, SCBM-PO2601008, SCBM-PO2601009, SCBM-PO2601010, SCBM-PO2601011, SCBM-PO2601012, SCBM-PO2601013, SCBM-PO2601014, SCBM-PO2601015, SCBM-PO2601016, SCBM-PO2601017, SCBM-PO2601018, SCBM-PO2601019, SCBM-PO2601020, SCBM-PO2601021, SCBM-PO2601022, SCBM-PO2601023, SCBM-PO2601025, SCBM-PO2601027, SCBM-PO2601029, SCBM-PO2601030, SCBM-PO2601032, SCBM-PO2601036, SCBM-PO2601038, SCBM-PO2601039, SCBM-PO2601043, SCBM-PO2601048, SCBM-PO2601049, SCBM-PO2601050, SCBM-PO2601051, SCBM-PO2601052, SCBM-PO2601053, SCBM-PO2601054, SCBM-PO2601055, SCBM-PO2601056, SCBM-PO2601057, SCBM-PO2601058, SCBM-PO2601059, SCBM-PO2601061, SCBM-PO2601062, SCBM-PO2601063, SCBM-PO2601065, SCBM-PO2601066, SCBM-PO2601069, SCBM-PO2601070, SCBM-PO2601071, SCBM-PO2601073, SCBM-PO2601074, SCBM-PO2601077, SCBM-PO2601078, SCBM-PO2601079, SCBM-PO2601080, SCBM-PO2601081, SCBM-PO2601082, SCBM-PO2601083, SCBM-PO2601084, SCBM-PO2601085, SCBM-PO2601086, SCBM-PO2601087, SCBM-PO2601088, SCBM-PO2601089, SCBM-PO2601094, SCBM-PO2601095, SCBM-PO2601096, SCBM-PO2601098, SCBM-PO2601099, SCBM-PO2601100, SCBM-PO2601101, SCBM-PO2601106, SCBM-PO2601107, SCBM-PO2601108, SCBM-PO2601109, SCBM-PO2601110, SCBM-PO2601112, SCBM-PO2601114, SCBM-PO2601117, SCBM-PO2601118, SCBM-PO2601125, SCBM-PO2601126, SCBM-PO2601128, SCBM-PO2601129, SCBM-PO2601130, SCBM-PO2601131, SCBM-PO2601132, SCBM-PO2601133, SCBM-PO2601135, SCBM-PO2601136, SCBM-PO2601139, SCBM-PO2601142, SCBM-PO2601143, SCBM-PO2601144, SCBM-PO2601145, SCBM-PO2601146, SCBM-PO2601147, SCBM-PO2601148, SCBM-PO2601149, SCBM-PO2601150, SCBM-PO2601151, SCBM-PO2601152, SCBM-PO2601153, SCBM-PO2601154, SCBM-PO2601155, SCBM-PO2601157, SCBM-PO2601160, SCBM-PO2601161, SCBM-PO2601162, SCBM-PO2601163, SCBM-PO2601164, SCBM-PO2601165, SCBM-PO2601166, SCBM-PO2601167, SCBM-PO2601168, SCBM-PO2601169, SCBM-PO2601170, SCBM-PO2601171, SCBM-PO2601172, SCBM-PO2601173, SCBM-PO2601174, SCBM-PO2601177, SCBM-PO2601178, SCBM-PO2601179, SCBM-PO2601181, SCBM-PO2601183, SCBM-PO2601185, SCBM-PO2601186, SCBM-PO2601188, SCBM-PO2601190, SCBM-PO2601191, SCBM-PO2601192, SCBM-PO2601193, SCBM-PO2601194, SCBM-PO2601195, SCBM-PO2601196, SCBM-PO2601198, SCBM-PO2601199, SCBM-PO2601200, SCBM-PO2601201, SCBM-PO2601202, SCBM-PO2601203, SCBM-PO2601205, SCBM-PO2601206, SCBM-PO2601209, SCBM-PO2601211, SCBM-PO2601212, SCBM-PO2601213, SCBM-PO2601214, SCBM-PO2601215, SCBM-PO2601216, SCBM-PO2601217, SCBM-PO2601218, SCBM-PO2601219, SCBM-PO2601221, SCBM-PO2601225, SCBM-PO2601227, SCBM-PO2601230, SCBM-PO2601231, SCBM-PO2601232, SCBM-PO2601233, SCBM-PO2601234, SCBM-PO2601235, SCBM-PO2601236, SCBM-PO2601237, SCBM-PO2601238, SCBM-PO2601239, SCBM-PO2601240, SCBM-PO2601241, SCBM-PO2601242, SCBM-PO2601244, SCBM-PO2601245, SCBM-PO2601246, SCBM-PO2601248, SCBM-PO2601250, SCBM-PO2601251, SCBM-PO2601252, SCBM-PO2601253, SCBM-PO2601254, SCBM-PO2601256, SCBM-PO2601258, SCBM-PO2601259, SCBM-PO2601260, SCBM-PO2601261, SCBM-PO2601262, SCBM-PO2601263, SCBM-PO2601264, SCBM-PO2601266, SCBM-PO2601270, SCBM-PO2601271, SCBM-PO2601272, SCBM-PO2601274, SCBM-PO2601276, SCBM-PO2601277, SCBM-PO2601279, SCBM-PO2601280, SCBM-PO2601282, SCBM-PO2601283, SCBM-PO2601284, SCBM-PO2601285, SCBM-PO2601286, SCBM-PO2601287, SCBM-PO2601289, SCBM-PO2601294, SCBM-PO2601295, SCBM-PO2601296, SCBM-PO2601298, SCBM-PO2601299, SCBM-PO2601300, SCBM-PO2601301, SCBM-PO2601302, SCBM-PO2601303, SCBM-PO2601304, SCBM-PO2601305, SCBM-PO2601306, SCBM-PO2601307, SCBM-PO2601308, SCBM-PO2601309, SCBM-PO2601310, SCBM-PO2601312, SCBM-PO2601313, SCBM-PO2601316, SCBM-PO2601317, SCBM-PO2601320, SCBM-PO2601321, SCBM-PO2601322, SCBM-PO2601323, SCBM-PO2601324, SCBM-PO2601326, SCBM-PO2601327, SCBM-PO2601328, SCBM-PO2601329, SCBM-PO2601330, SCBM-PO2601333, SCBM-PO2601334, SCBM-PO2601335, SCBM-PO2601336, SCBM-PO2601337, SCBM-PO2601338, SCBM-PO2601339, SCBM-PO2601340, SCBM-PO2601341, SCBM-PO2601342, SCBM-PO2601343, SCBM-PO2601345, SCBM-PO2601346, SCBM-PO2601347, SCBM-PO2601348, SCBM-PO2601349, SCBM-PO2601354, SCBM-PO2601358, SCBM-PO2601359, SCBM-PO2601360, SCBM-PO2601365, SCBM-PO2601366, SCBM-PO2601369, SCBM-PO2601371, SCBM-PO2601373, SCBM-PO2601375, SCBM-PO2601376, SCBM-PO2601377, SCBM-PO2601380, SCBM-PO2601381, SCBM-PO2601382, SCBM-PO2601383, SCBM-PO2601384, SCBM-PO2601385, SCBM-PO2601386, SCBM-PO2601388, SCBM-PO2601389, SCBM-PO2601390, SCBM-PO2601392, SCBM-PO2601393, SCBM-PO2601394, SCBM-PO2601395, SCBM-PO2601402, SCBM-PO2601403, SCBM-PO2601404, SCBM-PO2601407, SCBM-PO2601410, SCBM-PO2601411, SCBM-PO2601412, SCBM-PO2601413, SCBM-PO2601415, SCBM-PO2601416, SCBM-PO2601418, SCBM-PO2601422, SCBM-PO2601427, SCBM-PO2601439, SCBM-PO2601443, SCBM-PO2601448, SCBM-PO2601455, SCBM-PO2601460, SCBM-PO2601461, SCBM-PO2601462, SCBM-PO2601465, SCBM-PO2601470, SCBM-PO2601471, SCBM-PO2601473, SCBM-PO2601477, SCBM-PO2601479, SCBM-PO2601480, SCBM-PO2601482, SCBM-PO2601483, SCBM-PO2601486, SCBM-PO2601496, SCBM-PO2601497, SCBM-PO2601499, SCBM-PO2601508, SCBM-PO2601509, SCBM-PO2601515, SCBM-PO2601527, SCBM-PO2601571

## PR procurement clock differences over one day

- CPR-028843: PR in review; workbook `2026-07-17T10:02:21Z`; F&O modified-time seed `2026-07-20T05:13:17Z`.
- PR-001700: PR in review; workbook `2026-09-01T10:14:53Z`; F&O modified-time seed `2026-09-07T11:02:55Z`.
- PR-001701: PR in review; workbook `2026-09-01T10:21:57Z`; F&O modified-time seed `2026-09-07T11:03:55Z`.
- PR-001702: PR in review; workbook `2026-08-25T12:18:43Z`; F&O modified-time seed `2026-09-07T11:04:49Z`.
- PR-001725: PR in review; workbook `2026-09-04T16:11:56Z`; F&O modified-time seed `2026-09-07T12:34:56Z`.
- CPR-034162: Sourcing; workbook `2026-08-31T17:33:35Z`; F&O modified-time seed `2026-09-04T04:56:36Z`.
- PR-001726: PR in review; workbook `2026-08-31T17:03:57Z`; F&O modified-time seed `2026-09-04T04:57:00Z`.
- CPR-034154: Priced — awaiting approval; workbook `2026-08-27T16:40:14Z`; F&O modified-time seed `2026-09-04T04:56:07Z`.
- CPR-034527: Sourcing; workbook `2026-09-03T15:22:31Z`; F&O modified-time seed `2026-09-07T05:36:43Z`.
- CPR-034541: Sourcing; workbook `2026-09-04T13:20:56Z`; F&O modified-time seed `2026-09-07T09:14:14Z`.
- PR-001747: PR in review; workbook `2026-09-02T13:36:52Z`; F&O modified-time seed `2026-09-07T12:22:47Z`.
- CPR-034663: Sourcing; workbook `2026-09-04T10:52:11Z`; F&O modified-time seed `2026-09-07T05:26:54Z`.
- CPR-034667: Sourcing; workbook `2026-09-04T13:46:06Z`; F&O modified-time seed `2026-09-07T12:41:53Z`.
- CPR-034805: PR in review; workbook `2026-09-04T11:41:51Z`; F&O modified-time seed `2026-09-07T08:14:46Z`.
- CPR-034616: Sourcing; workbook `2026-09-04T11:47:01Z`; F&O modified-time seed `2026-09-07T07:29:24Z`.
- CPR-034832: PR in review; workbook `2026-09-04T13:41:53Z`; F&O modified-time seed `2026-09-07T11:43:56Z`.
- CPR-034902: PR in review; workbook `2026-09-05T13:41:52Z`; F&O modified-time seed `2026-09-07T11:54:49Z`.
- CPR-034908: PR in review; workbook `2026-09-05T14:42:02Z`; F&O modified-time seed `2026-09-07T11:47:44Z`.
- CPR-034878: PR in review; workbook `2026-09-05T14:42:01Z`; F&O modified-time seed `2026-09-07T05:35:57Z`.
- CPR-034911: PR in review; workbook `2026-09-05T14:42:00Z`; F&O modified-time seed `2026-09-07T08:21:26Z`.
- CPR-034808: PR in review; workbook `2026-09-05T14:41:59Z`; F&O modified-time seed `2026-09-07T08:18:48Z`.
- CPR-034914: PR in review; workbook `2026-09-05T14:41:58Z`; F&O modified-time seed `2026-09-07T08:24:28Z`.
- CPR-034920: PR in review; workbook `2026-09-05T15:41:51Z`; F&O modified-time seed `2026-09-07T07:34:00Z`.

## PO workbook stage assumption check

The exact non-blank PO steps are `LPO sent/shared with supplier` (1,425), `Procurement Manager` (59), `Accounting Manager` (45), `Advance payment request submitted (if applicable)` (10), `Finance and Accounts Director` (2), `CEO` (1) and `PurchTableApproval` (1); 1,434 rows are blank. This confirms there are no hidden workbook sourcing sub-steps, but `PurchTableApproval` still needs an explicit mapping.

## Problems and risks

- The live sources cannot truthfully separate `PR in review` from `Sourcing` for shared elements. Line pricing can separate `Priced`, but cannot establish whether an unpriced document is still in review or already sourcing.
- `Submission Status`, `Accepted By/Assign To`, PR RFQ case, PO RFQ number and PO `Created by` have no exposed like-for-like live source for the non-blank counts above.
- Current approval identities do not fully reproduce the older workbook owner. Parallel, reassigned, older-workbook and unexplained cases are listed above.
- A posted packing slip is a receipt event, not a delivery date. Partial receipts create a materially different PO stage result from the workbook's single `LPO sent/shared with supplier` step.
- The cloned `pr-po-proxy` repository's only workflow targets the out-of-scope `pr-po-dashboard-proxy`, not authorised `ssg-prpo-proxy`. It was not run; repository documentation now warns against using it.

## Files changed

- `tests/reconcile_workbook_retirement.py` — reproducible, read-only reconciliation.
- `evidence/workbook-retirement-reconciliation.json` — complete machine evidence and document differences.
- `docs/workbook-retirement-change-note.md` and `.html` — unpublished blocked change-note draft.
- Both repositories' `README.md` / `CLAUDE.md` — current truth and deployment guardrails.
- `NOTES.md` — this verdict and evidence.

## What I did not change

- No workbook, fallback, snapshot generator, workflow, dashboard logic, email logic, recipient, sender, quiet-mode setting or stage map was removed or changed.
- No write was made to either Dataverse organisation. No Azure resource or app registration was created or changed.
- Neither function app was deployed. Chandan's app, flow, OneDrive and tokens were not touched; only the stale documentation naming his app as the target was corrected.

## Testing performed

- Python compile check passed for the reconciliation script.
- One complete read-only reconciliation succeeded against both live organisations and both unchanged workbooks.
- The evidence contains every PR/PO stage mismatch and every PR clock mismatch over one day.
- Verification level: code verified; reconciliation verified live; build not applicable; deployment deliberately not performed; production workbook behaviour unchanged.

## Remaining risks

- The operational systems continue moving. The UTC timestamps above identify this exact evidence position.
- The business decision below is required before a safe candidate stage model can be built and tested.

## Recommended next step

Waqas must decide whether unpriced documents on shared procurement elements may be reported in one combined `PR in review / Sourcing` stage, or provide another deterministic exposed rule that separates them. After that decision, rerun this reconciliation before implementing any cutover.

---

# Workbook retirement correction 01 — 7 September 2026

## Verdict

**Cannot retire.** The corrected business rules remove the `PR in review` decision blocker, but three mandatory computed gates still fail. The safe-cutover stop applies before deployment or workbook removal.

| Gate | 7 September verdict | Correction 01 | Result |
|---|---:|---:|---|
| PR stage agreement | 489/571 (85.64%) | 512/571 (89.67%) | FAIL; threshold 95% |
| PR procurement clock within one day | 541/564 (95.92%) | 540/564 (95.74%) | PASS; threshold 90% |
| PO stage agreement | 430/1,493 (28.80%) | 653/1,495 (43.68%) | FAIL; threshold 95% |
| PR amount agreement | 819/4,394 (18.64%, old unadjusted basis) | 3,560/4,394 (81.02%, corrected ex-VAT basis) | FAIL; threshold 95% |
| PO amount agreement | 85/2,977 (2.86%, old unadjusted basis) | 2,923/2,977 (98.19%, corrected ex-VAT basis) | PASS; threshold 95% |
| Distinct-document count | Not a failing gate | 923 resolved documents; 1,414 work items | PASS |

Even if all 755 workbook `LPO sent/shared with supplier` rows now marked `Invoiced` were accepted as later lifecycle progress, PO agreement would be 1,408/1,495 (94.18%), still below 95%. Correction 01 explicitly grants progression equivalence for `Receipt posted`, not for `Invoiced`; the measured gate above applies that rule literally.

## Read-only source evidence

- Workbooks: 4,394 PR and 2,977 PO documents.
- F&O: 4,413 PR headers, 20,711 PR lines, 3,188 PO headers, 14,977 PO lines and 3,868 packing-slip journals.
- Approval capture: 1,781 snapshots and 1,414 current work items.
- Dataset generated/F&O read: `2026-09-07T14:03:26.088700Z` / `2026-09-07T14:03:26.088700Z`.
- Approval capture reconciled/effective data time: `2026-09-07T14:00:29Z` / `2026-09-07T14:00:29Z`; capture age 2.95 minutes.

## Corrected amount basis

Tax applicability comes from the exposed F&O sales-tax-group and item-tax-group pair. Live group descriptions confirm `SR-RCVR` is Standard Recoverable, `OS` is Out of Scope of VAT and `ZR` is Zero Rate. A standard-rate line requires both codes to be standard-rate; an OS/ZR code makes the line non-VAT. Standard-rate documents divide the workbook total by 1.05; non-VAT documents keep the workbook value. Mixed or blank pairs remain unmatched rather than being guessed. Zero matches only zero.

### pr.xlsx

- Agreement: 3,560/4,394 (81.02%).
- Workbook including VAT: AED 53,093,720.31.
- Deterministically adjusted workbook excl. VAT: AED 47,938,970.43 across 3,624 documents.
- Live line total excl. VAT: AED 49,314,746.25.
- Tax-basis counts: mixed VAT basis 15, non-VAT 23, standard-rate VAT 2,823, unknown 38, zero amount 1,495.

### po.xlsx

- Agreement: 2,923/2,977 (98.19%).
- Workbook including VAT: AED 36,836,401.82.
- Deterministically adjusted workbook excl. VAT: AED 34,684,077.18 across 2,956 documents.
- Live line total excl. VAT: AED 48,404,855.18.
- Tax-basis counts: mixed VAT basis 1, non-VAT 37, standard-rate VAT 2,880, unknown 13, zero amount 46.

## PR stage differences

- Dep Managers → Priced — awaiting approval: PR-001694, PR-001743
- Dep Managers → Sourcing (ZERO_PRICE_LINES): PR-001654
- Finance → Priced — awaiting approval: PR-001684
- Priced — awaiting approval → Sourcing (ZERO_PRICE_LINES): CPR-030786, CPR-034165
- Sourcing → Approval — unmapped element (ZERO_ACTIVE_LINES): PR-000121, CPR-000081, CPR-000432, CPR-000437, CPR-000440, CPR-000232, CPR-001486, CPR-001538, CPR-001548, CPR-010607, CPR-010937, CPR-010959, CPR-011003, CPR-011059, CPR-011816, CPR-011832, CPR-026422, CPR-030136
- Sourcing → Priced — awaiting approval: CPR-000971, CPR-022436, CPR-026592, CPR-027046, CPR-028312, CPR-028662, CPR-028843, CPR-029367, CPR-029477, PR-001545, CPR-030133, CPR-030558, CPR-032057, CPR-032136, CPR-032260, PR-001622, PR-001623, CPR-033076, CPR-033128, CPR-033260, PR-001682, CPR-033658, PR-001700, PR-001701, PR-001702, CPR-033852, CPR-034069, PR-001725, CPR-034541, PR-001742, CPR-034582, CPR-034663, CPR-034667, CPR-034902, CPR-034908

## PO stage differences

- CEO → Receipt posted: P0000000011
- Finance → Invoiced: SCBM-PO2600420, SCBM-PO2600430, SCBM-PO2600431, SCBM-PO2600436, SCBM-PO2600451, SCBM-PO2600512, SCBM-PO2600525, SCBM-PO2600576, SCBM-PO2600692, SCBM-PO2600777, SCBM-PO2600783, SCBM-PO2601220
- Finance → Receipt posted: P0000000151, SCBM-PO2600088, SCBM-PO2600568, SCBM-PO2600780, SCBM-PO2600784, SCBM-PO2601243, SCBM-PO2601356, SCBM-PO2601391
- Finance → Sent to supplier: SCBM-PO2600399, SCBM-PO2600624, SCBM-PO2601344, SCBM-PO2601421, SCBM-PO2601434, SCBM-PO2601534, SCBM-PO2601581, SCBM-PO2601589, SCBM-PO2601590, SCBM-PO2601591
- Procurement → Invoiced: SCBM-PO2600547, SCBM-PO2600973, SCBM-PO2601037, SCBM-PO2601040, SCBM-PO2601041, SCBM-PO2601042, SCBM-PO2601046, SCBM-PO2601091, SCBM-PO2601103, SCBM-PO2601124, SCBM-PO2601156, SCBM-PO2601187, SCBM-PO2601189, SCBM-PO2601222, SCBM-PO2601223, SCBM-PO2601229, SCBM-PO2601350, SCBM-PO2601351, SCBM-PO2601362, SCBM-PO2601370, SCBM-PO2601396, SCBM-PO2601408, SCBM-PO2601428, SCBM-PO2601532
- Procurement → Receipt posted: SCBM-PO2600218, SCBM-PO2600317, SCBM-PO2600748, SCBM-PO2600958, SCBM-PO2601281, SCBM-PO2601425, SCBM-PO2601441, SCBM-PO2601507, SCBM-PO2601558
- Procurement → Sent to supplier: SCBM-PO2600902, SCBM-PO2601092, SCBM-PO2601093, SCBM-PO2601104, SCBM-PO2601158, SCBM-PO2601176, SCBM-PO2601180, SCBM-PO2601182, SCBM-PO2601273, SCBM-PO2601398, SCBM-PO2601524, SCBM-PO2601526, SCBM-PO2601546, SCBM-PO2601551, SCBM-PO2601561, SCBM-PO2601562, SCBM-PO2601586, SCBM-PO2601592, SCBM-PO2601593, SCBM-PO2601594, SCBM-PO2601595, SCBM-PO2601596, SCBM-PO2601597
- Sent to supplier → Invoiced: P0000000002, P0000000004, P0000000005, P0000000484, P0000000694, P0000000878, P0000001110, P0000001227, P0000001248, P0000001249, P0000001250, P0000001254, P0000001255, P0000001258, P0000001260, P0000001261, P0000001246, P0000001262, P0000001263, P0000001267, P0000001268, P0000001273, P0000001275, P0000001277, P0000001283, P0000001285, P0000001287, P0000001288, P0000001289, P0000001290, P0000001291, P0000001293, P0000001297, P0000001298, P0000001299, P0000001300, P0000001302, P0000001303, P0000001304, P0000001305, P0000001306, P0000001307, P0000001294, P0000001295, P0000001312, P0000001308, P0000001324, P0000001489, SCBM-PO2600115, SCBM-PO2600137, SCBM-PO2600163, SCBM-PO2600171, SCBM-PO2600172, SCBM-PO2600174, SCBM-PO2600179, SCBM-PO2600192, SCBM-PO2600208, SCBM-PO2600270, SCBM-PO2600284, SCBM-PO2600305, SCBM-PO2600306, SCBM-PO2600309, SCBM-PO2600332, SCBM-PO2600333, SCBM-PO2600343, SCBM-PO2600398, SCBM-PO2600402, SCBM-PO2600418, SCBM-PO2600419, SCBM-PO2600422, SCBM-PO2600423, SCBM-PO2600424, SCBM-PO2600425, SCBM-PO2600427, SCBM-PO2600428, SCBM-PO2600434, SCBM-PO2600437, SCBM-PO2600438, SCBM-PO2600439, SCBM-PO2600440, SCBM-PO2600441, SCBM-PO2600442, SCBM-PO2600443, SCBM-PO2600444, SCBM-PO2600445, SCBM-PO2600447, SCBM-PO2600448, SCBM-PO2600449, SCBM-PO2600450, SCBM-PO2600453, SCBM-PO2600455, SCBM-PO2600456, SCBM-PO2600457, SCBM-PO2600458, SCBM-PO2600459, SCBM-PO2600460, SCBM-PO2600461, SCBM-PO2600462, SCBM-PO2600463, SCBM-PO2600464, SCBM-PO2600465, SCBM-PO2600466, SCBM-PO2600467, SCBM-PO2600468, SCBM-PO2600470, SCBM-PO2600471, SCBM-PO2600472, SCBM-PO2600473, SCBM-PO2600474, SCBM-PO2600476, SCBM-PO2600477, SCBM-PO2600478, SCBM-PO2600481, SCBM-PO2600482, SCBM-PO2600489, SCBM-PO2600490, SCBM-PO2600491, SCBM-PO2600492, SCBM-PO2600493, SCBM-PO2600494, SCBM-PO2600495, SCBM-PO2600496, SCBM-PO2600497, SCBM-PO2600498, SCBM-PO2600499, SCBM-PO2600501, SCBM-PO2600503, SCBM-PO2600504, SCBM-PO2600505, SCBM-PO2600506, SCBM-PO2600508, SCBM-PO2600509, SCBM-PO2600517, SCBM-PO2600518, SCBM-PO2600519, SCBM-PO2600520, SCBM-PO2600521, SCBM-PO2600524, SCBM-PO2600527, SCBM-PO2600528, SCBM-PO2600529, SCBM-PO2600530, SCBM-PO2600531, SCBM-PO2600532, SCBM-PO2600533, SCBM-PO2600535, SCBM-PO2600537, SCBM-PO2600539, SCBM-PO2600541, SCBM-PO2600546, SCBM-PO2600545, SCBM-PO2600548, SCBM-PO2600549, SCBM-PO2600550, SCBM-PO2600551, SCBM-PO2600553, SCBM-PO2600554, SCBM-PO2600555, SCBM-PO2600556, SCBM-PO2600557, SCBM-PO2600559, SCBM-PO2600562, SCBM-PO2600563, SCBM-PO2600564, SCBM-PO2600565, SCBM-PO2600566, SCBM-PO2600567, SCBM-PO2600570, SCBM-PO2600571, SCBM-PO2600572, SCBM-PO2600573, SCBM-PO2600574, SCBM-PO2600575, SCBM-PO2600578, SCBM-PO2600579, SCBM-PO2600581, SCBM-PO2600582, SCBM-PO2600584, SCBM-PO2600585, SCBM-PO2600587, SCBM-PO2600588, SCBM-PO2600589, SCBM-PO2600591, SCBM-PO2600592, SCBM-PO2600593, SCBM-PO2600594, SCBM-PO2600596, SCBM-PO2600597, SCBM-PO2600598, SCBM-PO2600599, SCBM-PO2600600, SCBM-PO2600601, SCBM-PO2600602, SCBM-PO2600605, SCBM-PO2600607, SCBM-PO2600608, SCBM-PO2600611, SCBM-PO2600612, SCBM-PO2600616, SCBM-PO2600617, SCBM-PO2600618, SCBM-PO2600619, SCBM-PO2600620, SCBM-PO2600621, SCBM-PO2600623, SCBM-PO2600627, SCBM-PO2600628, SCBM-PO2600630, SCBM-PO2600631, SCBM-PO2600634, SCBM-PO2600636, SCBM-PO2600639, SCBM-PO2600640, SCBM-PO2600641, SCBM-PO2600642, SCBM-PO2600646, SCBM-PO2600647, SCBM-PO2600648, SCBM-PO2600649, SCBM-PO2600650, SCBM-PO2600652, SCBM-PO2600654, SCBM-PO2600656, SCBM-PO2600657, SCBM-PO2600660, SCBM-PO2600662, SCBM-PO2600663, SCBM-PO2600664, SCBM-PO2600667, SCBM-PO2600669, SCBM-PO2600670, SCBM-PO2600672, SCBM-PO2600673, SCBM-PO2600676, SCBM-PO2600677, SCBM-PO2600678, SCBM-PO2600679, SCBM-PO2600680, SCBM-PO2600681, SCBM-PO2600682, SCBM-PO2600683, SCBM-PO2600685, SCBM-PO2600686, SCBM-PO2600688, SCBM-PO2600689, SCBM-PO2600691, SCBM-PO2600693, SCBM-PO2600696, SCBM-PO2600697, SCBM-PO2600698, SCBM-PO2600699, SCBM-PO2600700, SCBM-PO2600701, SCBM-PO2600702, SCBM-PO2600703, SCBM-PO2600704, SCBM-PO2600705, SCBM-PO2600707, SCBM-PO2600709, SCBM-PO2600710, SCBM-PO2600711, SCBM-PO2600715, SCBM-PO2600716, SCBM-PO2600717, SCBM-PO2600718, SCBM-PO2600719, SCBM-PO2600720, SCBM-PO2600721, SCBM-PO2600722, SCBM-PO2600723, SCBM-PO2600725, SCBM-PO2600727, SCBM-PO2600729, SCBM-PO2600730, SCBM-PO2600734, SCBM-PO2600735, SCBM-PO2600742, SCBM-PO2600745, SCBM-PO2600746, SCBM-PO2600747, SCBM-PO2600749, SCBM-PO2600751, SCBM-PO2600752, SCBM-PO2600756, SCBM-PO2600757, SCBM-PO2600758, SCBM-PO2600760, SCBM-PO2600761, SCBM-PO2600762, SCBM-PO2600763, SCBM-PO2600764, SCBM-PO2600765, SCBM-PO2600766, SCBM-PO2600769, SCBM-PO2600774, SCBM-PO2600775, SCBM-PO2600776, SCBM-PO2600778, SCBM-PO2600779, SCBM-PO2600781, SCBM-PO2600786, SCBM-PO2600787, SCBM-PO2600788, SCBM-PO2600789, SCBM-PO2600790, SCBM-PO2600791, SCBM-PO2600792, SCBM-PO2600793, SCBM-PO2600794, SCBM-PO2600797, SCBM-PO2600798, SCBM-PO2600799, SCBM-PO2600800, SCBM-PO2600801, SCBM-PO2600802, SCBM-PO2600803, SCBM-PO2600804, SCBM-PO2600805, SCBM-PO2600808, SCBM-PO2600809, SCBM-PO2600810, SCBM-PO2600812, SCBM-PO2600814, SCBM-PO2600815, SCBM-PO2600817, SCBM-PO2600820, SCBM-PO2600821, SCBM-PO2600822, SCBM-PO2600823, SCBM-PO2600824, SCBM-PO2600825, SCBM-PO2600826, SCBM-PO2600828, SCBM-PO2600830, SCBM-PO2600831, SCBM-PO2600832, SCBM-PO2600833, SCBM-PO2600834, SCBM-PO2600836, SCBM-PO2600838, SCBM-PO2600839, SCBM-PO2600841, SCBM-PO2600842, SCBM-PO2600843, SCBM-PO2600844, SCBM-PO2600848, SCBM-PO2600849, SCBM-PO2600852, SCBM-PO2600853, SCBM-PO2600854, SCBM-PO2600855, SCBM-PO2600856, SCBM-PO2600857, SCBM-PO2600859, SCBM-PO2600860, SCBM-PO2600862, SCBM-PO2600863, SCBM-PO2600864, SCBM-PO2600865, SCBM-PO2600866, SCBM-PO2600867, SCBM-PO2600868, SCBM-PO2600869, SCBM-PO2600871, SCBM-PO2600872, SCBM-PO2600873, SCBM-PO2600875, SCBM-PO2600876, SCBM-PO2600877, SCBM-PO2600878, SCBM-PO2600881, SCBM-PO2600882, SCBM-PO2600883, SCBM-PO2600884, SCBM-PO2600887, SCBM-PO2600888, SCBM-PO2600890, SCBM-PO2600892, SCBM-PO2600894, SCBM-PO2600896, SCBM-PO2600898, SCBM-PO2600899, SCBM-PO2600900, SCBM-PO2600901, SCBM-PO2600905, SCBM-PO2600906, SCBM-PO2600907, SCBM-PO2600908, SCBM-PO2600909, SCBM-PO2600910, SCBM-PO2600911, SCBM-PO2600914, SCBM-PO2600915, SCBM-PO2600916, SCBM-PO2600917, SCBM-PO2600918, SCBM-PO2600920, SCBM-PO2600921, SCBM-PO2600924, SCBM-PO2600925, SCBM-PO2600926, SCBM-PO2600927, SCBM-PO2600928, SCBM-PO2600930, SCBM-PO2600931, SCBM-PO2600932, SCBM-PO2600933, SCBM-PO2600934, SCBM-PO2600935, SCBM-PO2600936, SCBM-PO2600937, SCBM-PO2600938, SCBM-PO2600940, SCBM-PO2600941, SCBM-PO2600942, SCBM-PO2600943, SCBM-PO2600944, SCBM-PO2600945, SCBM-PO2600946, SCBM-PO2600947, SCBM-PO2600951, SCBM-PO2600953, SCBM-PO2600955, SCBM-PO2600956, SCBM-PO2600959, SCBM-PO2600960, SCBM-PO2600962, SCBM-PO2600963, SCBM-PO2600970, SCBM-PO2600971, SCBM-PO2600972, SCBM-PO2600974, SCBM-PO2600975, SCBM-PO2600977, SCBM-PO2600978, SCBM-PO2600981, SCBM-PO2600982, SCBM-PO2600983, SCBM-PO2600984, SCBM-PO2600987, SCBM-PO2600988, SCBM-PO2600989, SCBM-PO2600990, SCBM-PO2600991, SCBM-PO2600992, SCBM-PO2600993, SCBM-PO2600994, SCBM-PO2600996, SCBM-PO2600997, SCBM-PO2600998, SCBM-PO2600999, SCBM-PO2601000, SCBM-PO2601001, SCBM-PO2601003, SCBM-PO2601004, SCBM-PO2601005, SCBM-PO2601007, SCBM-PO2601008, SCBM-PO2601010, SCBM-PO2601012, SCBM-PO2601013, SCBM-PO2601015, SCBM-PO2601016, SCBM-PO2601017, SCBM-PO2601018, SCBM-PO2601019, SCBM-PO2601020, SCBM-PO2601021, SCBM-PO2601022, SCBM-PO2601023, SCBM-PO2601025, SCBM-PO2601027, SCBM-PO2601029, SCBM-PO2601030, SCBM-PO2601032, SCBM-PO2601036, SCBM-PO2601038, SCBM-PO2601039, SCBM-PO2601043, SCBM-PO2601048, SCBM-PO2601049, SCBM-PO2601050, SCBM-PO2601051, SCBM-PO2601052, SCBM-PO2601053, SCBM-PO2601054, SCBM-PO2601055, SCBM-PO2601056, SCBM-PO2601057, SCBM-PO2601058, SCBM-PO2601059, SCBM-PO2601061, SCBM-PO2601062, SCBM-PO2601063, SCBM-PO2601065, SCBM-PO2601066, SCBM-PO2601069, SCBM-PO2601070, SCBM-PO2601071, SCBM-PO2601073, SCBM-PO2601074, SCBM-PO2601077, SCBM-PO2601078, SCBM-PO2601079, SCBM-PO2601080, SCBM-PO2601081, SCBM-PO2601082, SCBM-PO2601084, SCBM-PO2601085, SCBM-PO2601086, SCBM-PO2601087, SCBM-PO2601088, SCBM-PO2601089, SCBM-PO2601094, SCBM-PO2601095, SCBM-PO2601096, SCBM-PO2601098, SCBM-PO2601099, SCBM-PO2601101, SCBM-PO2601106, SCBM-PO2601107, SCBM-PO2601108, SCBM-PO2601109, SCBM-PO2601110, SCBM-PO2601112, SCBM-PO2601114, SCBM-PO2601117, SCBM-PO2601118, SCBM-PO2601125, SCBM-PO2601126, SCBM-PO2601128, SCBM-PO2601129, SCBM-PO2601130, SCBM-PO2601131, SCBM-PO2601132, SCBM-PO2601133, SCBM-PO2601136, SCBM-PO2601139, SCBM-PO2601142, SCBM-PO2601143, SCBM-PO2601144, SCBM-PO2601145, SCBM-PO2601146, SCBM-PO2601147, SCBM-PO2601148, SCBM-PO2601149, SCBM-PO2601150, SCBM-PO2601152, SCBM-PO2601153, SCBM-PO2601154, SCBM-PO2601155, SCBM-PO2601157, SCBM-PO2601160, SCBM-PO2601161, SCBM-PO2601162, SCBM-PO2601163, SCBM-PO2601164, SCBM-PO2601165, SCBM-PO2601166, SCBM-PO2601167, SCBM-PO2601168, SCBM-PO2601169, SCBM-PO2601170, SCBM-PO2601171, SCBM-PO2601172, SCBM-PO2601173, SCBM-PO2601174, SCBM-PO2601177, SCBM-PO2601178, SCBM-PO2601179, SCBM-PO2601181, SCBM-PO2601183, SCBM-PO2601185, SCBM-PO2601186, SCBM-PO2601188, SCBM-PO2601190, SCBM-PO2601191, SCBM-PO2601192, SCBM-PO2601193, SCBM-PO2601194, SCBM-PO2601195, SCBM-PO2601196, SCBM-PO2601198, SCBM-PO2601199, SCBM-PO2601200, SCBM-PO2601201, SCBM-PO2601202, SCBM-PO2601203, SCBM-PO2601205, SCBM-PO2601206, SCBM-PO2601209, SCBM-PO2601211, SCBM-PO2601213, SCBM-PO2601214, SCBM-PO2601215, SCBM-PO2601216, SCBM-PO2601217, SCBM-PO2601218, SCBM-PO2601219, SCBM-PO2601221, SCBM-PO2601225, SCBM-PO2601227, SCBM-PO2601230, SCBM-PO2601232, SCBM-PO2601233, SCBM-PO2601234, SCBM-PO2601235, SCBM-PO2601236, SCBM-PO2601237, SCBM-PO2601238, SCBM-PO2601239, SCBM-PO2601240, SCBM-PO2601241, SCBM-PO2601242, SCBM-PO2601244, SCBM-PO2601245, SCBM-PO2601246, SCBM-PO2601248, SCBM-PO2601250, SCBM-PO2601251, SCBM-PO2601252, SCBM-PO2601253, SCBM-PO2601254, SCBM-PO2601256, SCBM-PO2601258, SCBM-PO2601259, SCBM-PO2601260, SCBM-PO2601261, SCBM-PO2601262, SCBM-PO2601263, SCBM-PO2601264, SCBM-PO2601266, SCBM-PO2601270, SCBM-PO2601271, SCBM-PO2601272, SCBM-PO2601274, SCBM-PO2601276, SCBM-PO2601277, SCBM-PO2601279, SCBM-PO2601280, SCBM-PO2601282, SCBM-PO2601283, SCBM-PO2601284, SCBM-PO2601285, SCBM-PO2601286, SCBM-PO2601287, SCBM-PO2601289, SCBM-PO2601294, SCBM-PO2601295, SCBM-PO2601296, SCBM-PO2601298, SCBM-PO2601299, SCBM-PO2601300, SCBM-PO2601301, SCBM-PO2601302, SCBM-PO2601303, SCBM-PO2601304, SCBM-PO2601305, SCBM-PO2601306, SCBM-PO2601307, SCBM-PO2601308, SCBM-PO2601309, SCBM-PO2601310, SCBM-PO2601312, SCBM-PO2601317, SCBM-PO2601320, SCBM-PO2601321, SCBM-PO2601322, SCBM-PO2601323, SCBM-PO2601324, SCBM-PO2601326, SCBM-PO2601327, SCBM-PO2601328, SCBM-PO2601329, SCBM-PO2601330, SCBM-PO2601333, SCBM-PO2601334, SCBM-PO2601335, SCBM-PO2601336, SCBM-PO2601337, SCBM-PO2601338, SCBM-PO2601339, SCBM-PO2601340, SCBM-PO2601341, SCBM-PO2601342, SCBM-PO2601343, SCBM-PO2601345, SCBM-PO2601346, SCBM-PO2601347, SCBM-PO2601348, SCBM-PO2601349, SCBM-PO2601354, SCBM-PO2601358, SCBM-PO2601359, SCBM-PO2601360, SCBM-PO2601365, SCBM-PO2601366, SCBM-PO2601369, SCBM-PO2601371, SCBM-PO2601373, SCBM-PO2601375, SCBM-PO2601376, SCBM-PO2601377, SCBM-PO2601380, SCBM-PO2601382, SCBM-PO2601384, SCBM-PO2601385, SCBM-PO2601386, SCBM-PO2601388, SCBM-PO2601389, SCBM-PO2601390, SCBM-PO2601392, SCBM-PO2601393, SCBM-PO2601394, SCBM-PO2601395, SCBM-PO2601403, SCBM-PO2601407, SCBM-PO2601410, SCBM-PO2601411, SCBM-PO2601412, SCBM-PO2601413, SCBM-PO2601415, SCBM-PO2601416, SCBM-PO2601418, SCBM-PO2601420, SCBM-PO2601422, SCBM-PO2601427, SCBM-PO2601439, SCBM-PO2601443, SCBM-PO2601448, SCBM-PO2601452, SCBM-PO2601455, SCBM-PO2601460, SCBM-PO2601461, SCBM-PO2601462, SCBM-PO2601465, SCBM-PO2601470, SCBM-PO2601473, SCBM-PO2601477, SCBM-PO2601479, SCBM-PO2601480, SCBM-PO2601482, SCBM-PO2601483, SCBM-PO2601486, SCBM-PO2601487, SCBM-PO2601494, SCBM-PO2601496, SCBM-PO2601497, SCBM-PO2601500, SCBM-PO2601508, SCBM-PO2601512, SCBM-PO2601530, SCBM-PO2601531, SCBM-PO2601536, SCBM-PO2601571

## PR procurement clock differences over one day

- CPR-028843: Sourcing; workbook `2026-07-17T10:02:21Z`; F&O modified-time seed `2026-07-20T05:13:17Z`.
- PR-001700: Sourcing; workbook `2026-09-01T10:14:53Z`; F&O modified-time seed `2026-09-07T11:02:55Z`.
- PR-001701: Sourcing; workbook `2026-09-01T10:21:57Z`; F&O modified-time seed `2026-09-07T11:03:55Z`.
- PR-001702: Sourcing; workbook `2026-08-25T12:18:43Z`; F&O modified-time seed `2026-09-07T11:04:49Z`.
- PR-001725: Sourcing; workbook `2026-09-04T16:11:56Z`; F&O modified-time seed `2026-09-07T12:34:56Z`.
- CPR-034162: Sourcing; workbook `2026-08-31T17:33:35Z`; F&O modified-time seed `2026-09-04T04:56:36Z`.
- PR-001726: Sourcing; workbook `2026-08-31T17:03:57Z`; F&O modified-time seed `2026-09-04T04:57:00Z`.
- CPR-034154: Priced — awaiting approval; workbook `2026-08-27T16:40:14Z`; F&O modified-time seed `2026-09-04T04:56:07Z`.
- CPR-034527: Sourcing; workbook `2026-09-03T15:22:31Z`; F&O modified-time seed `2026-09-07T05:36:43Z`.
- CPR-034541: Sourcing; workbook `2026-09-04T13:20:56Z`; F&O modified-time seed `2026-09-07T09:14:14Z`.
- PR-001742: Sourcing; workbook `2026-09-04T09:34:09Z`; F&O modified-time seed `2026-09-07T13:50:11Z`.
- PR-001747: Sourcing; workbook `2026-09-02T13:36:52Z`; F&O modified-time seed `2026-09-07T12:22:47Z`.
- CPR-034663: Sourcing; workbook `2026-09-04T10:52:11Z`; F&O modified-time seed `2026-09-07T05:26:54Z`.
- CPR-034667: Sourcing; workbook `2026-09-04T13:46:06Z`; F&O modified-time seed `2026-09-07T12:41:53Z`.
- CPR-034805: Sourcing; workbook `2026-09-04T11:41:51Z`; F&O modified-time seed `2026-09-07T08:14:46Z`.
- CPR-034616: Sourcing; workbook `2026-09-04T11:47:01Z`; F&O modified-time seed `2026-09-07T07:29:24Z`.
- CPR-034832: Sourcing; workbook `2026-09-04T13:41:53Z`; F&O modified-time seed `2026-09-07T11:43:56Z`.
- CPR-034902: Sourcing; workbook `2026-09-05T13:41:52Z`; F&O modified-time seed `2026-09-07T11:54:49Z`.
- CPR-034908: Sourcing; workbook `2026-09-05T14:42:02Z`; F&O modified-time seed `2026-09-07T11:47:44Z`.
- CPR-034878: Sourcing; workbook `2026-09-05T14:42:01Z`; F&O modified-time seed `2026-09-07T05:35:57Z`.
- CPR-034911: Sourcing; workbook `2026-09-05T14:42:00Z`; F&O modified-time seed `2026-09-07T13:56:32Z`.
- CPR-034808: Sourcing; workbook `2026-09-05T14:41:59Z`; F&O modified-time seed `2026-09-07T13:56:16Z`.
- CPR-034914: Sourcing; workbook `2026-09-05T14:41:58Z`; F&O modified-time seed `2026-09-07T08:24:28Z`.
- CPR-034920: Sourcing; workbook `2026-09-05T15:41:51Z`; F&O modified-time seed `2026-09-07T07:34:00Z`.

## PO clock evidence

Only like-for-like approval clocks are comparable: 2/3 (66.67%) are within one day. The 1,405 workbook LPO-sent clocks are not compared with later receipt-posting dates because they are different events.

- SCBM-PO2601579: Finance; workbook `2026-09-04T09:44:26Z`; capture assignment `2026-09-07T13:12:22Z`.

## pr.xlsx amount differences

- PR-000007: workbook AED 720.00; adjusted excl. VAT unavailable; live excl. VAT AED 720.00; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- PR-000008: workbook AED 365.00; adjusted excl. VAT unavailable; live excl. VAT AED 365.00; difference unavailable; basis `unknown`; codes `(blank)/(blank)`.
- PR-000018: workbook AED 726.00; adjusted excl. VAT unavailable; live excl. VAT AED 726.00; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- PR-000107: workbook AED 777.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000111: workbook AED 101.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000114: workbook AED 112.14; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000115: workbook AED 10,000.00; adjusted excl. VAT unavailable; live excl. VAT AED 10,000.00; difference unavailable; basis `unknown`; codes `(blank)/SR-SRVC`.
- PR-000117: workbook AED 38.20; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000139: workbook AED 648.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000105: workbook AED 1,025.50; adjusted excl. VAT unavailable; live excl. VAT AED 1,025.50; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- PR-000142: workbook AED 2,100.00; adjusted excl. VAT unavailable; live excl. VAT AED 2,100.00; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- PR-000145: workbook AED 2,265.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000149: workbook AED 1,115.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000155: workbook AED 210.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000158: workbook AED 142.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000167: workbook AED 287.43; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000168: workbook AED 170.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000178: workbook AED 35.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000180: workbook AED 485.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000188: workbook AED 600.00; adjusted excl. VAT unavailable; live excl. VAT AED 600.00; difference unavailable; basis `unknown`; codes `(blank)/SR-SRVC`.
- PR-000196: workbook AED 35.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000197: workbook AED 940.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000224: workbook AED 280.00; adjusted excl. VAT AED 266.67; live excl. VAT AED 280.00; difference AED -13.33; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- PR-000225: workbook AED 793.50; adjusted excl. VAT AED 755.71; live excl. VAT AED 755.00; difference AED 0.71; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- PR-000228: workbook AED 13,600.00; adjusted excl. VAT unavailable; live excl. VAT AED 13,600.00; difference unavailable; basis `unknown`; codes `(blank)/SR-SRVC`.
- PR-000236: workbook AED 1,240.00; adjusted excl. VAT unavailable; live excl. VAT AED 1,240.00; difference unavailable; basis `unknown`; codes `(blank)/(blank)`.
- PR-000237: workbook AED 155,000.00; adjusted excl. VAT unavailable; live excl. VAT AED 155,000.00; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- CPR-000003: workbook AED 750.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000008: workbook AED 41.35; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000010: workbook AED 312.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000014: workbook AED 130.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000036: workbook AED 825.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000038: workbook AED 345.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000040: workbook AED 67.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000042: workbook AED 90.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000047: workbook AED 57.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000048: workbook AED 568.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000049: workbook AED 360.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000260: workbook AED 70.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000065: workbook AED 7.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000067: workbook AED 2.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000078: workbook AED 35.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000285: workbook AED 1,000.00; adjusted excl. VAT unavailable; live excl. VAT AED 1,000.00; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- CPR-000095: workbook AED 21,678.99; adjusted excl. VAT AED 20,646.66; live excl. VAT AED 20,315.70; difference AED 330.96; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-000098: workbook AED 63.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000111: workbook AED 102.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000219: workbook AED 134.98; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000432: workbook AED 136.59; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000437: workbook AED 805.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000232: workbook AED 3.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000478: workbook AED 143.13; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000297: workbook AED 7,625.31; adjusted excl. VAT AED 7,262.20; live excl. VAT AED 6,700.00; difference AED 562.20; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD`.
- CPR-000591: workbook AED 407.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000458: workbook AED 12.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000673: workbook AED 400.00; adjusted excl. VAT unavailable; live excl. VAT AED 400.00; difference unavailable; basis `unknown`; codes `(blank)/SR-SRVC`.
- CPR-000707: workbook AED 282.27; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000710: workbook AED 80,213.19; adjusted excl. VAT unavailable; live excl. VAT AED 80,213.19; difference unavailable; basis `unknown`; codes `(blank)/SR-SRVC`.
- CPR-000763: workbook AED 50.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000794: workbook AED 1,845.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000309: workbook AED 829.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000644: workbook AED 6.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000762: workbook AED 27.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000832: workbook AED 356.30; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000875: workbook AED 254.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000317: workbook AED 1,550.00; adjusted excl. VAT unavailable; live excl. VAT AED 1,550.00; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- PR-000318: workbook AED 1,132.96; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001054: workbook AED 14.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001051: workbook AED 280.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001059: workbook AED 314.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000320: workbook AED 26,450.00; adjusted excl. VAT unavailable; live excl. VAT AED 26,450.00; difference unavailable; basis `unknown`; codes `(blank)/(blank)`.
- CPR-000976: workbook AED 6,061.55; adjusted excl. VAT unavailable; live excl. VAT AED 5,791.00; difference unavailable; basis `unknown`; codes `(blank)/SR-SRVC, SR-RCVR/SR-SRVC`.
- CPR-001163: workbook AED 2,750.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001134: workbook AED 74.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001172: workbook AED 175.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001177: workbook AED 1,400.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001184: workbook AED 1,320.59; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001231: workbook AED 4,711.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001262: workbook AED 2,900.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000327: workbook AED 517.50; adjusted excl. VAT unavailable; live excl. VAT AED 517.50; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- CPR-001511: workbook AED 5.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001530: workbook AED 3,482.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001486: workbook AED 4.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001538: workbook AED 141.60; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001548: workbook AED 1,972.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-000607: workbook AED 16.33; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000332: workbook AED 39.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000333: workbook AED 846.50; adjusted excl. VAT unavailable; live excl. VAT AED 840.00; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank), SR-RCVR/SR-GOOD`.
- CPR-001539: workbook AED 3,591.22; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001698: workbook AED 41.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000336: workbook AED 791.00; adjusted excl. VAT unavailable; live excl. VAT AED 791.00; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- CPR-001771: workbook AED 956.69; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001687: workbook AED 6.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001889: workbook AED 295.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001969: workbook AED 1.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001950: workbook AED 15.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001974: workbook AED 382.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001984: workbook AED 77.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001998: workbook AED 50.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-002008: workbook AED 1,900.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-001996: workbook AED 54,471.19; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-002062: workbook AED 3,540.93; adjusted excl. VAT AED 3,372.31; live excl. VAT AED 3,086.60; difference AED 285.71; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-002182: workbook AED 40.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-002457: workbook AED 800.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-002655: workbook AED 1,678.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-002668: workbook AED 300.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-002499: workbook AED 16,113.96; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-002725: workbook AED 1,756.63; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-002790: workbook AED 100.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000364: workbook AED 2,560.00; adjusted excl. VAT unavailable; live excl. VAT AED 2,560.00; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- CPR-002915: workbook AED 15.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000365: workbook AED 89,500.00; adjusted excl. VAT unavailable; live excl. VAT AED 89,500.00; difference unavailable; basis `unknown`; codes `(blank)/(blank)`.
- CPR-002962: workbook AED 80.05; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-002989: workbook AED 140.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-002991: workbook AED 11.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-003202: workbook AED 1,590.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-003245: workbook AED 2,283.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-003246: workbook AED 13,750.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-003247: workbook AED 37,500.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-003248: workbook AED 2,500.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-003249: workbook AED 2,283.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000392: workbook AED 6,600.00; adjusted excl. VAT unavailable; live excl. VAT AED 6,600.00; difference unavailable; basis `unknown`; codes `(blank)/(blank)`.
- PR-000397: workbook AED 268,684.04; adjusted excl. VAT unavailable; live excl. VAT AED 248,455.54; difference unavailable; basis `unknown`; codes `(blank)/(blank), SR-RCVR/SR-GOOD`.
- CPR-003315: workbook AED 26.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-003417: workbook AED 520.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-003416: workbook AED 19,468.68; adjusted excl. VAT AED 18,541.60; live excl. VAT AED 18,362.50; difference AED 179.10; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-003424: workbook AED 520.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-003407: workbook AED 67.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000402: workbook AED 20,494.00; adjusted excl. VAT unavailable; live excl. VAT AED 20,494.00; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- CPR-003409: workbook AED 27.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000406: workbook AED 18,000.00; adjusted excl. VAT unavailable; live excl. VAT AED 18,000.00; difference unavailable; basis `unknown`; codes `(blank)/(blank)`.
- CPR-003703: workbook AED 187.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-003688: workbook AED 54.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-003811: workbook AED 84,000.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-003708: workbook AED 17.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-003797: workbook AED 3.82; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004009: workbook AED 47.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-003686: workbook AED 1,282.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004044: workbook AED 234.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004049: workbook AED 460.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000419: workbook AED 1,760.61; adjusted excl. VAT AED 1,760.61; live excl. VAT AED 147.95; difference AED 1,612.66; basis `non-VAT`; codes `OS/OS-SRVC`.
- CPR-004168: workbook AED 207.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004285: workbook AED 6.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004404: workbook AED 40.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000420: workbook AED 4.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004437: workbook AED 205.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004520: workbook AED 21.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004548: workbook AED 123.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004609: workbook AED 90.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004957: workbook AED 2.95; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004466: workbook AED 2,607.77; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004467: workbook AED 6,339.89; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004468: workbook AED 10,764.40; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004964: workbook AED 60.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000433: workbook AED 159,000.00; adjusted excl. VAT AED 151,428.57; live excl. VAT AED 159,000.00; difference AED -7,571.43; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-005149: workbook AED 6,500.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005157: workbook AED 1,005.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005374: workbook AED 6,000.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005392: workbook AED 579.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005548: workbook AED 275.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000444: workbook AED 14,995.60; adjusted excl. VAT unavailable; live excl. VAT AED 14,995.60; difference unavailable; basis `unknown`; codes `(blank)/(blank)`.
- CPR-005593: workbook AED 1,195.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005278: workbook AED 108.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005620: workbook AED 1,388.71; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005617: workbook AED 1,005.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004790: workbook AED 4.96; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005701: workbook AED 7.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005734: workbook AED 19.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005814: workbook AED 87.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005840: workbook AED 161.35; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004913: workbook AED 62.96; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-004911: workbook AED 30.46; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005936: workbook AED 95.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005943: workbook AED 53.63; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005830: workbook AED 18.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005947: workbook AED 6.55; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006008: workbook AED 13.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000459: workbook AED 4,000.00; adjusted excl. VAT unavailable; live excl. VAT AED 4,000.00; difference unavailable; basis `unknown`; codes `(blank)/SR-SRVC`.
- CPR-006129: workbook AED 13.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006161: workbook AED 17.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006197: workbook AED 725.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005980: workbook AED 9.60; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006203: workbook AED 25.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006216: workbook AED 30.10; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006180: workbook AED 225.19; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006290: workbook AED 724.75; adjusted excl. VAT AED 690.24; live excl. VAT AED 650.00; difference AED 40.24; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-006248: workbook AED 150.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006375: workbook AED 2.90; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006287: workbook AED 8.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-005014: workbook AED 1,184.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006345: workbook AED 2,708.40; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006494: workbook AED 92.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006508: workbook AED 690.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006512: workbook AED 1,170.02; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006388: workbook AED 11.05; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006387: workbook AED 107.52; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006323: workbook AED 61.80; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006322: workbook AED 11.40; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006579: workbook AED 20.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006587: workbook AED 650.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006634: workbook AED 340.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006702: workbook AED 270.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006778: workbook AED 820.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006844: workbook AED 2,953.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006850: workbook AED 210.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006868: workbook AED 1,425.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006854: workbook AED 163,859.99; adjusted excl. VAT AED 156,057.13; live excl. VAT AED 155,960.37; difference AED 96.76; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-006783: workbook AED 12.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006925: workbook AED 90,477.14; adjusted excl. VAT AED 86,168.70; live excl. VAT AED 86,086.80; difference AED 81.90; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-006967: workbook AED 28.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006969: workbook AED 37.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-007082: workbook AED 1,252.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-007115: workbook AED 2.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-006659: workbook AED 60.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-007121: workbook AED 10.55; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-007272: workbook AED 150.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-007381: workbook AED 60.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-007395: workbook AED 1,593.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-007416: workbook AED 61,819.60; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-007487: workbook AED 96.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-007692: workbook AED 192.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-007745: workbook AED 8.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-007839: workbook AED 347.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008011: workbook AED 8.80; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008180: workbook AED 12.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008155: workbook AED 8.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-007653: workbook AED 64.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008367: workbook AED 1,380.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008372: workbook AED 1,326.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008375: workbook AED 520.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008456: workbook AED 7.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008497: workbook AED 505.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008482: workbook AED 3.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000554: workbook AED 416.50; adjusted excl. VAT AED 416.50; live excl. VAT AED 35.00; difference AED 381.50; basis `non-VAT`; codes `OS/SR-SRVC`.
- CPR-008347: workbook AED 14.05; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008534: workbook AED 20.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008508: workbook AED 279.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008502: workbook AED 757.93; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008639: workbook AED 13.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008417: workbook AED 21.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008816: workbook AED 3,195.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008895: workbook AED 487.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008905: workbook AED 325.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008915: workbook AED 2,962.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008946: workbook AED 32.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008572: workbook AED 400.70; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000558: workbook AED 1,166.20; adjusted excl. VAT AED 1,166.20; live excl. VAT AED 98.00; difference AED 1,068.20; basis `non-VAT`; codes `OS/SR-SRVC`.
- CPR-009050: workbook AED 285.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009047: workbook AED 2,977.21; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009058: workbook AED 115.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008839: workbook AED 223.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009109: workbook AED 27.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-008690: workbook AED 77.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009144: workbook AED 491.44; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009145: workbook AED 325.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009189: workbook AED 213.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009051: workbook AED 150.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000574: workbook AED 918.60; adjusted excl. VAT unavailable; live excl. VAT AED 876.00; difference unavailable; basis `mixed VAT basis`; codes `SR-RCVR/OS-GOOD, SR-RCVR/SR-GOOD`.
- CPR-009593: workbook AED 1,010.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009594: workbook AED 11.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009616: workbook AED 85.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009633: workbook AED 351.19; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009631: workbook AED 755.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009700: workbook AED 492.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009702: workbook AED 492.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009703: workbook AED 420.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009704: workbook AED 447.20; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009720: workbook AED 107.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009759: workbook AED 262.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009761: workbook AED 20,974.54; adjusted excl. VAT unavailable; live excl. VAT AED 20,590.04; difference unavailable; basis `mixed VAT basis`; codes `OS/OS-GOOD, OS/SR-SRVC, SR-RCVR/SR-SRVC`.
- CPR-009800: workbook AED 91,115.20; adjusted excl. VAT unavailable; live excl. VAT AED 89,871.45; difference unavailable; basis `mixed VAT basis`; codes `OS/SR-SRVC, SR-RCVR/SR-SRVC`.
- CPR-009810: workbook AED 755.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009841: workbook AED 275.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009875: workbook AED 160.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009834: workbook AED 0.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-009843: workbook AED 726.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-010101: workbook AED 4.80; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-010144: workbook AED 983.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-010099: workbook AED 2,823.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-010172: workbook AED 1.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-010275: workbook AED 15.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-010305: workbook AED 55.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-010565: workbook AED 184.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-010585: workbook AED 156.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-010587: workbook AED 150.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-010562: workbook AED 495.05; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-010553: workbook AED 610.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-010617: workbook AED 20.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-010748: workbook AED 253.31; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000620: workbook AED 8,600.00; adjusted excl. VAT unavailable; live excl. VAT AED 8,600.00; difference unavailable; basis `unknown`; codes `(blank)/SR-GOOD`.
- CPR-010937: workbook AED 38.05; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011003: workbook AED 199.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011149: workbook AED 25.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011158: workbook AED 52.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-010803: workbook AED 2,926.15; adjusted excl. VAT AED 2,786.81; live excl. VAT AED 2,170.00; difference AED 616.81; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-011156: workbook AED 36.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011189: workbook AED 27.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011195: workbook AED 260.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011233: workbook AED 115.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011303: workbook AED 476.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011305: workbook AED 476.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011390: workbook AED 116.70; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011595: workbook AED 1,300.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011596: workbook AED 1,067.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011739: workbook AED 507.70; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011816: workbook AED 978.66; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011579: workbook AED 261.40; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011821: workbook AED 800.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011823: workbook AED 800.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011824: workbook AED 800.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011825: workbook AED 800.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011826: workbook AED 800.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011745: workbook AED 10.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011827: workbook AED 800.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011828: workbook AED 800.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000654: workbook AED 13,900.48; adjusted excl. VAT unavailable; live excl. VAT AED 13,821.50; difference unavailable; basis `unknown`; codes `(blank)/(blank), SR-RCVR/SR-GOOD`.
- CPR-011832: workbook AED 10.55; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011847: workbook AED 10.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011876: workbook AED 65.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-010295: workbook AED 4,634.60; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-011925: workbook AED 79.53; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012077: workbook AED 4.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012084: workbook AED 800.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012128: workbook AED 524.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012132: workbook AED 1.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012038: workbook AED 13.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012211: workbook AED 60.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012219: workbook AED 103.60; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012147: workbook AED 289.78; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000670: workbook AED 220,200.00; adjusted excl. VAT unavailable; live excl. VAT AED 220,200.00; difference unavailable; basis `unknown`; codes `OS/(blank)`.
- CPR-012531: workbook AED 67.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012541: workbook AED 200.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012558: workbook AED 14,011.50; adjusted excl. VAT AED 13,344.29; live excl. VAT AED 13,330.00; difference AED 14.29; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-012611: workbook AED 40.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012628: workbook AED 21.20; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012658: workbook AED 391.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012556: workbook AED 70.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012791: workbook AED 151.73; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012808: workbook AED 165.49; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012843: workbook AED 31.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-012968: workbook AED 1,963.90; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000688: workbook AED 282,285.72; adjusted excl. VAT unavailable; live excl. VAT AED 282,285.72; difference unavailable; basis `unknown`; codes `(blank)/SR-SRVC`.
- CPR-013052: workbook AED 575.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-013635: workbook AED 5.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-013671: workbook AED 947.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-013659: workbook AED 2.90; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-013770: workbook AED 4.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-013787: workbook AED 4,190.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014162: workbook AED 635.03; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014179: workbook AED 108.14; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014201: workbook AED 34.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014205: workbook AED 37.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014412: workbook AED 240.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-013926: workbook AED 164.73; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014460: workbook AED 339.87; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014474: workbook AED 80.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014501: workbook AED 190.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014537: workbook AED 9.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014587: workbook AED 27.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014506: workbook AED 75,499.26; adjusted excl. VAT AED 71,904.06; live excl. VAT AED 71,881.77; difference AED 22.29; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-014688: workbook AED 70.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014720: workbook AED 726.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014723: workbook AED 1,329.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014726: workbook AED 680.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014731: workbook AED 2,539.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014704: workbook AED 187.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000727: workbook AED 5,045.60; adjusted excl. VAT AED 5,045.60; live excl. VAT AED 424.00; difference AED 4,621.60; basis `non-VAT`; codes `OS/SR-SRVC`.
- CPR-014703: workbook AED 650.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014973: workbook AED 100.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014975: workbook AED 5,469.80; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-014994: workbook AED 49.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000737: workbook AED 9,234.40; adjusted excl. VAT AED 9,234.40; live excl. VAT AED 776.00; difference AED 8,458.40; basis `non-VAT`; codes `OS/SR-SRVC`.
- CPR-015230: workbook AED 25.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-015238: workbook AED 1,627.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-015040: workbook AED 45.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-015415: workbook AED 697.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-015519: workbook AED 450.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-015081: workbook AED 947.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-015786: workbook AED 86.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-015826: workbook AED 5.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-015866: workbook AED 240.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-016120: workbook AED 4.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-016355: workbook AED 32.76; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-016371: workbook AED 96.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-016379: workbook AED 429.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-016537: workbook AED 47.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-016630: workbook AED 3.95; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-016528: workbook AED 13.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-016676: workbook AED 53.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-016808: workbook AED 115.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-016896: workbook AED 180.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-016897: workbook AED 165.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000816: workbook AED 9,117.50; adjusted excl. VAT AED 8,683.33; live excl. VAT AED 8,400.00; difference AED 283.33; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD`.
- CPR-016923: workbook AED 779.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-016947: workbook AED 5.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-016953: workbook AED 5.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-016981: workbook AED 26.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017209: workbook AED 1,260.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017237: workbook AED 51.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017266: workbook AED 118.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017416: workbook AED 3.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017431: workbook AED 7,302.70; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017433: workbook AED 10.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017445: workbook AED 3,425.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017449: workbook AED 91.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017485: workbook AED 218.03; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017492: workbook AED 1,510.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017448: workbook AED 313.60; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017515: workbook AED 1,305.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017521: workbook AED 38.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017655: workbook AED 3,675.59; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000880: workbook AED 487.90; adjusted excl. VAT AED 487.90; live excl. VAT AED 41.00; difference AED 446.90; basis `non-VAT`; codes `OS/SR-SRVC`.
- PR-000881: workbook AED 2,475.20; adjusted excl. VAT AED 2,475.20; live excl. VAT AED 208.00; difference AED 2,267.20; basis `non-VAT`; codes `OS/SR-SRVC`.
- CPR-017722: workbook AED 302.74; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017523: workbook AED 23.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017749: workbook AED 28.60; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017784: workbook AED 3,000.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017819: workbook AED 238.31; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017850: workbook AED 385.86; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018012: workbook AED 700.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018025: workbook AED 4.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-017913: workbook AED 10.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000899: workbook AED 2,097.45; adjusted excl. VAT AED 1,997.57; live excl. VAT AED 1,749.00; difference AED 248.57; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD`.
- CPR-018142: workbook AED 89.20; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018168: workbook AED 48.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018206: workbook AED 187.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018237: workbook AED 234.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018274: workbook AED 360.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018275: workbook AED 260.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018450: workbook AED 17.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018479: workbook AED 603.30; adjusted excl. VAT AED 574.57; live excl. VAT AED 551.00; difference AED 23.57; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-018507: workbook AED 4,512.90; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018517: workbook AED 105.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018618: workbook AED 61.90; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018699: workbook AED 135.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018730: workbook AED 117.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018728: workbook AED 142.86; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018816: workbook AED 649.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018723: workbook AED 75.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018842: workbook AED 53,164.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000917: workbook AED 10,800.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018882: workbook AED 53,164.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018962: workbook AED 1,467.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018965: workbook AED 166.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018968: workbook AED 375.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018978: workbook AED 610.53; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-018904: workbook AED 79.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019023: workbook AED 5.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019038: workbook AED 30.70; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019058: workbook AED 425.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019087: workbook AED 5.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019283: workbook AED 27.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019337: workbook AED 110.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019339: workbook AED 410.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019411: workbook AED 5.90; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019479: workbook AED 199.85; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019523: workbook AED 525.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019524: workbook AED 262.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019532: workbook AED 110.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019585: workbook AED 1,870.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019595: workbook AED 7.95; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019604: workbook AED 225.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000976: workbook AED 27.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019724: workbook AED 37.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019767: workbook AED 240.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019772: workbook AED 2,700.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019777: workbook AED 60.12; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000993: workbook AED 343.40; adjusted excl. VAT AED 327.05; live excl. VAT AED 318.00; difference AED 9.05; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD`.
- CPR-019697: workbook AED 85,059.86; adjusted excl. VAT AED 81,009.39; live excl. VAT AED 80,708.20; difference AED 301.19; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-019854: workbook AED 360.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019855: workbook AED 142.86; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019972: workbook AED 33.20; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019913: workbook AED 65.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020108: workbook AED 10.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020145: workbook AED 79.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-000999: workbook AED 2,559.75; adjusted excl. VAT AED 2,437.86; live excl. VAT AED 2,295.00; difference AED 142.86; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD`.
- CPR-020144: workbook AED 22.51; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020183: workbook AED 45.15; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020191: workbook AED 37.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020256: workbook AED 592.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020241: workbook AED 21.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020363: workbook AED 25.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020545: workbook AED 1,125.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020550: workbook AED 95.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020581: workbook AED 88.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001017: workbook AED 60.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020629: workbook AED 1,920.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020635: workbook AED 620.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020684: workbook AED 4.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020692: workbook AED 588.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020682: workbook AED 5.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001027: workbook AED 499.80; adjusted excl. VAT AED 499.80; live excl. VAT AED 42.00; difference AED 457.80; basis `non-VAT`; codes `OS/SR-SRVC`.
- CPR-020765: workbook AED 35.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020702: workbook AED 34.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001031: workbook AED 178.50; adjusted excl. VAT AED 178.50; live excl. VAT AED 15.00; difference AED 163.50; basis `non-VAT`; codes `OS/SR-SRVC`.
- PR-001033: workbook AED 1,755.25; adjusted excl. VAT AED 1,755.25; live excl. VAT AED 147.50; difference AED 1,607.75; basis `non-VAT`; codes `OS/SR-SRVC`.
- CPR-020811: workbook AED 7.95; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-020823: workbook AED 24.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001049: workbook AED 245.78; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001051: workbook AED 466.31; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001053: workbook AED 4,746.71; adjusted excl. VAT AED 4,520.68; live excl. VAT AED 4,489.30; difference AED 31.38; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-021025: workbook AED 2.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-021145: workbook AED 1.80; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-021440: workbook AED 49.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-021512: workbook AED 3,415.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-021514: workbook AED 3,080.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001061: workbook AED 1,013.86; adjusted excl. VAT unavailable; live excl. VAT AED 970.93; difference unavailable; basis `mixed VAT basis`; codes `SR-RCVR/OS-GOOD, SR-RCVR/SR-GOOD`.
- CPR-021613: workbook AED 28.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-021443: workbook AED 3.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-021445: workbook AED 40.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-021622: workbook AED 3.70; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-021630: workbook AED 790.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-021647: workbook AED 10.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-021983: workbook AED 42.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-022056: workbook AED 188.40; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-022083: workbook AED 23.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-022119: workbook AED 684.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001128: workbook AED 748.55; adjusted excl. VAT unavailable; live excl. VAT AED 716.59; difference unavailable; basis `mixed VAT basis`; codes `SR-RCVR/OS-GOOD, SR-RCVR/SR-GOOD`.
- PR-001129: workbook AED 748.55; adjusted excl. VAT unavailable; live excl. VAT AED 716.59; difference unavailable; basis `mixed VAT basis`; codes `SR-RCVR/OS-GOOD, SR-RCVR/SR-GOOD`.
- PR-001130: workbook AED 748.55; adjusted excl. VAT unavailable; live excl. VAT AED 716.59; difference unavailable; basis `mixed VAT basis`; codes `SR-RCVR/OS-GOOD, SR-RCVR/SR-GOOD`.
- CPR-022319: workbook AED 1,155.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-022334: workbook AED 110.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-022342: workbook AED 325.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001138: workbook AED 1,425.50; adjusted excl. VAT unavailable; live excl. VAT AED 1,425.50; difference unavailable; basis `unknown`; codes `(blank)/SR-SRVC`.
- CPR-022394: workbook AED 925.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001139: workbook AED 1,222.47; adjusted excl. VAT unavailable; live excl. VAT AED 1,175.97; difference unavailable; basis `mixed VAT basis`; codes `SR-RCVR/OS-GOOD, SR-RCVR/SR-GOOD`.
- CPR-022403: workbook AED 9.60; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001141: workbook AED 1,106.42; adjusted excl. VAT unavailable; live excl. VAT AED 1,064.09; difference unavailable; basis `mixed VAT basis`; codes `SR-RCVR/OS-GOOD, SR-RCVR/SR-GOOD`.
- CPR-022446: workbook AED 9.35; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-022416: workbook AED 58.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-022467: workbook AED 480.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-022471: workbook AED 325.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-022487: workbook AED 362.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001152: workbook AED 1,065.85; adjusted excl. VAT unavailable; live excl. VAT AED 1,025.45; difference unavailable; basis `mixed VAT basis`; codes `SR-RCVR/OS-GOOD, SR-RCVR/SR-GOOD`.
- CPR-022538: workbook AED 862.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-022539: workbook AED 99.40; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001158: workbook AED 773.67; adjusted excl. VAT unavailable; live excl. VAT AED 743.52; difference unavailable; basis `mixed VAT basis`; codes `SR-RCVR/OS-GOOD, SR-RCVR/SR-GOOD`.
- CPR-022558: workbook AED 7.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-022772: workbook AED 48.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-022910: workbook AED 865.45; adjusted excl. VAT AED 824.24; live excl. VAT AED 824.00; difference AED 0.24; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-022916: workbook AED 129.10; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001183: workbook AED 1,000.00; adjusted excl. VAT unavailable; live excl. VAT AED 1,000.00; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- CPR-022977: workbook AED 4,696.45; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023074: workbook AED 365.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023145: workbook AED 47.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023377: workbook AED 32.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-019645: workbook AED 26,417.31; adjusted excl. VAT AED 25,159.34; live excl. VAT AED 25,101.00; difference AED 58.34; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-023525: workbook AED 60.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023655: workbook AED 160.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023656: workbook AED 275.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023657: workbook AED 250.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023661: workbook AED 120.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023649: workbook AED 18.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023663: workbook AED 6.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023775: workbook AED 102.73; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023869: workbook AED 425.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023881: workbook AED 9.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023722: workbook AED 14.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023938: workbook AED 1,150.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023984: workbook AED 577.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023992: workbook AED 577.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024080: workbook AED 476.10; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024237: workbook AED 10,439.75; adjusted excl. VAT AED 9,942.62; live excl. VAT AED 9,884.52; difference AED 58.10; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-024302: workbook AED 601.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024364: workbook AED 23.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024525: workbook AED 268.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024595: workbook AED 165.60; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024608: workbook AED 23.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024651: workbook AED 22,081.30; adjusted excl. VAT AED 21,029.81; live excl. VAT AED 21,000.00; difference AED 29.81; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-024655: workbook AED 10.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024676: workbook AED 500.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024705: workbook AED 111.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024750: workbook AED 190.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024751: workbook AED 75.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024669: workbook AED 654.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024732: workbook AED 14.85; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-023987: workbook AED 122.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024870: workbook AED 125.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024938: workbook AED 865.45; adjusted excl. VAT AED 824.24; live excl. VAT AED 824.00; difference AED 0.24; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- PR-001259: workbook AED 458.42; adjusted excl. VAT unavailable; live excl. VAT AED 439.60; difference unavailable; basis `mixed VAT basis`; codes `SR-RCVR/OS-GOOD, SR-RCVR/SR-GOOD`.
- CPR-025051: workbook AED 1,250.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025083: workbook AED 106.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025101: workbook AED 50.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025110: workbook AED 9.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025130: workbook AED 6.85; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-024753: workbook AED 192.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025164: workbook AED 30.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025172: workbook AED 140.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001271: workbook AED 2,257.50; adjusted excl. VAT unavailable; live excl. VAT AED 2,257.50; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- CPR-025238: workbook AED 30.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025237: workbook AED 1,628.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025283: workbook AED 360.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025018: workbook AED 42.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025299: workbook AED 19.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025335: workbook AED 9.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025461: workbook AED 37.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025524: workbook AED 1,277.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001277: workbook AED 12,802.00; adjusted excl. VAT AED 12,192.38; live excl. VAT AED 12,045.00; difference AED 147.38; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-025556: workbook AED 38.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025580: workbook AED 240.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025565: workbook AED 214.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025588: workbook AED 85.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025656: workbook AED 86.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025675: workbook AED 249.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025685: workbook AED 720.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025742: workbook AED 37.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025944: workbook AED 315.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025963: workbook AED 349.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026004: workbook AED 145.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-025996: workbook AED 35.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026006: workbook AED 20.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026018: workbook AED 17,357.21; adjusted excl. VAT AED 16,530.68; live excl. VAT AED 15,569.00; difference AED 961.68; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-026056: workbook AED 43.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026067: workbook AED 385.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026068: workbook AED 52.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026109: workbook AED 24.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026113: workbook AED 120.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026118: workbook AED 12,320.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026176: workbook AED 3.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026197: workbook AED 100.60; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026224: workbook AED 74.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026225: workbook AED 262.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001324: workbook AED 12,138.00; adjusted excl. VAT AED 12,138.00; live excl. VAT AED 1,020.00; difference AED 11,118.00; basis `non-VAT`; codes `OS/SR-SRVC`.
- CPR-026242: workbook AED 4.05; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026302: workbook AED 19.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026345: workbook AED 2.90; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026348: workbook AED 93.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001339: workbook AED 1,142.40; adjusted excl. VAT AED 1,142.40; live excl. VAT AED 96.00; difference AED 1,046.40; basis `non-VAT`; codes `OS/SR-SRVC`.
- CPR-026422: workbook AED 247,993.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026339: workbook AED 37.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026475: workbook AED 1,645.02; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026478: workbook AED 525.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026504: workbook AED 150.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026505: workbook AED 193.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026536: workbook AED 60.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026583: workbook AED 251,749.98; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026589: workbook AED 18.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026634: workbook AED 35.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026649: workbook AED 56.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026747: workbook AED 340.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026566: workbook AED 904.05; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026814: workbook AED 10.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001365: workbook AED 3,135.50; adjusted excl. VAT unavailable; live excl. VAT AED 3,135.50; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- CPR-026886: workbook AED 10.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026887: workbook AED 4.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026892: workbook AED 2.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-026920: workbook AED 92.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027044: workbook AED 37.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027049: workbook AED 11.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027051: workbook AED 350.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027123: workbook AED 3.65; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001394: workbook AED 476.00; adjusted excl. VAT AED 476.00; live excl. VAT AED 40.00; difference AED 436.00; basis `non-VAT`; codes `OS/SR-SRVC`.
- CPR-027186: workbook AED 3,900.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027206: workbook AED 11.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027231: workbook AED 17.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027235: workbook AED 49.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027251: workbook AED 500.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027189: workbook AED 185.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027284: workbook AED 98.72; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027333: workbook AED 4.76; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027387: workbook AED 12.40; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027686: workbook AED 265.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027687: workbook AED 450.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027838: workbook AED 4,677.00; adjusted excl. VAT AED 4,454.29; live excl. VAT AED 4,433.00; difference AED 21.29; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-027853: workbook AED 150.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-027899: workbook AED 1,388.10; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028012: workbook AED 142.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028016: workbook AED 72.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028021: workbook AED 60.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028053: workbook AED 247.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028058: workbook AED 411.60; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028060: workbook AED 840.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001427: workbook AED 1,774.00; adjusted excl. VAT unavailable; live excl. VAT AED 1,774.00; difference unavailable; basis `unknown`; codes `(blank)/SR-SRVC`.
- CPR-028122: workbook AED 90.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028157: workbook AED 400.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028162: workbook AED 11.40; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028165: workbook AED 60.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028177: workbook AED 1.17; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028228: workbook AED 5.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028341: workbook AED 22.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028345: workbook AED 3,262.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028386: workbook AED 8,874.73; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028050: workbook AED 220.17; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028400: workbook AED 43.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028464: workbook AED 43.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028469: workbook AED 137.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028503: workbook AED 3,395.95; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028512: workbook AED 2,163.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028513: workbook AED 187.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028514: workbook AED 130.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028564: workbook AED 294.25; adjusted excl. VAT AED 280.24; live excl. VAT AED 245.00; difference AED 35.24; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-028608: workbook AED 27.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028626: workbook AED 3.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028664: workbook AED 64.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028736: workbook AED 35.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028777: workbook AED 102.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028841: workbook AED 252.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028842: workbook AED 185.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028934: workbook AED 585.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028905: workbook AED 195.78; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028953: workbook AED 141.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028805: workbook AED 9.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-028728: workbook AED 2,123.10; adjusted excl. VAT AED 2,022.00; live excl. VAT AED 2,007.00; difference AED 15.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-029043: workbook AED 141.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001514: workbook AED 1,129.75; adjusted excl. VAT AED 1,075.95; live excl. VAT AED 1,075.00; difference AED 0.95; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-029204: workbook AED 91.25; adjusted excl. VAT AED 86.90; live excl. VAT AED 85.00; difference AED 1.90; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-029217: workbook AED 157.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029300: workbook AED 0.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029234: workbook AED 105.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029365: workbook AED 102.44; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029373: workbook AED 86.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029392: workbook AED 772.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001525: workbook AED 4,268.00; adjusted excl. VAT unavailable; live excl. VAT AED 4,268.00; difference unavailable; basis `unknown`; codes `(blank)/SR-SRVC`.
- PR-001527: workbook AED 599.50; adjusted excl. VAT AED 570.95; live excl. VAT AED 570.00; difference AED 0.95; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-029295: workbook AED 33.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029486: workbook AED 9.80; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029491: workbook AED 260.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029584: workbook AED 58.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029586: workbook AED 256.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029590: workbook AED 253.80; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029645: workbook AED 6,290.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029711: workbook AED 410.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029719: workbook AED 1,846.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029723: workbook AED 10,446.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029724: workbook AED 7,320.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029727: workbook AED 2,880.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029728: workbook AED 4,750.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029731: workbook AED 1,647.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029732: workbook AED 6,008.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029733: workbook AED 3,615.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029734: workbook AED 3,700.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029737: workbook AED 9,960.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029739: workbook AED 10,348.73; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029744: workbook AED 11.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029752: workbook AED 157.53; adjusted excl. VAT AED 150.03; live excl. VAT AED 150.00; difference AED 0.03; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- PR-001541: workbook AED 30.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029779: workbook AED 447.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001545: workbook AED 1,100.00; adjusted excl. VAT unavailable; live excl. VAT AED 1,100.00; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- CPR-029841: workbook AED 575.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-029962: workbook AED 97.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030012: workbook AED 308.65; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030016: workbook AED 4,739.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030095: workbook AED 555.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030106: workbook AED 15.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030153: workbook AED 93.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001558: workbook AED 15,800.00; adjusted excl. VAT AED 15,047.62; live excl. VAT AED 15,000.00; difference AED 47.62; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-030162: workbook AED 28.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030184: workbook AED 7.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030191: workbook AED 18.90; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030247: workbook AED 78.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030171: workbook AED 15.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030340: workbook AED 128.00; adjusted excl. VAT AED 121.90; live excl. VAT AED 110.00; difference AED 11.90; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-030082: workbook AED 66.09; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030553: workbook AED 497.75; adjusted excl. VAT AED 474.05; live excl. VAT AED 470.00; difference AED 4.05; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-030548: workbook AED 254.21; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030596: workbook AED 381.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030662: workbook AED 7,675.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030663: workbook AED 74.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030690: workbook AED 13,599.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030698: workbook AED 10.93; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030724: workbook AED 0.05; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030732: workbook AED 52.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030801: workbook AED 9.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030810: workbook AED 1,624.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030811: workbook AED 1,624.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030819: workbook AED 520.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-030552: workbook AED 6,783.03; adjusted excl. VAT AED 6,460.03; live excl. VAT AED 6,456.45; difference AED 3.58; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-031057: workbook AED 838.13; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031049: workbook AED 85.95; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031085: workbook AED 160.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031143: workbook AED 14,464.70; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031203: workbook AED 12.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031164: workbook AED 15.30; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031321: workbook AED 832.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031377: workbook AED 10.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031393: workbook AED 430.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031404: workbook AED 4.85; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031383: workbook AED 12.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031497: workbook AED 4,190.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031503: workbook AED 1,425.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031499: workbook AED 15,250.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031446: workbook AED 54.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031622: workbook AED 5.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031640: workbook AED 86.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031266: workbook AED 75.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031722: workbook AED 165.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031667: workbook AED 86.55; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031723: workbook AED 26.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031734: workbook AED 22.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031752: workbook AED 375.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031753: workbook AED 45.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031818: workbook AED 25.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031825: workbook AED 41.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031969: workbook AED 583.33; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-031995: workbook AED 2.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-032008: workbook AED 17.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-032099: workbook AED 30.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-032013: workbook AED 72.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-032162: workbook AED 20.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-032170: workbook AED 0.10; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001621: workbook AED 261.80; adjusted excl. VAT AED 261.80; live excl. VAT AED 22.00; difference AED 239.80; basis `non-VAT`; codes `OS/SR-SRVC`.
- PR-001622: workbook AED 261.80; adjusted excl. VAT AED 261.80; live excl. VAT AED 22.00; difference AED 239.80; basis `non-VAT`; codes `OS/SR-SRVC`.
- PR-001623: workbook AED 261.80; adjusted excl. VAT AED 261.80; live excl. VAT AED 22.00; difference AED 239.80; basis `non-VAT`; codes `OS/SR-SRVC`.
- CPR-032625: workbook AED 52.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-032643: workbook AED 142.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-032529: workbook AED 159.38; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-032635: workbook AED 47.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-032671: workbook AED 192.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-032668: workbook AED 11.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-032983: workbook AED 802.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-032658: workbook AED 1,464.10; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-033177: workbook AED 1,207.58; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-033212: workbook AED 430.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-033448: workbook AED 190.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-033474: workbook AED 1,377.60; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001680: workbook AED 3,570.00; adjusted excl. VAT AED 3,570.00; live excl. VAT AED 300.00; difference AED 3,270.00; basis `non-VAT`; codes `OS/SR-SRVC`.
- CPR-033583: workbook AED 3,675.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-033705: workbook AED 1,222.50; adjusted excl. VAT AED 1,164.29; live excl. VAT AED 1,150.00; difference AED 14.29; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- PR-001700: workbook AED 0.00; adjusted excl. VAT unavailable; live excl. VAT AED 803.67; difference unavailable; basis `mixed VAT basis`; codes `SR-RCVR/OS-GOOD, SR-RCVR/SR-SRVC`.
- PR-001701: workbook AED 0.00; adjusted excl. VAT unavailable; live excl. VAT AED 803.67; difference unavailable; basis `mixed VAT basis`; codes `SR-RCVR/OS-GOOD, SR-RCVR/SR-SRVC`.
- PR-001702: workbook AED 0.00; adjusted excl. VAT unavailable; live excl. VAT AED 803.67; difference unavailable; basis `mixed VAT basis`; codes `SR-RCVR/OS-GOOD, SR-RCVR/SR-SRVC`.
- CPR-033932: workbook AED 200.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001710: workbook AED 535.50; adjusted excl. VAT AED 535.50; live excl. VAT AED 45.00; difference AED 490.50; basis `non-VAT`; codes `OS/SR-SRVC`.
- CPR-034004: workbook AED 114.75; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-034080: workbook AED 80.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- PR-001723: workbook AED 178.50; adjusted excl. VAT AED 178.50; live excl. VAT AED 15.00; difference AED 163.50; basis `non-VAT`; codes `OS/SR-SRVC`.
- CPR-034421: workbook AED 8,218.35; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-034204: workbook AED 2,016.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-034432: workbook AED 2,457.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- CPR-034541: workbook AED 0.00; adjusted excl. VAT AED 0.00; live excl. VAT AED 10,400.00; difference AED -10,400.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- PR-001742: workbook AED 0.00; adjusted excl. VAT AED 0.00; live excl. VAT AED 869.00; difference AED -869.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-034663: workbook AED 0.00; adjusted excl. VAT AED 0.00; live excl. VAT AED 2,040.00; difference AED -2,040.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-034667: workbook AED 0.00; adjusted excl. VAT AED 0.00; live excl. VAT AED 9,125.00; difference AED -9,125.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-034902: workbook AED 0.00; adjusted excl. VAT AED 0.00; live excl. VAT AED 14,400.00; difference AED -14,400.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- CPR-034908: workbook AED 0.00; adjusted excl. VAT AED 0.00; live excl. VAT AED 5,650.00; difference AED -5,650.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.

## po.xlsx amount differences

- P0000000001: workbook AED 0.00; adjusted excl. VAT unavailable; live excl. VAT AED 409,885.00; difference unavailable; basis `unknown`; codes `OS/(blank), SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000008: workbook AED 2,800.00; adjusted excl. VAT AED 2,666.67; live excl. VAT AED 1,243,466.67; difference AED -1,240,800.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- P0000000002: workbook AED 52,500.00; adjusted excl. VAT AED 50,000.00; live excl. VAT AED 51,377.00; difference AED -1,377.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000003: workbook AED 148,719.15; adjusted excl. VAT AED 141,637.29; live excl. VAT AED 134,936.33; difference AED 6,700.96; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD`.
- P0000000011: workbook AED 578,272.80; adjusted excl. VAT AED 550,736.00; live excl. VAT AED 640,516.00; difference AED -89,780.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000016: workbook AED 1,518.30; adjusted excl. VAT AED 1,446.00; live excl. VAT AED 1,936,603.59; difference AED -1,935,157.59; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- P0000000006: workbook AED 945.00; adjusted excl. VAT AED 900.00; live excl. VAT AED 228,900.00; difference AED -228,000.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000010: workbook AED 13,072.50; adjusted excl. VAT AED 12,450.00; live excl. VAT AED 1,608,450.00; difference AED -1,596,000.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- P0000000009: workbook AED 207,900.00; adjusted excl. VAT AED 198,000.00; live excl. VAT AED 3,173,000.00; difference AED -2,975,000.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- P0000000020: workbook AED 210.00; adjusted excl. VAT AED 200.00; live excl. VAT AED 306,200.00; difference AED -306,000.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000021: workbook AED 577.50; adjusted excl. VAT AED 550.00; live excl. VAT AED 4,418.00; difference AED -3,868.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000012: workbook AED 0.00; adjusted excl. VAT AED 0.00; live excl. VAT AED 1,111,317.00; difference AED -1,111,317.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- P0000000013: workbook AED 2,247.00; adjusted excl. VAT AED 2,140.00; live excl. VAT AED 546,940.00; difference AED -544,800.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000017: workbook AED 325.50; adjusted excl. VAT AED 310.00; live excl. VAT AED 318,310.00; difference AED -318,000.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000018: workbook AED 7,626.15; adjusted excl. VAT AED 7,263.00; live excl. VAT AED 1,207,263.00; difference AED -1,200,000.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000019: workbook AED 3,282.30; adjusted excl. VAT AED 3,126.00; live excl. VAT AED 591,126.00; difference AED -588,000.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000022: workbook AED 3,859.38; adjusted excl. VAT AED 3,675.60; live excl. VAT AED 177,075.60; difference AED -173,400.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000024: workbook AED 4,406.33; adjusted excl. VAT AED 4,196.50; live excl. VAT AED 249,746.50; difference AED -245,550.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000026: workbook AED 3,864.00; adjusted excl. VAT AED 3,680.00; live excl. VAT AED 31,233.00; difference AED -27,553.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000031: workbook AED 498.33; adjusted excl. VAT AED 474.60; live excl. VAT AED 99,963.60; difference AED -99,489.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000035: workbook AED 1,470.00; adjusted excl. VAT AED 1,400.00; live excl. VAT AED 1,230.00; difference AED 170.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD`.
- P0000000036: workbook AED 824.25; adjusted excl. VAT AED 785.00; live excl. VAT AED 10,233.50; difference AED -9,448.50; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD`.
- P0000000042: workbook AED 4,620.00; adjusted excl. VAT AED 4,400.00; live excl. VAT AED 10,847.00; difference AED -6,447.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000046: workbook AED 762.30; adjusted excl. VAT AED 726.00; live excl. VAT AED 2,776.00; difference AED -2,050.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000051: workbook AED 1,953.00; adjusted excl. VAT AED 1,860.00; live excl. VAT AED 5,240.00; difference AED -3,380.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000052: workbook AED 63,787.50; adjusted excl. VAT AED 60,750.00; live excl. VAT AED 61,646.00; difference AED -896.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000057: workbook AED 42,105.00; adjusted excl. VAT AED 40,100.00; live excl. VAT AED 45,485.00; difference AED -5,385.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000058: workbook AED 5,775.00; adjusted excl. VAT AED 5,500.00; live excl. VAT AED 6,920.00; difference AED -1,420.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000066: workbook AED 254,203.32; adjusted excl. VAT AED 242,098.40; live excl. VAT AED 252,348.40; difference AED -10,250.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD`.
- P0000000072: workbook AED 2,835.00; adjusted excl. VAT AED 2,700.00; live excl. VAT AED 421,900.00; difference AED -419,200.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- P0000000077: workbook AED 172,373.04; adjusted excl. VAT AED 164,164.80; live excl. VAT AED 300.00; difference AED 163,864.80; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD`.
- P0000000134: workbook AED 22,036.00; adjusted excl. VAT unavailable; live excl. VAT AED 22,036.00; difference unavailable; basis `unknown`; codes `(blank)/(blank)`.
- P0000000203: workbook AED 1,092.00; adjusted excl. VAT AED 1,040.00; live excl. VAT AED 880.00; difference AED 160.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- P0000000212: workbook AED 114,688.00; adjusted excl. VAT unavailable; live excl. VAT AED 114,688.00; difference unavailable; basis `unknown`; codes `(blank)/(blank)`.
- P0000000213: workbook AED 36,723.00; adjusted excl. VAT unavailable; live excl. VAT AED 36,723.00; difference unavailable; basis `unknown`; codes `(blank)/(blank)`.
- P0000000230: workbook AED 2,436.00; adjusted excl. VAT AED 2,320.00; live excl. VAT AED 1,920.00; difference AED 400.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-SRVC`.
- P0000000232: workbook AED 4,000.00; adjusted excl. VAT unavailable; live excl. VAT AED 4,000.00; difference unavailable; basis `unknown`; codes `(blank)/(blank)`.
- P0000000461: workbook AED 57,225.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- P0000000532: workbook AED 525.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- P0000000585: workbook AED 1,844.10; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- P0000000654: workbook AED 21,043.05; adjusted excl. VAT AED 20,041.00; live excl. VAT AED 13,801.00; difference AED 6,240.00; basis `standard-rate VAT`; codes `SR-RCVR/SR-GOOD`.
- P0000000737: workbook AED 11,000.00; adjusted excl. VAT unavailable; live excl. VAT AED 11,000.00; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank)`.
- P0000000886: workbook AED 112,877.90; adjusted excl. VAT unavailable; live excl. VAT AED 112,877.90; difference unavailable; basis `unknown`; codes `(blank)/(blank)`.
- P0000000993: workbook AED 16,936.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- P0000001287: workbook AED 876.80; adjusted excl. VAT unavailable; live excl. VAT AED 836.00; difference unavailable; basis `mixed VAT basis`; codes `SR-RCVR/OS-GOOD, SR-RCVR/SR-GOOD`.
- P0000001436: workbook AED 10,948.95; adjusted excl. VAT unavailable; live excl. VAT AED 10,499.00; difference unavailable; basis `unknown`; codes `(blank)/SR-GOOD, SR-RCVR/SR-GOOD`.
- P0000001526: workbook AED 20,800.96; adjusted excl. VAT unavailable; live excl. VAT AED 19,813.77; difference unavailable; basis `unknown`; codes `SR-RCVR/(blank), SR-RCVR/SR-GOOD, SR-RCVR/SR-SRVC`.
- SCBM-PO2600306: workbook AED 1,425.00; adjusted excl. VAT unavailable; live excl. VAT AED 1,425.00; difference unavailable; basis `unknown`; codes `(blank)/(blank)`.
- SCBM-PO2600614: workbook AED 1,995.00; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- SCBM-PO2600615: workbook AED 1,790.25; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- SCBM-PO2600796: workbook AED 157.50; adjusted excl. VAT unavailable; live excl. VAT AED 0.00; difference unavailable; basis `zero amount`; codes `no material live lines`.
- SCBM-PO2600813: workbook AED 7,500.00; adjusted excl. VAT unavailable; live excl. VAT AED 7,500.00; difference unavailable; basis `unknown`; codes `(blank)/SR-SRVC`.
- SCBM-PO2601134: workbook AED 1,712.00; adjusted excl. VAT unavailable; live excl. VAT AED 1,712.00; difference unavailable; basis `unknown`; codes `(blank)/SR-SRVC`.
- SCBM-PO2601421: workbook AED 2,875.00; adjusted excl. VAT unavailable; live excl. VAT AED 2,750.00; difference unavailable; basis `unknown`; codes `(blank)/SR-SRVC, SR-RCVR/SR-SRVC`.

## Decisions applied

- `PurchReqReviewTask` maps to `Sourcing`; the separate `PR in review` bucket is removed from the corrected comparison.
- Amounts use live F&O line values excluding VAT. No amount is grossed up.
- PO event stages are `Sent to supplier`, `Receipt posted` and `Invoiced`; a packing slip is a posting event, not a delivery date.
- Approved dropped columns are not treated as retirement blockers. They remain untouched because the cutover stopped before code removal.

## Workflow trigger proof

- `.github/workflows/main_pr-po-dashboard-proxy.yml` in `pr-po-proxy` is manual-only and contains no deployment action.
- `.github/workflows/deploy-ssg-prpo-proxy.yml` is manual-only, requires an exact tested SHA and targets only `ssg-prpo-proxy`.
- Required secret: `AZURE_FUNCTIONAPP_PUBLISH_PROFILE_SSG_PRPO_PROXY`, containing only the authorised app's publish profile.

## What I found

- Merging `PR in review` into `Sourcing` improves PR stage agreement, but current line pricing and zero-active-line cases still disagree with 59 workbook rows.
- The PO workbook is substantially behind live lifecycle events. Old approval labels now coexist with sent, received or invoiced live orders.
- PR amount mismatch is dominated by 717 workbook-valued documents whose current live active-line amount is zero; tax adjustment cannot repair a missing/current-line basis difference.

## Problems and risks

- Deploying now would knowingly replace the workbook with a stage model below both 95% stage gates and a PR amount model below the 95% amount gate.
- The PO sent timestamp is not exposed. Receipt posting and approval assignment have truthful clocks; the old LPO-sent time has no like-for-like live clock.
- The live sources continue moving. All figures above belong to the recorded UTC evidence position.

## Files changed

- Reconciliation logic, correction evidence/report, `NOTES.md` and the unpublished change note in the dashboard repository.
- Deployment workflows and safety documentation in `pr-po-proxy`.

## What I did not change

- No dashboard, Race Control, email, snapshot or proxy runtime path was cut over.
- No workbook, generator, fallback, recipient, sender or quiet-mode setting was removed or changed.
- No Dataverse or Azure resource was written. Neither function app was deployed.
- Dashboard `main` was not updated because its legacy Pages source auto-publishes every main commit.

## Testing performed

- Python compile and JSON gate assertions.
- Complete read-only reconciliation against both Dataverse organisations and both unchanged workbooks.
- Existing dashboard JavaScript and weekly snapshot regression tests.
- Dependency-free trigger/target assertions and manual YAML structure review for both proxy workflows.
- Change-note visual check at desktop and 412 x 915 phone viewports.

## Commands recorded

- `python tests/reconcile_workbook_retirement.py --out evidence/workbook-retirement-correction-01.json` with short-lived Azure CLI tokens supplied only to the child process.
- `python tests/render_retirement_correction.py evidence/workbook-retirement-correction-01.json evidence/workbook-retirement-reconciliation.json evidence/workbook-retirement-correction-01.md --notes NOTES.md`.
- `node --test tests/dataverse-live.test.js tests/race-control.test.js`.
- `python tests/test_weekly_snapshot.py`.
- PowerShell trigger/target assertions for both proxy workflows; no YAML parser was installed.

## Publication evidence

- The proxy protection is merged and pushed on `pr-po-proxy` `main` at `3b930f44289f051f04df442331549ff057f9cfa2`.
- GitHub reported no Actions run for that main head; neither the legacy nor authorised function app was deployed.
- The dashboard correction is pushed only to `audit/workbook-retirement-verdict`; Pages still publishes `main` at `a6adb0575c02ab903ccc2030c68698dc538e6338`.

## Remaining risks

- The failed document populations need a source-level correction or a newly approved reconciliation rule before another cutover attempt.
- Production remains workbook-dependent and therefore still depends on the morning email chain.

## Recommended next step

Investigate the 717 PR amount cases with no current active-line value and the 87 PO approval-to-event differences. Rerun the same gates after the sources or approved population rules change. Do not deploy or remove workbooks before all mandatory gates pass.

# Workbook retirement correction 02 — 7 September 2026

## Verdict

**Cannot retire.** Measuring the documents the dashboard displays fixes the PR stage and both amount gates, but the PO stage gate remains below 95%. The safe-cutover stop applies before deployment or workbook removal.

| Gate | 7 Sep verdict | Correction 01 | Correction 02: all rows / dashboard population | Result |
|---|---:|---:|---:|---|
| PR stage | 489/571 (85.64%) | 512/571 (89.67%) | 521/571 (91.24%) / 521/547 (95.25%) | PASS; threshold 95% |
| PR procurement clock within one day | 541/564 (95.92%) | 540/564 (95.74%) | 496/509 (97.45%) / 496/509 (97.45%) | PASS; threshold 90% |
| PO stage | 430/1,493 (28.80%) | 653/1,495 (43.68%) | 320/1,495 (21.40%) / 309/702 (44.02%) | FAIL; threshold 95% |
| PR amount | 819/4,394 (18.64%) | 3,560/4,394 (81.02%) | 3,596/4,394 (81.84%) / 556/566 (98.23%) | PASS; threshold 95% |
| PO amount | 85/2,977 (2.86%) | 2,923/2,977 (98.19%) | 2,932/2,977 (98.49%) / 707/714 (99.02%) | PASS; threshold 95% |
| Distinct documents | Exact | Exact | Exact / Exact | PASS |

The two Correction 02 figures show all workbook rows first and the dashboard population second. No excluded row is hidden; every excluded row appears in the stale lane below.

## Why the PO stage gate still fails

The dashboard population contains 702 comparable PO rows. 309 match and 393 do not. Of the differences, 359 have a later live stage whose event occurred before the export cutoff, and 34 have no exposed event timestamp. The exposed PO-confirmation entity returned 0 rows, so an approval-to-sent progression cannot be assumed.

## Measurement rules applied

- Workbook export cutoff: `2026-09-07T05:30:00Z` (user-supplied approximately 09:30 Asia/Dubai on 7 September 2026).
- PR population: live status `In review` or `Approved`, with a mapped workbook step, matching the production live-pipeline predicate.
- PO population: mapped rows excluding invoiced/closed/cancelled POs and rejected approvals, matching the production live-pipeline predicate.
- A later stage matches only when its authoritative live timestamp is after the export cutoff. It is tagged `PROGRESSED_AFTER_EXPORT`.
- Amount equality within AED 0.01 matches first. Standard, mixed or unknown tax basis also tests workbook divided by 1.05.

## Read-only source evidence

- Workbooks: 4,394 PR and 2,977 PO documents; neither file was modified.
- F&O: 4,413 PR headers, 20,711 PR lines, 3,188 PO headers and 14,977 PO lines.
- PO events: 3,868 packing slips, 0 exposed confirmations and 25,198 invoice-journal rows.
- Approval capture: 1,781 snapshots and 1,414 current work items.
- Dataset generated/F&O read: `2026-09-07T14:56:19.280956Z`; approval capture reconciled: `2026-09-07T14:54:37Z`; effective data time: `2026-09-07T14:54:37Z`.

## PROGRESSED_AFTER_EXPORT matches

Count: 20. Each row records the two timestamps used by R2.

- CPR-034541: Sourcing → Priced — awaiting approval; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T09:14:14Z`; source `PR header modified time after line pricing`; `PROGRESSED_AFTER_EXPORT`.
- CPR-034667: Sourcing → Priced — awaiting approval; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T12:41:53Z`; source `PR header modified time after line pricing`; `PROGRESSED_AFTER_EXPORT`.
- CPR-034902: Sourcing → Priced — awaiting approval; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T11:54:49Z`; source `PR header modified time after line pricing`; `PROGRESSED_AFTER_EXPORT`.
- CPR-034908: Sourcing → Priced — awaiting approval; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T11:47:44Z`; source `PR header modified time after line pricing`; `PROGRESSED_AFTER_EXPORT`.
- PR-001700: Sourcing → Priced — awaiting approval; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T11:02:55Z`; source `PR header modified time after line pricing`; `PROGRESSED_AFTER_EXPORT`.
- PR-001701: Sourcing → Priced — awaiting approval; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T11:03:55Z`; source `PR header modified time after line pricing`; `PROGRESSED_AFTER_EXPORT`.
- PR-001702: Sourcing → Priced — awaiting approval; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T11:04:49Z`; source `PR header modified time after line pricing`; `PROGRESSED_AFTER_EXPORT`.
- PR-001725: Sourcing → Priced — awaiting approval; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T12:34:56Z`; source `PR header modified time after line pricing`; `PROGRESSED_AFTER_EXPORT`.
- PR-001742: Sourcing → Priced — awaiting approval; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T13:50:11Z`; source `PR header modified time after line pricing`; `PROGRESSED_AFTER_EXPORT`.
- SCBM-PO2601103: Procurement → Invoiced; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T10:24:54Z`; source `vendor-invoice posting`; `PROGRESSED_AFTER_EXPORT`.
- SCBM-PO2601420: Sent to supplier → Invoiced; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T10:24:58Z`; source `vendor-invoice posting`; `PROGRESSED_AFTER_EXPORT`.
- SCBM-PO2601452: Sent to supplier → Invoiced; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T10:22:14Z`; source `vendor-invoice posting`; `PROGRESSED_AFTER_EXPORT`.
- SCBM-PO2601487: Sent to supplier → Invoiced; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T10:22:05Z`; source `vendor-invoice posting`; `PROGRESSED_AFTER_EXPORT`.
- SCBM-PO2601494: Sent to supplier → Invoiced; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T10:20:51Z`; source `vendor-invoice posting`; `PROGRESSED_AFTER_EXPORT`.
- SCBM-PO2601500: Sent to supplier → Invoiced; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T10:21:56Z`; source `vendor-invoice posting`; `PROGRESSED_AFTER_EXPORT`.
- SCBM-PO2601512: Sent to supplier → Invoiced; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T10:24:50Z`; source `vendor-invoice posting`; `PROGRESSED_AFTER_EXPORT`.
- SCBM-PO2601530: Sent to supplier → Invoiced; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T10:20:04Z`; source `vendor-invoice posting`; `PROGRESSED_AFTER_EXPORT`.
- SCBM-PO2601531: Sent to supplier → Invoiced; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T10:19:55Z`; source `vendor-invoice posting`; `PROGRESSED_AFTER_EXPORT`.
- SCBM-PO2601532: Procurement → Invoiced; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T10:23:49Z`; source `vendor-invoice posting`; `PROGRESSED_AFTER_EXPORT`.
- SCBM-PO2601536: Sent to supplier → Invoiced; workbook export `2026-09-07T05:30:00Z`; live evidence `2026-09-07T10:21:50Z`; source `vendor-invoice posting`; `PROGRESSED_AFTER_EXPORT`.

## PR stage differences in dashboard population

- CPR-022436: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- CPR-026592: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- CPR-027046: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- CPR-028312: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- CPR-028662: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- CPR-029477: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- PR-001545: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- CPR-030558: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- CPR-030786: Priced — awaiting approval → Sourcing; `REGRESSION_OR_UNMAPPED`; flags `ZERO_PRICE_LINES`.
- CPR-032057: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- CPR-032136: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- CPR-032260: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- CPR-033076: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- PR-001654: Dep Managers → Sourcing; `REGRESSION_OR_UNMAPPED`; flags `ZERO_PRICE_LINES`.
- CPR-033128: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- CPR-033260: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- PR-001682: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- PR-001684: Finance → Priced — awaiting approval; `REGRESSION_OR_UNMAPPED`.
- PR-001694: Dep Managers → Priced — awaiting approval; `REGRESSION_OR_UNMAPPED`.
- CPR-033658: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- CPR-033852: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- CPR-034069: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- CPR-034165: Priced — awaiting approval → Sourcing; `REGRESSION_OR_UNMAPPED`; flags `ZERO_PRICE_LINES`.
- PR-001743: Dep Managers → Priced — awaiting approval; `REGRESSION_OR_UNMAPPED`.
- CPR-034582: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.
- CPR-034663: Sourcing → Priced — awaiting approval; `PROGRESSION_NOT_AFTER_EXPORT`.

## PO stage differences in dashboard population

- P0000000008: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000011: CEO → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000016: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000032: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000048: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000049: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000052: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000062: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000123: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000127: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000128: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000129: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000130: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000137: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000138: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000142: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000147: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000150: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000151: Finance → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000159: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000160: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000146: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000161: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000169: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000172: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000176: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000178: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000179: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000180: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000187: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000188: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000191: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000202: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000203: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000209: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000212: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000210: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000213: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000217: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000229: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000214: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000241: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000340: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000325: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000345: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000347: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000348: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000349: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000350: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000351: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000366: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000370: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000359: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000373: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000376: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000419: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000422: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000467: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000479: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000483: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000488: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000524: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000582: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000606: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000654: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000680: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000710: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000693: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000737: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000764: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000767: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000770: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000793: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000794: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000795: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000817: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000869: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000875: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000886: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000892: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000889: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000905: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000925: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000930: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000962: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000969: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000988: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000000994: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001003: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001017: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001036: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001042: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001052: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001105: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001118: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001130: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001147: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001156: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001168: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001179: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001193: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001196: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001200: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001201: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001202: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001225: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001256: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001257: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001259: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001292: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001301: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001321: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001337: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001416: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001422: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001437: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001438: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001439: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001443: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001455: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001464: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001497: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001499: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001500: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001517: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- P0000001567: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600021: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600024: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600038: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600054: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600055: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600056: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600057: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600072: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600073: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600074: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600075: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600076: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600077: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600078: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600079: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600080: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600084: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600085: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600087: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600089: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600090: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600091: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600092: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600108: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600135: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600136: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600138: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600139: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600142: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600154: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600170: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600176: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600177: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600178: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600180: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600181: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600195: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600198: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600218: Procurement → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600220: Sent to supplier → Receipt posted; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2600226: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600250: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600252: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600253: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600259: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600261: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600268: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600272: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600281: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600286: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600304: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600307: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600317: Procurement → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600327: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600337: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600354: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600358: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600374: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600378: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600382: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600387: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600388: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600389: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600392: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600399: Finance → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2600408: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600409: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600433: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600452: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600454: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600479: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600486: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600500: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600502: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600507: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600510: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600511: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600513: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600514: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600515: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600516: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600522: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600534: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600540: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600542: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600544: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600568: Finance → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600580: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600583: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600586: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600590: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600595: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600609: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600610: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600622: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600624: Finance → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2600625: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600626: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600629: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600632: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600633: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600643: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600644: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600665: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600671: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600684: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600687: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600712: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600724: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600726: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600728: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600739: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600740: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600743: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600748: Procurement → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600750: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600755: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600767: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600768: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600770: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600771: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600772: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600773: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600780: Finance → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600782: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600784: Finance → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600785: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600806: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600807: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600811: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600816: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600818: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600829: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600835: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600837: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600840: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600851: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600858: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600861: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600870: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600874: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600889: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600891: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600893: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600902: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2600912: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600913: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600923: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600929: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600949: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600950: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600952: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600958: Procurement → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600964: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600965: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600966: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600967: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600968: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2600969: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601006: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601009: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601011: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601014: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601044: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601072: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601083: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601090: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601092: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601093: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601100: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601102: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601104: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601105: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601113: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601135: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601137: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601151: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601158: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601159: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601176: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601180: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601182: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601212: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601231: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601243: Finance → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601247: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601267: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601273: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601275: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601278: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601281: Procurement → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601288: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601292: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601293: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601313: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601314: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601315: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601316: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601318: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601331: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601332: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601344: Finance → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601356: Finance → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601357: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601368: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601374: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601379: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601381: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601383: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601391: Finance → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601397: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601398: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601401: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601402: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601404: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601406: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601414: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601421: Finance → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601423: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601424: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601425: Procurement → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601431: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601432: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601434: Finance → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601441: Procurement → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601450: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601451: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601458: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601459: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601463: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601468: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601471: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601472: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601475: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601478: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601481: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601484: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601492: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601499: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601502: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601503: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601507: Procurement → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601509: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601515: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601524: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601526: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601527: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601534: Finance → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601535: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601546: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601551: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601557: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601558: Procurement → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601561: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601562: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601572: Sent to supplier → Receipt posted; `PROGRESSION_NOT_AFTER_EXPORT`.
- SCBM-PO2601581: Finance → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601586: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601589: Finance → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601590: Finance → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601591: Finance → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601592: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601593: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601594: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601595: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601596: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- SCBM-PO2601597: Procurement → Sent to supplier; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.

## PR procurement clock differences over one day

- CPR-034162: Sourcing; workbook `2026-08-31T17:33:35Z`; live seed `2026-09-04T04:56:36Z`.
- PR-001726: Sourcing; workbook `2026-08-31T17:03:57Z`; live seed `2026-09-04T04:57:00Z`.
- CPR-034154: Priced — awaiting approval; workbook `2026-08-27T16:40:14Z`; live seed `2026-09-04T04:56:07Z`.
- CPR-034527: Sourcing; workbook `2026-09-03T15:22:31Z`; live seed `2026-09-07T05:36:43Z`.
- PR-001747: Sourcing; workbook `2026-09-02T13:36:52Z`; live seed `2026-09-07T12:22:47Z`.
- CPR-034805: Sourcing; workbook `2026-09-04T11:41:51Z`; live seed `2026-09-07T08:14:46Z`.
- CPR-034616: Sourcing; workbook `2026-09-04T11:47:01Z`; live seed `2026-09-07T07:29:24Z`.
- CPR-034832: Sourcing; workbook `2026-09-04T13:41:53Z`; live seed `2026-09-07T11:43:56Z`.
- CPR-034878: Sourcing; workbook `2026-09-05T14:42:01Z`; live seed `2026-09-07T05:35:57Z`.
- CPR-034911: Sourcing; workbook `2026-09-05T14:42:00Z`; live seed `2026-09-07T13:56:32Z`.
- CPR-034808: Sourcing; workbook `2026-09-05T14:41:59Z`; live seed `2026-09-07T13:56:16Z`.
- CPR-034914: Sourcing; workbook `2026-09-05T14:41:58Z`; live seed `2026-09-07T08:24:28Z`.
- CPR-034920: Sourcing; workbook `2026-09-05T15:41:51Z`; live seed `2026-09-07T07:34:00Z`.

## PO clock evidence

- Like-for-like approval clocks: 2/3 (66.67%) within one day.
- Receipt-posted clocks: 360/360 current receipt rows have a packing-slip `Posted on` date.
- Workbook `LPO sent` clocks remain non-comparable with receipt posting and are not a gate.

- SCBM-PO2601579: Finance; workbook `2026-09-04T09:44:26Z`; capture `2026-09-07T13:12:22Z`.

## pr.xlsx amount differences in dashboard population

Agreement: 556/566 (98.23%). Match rules: AMOUNT_DIFFERENCE 10, EXACT_EQUALITY 167, VAT_ADJUSTED 389.

- CPR-030552: workbook AED 6,783.03; compared ex-VAT AED 6,460.03; live ex-VAT AED 6,456.45; difference AED 3.58; basis `standard-rate VAT`; `AMOUNT_DIFFERENCE`.
- PR-001700: workbook AED 0.00; compared ex-VAT AED 0.00; live ex-VAT AED 803.67; difference AED -803.67; basis `mixed VAT basis`; `AMOUNT_DIFFERENCE`.
- PR-001701: workbook AED 0.00; compared ex-VAT AED 0.00; live ex-VAT AED 803.67; difference AED -803.67; basis `mixed VAT basis`; `AMOUNT_DIFFERENCE`.
- PR-001702: workbook AED 0.00; compared ex-VAT AED 0.00; live ex-VAT AED 803.67; difference AED -803.67; basis `mixed VAT basis`; `AMOUNT_DIFFERENCE`.
- CPR-034541: workbook AED 0.00; compared ex-VAT AED 0.00; live ex-VAT AED 10,400.00; difference AED -10,400.00; basis `standard-rate VAT`; `AMOUNT_DIFFERENCE`.
- PR-001742: workbook AED 0.00; compared ex-VAT AED 0.00; live ex-VAT AED 869.00; difference AED -869.00; basis `standard-rate VAT`; `AMOUNT_DIFFERENCE`.
- CPR-034663: workbook AED 0.00; compared ex-VAT AED 0.00; live ex-VAT AED 2,040.00; difference AED -2,040.00; basis `standard-rate VAT`; `AMOUNT_DIFFERENCE`.
- CPR-034667: workbook AED 0.00; compared ex-VAT AED 0.00; live ex-VAT AED 9,125.00; difference AED -9,125.00; basis `standard-rate VAT`; `AMOUNT_DIFFERENCE`.
- CPR-034902: workbook AED 0.00; compared ex-VAT AED 0.00; live ex-VAT AED 14,400.00; difference AED -14,400.00; basis `standard-rate VAT`; `AMOUNT_DIFFERENCE`.
- CPR-034908: workbook AED 0.00; compared ex-VAT AED 0.00; live ex-VAT AED 5,650.00; difference AED -5,650.00; basis `standard-rate VAT`; `AMOUNT_DIFFERENCE`.

## po.xlsx amount differences in dashboard population

Agreement: 707/714 (99.02%). Match rules: AMOUNT_DIFFERENCE 7, EXACT_EQUALITY 25, VAT_ADJUSTED 682.

- P0000000008: workbook AED 2,800.00; compared ex-VAT AED 2,666.67; live ex-VAT AED 1,243,466.67; difference AED -1,240,800.00; basis `standard-rate VAT`; `AMOUNT_DIFFERENCE`.
- P0000000011: workbook AED 578,272.80; compared ex-VAT AED 550,736.00; live ex-VAT AED 640,516.00; difference AED -89,780.00; basis `standard-rate VAT`; `AMOUNT_DIFFERENCE`.
- P0000000016: workbook AED 1,518.30; compared ex-VAT AED 1,446.00; live ex-VAT AED 1,936,603.59; difference AED -1,935,157.59; basis `standard-rate VAT`; `AMOUNT_DIFFERENCE`.
- P0000000052: workbook AED 63,787.50; compared ex-VAT AED 60,750.00; live ex-VAT AED 61,646.00; difference AED -896.00; basis `standard-rate VAT`; `AMOUNT_DIFFERENCE`.
- P0000000203: workbook AED 1,092.00; compared ex-VAT AED 1,040.00; live ex-VAT AED 880.00; difference AED 160.00; basis `standard-rate VAT`; `AMOUNT_DIFFERENCE`.
- P0000000654: workbook AED 21,043.05; compared ex-VAT AED 20,041.00; live ex-VAT AED 13,801.00; difference AED 6,240.00; basis `standard-rate VAT`; `AMOUNT_DIFFERENCE`.
- SCBM-PO2601421: workbook AED 2,875.00; compared ex-VAT AED 2,738.10; live ex-VAT AED 2,750.00; difference AED -11.90; basis `unknown`; `AMOUNT_DIFFERENCE`.

## Stale rows the workbook still carries

Count: 2,944 (2,115 PR; 829 PO). These rows retain a workbook step but are outside the production dashboard's live-pipeline population. They do not enter a gate.

- PO P0000000002: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000000004: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000000005: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000000007: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000000124: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000000484: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000000694: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000000813: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000000878: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001110: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001227: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001246: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001248: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001249: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001250: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001254: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001255: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001258: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001260: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001261: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001262: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001263: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001267: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001268: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001273: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001275: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001277: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001283: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001285: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001287: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001288: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001289: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001290: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001291: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001293: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001294: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001295: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001297: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001298: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001299: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001300: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001302: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001303: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001304: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001305: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001306: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001307: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001308: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001312: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001324: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO P0000001489: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600088: workbook step `Accounting Manager`; live status `Open order`; approval `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600115: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600137: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600163: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600171: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600172: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600174: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600175: workbook step `Accounting Manager`; live status `Open order`; approval `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600179: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600192: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600207: workbook step `Finance and Accounts Director`; live status `Open order`; approval `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600208: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600270: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600284: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600305: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600306: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600309: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600332: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600333: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600343: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600398: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600402: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600418: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600419: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600420: workbook step `Accounting Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600422: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600423: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600424: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600425: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600427: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600428: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600430: workbook step `Accounting Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600431: workbook step `Accounting Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600434: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600436: workbook step `Accounting Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600437: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600438: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600439: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600440: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600441: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600442: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600443: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600444: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600445: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600447: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600448: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600449: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600450: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600451: workbook step `Accounting Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600453: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600455: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600456: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600457: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600458: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600459: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600460: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600461: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600462: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600463: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600464: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600465: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600466: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600467: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600468: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600469: workbook step `Accounting Manager`; live status `Open order`; approval `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600470: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600471: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600472: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600473: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600474: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600476: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600477: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600478: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600481: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600482: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600487: workbook step `Accounting Manager`; live status `Open order`; approval `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600489: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600490: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600491: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600492: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600493: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600494: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600495: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600496: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600497: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600498: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600499: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600501: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600503: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600504: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600505: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600506: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600508: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600509: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600512: workbook step `Accounting Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600517: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600518: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600519: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600520: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600521: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600524: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600525: workbook step `Accounting Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600527: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600528: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600529: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600530: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600531: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600532: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600533: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600535: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600537: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600539: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600541: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600545: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600546: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600547: workbook step `Advance payment request submitted (if applicable)`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600548: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600549: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600550: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600551: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600552: workbook step `Accounting Manager`; live status `Open order`; approval `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600553: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600554: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600555: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600556: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600557: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600559: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600562: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600563: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600564: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600565: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600566: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600567: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600570: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600571: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600572: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600573: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600574: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600575: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600576: workbook step `Accounting Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600577: workbook step `Procurement Manager`; live status `Open order`; approval `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600578: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600579: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600581: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600582: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600584: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600585: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600587: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600588: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600589: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600591: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600592: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600593: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600594: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600596: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600597: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600598: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600599: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600600: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600601: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600602: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600605: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600606: workbook step `Procurement Manager`; live status `Open order`; approval `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600607: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600608: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600611: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600612: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600613: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600614: workbook step `Accounting Manager`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600615: workbook step `Accounting Manager`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600616: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600617: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600618: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600619: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600620: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600621: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600623: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600627: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600628: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600630: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600631: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600634: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600636: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600637: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600639: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600640: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600641: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600642: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600646: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600647: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600648: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600649: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600650: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600652: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600654: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600656: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600657: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600659: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600660: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600661: workbook step `Advance payment request submitted (if applicable)`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600662: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600663: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600664: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600666: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600667: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600668: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600669: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600670: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600672: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600673: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600674: workbook step `Accounting Manager`; live status `Open order`; approval `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600675: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600676: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600677: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600678: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600679: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600680: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600681: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600682: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600683: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600685: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600686: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600688: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600689: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600691: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600692: workbook step `Accounting Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600693: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600695: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600696: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600697: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600698: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600699: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600700: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600701: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600702: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600703: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600704: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600705: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600707: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600709: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600710: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600711: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600715: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600716: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600717: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600718: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600719: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600720: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600721: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600722: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600723: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600725: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600727: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600729: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600730: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600733: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600734: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600735: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600741: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600742: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600745: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600746: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600747: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600749: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600751: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600752: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600756: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600757: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600758: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600759: workbook step `Accounting Manager`; live status `Open order`; approval `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600760: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600761: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600762: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600763: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600764: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600765: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600766: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600769: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600774: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600775: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600776: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600777: workbook step `Accounting Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600778: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600779: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600781: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600783: workbook step `Accounting Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600786: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600787: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600788: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600789: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600790: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600791: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600792: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600793: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600794: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600796: workbook step `Procurement Manager`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600797: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600798: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600799: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600800: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600801: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600802: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600803: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600804: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600805: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600808: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600809: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600810: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600812: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600814: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600815: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600817: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600820: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600821: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600822: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600823: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600824: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600825: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600826: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600828: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600830: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600831: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600832: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600833: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600834: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600836: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600838: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600839: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600841: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600842: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600843: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600844: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600848: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600849: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600852: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600853: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600854: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600855: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600856: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600857: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600859: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600860: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600862: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600863: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600864: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600865: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600866: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600867: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600868: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600869: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600871: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600872: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600873: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600875: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600876: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600877: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600878: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600881: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600882: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600883: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600884: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600887: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600888: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600890: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600892: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600894: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600896: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600898: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600899: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600900: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600901: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600905: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600906: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600907: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600908: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600909: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600910: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600911: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600914: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600915: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600916: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600917: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600918: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600920: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600921: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600924: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600925: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600926: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600927: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600928: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600930: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600931: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600932: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600933: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600934: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600935: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600936: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600937: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600938: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600939: workbook step `PurchTableApproval`; live status `Open order`; approval `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600940: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600941: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600942: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600943: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600944: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600945: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600946: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600947: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600951: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600953: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600955: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600956: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600959: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600960: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600962: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600963: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600970: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600971: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600972: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600973: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600974: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600975: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600977: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600978: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600981: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600982: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600983: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600984: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600987: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600988: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600989: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600990: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600991: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600992: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600993: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600994: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600996: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600997: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600998: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2600999: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601000: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601001: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601003: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601004: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601005: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601007: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601008: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601010: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601012: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601013: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601015: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601016: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601017: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601018: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601019: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601020: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601021: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601022: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601023: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601025: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601027: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601029: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601030: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601032: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601036: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601037: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601038: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601039: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601040: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601041: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601042: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601043: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601046: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601048: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601049: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601050: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601051: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601052: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601053: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601054: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601055: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601056: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601057: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601058: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601059: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601061: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601062: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601063: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601064: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601065: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601066: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601067: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601069: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601070: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601071: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601073: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601074: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601075: workbook step `Procurement Manager`; live status `Open order`; approval `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601077: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601078: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601079: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601080: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601081: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601082: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601084: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601085: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601086: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601087: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601088: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601089: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601091: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601094: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601095: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601096: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601098: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601099: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601101: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601103: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601106: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601107: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601108: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601109: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601110: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601112: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601114: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601117: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601118: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601119: workbook step `Finance and Accounts Director`; live status `Open order`; approval `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601124: workbook step `Advance payment request submitted (if applicable)`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601125: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601126: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601128: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601129: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601130: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601131: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601132: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601133: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601136: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601139: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601142: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601143: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601144: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601145: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601146: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601147: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601148: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601149: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601150: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601152: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601153: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601154: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601155: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601156: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601157: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601160: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601161: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601162: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601163: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601164: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601165: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601166: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601167: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601168: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601169: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601170: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601171: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601172: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601173: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601174: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601177: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601178: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601179: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601181: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601183: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601185: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601186: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601187: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601188: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601189: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601190: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601191: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601192: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601193: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601194: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601195: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601196: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601198: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601199: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601200: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601201: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601202: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601203: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601205: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601206: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601209: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601211: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601213: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601214: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601215: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601216: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601217: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601218: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601219: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601220: workbook step `Accounting Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601221: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601222: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601223: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601225: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601227: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601229: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601230: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601232: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601233: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601234: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601235: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601236: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601237: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601238: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601239: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601240: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601241: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601242: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601244: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601245: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601246: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601248: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601250: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601251: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601252: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601253: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601254: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601256: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601257: workbook step `Procurement Manager`; live status `Open order`; approval `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601258: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601259: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601260: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601261: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601262: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601263: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601264: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601266: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601270: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601271: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601272: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601274: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601276: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601277: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601279: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601280: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601282: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601283: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601284: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601285: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601286: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601287: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601289: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601290: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601291: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601294: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601295: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601296: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601298: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601299: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601300: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601301: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601302: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601303: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601304: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601305: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601306: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601307: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601308: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601309: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601310: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601312: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601317: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601320: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601321: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601322: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601323: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601324: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601326: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601327: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601328: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601329: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601330: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601333: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601334: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601335: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601336: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601337: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601338: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601339: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601340: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601341: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601342: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601343: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601345: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601346: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601347: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601348: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601349: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601350: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601351: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601354: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601358: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601359: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601360: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601362: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601365: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601366: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601369: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601370: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601371: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601373: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601375: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601376: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601377: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601380: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601382: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601384: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601385: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601386: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601388: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601389: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601390: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601392: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601393: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601394: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601395: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601396: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601403: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601407: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601408: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601410: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601411: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601412: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601413: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601415: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601416: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601417: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601418: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601420: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601422: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601427: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601428: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601439: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601442: workbook step `Procurement Manager`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601443: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601444: workbook step `Procurement Manager`; live status `Open order`; approval `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601448: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601452: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601455: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601460: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601461: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601462: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601465: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601469: workbook step `LPO sent/shared with supplier`; live status `Canceled`; approval `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601470: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601473: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601477: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601479: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601480: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601482: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601483: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601486: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601487: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601494: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601496: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601497: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601500: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601508: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601512: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601530: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601531: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601532: workbook step `Procurement Manager`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601536: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PO SCBM-PO2601571: workbook step `LPO sent/shared with supplier`; live status `Invoiced`; approval `Confirmed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000001: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000002: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000003: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000005: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000008: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000009: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000010: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000012: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000014: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000016: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000020: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000025: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000029: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000030: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000032: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000036: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000037: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000038: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000039: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000040: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000042: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000044: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000046: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000047: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000048: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000049: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000056: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000060: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000062: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000065: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000066: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000067: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000078: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000079: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000081: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000093: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000094: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000097: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000098: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000101: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000111: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000219: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000224: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000232: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000259: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000432: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000434: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000437: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000440: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000458: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000478: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000591: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000607: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000644: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000707: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000762: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000763: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000794: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000832: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000875: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000966: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000968: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-000971: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001014: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001037: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001051: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001059: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001074: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001075: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001104: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001134: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001163: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001170: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001172: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001177: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001184: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001231: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001262: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001273: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001417: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001486: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001499: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001511: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001530: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001538: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001539: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001548: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001551: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001687: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001698: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001771: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001794: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001823: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001889: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001896: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001924: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001929: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001950: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001974: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-001984: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-002008: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-002014: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-002182: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-002447: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-002457: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-002499: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-002655: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-002668: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-002725: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-002790: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-002915: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-002962: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-002989: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-002991: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003044: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003114: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003115: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003202: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003212: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003213: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003215: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003245: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003246: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003247: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003248: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003249: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003315: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003317: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003334: workbook step `Unit prices updated in PR lines`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003372: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003407: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003409: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003417: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003424: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003661: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003673: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003686: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003688: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003703: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003708: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003712: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003742: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003743: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003797: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003811: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003911: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-003937: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004006: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004009: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004044: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004049: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004168: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004285: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004404: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004437: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004466: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004467: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004468: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004520: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004547: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004548: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004609: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004643: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004753: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004790: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004873: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004911: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004913: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004957: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004964: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-004970: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005014: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005016: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005149: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005151: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005157: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005278: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005374: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005392: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005450: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005516: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005519: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005548: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005562: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005593: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005617: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005620: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005701: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005719: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005730: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005734: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005735: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005814: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005830: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005832: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005840: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005850: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005882: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005936: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005943: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005947: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-005980: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006008: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006060: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006102: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006129: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006153: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006161: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006180: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006197: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006198: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006203: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006216: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006248: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006287: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006322: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006323: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006324: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006345: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006375: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006387: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006388: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006494: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006508: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006512: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006575: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006576: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006579: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006585: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006587: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006634: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006659: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006702: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006778: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006783: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006844: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006849: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006850: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006853: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006868: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006967: workbook step `Unit prices updated in PR lines`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-006969: workbook step `Unit prices updated in PR lines`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-007082: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-007115: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-007121: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-007235: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-007272: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-007381: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-007395: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-007416: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-007425: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-007487: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-007653: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-007692: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-007745: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-007839: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-007943: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008011: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008088: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008091: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008137: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008155: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008180: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008311: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008332: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008347: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008367: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008372: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008375: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008417: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008456: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008482: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008497: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008502: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008508: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008534: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008538: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008572: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008639: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008688: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008690: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008816: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008839: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008895: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008902: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008905: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008915: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-008946: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009047: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009050: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009051: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009058: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009059: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009104: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009109: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009144: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009145: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009189: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009593: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009594: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009597: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009616: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009630: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009631: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009633: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009700: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009702: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009703: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009704: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009708: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009720: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009759: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009810: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009812: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009834: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009841: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009843: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009844: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-009875: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010099: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010101: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010144: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010172: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010181: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010275: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010305: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010316: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010383: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010426: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010553: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010562: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010565: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010568: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010585: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010587: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010588: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010592: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010600: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010607: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010617: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010748: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010857: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010937: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010938: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-010959: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011003: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011059: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011149: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011150: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011156: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011158: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011189: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011195: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011224: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011233: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011303: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011305: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011306: workbook step `Unit prices updated in PR lines`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011342: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011369: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011380: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011390: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011393: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011466: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011563: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011579: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011590: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011595: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011596: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011627: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011646: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011737: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011739: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011745: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011816: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011821: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011823: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011824: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011825: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011826: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011827: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011828: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011832: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011847: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011861: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011874: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011876: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011925: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-011998: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012038: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012077: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012084: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012125: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012128: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012132: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012147: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012211: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012219: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012531: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012541: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012556: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012611: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012628: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012658: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012683: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012791: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012808: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012843: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-012968: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-013052: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-013125: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-013635: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-013659: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-013671: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-013770: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-013787: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-013926: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014162: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014179: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014184: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014201: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014205: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014208: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014404: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014412: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014432: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014455: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014460: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014474: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014496: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014498: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014501: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014537: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014587: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014659: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014688: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014703: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014704: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014720: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014723: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014726: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014731: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014860: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014944: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014964: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014970: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014973: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014975: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-014994: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-015040: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-015081: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-015205: workbook step `Unit prices updated in PR lines`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-015230: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-015238: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-015415: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-015417: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-015519: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-015754: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-015786: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-015826: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-015866: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016120: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016355: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016360: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016371: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016379: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016387: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016528: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016537: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016630: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016676: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016808: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016841: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016895: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016896: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016897: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016913: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016923: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016947: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016953: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016981: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-016988: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017205: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017209: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017237: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017256: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017257: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017259: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017266: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017416: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017431: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017433: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017437: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017439: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017445: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017448: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017449: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017485: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017487: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017488: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017492: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017511: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017515: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017516: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017521: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017523: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017527: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017553: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017596: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017597: workbook step `Unit prices updated in PR lines`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017648: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017651: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017655: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017689: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017722: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017749: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017784: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017817: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017819: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017839: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017840: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017841: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017844: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017850: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-017913: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018012: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018025: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018061: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018142: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018168: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018188: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018196: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018197: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018201: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018203: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018206: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018234: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018237: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018238: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018239: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018244: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018245: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018274: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018275: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018345: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018450: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018479: workbook step `Unit prices updated in PR lines`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018507: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018517: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018618: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018695: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018699: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018700: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018723: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018728: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018730: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018766: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018771: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018806: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018816: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018842: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018882: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018904: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018962: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018964: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018965: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018968: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-018978: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019023: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019038: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019058: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019087: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019112: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019156: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019283: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019337: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019339: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019357: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019411: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019479: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019520: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019522: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019523: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019524: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019528: workbook step `Quotation shared to Operations for confirmation`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019530: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019532: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019534: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019564: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019585: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019591: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019595: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019600: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019604: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019645: workbook step `Unit prices updated in PR lines`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019724: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019758: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019764: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019767: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019772: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019773: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019777: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019840: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019854: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019855: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019910: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019913: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019954: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-019972: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020043: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020057: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020065: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020108: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020144: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020145: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020183: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020185: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020189: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020191: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020220: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020241: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020256: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020259: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020308: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020325: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020363: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020384: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020387: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020459: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020545: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020546: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020547: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020550: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020553: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020581: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020629: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020635: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020639: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020678: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020682: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020684: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020692: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020702: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020765: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020811: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020823: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020857: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020863: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020865: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020913: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-020917: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021025: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021083: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021090: workbook step `Unit prices updated in PR lines`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021091: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021095: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021113: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021145: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021178: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021265: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021297: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021303: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021323: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021325: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021340: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021352: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021354: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021364: workbook step `Unit prices updated in PR lines`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021398: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021436: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021440: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021443: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021445: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021466: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021469: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021512: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021514: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021608: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021613: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021622: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021630: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021631: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021644: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021647: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021660: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021747: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021846: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021847: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021865: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021920: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-021983: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022056: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022059: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022062: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022083: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022097: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022103: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022119: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022123: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022127: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022319: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022334: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022336: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022342: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022343: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022352: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022394: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022403: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022416: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022435: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022437: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022446: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022450: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022454: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022467: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022471: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022484: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022485: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022486: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022487: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022537: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022538: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022539: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022558: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022581: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022729: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022766: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022768: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022772: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022802: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022805: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022816: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022818: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022840: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022895: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022910: workbook step `Unit prices updated in PR lines`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022916: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022922: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022931: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022936: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022946: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022977: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-022988: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023074: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023145: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023208: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023309: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023328: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023365: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023369: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023374: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023377: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023426: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023503: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023525: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023631: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023649: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023655: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023656: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023657: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023658: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023659: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023661: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023663: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023722: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023770: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023775: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023844: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023867: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023869: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023871: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023881: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023890: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023906: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023919: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023923: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023925: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023932: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023936: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023937: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023938: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023976: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023984: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023987: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023990: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-023992: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024064: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024080: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024125: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024126: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024127: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024237: workbook step `Unit prices updated in PR lines`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024275: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024300: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024302: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024305: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024331: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024364: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024421: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024468: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024525: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024545: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024578: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024579: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024594: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024595: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024608: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024609: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024651: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024655: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024669: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024676: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024705: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024729: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024732: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024738: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024749: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024750: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024751: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024753: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024754: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024759: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024768: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024844: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024846: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024848: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024870: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024891: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024897: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024899: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024919: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024938: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024954: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-024959: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025018: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025040: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025043: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025044: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025051: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025070: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025083: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025100: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025101: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025107: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025110: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025130: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025161: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025162: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025164: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025171: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025172: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025202: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025206: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025209: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025214: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025219: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025221: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025222: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025224: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025228: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025232: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025237: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025238: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025260: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025262: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025269: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025276: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025283: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025284: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025287: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025295: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025299: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025300: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025335: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025369: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025459: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025461: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025464: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025468: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025483: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025485: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025524: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025551: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025556: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025560: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025565: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025567: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025570: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025572: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025576: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025579: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025580: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025588: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025609: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025626: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025628: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025639: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025641: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025643: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025656: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025671: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025672: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025675: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025681: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025683: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025685: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025691: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025709: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025725: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025731: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025732: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025733: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025736: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025737: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025742: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025745: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025944: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025955: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025956: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025958: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025959: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025961: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025963: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025984: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025985: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025988: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-025996: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026004: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026006: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026008: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026018: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026056: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026067: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026068: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026074: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026105: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026109: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026112: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026113: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026114: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026115: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026118: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026122: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026176: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026194: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026197: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026223: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026224: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026225: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026226: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026228: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026229: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026242: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026264: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026272: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026273: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026274: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026275: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026287: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026302: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026339: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026345: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026348: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026422: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026473: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026475: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026477: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026478: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026481: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026496: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026498: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026499: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026501: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026504: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026505: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026536: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026539: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026543: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026548: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026566: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026567: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026568: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026583: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026589: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026634: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026649: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026747: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026748: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026791: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026814: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026870: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026886: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026887: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026892: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026916: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026917: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026919: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026920: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026922: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026950: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026956: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026963: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026964: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026970: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-026979: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027005: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027009: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027018: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027038: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027043: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027044: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027045: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027047: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027049: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027051: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027054: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027123: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027128: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027129: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027138: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027164: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027185: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027186: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027189: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027201: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027206: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027214: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027217: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027231: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027235: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027236: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027251: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027284: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027285: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027286: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027288: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027289: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027292: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027333: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027382: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027387: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027437: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027582: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027684: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027686: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027687: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027688: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027741: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027753: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027838: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027853: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027871: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027876: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027899: workbook step `Unit prices updated in PR lines`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027903: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027905: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027907: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027924: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027936: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027941: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-027992: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028008: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028010: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028012: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028014: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028016: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028021: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028050: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028052: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028053: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028058: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028060: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028080: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028088: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028094: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028108: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028111: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028122: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028132: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028135: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028143: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028146: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028150: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028152: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028153: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028157: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028159: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028162: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028165: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028175: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028177: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028213: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028228: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028238: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028287: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028301: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028302: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028314: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028341: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028345: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028349: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028357: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028386: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028391: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028400: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028464: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028468: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028469: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028503: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028512: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028513: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028514: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028542: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028564: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028608: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028610: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028611: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028612: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028614: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028626: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028664: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028673: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028674: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028681: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028688: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028702: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028728: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028736: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028766: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028777: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028805: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028841: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028842: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028843: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028844: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028905: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028919: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028924: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028926: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028934: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028950: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028953: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028957: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028964: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-028986: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029043: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029064: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029081: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029106: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029112: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029137: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029147: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029150: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029204: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029217: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029234: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029250: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029259: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029260: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029261: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029262: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029263: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029265: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029266: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029267: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029295: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029300: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029365: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029366: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029367: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029368: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029371: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029373: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029378: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029379: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029380: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029381: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029392: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029395: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029399: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029425: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029426: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029428: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029453: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029483: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029486: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029491: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029498: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029512: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029555: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029573: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029584: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029586: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029590: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029599: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029633: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029645: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029706: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029711: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029719: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029723: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029724: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029727: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029728: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029731: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029732: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029733: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029734: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029735: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029737: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029739: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029740: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029744: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029752: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029756: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029774: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029775: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029779: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029780: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029783: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029804: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029841: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029907: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029960: workbook step `Quotation shared to Operations for confirmation`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029962: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029963: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029964: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029967: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-029979: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030012: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030013: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030016: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030020: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030028: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030082: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030095: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030098: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030100: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030104: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030106: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030133: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030136: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030150: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030153: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030162: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030170: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030171: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030184: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030191: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030247: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030255: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030279: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030284: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030340: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030351: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030371: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030378: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030488: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030505: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030513: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030515: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030524: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030548: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030553: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030560: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030564: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030596: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030601: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030603: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030604: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030629: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030657: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030659: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030662: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030663: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030664: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030677: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030688: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030690: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030698: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030699: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030702: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030703: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030704: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030713: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030724: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030731: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030732: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030735: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030784: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030798: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030801: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030810: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030811: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030819: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030824: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030834: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030835: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030893: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-030908: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031040: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031045: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031049: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031051: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031057: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031085: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031135: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031143: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031152: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031163: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031164: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031173: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031203: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031210: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031266: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031289: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031305: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031316: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031320: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031321: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031326: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031327: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031358: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031377: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031379: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031383: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031389: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031393: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031404: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031446: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031481: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031493: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031495: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031497: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031499: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031503: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031524: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031525: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031545: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031589: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031596: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031609: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031622: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031633: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031638: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031640: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031657: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031667: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031681: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031682: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031722: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031723: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031728: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031731: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031734: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031735: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031742: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031750: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031751: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031752: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031753: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031754: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031755: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031760: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031762: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031777: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031786: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031818: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031825: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031969: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031977: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031995: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-031997: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032008: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032013: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032038: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032058: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032084: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032086: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032099: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032116: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032153: workbook step `Procurement sends inquiry/RFQ to suppliers`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032162: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032170: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032174: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032242: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032342: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032457: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032468: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032522: workbook step `Quotation shared to Operations for confirmation`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032529: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032539: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032562: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032625: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032635: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032643: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032658: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032668: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032671: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032693: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032729: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032741: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032748: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032763: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032768: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032775: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032780: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032799: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032981: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032983: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-032993: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033009: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033110: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033124: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033160: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033175: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033177: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033209: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033212: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033257: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033306: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033315: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033329: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033448: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033457: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033459: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033469: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033474: workbook step `Unit prices updated in PR lines`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033548: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033578: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033579: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033580: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033583: workbook step `Unit prices updated in PR lines`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033599: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033609: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033615: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033631: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033662: workbook step `Quotation shared to Operations for confirmation`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033663: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033705: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033727: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033746: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033761: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033774: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033813: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033827: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033839: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033856: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033861: workbook step `Unit prices updated in PR lines`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-033932: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-034004: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-034051: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-034080: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-034108: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-034177: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-034182: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-034198: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-034204: workbook step `Unit prices updated in PR lines`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-034417: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-034421: workbook step `Unit prices updated in PR lines`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-034432: workbook step `Unit prices updated in PR lines`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-034478: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-034801: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR CPR-034845: workbook step `Unit prices updated in PR lines`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000107: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000109: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000110: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000111: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000113: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000114: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000117: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000118: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000119: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000120: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000121: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000122: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000123: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000124: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000125: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000127: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000129: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000130: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000131: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000134: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000136: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000137: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000138: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000139: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000145: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000146: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000149: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000151: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000152: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000155: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000156: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000160: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000165: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000166: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000167: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000168: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000169: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000171: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000173: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000177: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000178: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000180: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000181: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000185: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000190: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000196: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000197: workbook step `PurchReqReviewTask`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000622: workbook step `Building Services_Asst. Facility Managers 1`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000671: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000710: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000740: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000743: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000745: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000822: workbook step `PurchReqReviewApproval`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000826: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000856: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000902: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000914: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000916: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000917: workbook step `Facilities Management_Director`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000950: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000956: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000958: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000986: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000987: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000989: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000990: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-000998: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001000: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001003: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001012: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001016: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001017: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001018: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001019: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001020: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001030: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001032: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001036: workbook step `Home Services_Operations Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001037: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001041: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001042: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001045: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001046: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001047: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001048: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001049: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001050: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001051: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001052: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001053: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001054: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001059: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001061: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001063: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001064: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001065: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001066: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001067: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001068: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001070: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001072: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001073: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001074: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001075: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001076: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001078: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001080: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001082: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001083: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001085: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001086: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001087: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001088: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001089: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001090: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001091: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001092: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001093: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001094: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001095: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001096: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001097: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001098: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001099: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001100: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001101: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001102: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001103: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001104: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001105: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001106: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001107: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001108: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001109: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001112: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001113: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001114: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001115: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001116: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001122: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001126: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001128: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001129: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001130: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001131: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001132: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001133: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001134: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001135: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001136: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001137: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001138: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001139: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001141: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001142: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001143: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001145: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001146: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001147: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001148: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001149: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001150: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001151: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001152: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001153: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001154: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001155: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001156: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001157: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001158: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001159: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001160: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001161: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001164: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001165: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001166: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001168: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001169: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001170: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001171: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001172: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001174: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001175: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001176: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001178: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001179: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001183: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001185: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001186: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001187: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001188: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001194: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001195: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001196: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001197: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001198: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001199: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001200: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001201: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001202: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001203: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001204: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001205: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001206: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001207: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001208: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001209: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001210: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001211: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001212: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001214: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001215: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001216: workbook step `Finance & Accounts_Accounting Manager`; live status `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001217: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001218: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001219: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001220: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001221: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001222: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001223: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001224: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001225: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001227: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001228: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001229: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001230: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001231: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001232: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001233: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001234: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001235: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001236: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001237: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001238: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001239: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001240: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001241: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001242: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001243: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001244: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001245: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001246: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001247: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001248: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001249: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001250: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001251: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001252: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001253: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001254: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001256: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001257: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001259: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001260: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001262: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001263: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001264: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001265: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001267: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001268: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001269: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001270: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001271: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001272: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001273: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001274: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001275: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001276: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001277: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001278: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001279: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001280: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001281: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001282: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001283: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001284: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001285: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001287: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001288: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001289: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001290: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001291: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001292: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001293: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001294: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001295: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001296: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001297: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001298: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001300: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001301: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001302: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001303: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001304: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001305: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001306: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001307: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001308: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001309: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001310: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001311: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001312: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001314: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001315: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001316: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001317: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001319: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001320: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001321: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001322: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001323: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001324: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001325: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001326: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001328: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001332: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001333: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001334: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001335: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001336: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001337: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001338: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001339: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001340: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001341: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001342: workbook step `Unit prices updated in PR lines`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001343: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001344: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001345: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001346: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001347: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001348: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001349: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001350: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001351: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001352: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001353: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001354: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001355: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001356: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001357: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001362: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001363: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001364: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001365: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001366: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001367: workbook step `Housekeeping_Asst. Manager`; live status `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001368: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001369: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001370: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001371: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001372: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001373: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001374: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001375: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001376: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001377: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001378: workbook step `Building Services_Facilities Manager`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001379: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001380: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001381: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001382: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001383: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001384: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001385: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001386: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001387: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001388: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001389: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001390: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001391: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001392: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001393: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001394: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001395: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001396: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001397: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001398: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001399: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001400: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001401: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001402: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001403: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001405: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001406: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001407: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001408: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001409: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001410: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001412: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001414: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001415: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001416: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001417: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001418: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001419: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001420: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001421: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001424: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001425: workbook step `PurchReqReviewApproval`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001426: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001427: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001428: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001429: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001430: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001432: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001433: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001435: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001438: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001439: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001442: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001443: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001444: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001445: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001447: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001449: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001450: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001452: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001453: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001454: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001455: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001456: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001458: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001459: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001460: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001461: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001462: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001463: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001464: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001465: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001466: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001467: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001468: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001469: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001470: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001471: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001472: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001473: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001474: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001475: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001476: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001477: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001478: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001479: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001480: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001481: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001482: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001483: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001484: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001485: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001486: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001487: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001488: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001489: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001490: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001491: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001492: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001494: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001495: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001496: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001497: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001498: workbook step `Unit prices updated in PR lines`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001499: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001500: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001501: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001502: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001503: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001504: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001505: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001506: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001507: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001508: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001509: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001510: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001511: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001513: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001514: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001515: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001516: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001517: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001518: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001519: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001520: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001521: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001522: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001524: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001525: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001526: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001527: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001528: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001529: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001530: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001531: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001532: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001533: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001535: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001538: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001539: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001540: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001541: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001542: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001543: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001547: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001548: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001549: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001550: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001551: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001552: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001553: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001554: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001557: workbook step `Commercial_Director`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001558: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001559: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001560: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001561: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001562: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001563: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001565: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001566: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001567: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001568: workbook step `PurchReqReviewTask`; live status `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001569: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001570: workbook step `Home Services_Operations Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001571: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001572: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001573: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001574: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001576: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001578: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001579: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001580: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001581: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001582: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001583: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001585: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001586: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001587: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001588: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001589: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001590: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001591: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001592: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001593: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001594: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001595: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001596: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001597: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001598: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001599: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001600: workbook step `Unit prices updated in PR lines`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001601: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001602: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001603: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001604: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001605: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001606: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001607: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001608: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001609: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001610: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001611: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001612: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001613: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001614: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001615: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001616: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001617: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001618: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001621: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001622: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001623: workbook step `PurchReqReviewTask`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001625: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001626: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001628: workbook step `Finance & Accounts_Accounting Manager`; live status `Cancelled`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001629: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001631: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001633: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001634: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001635: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001636: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001637: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001638: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001639: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001640: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001641: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001642: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001644: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001645: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001646: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001647: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001648: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001655: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001657: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001659: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001660: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001663: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001664: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001665: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001666: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001667: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001669: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001670: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001671: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001673: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001674: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001675: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001676: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001677: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001680: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001683: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001685: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001686: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001687: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001688: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001689: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001690: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001691: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001692: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001693: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001696: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001697: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001704: workbook step `PurchReqReviewTask`; live status `Rejected`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001705: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001707: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001710: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001711: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001712: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001716: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001719: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001722: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001723: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001724: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001727: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001729: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001730: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001731: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001732: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001733: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001734: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001736: workbook step `PAC Services_Manager`; live status `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001739: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001740: workbook step `PurchReqReviewTask`; live status `Draft`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001741: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001745: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001749: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001752: workbook step `Executive Management_CEO`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001755: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001756: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001757: workbook step `Finance & Accounts_Accounting Manager`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.
- PR PR-001760: workbook step `Facilities Management_Director`; live status `Closed`; `STALE_WORKBOOK_ROW_OUTSIDE_DASHBOARD_POPULATION`.

## What I found

- R1 removes closed, cancelled, rejected and invoiced rows from the gate without deleting or hiding their evidence.
- R3 fixes exact-equality false negatives and lifts both dashboard-population amount gates above 95%.
- PO stage still fails because most current receipt events pre-date the export and the exposed confirmation entity has no rows.

## Problems and risks

- Counting old PO events as post-export progression would directly violate R2.
- Deploying now would replace the workbook with a PO stage model measured at 44.02% agreement.
- The operational systems continue moving; the UTC evidence position above identifies this run.

## Files changed

- Reconciliation logic, Correction 02 evidence/report, project status documentation and the unpublished change note.

## What I did not change

- No dashboard, Race Control, email, snapshot or proxy runtime path was cut over.
- No workbook, generator, fallback or workbook workflow was removed.
- No Dataverse or Azure resource was written. No function app or GitHub Pages site was deployed.
- The proxy guard on `main` remains unchanged and prevents push deployment to Chandan's app.

## Testing performed

- Python compile and machine-evidence assertions.
- Complete read-only reconciliation against both Dataverse organisations and both unchanged workbooks.
- Existing dashboard JavaScript and weekly-snapshot regression tests.
- Desktop browser visual check and inspection of the existing 700 px responsive rule in the unpublished change note.
- Git diff and remote-branch verification; production remained unchanged.

## Commands recorded

- `python tests/reconcile_workbook_retirement.py --out evidence/workbook-retirement-correction-02.json` with short-lived Azure CLI tokens supplied only to the child process.
- `python tests/render_retirement_correction02.py evidence/workbook-retirement-reconciliation.json evidence/workbook-retirement-correction-01.json evidence/workbook-retirement-correction-02.json evidence/workbook-retirement-correction-02.md --notes NOTES.md`.
- `node --test tests/dataverse-live.test.js tests/race-control.test.js`.
- `python tests/test_weekly_snapshot.py`.

## Remaining risks

- The 393 reason-coded PO stage differences prevent retirement under the supplied rules.
- Production remains workbook-dependent and still depends on the morning email chain.

## Recommended next step

Do not invent another progression rule. Resolve the PO event-timing gap at source or explicitly change R2, then rerun the same dashboard-population gates.

# Workbook retirement correction 03 — 7 September 2026

## Verdict

**Cannot retire.** The replacement PO tests are valid, but P1 and P3 fail. The safe-cutover stop applies before deployment, merge to `main`, or workbook removal.

| Gate | 7 Sep verdict | Correction 01 | Correction 02 | Correction 03 |
|---|---:|---:|---:|---:|
| PR stage | 489/571 (85.64%) | 512/571 (89.67%) | 521/547 (95.25%) | 521/547 (95.25%) settled PASS |
| PR procurement clock | 541/564 (95.92%) | 540/564 (95.74%) | 496/509 (97.45%) | 496/509 (97.45%) settled PASS |
| PO stage | 430/1,493 (28.80%) | 653/1,495 (43.68%) | 309/702 (44.02%) | RETIRED |
| PO P1 stage evidence | — | — | — | 512/983 (52.09%) FAIL |
| PO P2 F&O population parity | — | — | — | 983/983 (100.00%) PASS |
| PO P3 maintained approval steps | — | — | — | 3/61 (4.92%) FAIL |
| PO P4 LPO-sent distribution | — | — | — | Reported; 1,099 received or invoiced |
| PO P5 human sample | — | — | — | 25/25 complete |
| PR amount | 819/4,394 (18.64%) | 3,560/4,394 (81.02%) | 556/566 (98.23%) | 556/566 (98.23%) settled PASS |
| PO amount | 85/2,977 (2.86%) | 2,923/2,977 (98.19%) | 707/714 (99.02%) | 707/714 (99.02%) settled PASS |
| Distinct documents | Exact | Exact | Exact | Exact settled PASS |

Correction 03 carries the accepted Correction 02 PR, amount and document-count results unchanged. It replaces only the retired PO stage gate.

## P1 — every live PO stage is evidenced

Result: **FAIL**. 512/983 open F&O purchase orders have a dated event (52.09%); 471 are displayed as `STAGE_NOT_EVIDENCED`.

Reason counts: `NO_LIVE_STAGE_EVIDENCE` 79, `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE` 389, `STAGE_EVENT_TIMESTAMP_UNAVAILABLE` 3.

- ihhr / P0000000001: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- pblc / P0000000001: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- pblc / P0000000006: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- pblc / P0000000036: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- pblc / P0000000041: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- pblc / P0000000042: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- pblc / P0000000046: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- pblc / P0000000047: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- pblc / P0000000061: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- pblc / P0000000072: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- pblc / PBLC-PO2600002: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- pblc / PBLC-PO2600014: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- pblc / PBLC-PO2600017: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- pblc / PBLC-PO2600018: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Approved`; `NO_LIVE_STAGE_EVIDENCE`.
- pblc / PBLC-PO2600020: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- pblc / PBLC-PO2600028: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- pblc / PBLC-PO2600029: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- pblc / PBLC-PO2600031: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- pbll / P0000000012: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- pbll / P0000000016: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- rsrs / P0000000016: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- rsrs / P0000000021: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- rsrs / P0000000026: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- rsrs / RSRS-PO2600003: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- rsrs / RSRS-PO2600009: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- rsrs / RSRS-PO2600028: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Approved`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000001: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000009: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000029: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000040: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000059: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000081: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000091: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000099: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000108: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000112: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000115: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000132: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000174: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000175: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000182: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000195: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000206: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000207: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000208: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000220: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000221: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000232: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000238: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000251: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000258: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000259: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000271: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000274: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000291: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000296: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000303: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000307: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000308: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000313: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000315: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000322: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000327: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000328: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000341: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000356: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000361: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000375: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000400: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000404: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000405: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000407: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000423: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000427: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000474: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000485: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000510: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000512: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000535: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000547: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000559: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000563: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000575: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000633: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000676: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000681: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000754: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000755: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000760: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000774: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000796: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000798: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000802: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000804: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000805: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000824: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000829: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000830: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000833: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000834: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000843: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000867: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000907: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000917: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000918: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000947: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000948: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000964: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000982: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000985: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000990: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000001002: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001019: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001038: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001040: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001048: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001093: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001153: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001160: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Approved`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000001170: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001172: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001185: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001212: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001233: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001239: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001244: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001252: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000001253: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000001272: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001274: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001276: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001278: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001280: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001282: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001284: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001286: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000001296: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001313: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001319: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001338: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001345: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001355: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001371: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001387: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000001388: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000001391: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001392: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000001403: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000001405: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001407: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000001408: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001409: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001410: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000001440: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001446: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001454: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001477: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001483: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001518: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001522: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001532: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000001533: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001535: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001546: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001550: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001556: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001557: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000001588: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001589: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600023: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600029: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600049: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600062: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600064: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600065: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600094: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600099: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600101: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600111: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600130: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600140: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600149: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600167: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600196: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600204: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600213: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600220: candidate `Receipt posted`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `STAGE_EVENT_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600236: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600241: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600246: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600251: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600314: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600338: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600352: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600365: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600371: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600390: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600397: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600399: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600401: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600446: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600475: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600480: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600484: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600485: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600488: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600523: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600526: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600536: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600538: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600543: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600558: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600560: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600561: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600569: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600603: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600604: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600624: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600638: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600645: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600651: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600653: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600655: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600658: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600690: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600694: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600706: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600708: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600713: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600714: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600736: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600737: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600738: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600744: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600753: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600754: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600795: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600813: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600819: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600827: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600845: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600846: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600847: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600850: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600885: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600886: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600895: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600897: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600902: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600903: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600904: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600919: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600922: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600948: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600954: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600957: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600961: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600976: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600980: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600995: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601002: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601026: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601028: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601031: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `In review`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601033: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601034: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601035: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601045: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601047: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601060: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601068: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601076: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601092: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601093: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601097: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601104: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601111: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601115: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601120: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601121: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601122: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601123: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601134: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `In review`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601138: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `In review`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601140: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601141: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601158: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601175: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601176: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601180: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601182: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601184: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601197: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601204: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601207: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601208: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601210: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601226: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601228: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601249: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601255: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601265: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601268: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601269: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601273: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601297: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601311: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601319: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601325: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601344: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601352: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601353: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601355: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601363: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601364: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601367: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601372: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601378: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601387: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601398: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601399: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601400: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601405: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601409: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601419: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601421: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601426: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601429: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601430: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601433: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601434: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601435: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601437: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601438: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601440: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601445: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601446: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601447: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601449: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601453: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601454: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601456: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601457: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601464: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601466: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601467: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601474: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601476: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601485: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601488: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601489: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601490: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601491: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601493: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601495: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601498: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601501: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601504: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601505: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601506: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601510: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601511: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601513: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601514: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601516: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Approved`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601517: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `In review`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601518: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601519: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601520: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601521: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601522: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601523: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601524: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601525: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601526: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601528: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601529: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601533: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601534: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601537: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601538: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601539: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601540: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601541: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601542: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601543: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601544: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601545: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601546: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601547: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601548: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601549: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601550: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601551: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601552: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601553: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601554: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601555: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601556: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601559: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601560: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601561: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601562: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601563: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601564: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601565: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601566: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601567: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601568: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601569: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601570: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601573: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601574: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601575: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601576: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601577: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601578: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601580: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601581: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601582: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601583: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601584: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601586: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601587: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601589: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601590: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601591: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601592: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601593: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601594: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601595: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601596: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601597: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601599: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601600: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601601: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601602: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601605: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601606: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / P0000000001: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / P0000000031: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / P0000000046: candidate `Receipt posted`; displayed `STAGE_NOT_EVIDENCED`; F&O `Received` / approval `Confirmed`; `STAGE_EVENT_TIMESTAMP_UNAVAILABLE`.
- scpg / P0000000051: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scpg / P0000000061: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scpg / SCPG-PO2600002: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600004: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600006: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600009: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600011: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scpg / SCPG-PO2600012: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scpg / SCPG-PO2600014: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600037: candidate `none`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Draft`; `NO_LIVE_STAGE_EVIDENCE`.
- scpg / SCPG-PO2600039: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600040: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600041: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600042: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600043: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600044: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600045: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600058: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600061: candidate `Receipt posted`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `STAGE_EVENT_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600063: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600065: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600066: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600067: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600069: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600070: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600071: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600072: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600075: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scpg / SCPG-PO2600076: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; F&O `Open order` / approval `Confirmed`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.

## P2 — population parity with F&O

Result: **PASS**. The candidate live population contains 983/983 open legal-entity/document keys (100.00%). Purchase-order numbers reused across companies are keyed by legal entity and are not collapsed.

- Differences: none.

## P3 — workbook parity where the workbook is maintained

Result: **FAIL**. 3/61 R1-population approval rows agree after R2 (4.92%); the target is 95%.
The supplied count of 108 is not the workbook count: the six named approval values total 118. Of those, 61 are in the current R1 population and 57 are outside it. This arithmetic is reported rather than forced to 108.

Reason counts: `PROGRESSION_NOT_AFTER_EXPORT` 16, `PROGRESSION_TIMESTAMP_UNAVAILABLE` 33, `STAGE_NOT_EVIDENCED` 9.

- scbm / P0000000151: workbook `Accounting Manager` → live `Receipt posted`; event `posted packing slip` at `2026-07-27T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / P0000001160: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `none` at `none`; `STAGE_NOT_EVIDENCED`.
- scbm / SCBM-PO2600218: workbook `Procurement Manager` → live `Receipt posted`; event `posted packing slip` at `2026-06-29T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / SCBM-PO2600317: workbook `Advance payment request submitted (if applicable)` → live `Receipt posted`; event `posted packing slip` at `2026-04-15T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / SCBM-PO2600399: workbook `Accounting Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600488: workbook `Advance payment request submitted (if applicable)` → live `STAGE_NOT_EVIDENCED`; event `none` at `none`; `STAGE_NOT_EVIDENCED`.
- scbm / SCBM-PO2600568: workbook `Accounting Manager` → live `Receipt posted`; event `posted packing slip` at `2026-04-16T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / SCBM-PO2600624: workbook `Accounting Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600638: workbook `Accounting Manager` → live `STAGE_NOT_EVIDENCED`; event `none` at `none`; `STAGE_NOT_EVIDENCED`.
- scbm / SCBM-PO2600645: workbook `Accounting Manager` → live `STAGE_NOT_EVIDENCED`; event `none` at `none`; `STAGE_NOT_EVIDENCED`.
- scbm / SCBM-PO2600706: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `none` at `none`; `STAGE_NOT_EVIDENCED`.
- scbm / SCBM-PO2600713: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `none` at `none`; `STAGE_NOT_EVIDENCED`.
- scbm / SCBM-PO2600748: workbook `Advance payment request submitted (if applicable)` → live `Receipt posted`; event `posted packing slip` at `2026-07-22T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / SCBM-PO2600780: workbook `Accounting Manager` → live `Receipt posted`; event `posted packing slip` at `2026-05-28T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / SCBM-PO2600784: workbook `Accounting Manager` → live `Receipt posted`; event `posted packing slip` at `2026-05-28T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / SCBM-PO2600902: workbook `Advance payment request submitted (if applicable)` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600958: workbook `Procurement Manager` → live `Receipt posted`; event `posted packing slip` at `2026-08-15T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / SCBM-PO2601092: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601093: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601104: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601138: workbook `Accounting Manager` → live `STAGE_NOT_EVIDENCED`; event `none` at `none`; `STAGE_NOT_EVIDENCED`.
- scbm / SCBM-PO2601158: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601176: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601180: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601182: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601243: workbook `Accounting Manager` → live `Receipt posted`; event `posted packing slip` at `2026-08-05T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / SCBM-PO2601273: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601281: workbook `Advance payment request submitted (if applicable)` → live `Receipt posted`; event `posted packing slip` at `2026-08-31T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / SCBM-PO2601344: workbook `Accounting Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601356: workbook `Accounting Manager` → live `Receipt posted`; event `posted packing slip` at `2026-08-04T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / SCBM-PO2601391: workbook `Accounting Manager` → live `Receipt posted`; event `posted packing slip` at `2026-07-31T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / SCBM-PO2601398: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601421: workbook `Accounting Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601425: workbook `Procurement Manager` → live `Receipt posted`; event `posted packing slip` at `2026-08-31T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / SCBM-PO2601434: workbook `Accounting Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601441: workbook `Procurement Manager` → live `Receipt posted`; event `posted packing slip` at `2026-08-28T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / SCBM-PO2601507: workbook `Procurement Manager` → live `Receipt posted`; event `posted packing slip` at `2026-08-27T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / SCBM-PO2601516: workbook `Accounting Manager` → live `STAGE_NOT_EVIDENCED`; event `none` at `none`; `STAGE_NOT_EVIDENCED`.
- scbm / SCBM-PO2601523: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `none` at `none`; `STAGE_NOT_EVIDENCED`.
- scbm / SCBM-PO2601524: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601526: workbook `Advance payment request submitted (if applicable)` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601534: workbook `Accounting Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601546: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601551: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601558: workbook `Procurement Manager` → live `Receipt posted`; event `posted packing slip` at `2026-09-07T00:00:00Z`; `PROGRESSION_NOT_AFTER_EXPORT`.
- scbm / SCBM-PO2601561: workbook `Advance payment request submitted (if applicable)` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601562: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601581: workbook `Accounting Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601586: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601589: workbook `Accounting Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601590: workbook `Accounting Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601591: workbook `Accounting Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601592: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601593: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601594: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601595: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601596: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601597: workbook `Procurement Manager` → live `STAGE_NOT_EVIDENCED`; event `PO confirmation` at `none`; `PROGRESSION_TIMESTAMP_UNAVAILABLE`.

### P3 rows excluded by R1

- scbm / P0000000011: workbook `CEO`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600088: workbook `Accounting Manager`; F&O `Open order` / approval `Rejected`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600175: workbook `Accounting Manager`; F&O `Open order` / approval `Rejected`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600207: workbook `Finance and Accounts Director`; F&O `Open order` / approval `Rejected`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600420: workbook `Accounting Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600430: workbook `Accounting Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600431: workbook `Accounting Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600436: workbook `Accounting Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600451: workbook `Accounting Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600469: workbook `Accounting Manager`; F&O `Open order` / approval `Rejected`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600487: workbook `Accounting Manager`; F&O `Open order` / approval `Rejected`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600512: workbook `Accounting Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600525: workbook `Accounting Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600547: workbook `Advance payment request submitted (if applicable)`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600552: workbook `Accounting Manager`; F&O `Open order` / approval `Rejected`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600576: workbook `Accounting Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600577: workbook `Procurement Manager`; F&O `Open order` / approval `Rejected`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600606: workbook `Procurement Manager`; F&O `Open order` / approval `Rejected`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600614: workbook `Accounting Manager`; F&O `Canceled` / approval `Draft`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600615: workbook `Accounting Manager`; F&O `Canceled` / approval `Draft`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600661: workbook `Advance payment request submitted (if applicable)`; F&O `Canceled` / approval `Draft`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600674: workbook `Accounting Manager`; F&O `Open order` / approval `Rejected`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600692: workbook `Accounting Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600759: workbook `Accounting Manager`; F&O `Open order` / approval `Rejected`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600777: workbook `Accounting Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600783: workbook `Accounting Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600796: workbook `Procurement Manager`; F&O `Canceled` / approval `Draft`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600939: workbook `PurchTableApproval`; F&O `Open order` / approval `Rejected`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2600973: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601037: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601040: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601041: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601042: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601046: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601075: workbook `Procurement Manager`; F&O `Open order` / approval `Rejected`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601091: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601103: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601119: workbook `Finance and Accounts Director`; F&O `Open order` / approval `Rejected`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601124: workbook `Advance payment request submitted (if applicable)`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601156: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601187: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601189: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601220: workbook `Accounting Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601222: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601223: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601229: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601257: workbook `Procurement Manager`; F&O `Open order` / approval `Rejected`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601350: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601351: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601362: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601370: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601396: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601408: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601428: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601442: workbook `Procurement Manager`; F&O `Canceled` / approval `Draft`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601444: workbook `Procurement Manager`; F&O `Open order` / approval `Rejected`; `OUTSIDE_R1_DASHBOARD_POPULATION`.
- scbm / SCBM-PO2601532: workbook `Procurement Manager`; F&O `Invoiced` / approval `Confirmed`; `OUTSIDE_R1_DASHBOARD_POPULATION`.

### P3 PROGRESSED_AFTER_EXPORT matches

- None. No P3 progression had qualifying post-export evidence.

## P4 — LPO-sent rows reported, not gated

The business-case number is **1,099**: that many purchase orders still shown as merely `LPO sent` in the workbook are `Receipt posted` or `Invoiced` in F&O.

Live distribution: `Invoiced` 758, `Receipt posted` 341, `STAGE_NOT_EVIDENCED` 20, `Sent to supplier` 306.
Evidence coverage: 1,098/1,425; 327 do not have the dated event P1 requires.

### P4 rows without dated stage evidence

- scbm / P0000000029: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000040: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000099: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000081: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000108: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000112: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000115: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000124: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000132: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000174: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000175: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000182: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000195: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000206: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000207: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000208: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000220: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000221: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000232: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000238: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000251: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000258: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000259: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000271: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000274: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000307: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000308: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000313: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000315: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000322: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000327: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000328: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000341: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000356: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000375: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000361: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000400: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000404: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000405: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000407: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000423: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000474: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000510: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000512: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000547: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000563: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000575: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000633: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000676: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000681: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000754: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000755: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000760: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000774: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000802: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000804: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000805: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000813: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / P0000000824: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000829: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000833: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000843: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000907: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000918: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000948: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000964: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000000982: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001002: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001019: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001038: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001048: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001040: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001093: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001153: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001170: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001172: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001185: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001212: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001233: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001239: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001244: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001272: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001274: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001276: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001278: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001280: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001282: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001284: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001296: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001313: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001319: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001338: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001345: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001355: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001371: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001391: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001408: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001409: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001405: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001440: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001446: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001454: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001477: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001483: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001518: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001522: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001533: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001535: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001546: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001556: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001550: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001588: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / P0000001589: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600023: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600049: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600064: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600065: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600094: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600099: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600101: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600111: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600130: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600140: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600149: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600196: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600204: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600213: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600220: candidate `Receipt posted`; displayed `STAGE_NOT_EVIDENCED`; `STAGE_EVENT_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600241: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600314: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600352: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600365: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600390: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600397: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600446: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600475: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600480: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600485: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600523: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600526: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600536: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600538: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600543: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600558: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600560: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600561: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600603: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600604: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600613: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600637: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600651: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600653: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600655: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600658: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600659: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600666: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600668: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600675: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600690: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600694: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600695: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600708: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600714: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600733: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600738: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600741: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600744: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600753: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600754: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600795: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600813: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2600819: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600845: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600846: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600847: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600885: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600886: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600895: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600897: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600903: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600904: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600919: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600922: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600948: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600954: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600957: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600961: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600976: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600980: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2600995: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601002: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601026: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601028: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601033: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601034: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601035: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601045: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601047: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601060: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601064: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601067: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601068: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601076: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601097: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601111: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601115: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601120: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601121: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601122: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601123: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601140: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601141: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601175: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601184: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601197: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601204: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601207: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601208: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601210: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601226: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601228: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601249: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601255: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601265: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601268: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601290: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601291: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601297: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601311: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601319: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601325: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601353: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601355: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601364: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601367: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601372: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601378: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601387: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601399: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601400: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601405: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601409: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601417: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601419: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601426: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601429: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601430: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601433: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601435: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601437: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601438: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601440: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601445: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601446: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601447: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601449: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601454: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601456: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601457: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601464: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601466: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601467: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601469: candidate `STAGE_NOT_EVIDENCED`; displayed `STAGE_NOT_EVIDENCED`; `NO_LIVE_STAGE_EVIDENCE`.
- scbm / SCBM-PO2601474: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601476: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601485: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601488: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601489: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601490: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601491: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601493: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601495: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601498: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601501: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601504: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601505: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601506: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601510: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601511: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601513: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601514: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601518: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601519: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601520: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601521: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601522: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601528: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601529: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601533: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601538: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601539: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601540: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601541: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601542: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601543: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601544: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601545: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601547: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601548: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601549: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601550: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601552: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601553: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601554: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601555: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601556: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601559: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601560: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601563: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601564: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601565: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601566: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601567: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601568: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601569: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601570: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601573: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601574: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601575: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601576: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601577: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601578: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601580: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601582: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601583: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601584: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.
- scbm / SCBM-PO2601587: candidate `Sent to supplier`; displayed `STAGE_NOT_EVIDENCED`; `PO_CONFIRMATION_TIMESTAMP_UNAVAILABLE`.

## P5 — 25 purchase orders with human-checkable evidence

| Legal entity | Purchase order | Displayed live stage | Candidate stage | Evidence event | Event date (UTC) |
|---|---|---|---|---|---|
| scbm | SCBM-PO2600373 | Finance | Finance | approval capture assignment | 2026-08-06T17:17:36Z |
| pblc | PBLC-PO2600030 | Approval — unmapped element | Approval — unmapped element | approval capture assignment | 2026-09-04T13:55:03Z |
| ihhr | P0000000001 | STAGE_NOT_EVIDENCED | Sent to supplier | PO confirmation | none |
| scpg | P0000000006 | Receipt posted | Receipt posted | posted packing slip | 2025-07-17T00:00:00Z |
| rsrs | P0000000001 | Invoiced | Invoiced | posted vendor invoice | 2025-08-26T13:28:49Z |
| pblc | P0000000001 | STAGE_NOT_EVIDENCED | none | none | none |
| scbm | SCBM-PO2601579 | Finance | Finance | approval capture assignment | 2026-09-07T13:12:22Z |
| scbm | SCBM-PO2601603 | Approval — unmapped element | Approval — unmapped element | approval capture assignment | 2026-09-07T07:17:04Z |
| scpg | P0000000001 | STAGE_NOT_EVIDENCED | Sent to supplier | PO confirmation | none |
| rsrs | P0000000008 | Receipt posted | Receipt posted | posted packing slip | 2025-11-07T00:00:00Z |
| scbm | P0000000002 | Invoiced | Invoiced | posted vendor invoice | 2025-11-21T05:40:52Z |
| scbm | P0000000001 | STAGE_NOT_EVIDENCED | none | none | none |
| scbm | SCBM-PO2601585 | Finance | Finance | approval capture assignment | 2026-09-04T13:52:04Z |
| scpg | SCPG-PO2600077 | Approval — unmapped element | Approval — unmapped element | approval capture assignment | 2026-09-04T13:55:03Z |
| pbll | P0000000012 | STAGE_NOT_EVIDENCED | Sent to supplier | PO confirmation | none |
| rsrs | P0000000009 | Receipt posted | Receipt posted | posted packing slip | 2025-11-07T00:00:00Z |
| scpg | P0000000002 | Invoiced | Invoiced | posted vendor invoice | 2026-02-13T10:56:18Z |
| pblc | P0000000006 | STAGE_NOT_EVIDENCED | none | none | none |
| scbm | SCBM-PO2601588 | Finance | Finance | approval capture assignment | 2026-09-04T14:01:03Z |
| scpg | SCPG-PO2600078 | Approval — unmapped element | Approval — unmapped element | approval capture assignment | 2026-09-04T13:55:03Z |
| pbll | P0000000016 | STAGE_NOT_EVIDENCED | Sent to supplier | PO confirmation | none |
| rsrs | P0000000010 | Receipt posted | Receipt posted | posted packing slip | 2025-11-07T00:00:00Z |
| scbm | P0000000004 | Invoiced | Invoiced | posted vendor invoice | 2025-07-18T06:17:27Z |
| scbm | P0000000009 | STAGE_NOT_EVIDENCED | none | none | none |
| scbm | SCBM-PO2601598 | Finance | Finance | approval capture assignment | 2026-09-07T13:00:23Z |

## Source and stale-population evidence

- `po.xlsx`: 2,977 rows, 2,977 distinct order numbers, SHA-256 `cf55ac429b5623fff30e60a483fd1fcadbce20f1c409dbfc59780af894d09448`.
- F&O: 3,188 PO header keys, 3,868 packing slips, 25,198 invoice journals and 0 exposed confirmation rows.
- Approval capture: 11 current PO snapshots and 11 current PO work items.
- Evidence time: F&O read `2026-09-07T15:41:49.888172Z`; approval capture `2026-09-07T15:39:29Z`; effective `2026-09-07T15:39:29Z`.
- Stale workbook lane retained from Correction 02: 2,944 rows total, including 829 PO rows. The complete list remains at `evidence/workbook-retirement-correction-02.md#stale-rows-the-workbook-still-carries`.

### F&O confirmation entity catalogue

- `PurchPurchaseOrderConfirmationHeaderEntity`: generated in Dataverse = `false`.
- `PurchPurchaseOrderConfirmationLineEntity`: generated in Dataverse = `false`.
- `VRMPURCHASEORDERCONFIRMATIONARCHIVEDLINEENTITY`: generated in Dataverse = `true`.
- `VRMPURCHASEORDERCONFIRMATIONHEADERENTITY`: generated in Dataverse = `true`.
- `VRMPURCHASEORDERCONFIRMATIONLINEENTITY`: generated in Dataverse = `true`.
- `VRMPURCHASEORDERCONFIRMATIONWORKSPACE`: generated in Dataverse = `true`.

## What I found

- The retired all-stage workbook comparison was invalid because `po.xlsx` has no receipt or invoice stage value.
- P2 proves the candidate open population is complete when legal entity forms part of the PO key.
- P1 still blocks cutover because the enabled confirmation entity has no rows and 471 open POs lack dated stage evidence.
- P3 independently blocks cutover because only 3 of 61 maintained approval rows agree under R2.

## Problems and risks

- Calling an undated confirmed/open status `Sent to supplier` would violate P1.
- Treating pre-export receipts as progress after export would violate R2.
- Joining PO number without legal entity silently collapses reused order numbers across companies.

## Files changed

- Added isolated Correction 03 reconciliation, evidence and report generation.
- Updated the blocked project status and unpublished change note with the P4 number.

## Exact changes made

- Replaced the obsolete PO stage gate in the audit verdict with P1–P5.
- Added `STAGE_NOT_EVIDENCED`, composite PO identity, full exception lists and a 25-order sample.
- Carried accepted Correction 02 PR, amount, count and stale-lane evidence unchanged.

## What I did not change

- No dashboard, Race Control, snapshot, email or proxy runtime path was cut over.
- No workbook, generator, fallback or workflow was removed.
- No Dataverse or Azure resource was written. No function app or GitHub Pages site was deployed.
- Basit's morning email and Chandan's parallel chain remain untouched.
- Production primary `main` remained `a6adb057`; proxy `main` remained `3b930f44`.
- GitHub Pages remained built from `main`; no Correction 03 deployment run was triggered.

## Testing performed

- Python compile and machine-evidence assertions for P1–P5.
- Complete read-only PO reconciliation against both Dataverse organisations and the unchanged workbook.
- Existing dashboard JavaScript and weekly-snapshot regression tests.
- Desktop and 390 x 844 browser visual checks of the unpublished change note.
- Production Pages returned HTTP 200; the unchanged proxy returned 4,413 PR and 2,986 PO rows.
- Git diff and remote-branch verification; production remained unchanged.

## Commands recorded

- `python tests/reconcile_workbook_retirement_correction03.py --out evidence/workbook-retirement-correction-03.json` with short-lived Azure CLI tokens supplied only to the child process.
- `python tests/render_retirement_correction03.py evidence/workbook-retirement-reconciliation.json evidence/workbook-retirement-correction-01.json evidence/workbook-retirement-correction-02.json evidence/workbook-retirement-correction-03.json evidence/workbook-retirement-correction-03.md --notes NOTES.md`.
- `python -m py_compile tests/reconcile_workbook_retirement.py tests/reconcile_workbook_retirement_correction03.py tests/render_retirement_correction02.py tests/render_retirement_correction03.py tests/validate_retirement_correction03.py`.
- `python tests/validate_retirement_correction03.py`.
- `node --test tests/dataverse-live.test.js tests/race-control.test.js`.
- `python tests/test_weekly_snapshot.py`.
- `git diff --check`, scoped status/diff review, and remote ref verification.

## Assumptions

- The accepted Correction 02 gates stay settled as instructed and are not recalculated into a new verdict.
- R1 identity is legal entity plus purchase-order number because F&O reuses order numbers between companies.
- An empty enabled confirmation entity is not evidence of a confirmation event.

## Remaining risks

- P1 has 471 exact blockers and P3 has 58; retirement is prohibited.
- Production remains workbook-dependent and still depends on the morning email chain.

## Recommended next step

Expose a dated F&O PO confirmation event through an already-authorised read path and resolve the P3 historical approval discrepancies. Then rerun the same P1–P5 tests without weakening P1 or R2.

# Workbook retirement correction 04 — 7 September 2026

## Verdict

**Retire totally.** Correction 04 separates authoritative PO stage from its clock. P1a and P2 pass at 100%, every settled gate remains passed, the one-time seed is recorded, and the live dashboard/email revision is proven. Workbook runtime files, generators and workflows were removed only after the proxy production path returned the expected counts.

| Gate | 7 Sep verdict | Correction 01 | Correction 02 | Correction 03 | Correction 04 |
|---|---:|---:|---:|---:|---:|
| PR stage | 489/571 (85.64%) | 512/571 (89.67%) | 521/547 (95.25%) | 521/547 (95.25%) settled | 521/547 (95.25%) settled PASS |
| PR procurement clock | 541/564 (95.92%) | 540/564 (95.74%) | 496/509 (97.45%) | 496/509 (97.45%) settled | 496/509 (97.45%) settled PASS |
| PO stage | 430/1,493 (28.80%) | 653/1,495 (43.68%) | 309/702 (44.02%) | RETIRED | RETIRED |
| PO P1 / P1a | — | — | — | 512/983 dated (52.09%) FAIL | 983/983 authoritative stage (100.00%) PASS |
| PO P1b clock coverage | — | — | — | — | Report: 904 live-dated; 12 seeded; 0 first-observed baseline; 67 not recorded |
| PO P2 F&O population parity | — | — | — | 983/983 (100.00%) PASS | 983/983 (100.00%) PASS |
| PO P3 workbook approval parity | — | — | — | 3/61 (4.92%) FAIL | RETIRED |
| PO P4 LPO-sent distribution | — | — | — | 1,099 received or invoiced | 1,099 received or invoiced |
| PO P5 human sample | — | — | — | 25/25 complete | 25/25 carried and complete |
| PR amount | 819/4,394 (18.64%) | 3,560/4,394 (81.02%) | 556/566 (98.23%) | 556/566 (98.23%) settled | 556/566 (98.23%) settled PASS |
| PO amount | 85/2,977 (2.86%) | 2,923/2,977 (98.19%) | 707/714 (99.02%) | 707/714 (99.02%) settled | 707/714 (99.02%) settled PASS |
| Distinct documents | Exact | Exact | Exact | Exact | Exact PASS |

## P1a — authoritative PO stage

- Result: **PASS**, 983/983 open F&O purchase orders have a stage; `STAGE_NOT_EVIDENCED` = 0.
- Open-stage distribution: `Receipt posted` 504; `Sent to supplier` 389; `Not yet sent` 79; `Finance` 7; `Approval — unmapped element` 4.
- Stage is derived from each order's F&O status and approval status, posted packing slips, posted vendor invoices, or the current approval capture. Missing time never invalidates a known state.

## P1b — PO clocks, reported not gated

- Production after seed: 904 `LIVE_EVENT_DATE`; 12 `SEEDED_FROM_FINAL_WORKBOOK`; 0 baseline `PENDING_SINCE_FIRST_OBSERVED`; 67 `NOT_RECORDED`.
- Screen and email render `SEEDED_FROM_FINAL_WORKBOOK` as `since (from last export)`.
- `NOT_RECORDED` renders as `since — not recorded`; it never receives a fabricated date.
- `Stage event date and time` contains only a genuine F&O/capture event. Seed and first-observed values stay in `Step date and time` with their provenance.

### Final-workbook seeds

Every seed below records the workbook value and the export timestamp `2026-09-07T05:30:00Z`.

| Observation key | Stage | Seeded clock UTC | Flag |
|---|---|---|---|
| ifahr-live\|PO\|scbm\|P0000001160 | Not yet sent | 2025-10-31T11:21:31Z | SEEDED_FROM_FINAL_WORKBOOK |
| ifahr-live\|PO\|scbm\|SCBM-PO2600488 | Not yet sent | 2026-05-01T16:09:47Z | SEEDED_FROM_FINAL_WORKBOOK |
| ifahr-live\|PO\|scbm\|SCBM-PO2600638 | Not yet sent | 2026-04-17T16:24:45Z | SEEDED_FROM_FINAL_WORKBOOK |
| ifahr-live\|PO\|scbm\|SCBM-PO2600645 | Not yet sent | 2026-04-20T09:59:18Z | SEEDED_FROM_FINAL_WORKBOOK |
| ifahr-live\|PO\|scbm\|SCBM-PO2600651 | Not yet sent | 2026-04-20T15:02:15Z | SEEDED_FROM_FINAL_WORKBOOK |
| ifahr-live\|PO\|scbm\|SCBM-PO2600706 | Not yet sent | 2026-04-27T16:40:49Z | SEEDED_FROM_FINAL_WORKBOOK |
| ifahr-live\|PO\|scbm\|SCBM-PO2600713 | Not yet sent | 2026-04-28T16:17:53Z | SEEDED_FROM_FINAL_WORKBOOK |
| ifahr-live\|PO\|scbm\|SCBM-PO2600795 | Not yet sent | 2026-05-12T11:25:00Z | SEEDED_FROM_FINAL_WORKBOOK |
| ifahr-live\|PO\|scbm\|SCBM-PO2600813 | Not yet sent | 2026-05-15T16:14:49Z | SEEDED_FROM_FINAL_WORKBOOK |
| ifahr-live\|PO\|scbm\|SCBM-PO2601138 | Not yet sent | 2026-08-10T15:37:54Z | SEEDED_FROM_FINAL_WORKBOOK |
| ifahr-live\|PO\|scbm\|SCBM-PO2601516 | Not yet sent | 2026-08-25T12:28:50Z | SEEDED_FROM_FINAL_WORKBOOK |
| ifahr-live\|PO\|scbm\|SCBM-PO2601523 | Not yet sent | 2026-08-26T09:38:54Z | SEEDED_FROM_FINAL_WORKBOOK |

## Stage-observation proof

- A non-reportable proof row changed from `Sent to supplier` with no clock to `Receipt posted` at `2026-09-07T17:16:15Z`.
- Dataverse stored `PENDING_SINCE_FIRST_OBSERVED`, the same first-observed second, and `liveEvent = first observed after cutover`.
- Proof key: `ifahr-live|PO|proof|C04-STAGE-CHANGE-PROOF`; `ssg_isreportable = false`, so it cannot enter the dashboard population.
- Evidence: `evidence/workbook-retirement-stage-observation-live-proof.json`.

## Stale rows the workbook still carries

- Correction 04 carries R4 unchanged: **2,944 stale workbook rows**, including **829 PO rows**.
- The complete counted-once document list remains under the earlier same-named section and in `evidence/workbook-retirement-correction-02.md`; stale rows are not gates.

## Production same-revision and failure proof

- Pre-seed local proof: dashboard revision and email dry-run revision both `c96917d99719d6316aad038a82fdf57de012bffc1da9bf21e95e142b1b2a7cd3`; 4,413 PR headers, 3,188 PO headers, 983 open POs, 1,805 email open items; zero sends.
- Production proof after seed: proxy commit `1dfb69be2c58c458a40d6697f9268554547b3a4b`; dashboard and email dry-run both returned revision `cfff6fb83ee9e9ebc0a372bb91d3260281aa8a6afc93f883c8d977be7a3333e5`; source state `LIVE`; 4,413 PRs; 3,188 POs; 983 open POs; zero unevidenced stages; zero pending observation writes.
- The production email dry-run returned `sentAll = false`, two active division summaries and 19 personal summaries; no email was sent.
- Unit proof forces the loader to fail: a prior revision returns `sourceState = STALE`; with no last-good revision the same failure propagates. There is no workbook fallback.
- Browser cache is rendered immediately while refresh runs; stale state remains visibly labelled.

## Dataverse security and seed record

- Created development application user `2dae4ee2-dbaa-f111-aaac-7ced8dacd849` for the `ssg-prpo-proxy` user-assigned managed identity (`6435d989-1467-4cfb-a377-919011f03a94`).
- Assigned only `SSG PR PO Approval Capture Application` in the Shared Services business unit.
- Added organisation-level Create, Read, Write, Append and Append To on `ssg_PRPODocument` to that custom role; Delete was not added.
- No write occurred in `operations-ifahr-live`. No non-`ssg_` development table was written.
- Seed dry-run planned 983; apply wrote 983; post-seed verification found all 983 with exact stage/payload hashes and planned no new writes.

## What I found

- Correction 03's 471 failures were clock gaps, not unknown stages. F&O status makes all 983 open PO stages authoritative.
- The final workbook could seed 12 of the 79 missing current-stage clocks; 67 legitimately have no recorded time.
- The workbook's frozen PO labels are not a valid lifecycle gate. F&O shows **1,099** workbook-`LPO sent` orders as received or invoiced.

## Problems and risks

- The GitHub proxy deploy workflow lacks `AZURE_FUNCTIONAPP_PUBLISH_PROFILE_SSG_PRPO_PROXY`; run 34146527247 stopped before deployment. The authorised Azure Functions CLI deployment succeeded instead.
- The first production browser proof exposed a missing GitHub Pages CORS origin. Proxy commit `1dfb69b` added it while preserving Chandan's configured origin, and the corrected deployment passed the browser proof.
- 67 open POs initially show `since — not recorded`; their next observed stage change starts our own clock.
- The non-reportable proof row is retained because the approved role deliberately has no Delete permission.
- The package audit reports two moderate and one high transitive dependency advisory; no forced/breaking dependency upgrade was mixed into this cutover.

## Files changed

- Dashboard runtime now reads `/api/dataset`, shows cache/freshness/provenance, and uses current stages.
- Proxy now assembles one cross-company revision for dashboard, email and weekly snapshots.
- Final workbooks, overlay, generators, obsolete tests and four workbook workflows were deleted.

## Exact changes made

- Kept accepted PR capture/active-line pricing rules and active-line excl.-VAT amounts.
- Implemented P1a PO state independently from live-event, seeded and first-observed clocks.
- Added composite legal-entity/PO observation keys and development-only managed-identity writes.
- Kept posted packing-slip date as posting date, never delivery date.
- Kept P4's 1,099 business-case number in the screen/email change note.

## What I did not change

- No F&O or `operations-ifahr-live` row was written.
- No email sender, recipient, quiet-mode switch or scheduled morning send was changed or triggered.
- Chandan's parallel app, flow, OneDrive and tokens were not touched.
- Existing `weekly_snapshots.json` and `stuck_items.json` history remain; the proxy weekly job now reads the shared live revision.

## Testing performed

- Correction-04 reconciliation: P1a/P2 and settled-gate assertions passed against all F&O companies.
- Proxy syntax and nine focused stage/clock/cache/email/CORS tests passed.
- Dashboard data-client and Race Control tests passed; both HTML inline-script sets parse under Node `vm.Script`.
- Seed dry-run, apply and exact post-seed comparison passed.
- Production `/api/dataset`, `/api/pr`, `/api/po` and function-key email dry-run returned the same live revision/count model.
- The public Procurement division loaded 1,287 live items, explicit excl.-VAT values and all 12 seeded-clock labels with no stale/failure warning.
- Live development Dataverse stage-change proof passed.
- Post-removal search confirmed no runtime workbook URL, file, overlay generator or retired workflow remains.

## Commands recorded

- `python tests/reconcile_workbook_retirement_correction04.py --out evidence/workbook-retirement-correction-04.json`.
- `python tests/seed_final_workbook_po_clocks.py --evidence evidence/workbook-retirement-correction-04.json --out evidence/workbook-retirement-clock-seed-dry-run.json`.
- The same seed command with `--apply`, followed by a second read-only exact comparison.
- `node test/sameRevisionProof.js ...workbook-retirement-same-revision-preseed.json` and `node test/liveStageObservationProof.js ...workbook-retirement-stage-observation-live-proof.json`.
- `node --test test/prpoDataset.test.js` and `node --test tests/dataverse-live.test.js tests/race-control.test.js`.
- `func azure functionapp publish ssg-prpo-proxy --javascript` after the exact-SHA workflow stopped on its missing secret.
- Production GETs to `/api/dataset?refresh=1`, `/api/pr`, `/api/po` and `/api/prpo-email` without `send=1`.

## Assumptions

- The user explicitly settled Correction 02's PR, amount and distinct-count gates; they were carried, not reopened.
- The final-workbook export timestamp is `2026-09-07T05:30:00Z`, as used by the accepted correction evidence.
- Legal entity plus PO number is the stable observation identity because F&O reuses PO numbers across companies.

## Remaining risks

- The browser's first ever visit has no cached dataset; it shows the loading shell until the live function returns. Subsequent visits show cache immediately while refreshing.
- Historical three-day email cards show today only until new live weekly observations accumulate; daily email delivery itself is unchanged.
- Azure Functions still reports Node 20 runtime deprecation guidance; this cutover did not change the runtime stack.

## Recommended next step

Monitor the next scheduled morning email and first weekly live snapshot. Repair the missing GitHub publish-profile secret separately so future exact-SHA deployments use the repository workflow again.

# Urgent daily-email compatibility bridge — 2026-09-07

## Outcome

- Commit `31e5930d79559e0e9c05b52b8710ff2a54857d03` restored `pr.xlsx` and `po.xlsx` as one-way outputs of live revision `cfff6fb83ee9e9ebc0a372bb91d3260281aa8a6afc93f883c8d977be7a3333e5`.
- The commit was created at `2026-09-07T18:48:56Z`, more than eleven hours before the next `06:00 UTC` sender run.
- Pages deployment 34153150970 completed successfully at `2026-09-07T18:49:38Z` for that exact commit.
- Public verification returned HTTP 200 for both URLs. The downloaded files opened and parsed as valid Excel workbooks.
- Machine proof: `evidence/legacy-email-public-proof.json`.
- `pr.xlsx`: 822 rows, exactly 18 original columns, SHA-256 `42df2352c9c72945c04c5f523d6137b63d5aae84fab5413c178b35777a90f3c5`.
- `po.xlsx`: 983 rows, exactly 20 original columns, SHA-256 `5fc48c7b33f0ef011f526f784eece1a372852b8159c58a5b07b8d746ba8748ac`.
- Both files carry the cell note: `Generated from the live dataset for the legacy email app only; not a data source; delete when the sender moves to ssg-prpo-proxy.`

## Scheduled publication

- New workflow: `.github/workflows/publish-legacy-email-workbooks.yml`.
- Schedule: `*/15 4-5 * * 1-5`, meaning eight weekday attempts at 04:00, 04:15, 04:30, 04:45, 05:00, 05:15, 05:30 and 05:45 UTC, plus manual dispatch.
- The generator fails closed unless the shared proxy dataset says `sourceState = LIVE` and has a revision.
- A content sidecar prevents rewrites when the exported rows are unchanged. Changed outputs are committed, pushed and deployed directly to Pages so a `GITHUB_TOKEN` push cannot strand a new workbook behind a missing Pages rebuild.
- Manual-dispatch run 34153156222 succeeded at `2026-09-07T18:49:22Z` on `31e5930`; it read 822 PR rows and 983 PO rows from the live revision and correctly reported `contentChanged = false`, creating no empty commit.
- The retired OneDrive fetch, overlay generators and prior workflows remain removed. The only workflow in the primary repository is this new live-to-legacy output job.

## Workbook contract and mapping

- The exact pre-cutover schemas came from `bc65aca:pr.xlsx` and `bc65aca:po.xlsx`. Header spelling, order, `Sheet1`, `AxTable1`, number/date formats and original widths are preserved.
- The committed, commented translation table is in `scripts/legacy_email_stage_map.py`; the human-readable table and complete no-equivalent list are in `docs/legacy-email-workbook-bridge.md`.
- Sourcing and Priced have no exact old stage name. Both use old Procurement labels because that preserves the current pending owner and recipient document-for-document.
- Receipt posted uses `LPO sent/shared with supplier` plus legacy-compatible `Confirmed / Received`, the only frozen-code rule that lands the row in Pending Invoicing. It does not alter F&O or claim a delivery date.
- Open PO stage coverage is complete. An open `STAGE_NOT_EVIDENCED` or any unknown displayed stage aborts generation.
- Open PR rows with blank stage (59) or `Approval — unmapped element` (39) are excluded by the existing dashboard filter and reported as no-equivalent rows; they are not silently dropped from a displayed queue.

## Amount and date proof

- `Total amount` is copied from the settled live active-line amount excl. VAT. The change note now tells recipients that familiar totals will read about 5% lower than yesterday.
- PO clock coverage carried into the output is 904 live-event dates, 12 final-workbook seeds, zero first-observed baseline rows and 67 `NOT_RECORDED` blanks.
- `NOT_RECORDED` always writes a blank. No fallback date is generated. F&O date values, including its 1900 sentinel where supplied as a live event, remain source values rather than substituted dates.

## Frozen sender dry-run

- The last pre-cutover implementation `73fef6abc6e9610782c37097fc3e462148dd0c93:src/functions/prpoEmail.js` was executed locally in a sandbox with its timer and HTTP registrations stubbed.
- No send function or URL with `send=1` was invoked.
- Current live-dataset logic produced 1,805 items. The frozen logic parsed the generated workbooks and produced the same 1,805 items.
- Actual addressed channel membership was exact, document-for-document: zero differences across active named personal queues, Suppliers and Pending Invoicing.
- All 504 live Receipt-posted orders landed in Pending Invoicing; all 389 Sent-to-supplier orders landed in Suppliers.
- The 818 stage-label differences are the expected named crosswalk from consolidated Sourcing/Priced labels to the frozen vocabulary. Every document and reason is recorded in `evidence/legacy-email-parity.json`; there are zero unexplained recipient or list differences.
- The public workbook SHA-256 values exactly matched the locally dry-run bytes, so the published files are the files tested.

## No reverse dependency proof

- Primary search across `index.html`, `dataverse-live.js`, `divisions.html`, `race-control.js`, `tests` and `.github` found no `PRPO_PR_URL`, `PRPO_PO_URL`, `/pr.xlsx`, `/po.xlsx` or `fetchXlsx` reader.
- Proxy active code contains no fixed workbook URL. `loadItems()` in `src/functions/prpoEmail.js` calls `getDataset()`; the remaining parameterized `fetchXlsx` is an uncalled definition, and `historyItems()` returns an empty live-history object.
- Proxy `package.json` registers only `src/functions/*.js`. The old root `prpoEmail.js` is an inactive reference file and is not an Azure Functions entry point.
- The generator fetches `/api/dataset`; no workflow fetches either workbook back into the dashboard, current email, Race Control, weekly snapshot or a test.

## Mail.Send finding — read only

- `ssg-prpo-proxy` uses app registration client ID `780ac097-75e1-4cdb-a760-a032e8722a34` for its existing client-credential settings.
- Its service principal already holds Microsoft Graph `Mail.Send` as an **Application** permission (`b633e1c5-b582-4048-a93e-9f11b44c7e96`). No permission or Azure setting was changed.
- Therefore moving the sender does not require new Graph Mail.Send administrator consent.
- An Exchange application access policy covering `Racecontrol@striveservicesgroup.com` was not visible through the Azure AD app-role assignment available in this read-only session. That mailbox-policy detail remains unverified, not assumed.
- Evidence: `evidence/ssg-prpo-proxy-mail-send-finding.json`.

## Commands and checks

- `git restore --source=bc65aca -- pr.xlsx po.xlsx` to recover the exact reference schemas before replacing their content.
- `python scripts/generate_legacy_email_workbooks.py --evidence evidence/legacy-email-workbook-generation.json`.
- Local sandbox execution of `git show 73fef6a:src/functions/prpoEmail.js` against the generated files, send disabled.
- `node --test tests/dataverse-live.test.js tests/race-control.test.js`.
- Artifact-tool import, table inspection and rendered review of both generated sheets, followed by independent `openpyxl` reopen/header/table/note validation.
- `gh workflow run publish-legacy-email-workbooks.yml --ref main` and `gh run watch 34153156222 --exit-status`.
- Public HTTP downloads followed by workbook reopen and exact header/hash validation.

## Protected systems

- Chandan's function app, flow, OneDrive, tokens and mailbox were untouched.
- No email was sent. No recipient, sender, quiet-mode setting or timer in either function app was changed.
- `operations-ifahr-live` remained read-only. No Azure resource or setting was created or changed.
- The `ssg-prpo-proxy` repository and deployment were inspected read-only and not modified or redeployed.

## Remaining risk and removal condition

- GitHub scheduled workflows can start late, so eight attempts are intentional; the current files are already published before the first scheduled attempt.
- Delete both workbooks, the generator, mapping, sidecar and workflow as soon as production sending moves to `ssg-prpo-proxy`.

# Popup-window sign-in repair — 2026-09-08

## What I found

- `index.html` was the only page with an MSAL sign-in implementation. `divisions.html`, `journey-board.html` and `journey-live.html` contain no copied login code.
- `signIn()` always called `loginPopup()`, including when the dashboard itself was a popup. MSAL rejects that nested-popup request.
- The boot path called `handleRedirectPromise()` but discarded both its successful response and its failure.
- Azure app registration `8a4338bf-6c78-4a70-9c62-478bb19b171c` already has the exact SPA redirect URI `https://strive-services-group.github.io/PR-PO-Pipeline-Dashboard/`. No Entra change was needed or made.

## Exact changes made

- Commit `bd667e91f60d51fb1b4103142a1687f2c1891c41` keeps `loginPopup()` for an ordinary unnamed tab.
- Popup, named and standalone display-mode windows use `loginRedirect()` in the same window.
- A popup-related MSAL error automatically retries with `loginRedirect()` instead of exposing the library error.
- Successful popup and redirect responses share one completion path: set the active account, write `strive_auth` and `strive_user`, then call `enterDashboard()`.
- Interactive sign-in waits for the initial `handleRedirectPromise()` check to finish, preventing overlapping MSAL interactions.
- A cancelled or otherwise failed sign-in now uses plain English. The library-load and placeholder-config paths are unchanged.

## Production browser evidence

- GitHub Pages deployment `34187067482` completed successfully for `bd667e9` at `2026-09-08T04:28:24Z`.
- A normal Chrome browser tab completed sign-in and rendered the live dashboard. The live source badge and 1,805-item Race Control population loaded.
- A same-origin acceptance page opened the production dashboard with `window.open(..., 'popup=yes,width=1200,height=800')`. The chromeless child used redirect sign-in, returned to the registered Pages URI, hid the login overlay and loaded the live dashboard.
- The acceptance page observed the returned child DOM and reported: `PASS: popup returned signed in and rendered the dashboard.`
- The temporary acceptance page was removed immediately after this proof and is not part of the final production surface.

![Chrome popup sign-in proof](evidence/popup-sign-in-proof.jpg)

## Testing performed

- `node --test tests/auth-flow.test.js tests/dataverse-live.test.js tests/race-control.test.js`: 9/9 passed.
- Auth tests cover popup detection, named/standalone windows, unchanged normal-tab popup completion, popup-error fallback, redirect-return completion, cancellation wording and redirect-handler ordering.
- Both inline scripts in `index.html` parsed under `vm.Script`.
- Existing live-dataset and Race Control tests passed. The staged diff contains no dashboard data, figure, label, bucket, email or workbook code change.
- Microsoft documents `handleRedirectPromise()` as mandatory for redirect responses and lists `popup_window_error`, `block_nested_popups` and `block_iframe_reload` as browser error codes; the implementation follows those contracts.

## What I did not change

- MSAL client ID, tenant, scopes, redirect URI and cache configuration.
- Dashboard data, Race Control, figures, labels, buckets, emails or the legacy workbook publisher.
- `ssg-prpo-proxy`, Azure resources and the Entra app registration.
- Login visuals or the separate approved overlay redesign.

## Remaining risks

- The browser cannot reliably expose whether a tab strip is visible. The proactive check therefore uses opener, window name and standalone display mode; the error fallback covers other chromeless cases MSAL identifies at runtime.
- Chrome automation could not directly drive a separate popup window, so the temporary same-origin acceptance page invoked the popup's existing SIGN IN button and independently observed the hidden overlay after the redirect return. No authentication dialog, credential or token was automated or recorded.

# Lights-out sign-in redesign — 2026-09-08

## What I found

- The named OneDrive task folder was not a Git checkout. Work was performed from a fresh canonical clone of `Strive-Services-Group/PR-PO-Pipeline-Dashboard` at `C:\Claude\PR-PO-Pipeline-Dashboard`.
- The approved specification was `SIGNIN_DESIGN_race-control-signin.html`, SHA-256 `A7D8BCB4306ABDF78EE842B2AAE37234A3161F40F5A58D6DA2F09DA2E31FDD5F`.
- `index.html` was the only page containing sign-in markup and MSAL logic. The popup/redirect repair from `bd667e9` was present on current `main` and covered by `tests/auth-flow.test.js`.
- The approved preview's unconstrained full-resolution canvas measured about 20 fps at 1920 × 1080 in Chrome. Repeated crowd geometry, light pools, blur and full-size drawing were the main avoidable per-frame costs.

## Exact changes made

- Replaced the static grid/card and falling-lines overlay with the approved night pit-straight canvas, five stage gantries, lights sequence, sector chips, car, checkered finish, Dubai clock and right-side access panel.
- Kept `#loginOverlay`, `#loginUser`, `#loginErr` and direct `signIn()` wiring. The button is enabled and visible from the first frame; the sequence never gates authentication.
- Preserved the existing MSAL client ID, tenant, scopes, cache, popup/redirect selection, popup-error fallback and redirect-return completion logic.
- Added a self-contained `signin-lights-out.js` lifecycle. Rendering is paused in a background tab, permanently stopped when the overlay closes, and not initialized for an already-authenticated session.
- Capped canvas DPR at 2 and capped the backing canvas at 500,000 pixels independent of device DPR. Slow devices retain every timed light state but automatically pause continuous drawing after two frames over budget.
- Deferred Plotly, jQuery, DataTables, XLSX, html2canvas, jsPDF, Font Awesome, Dataverse and Race Control assets until authentication. Signed-out dashboard layout is also suppressed beneath the overlay.
- Reduced-motion users get all five green sectors, the permanent `Lights out` callout and `Lights out · Sign in` button immediately, with no animation frame.
- Added the exact Dubai Race / Session / Lap calculation from the approved design and stopped its one-second clock with the overlay.
- Added a 899 px stacked breakpoint and compact 390 px panel while keeping the sign-in action in the initial mobile viewport.
- Added Montserrat and Titillium Web through Google Fonts with `display=swap` plus metric-adjusted local fallbacks.
- Inlined the exact geometry from repository `strive-logo.svg`; only the approved night-livery fills are applied by scoped CSS.

## Strive brand tokens applied

- Steel blue `#618FB4`.
- Deep ocean blue `#145A95`.
- Slate blue `#1F466B`.
- White/night text `#EEF4FA` and `#FFFFFF`.
- Montserrat body stack and Titillium Web race-label stack, with the existing dashboard typography unchanged.

## Files changed

- `index.html` — overlay markup, scoped styles, font loading and animation shutdown hook.
- `signin-lights-out.js` — canvas scene, sequence, clock and lifecycle.
- `tests/signin-lights-out.test.js` — overlay, logo, timing, reduced-motion and lifecycle checks.
- `evidence/signin-lights-out-desktop.png` — Chrome 1440 × 860 evidence.
- `evidence/signin-lights-out-mobile.png` — Chrome 390 × 844 evidence.
- `NOTES.md` — implementation and verification record.

## Visual evidence

![Lights-out sign-in at 1440 by 860](evidence/signin-lights-out-desktop.png)

![Lights-out sign-in at 390 by 844](evidence/signin-lights-out-mobile.png)

## Testing performed before publication

- `node --check signin-lights-out.js` passed.
- Both inline `index.html` scripts parsed under Node `vm.Script`.
- `node --test tests/auth-flow.test.js tests/signin-lights-out.test.js tests/dataverse-live.test.js tests/race-control.test.js`: 16/16 passed.
- Auth regression criteria 1–3 remain covered: popup/named/standalone windows choose redirect; normal tabs keep popup; redirect return restores the same session and enters the dashboard.
- The exact `user_cancelled` MSAL error maps to `Sign-in was cancelled. Please try again.`; Chrome confirmed the error line renders inside the new mobile panel. A live-provider cancellation was not automated because credentials and authentication dialogs remain user-controlled.
- Isolated Headless Chrome 152 at an exact CDP 1920 × 1080 viewport measured 151 animation frames over 2,509.8 ms: 60.164 fps. The button was visible, continuous animation remained active, adaptive fallback was not triggered and canvas DPR was 0.491.
- Chrome reduced-motion emulation showed `Lights out · Sign in`, five completed sectors, no active animation frame and an active Dubai clock.
- A simulated authenticated session hid the overlay, removed the body scroll lock, initialized Race Control and created no lights-out scene object or recurring work.
- Chrome verified the 1440 × 860 and 390 × 844 layouts visually. Both evidence PNGs were reopened and checked at their exact dimensions.

## What I did not change

- No MSAL configuration, token handling, redirect URI, session keys or sign-out logic.
- No dashboard data, Dataverse read, Race Control figure, label, bucket, filter, email or workbook logic.
- No Azure resource, Entra registration or function app.
- No page other than `index.html`; the other HTML pages have no copied sign-in implementation.

## Production publication and verification

- Feature commits `ab210c2`, `4a921b5` and `465a65c` were pushed to `feature/lights-out-signin`, then merged to `main` as authorised. Final implementation merge is `23739695d5fe6821184829bea2fb2b33a5e6c8ed`.
- GitHub Pages deployment `34191024101` completed successfully for that exact final implementation merge.
- The deployed `index.html` and `signin-lights-out.js` returned HTTP 200. A fresh signed-out Chrome tab showed the five-stage race scene, Dubai race/session/lap chip, working sequence and enabled Microsoft sign-in action.
- Official PageSpeed Insights captured the final production URL at 9:33 AM Dubai time with Lighthouse 13.4.1. Desktop Performance scored **97**: FCP 0.8 s, LCP 0.8 s, TBT 30 ms, CLS 0.008 and Speed Index 1.5 s.
- The first deployed desktop audit scored 38 and exposed eager dashboard libraries plus unconstrained canvas work. Those two measured causes were corrected before the final 97 result; no package was installed.
- Live authentication dialogs and credentials were not automated. Successful dashboard entry was regression-checked with the existing authenticated session path: the overlay closed, all deferred assets loaded, Race Control initialized and no sign-in scene or recurring scene work was created.
- Final desktop evidence is 1440 × 860, SHA-256 `404C8970DA0B26DE718BDC1FC142B24A17C5B81DC03238B55CEC8DDBCC4351DB`. Final mobile evidence is 390 × 844, SHA-256 `2910C1886E5FDA8935D296A7CF98BDA2DF392989A12B0952609AEB95C82E3DBF`.

# Lights-out sign-in correction 02 — real SSG car — 2026-09-08

## What I found

- `main` now contains the seven authorised transparent car assets from commit `4da6a4e`. Their dimensions, RGBA channels, alpha transparency, byte counts and Git tracking status were checked before use.
- The live scene still used the vector `drawCar()` implementation, a DOM callout for `1 LIGHT` through `5 LIGHTS`, and a canvas backing-store cap of 500,000 pixels. Those three items were the correction's confirmed faults.
- The authentication source remains the implementation from `bd667e9`: normal windows use `loginPopup()`, popup/named/standalone windows use `loginRedirect()`, popup-related failures fall back to redirect, and `authGate()` awaits `handleRedirectPromise()`.

## Problems and risks

- A real transparent render can read as a sticker unless its road contact, scene lighting and reflection are tied to the track projection.
- Loading the selected image after animation starts would produce a visible pop. The sequence therefore starts only after image load and decode complete; the sign-in control remains immediately usable in the DOM.
- Native DPR removes the earlier performance safety cap. The full scene had to be measured at the required 1920 × 1080 rather than assumed safe.

## Files changed

- `signin-lights-out.js` — real-car loading and rendering, five start lights, native-DPR lifecycle.
- `index.html` — removed the obsolete countdown callout markup and scoped CSS only.
- `tests/signin-lights-out.test.js` — updated lifecycle assertions and added correction regressions.
- `evidence/signin-correction-02/measure-performance.js` — reproducible Chrome DevTools measurement harness.
- `evidence/signin-correction-02/*.jpg` — required desktop and HiDPI visual evidence.
- `NOTES.md` — this implementation, verification and deployment record.

## Exact changes made

- Deleted `drawCar()` and every caller. The scene selects `car-rear-700.webp`, `car-rear-1100.webp` or `car-rear-1600.webp` from CSS width and physical pixel width, with `car-rear-1100.png` as the decode/load fallback.
- The selected car is loaded and decoded before `resize()`, the clock and the first animation sequence begin. A one-time offscreen texture adds restrained Strive-blue floodlight colour without per-frame image processing.
- The real rear render is sized through the existing perspective projection. Its wheel line meets the road plane, with a soft elliptical contact shadow, faint compressed asphalt reflection, subtle floodlight pool and low-cost heat trails after launch.
- Replaced the word callout with five separate dark lamp housings on the first overhead gantry. Each red lens fills left-to-right, the fifth holds for 650–1,050 ms, all five extinguish together, and acceleration starts on release.
- Removed `loginCallout`, `say()`, `Lap complete`, all numeric light wording and the unused callout CSS. The allowed stage labels, chips, sign-in panel and button wording remain.
- Canvas DPR is now the actual `window.devicePixelRatio`. Backing dimensions are rounded `clientWidth × DPR` and `clientHeight × DPR`; the transform and high-quality image smoothing are reapplied on resize and a resolution-media-query watcher handles DPR changes.
- Removed the adaptive low-resolution/animation-stop fallback because it violated native sharpness and the required sustained sequence. Visibility pausing, permanent shutdown and reduced motion are unchanged.

## Strive brand-system influence

- The authorised SSG livery render is used without redrawing or altering its logo geometry.
- Scene lighting uses the existing Strive steel blue `#618FB4`, deep blue `#145A95` and restrained white highlight; the approved sign-in panel, typography and wording were not restyled.

## Visual evidence

![Correction 02 at 1920 by 1080](evidence/signin-correction-02/signin-1920x1080.jpg)

![Correction 02 at 1366 by 768](evidence/signin-correction-02/signin-1366x768.jpg)

![Correction 02 at 1440 by 900 and DPR 2](evidence/signin-correction-02/signin-hidpi-1440x900@2x.jpg)

- 1920 × 1080 screenshot: 251,964 bytes, SHA-256 `78A6D149D711C808BE9097099303018F0DE7A1A6C01D2F3444E46E435462970C`.
- 1366 × 768 screenshot: 170,429 bytes, SHA-256 `2917655DEDBEB5A25660CD804271FD449D77CFA4933D59C1270DF650A9E085E6`.
- HiDPI screenshot: CSS 1440 × 900 at DPR 2, 2,880 × 1,800 pixels, 497,847 bytes, SHA-256 `FCE1EBDA52A506A44F6DDA4AFF64661010DF2D6F92A0F382D344F1E868E6F998`.
- All three were reopened at original resolution and visually inspected. The car reads as the SSG photographic render, the tires meet the asphalt, the soft shadow/reflection ground it, and no countdown words appear.

## Testing performed before publication

- `node --check signin-lights-out.js` passed.
- The one inline script in `index.html` parsed under Node `vm.Script`.
- `node --test tests/auth-flow.test.js tests/signin-lights-out.test.js tests/dataverse-live.test.js tests/race-control.test.js`: 19/19 passed.
- Auth regression tests passed all seven popup, normal-window, redirect-return, cancellation and redirect-handler-order cases without changing auth code.
- At an exact foreground CDP viewport of 1920 × 1080 and DPR 1, canvas CSS/backing dimensions were `1920 × 1080` / `1920 × 1080`.
- After resize to 1366 × 768 and DPR 1, dimensions were `1366 × 768` / `1366 × 768`.
- After DPR change to 2 at CSS 1440 × 900, dimensions were `1440 × 900` / `2880 × 1800`.
- The full seven-second start sequence recorded 420 frames over 7,000.1 ms: 59.999 fps, 16.7 ms median, 16.9 ms p95, 17.6 ms maximum, and zero frames above 20 ms. `document.hidden` was false throughout the foreground measurement.
- Runtime text inspection returned no element whose text matched `1 LIGHT` through `5 LIGHTS`.
- Reduced-motion emulation produced the immediate final state: no animation frame, five completed sector chips, active clock and `Lights out · Sign in` button.
- Chrome lifecycle freezing emitted a hidden visibility event with both `frameActive: false` and `clockActive: false`, confirming background pausing remains effective.
- A fresh 1366 × 768 load selected `assets/car/car-rear-1100.webp`; the 1920 and HiDPI loads selected `car-rear-1600.webp`. Code and tests cover the ≤720 px `car-rear-700.webp` selection.
- This is a static GitHub Pages application with no `package.json` or production build command. The JavaScript syntax, inline-script parse and full repository test suite are the available build-equivalent checks.
- The seven repository car files total 853,258 bytes. Largest is the existing 452,844-byte PNG fallback; selected WebP transfer is 37,184, 70,534 or 118,258 bytes. No new car image or source render was added.

## What I did not change

- No MSAL client, tenant, scopes, redirect URI, popup detection, redirect fallback, session key, token or sign-out code.
- No clock, Dubai Race / Session / Lap formula, sector-strip structure, session target, eyebrow, panel copy or panel layout.
- No dashboard data, Dataverse, Race Control, email, workbook, workflow or GitHub Actions file.
- No car source render outside the repository and no image over 1 MB was added.

## Remaining risks

- Real Microsoft credentials and authentication dialogs are intentionally not automated. Deployed verification therefore uses the existing successful real-browser proof plus live-provider launch/return checks that do not capture credentials or tokens.
- WebP decode failure uses the 452,844-byte PNG fallback; this path is code- and unit-verified but was not forced in the production browser because current Chrome supports WebP.

## Recommended next step

- Keep the current car scale and lighting unless CEO review identifies a specific visual adjustment; the measured native-DPR version has sufficient performance headroom.

## Production publication and verification

- Feature commit `27a2aa2f717bb517be4dc35f1329c3435157c20b` was pushed to `feature/signin-real-ssg-car`, fast-forward merged to `main` under the granted authority, and confirmed byte-for-byte at `origin/main`.
- GitHub Pages run `34203961970` completed successfully for implementation commit `27a2aa2` (build 32 seconds, deploy 11 seconds).
- Production `index.html`, `signin-lights-out.js` and `assets/car/car-rear-1600.webp` returned HTTP 200. Git blob checks proved the deployed HTML (`466b2dec…`) and scene script (`8272e809…`) exactly match the committed files.
- A fresh signed-out Chrome tab on the production HTTPS URL displayed the real SSG rear car, native five-lamp gantry, live Dubai clock, `Race 9 · Session 2 · Lap 8`, sector chips and enabled Microsoft sign-in button. DOM inspection found zero numeric light-count words.
- The production normal-window sign-in completed through the live Microsoft provider using the existing SSO session. The overlay closed, the dashboard rendered, sign-out appeared and live F&O loading began; no credential, token or authentication dialog was read or automated.
- Current deployed popup/redirect code is byte-identical to the locally tested source and the protected `bd667e9` implementation. All seven deployed-source auth regression cases pass. The earlier same-day production popup proof recorded above remains valid because this correction changed no auth line.
- Browser security policy blocked creating a new synthetic `data:` opener for an additional popup round trip, and prohibited an indirect workaround. This does not change the result: a real production popup round trip was already proven after `bd667e9`, the implementation is unchanged, the current deployed file hash matches, and the current normal-window round trip completed.
