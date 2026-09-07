# PR/PO reporting change note — draft, not approved for issue

Status: **Blocked. Do not publish or forward yet.** Correction 02 passes the PR stage, PR procurement clock and both amount gates for the dashboard population, but PO stage is only 44.02% against its 95% gate. Production remains unchanged.

## Exact bucket changes

| Current dashboard/email bucket | Proposed live bucket |
|---|---|
| PR In Review | Sourcing |
| RFQ to suppliers | Sourcing |
| Qt received & Logged | Sourcing |
| Qt Shared to Op | Sourcing |
| OP confirms material | Sourcing |
| Unit Price Updated | Priced — awaiting approval |
| Sent to Supplier | Sent to supplier |
| Pending Invoicing | Receipt posted or Invoiced, from the live event |

Approval stages remain Procurement, Dep Managers, Finance, Director and CEO. Any approval element without an unambiguous versioned mapping is shown as `Approval — unmapped element` and flagged for data quality.

## What Sourcing contains

`Sourcing` means **with Procurement, lines not yet priced**. It includes the former PR review, supplier inquiry/RFQ, quotation receipt and logging, quotation sharing to Operations, and Operations material or scope confirmation stages. These stages become one because the exposed live system does not distinguish them. `Priced — awaiting approval` means every active PR line has a positive purchase price.

## Amount basis

Every dashboard and email amount will use live F&O line values **excl. VAT**. Familiar totals will normally read about 5% lower because the old workbook values included 5% VAT. The new reporting will not gross amounts up. Every displayed amount must carry the label `excl. VAT`.

## PO stages

- **Sent to supplier** — the PO is confirmed or sent.
- **Receipt posted** — a packing slip has been posted.
- **Invoiced** — the purchase order is invoiced where that status is exposed.

`Posted on` is the packing-slip document date. It is a receipt-posting date, never a delivery date.

## What each clock means

- **Assigned since** — the earliest captured assignment for the current approval stage.
- **Observed in stage since** — the preserved first observation of Sourcing or Priced. The F&O header modified time only seeds records already open at cutover.
- **Posted on** — the packing-slip document date for Receipt posted.

The dataset time is the oldest required source timestamp. The screen shows `Dataset generated`, `F&O read` and `Approval capture reconciled` separately in Dubai time, while the dataset stores UTC. Cached means an earlier Dataverse-derived dataset, never workbook data.

## Forwardable paragraph — hold until every gate passes

PR/PO reporting will move from emailed workbooks to automatically refreshed Dataverse data. PR review, supplier inquiry, quotation logging, quotation sharing and Operations confirmation will appear together as Sourcing, meaning with Procurement and not yet priced. Priced — awaiting approval will mean every active PR line has a positive purchase price. All amounts will come from live F&O lines and will be labelled excl. VAT, so familiar totals will normally be about 5% lower than the VAT-inclusive workbook totals. PO reporting will follow live events from Sent to supplier to Receipt posted and then Invoiced. Approval clocks will use captured assignment times, procurement clocks will use the preserved first observation in the stage, and Posted on will be the packing-slip posting date, never a delivery date. The dashboard and daily emails will use the same dated dataset and will show unresolved or unmapped workflow items separately instead of guessing.

This paragraph is not approved for issue until every retirement gate passes and the live cutover is verified.
