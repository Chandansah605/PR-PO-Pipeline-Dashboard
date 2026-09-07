"""Live-stage to final legacy-workbook Step name translation.

The generated workbooks are outputs for Chandan's frozen email function only.
They are not reporting inputs.  `legacy_bucket` names are the buckets produced
by commit 73fef6a of pr-po-proxy.
"""

# PR translation table. Sourcing and Priced have no exact old stage because
# the live model deliberately consolidated the old workflow labels. Their
# selected labels preserve the legacy Procurement and Operations queues.
PR_STAGE_RULES = {
    "Review": {
        "workbook_step": "PurchReqReviewTask",
        "legacy_bucket": "Procurement",
        "exact_equivalent": True,
    },
    "Sourcing": {
        "workbook_step": "Procurement sends inquiry/RFQ to suppliers",
        "legacy_bucket": "Procurement",
        "exact_equivalent": False,
    },
    "Priced — awaiting approval": {
        "workbook_step": "Quotation received and logged/attached",
        "legacy_bucket": "Procurement",
        "exact_equivalent": False,
    },
    "Dep Managers": {
        "workbook_step": "Building Services_Asst. Facility Managers 1",
        "legacy_bucket": "Dep Managers",
        "exact_equivalent": True,
    },
    "Finance": {
        "workbook_step": "Finance & Accounts_Accounting Manager",
        "legacy_bucket": "Finance",
        "exact_equivalent": True,
    },
    "Director": {
        "workbook_step": "Facilities Management_Director",
        "legacy_bucket": "Director",
        "exact_equivalent": True,
    },
    "CEO": {
        "workbook_step": "Executive Management_CEO",
        "legacy_bucket": "CEO",
        "exact_equivalent": True,
    },
}

# The old manager label varied by requisition department. These are all names
# accepted by Chandan's deployed PR_MAP and all resolve to Dep Managers.
PR_MANAGER_STEP_BY_DEPARTMENT = {
    "Building Services": "Building Services_Asst. Facility Managers 1",
    "Contracted Cleaning Services": "PAC Services_Manager",
    "Concierge Services": "Concierge Services_Manager",
    "Security Services": "Security Services_Manager",
    "Home Maintenance Services": "Home Services_Operations Manager",
    "FitOut Services": "Home Services_Operations Manager",
    "Landscaping Services": "Landscaping_Manager",
}

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
        "Priced — awaiting approval": "consolidated live stage; mapped to legacy Procurement",
        "Approval — unmapped element": "not displayed by the dashboard; excluded",
        "(blank)": "not displayed by the dashboard; excluded",
    },
    "PO": {
        "Not yet sent": "authoritative F&O state; mapped to legacy Procurement",
        "Approval — unmapped element": "displayed fallback; mapped to legacy Procurement",
        "Receipt posted": "routed by Confirmed plus Received to Pending Invoicing",
        "Invoiced": "excluded by the open-pipeline rule",
        "STAGE_NOT_EVIDENCED": "must never be open; generation fails if it is",
    },
}
