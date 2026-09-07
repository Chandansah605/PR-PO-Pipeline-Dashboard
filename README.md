# PR / PO Pipeline Dashboard

Live dashboard for Strive Services Group showing the purchase requisition (PR) and purchase order (PO) pipeline from D365 Finance & Operations.

**Live site:** https://strive-services-group.github.io/PR-PO-Pipeline-Dashboard/ (sign in with your Microsoft work account)

## Workbook retirement status

Correction 04 separates PO stage from its clock. P1a and P2 pass at 100%, so the dashboard now reads one shared live revision from the proxy. The final workbook seeded otherwise unavailable clocks once; every seed remains visibly labelled `since (from last export)`. The workbook still showed 1,099 orders as merely sent although F&O showed them received or invoiced.

`pr.xlsx` and `po.xlsx` are generated from that live revision for the legacy email app only. They are not data sources and must be deleted when the sender moves to `ssg-prpo-proxy`.

## This is one of two repos (same project)
| Repo | Purpose | Deploys to |
|---|---|---|
| **PR-PO-Pipeline-Dashboard** (this repo) | The dashboard website (HTML/JS) | GitHub Pages |
| **pr-po-proxy** | Small Azure Function that reads D365 over OData and returns JSON the dashboard uses | Azure Functions |

They're kept separate because they deploy to different places. The dashboard calls the proxy for live data.

## How the data flows
1. On sign-in, the dashboard calls the proxy `/api/dataset` for one shared live revision.
2. F&O supplies headers, active lines and PO lifecycle state; the development `ssg_` capture supplies approval assignments and first-observed PO stage clocks.
3. Browser cache is shown while a newer revision refreshes. A stale revision is labelled; no workbook fallback exists.
4. A one-way scheduled compatibility job publishes `pr.xlsx` and `po.xlsx`; no dashboard or current email path reads them.

## Key files
- `index.html` — the entire dashboard (UI + data loading + charts).
- `dataverse-live.js` — shared live-dataset client and stale-cache handling.
- `evidence/workbook-retirement-correction-04.json` — final gate evidence.
- `msal-browser.min.js` — Microsoft sign-in library (self-hosted).
- `LIVE-INTEGRATION-PLAN.md` — background on the live integration.

## To edit / publish
Edit files (GitHub web pencil for small changes, or GitHub Desktop for full edits) → **Commit** → **Push**. GitHub Pages republishes automatically in ~1 minute.

## Retirement gate

The correction-04 cutover passed. PR stages, amounts and counts remain settled; PO P1a/P2 are 100%. P1b is reported, not gated. Never display a seeded or missing clock as a live event date.
