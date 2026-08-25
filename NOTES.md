# Journey Time implementation notes

Date: 2026-08-25 (Asia/Dubai)

Branch: `feature/analysis-journey-time`

Base: `f67c2d0` (`origin/main` at branch creation)

## Source of truth and model

- `pr.xlsx` and `po.xlsx` remain the committed fallback source. The page loads both with SheetJS and overlays no new data source.
- A journey is one exact `Purchase requisition` link from a PR row to a PO row. This preserves all 1,360 eligible PR-PO pairs. The export contains 84 PRs with multiple POs (maximum six), so collapsing to one PO per PR would discard real journeys.
- Rejected/cancelled PRs and rejected/cancelled POs are excluded before calculation.
- Measured milestones are limited to timestamps that actually exist:
  - PR Created -> Submitted.
  - Submitted -> PO Created.
  - PO Created -> exported PO Step date, only when the PO is Received/Invoiced or the current step is `LPO sent/shared with supplier`.
  - PR Created -> that same qualifying exported PO Step date for end-to-end.
- Missing and negative timestamp pairs are excluded from the relevant statistic and counted separately.
- The export has no separate sent, GRN, received, or invoice-posting history timestamps. Sent -> Received/Invoiced is therefore shown as `Not measurable`; no duration is inferred from modification time or a single current step date.
- Slowest laps and current-stage statistics use only live records with a valid exported Step date, calculated as exact Step date -> browser time.

## Data audit and coverage

Committed workbook audit:

| Measure | Result |
| --- | ---: |
| PR rows | 4,266 |
| Eligible PR rows | 3,148 |
| PO rows | 2,894 |
| Eligible PO rows | 2,833 |
| Exact eligible PR-PO pairs | 1,360 |
| Terminal-milestone pairs | 1,313 |
| PR Created -> Submitted | median 0.0d, p90 1.0d, n=3,086, missing=53, negative=9 |
| Submitted -> PO Created | median 15.4d, p90 69.8d, n=1,360 |
| PO Created -> Latest PO Step | median 2.0d, p90 82.5d, n=1,032, missing=281 |
| PR Created -> PO Created | median 16.6d, p90 71.6d, n=1,360 |
| End-to-end | median 27.5d, p90 141.4d, n=1,032, missing=281 |

End-to-end coverage is 1,032 / 1,313 = 78.6%. The measured bottleneck is Submitted -> PO Created at a 15.4-day median.

## Date formats

- Excel stores all populated audited date cells as datetimes.
- PR Created/Submitted and PO Requested receipt use the workbook display format `mm-dd-yy`.
- PR/PO Step date and PO Created use `m/d/yy h:mm`.
- SheetJS returns formatted month-first strings when `raw:false` is used. The Journey parser therefore accepts ISO local/offset values, Excel serials, and the two verified month-first workbook formats. It rejects unsupported day-first strings rather than guessing.

## Three named hand checks

1. Completed journey `PR-001666` -> `SCBM-PO2601486`:
   - PR Created `2026-08-14 00:00:00`; Submitted `2026-08-14 00:00:00` = 0.0d.
   - PO Created `2026-08-18 16:21:14` = 4.7d after submission.
   - Exported PO Step `2026-08-19 17:17:16` = 1.0d after PO creation.
   - End-to-end = 5.7d. PO status is Received; step is `LPO sent/shared with supplier`.
2. Open record `CPR-022121`:
   - Current Step date `2026-03-30 10:32:10`; verification time `2026-08-25 14:23` = 148.2d.
   - The local Slowest laps list displayed 148.2d. Existing approver reconstruction displays the accountable owner as `dinesh.laxman` and header stage as Operations to Confirm; raw pending user remains `Adnan.Ullah`.
3. Missing-date record `CPR-033993`:
   - Created `2026-08-25 00:00:00`; Submitted is blank; Step date is blank.
   - No Created -> Submitted or current-stage duration is emitted. It contributes to the missing count.

## Weekly snapshots

