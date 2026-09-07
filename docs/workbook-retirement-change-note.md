# PR/PO reporting change note — draft, not approved for issue

Status: **Blocked. Do not publish or forward yet.** The live evidence cannot separate `PR in review` from `Sourcing`. Waqas must decide that reporting rule before this note can become final.

## Proposed bucket names

| Exact current display/source label | Proposed live label |
|---|---|
| PR In Review | PR in review — blocked pending separability decision |
| RFQ to suppliers | Sourcing |
| Qt received & Logged | Sourcing |
| Qt Shared to Op | Sourcing |
| OP confirms material | Sourcing |
| Unit Price Updated | Priced — awaiting approval |
| Department manager names | Dep Managers |
| Finance & Accounts_Accounting Manager | Finance |
| Facilities Management_Director / Commercial_Director | Director |
| Executive Management_CEO | CEO |
| Advance payment request submitted / Procurement Manager | Procurement |
| Accounting Manager | Finance |
| Finance and Accounts Director | Director |
| LPO sent/shared with supplier, before receipt | Sent to Supplier |
| Posted packing slip | Receipt posted |

## What Sourcing contains

`Sourcing` combines supplier inquiry/RFQ, quotation receipt/logging, quotation sharing to Operations and Operations material/scope confirmation. Those four sub-steps are removed because no exposed live source distinguishes them. The live sources can tell whether all active lines have a positive purchase price, which separates `Priced — awaiting approval` from the unpriced population. They cannot currently tell whether an unpriced document is still `PR in review` or has entered `Sourcing` when both use the same workflow element.

## What each clock means

- **Assigned since** — the earliest captured assignment for the current approval stage. Several active approvals in one stage use the earliest assignment.
- **Observed in stage since** — the preserved first observation of a procurement stage. At initial cutover only, the F&O header modified time seeds records already open; it is not claimed as the exact stage-change time.
- **Posted on** — the packing-slip document date. It is a receipt-posting date, never a promised or actual delivery date.

The dataset time must be the oldest required source timestamp. The screen must show `Dataset generated`, `F&O read` and `Approval capture reconciled` separately in Dubai time, while the dataset stores UTC. A cached value means an earlier Dataverse-derived dataset, never workbook data.

## Forwardable paragraph — hold until the blocker is decided

PR/PO reporting will move from emailed workbooks to automatically refreshed Dataverse data. Supplier inquiry, quotation logging, quotation sharing and Operations confirmation will be reported together as Sourcing because the live system does not expose those sub-steps separately. Priced — awaiting approval will mean every active PR line has a positive purchase price. Approval clocks will start from the captured assignment, procurement clocks will use the preserved first time observed in that stage, and receipt posted will use the packing-slip posting date, not a delivery date. The dashboard and daily emails will use the same dated dataset and will show unresolved or unmapped workflow items separately instead of guessing.

This paragraph is not approved for issue until the `PR in review` versus `Sourcing` rule is decided and the failed reconciliation gate is rerun.
