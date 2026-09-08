"""Live-stage to final legacy-workbook Step name translation.

The generated workbooks are outputs for Chandan's frozen email function only.
They are not reporting inputs.  `legacy_bucket` names are the buckets produced
by commit 73fef6a of pr-po-proxy.
"""

# PR holder and compatibility-step routing has one source of truth in
# holder-rule.json. It is loaded by the generator and mirrored in the pages;
# tests fail if those copies drift.

# PO translation table. Receipt posted deliberately writes the legacy LPO-sent
# label: the frozen code then uses Confirmed + Received to route it to Pending
# Invoicing. Approval-unmapped has no exact label, so the documented fallback
# keeps the displayed order in the legacy Procurement queue.
PO_STAGE_RULES = {
    "Not yet sent": {
        "workbook_step": "Procurement Manager",
        "legacy_bucket": "Procurement",
        "exact_equivalent": False,
    },
    "Procurement": {
        "workbook_step": "Procurement Manager",
        "legacy_bucket": "Procurement",
        "exact_equivalent": True,
    },
    "Finance": {
        "workbook_step": "Accounting Manager",
        "legacy_bucket": "Finance",
        "exact_equivalent": True,
    },
    "Director": {
        "workbook_step": "Finance and Accounts Director",
        "legacy_bucket": "Director",
        "exact_equivalent": True,
    },
    "CEO": {
        "workbook_step": "CEO",
        "legacy_bucket": "CEO",
        "exact_equivalent": True,
    },
    "Approval — unmapped element": {
        "workbook_step": "Procurement Manager",
        "legacy_bucket": "Procurement",
        "exact_equivalent": False,
    },
    "Sent to supplier": {
        "workbook_step": "LPO sent/shared with supplier",
        "legacy_bucket": "Sent to Supplier",
        "exact_equivalent": True,
    },
    "Receipt posted": {
        "workbook_step": "LPO sent/shared with supplier",
        "legacy_bucket": "Pending Invoicing",
        "exact_equivalent": False,
        "approval_status_override": "Confirmed",
        "purchase_order_status_override": "Received",
    },
}

# Complete live-stage list with no old exact equivalent. Rows excluded by the
# dashboard remain excluded; an open STAGE_NOT_EVIDENCED row fails generation.
NO_EXACT_OLD_EQUIVALENT = {
    "PR": {
        "Sourcing": "consolidated live stage; mapped to legacy Procurement",
        "Priced — awaiting approval": "live priced signal; mapped to legacy Operations to Confirm",
        "Approval — unmapped element": "shown as Step not reported by F&O",
        "(blank)": "shown as Step not reported by F&O",
    },
    "PO": {
        "Not yet sent": "authoritative F&O state; mapped to legacy Procurement",
        "Approval — unmapped element": "displayed fallback; mapped to legacy Procurement",
        "Receipt posted": "routed by Confirmed plus Received to Pending Invoicing",
        "Invoiced": "excluded by the open-pipeline rule",
        "STAGE_NOT_EVIDENCED": "must never be open; generation fails if it is",
    },
}
