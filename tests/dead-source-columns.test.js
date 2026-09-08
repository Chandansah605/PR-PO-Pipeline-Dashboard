'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const displaySources = ['index.html', 'divisions.html', 'race-control.js'];
const deadOwnerOrMetricFields = [
  'Submission Status',
  'Accepted By/Assign To',
  'Request for quotation case',
  'Purchase type',
  'RFQ number',
  'Created by',
  'Created By'
];

for (const file of displaySources) {
  const source = fs.readFileSync(path.join(root, file), 'utf8');
  for (const field of deadOwnerOrMetricFields) {
    assert.equal(source.includes(field), false, `${file} still reads or names dead field ${field}`);
  }
}

// Preparer is the one formerly unusable field that now has an authorised,
// mapped use: routing NO_CURRENT_WORK_ITEM rows to a resolved employee name.
// It must not leak into another display or calculation path.
const indexSource = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
assert.equal((indexSource.match(/r\['Preparer'\]/g) || []).length, 1);
assert.match(indexSource, /holderMode==='preparer'\)holders=holderNames\(r\['Preparer'\]\)/);
for (const file of ['divisions.html', 'race-control.js']) {
  assert.equal(fs.readFileSync(path.join(root, file), 'utf8').includes('Preparer'), false);
}

const index = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const analysis = index.slice(index.indexOf('function renderAnalysis(){'), index.indexOf('function raceLiveRecords('));
assert.ok(analysis.includes('No quotation recorded'));
assert.ok(analysis.includes('Quotation referenced'));
assert.ok(analysis.includes('PR-to-PO conversion is withheld because lineage is incomplete.'));
assert.equal(analysis.includes('No RFQ issued'), false);
assert.equal(analysis.includes('RFQ issued'), false);
assert.equal(analysis.includes('PO created'), false);

console.log('Dead source column display tests passed');
