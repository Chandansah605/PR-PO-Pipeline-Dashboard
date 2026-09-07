# Legacy email workbook bridge

`pr.xlsx` and `po.xlsx` are generated outputs for Chandan's frozen email app. They are not dashboard, Race Control, current-email or weekly-snapshot inputs. Delete them and this bridge when sending moves to `ssg-prpo-proxy`.

## PR stage translation

| Live stage | Workbook `Step name` | Frozen email bucket | Exact old equivalent |
|---|---|---|---|
| Review | `PurchReqReviewTask` | Procurement | Yes |
| Sourcing | `Procurement sends inquiry/RFQ to suppliers` | Procurement | No; live consolidation |
| Priced — awaiting approval | `Quotation received and logged/attached` | Procurement | No; live consolidation |
| Dep Managers | Department-specific accepted manager label | Dep Managers | Yes |
| Finance | `Finance & Accounts_Accounting Manager` | Finance | Yes |
| Director | `Facilities Management_Director` | Director | Yes |
| CEO | `Executive Management_CEO` | CEO | Yes |

Open PR rows with blank or `Approval — unmapped element` stages are not displayed by the dashboard and are excluded. They have no old equivalent. The generator reports their counts instead of silently dropping them.

## PO stage translation

| Live stage | Workbook `Step name` | Frozen email bucket | Exact old equivalent |
|---|---|---|---|
| Not yet sent | `Procurement Manager` | Procurement | No; authoritative F&O state |
| Procurement | `Procurement Manager` | Procurement | Yes |
| Finance | `Accounting Manager` | Finance | Yes |
| Director | `Finance and Accounts Director` | Director | Yes |
| CEO | `CEO` | CEO | Yes |
| Approval — unmapped element | `Procurement Manager` | Procurement | No; displayed fallback |
| Sent to supplier | `LPO sent/shared with supplier` | Sent to Supplier | Yes |
| Receipt posted | `LPO sent/shared with supplier` plus compatibility `Confirmed / Received` | Pending Invoicing | No; frozen rule uses status |

`Invoiced` is excluded by the open-pipeline rule. `STAGE_NOT_EVIDENCED` has no old equivalent and generation fails if one is open. Cancelled and closed orders are excluded. A Receipt-posted compatibility row does not change F&O: it only expresses the authoritative posted-receipt stage in the vocabulary the frozen reader understands.

## Values and clocks

- `Total amount` is the settled live active-line value excl. VAT.
- `Step date and time` is the live event or final-workbook seed.
- `NOT_RECORDED` is blank. The generator never invents a date.