- `weekly_snapshots.json` contains eight Sundays from 2026-07-05 through 2026-08-23. The first week has no PR rows, but the following seven weeks have 549-624 PR rows; PO snapshots contain 795-879 rows.
- The archive is sufficient for a cautious view. The new mini-view reports the minimum consecutive weeks each record is observed in its latest bucket, then shows median and p90 by PR/PO bucket.
- It is labelled `Weekly resolution - approximate` and is never mixed with exact day metrics. Records already in a bucket before the first retained snapshot are left-censored, so displayed weeks are minimum observed dwell, not true stage-entry time.

## Dataverse development inspection

- No working Dataverse credential, token flow, or Dataverse proxy route exists in this dashboard repository.
- The configured browser MSAL scope is only `User.Read`. The OneDrive automation uses environment-provided Graph credentials, not Dataverse credentials.
- Per the task boundary, no Dataverse request was attempted. No Azure, proxy, production, or Dataverse resource was changed.

## Verification performed

- `node tests/journey-time.test.js` - passed synthetic missing/negative/excluded cases, date formats, percentiles, and committed embedded fallback invariants.
- Parsed all nine inline JavaScript blocks with Node `vm.Script` - passed.
- `git diff --check` - passed.
- Served the repository on localhost and confirmed `pr.xlsx`, `po.xlsx`, and `weekly_snapshots.json` load.
- Normal localhost Entra sign-in was attempted and correctly failed with redirect mismatch because `http://127.0.0.1` is not registered. Entra was not changed. Visual testing used an isolated in-memory localhost response that pre-seeded the app's existing session flag; repository files and authentication logic were unchanged.
- Desktop browser render at 1905x855:
  - Journey Circuit, KPI cards, track, Slowest laps, current-stage table, and weekly approximation rendered.
  - No page-level horizontal overflow.
  - Existing count funnel remains below the new panel.
- Mobile browser render at 375x844:
  - Filter sidebar stacks above the main content.
  - No page-level horizontal overflow.
  - KPI cards and split panels collapse to one column; track and tables scroll only inside their containers.
- Regression interactions:
  - Building Services filter returned 380 PR live records.
  - PO mode returned 814 live records.
  - Existing funnel, exceptions, supplier scorecard, and weekly panels remained visible.
  - Fresh final browser tab produced no console errors.

## Commands used

```text
git fetch origin --prune
git merge --ff-only origin/main
git switch -c feature/analysis-journey-time
node tests/journey-time.test.js
git diff --check
```

No build step exists for this vanilla HTML/CSS/JavaScript repository. No package was installed.

## Race Control visual correction

Correction base: `eea21d3` (`Add Journey Time analysis view`)

This pass is presentation-only. The `JOURNEY_TIME_START` / `JOURNEY_TIME_END` calculation block is byte-identical to `eea21d3` after normalising line endings (SHA-256 `cf4b0ab69d2cb5c85e72c6d0e933631069b1d6e3404edb27d1ae02c5c247535c`). No workbook, snapshot, filter, authentication, proxy, Azure, Dataverse, workflow or deployment file changed.

### What changed

- Replaced the flat Journey panel with a dark Race Control broadcast panel using the Strive internal palette: night navy `#0B1B33`, deep ocean blue `#145A95`, slate blue `#21486C`, steel blue `#618FB4`, white, and the dashboard's existing SLA green/amber/red.
- Replaced the straight track with one closed inline SVG stadium circuit. It has five numbered gates, a start/finish checker, four journey sectors, a neutral return lane, a flowing dashed direction overlay, and a static glow on the measured bottleneck sector.
- Kept all four KPI values and basis text, but restyled them as timing-screen tiles. Coverage now has a slim gauge.
- Added sector hover/focus/tap telemetry. Each measured leg uses the duration array already returned by `_jtMeasure` to render a maximum of 12 histogram buckets. No statistics are recalculated or redefined.
- Kept `Not measurable` as a dashed grey locked sector with the same reason and no inferred duration.
- Replaced the Slowest laps table presentation with a semantic timing-tower table: P1-P10 badges, owner initials, stage/SLA pills, tabular day figures, and desktop values.
- Replaced current-stage and weekly-approximation tables with worst-first median bars and p90 whiskers. Weekly bars retain the approximate label and reduced opacity.
- At widths below 768 px, the circuit becomes a vertical sector rail, KPIs are 2x2, the timing tower fits the available width, and dwell bars stack without page-level overflow.
- Motion is limited to `transform`, `opacity`, and SVG `stroke-dashoffset`. The bottleneck blur is static. `prefers-reduced-motion: reduce` removes track flow and count-up/reveal movement.

