# PR/PO reporting change note — correction 04 cutover

Status: **Implemented.** PO stage and PO clock are now separate. P1a and P2 both pass at 100%; P1b is reported rather than used as a stage gate.

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

During the temporary legacy-sender bridge, `pr.xlsx` and `po.xlsx` also carry these settled live ex-VAT values. Recipient totals will therefore read about 5% lower than yesterday even though Chandan's unchanged sender still reads workbook-shaped outputs.

## PO stages

- **Sent to supplier** — the PO is confirmed or sent.
- **Receipt posted** — a packing slip has been posted.
- **Invoiced** — the purchase order is invoiced where that status is exposed.

The final workbook still shows **1,099 purchase orders** as merely `LPO sent` even though F&O shows them as `Receipt posted` or `Invoiced`. In the live view, an order that used to remain at `LPO sent` indefinitely advances when F&O records the posted packing slip or vendor invoice.

`Posted on` is the packing-slip document date. It is a receipt-posting date, never a delivery date.

## What each clock means

- **Assigned since** — the earliest captured assignment for the current approval stage.
- **Observed in stage since** — the preserved first observation of Sourcing or Priced. The F&O header modified time only seeds records already open at cutover.
- **Posted on** — the packing-slip document date for Receipt posted.
- **Since (from last export)** — the final workbook seeded the clock because F&O exposed the stage but no event time. It is never presented as a live event date.
- **Since — not recorded** — neither a live event nor a final-workbook time existed. No date is invented.

The dataset time is the oldest required source timestamp. The screen shows `Dataset generated`, `F&O read` and `Approval capture reconciled` separately in Dubai time, while the dataset stores UTC. Cached means an earlier Dataverse-derived dataset, never workbook data.

## Forwardable paragraph

PR/PO reporting now reads automatically refreshed F&O and approval-capture data instead of emailed workbooks. PR review, supplier inquiry, quotation logging, quotation sharing and Operations confirmation appear together as Sourcing, meaning with Procurement and not yet priced. Priced — awaiting approval means every active PR line has a positive purchase price. All amounts come from live F&O lines and are labelled excl. VAT. Purchase orders now move from Sent to supplier to Receipt posted and Invoiced; **1,099** orders that the final workbook still called merely sent were already received or invoiced in F&O. Some orders show **since (from last export)** until our own first-observed clock takes over. A posted packing-slip date is a posting date, never a delivery date. The dashboard and daily emails use the same dataset revision and show missing clocks rather than inventing dates.
