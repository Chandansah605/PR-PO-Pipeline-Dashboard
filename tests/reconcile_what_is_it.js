'use strict';

const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const [datasetPath, proxyRepo, evidencePath, htmlPath] = process.argv.slice(2);
if (!datasetPath || !proxyRepo || !evidencePath || !htmlPath) {
  throw new Error('usage: node reconcile_what_is_it.js <dataset.json> <proxy-repo> <evidence.json> <email.html>');
}

const email = require(path.join(proxyRepo, 'src/functions/prpoEmail.js'));
const dataset = JSON.parse(fs.readFileSync(datasetPath, 'utf8'));
const html = fs.readFileSync('index.html', 'utf8');
const start = html.indexOf('const PR_DATA = []');
const end = html.indexOf('let _t=null;');
assert.ok(start >= 0 && end > start, 'dashboard core markers not found');
const context = vm.createContext({ console, window: {}, setTimeout, clearTimeout, addEventListener() {} });
vm.runInContext(html.slice(start, end), context, { filename: 'index-dashboard-core.js' });
context.__rows = dataset.pr.rows;
const dashboardRecords = vm.runInContext('buildPRRecords(__rows)', context).filter(row => row._isOpenPipeline);
context.__poRows = dataset.po.rows;
const dashboardPoRecords = vm.runInContext('buildPORecords(__poRows)', context)
  .filter(row => !row._isUnmapped && !row._isPORejected && !row._isPOCanceled && !row._isInvoiced);
const mainColumns = vm.runInContext("mode='PR'; getMainColumns()", context);
const drillColumns = vm.runInContext('getDrillColumns()', context);
assert.ok(html.includes('id="filterClass"'), 'dashboard class filter is missing');
assert.ok(mainColumns.includes('Class of work') && mainColumns.includes('Age band'), 'main PR columns are incomplete');
assert.ok(drillColumns.includes('Class of work') && drillColumns.includes('Age band'), 'drill PR columns are incomplete');

const baselineHtml = execFileSync('git', ['show', 'HEAD:index.html'], { encoding: 'utf8' });
const baselineStart = baselineHtml.indexOf('const PR_DATA = []');
const baselineEnd = baselineHtml.indexOf('let _t=null;');
assert.ok(baselineStart >= 0 && baselineEnd > baselineStart, 'baseline dashboard core markers not found');
const baselineContext = vm.createContext({ console, window: {}, setTimeout, clearTimeout, addEventListener() {} });
vm.runInContext(baselineHtml.slice(baselineStart, baselineEnd), baselineContext, { filename: 'baseline-index-dashboard-core.js' });
baselineContext.__rows = dataset.pr.rows;
baselineContext.__poRows = dataset.po.rows;
const baselinePrRecords = vm.runInContext('buildPRRecords(__rows)', baselineContext)
  .filter(row => row._isOpenPipeline);
const baselinePoRecords = vm.runInContext('buildPORecords(__poRows)', baselineContext)
  .filter(row => !row._isUnmapped && !row._isPORejected && !row._isPOCanceled && !row._isInvoiced);

function recordSummary(rows) {
  return {
    documents: rows.length,
    amount: Number(rows.reduce((sum, row) => sum + (Number(row.amount) || 0), 0).toFixed(2)),
    stages: counts(rows, row => row.hdrBucket || row.bucket || 'Not reported')
  };
}

const regression = {
  prBaseline: recordSummary(baselinePrRecords),
  prCurrent: recordSummary(dashboardRecords),
  poBaseline: recordSummary(baselinePoRecords),
  poCurrent: recordSummary(dashboardPoRecords)
};
assert.equal(regression.prCurrent.documents, regression.prBaseline.documents, 'PR headline count changed');
assert.equal(regression.prCurrent.amount, regression.prBaseline.amount, 'PR headline amount changed');
assert.deepEqual(regression.poCurrent, regression.poBaseline, 'purchase-order figures changed');

const prRows = email.parseXlsx(fs.readFileSync('pr.xlsx'));
const poRows = email.parseXlsx(fs.readFileSync('po.xlsx'));
const emailItems = email.buildItems(prRows, poRows);
const emailPr = emailItems.filter(item => item.doc === 'PR');
const expectedAttributions = dashboardRecords.reduce((sum, row) => sum + row.holders.length, 0);
assert.equal(prRows.length, expectedAttributions, 'workbook attribution rows do not match dashboard holders');

function counts(rows, keyFn, uniqueFn) {
  const out = {};
  const seen = new Set();
  for (const row of rows) {
    const unique = uniqueFn ? uniqueFn(row) : null;
    if (unique && seen.has(unique)) continue;
    if (unique) seen.add(unique);
    const key = keyFn(row);
    out[key] = (out[key] || 0) + 1;
  }
  return Object.fromEntries(Object.entries(out).sort());
}

const dashboardClassCounts = counts(dashboardRecords, row => row.classCode);
const emailClassCounts = counts(emailPr, item => item.workClassCode, item => `${item.ref}|${item.workClassCode}`);
assert.deepEqual(emailClassCounts, dashboardClassCounts, 'dashboard and email class counts differ');
assert.equal(dashboardRecords.length, 979, 'live actionable count changed unexpectedly inside one saved revision');
assert.ok(dashboardRecords.every(row => row.workClass && row.workAction && row.ageBand), 'dashboard has an unclassified item');
assert.ok(emailPr.every(item => item.workClass && item.workAction && item.ageBand), 'email has an unclassified item');

