# PR / PO Pipeline Dashboard

Live dashboard for Strive Services Group showing the purchase requisition (PR) and purchase order (PO) pipeline from D365 Finance & Operations.

**Live site:** https://strive-services-group.github.io/PR-PO-Pipeline-Dashboard/ (sign in with your Microsoft work account)

## Workbook retirement status

Correction 03 retires the invalid all-stage PO workbook gate and tests dated stage evidence, F&O population parity and the approval rows the workbook maintains. The verdict remains **cannot retire**: P2 passes at 983/983, but P1 is 512/983 (52.09%) and P3 is 3/61 (4.92%). The workbook still shows 1,099 orders as merely sent although F&O shows them received or invoiced. The workbook overlay, jobs, fallback and daily emails remain in production. See `evidence/workbook-retirement-correction-03.md`.

## This is one of two repos (same project)
| Repo | Purpose | Deploys to |
|---|---|---|
| **PR-PO-Pipeline-Dashboard** (this repo) | The dashboard website (HTML/JS) | GitHub Pages |
| **pr-po-proxy** | Small Azure Function that reads D365 over OData and returns JSON the dashboard uses | Azure Functions |

They're kept separate because they deploy to different places. The dashboard calls the proxy for live data.

## How the data flows
1. On sign-in, the dashboard calls the proxy (`/api/pr`, `/api/po`) for **live** D365 data — amounts, status, departments, vendors, dates — and auto-refreshes every 3 minutes.
2. The **Step name / step date / pending approver / department-location-contract** come from `pr_steps.json` (generated from the latest D365 PR export), because the workflow "Step name" is a stored field not yet exposed on D365's live OData. The dashboard overlays these onto the live data by requisition number.

## Key files
- `index.html` — the entire dashboard (UI + data loading + charts).
- `pr_steps.json` — step lookup overlaid onto live data (PR → step, step date, approver, dept/loc/contract).
- `gen_pr_steps.py` — regenerates `pr_steps.json` from a fresh PR export: `python gen_pr_steps.py pr.xlsx`.
- `pr.xlsx` / `po.xlsx` — committed exports (fallback data + source for the step lookup).
- `msal-browser.min.js` — Microsoft sign-in library (self-hosted).
- `LIVE-INTEGRATION-PLAN.md` — background on the live integration.

## To edit / publish
Edit files (GitHub web pencil for small changes, or GitHub Desktop for full edits) → **Commit** → **Push**. GitHub Pages republishes automatically in ~1 minute.

## To refresh the workflow steps
Export the *All purchase requisitions* list from D365 → save as `pr.xlsx` → run `python gen_pr_steps.py pr.xlsx` → commit `pr_steps.json` → push.

## Retirement gate

Do not remove `pr.xlsx`, `po.xlsx`, `pr_steps.json` or their jobs until a fresh reconciliation passes every cutover threshold. The Sourcing, ex-VAT amount and PO lifecycle rules are settled; no further business decision is pending. No F&O development is assumed or requested.
