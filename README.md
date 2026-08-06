# PR / PO Pipeline Dashboard

Live dashboard for Strive Services Group showing the purchase requisition (PR) and purchase order (PO) pipeline from D365 Finance & Operations.

**Live site:** https://chandansah605.github.io/PR-PO-Pipeline-Dashboard/ (sign in with your Microsoft work account)

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

## Pending improvement (makes steps fully live, no exports)
Have the F&O developer expose the `IFAHR*` fields (esp. `IFAHRPendingStep`) on the OData entity. Once done, the dashboard reads the step live and `pr_steps.json` is no longer needed.
