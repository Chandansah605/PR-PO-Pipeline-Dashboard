'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const [datasetPath, proxyRepo, evidencePath, previewPath] = process.argv.slice(2);
if (!datasetPath || !proxyRepo || !evidencePath || !previewPath) {
  throw new Error('usage: node reconcile_email_meaning.js <dataset.json> <proxy-repo> <evidence.json> <preview.html>');
}

const email = require(path.join(proxyRepo, 'src/functions/prpoEmail.js'));
const dataset = JSON.parse(fs.readFileSync(datasetPath, 'utf8'));
const state = JSON.parse(fs.readFileSync('legacy-email-workbook-state.json', 'utf8'));
assert.equal(state.datasetRevision, dataset.revision, 'workbooks were not built from the saved live revision');

const prRows = email.parseXlsx(fs.readFileSync('pr.xlsx'));
const poRows = email.parseXlsx(fs.readFileSync('po.xlsx'));
const items = email.applyDeliveryPolicy(email.buildItems(prRows, poRows));
const people = email.groupByOwner(email.personalPool(items));
const adnan = people.find(person => person.key === 'adnan.ullah');
assert.ok(adnan, 'Adnan has no rendered queue');
const rendered = email.buildPersonal(adnan, {});
fs.writeFileSync(previewPath, rendered.html, 'utf8');

assert.equal(rendered.count, rendered.pricingQueueCount + rendered.pricedCount + rendered.unvaluedOutsidePricing);
assert.doesNotMatch(rendered.html, /totalling/i);
assert.doesNotMatch(rendered.html, /oldest has been waiting/i);
assert.doesNotMatch(rendered.html, /Layusha\.cleatus/i);
assert.ok(rendered.fil.every(item => item.doc !== 'PR' || item.clockBasis === 'raised' || item.clockBasis === 'current step'));
assert.ok(rendered.fil.every(item => !item.sourceShared || item.sharedLabel.startsWith('Shared')));

const html = fs.readFileSync('index.html', 'utf8');
const start = html.indexOf('const PR_DATA = []');
const end = html.indexOf('let _t=null;');
const context = vm.createContext({ console, window: {}, setTimeout, clearTimeout, addEventListener() {} });
vm.runInContext(html.slice(start, end), context, { filename: 'index-dashboard-core.js' });
context.__rows = dataset.pr.rows;
const dashboard = vm.runInContext('buildPRRecords(__rows)', context).filter(row => row._isOpenPipeline);
assert.ok(dashboard.every(row => row.ageLabel && row.ageBandLabel));
assert.ok(dashboard.every(row => row.sharedLabel));
assert.match(html, /Recorded price/);
assert.match(html, /Shared buyers/);

const opsSource = dashboard.filter(row => row.classCode === 'ACTIVE_LINES_PRICED');
const opsEmail = items.filter(item => item.doc === 'PR' && item.workClassCode === 'ACTIVE_LINES_PRICED');
const opsEmailByDocument = new Map(opsEmail.map(item => [String(item.ref).toUpperCase(), item]));
assert.equal(opsEmailByDocument.size, opsSource.length);
const opsDashboardValue = Number(opsSource.reduce((sum, row) => sum + row.amount, 0).toFixed(2));
const opsEmailValue = Number([...opsEmailByDocument.values()].reduce((sum, item) => sum + item.value, 0).toFixed(2));
assert.equal(opsEmailValue, opsDashboardValue, 'operations-confirm priced value changed');

const proof = {
  provedAt: new Date().toISOString(),
  datasetRevision: dataset.revision,
  datasetGeneratedAt: dataset.generatedAt,
  workbookRows: { pr: prRows.length, po: poRows.length },
  adnan: {
    count: rendered.count,
    pricingQueueCount: rendered.pricingQueueCount,
    pricedCount: rendered.pricedCount,
    unvaluedOutsidePricing: rendered.unvaluedOutsidePricing,
    pricedValueExVat: rendered.value,
    sourceSharedCount: rendered.sourceSharedCount,
    sharedWithOtherActiveBuyers: rendered.sharedWithOtherActiveBuyers,
    headerLines: [rendered.priceSummaryText + '.', rendered.oldestSummaryText, rendered.sharedSummaryText],
    sections: rendered.sections
  },
  operationsConfirmation: {
    documentsDashboard: opsSource.length,
    documentsEmail: opsEmailByDocument.size,
    pricedValueDashboardExVat: opsDashboardValue,
    pricedValueEmailExVat: opsEmailValue
  },
  dashboard: {
    actionableDocuments: dashboard.length,
    sourceLabelledAgeRows: dashboard.filter(row => row.ageLabel && row.ageBandLabel).length,
    sourceSharedDocuments: dashboard.filter(row => row.sourceShared).length
  },
  sendsPerformed: 0
};
fs.writeFileSync(evidencePath, JSON.stringify(proof, null, 2) + '\n', 'utf8');
process.stdout.write(JSON.stringify(proof, null, 2) + '\n');
