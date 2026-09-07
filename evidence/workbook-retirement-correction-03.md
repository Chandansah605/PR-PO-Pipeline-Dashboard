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

## Testing performed

- Python compile and machine-evidence assertions for P1–P5.
- Complete read-only PO reconciliation against both Dataverse organisations and the unchanged workbook.
- Existing dashboard JavaScript and weekly-snapshot regression tests.
- Desktop browser visual check and responsive-rule inspection of the unpublished change note.
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
