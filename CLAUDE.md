# Repository source of truth

This is a static PR / PO dashboard. Preserve the existing PR and PO tabs, MSAL wiring, and `fetch_from_onedrive.py` semantics unless a task explicitly changes them. Never write to Dataverse or D365 from this repository.

## Journey Board data contract

`gen_journey_board.py` is the single calculation source for `journey_board.json`. The Analysis tab renders `journey-board.html`; the browser must not parse XLSX files to calculate Journey Board figures.

- Window: PR `Created date >= 2026-04-01`. Exclude PR status `Cancelled` and `Rejected` case-insensitively.
- Journey grain: one exact PR–PO pair joined by PO `Purchase requisition`.
- Terminal PO: status `Received` or `Invoiced`, or PO step contains `LPO sent` / `shared with supplier`, case-insensitively. Use the earliest qualifying terminal step timestamp for duplicate rows of the same exact PR–PO pair. Reject missing or chronologically invalid milestone sequences.
- Type: `CPR-` means non-contracted revenue created from a CRM quote; `PR-` means contracted / back-office created in F&O. The prefix is CPR, never CRP.
- Divisions by PR Department:
  - Facilities Management: Building Services, Concierge Services, Leisure Services, Security Services, Landscaping Services, Contracted Cleaning Services.
  - Home Services: Home Maintenance Services, Housekeeping Services, Laundry.
  - FitOut Solutions: FitOut Services, Surveying Services.
  - Factory — Head Office: all other values and blanks.
- Durations: working days, Monday–Friday, with `numpy.busday_count` boundary semantics.
- Cumulative milestones from PR Raised: Submitted, PO Created, LPO Sent. Sector legs are differences between the cumulative medians.
- Targets: PR Raised to Goods Received is 10 WD; Goods to Supplier Invoice is at most 2 days. The export has neither timestamp, so both remain ghost milestones. The measured headline is explicitly to LPO Sent as proxy.
- Trend: completed journeys by ISO week of terminal date, median end-to-end WD, last eight full weeks plus current partial week.
- Live pipeline: eligible PRs not terminal, excluding Closed PRs with no PO. Age is working days from Created to the source as-of date; yesterday deltas are reconstructed from the same timestamps.
- Queues: Status `In review`; gate mapping is PurchReqReview → PR Review, RFQ/inquiry → RFQ to Suppliers, quotation received → Quotation Received, operations sharing/confirmation → Ops Confirmation, unit prices → Prices Updated, otherwise Mgmt Approvals. Holder is Pending Approver/User. Dwell is calendar days since PR step timestamp, clamped to zero.
- SLA colours: green `<=3`, amber `<=10`, red `>10` (working days for journey sectors; calendar days for queues).
- Legacy card: keep the approved 831-record corrective text. Do not backfill legacy records in this repository.
- Page 1 circuits: HS · CPR, Factory · PR, FM · PR, FitOut · CPR, FM · CPR. Do not add a Factory · CPR circuit.

Run `python gen_journey_board.py --out journey_board.json --sync-index index.html` after either workbook changes. Run `node tests/journey-board.test.js` and `python tests/reconcile_journey_board.py` before publishing.