const dashboardHolderCounts = {};
for (const row of dashboardRecords) {
  for (const holder of row.holders) {
    const key = String(holder).trim().toLowerCase();
    if (!key || key === 'not recorded' || key.startsWith('no named owner') || key.startsWith('employee number ')) continue;
    dashboardHolderCounts[key] = (dashboardHolderCounts[key] || 0) + 1;
  }
}
const people = email.groupByOwner(email.personalPool(emailItems));
const emailHolderCounts = Object.fromEntries(people.map(person => [person.key, person.items.filter(item => item.doc === 'PR').length]));
const comparedHolders = ['dinesh.laxman', 'adnan.ullah', 'roderick.red', 'layusha.cleatus', 'aparna.pauly'];
const holderComparison = {};
const procurementClassHolderComparison = {};
for (const holder of comparedHolders) {
  holderComparison[holder] = { dashboard: dashboardHolderCounts[holder] || 0, email: emailHolderCounts[holder] || 0 };
  assert.equal(holderComparison[holder].email, holderComparison[holder].dashboard, `holder mismatch: ${holder}`);
  const dashboardClass = dashboardRecords.filter(row => row.classCode === 'ACTIVE_LINES_NOT_FULLY_PRICED' && row.holders.some(name => String(name).toLowerCase() === holder)).length;
  const emailClass = emailPr.filter(item => item.workClassCode === 'ACTIVE_LINES_NOT_FULLY_PRICED' && String(item.owner).toLowerCase() === holder).length;
  procurementClassHolderComparison[holder] = { dashboard: dashboardClass, email: emailClass };
  assert.equal(emailClass, dashboardClass, `procurement-class holder mismatch: ${holder}`);
}

const largest = people.find(person => person.key === 'dinesh.laxman') || people[0];
const rendered = email.buildPersonal(largest, {});
for (const item of largest.items.filter(item => item.doc === 'PR')) {
  assert.ok(rendered.html.includes(String(item.ref)), `largest-holder email omitted ${item.ref}`);
}
fs.writeFileSync(htmlPath, rendered.html, 'utf8');
const noNamed = emailPr.filter(item => item.noNamedOwner);
const procurementDigest = email.buildDivision(email.DIVS.find(item => item.key === 'procurement'), emailItems, {});
assert.match(procurementDigest.html, /No named owner/);
assert.match(procurementDigest.html, new RegExp(`${new Set(noNamed.map(item => item.ref)).size} requisitions`));
const preparerRouted = dashboardRecords.filter(row => ['NO_CURRENT_WORK_ITEM', 'ZERO_ACTIVE_LINES'].includes(row.classCode));
const preparerResolution = {
  sourceDocuments: preparerRouted.length,
  namedPeople: preparerRouted.filter(row => row.holders.every(name => !String(name).startsWith('No named owner') && !String(name).startsWith('employee number ') && name !== 'not recorded')).length,
  systemAccounts: preparerRouted.filter(row => row.holders.some(name => String(name).startsWith('No named owner — D365CRM ADMIN') || String(name).startsWith('No named owner — IT DEPARTMENT'))).length,
  unresolvedNumbers: preparerRouted.filter(row => row.holders.some(name => String(name).startsWith('employee number '))).length
};
const proof = {
  provedAt: new Date().toISOString(),
  datasetRevision: dataset.revision,
  datasetGeneratedAt: dataset.generatedAt,
  liveActionableDocuments: dashboardRecords.length,
  workbookAttributionRows: prRows.length,
  senderParsedRows: prRows.length,
  senderSampleRow: {
    requisition: prRows[0]['Purchase requisition'],
    stageReasonCode: prRows[0]['Stage reason code'],
    holder: prRows[0]['Pending Approver/User']
  },
  classCounts: { dashboard: dashboardClassCounts, email: emailClassCounts },
  holderComparison,
  procurementClassHolderComparison,
  preparerResolution,
  largestHolder: {
    user: rendered.user,
    count: rendered.count,
    everyPrLineRendered: true,
    htmlBytes: Buffer.byteLength(rendered.html, 'utf8'),
    sections: rendered.sections
  },
  noNamedOwner: {
    documents: new Set(noNamed.map(item => item.ref)).size,
    procurementDigestEvidencePresent: true,
    departments: counts(noNamed, item => item.dept || 'Department not reported', item => item.ref),
    classCounts: counts(noNamed, item => item.workClassCode, item => item.ref)
  },
  attributionConvention: {
    headlineDocuments: dashboardRecords.length,
    holderAttributionRows: expectedAttributions,
    multiHolderDocuments: dashboardRecords.filter(row => row.holders.length > 1).length,
    extraAttributions: expectedAttributions - dashboardRecords.length
  },
  pendingSplit: counts(emailPr, item => item.stage === 'Operations to Confirm' ? (String(item.raw['Step name'] || '') === 'Unit prices updated in PR lines' ? 'Pending Client' : 'Pending Internal') : 'Not operations confirmation'),
  dashboardUi: { classFilter: true, mainColumns, drillColumns },
  regression,
  bareNumericDashboardHolders: dashboardRecords.flatMap(row => row.holders).filter(holder => /^\d+$/.test(String(holder).trim())).length,
  bareNumericWorkbookHolders: prRows.filter(row => /^\d+$/.test(String(row['Pending Approver/User'] || '').trim())).length,
  sendsPerformed: 0
};
fs.writeFileSync(evidencePath, JSON.stringify(proof, null, 2) + '\n', 'utf8');
process.stdout.write(JSON.stringify(proof, null, 2) + '\n');
