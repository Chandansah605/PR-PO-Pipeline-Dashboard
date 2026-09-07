'use strict';

const assert = require('node:assert/strict');
const live = require('../dataverse-live.js');

assert.deepEqual(
  live.parseLedgerDimension('-Contracted--Building Services--THE8-Materials-Threshold-'),
  { contract: 'Contracted', department: 'Building Services', location: 'THE8' }
);

const prRows = live.mapPRRows(
  [{
    mserp_requisitionnumber: 'PR-TEST',
    mserp_requisitionname: 'Test requisition',
    mserp_requisitionstatus: 200000002,
    'mserp_requisitionstatus@OData.Community.Display.V1.FormattedValue': 'In review',
    mserp_requisitionpurpose: 200000000,
    'mserp_requisitionpurpose@OData.Community.Display.V1.FormattedValue': 'Consumption',
    mserp_defaultaccountingdate: '2026-09-04T00:00:00Z'
  }],
  [
    { mserp_requisitionnumber: 'PR-TEST', mserp_lineamount: 10, mserp_defaultledgerdimensiondisplayvalue: '-Contracted--Building Services--THE8-Materials-' },
    { mserp_requisitionnumber: 'PR-TEST', mserp_lineamount: 5 }
  ],
  [{
    mserp_requisitionnumber: 'PR-TEST',
    mserp_workflowelementid: 'GUID-LIVE',
    mserp_approvaluser: 'live.user',
    mserp_workitemrecid_bigint: 2
  }],
  {
    stepMap: { 'guid-live': 'Wrong historical step' },
    workflowLookup: {
      'PR-TEST': { step: 'PurchReqReviewTask', stepDate: '2026-09-05T10:00:00', pendingUser: 'current.user' }
    }
  }
);

assert.equal(prRows[0]['Status'], 'In review');
assert.equal(prRows[0]['Total amount'], 15);
assert.equal(prRows[0]['Department'], 'Building Services');
assert.equal(prRows[0]['Location'], 'THE8');
assert.equal(prRows[0]['Contract'], 'Contracted');
assert.equal(prRows[0]['Step name'], 'PurchReqReviewTask');
assert.equal(prRows[0]['Step date and time'], '2026-09-05T10:00:00');
assert.equal(prRows[0]['Pending Approver/User'], 'current.user');
assert.equal(prRows[0]._workflowGuarded, true);

const poRows = live.mapPORows(
  [{
    mserp_purchaseordernumber: 'SCBM-PO-TEST',
    mserp_purchaseordername: 'Vendor Name',
    mserp_documentapprovalstatus: 200000006,
    'mserp_documentapprovalstatus@OData.Community.Display.V1.FormattedValue': 'Confirmed',
    mserp_purchaseorderstatus: 200000002,
    'mserp_purchaseorderstatus@OData.Community.Display.V1.FormattedValue': 'Received',
    mserp_accountingdate: '2026-09-04T00:00:00Z',
    mserp_currencycode: 'AED'
  }],
  [{
    mserp_purchaseordernumber: 'SCBM-PO-TEST',
    mserp_lineamount: 99.25,
    mserp_defaultledgerdimensiondisplayvalue: '-Variation--FitOut Services--NORTH RESIDENCE-Materials-',
    mserp_purchaserequisitionid: 'CPR-123456'
  }],
  [],
  {}
);

assert.equal(poRows[0]['Purchase requisition'], 'CPR-123456');
assert.equal(poRows[0]['Vendor name'], 'Vendor Name');
assert.equal(poRows[0]['Total amount'], 99.25);
assert.equal(poRows[0]['Department'], 'FitOut Services');
assert.equal(poRows[0]['Location'], 'NORTH RESIDENCE');
assert.equal(poRows[0]['Contract'], 'Variation');
assert.equal(poRows[0]['Step name'], 'LPO sent/shared with supplier');

const duplicatePOs = live.mapPORows(
  [
    { mserp_purchaseordernumber: 'P0000000008', mserp_dataareaid: 'scbm', mserp_ordervendoraccountnumber: 'VEND-1', mserp_purchaseordername: 'Vendor One', 'mserp_documentapprovalstatus@OData.Community.Display.V1.FormattedValue': 'Confirmed', 'mserp_purchaseorderstatus@OData.Community.Display.V1.FormattedValue': 'Received' },
    { mserp_purchaseordernumber: 'P0000000008', mserp_dataareaid: 'rsrs', mserp_ordervendoraccountnumber: 'VEND-2', mserp_purchaseordername: 'Vendor Two', 'mserp_documentapprovalstatus@OData.Community.Display.V1.FormattedValue': 'Confirmed', 'mserp_purchaseorderstatus@OData.Community.Display.V1.FormattedValue': 'Received' }
  ],
  [
    { mserp_purchaseordernumber: 'P0000000008', mserp_dataareaid: 'scbm', mserp_lineamount: 100 },
    { mserp_purchaseordernumber: 'P0000000008', mserp_dataareaid: 'rsrs', mserp_lineamount: 200 }
  ],
  [],
  { workflowLookup: { 'P0000000008|vend-1': { step: 'Accounting Manager', stepDate: '2026-09-04T10:00:00' } } }
);

assert.equal(duplicatePOs[0]['Total amount'], 100);
assert.equal(duplicatePOs[0]['Step name'], 'Accounting Manager');
assert.equal(duplicatePOs[1]['Total amount'], 200);
assert.equal(duplicatePOs[1]['Step name'], 'LPO sent/shared with supplier');

assert.equal(
  live.newestDataDate(prRows, poRows).getTime(),
  new Date('2026-09-05T10:00:00').getTime()
);
assert.equal(
  live.workingDaysOld(new Date('2026-09-04T12:00:00Z'), new Date('2026-09-08T12:00:00Z')),
  2
);

assert.match(live.PATHS.prHeaders, /^mserp_purchaserequisitionheaderv2entities\?/);
assert.match(live.PATHS.poHeaders, /^mserp_purchpurchaseorderheaderv2entities\?/);
assert.match(live.PATHS.prApprovals, /^mserp_purchreqapprovalheaderentities\?/);
assert.match(live.PATHS.poApprovals, /^mserp_purchapprovalheaderentities\?/);

console.log('Dataverse live data tests passed');