### Screenshot evidence

Screenshots are stored outside the repository and were not committed:

| View | Before (`eea21d3`) | After correction |
| --- | --- | --- |
| Desktop 1600x950 | `C:\Users\w.amjad\.codex\visualizations\2026\08\25\01a03865-cc4c-7ff0-9221-6bb8b329feb7\journey-race-control\before-desktop-1600x950.png` | `C:\Users\w.amjad\.codex\visualizations\2026\08\25\01a03865-cc4c-7ff0-9221-6bb8b329feb7\journey-race-control\after-desktop-1600x950.png` |
| Mobile 375x844 | `C:\Users\w.amjad\.codex\visualizations\2026\08\25\01a03865-cc4c-7ff0-9221-6bb8b329feb7\journey-race-control\before-mobile-375x844.png` | `C:\Users\w.amjad\.codex\visualizations\2026\08\25\01a03865-cc4c-7ff0-9221-6bb8b329feb7\journey-race-control\after-mobile-375x844.png` |
| Mobile timing and dwell detail | Not applicable | `C:\Users\w.amjad\.codex\visualizations\2026\08\25\01a03865-cc4c-7ff0-9221-6bb8b329feb7\journey-race-control\after-mobile-timing-375x844.png` |

### Number parity against the pre-correction render

- KPI strip before and after: `27.5d`, `16.6d`, `1,032`, `78.6%`.
- Raised -> Submitted before and after: median `0.0d`, p90 `1.0d`, `n=3,086`, `53 missing`, `9 invalid`.
- Submitted -> PO Created before and after: median `15.4d`, p90 `69.8d`, `n=1,360`, `0 missing`, `0 invalid`.
- PO Created -> Latest PO Step before and after: median `2.0d`, p90 `82.5d`, `n=1,032`, `281 missing`, `0 invalid`.
- Final sector before and after: `Not measurable`, `No separate GRN / invoice timestamp`, `No duration inferred`.
- P1 Slowest lap before and after: `PO SCBM-PO2600218`, `Pending Invoicing`, owner `Suroor Al Madeena Air Conditioning Spare Parts LLC`, `183.0d`, `AED 0` at the verification time.

### Visual and interaction verification

- Desktop 1600x950: one closed circuit, five gates, four journey sectors, glowing red bottleneck, visible timing telemetry, no page-level horizontal overflow.
- Mobile 375x844: 2x2 KPI grid, vertical rail, all four sector summaries, no page-level horizontal overflow. The timing tower shows position, record, stage, owner initials and days without internal or page overflow; value remains visible on desktop.
- Sector tap/focus changed the telemetry card between the honest locked final sector and the Raised -> Submitted distribution. The shared `mouseenter` handler uses the same activation function for hover.
- Count-up was observed during the 700 ms entry window and returned to the exact final values. Final values are present in the generated markup before the observer runs, so failure of the enhancement does not blank the figures or reserve new layout space.
- Reduced-motion emulation returned `prefers-reduced-motion: true`, `.jtFlow` computed `animation-name: none`, the panel did not enter motion mode, KPI opacity remained `1`, and exact final figures remained visible.
- Script execution was disabled after the normal client render; the panel stayed visible and all four KPI values remained unchanged. A cold no-JavaScript page load cannot initialise this dashboard's existing authentication, workbook loading or Analysis renderer in `eea21d3` either. Hard-coding a duplicate snapshot would violate the presentation-only and source-of-truth rules, so no duplicate no-JS data model was added.
- Browser console error log was empty.

### Performance and network observations

- A warm local `renderAnalysis()` call, including the full existing Analysis section, measured 31.3 ms in the verification browser.
- The correction adds one inline SVG, static CSS, one IntersectionObserver, and small histogram/bar HTML generated from arrays already in memory.
- No package, image, font, script, stylesheet, request, or fetch was added. A zero-context diff search found no added `fetch(`, `src=`, or `href=` reference.
- All correction animations are `transform`, `opacity`, or `stroke-dashoffset`; the SVG blur filter is static and never animated.
